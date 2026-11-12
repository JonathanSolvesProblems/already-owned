# Rehearsal results

A small, fast model played the NAS assistant. It was given the brief in [assistant-brief.md](assistant-brief.md) and the Skill package, and nothing else, and acted only through [tools/mock_nas.py](../../tools/mock_nas.py): a scripted NAS whose five experts answer from a made-up library ([library.json](library.json)) and whose user answers from a script ([scenarios.json](scenarios.json)). [tools/check_rehearsal.py](../../tools/check_rehearsal.py) then scored what it sent, what was saved and what it told the user. The mock accepts an instruction only if it is one of the Skill's templates with every slot filled, so a run also measures how often the model sent the template as written.

This is a fixture test. It shows that a small model can follow the instructions as written, that no write happens without approval, and that the checks hold on a made-up library. It says nothing about recall on a real library or about how the real experts behave: those wait for the NAS.

## Round 7: the package as submitted

**140 of 140 checks passed over 7 runs of 6 scenarios.** 149 delegations and 29 write approvals in all; 146 of 149 instructions were accepted as first sent; the rest were rejected by the mock as not matching a template. The longest instruction was 3,761 characters.

| Run | Scenario | Test-plan cases | Checks | Delegations | Accepted as first sent | Failed checks |
| --- | --- | --- | --- | --- | --- | --- |
| claim-voice-a | A claim from a voice walk-through, with no saved inventory | test-plan cases 1, 4, 5, 8, 12, 13, 14, 16, 20, 21 | 31 of 31 | 36 | 35 | none |
| claim-voice-b | A claim from a voice walk-through, with no saved inventory | test-plan cases 1, 4, 5, 8, 12, 13, 14, 16, 20, 21 | 31 of 31 | 35 | 34 | none |
| no-index-keyword | A library whose recognition has no household categories | test-plan case 27 | 17 of 17 | 15 | 14 | none |
| receipt-week-corrupt-save | A week with a new receipt and no new photo, and a save that comes back altered | test-plan cases 15, 24, 26 | 13 of 13 | 14 | 14 | none |
| refuse-redate | A request to change the date on a receipt | test-plan case 9 | 3 of 3 | 0 | 0 | none |
| theft-ledger-declines | A break-in with a saved inventory and camera events; the copies turned down, the album declined | test-plan cases 10, 19, and the camera step | 19 of 19 | 18 | 18 | none |
| update-then-ask | A first update, a second run that must write nothing, then a question | test-plan cases 2, 3, 6, 7, 14, 17 | 26 of 26 | 31 | 31 | none |

The logs of these runs (every instruction sent, every reply, every question and answer) are in [runs/](runs/), with each run's `checks.json`.

## Every round

Each round found gaps in the Skill's wording; they were fixed before the next. The same checks score every round.

| Round | Runs | Checks passed | Accepted as first sent |
| --- | --- | --- | --- |
| Round 1 | 5 | 84 of 90 | 88 of 95 |
| Round 2 | 7 | 133 of 140 | 133 of 146 |
| Round 3 | 7 | 134 of 140 | 138 of 148 |
| Round 4 | 7 | 138 of 140 | 138 of 142 |
| Round 5 | 7 | 140 of 140 | 143 of 148 |
| Round 6 | 7 | 133 of 140 | 132 of 137 |
| Round 7 | 7 | 140 of 140 | 146 of 149 |

Failed in Round 1: claim-voice: no instruction is longer than 4,000 characters; claim-voice: no save carries more than ten rows and exhibit lines; claim-voice: the receipt price is on the row: sofa 1,799.99; claim-voice: the receipt price is on the row: fridge 219.99; update-then-ask: no instruction is longer than 4,000 characters; update-then-ask: no save carries more than ten rows and exhibit lines.

Failed in Round 2: claim-voice-a: no instruction is longer than 4,000 characters; claim-voice-a: no save carries more than ten rows and exhibit lines; claim-voice-a: the user is told about the assistant's own model before the first read; claim-voice-b: no instruction is longer than 4,000 characters; claim-voice-b: no save carries more than ten rows and exhibit lines; update-then-ask: no instruction is longer than 4,000 characters; update-then-ask: no save carries more than ten rows and exhibit lines.

Failed in Round 3: claim-voice-a: no instruction is longer than 4,000 characters; claim-voice-a: no save carries more than ten rows and exhibit lines; claim-voice-b: no instruction is longer than 4,000 characters; claim-voice-b: no save carries more than ten rows and exhibit lines; update-then-ask: no instruction is longer than 4,000 characters; update-then-ask: no save carries more than ten rows and exhibit lines.

Failed in Round 4: claim-voice-a: no instruction is longer than 4,000 characters; claim-voice-b: no instruction is longer than 4,000 characters.

Failed in Round 6: claim-voice-b: proven with the right pre-loss photo: sofa; claim-voice-b: proven with the right pre-loss photo: dumbbell; claim-voice-b: proven with the right pre-loss photo: vacuum; claim-voice-b: proven with the right pre-loss photo: power tower; claim-voice-b: the receipt price is on the row: sofa 1,799.99; claim-voice-b: the receipt price is on the row: vacuum 799.99; claim-voice-b: the receipt price is on the row: power tower 389.00.

## Notes

- Round 1 had a sixth run, the break-in. It is left out: the scripted user answered a question about the camera window with its answer about the exhibit copies, a fault in the mock's script that was fixed before round 2.
- The checks were tightened as the Skill was: the ten-line and 4,000-character checks were added when the Skill set those limits, and every round above is scored with today's checks.
- Rounds 6 and 7 ran after the claim search was changed to describe nine photos spread across the capture dates instead of the eight latest (the version note in `references/disclosures.md` says why). In round 6, one run asked about the items of the voice walk-through instead of listing them; the user's reply did not answer, and under the rule that an unanswered question decides nothing, four lost items were left off the claim. C2 and C3 now keep what the user names, typed or spoken, on the list unless the user removes it. Round 6 also found three wording gaps, fixed before round 7: a receipt for a row already in the ledger, the exhibit line when the copies are declined, and what continuing a claim search means.
- One check in the altered-save scenario, "the mock altered one saved value", confirms the mock did its part rather than testing the assistant.
- After the last round, nothing in the package changed.
