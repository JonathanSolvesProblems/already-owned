# Sources

Every number or quotation used in the proposal, the README or the replay page, with where it comes from.

## Measured by this project

| Statement | Source |
| --- | --- |
| 27 items, $10,915 CAD on the June 2026 contents list | my own claim list, written for my insurer before the Skill existed; items in `results/june-2026-items.csv` (value per unit; times the quantity they add up to $10,915) |
| File-name-and-date search proves 0 of 27, over 1,769 pre-loss photos | `results/ablation-filename-date.md`: 9 raw hits, every one checked by eye in `results/ablation-verification.md` |
| 22 of 27 items appear in a pre-loss photo, 3 uncertain, 2 in none (counted by hand) | `results/pre-loss-photo-census.md`; the camera rig, one of the 2, found later by the recall measurement, is under "Found after this count" |
| With a local stand-in for the NAS, the Skill proves 13 of the 22 on the first pass ($6,945 of $10,915), 15 continuing; 11 and 13 with the earlier eight-latest cap | `results/recall-standin.md` and `.json`, made by `python tools/recall_standin.py report` (needs Ollama and the photos, which stay on my computer); every cited photo's verdict in `results/recall-standin-checks.csv` |
| 1,749 photos read by the stand-in, of 1,769 before the loss | the other 20 are kept only in the cloud, with no copy on the computer |
| 24 steps, 25 delegation templates, 5 experts, seven references, checker static-pass | `python tools/check_package.py`, and UGREEN's `check-skill.mjs` |
| 28 of the catalog's 78 actions | `skill/home-contents-inventory/references/capability-map.md` |
| Model rehearsal: 140 of 140 checks over 7 runs, 7 rounds | `tests/rehearsal/results.md`, logs in `tests/rehearsal/runs/` |
| Five paper dry runs, 69 defects found and fixed | `tests/dry-run/findings.md` (24), `verification.md` (12), `runs-2026-11-11.md` (33) |

## Published sources

| Statement | Source |
| --- | --- |
| "They want a model number. They want the price. The quantity." | Selina Clark, former insurance adjuster, quoted in The New York Times, February 6, 2025; reposted by United Policyholders at https://uphelp.org/the-agony-of-the-list/ |
| "It's very, very rare." (on policyholders having a home inventory before a loss) | Jay Straughan, vice president of claims at Enservio, in Insurance Journal, September 8, 2014: https://www.insurancejournal.com/magazines/mag-features/2014/09/08/339278.htm |
| "nearly half of U.S. residents (44%) have never made a home inventory list" | Farmers Insurance news release, March 20, 2019: https://insurancenewsnet.com/oarticle/farmers-insurance-study-finds-almost-half-of-u-s-residents-do-not-have-a-home-inventory-list-should-a-disaster-strike |

## Not yet measured

The number of the 27 items the Skill itself proves on a real NAS, with the NAS's own index and experts instead of the stand-in. It is measured on the finalist testing day and will be added to `results/` with the run it came from.
