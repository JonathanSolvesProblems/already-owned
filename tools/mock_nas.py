"""A scripted mock NAS, for rehearsing the Skill without the hardware.

It plays the five expert agents and the user. An assistant under test follows SKILL.md and can act
only through these commands, each of which is logged to <run>/log.jsonl:

    py tools/mock_nas.py --run RUN init SCENARIO
    py tools/mock_nas.py --run RUN delegate --target AGENT --instruction 'ONE LINE'
    py tools/mock_nas.py --run RUN wait APPROVAL_ID "what the assistant told the user"
    py tools/mock_nas.py --run RUN ask "a question for the user"
    py tools/mock_nas.py --run RUN tell "a statement for the user"
    py tools/mock_nas.py --run RUN report "the final report"

Rules of the mock:
- An instruction is accepted only if it is one of the templates of SKILL.md with every slot filled.
  Anything else comes back as failed, with the nearest template named. That is stricter than a real
  expert, on purpose: it measures whether the assistant sends what the Skill wrote.
- Every answer comes from tests/rehearsal/library.json, a made-up library. Nothing else exists.
- A write returns waiting_approval. The scripted user of the scenario approves or declines it when
  the assistant calls wait.
- The mock never deletes, moves or overwrites; it has no command for it.

This is a fixture test. It shows that an assistant can follow the instructions as written and that
the checks in tools/check_rehearsal.py hold on a made-up library. It says nothing about recall on a
real library or about how the real experts behave.
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill" / "home-contents-inventory" / "SKILL.md"
DATA = ROOT / "tests" / "rehearsal"

KEYS = [  # template id, a phrase only that template contains
    ("U1", "find the folder named Home Contents in it"),
    ("U2", "list the recognized object categories"),
    ("U3", "For the household object category"),
    ("U4", "find PDF and image files"),
    ("U5", "for receipts and invoices, using the text recognized"),
    ("U6", "Extract the purchased line items"),
    ("OCR", "Read all text in the image"),
    ("U9", "Create a folder named Home Contents in the personal space of the current user. This is a write"),
    ("U10", "Create an album named Home contents"),
    ("U11", "file tag named home-contents"),
    ("U12", "Save the contents list"),
    ("READ", "Return the full text of the file"),
    ("C2F", "Find audio recordings"),
    ("C2T", "Transcribe the audio recording"),
    ("C4A", "Take the twelve earliest"),
    ("C4B", "captured strictly before"),
    ("C4S", "Look again at the photos"),
    ("C5", "List the cameras"),
    ("C8D", "Draft, in"),
    ("C8T", "Translate into"),
    ("C9F", "a folder named Claims inside it"),
    ("C9C", "Copy each file"),
    ("C9H", "Compute the SHA-256 of each file"),
    ("C9S", "Save a new Markdown file in the claim folder"),
    ("C9A", "Create an album named Claim"),
]
WRITES = {"U9": "folder", "U10": "album", "U11": "tag", "U12": "page", "C9F": "claim folder", "C9C": "copies",
          "C9S": "claim document", "C9A": "claim album"}
MODEL_READS = {"U6": "paths", "C4S": "paths"}  # at most ten paths
HOUSEHOLD = {"sofa", "television", "chair", "bed", "table", "bicycle", "dumbbell", "vacuum cleaner", "refrigerator",
             "washing machine", "lamp", "bookcase"}
RECEIPT_WORDS = ("total", "subtotal", "receipt", "invoice", "tax", "order")
MONTHS = {m: i for i, m in enumerate("january february march april may june july august september october november december".split(), 1)}


# ---------------------------------------------------------------- templates
def load_templates():
    found = []
    for line in SKILL.read_text(encoding="utf-8").splitlines():
        m = re.match(r"`delegate --target ([a-z-]+) --instruction '(.*)'`$", line.strip())
        if m:
            found.append((m.group(1), m.group(2)))
    out = {}
    for target, text in found:
        ids = [k for k, phrase in KEYS if phrase in text]
        assert len(ids) == 1, (text[:60], ids)
        out[ids[0]] = {"target": target, "text": text, "regex": to_regex(text)}
    assert len(out) == len(KEYS) == len(found), (len(out), len(KEYS), len(found))
    return out


LABELS = ("Heading", "Summary", "Rows", "Totals", "Camera events", "Exhibits")


def to_regex(text):
    # Labelled lists sit at the end of an instruction, and a label with nothing to carry is left out.
    tail = re.search(r"((?: (?:%s): \{[^}]+\})+)$" % "|".join(LABELS), text)
    if tail:
        head = to_regex(text[:tail.start()])
        for label, slot in re.findall(r" (%s): \{([^}]+)\}" % "|".join(LABELS), tail.group(1)):
            head += r"(?:\s+%s:\s*(?P<%s__1>.*?))?" % (re.escape(label).replace("\\ ", r"\s+"), re.sub(r"\W", "_", slot))
        return head + r"\s*"
    parts = re.split(r"(\{[^}]+\})", text)
    rx, seen = "", {}
    for i, part in enumerate(parts):
        if part.startswith("{"):
            name = re.sub(r"\W", "_", part[1:-1])
            seen[name] = seen.get(name, 0) + 1
            last = all(not p.strip() for p in parts[i + 1:])
            rx += f"(?P<{name}__{seen[name]}>.+)" if last else f"(?P<{name}__{seen[name]}>.+?)"
        else:
            lit = re.escape(part)
            lit = re.sub(r"(\\ )+", r"\\s+", lit)
            rx += lit
    # a sentence may be added before the closing "Read only." (the Skill does this in claim mode)
    rx = re.sub(r"\\s\+Read\\ only\\\.$|\\s\+Read\\s\+only\\\.$", r"(?P<extra__1>\\s.*?)?\\s+Read\\s+only\\.", rx)
    return rx


def match(templates, target, instruction):
    text = " ".join(instruction.split())
    for tid, t in templates.items():
        if t["target"] != target:
            continue
        m = re.fullmatch(t["regex"], text, re.S)
        if m:
            slots = {}
            for k, v in m.groupdict().items():
                if v is not None:
                    slots.setdefault(k.split("__")[0], v.strip())
            return tid, slots
    same = {k: v for k, v in templates.items() if v["target"] == target} or templates
    best = max(same.items(), key=lambda kv: difflib.SequenceMatcher(None, kv[1]["text"], text).ratio())
    # Name the first fixed piece of the template that the instruction does not carry, in order.
    pieces = [" ".join(p.split()) for p in re.split(r"\{[^}]+\}", best[1]["text"]) if p.strip()]
    pos, first = 0, ""
    for piece in pieces:
        found = text.find(piece, pos)
        if found < 0:
            first = piece if len(piece) <= 160 else piece[:160] + " ..."
            break
        pos = found + len(piece)
    ratio = round(difflib.SequenceMatcher(None, re.sub(r"\{[^}]+\}", "", best[1]["text"]), text).ratio(), 2)
    return None, {"nearest": best[0], "nearest_target": best[1]["target"], "ratio": ratio, "near": first}


# ---------------------------------------------------------------- dates
def find_dates(s):
    out = []
    for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{1,2}):(\d{2}))?", s):
        y, mo, d, h, mi = m.groups()
        out.append((m.start(), datetime(int(y), int(mo), int(d), int(h or 0), int(mi or 0)), h is not None))
    for m in re.finditer(r"(?i)\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})(?:\D{1,12}?(\d{1,2})(?::(\d{2}))?\s*(am|pm))?", s):
        if m.group(1).lower() in MONTHS:
            h = int(m.group(4) or 0) % 12 + (12 if (m.group(6) or "").lower() == "pm" else 0) if m.group(4) else 0
            out.append((m.start(), datetime(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)), h, int(m.group(5) or 0)), bool(m.group(4))))
    for m in re.finditer(r"(?i)\b(\d{1,2})\s+([a-z]+)\s+(\d{4})", s):
        if m.group(2).lower() in MONTHS:
            out.append((m.start(), datetime(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))), False))
    out.sort()
    return [(d, timed) for _, d, timed in out]


def date_range(s, now):
    """A slot such as 'between 2026-05-01 and 2026-06-01' or 'at any date' -> (lo, hi), either may be None."""
    low = s.lower()
    ds = find_dates(s)
    if "any date" in low or not (ds or "today" in low or "now" in low):
        return (None, None) if "any date" in low else "unreadable"
    end_of = lambda d, timed: d if timed else d + timedelta(days=1) - timedelta(seconds=1)
    if len(ds) >= 2:
        return ds[0][0], end_of(*ds[1])
    if len(ds) == 1 and re.search(r"\b(today|now)\b", low):
        return ds[0][0], now
    if len(ds) == 1:
        if re.search(r"\b(before|until|up to|ending|ends|ended)\b", low):
            return None, end_of(*ds[0]) if not re.search(r"strictly before|before", low) else ds[0][0]
        return ds[0][0], now
    return None, now


def one_time(s):
    ds = find_dates(s)
    return ds[0][0] if ds else None


def cap(p):
    return datetime.fromisoformat(p["captured"]) if p.get("captured") else None


def fmt(d):
    return d.strftime("%Y-%m-%d %H:%M") if d else "none"


# ---------------------------------------------------------------- state
class Run:
    def __init__(self, path):
        self.dir = Path(path)
        self.state_file = self.dir / "state.json"
        self.log_file = self.dir / "log.jsonl"
        self.lib = json.loads((DATA / "library.json").read_text(encoding="utf-8"))
        self.s = json.loads(self.state_file.read_text(encoding="utf-8")) if self.state_file.exists() else None

    def save(self):
        self.state_file.write_text(json.dumps(self.s, indent=1, ensure_ascii=False), encoding="utf-8")

    def log(self, **entry):
        entry["n"] = sum(1 for _ in self.log_file.open(encoding="utf-8")) + 1 if self.log_file.exists() else 1
        entry["phase"] = self.s.get("phase", 1)
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    @property
    def now(self):
        return datetime.fromisoformat(self.s["now"])

    @property
    def scen(self):
        return self.s["scenario"]

    def photos(self):
        hide = set(self.scen.get("hide_categories", []))
        after = self.scen.get("hide_photos_after")
        out = []
        for p in self.lib["photos"]:
            if after and p.get("captured") and p["captured"] >= after:
                continue
            q = dict(p)
            if self.scen.get("no_household_index"):
                q["cats"] = [c for c in p["cats"] if c not in HOUSEHOLD]
            q["cats"] = [c for c in q["cats"] if c not in hide]
            out.append(q)
        return out


def sha(path):
    return hashlib.sha256(("mock bytes of " + path).encode("utf-8")).hexdigest()


def split_paths(s):
    return [p.rstrip(".,;") for p in re.findall(r"/home/me/[^,;]+?\.(?:jpe?g|png|heic|pdf|m4a|mp3|wav|md)", s, re.I)]


# ---------------------------------------------------------------- experts
def describe(p, items_text=None):
    line = f"- {p['path']} | captured {fmt(cap(p))} | camera {p.get('camera') or 'not recorded'} | room: {p.get('room') or 'cannot be seen'} | shows: {p['shows']}"
    if p.get("damage"):
        line += " | damage visible: yes"
    if items_text is not None:
        low = items_text.lower()
        listed = [i["name"] for i in p.get("items", []) if any(k in low for k in i["keys"])]
        other = [i["name"] for i in p.get("items", []) if not any(k in low for k in i["keys"])]
        line += f" | listed items visible: {', '.join(listed) or 'none'} | other durable items visible, not on the list: {', '.join(other) or 'none'}"
    if p.get("ocr"):
        line += f" | readable text: {p['ocr'][:60]}"
    return line


def by_route(photos, route, category=""):
    r = route.lower()
    if "captured between" in r:
        ds = find_dates(route)
        if len(ds) < 2:
            return None
        lo, hi = ds[0][0], ds[1][0] + timedelta(days=1)
        return [p for p in photos if cap(p) and lo <= cap(p) < hi]
    if "text visible" in r or "text in the photo" in r:
        words = [w for w in re.findall(r"[a-z0-9.]+", (r.split(":", 1)[1] if ":" in r else r.split("photo", 1)[-1]) + " " + category.lower()) if len(w) > 2 and w not in ("the", "and", "text", "visible", "photo", "model", "name", "brand", "words", "item")]
        return [p for p in photos if p.get("ocr") and any(w in p["ocr"].lower() for w in words)]
    if "keyword" in r:
        word = r.split("keyword", 1)[1].strip(" :.\"").replace("search of the library for", "").strip()
        words = [w for w in re.findall(r"[a-z0-9-]+", word) if len(w) > 2 and w not in ("the", "for", "and", "search", "word", "words", "library", "named", "item", "items")]
        return [p for p in photos if any(w in (p["shows"] + " " + " ".join(k for i in p.get("items", []) for k in i["keys"])).lower() for w in words)]
    if "recognized object" in r:
        name = r.split("recognized object", 1)[1].strip(" :.\"") or category.lower()
        return [p for p in photos if name in [c.lower() for c in p["cats"]]]
    return None


def spread(found, n=9):
    """Claim search: n matches spread across the capture dates, the latest and the earliest included."""
    dated = sorted([p for p in found if cap(p)], key=cap)
    undated = [p for p in found if not cap(p)]
    if len(dated) <= n:
        return dated, 0, undated
    idx = sorted({round(i * (len(dated) - 1) / (n - 1)) for i in range(n)})
    chosen = [dated[i] for i in idx]
    return chosen, len(dated) - len(chosen), undated


def take(found, newest, key=cap):
    dated = sorted([p for p in found if cap(p)], key=key)
    undated = [p for p in found if not cap(p)]
    chosen = dated[-newest:]
    if dated and dated[0] not in chosen:
        chosen = [dated[0]] + chosen
    return chosen, len(dated) - len(chosen), undated


def expert(run, tid, slots):
    """Return (state, text). Writes return ('waiting_approval', ...) through request()."""
    lib, s, now = run.lib, run.s, run.now
    home = lib["home"]
    hc = home + "/Home Contents"

    def not_processed(ps):
        return [p for p in ps if p.get("unreadable")]

    if tid == "U1":
        clock = f"NAS local date and time: {now.strftime('%Y-%m-%d %H:%M')}"
        if hc not in s["folders"]:
            return "completed", f"The folder Home Contents does not exist in {home}.\n{clock}"
        pages = sorted((p, t) for p, t in s["files"].items() if p.startswith(hc + "/") and "/" not in p[len(hc) + 1:] and (Path(p).name.startswith("Home contents list") or t.startswith("Home contents list")))
        if not pages:
            return "completed", f"Folder: {hc}\nIt holds no file whose name or first line starts with Home contents list.\n{clock}"
        body = "\n\n".join(f"--- {p} (modified {s['modified'].get(p, s['now'])})\n{t}" for p, t in pages)
        return "completed", f"Folder: {hc}\n{len(pages)} page(s), oldest first:\n\n{body}\n\n{clock}"

    if tid == "U2":
        rng = date_range(slots["date_range"], now)
        if rng == "unreadable":
            return "failed", "I could not read the date range in the instruction."
        lo, hi = rng
        counts = {}
        for p in run.photos():
            c = cap(p)
            if c and (lo is None or c >= lo) and (hi is None or c <= hi):
                for name in p["cats"]:
                    if name in HOUSEHOLD:
                        counts[name] = counts.get(name, 0) + 1
        if not counts:
            return "completed", "No results: no recognized category of household belongings has photos in that period."
        return "completed", "Categories (exact index name: photos in the period)\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(counts.items()))

    if tid in ("U3", "C4B"):
        if tid == "U3":
            rng = date_range(slots["date_range"], now)
            if rng == "unreadable":
                return "failed", "I could not read the date range in the instruction."
            lo, hi = rng
            strict = False
            items_text = None
        else:
            hi = one_time(slots["loss_time"])
            if not hi:
                return "failed", "I could not read the loss time in the instruction."
            lo, strict, items_text = None, True, slots["items"]
        found = by_route(run.photos(), slots["route"], slots.get("category", ""))
        if found is None:
            return "failed", f"I do not know the search route: {slots['route']}"
        pool = []
        for p in found:
            c = cap(p)
            if c is None:
                pool.append(p)
            elif (lo is None or c >= lo) and (hi is None or (c < hi if strict else c <= hi)):
                pool.append(p)
        pool = [p for p in pool if not p["path"].startswith(hc)]
        chosen, more, undated = spread(pool) if tid == "C4B" else take(pool, 8)
        if not chosen and not undated:
            return "completed", "No results for this search."
        bad = not_processed(chosen)
        good = [p for p in chosen if p not in bad]
        drop = run.scen.get("partial_return")
        dropped = []
        if drop and len(good) > 3 and not s.get("partial_done"):
            dropped, good = good[-2:], good[:-2]
            s["partial_done"] = True
        out = [describe(p, items_text) for p in good]
        text = f"{len(good)} photo(s) described:\n" + "\n".join(out)
        text += f"\nmore matched, not described: {more}"
        if dropped:
            text += "\n(the description stopped early; these paths were found but not described: " + ", ".join(p["path"] for p in dropped) + ")"
        text += "\nundated: " + (", ".join(f"{p['path']} (shows: {p['shows']})" for p in undated) or "none")
        text += "\nnot processed: " + (", ".join(p["path"] for p in bad) or "none")
        return "completed", text

    if tid == "C4S":
        paths = split_paths(slots["paths"])
        if len(paths) > 10:
            return "failed", f"{len(paths)} paths in one request; this expert reads at most ten files per request."
        by = {p["path"]: p for p in run.photos()}
        out, missing = [], []
        for path in paths:
            if path in by and not by[path].get("unreadable"):
                out.append(describe(by[path], slots["items"]))
            else:
                missing.append(path)
        return "completed", (f"{len(out)} photo(s) looked at again:\n" + "\n".join(out) if out else "No results.") + ("\nnot processed: " + ", ".join(missing) if missing else "")

    if tid == "C4A":
        lo, hi = one_time(slots["loss_time"]), one_time(slots["end_date"])
        if not lo or not hi:
            return "failed", "I could not read the two dates in the instruction."
        after = sorted([p for p in run.photos() if cap(p) and lo <= cap(p) <= hi + timedelta(days=1)], key=cap)
        chosen, more = after[:12], max(0, len(after) - 12)
        keep = [p for p in chosen if p.get("damage")]
        if not keep:
            return "completed", "No results: no photo in that period shows damage or these rooms."
        return "completed", f"{len(keep)} photo(s) kept of {len(chosen)} described:\n" + "\n".join(describe(p) for p in keep) + f"\nmore matched, not described: {more}"

    if tid == "U4":
        rng = date_range(slots["date_range"], now)
        if rng == "unreadable":
            return "failed", "I could not read the date range in the instruction."
        lo, hi = rng
        files = [f for f in lib["receipts"] if (lo is None or datetime.fromisoformat(f["modified"]) >= lo) and (hi is None or datetime.fromisoformat(f["modified"]) <= hi)]
        if not files:
            return "completed", "No results: no receipt or invoice file modified in that period."
        tagged = set(s["tags"].get("home-contents", []))
        files.sort(key=lambda f: (f["path"] not in tagged, f["modified"]), reverse=False)
        return "completed", "\n".join(f"- {f['path']} | {Path(f['path']).name} | modified {f['modified'][:10]}" + (" | tagged home-contents" if f["path"] in tagged else "") for f in files) + "\nmore matched: 0"

    if tid == "U5":
        rng = date_range(slots["date_range"], now)
        if rng == "unreadable":
            return "failed", "I could not read the date range in the instruction."
        lo, hi = rng
        hits = [p for p in run.photos() if p.get("ocr") and p.get("receipt") and cap(p) and (lo is None or cap(p) >= lo) and (hi is None or cap(p) <= hi)]
        if not hits:
            return "completed", "No results: no photographed receipt in that period."
        return "completed", "\n".join(f"- {p['path']} | captured {fmt(cap(p))} | full text: {p['ocr']}" for p in hits[-10:]) + "\nmore matched: 0\nnot processed: none"

    if tid == "U6":
        paths = split_paths(slots["paths"])
        if len(paths) > 10:
            return "failed", f"{len(paths)} paths in one request; this expert reads at most ten files per request."
        by = {f["path"]: f for f in lib["receipts"]}
        out, fail, flagged = [], [], []
        want = (slots.get("extra") or "").lower()
        for path in paths:
            f = by.get(path)
            if not f or f.get("image"):
                fail.append(f"{path} (unsupported file type: image)" if (f or path.lower().endswith((".jpg", ".jpeg", ".png"))) else f"{path} (not found)")
                continue
            if f.get("injection"):
                flagged.append(path)
            for ln in f["lines"]:
                if ln.get("skip"):
                    continue
                if "keep only lines" in want and not any(k in want for k in ln["keys"]):
                    continue
                out.append(f"- {ln['merchant']} | {ln['date']} | {ln['item']} | brand and model: {ln.get('model') or 'not printed'} | qty {ln['qty']} | {ln['price']} {ln['currency']} | source {path}")
        text = ("Purchase lines:\n" + "\n".join(out)) if out else "Empty result: no durable household item on these files."
        if fail:
            text += "\nfailures: " + "; ".join(fail)
        if flagged:
            text += "\ntext that addresses an assistant or asks for an action was found in: " + ", ".join(flagged)
        return "completed", text + "\nnot processed: none"

    if tid == "OCR":
        path = (split_paths(slots["path"]) or [slots["path"]])[0]
        for f in lib["receipts"]:
            if f["path"] == path and f.get("ocr"):
                return "completed", f"Text of {path}: {f['ocr']}"
        for p in run.photos():
            if p["path"] == path and p.get("ocr"):
                return "completed", f"Text of {path}: {p['ocr']}"
        return "failed", f"The image at {path} could not be read."

    if tid == "READ":
        path = slots["path"].strip().rstrip(".,")
        if path not in s["files"]:
            return "failed", f"No file at {path}."
        text = s["files"][path]
        return "completed", f"File {path}, {len(text.encode('utf-8'))} bytes:\n{text}"

    if tid == "C2F":
        since = one_time(slots["loss_date"])
        recs = [r for r in lib["recordings"] if not since or datetime.fromisoformat(r["modified"]) >= since]
        if not recs:
            return "completed", "No results: no audio recording modified on or after that date."
        return "completed", "\n".join(f"- {r['path']} | {Path(r['path']).name} | modified {r['modified'][:16].replace('T', ' ')}" for r in sorted(recs, key=lambda r: r["modified"], reverse=True))

    if tid == "C2T":
        path = slots["path"].strip().rstrip(".,")
        for r in lib["recordings"]:
            if r["path"] == path:
                return "completed", f"Transcript of {path}: {r['transcript']}"
        return "failed", f"The recording at {path} could not be read."

    if tid == "C5":
        cams = lib.get("cameras", []) if run.scen.get("cameras") else []
        if not cams:
            return "completed", "No results: no camera is registered for this user."
        ds = find_dates(slots["window"])
        lo, hi = (ds[0][0], ds[1][0]) if len(ds) >= 2 else (None, None)
        loss = one_time(slots["loss_time"])
        ev = [e for e in lib["events"] if (lo is None or lo <= datetime.fromisoformat(e["time"]) <= hi)]
        last = [e for e in lib["events"] if loss and datetime.fromisoformat(e["time"]) < loss]
        text = "Cameras: " + ", ".join(f"{c['name']} ({c['status']})" for c in cams)
        text += "\nEvents:\n" + ("\n".join(f"- {e['time'].replace('T', ' ')} | {e['camera']} | {e['type']} | snapshot {e['snapshot']}" for e in sorted(ev, key=lambda e: e["time"], reverse=True)) or "none") + "\nmore events: 0"
        if last:
            e = sorted(last, key=lambda e: e["time"])[-1]
            text += f"\nLast event before the loss time: {e['time'].replace('T', ' ')} | {e['camera']} | {e['type']} | snapshot {e['snapshot']}"
        return "completed", text

    if tid == "C8D":
        return "completed", f"Heading: Contents claim. {slots['claim_details']}\nSummary: This claim lists the household contents affected by the loss described here: {slots['loss_details_and_row_counts']}. Each row names the proof that exists for it."

    if tid == "C8T":
        return "completed", f"[{slots['target_language']}] Heading: {slots['heading']} Summary: {slots['summary']} Rows: {slots['rows']}"

    if tid == "C9H":
        paths = split_paths(slots["paths"])
        return "completed", "\n".join(f"- {p} | SHA-256 {sha(p)}" for p in paths) or "No results."

    return request(run, tid, slots)


def parse_rows(text):
    rows = []
    for chunk in re.split(r"\bRow\s*:", text)[1:]:
        vals = [v.strip() for v in chunk.strip().rstrip(".").split(";")]
        if vals and vals[-1].endswith("."):
            vals[-1] = vals[-1][:-1]
        rows.append(vals)
    return rows


def table(cols, rows):
    head = "| " + " | ".join(cols) + " |\n| " + " | ".join("---" for _ in cols) + " |\n"
    return head + "\n".join("| " + " | ".join(r) + " |" for r in rows) + "\n"


def columns(text):
    cols = [c.strip() for c in re.split(r",| and ", text) if c.strip()]
    return cols


def request(run, tid, slots):
    """Validate a write and park it until the scripted user answers."""
    s, home = run.s, run.lib["home"]
    hc = home + "/Home Contents"
    act = {"tid": tid, "kind": WRITES[tid], "slots": slots}
    if tid == "U9":
        act["what"] = f"create the folder {hc}"
    elif tid == "U10":
        paths = split_paths(slots["paths"])
        if not paths:
            return "failed", "No photo path in the instruction."
        act.update(what=f"create the album Home contents {slots['today']} with {len(paths)} photo(s)", paths=paths)
    elif tid == "U11":
        paths = split_paths(slots["paths"])
        act.update(what=f"attach the tag home-contents to {len(paths)} file(s)", paths=paths)
    elif tid in ("U12", "C9S"):
        rows = parse_rows(slots.get("rows", ""))
        bad = [r[0] for r in rows if len(r) != 12]
        if bad:
            return "failed", f"Row(s) {', '.join(bad)} do not have twelve values separated by semicolons; nothing was saved."
        lines = len(rows) + len(re.findall(r"\bExhibit\b|\.(?:jpe?g|pdf|m4a)\b[^.]*?[0-9a-f]{64}", slots.get("exhibits", "")))
        folder = (slots.get("folder_path") or slots.get("claim_folder_path")).strip().rstrip(".,")
        if folder not in s["folders"]:
            return "failed", f"The folder {folder} does not exist."
        act.update(what=f"save a new Markdown file in {folder}", folder=folder, rows=rows, lines=lines)
    elif tid == "C9F":
        name = slots["loss_date_and_kind"].strip()
        act.update(what=f"create the claim folder {hc}/Claims/{name}", name=name)
    elif tid == "C9C":
        paths = split_paths(slots["paths"])
        if len(paths) > 40:
            return "failed", f"{len(paths)} paths in one request; at most forty."
        folder = slots["claim_folder_path"].strip().rstrip(".,")
        if folder not in s["folders"]:
            return "failed", f"The folder {folder} does not exist."
        act.update(what=f"copy {len(paths)} file(s) into {folder}", paths=paths, folder=folder)
    elif tid == "C9A":
        paths = split_paths(slots["paths"])
        act.update(what=f"create the album Claim {slots['loss_date']} with {len(paths)} photo(s)", paths=paths)
    s["counter"] += 1
    aid = f"A{s['counter']}"
    s["pending"][aid] = act
    return "waiting_approval", f"approval id: {aid}\nwaiting for the user to approve: {act['what']}"


def execute(run, act):
    s, home = run.s, run.lib["home"]
    hc = home + "/Home Contents"
    tid, slots = act["tid"], act["slots"]
    stamp = run.s["now"]
    if tid == "U9":
        s["folders"].append(hc)
        return f"Created the folder. Real path: {hc}"
    if tid == "C9F":
        for f in (hc, hc + "/Claims"):
            if f not in s["folders"]:
                s["folders"].append(f)
        path = hc + "/Claims/" + act["name"]
        if path in s["folders"]:
            path += " " + run.now.strftime("%H%M")
        s["folders"].append(path)
        return f"Created. Real path of the claim folder: {path}"
    if tid in ("U10", "C9A"):
        known = {p["path"] for p in run.lib["photos"]}
        ok = [p for p in act["paths"] if p in known]
        aid = f"alb-{len(s['albums']) + 1:02d}"
        name = ("Home contents " + slots["today"]) if tid == "U10" else ("Claim " + slots["loss_date"])
        s["albums"].append({"id": aid, "name": name, "paths": ok})
        return f"Album created. Identifier: {aid}. Photos added: {len(ok)} of {len(act['paths'])} sent."
    if tid == "U11":
        tagged = s["tags"].setdefault("home-contents", [])
        for p in act["paths"]:
            if p not in tagged:
                tagged.append(p)
        return "Tag identifier: tag-12. " + "; ".join(f"{p}: tagged" for p in act["paths"])
    if tid == "C9C":
        out = []
        for i, p in enumerate(act["paths"]):
            dst = act["folder"] + "/" + Path(p).name
            if dst in s["copies"]:
                out.append(f"- {p} | a file of that name already exists in the claim folder; left as it is, not verified")
                continue
            orig = sha(p)
            copy = sha(p + " damaged") if run.scen.get("corrupt_copy") == Path(p).name else orig
            s["copies"][dst] = {"from": p, "sha": copy}
            out.append(f"- {p} | copy: {dst} | SHA-256 original {orig} | SHA-256 copy {copy} | match: {'yes' if orig == copy else 'NO'}")
        return "Copied, originals untouched:\n" + "\n".join(out)
    # save-text: never overwrites; the name follows the hint
    if tid == "U12":
        title = "Home contents list " + slots["today"].strip()
        body = title + "\n\n" + table(columns(slots["column_names"]), act["rows"])
    else:
        title = "Contents claim " + slots["loss_date"].strip()
        parts = [title, ""]
        for label, key in (("", "heading"), ("", "summary")):
            if slots.get(key):
                parts += [slots[key], ""]
        if act["rows"]:
            parts += [table(columns(slots["column_names"]), act["rows"])]
        for label, key in (("Totals", "totals"), ("Camera events", "camera_events")):
            if slots.get(key):
                parts += [f"{label}: {slots[key]}", ""]
        if slots.get("exhibits"):
            ex = [[v.strip() for v in chunk.strip().rstrip(".").split(";")] for chunk in re.split(r"\bExhibit\s*:", slots["exhibits"])[1:]]
            if ex and all(len(e) == 4 for e in ex):
                parts += ["Exhibits", "", table(["File", "Captured", "Camera", "SHA-256"], ex)]
            else:
                parts += [f"Exhibits: {slots['exhibits']}", ""]
        body = "\n".join(parts)
    path = act["folder"] + "/" + title + ".md"
    n = 2
    while path in s["files"]:
        path = act["folder"] + f"/{title} ({n}).md"
        n += 1
    if run.scen.get("corrupt_save") and not s.get("corrupted"):
        m = re.search(r"\d+\.\d{2}(?= CAD)", body)
        if m:
            wrong = m.group(0)[:-1] + ("1" if m.group(0)[-1] != "1" else "2")
            body = body[:m.start()] + wrong + body[m.end():]
            s["corrupted"] = {"path": path, "was": m.group(0), "became": wrong}
    s["files"][path] = body
    s["modified"][path] = stamp
    return f"Saved as a new file. Real path: {path}"


# ---------------------------------------------------------------- commands
def cmd_init(run, name):
    scen = json.loads((DATA / "scenarios.json").read_text(encoding="utf-8"))[name]
    run.dir.mkdir(parents=True, exist_ok=True)
    for f in (run.log_file, run.state_file):
        if f.exists():
            f.unlink()
    home = run.lib["home"]
    run.s = {"scenario": scen, "name": name, "now": scen["now"], "phase": 1, "counter": 0, "pending": {},
             "folders": [home, home + "/Documents", home + "/Documents/Receipts", home + "/Downloads", home + "/Scans", home + "/Photos", home + "/Recordings"],
             "files": {}, "modified": {}, "albums": [], "tags": {}, "copies": {}}
    for path, text in scen.get("preload", {}).items():
        folder = str(Path(path).parent).replace("\\", "/")
        for f in (home + "/Home Contents", folder):
            if f not in run.s["folders"]:
                run.s["folders"].append(f)
        run.s["files"][path] = text
        run.s["modified"][path] = scen.get("preload_modified", scen["now"])
    for t, paths in scen.get("pretagged", {}).items():
        run.s["tags"][t] = paths
    run.save()
    print(f"run {run.dir} ready: scenario {name}")
    print("The user says: " + scen["user"])


def cmd_phase(run, n):
    ph = run.scen["phases"][n - 2]
    run.s["phase"], run.s["now"] = n, ph["now"]
    run.save()
    print(f"phase {n}. The user says: " + ph["user"])


def cmd_delegate(run, target, instruction, templates):
    bad = [name for name, pat in (("a brace", r"[{}]"), ("a pipe", r"\|"), ("an angle bracket", r"[<>]"), ("a line break", r"[\r\n]"), ("a command option", r"\s--[a-z]")) if re.search(pat, instruction)]
    if bad:
        state, text, tid, slots = "failed", "The instruction holds " + ", ".join(bad) + "; it was not run.", None, {"malformed": bad}
    else:
        tid, slots = match(templates, target, instruction)
        if tid is None:
            state = "failed"
            text = (f"The instruction is not one of this Skill's templates for {target} with every slot filled. Nearest template: {slots['nearest']} for {slots['nearest_target']} "
                    f"(similarity {slots['ratio']}). The first fixed wording of that template missing from your instruction, in order, is: \"{slots['near']}\". Send the template as written in SKILL.md, changing only the slots.")
        else:
            limit = MODEL_READS.get(tid)
            state, text = expert(run, tid, slots)
    run.log(kind="delegate", target=target, template=tid, slots=slots, chars=len(instruction), instruction=instruction, state=state, reply=text)
    run.save()
    print(f"state: {state}\n{text}")


def cmd_wait(run, aid, told):
    s = run.s
    act = s["pending"].pop(aid, None)
    if act is None:
        print("state: failed\nNo write is waiting under that approval id.")
        run.log(kind="wait", approval=aid, state="failed", told=told)
        return
    declined = act["kind"] in run.scen.get("decline", [])
    if declined:
        state, text = "cancelled", f"The user declined this write: {act['what']}. Nothing was changed."
    else:
        state, text = "completed", execute(run, act)
    run.log(kind="wait", approval=aid, write=act["kind"], template=act["tid"], state=state, told=told, reply=text, lines=act.get("lines"))
    run.save()
    print(f"state: {state}\n{text}")


def cmd_ask(run, question):
    # A message that asks several things gets every answer the scripted user has for it, once each.
    parts, rules = [], []
    for i, r in enumerate(run.scen.get("answers", [])):
        if r.get("phase") and r["phase"] != run.s.get("phase", 1):
            continue
        if re.search(r["match"], question, re.I | re.S) and r["answer"] not in parts:
            parts.append(r["answer"])
            rules.append(i)
    answer = " ".join(parts) or run.scen.get("default_answer", "Yes, go on.")
    run.log(kind="ask", question=question, rule=rules, answer=answer)
    print("The user answers: " + answer)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").add_argument("scenario")
    sub.add_parser("phase").add_argument("n", type=int)
    d = sub.add_parser("delegate")
    d.add_argument("--target", required=True)
    d.add_argument("--instruction", required=True)
    w = sub.add_parser("wait")
    w.add_argument("approval")
    w.add_argument("told", nargs="?", default="")
    for name in ("ask", "tell", "report"):
        sub.add_parser(name).add_argument("text")
    a = ap.parse_args()
    run = Run(a.run)
    if a.cmd == "init":
        return cmd_init(run, a.scenario)
    if run.s is None:
        sys.exit("run not initialised")
    if a.cmd == "phase":
        return cmd_phase(run, a.n)
    if a.cmd == "delegate":
        return cmd_delegate(run, a.target, a.instruction, load_templates())
    if a.cmd == "wait":
        return cmd_wait(run, a.approval, a.told)
    if a.cmd == "ask":
        return cmd_ask(run, a.text)
    run.log(kind=a.cmd, text=a.text)
    print("noted")


if __name__ == "__main__":
    main()
