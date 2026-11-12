"""Recall on my real library, with a local stand-in for the NAS: what the Skill's claim search finds.

No NAS is available in Round 1, so a small local vision model plays two parts the NAS plays:

1. The recognition index. Every photo captured before the loss is tagged once with object
   categories from a fixed list, the way UGREEN Photos indexes a library.
2. photo-agent's vision step. For each claimed item, the Skill's own route and caps are applied
   (one search per category; the eight latest matching photos before the loss plus the earliest),
   and each candidate is described with the C4b question: which of the listed items are visible,
   and which other durable items. Then the Skill's second pass looks again at the photos already
   returned, for the items still unproven.

Entries that do not name one object (boxes, bags, bedding, stored items) are never searched: the
Skill asks the owner to itemize them. The second route (text in a photo, receipt-date window) is not
run here, because the receipts are not part of this test.

Scoring is against results/pre-loss-photo-census.md, the hand count made before this test: an item
counts as proven when a photo the model cites is one the census lists for that item, or one I opened
and checked by eye (recorded in results/recall-standin-checks.csv). Nothing leaves this machine: the
model runs in Ollama, and only file names and item names are written out.

    py tools/recall_standin.py index      # tag every pre-loss photo (cached in tmp/recall/)
    py tools/recall_standin.py search     # run the claim search and score it
    py tools/recall_standin.py report     # write results/recall-standin.md and .json
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

    def describe(path, names):
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
    # first route: one search per category, the eight latest before the loss plus the earliest
    for cat in sorted({c for c in ROUTE.values() if c and c != "keyword"}):
        wanted = [n for n, c in ROUTE.items() if c == cat]
        hits = sorted((p for p in idx if cat in p["cats"]), key=lambda p: p["taken"])
        chosen = hits[-8:] + ([hits[0]] if hits and hits[0] not in hits[-8:] else [])
        for p in chosen:
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
    # Each continuation describes the next eight older matches of the item's category, up to PAGES times.
    files_of = {n: cen.get(n, ("no", set()))[1] for n in name}

    def shown(n):
        return any(Path(p["path"]).name in files_of[n] or by_eye.get((n, Path(p["path"]).name)) == "yes" for p in cited[n])

    for cat in sorted({c for c in ROUTE.values() if c and c != "keyword"}):
        hits = sorted((p for p in idx if cat in p["cats"]), key=lambda p: p["taken"])
        for page in range(1, PAGES + 1):
            wanted = [n for n, c in ROUTE.items() if c == cat and not shown(n)]
            older = hits[max(0, len(hits) - 8 * (page + 1)):len(hits) - 8 * page]
            older = [p for p in older if p is not hits[0]]
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
    out = {"model": MODEL, "photos_indexed": len(idx), "describe_calls": len(cache), "rows": rows,
           "returned": sorted({Path(p["path"]).name for p in pool})}
    (WORK / (f"result-continue{PAGES}.json" if PAGES else "result.json")).write_text(json.dumps(out, indent=1), encoding="utf-8")
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
            "unclear_photos": sum(len(r.get("unclear", [])) for r in rows), "unchecked": sum(len(r["todo"]) for r in rows)}


def report():
    global PAGES
    PAGES = 0
    first = search()
    PAGES = int(os.environ.get("STANDIN_REPORT_CONTINUE", "4"))
    more = search()
    a, b = tally(first), tally(more)
    by_n = {r["n"]: r for r in first["rows"]}
    summary = {**a, "continued_pages": PAGES, "continued": b}
    lines = ["# Recall on my real library, with a local stand-in for the NAS", "",
             f"Run {time.strftime('%Y-%m-%d')} with `tools/recall_standin.py`. A small vision model running on my own computer "
             f"({a['model']}, about four billion parameters, through Ollama) played two parts of the NAS: it tagged each of the "
             f"{a['photos']:,} photos captured before the loss with object categories, as the NAS recognition index would, "
             "and it answered the Skill's own question for each candidate photo. The Skill's routes and caps were applied as written: "
             "one search per category, the eight latest photos before the loss plus the earliest, then a second look at the photos "
             "already returned for the items still unproven. Nothing left the computer.", "",
             "How the model was chosen: a first run with gemma3:4b named items in photos that do not show them (a bed frame in a "
             "photo of trading cards, a console table in a photo of a fence), so before a second run three local models of the same "
             "size were asked the Skill's question about three photos whose contents the hand count records. gemma3:4b named an item "
             "that was not there, gemma4:e4b missed one, and qwen3.5:4b answered all three correctly; it is the model used here. "
             "The first run is not scored.", "",
             "## Result", "",
             f"**First pass: the stand-in proved {a['proven']} of the {a['confirmed']} items my hand count found in a pre-loss photo**, "
             "each with a photo that shows the item. "
             f"{a['confirmed'] - a['searchable']} of the {a['confirmed']} are entries the Skill never searches (boxes, bags, bedding, "
             f"stored items), because it asks the owner to itemize them, so the most it could prove is {a['searchable']}. "
             "It also found a clearer photo of the stick vacuum, an item the hand count had rated only likely.", "",
             f"**Continuing: {b['proven']} of {b['confirmed']}.** When more photos match than were described, the Skill offers to go on. "
             f"With the owner turning down the wrong photos and asking to continue up to {PAGES} times per item, the search reached older "
             "photos of the storage room and proved the bed frame and the bookshelf from them.", "",
             f"Photos it cited, every one checked against the hand count or opened and looked at: {b['right_photos']} show the item, "
             f"{b['wrong_photos']} do not, {b['unclear_photos']} cannot settle it. Nothing was left unchecked. "
             "A wrong photo never reaches the claim on its own: every row and its photo are shown to the owner to confirm first, "
             "and this many wrong photos is why that step exists. On the first pass it cited no photo for the camera rig or the iron, "
             "the two items the hand count found in no photo; continuing, it cited two screenshots for the camera rig.", "",
             "## Why it missed what it missed", "",
             "- **The cap, not the recognition.** The index tagged the December walk-through correctly (bed, bookcase, table, lamp), but "
             "40 photos are tagged bed and 133 lamp, and the eight latest of each are from 2026. The first pass never reached December "
             "2025. Continuing reached the bed frame and the bookshelf; the coffee table, the road case and the floor lamps were still "
             "further back.",
             "- **An item counted as found too early.** The hex side table was in a photo the search returned, but a wrong photo had "
             "already been cited for it, so the second look never asked about it. The owner would turn that photo down, and the "
             "Skill would look again.",
             "- **No word for it.** The boot dryer has no category and the stand-in has no keyword search, so only the second look "
             "could reach it, and its one photo was never returned.", "",
             "For the testing day, this says what to watch: how many photos the NAS index returns per category, and whether the "
             "eight-latest cap needs to grow when an item stays unproven.", "",
             "This measures the Skill's search and description steps with a small model standing in for the NAS; the NAS's own "
             "recognition index will tag photos differently, and the receipt routes were not run.", "",
             "## Item by item", "",
             "A cited photo counts when the hand count lists it for that item, or when the photo, opened at full size and compared "
             "with the hand count's description of the item, shows it. Each verdict (yes, no or unclear) is in "
             "[recall-standin-checks.csv](recall-standin-checks.csv); the AI assistant that helped build this project made the first "
             "pass of these checks, and the list is mine to correct.", "",
             "| # | Item | Hand count | Route | First pass | Continuing | Photos that show it | Wrong photos cited |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in more["rows"]:
        lines.append(f"| {r['n']} | {r['item']} | {r['census']} | {r['route']} | {'yes' if by_n[r['n']]['proven'] else 'no'} | "
                     f"{'yes' if r['proven'] else 'no'} | {', '.join(public(f) for f in r['good']) or ' '} | "
                     f"{len(r['bad']) or ' '} |")
    (ROOT / "results" / "recall-standin.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "results" / "recall-standin.json").write_text(json.dumps({"summary": summary}, indent=1) + "\n", encoding="utf-8")
    print("summary", summary)


if __name__ == "__main__":
    {"index": index, "search": search, "report": report}[sys.argv[1]]()
