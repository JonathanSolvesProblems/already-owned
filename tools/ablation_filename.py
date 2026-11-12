"""The baseline: find the claim items with file names and dates only.

This is what a NAS without recognition can do: a search by name pattern and date range. No
recognition index, no text recognition, no vision model.

Usage:
  python tools/ablation_filename.py photos.csv [more.csv ...] --before 2026-06-20T00:00
      [--items results/june-2026-items.csv] [--out my-baseline.md] [--verification checked.md]

Each photo list is a CSV with the columns path and taken (the capture time, written 2026-06-17T06:38:12,
2026-06-17 06:38 or 2026:06:17 06:38:12; a row with no capture time is left out). Several lists are
merged, and a photo that appears in two of them is counted once.

The items file has one row per claim line: number, item, keywords (pipe separated). A keyword hits
when it appears as a whole word, singular or plural, case-insensitive, in the file name or in a folder name
on the path. Folder names
count because a user may have sorted photos by hand; file names count because cameras sometimes
write words (Screenshot, PANO) and users sometimes rename.

A raw hit is not a find. It counts only when the photo shows the item, which a person has to check.
"""
import argparse
import csv
import os
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")


def when(text):
    """A capture time as written by a camera or a census: 2026-06-17T06:38:12, 2026-06-17 06:38, 2026:06:17 06:38:12."""
    m = re.match(r"\s*(\d{4})[-:](\d{2})[-:](\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?", text or "")
    if not m:
        return None
    y, mo, d, h, mi, s = (int(v) if v else 0 for v in m.groups())
    return datetime(y, mo, d, h, mi, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("census", nargs="+")
    ap.add_argument("--before", default="2026-06-20T00:00")
    ap.add_argument("--items", default="results/june-2026-items.csv")
    ap.add_argument("--out", default="my-baseline.md")
    ap.add_argument("--verification", help="a Markdown file of hits checked by eye, appended to the report")
    args = ap.parse_args()
    before = when(args.before)
    if before is None:
        sys.exit(f"--before is not a date and time: {args.before}")

    photos, seen, undated = [], set(), 0
    for census in args.census:
        with open(census, encoding="utf-8-sig") as f:  # -sig: a list saved by Excel starts with a byte-order mark
            for r in csv.DictReader(f):
                key = (r.get("md5_64k") or r["path"], r.get("bytes"))
                taken = when(r.get("taken", ""))
                if taken is None:
                    undated += 1
                    continue
                if taken < before and key not in seen:
                    seen.add(key)
                    photos.append(r["path"].replace("\\", "/"))
    names = [(os.path.basename(p), os.path.dirname(p)) for p in photos]

    with open(args.items, encoding="utf-8-sig") as f:
        items = list(csv.DictReader(f))

    def word_hit(text, kws):
        # a keyword hits as a whole word, singular or plural (lamp, lamps; bench, benches)
        return any(re.search(r"(?<![a-z])" + re.escape(k) + r"(?:e?s)?(?![a-z])", text) for k in kws)

    rows, hits_total = [], 0
    for it in items:
        kws = [k.strip().lower() for k in it["keywords"].split("|") if k.strip()]
        by_name = sorted({n for n, d in names if word_hit(n.lower(), kws)})
        folders = {}
        for n, d in names:
            for part in d.split("/"):
                if word_hit(part.lower(), kws):
                    folders[part] = folders.get(part, 0) + 1
        by_folder = [f"a folder named {k} ({v} photos)" for k, v in sorted(folders.items())]
        hit = bool(by_name or by_folder)
        hits_total += hit
        rows.append((it["number"], it["item"], ", ".join(kws), by_name, by_folder, hit))

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# Baseline: the same items searched by file name and date only\n\n")
        f.write(f"Run {datetime.now():%Y-%m-%d} with `tools/ablation_filename.py` over {len(photos)} photos captured before "
                f"{args.before.replace('T', ' ')}, from {len(args.census)} photo list(s), each photo counted once"
                f"{f'; {undated} photo(s) with no capture time were left out' if undated else ''}. "
                "This is what a NAS without recognition offers: a search by name and by date.\n\n")
        f.write(f"Method: for each of the {len(items)} items, a case-insensitive search of its keywords in the photo file names, "
                "and separately in the folder names, with no recognition index, no text recognition and no vision model. "
                "A raw hit means at least one file name or folder name contains a keyword. A raw hit is not a find: "
                "it counts only if the photo shows the item, which is checked by eye further down.\n\n")
        f.write(f"**Raw hits: {hits_total} of {len(items)} items have a file name or a folder name that contains a keyword.**\n\n")
        f.write("| # | Item | Keywords | Hits by file name | Hits by folder name | Raw hit |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for n, item, kws, bn, bf, hit in rows:
            f.write(f"| {n} | {item} | {kws} | {'; '.join(bn) or 0} | {'; '.join(bf) or 0} | {'yes' if hit else 'no'} |\n")
        f.write("\nWhy it comes out this way: phone cameras name files by timestamp (20260617_063812.jpg), so a "
                "file name carries no content. Date alone cannot pick an item either, because nothing says which "
                "day a given belonging was photographed. Finding belongings in an unlabelled library needs the "
                "recognition index, the text in the photo and the vision model, which is what the Skill delegates to.\n")
        if args.verification:
            with open(args.verification, encoding="utf-8-sig") as n:
                f.write("\n" + n.read())
    print(f"{hits_total} of {len(items)} items with a raw hit, over {len(photos)} photos; written to {args.out}")


if __name__ == "__main__":
    main()
