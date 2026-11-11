# Dry runs against a mock NAS

Round 1 gives no hardware access, so the workflow was exercised on paper before submission: a model read `SKILL.md` as the Uliya parent would, issued each `delegate` call, and a second role answered as the expert agents from a fixed mock library ([fixture.md](fixture.md)) and nothing else.

| File | What it is |
| --- | --- |
| [fixture.md](fixture.md) | the mock library: photos with capture dates, receipts, an existing inventory, the user's answers |
| [claim-mode.md](claim-mode.md) | claim mode from the user's first sentence to the final report |
| [update-mode.md](update-mode.md) | update mode on a first run |
| [findings.md](findings.md) | 24 defects the first runs exposed, all applied to the Skill |
| [verification.md](verification.md) | a second pass on the corrected Skill: 12 more defects, all applied |
| [runs-2026-11-11.md](runs-2026-11-11.md) | three more runs on the day the package changed most: 33 more defects, all applied |

These transcripts record the Skill as it was on the day of each run, so step names differ in places from the current package: the old step C4 is now C4a and C4b, searches are grouped by route and room instead of one per item, the claim pack gained exhibit copies with SHA-256 values afterwards, and the saved list became a ledger of dated pages. The findings files say what changed and why.

A dry run shows that the instructions are complete and consistent. It says nothing about recall on a real library, which is measured on the NAS.
