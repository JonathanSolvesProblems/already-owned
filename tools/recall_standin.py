"""Recall on my real library, with a local stand-in for the NAS: what the Skill's claim search finds.

No NAS is available in Round 1, so a small local vision model plays two parts the NAS plays:

1. The recognition index. Every photo captured before the loss is tagged once with object
   categories from a fixed list, the way UGREEN Photos indexes a library.
2. photo-agent's vision step. For each claimed item, the Skill's own route and caps are applied
   (one search per category; nine matching photos before the loss spread across their capture dates, or with
   STANDIN_SELECT=latest the rule of Skill 0.1.0, the eight latest plus the earliest),
   and each candidate is described with the C4b question: which of the listed items are visible,
   and which other durable items. Then the Skill's second pass looks again at the photos already
   returned, for the items still unproven.

Entries that do not name one object (boxes, bags, bedding, stored items) are never searched: the
Skill asks the owner to itemize them. The second route (text in a photo, receipt-date window) is not
run here, because the receipts are not part of this test.

Scoring is against results/pre-loss-photo-census.md, the hand count made before this test: an item
counts as proven when a photo the model cites is one the census lists for that item, or one opened at full
size and checked by eye (recorded in results/recall-standin-checks.csv). Nothing leaves this machine: the
model runs in Ollama, and only file names and item names are written out.

    py tools/recall_standin.py index      # tag every pre-loss photo (cached in tmp/recall/)
    py tools/recall_standin.py search     # run the claim search and score it
    py tools/recall_standin.py report     # both cap rules, first pass and continuing: results/recall-standin.md and .json
"""
import base64
import csv
import io
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
# The stand-in model was chosen before the run, on three photos whose contents the census records (one with
# none of the listed items, one with one, one with two of three): gemma3:4b named items that were not there,
# gemma4:e4b missed one, qwen3.5:4b answered all three correctly. All three are about four billion parameters.
MODEL = os.environ.get("STANDIN_MODEL", "qwen3.5:4b")
PAGES = int(os.environ.get("STANDIN_CONTINUE", "0"))  # continuations the owner asks for, per category
# The claim-search cap: "spread", nine photos spread across the capture dates (Skill 0.2.0), or "latest", the eight
# latest plus the earliest (Skill 0.1.0, the rule of the first run of this measurement).
SELECT = os.environ.get("STANDIN_SELECT", "spread")
WORK = ROOT / "tmp" / "recall" / MODEL.replace(":", "-")
LOSS = "2026-06-20T00:00"
LISTS = [ROOT / "tmp" / "census" / "photos.csv", ROOT / "tmp" / "census-phone" / "photos.csv"]

CATEGORIES = ["sofa", "armchair", "office or gaming chair", "table", "bed", "television", "computer monitor", "refrigerator",
              "washing machine", "clothes dryer", "lamp", "bookcase", "shelving unit", "cabinet", "dumbbell", "exercise equipment",
              "vacuum cleaner", "case or trunk", "box", "bag", "picture frame", "camera", "clothes iron", "fan", "desk"]

# The route the Skill takes for each line of my June claim: the category its search uses, or None for an
# entry that does not name one object (the Skill asks the owner to itemize it and never searches it).
ROUTE = {
    1: "sofa", 2: "television", 3: "office or gaming chair", 4: "armchair", 5: "bed", 6: "table", 7: "table", 8: "table",
    9: "exercise equipment", 10: "dumbbell", 11: None, 12: "bookcase", 13: "shelving unit", 14: "vacuum cleaner",
    15: "case or trunk", 16: "camera", 17: "shelving unit", 18: "lamp", 19: "refrigerator", 20: "washing machine",
    21: None, 22: None, 23: None, 24: "keyword", 25: "clothes iron", 26: "computer monitor", 27: "picture frame",
}
# "keyword": the Skill searches the library for the word itself; the stand-in index has no such word, so the item
# is reached only by the second pass over the photos already returned.
CENSUS_ROW = re.compile(r"\|\s*(\d+)\s*\|([^|]*)\|\s*(yes|no|plausible|likely)\s*\|([^|]*)\|([^|]*)\|")
FILE_NAME = re.compile(r"[\w-]+\.(?:jpe?g|png|heic)", re.I)


