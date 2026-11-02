"""The baseline: find the claim items with file names and dates only.

This is what a NAS without the AI index can do: `ug-filesystem find` by name
pattern and date range. No recognition index, no OCR, no vision model.

Usage:
  python tools/ablation_filename.py tmp/census/photos.csv --before 2026-06-20T00:00
      [--items results/june-2026-items.csv] [--out results/ablation-filename-date.md]

The items file has one row per claim line: number, item, keywords (pipe separated).
A keyword hits when it appears, case-insensitive, in the file name or in the
folder names under the library root. Folder names count because a user may
have sorted photos by hand; file names count because cameras sometimes write
words (Screenshot, PANO) and users sometimes rename.
"""
import argparse
import csv
import os
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("census")
    ap.add_argument("--before", default="2026-06-20T00:00")
    ap.add_argument("--items", default="results/june-2026-items.csv")
    ap.add_argument("--out", default="results/ablation-filename-date.md")
    args = ap.parse_args()

    photos = []
    with open(args.census, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["taken"] < args.before:
                photos.append(r["path"])
    names = [(p, os.path.basename(p).lower(), os.path.dirname(p).lower()) for p in photos]

    with open(args.items, encoding="utf-8") as f:
        items = list(csv.DictReader(f))

    def word_hit(text, kws):
        return any(re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", text) for k in kws)

    rows, hits_total = [], 0
    for it in items:
        kws = [k.strip().lower() for k in it["keywords"].split("|") if k.strip()]
        by_name = sorted({os.path.basename(p) for p, n, d in names if word_hit(n, kws)})
        by_folder = sorted({os.path.basename(p) for p, n, d in names if word_hit(d, kws)})
        hit = bool(by_name or by_folder)
        hits_total += hit
        rows.append((it["number"], it["item"], ", ".join(kws), by_name, by_folder, hit))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# Ablation: the same items searched by file name and date only\n\n")
        f.write(f"Run {datetime.now():%Y-%m-%d} with `tools/ablation_filename.py` over {len(photos)} photos "
                f"captured before {args.before.replace('T', ' ')} (the June 20, 2026 loss), on the pre-loss "
                "photos reachable from this PC. To be re-run on the NAS testing day with `ug-filesystem find` "
                "over the full library, which is what a NAS without the AI index offers.\n\n")
        f.write("Method: for each of the 27 claim items, a case-insensitive search of its keywords in the "
                "photo file names, and separately in the folder names, with no recognition index, no OCR and "
                "no vision model. A hit means at least one pre-loss file name or folder name contains a keyword.\n\n")
        f.write(f"**Result: {hits_total} of {len(items)} items found by file name or folder name.**\n\n")
        f.write("| # | Item | Keywords | Hits by file name | Hits by folder name | Found |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for n, item, kws, bn, bf, hit in rows:
            f.write(f"| {n} | {item} | {kws} | {'; '.join(bn) or 0} | {'; '.join(bf) or 0} | {'yes' if hit else 'no'} |\n")
        f.write("\nWhy it comes out this way: phone cameras name files by timestamp (20260617_063812.jpg), so a "
                "file name carries no content. Date alone cannot pick an item either, because nothing says which "
                "day a given belonging was photographed. Finding belongings in an unlabelled library needs the "
                "recognition index, the OCR text and the vision model, which is what the Skill delegates to.\n")
        note = os.path.join(os.path.dirname(args.out), "ablation-verification.md")
        if os.path.exists(note):
            with open(note, encoding="utf-8") as n:
                f.write("\n" + n.read())
    print(f"{hits_total} of {len(items)} items found; written to {args.out}")


if __name__ == "__main__":
    main()