def img_b64(path, side=896):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im.thumbnail((side, side))
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def ask(prompt, path, tokens=300):
    body = {"model": MODEL, "prompt": prompt, "images": [img_b64(path)], "stream": False, "format": "json", "think": False,
            "options": {"temperature": 0, "num_predict": tokens}}
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(json.loads(r.read()).get("response") or "{}")


def photos_before_loss():
    seen, out = set(), []
    for lst in LISTS:
        with open(lst, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = (r.get("md5_64k") or r["path"], r.get("bytes"))
                if r["taken"] and r["taken"] < LOSS and key not in seen and r.get("cloud_only", "0") != "1":
                    seen.add(key)
                    out.append({"path": r["path"].replace("\\", "/"), "taken": r["taken"]})
    return out


def index():
    WORK.mkdir(parents=True, exist_ok=True)
    cache = WORK / "index.jsonl"
    done = {json.loads(line)["path"] for line in cache.open(encoding="utf-8")} if cache.exists() else set()
    todo = [p for p in photos_before_loss() if p["path"] not in done]
    print(f"{len(done)} indexed, {len(todo)} to go, model {MODEL}", flush=True)
    prompt = ("List the durable household objects clearly visible in this photo, using only these category names: "
              + ", ".join(CATEGORIES) + '. Answer as JSON: {"objects": [names]}. Use [] if none.')
    t0 = time.time()
    with cache.open("a", encoding="utf-8") as out:
        for n, p in enumerate(todo, 1):
            try:
                ans = ask(prompt, p["path"], tokens=120)
                cats = [c for c in ans.get("objects", []) if c in CATEGORIES]
                rec = {**p, "cats": cats}
            except Exception as e:  # unreadable file: kept as not processed, the way the Skill lists it
                rec = {**p, "cats": [], "error": str(e)[:120]}
            out.write(json.dumps(rec) + "\n")
            out.flush()
            if n % 50 == 0:
                print(f"{n}/{len(todo)} in {time.time() - t0:.0f}s", flush=True)
    print("index done", flush=True)


def census():
    """Item number -> (status, set of file names the census lists for it)."""
    text = (ROOT / "results" / "pre-loss-photo-census.md").read_text(encoding="utf-8")
    out = {}
    for line in text.splitlines():
        m = CENSUS_ROW.match(line)
        if m:
            out[int(m.group(1))] = (m.group(3), set(FILE_NAME.findall(m.group(4) + " " + m.group(5))))
    return out


def spread(hits, n=9):
    """n photos spread across the capture dates: the latest, the earliest and n - 2 at even steps between them."""
    if len(hits) <= n:
        return list(hits)
    return [hits[i] for i in sorted({round(i * (len(hits) - 1) / (n - 1)) for i in range(n)})]


def first_cut(hits):
    if SELECT == "latest":
        return hits[-8:] + ([hits[0]] if hits and hits[0] not in hits[-8:] else [])
    return spread(hits)


def search():
    idx = [json.loads(line) for line in (WORK / "index.jsonl").open(encoding="utf-8")]
    items = list(csv.DictReader((ROOT / "results" / "june-2026-items.csv").open(encoding="utf-8")))
    cen = census()
    checks_file = ROOT / "results" / "recall-standin-checks.csv"
    by_eye = {}
    if checks_file.exists():
        for r in csv.DictReader(checks_file.open(encoding="utf-8")):
            # yes, no, or unclear (the photo cannot settle it): unclear counts neither as proof nor as a wrong photo
            by_eye[(int(r["item"]), r["photo"])] = r["shows_item"].strip().lower()
    desc_cache = WORK / "describe.jsonl"
    cache = {}
    if desc_cache.exists():
        for line in desc_cache.open(encoding="utf-8"):
            r = json.loads(line)
            cache[(r["path"], r["items"])] = r["answer"]

    reads = [0]  # model reads this run would cost on the NAS, cached or not

    def describe(path, names):
        reads[0] += 1
        key = (path, " | ".join(names))
        if key not in cache:
            prompt = ("Say which of these household items are visible in this photo: " + "; ".join(names)
                      + ". Name any other durable household item clearly visible in it that is not on the list. "
                      'Do not substitute a similar item. Answer as JSON: {"visible": [items from the list], "other": [names]}.')
            try:
                cache[key] = ask(prompt, path)
            except Exception as e:
                cache[key] = {"error": str(e)[:120]}
            with desc_cache.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"path": path, "items": key[1], "answer": cache[key]}) + "\n")
        return cache[key]

    def seen(ans, item):
        # The model sometimes splits a listed name at its comma ("Leather reclining sofa", "3-seat (brown)"), so a
        # returned name counts when it is the item's name or the start of it, at least eight characters long.
        vis = ans.get("visible", []) if isinstance(ans, dict) else []
        it = item.strip().lower()
        for v in vis:
            v = v.strip().lower() if isinstance(v, str) else ""
            if v == it or (len(v) >= 8 and (it.startswith(v) or v.startswith(it))):
                return True
        return False

    name = {int(it["number"]): it["item"] for it in items}
    cited = {n: [] for n in name}
    returned = []
    # first route: one search per category, capped as the Skill version under test says (SELECT)
    for cat in sorted({c for c in ROUTE.values() if c and c != "keyword"}):
        wanted = [n for n, c in ROUTE.items() if c == cat]
        hits = sorted((p for p in idx if cat in p["cats"]), key=lambda p: p["taken"])
        for p in first_cut(hits):
            returned.append(p)
            ans = describe(p["path"], [name[n] for n in wanted])
            for n in wanted:
                if seen(ans, name[n]):
                    cited[n].append(p)
    # second pass: the photos already returned, for every searchable item still unproven
    pool = list({p["path"]: p for p in returned}.values())
    left = [n for n, c in ROUTE.items() if c and not cited[n]]
    for p in pool:
        if not left:
            break
        ans = describe(p["path"], [name[n] for n in left])
        for n in list(left):
            if seen(ans, name[n]):
                cited[n].append(p)
    # Continuing, as the Skill offers when more photos matched than were described: the owner has rejected every
    # photo shown for an item (here, the photos the census and the eye checks say do not show it) and asks to go on.
    # Each continuation goes on from where the last delegation stopped, up to PAGES times: with the "latest" cap the next
    # eight older matches; with the "spread" cap nine more spread across the matches not described yet.
    files_of = {n: cen.get(n, ("no", set()))[1] for n in name}

    def shown(n):
        return any(Path(p["path"]).name in files_of[n] or by_eye.get((n, Path(p["path"]).name)) == "yes" for p in cited[n])

    for cat in sorted({c for c in ROUTE.values() if c and c != "keyword"}):
        hits = sorted((p for p in idx if cat in p["cats"]), key=lambda p: p["taken"])
        done = {p["path"] for p in first_cut(hits)}
        for page in range(1, PAGES + 1):
            wanted = [n for n, c in ROUTE.items() if c == cat and not shown(n)]
            if SELECT == "latest":
                older = hits[max(0, len(hits) - 8 * (page + 1)):len(hits) - 8 * page]
                older = [p for p in older if p is not hits[0]]
            else:
                older = spread([p for p in hits if p["path"] not in done])
                done |= {p["path"] for p in older}
            if not wanted or not older:
                break
            for p in older:
                returned.append(p)
                ans = describe(p["path"], [name[n] for n in wanted])
                for n in wanted:
                    if seen(ans, name[n]):
                        cited[n].append(p)
    pool = list({p["path"]: p for p in returned}.values())
    # score
    rows, unchecked = [], []
    for n in sorted(name):
        status, files = cen.get(n, ("no", set()))
        photos = sorted({Path(p["path"]).name for p in cited[n]})
        good = [f for f in photos if f in files or by_eye.get((n, f)) == "yes"]
        bad = [f for f in photos if f not in good and by_eye.get((n, f)) == "no"]
        unclear = [f for f in photos if f not in good and by_eye.get((n, f)) == "unclear"]
        todo = [f for f in photos if f not in good and f not in bad and f not in unclear]
        unchecked += [(n, f) for f in todo]
        rows.append({"n": n, "item": name[n], "census": status, "route": ROUTE[n] or "owner to itemize",
                     "proven": bool(good), "good": good, "bad": bad, "unclear": unclear, "todo": todo})
    out = {"model": MODEL, "select": SELECT, "photos_indexed": len(idx), "describe_calls": len(cache), "rows": rows,
           "returned": sorted({Path(p["path"]).name for p in pool}), "described": len(pool), "model_reads": reads[0]}
    (WORK / f"result-{SELECT}-continue{PAGES}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    conf = [r for r in rows if r["census"] == "yes"]
    print(f"photos indexed {len(idx)}, descriptions {len(cache)}")
    print(f"confirmed by the census: {len(conf)}; searchable: {sum(1 for r in conf if r['route'] != 'owner to itemize')}; "
          f"proven with a checked photo: {sum(r['proven'] for r in conf)}")
    print(f"items not confirmed by the census but proven: {[r['n'] for r in rows if r['census'] != 'yes' and r['proven']]}")
    print(f"cited photos the census does not list and nobody has checked yet: {len(unchecked)}")
    for n, f in unchecked:
        print(f"  check: item {n} ({name[n]}) in {f}")
    return out


CAMERA_NAME = re.compile(r"^\d{8}_\d{6}(\(\d+\))?\.(jpe?g|heic|png)$", re.I)


def public(name):
    """A camera file name is a time stamp; a renamed file can carry words from an earlier claim, so it is not shown."""
    return name if CAMERA_NAME.match(name) else "a renamed photo"


def tally(res):
    rows = res["rows"]
    conf = [r for r in rows if r["census"] == "yes"]
    return {"model": res["model"], "photos": res["photos_indexed"], "descriptions": res["describe_calls"],
            "confirmed": len(conf), "searchable": sum(1 for r in conf if r["route"] != "owner to itemize"),
            "proven": sum(r["proven"] for r in conf),
            "proven_outside_census": [r["n"] for r in rows if r["census"] != "yes" and r["proven"]],
            "right_photos": sum(len(r["good"]) for r in rows), "wrong_photos": sum(len(r["bad"]) for r in rows),
            "unclear_photos": sum(len(r.get("unclear", [])) for r in rows), "unchecked": sum(len(r["todo"]) for r in rows),
            "photos_described": res.get("described"), "model_reads": res.get("model_reads")}


def causes(res, idx):
    """Why each searchable item the hand count found was not proven, worked out from the run itself."""
    cen = census()
    tags = {Path(p["path"]).name: set(p["cats"]) for p in idx}
    returned = set(res["returned"])
    out = {}
    for r in res["rows"]:
        if r["census"] != "yes" or r["proven"] or r["route"] == "owner to itemize":
            continue
        files = cen[r["n"]][1]
        if r["route"] == "keyword":
            why = "keyword"
        elif not files & set(tags):
            why = "not indexed"
        elif not any(r["route"] in tags[f] for f in files if f in tags):
            why = "recognition"
        elif not files & returned:
            why = "cap"
        elif r["bad"]:
            why = "wrong photo first"
        else:
            why = "description"
        out[r["n"]] = why
    return out


# How the report names an item in a sentence; the table keeps the claim's own wording.
SHORT = {1: "the sofa", 2: "the television", 3: "the gaming chair", 4: "the armchair", 5: "the bed frame",
         6: "the console and side tables", 7: "the coffee table", 8: "the hex side table", 9: "the power tower",
         10: "the dumbbells", 12: "the bookshelf", 13: "the storage shelving", 14: "the stick vacuum",
         15: "the road case", 16: "the camera rig", 17: "the chrome shelving", 18: "the floor lamps",
         19: "the mini-fridge", 20: "the washer and dryer", 24: "the boot dryer", 25: "the iron",
         26: "the monitor arm", 27: "the picture frames"}
RATED = {"likely": "rated only likely", "plausible": "rated plausible", "no": "which the hand count found in no photo"}


def report():
    global PAGES, SELECT
    cont = int(os.environ.get("STANDIN_REPORT_CONTINUE", "4"))
    idx = [json.loads(line) for line in (WORK / "index.jsonl").open(encoding="utf-8")]
    runs = {}
    for select in ("spread", "latest"):
        for pages in (0, cont):
            SELECT, PAGES = select, pages
            runs[(select, pages)] = search()
    SELECT, PAGES = "spread", cont
    a, b = tally(runs[("spread", 0)]), tally(runs[("spread", cont)])
    la, lb = tally(runs[("latest", 0)]), tally(runs[("latest", cont)])
    first_n = {r["n"]: r for r in runs[("spread", 0)]["rows"]}
    old_first = {r["n"]: r for r in runs[("latest", 0)]["rows"]}
    old_more = {r["n"]: r for r in runs[("latest", cont)]["rows"]}
    more = runs[("spread", cont)]
    items = list(csv.DictReader((ROOT / "results" / "june-2026-items.csv").open(encoding="utf-8-sig")))
    value = {int(it["number"]): int(it["qty"]) * int(it["replacement_cad_each"]) for it in items}
    total = sum(value.values())

    def worth(res):
        return sum(value[r["n"]] for r in res["rows"] if r["census"] == "yes" and r["proven"])

    why = causes(more, idx)
    name = {r["n"]: SHORT.get(r["n"], r["item"]) for r in more["rows"]}
    gained = [name[n] for n in sorted(name) if first_n[n]["census"] == "yes" and first_n[n]["proven"] and not old_first[n]["proven"]]
    lost = [name[n] for n in sorted(name) if first_n[n]["census"] == "yes" and old_first[n]["proven"] and not first_n[n]["proven"]]
    summary = {**a, "rule": "nine spread across the capture dates (Skill 0.2.0)", "value_proven": worth(runs[("spread", 0)]),
               "value_total": total, "continued_pages": cont,
               "continued": {**b, "value_proven": worth(more)},
               "before_change": {"rule": "eight latest plus the earliest (Skill 0.1.0)", "first": la, "continued": lb},
               "misses": {str(n): w for n, w in why.items()}}
    group = {"recognition": [], "cap": [], "wrong photo first": [], "description": [], "keyword": [], "not indexed": []}
    for n, w in why.items():
        group[w].append(name[n])

    def join(xs):
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]

    change = ""
    if gained:
        change += f" On the first pass the change proved {join(gained)}"
        change += f", and lost {join(lost)}." if lost else "."
    elif lost:
        change += f" On the first pass the change lost {join(lost)}."
    change += (f" The first pass also cited {a['wrong_photos']} wrong photos instead of {la['wrong_photos']}, and continuing "
               f"cost {b['model_reads']} model reads instead of {lb['model_reads']}.")
    status = {r["n"]: r["census"] for r in more["rows"]}
    beyond = [f"{name[n]} ({RATED.get(status[n], status[n])})" for n in b["proven_outside_census"]]
    beyond = (f" Beyond the hand count it also proved {join(beyond)}, each with a photo checked by eye." if beyond else "")
    lines = ["# Recall on my real library, with a local stand-in for the NAS", "",
             f"Run {time.strftime('%Y-%m-%d')} with `tools/recall_standin.py`. A small vision model running on my own computer "
             f"({a['model']}, about four billion parameters, through Ollama) played two parts of the NAS: it tagged each of the "
             f"{a['photos']:,} photos captured before the loss that are stored on the computer with object categories, as the NAS "
             "recognition index would, and it answered the Skill's own question for each candidate photo. The library holds 1,769 "
             f"photos from before the loss; the other {1769 - a['photos']} are kept only in the cloud and could not be read. Nothing "
             "left the computer.", "",
             "What I chose and what the Skill chose: I set the stand-in index's 25 categories, and the category each line of my "
             "claim is searched under, before the run, following the Skill's search-routes reference. The NAS index has its own "
             "category list, so its routes can differ. Everything after that follows the Skill as written: one search per category, "
             "capped, then a second look at the photos already returned, for the items still unproven.", "",
             "How the model was chosen: a first run with gemma3:4b named items in photos that do not show them (a bed frame in a "
             "photo of trading cards, a console table in a photo of a fence), so before a second run three local models of the same "
             "size were asked the Skill's question about three photos whose contents the hand count records. gemma3:4b named an item "
             "that was not there, gemma4:e4b missed one, and qwen3.5:4b answered all three correctly; it is the model used here. "
             "The gemma3:4b run is not scored.", "",
             "## Result", "",
             f"**Skill 0.2.0, nine photos spread across the capture dates: the stand-in proved {a['proven']} of the {a['confirmed']} "
             f"items my hand count found in a pre-loss photo on the first pass, worth ${summary['value_proven']:,} of the "
             f"${total:,} CAD claimed, and {b['proven']} (${summary['continued']['value_proven']:,}) when the owner asks it to "
             f"continue.** {a['confirmed'] - a['searchable']} of the {a['confirmed']} are entries the Skill never searches (boxes, "
             f"bags, bedding, stored items), because it asks the owner to itemize them, so the most it could prove is "
             f"{a['searchable']}. The first pass cost {a['model_reads']} model reads over {a['photos_described']} photos; "
             f"continuing, {b['model_reads']} over {b['photos_described']}." + beyond, "",
             f"**Skill 0.1.0, the eight latest matches plus the earliest: {la['proven']} on the first pass, {lb['proven']} "
             "continuing.** That was the rule of the first run of this measurement. Its misses showed that the eight latest matches "
             "of a busy category all came from 2026 and never reached the older photos that held the proof, so the claim search "
             "was changed to spread its nine photos across the capture dates. The change came after that run; both results are "
             "kept here and scored the same way." + change, "",
             f"Photos it cited (0.2.0, continuing), every one checked against the hand count or opened and looked at: "
             f"{b['right_photos']} show the item, {b['wrong_photos']} do not, {b['unclear_photos']} cannot settle it"
             + (". Nothing was left unchecked. " if not b["unchecked"] else f", {b['unchecked']} not checked yet. ")
             + "A wrong photo never reaches the claim on its own: every row and its photo are shown to the owner to confirm "
             "first, and this many wrong photos is why that step exists.", "",
             "## Why it missed what it missed", "",
             "Worked out from the run itself (0.2.0, continuing), for each item the hand count found and the Skill searches:", ""]
    text = {
        "recognition": "**Recognition.** The stand-in index never tagged the photos that show {x} with the category searched, "
                       "so no search could return them.",
        "cap": "**The cap.** The photos that show {x} were tagged correctly but were not among the photos described, even "
               "after continuing.",
        "wrong photo first": "**A wrong photo counted first.** A photo that shows {x} was returned, but a wrong photo had "
                             "already been cited, so the second look never asked about it. The owner would turn that photo "
                             "down, and the Skill would look again.",
        "description": "**The description.** A photo that shows {x} was described, and the model did not name it.",
        "keyword": "**No word for it.** No category names {x}, and the stand-in has no keyword search, so only the second "
                   "look could reach it.",
        "not indexed": "**Not on the computer.** The only photos of {x} are kept in the cloud.",
    }
    for k, xs in group.items():
        if xs:
            lines.append("- " + text[k].format(x=join(xs)))
    lines += ["", "For the testing day, this says what to watch: how many photos the NAS index returns per category, and how "
              "its categories cover a household's things.", "",
              "This measures the Skill's search and description steps with a small model standing in for the NAS; the NAS's own "
              "recognition index will tag photos differently, and the receipt routes were not run.", "",
              "## Item by item", "",
              "A cited photo counts when the hand count lists it for that item, or when the photo, opened at full size and "
              "compared with the hand count's description of the item, shows it. Each verdict (yes, no or unclear) is in "
              "[recall-standin-checks.csv](recall-standin-checks.csv), which also keeps the verdicts on photos cited by earlier "
              "runs; the AI assistant that helped build this project made the first pass of these checks, and the list is mine "
              "to correct.", "",
              "| # | Item | Hand count | Route | 0.1.0 first pass | 0.1.0 continuing | 0.2.0 first pass | 0.2.0 continuing | "
              "Photos that show it (0.2.0) | Wrong photos cited |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]

    def yn(v):
        return "yes" if v else "no"

    for r in more["rows"]:
        n = r["n"]
        lines.append(f"| {n} | {r['item']} | {r['census']} | {r['route']} | {yn(old_first[n]['proven'])} | "
                     f"{yn(old_more[n]['proven'])} | {yn(first_n[n]['proven'])} | {yn(r['proven'])} | "
                     f"{', '.join(public(f) for f in r['good']) or ' '} | {len(r['bad']) or ' '} |")
    (ROOT / "results" / "recall-standin.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "results" / "recall-standin.json").write_text(json.dumps({"summary": summary}, indent=1) + "\n", encoding="utf-8")
    print("summary", json.dumps(summary, indent=1))


if __name__ == "__main__":
    {"index": index, "search": search, "report": report}[sys.argv[1]]()
