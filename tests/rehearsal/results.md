# Rehearsal results

A small, fast model played the NAS assistant. It was given the brief in [assistant-brief.md](assistant-brief.md) and the Skill package, and nothing else, and acted only through [tools/mock_nas.py](../../tools/mock_nas.py): a scripted NAS whose five experts answer from a made-up library ([library.json](library.json)) and whose user answers from a script ([scenarios.json](scenarios.json)). [tools/check_rehearsal.py](../../tools/check_rehearsal.py) then scored what it sent, what was saved and what it told the user. The mock accepts an instruction only if it is one of the Skill's templates with every slot filled, so a run also measures how often the model sent the template as written.

This is a fixture test. It shows that a small model can follow the instructions as written, that no write happens without approval, and that the checks hold on a made-up library. It says nothing about recall on a real library or about how the real experts behave: those wait for the NAS.

## Round 5: the package as submitted

**140 of 140 checks passed over 7 runs of 6 scenarios.** 148 delegations and 29 write approvals in all; 143 of 148 instructions were accepted as first sent, the rest corrected by the model and sent again. The longest instruction was 3,601 characters.

| Run | Scenario | Test-plan cases | Checks | Delegations | Accepted as first sent | Failed checks |
| --- | --- | --- | --- | --- | --- | --- |
| claim-voice-a | A claim from a voice walk-through, with no saved inventory | test-plan cases 1, 4, 5, 8, 12, 13, 14, 16, 20, 21 | 31 of 31 | 34 | 33 | none |
| claim-voice-b | A claim from a voice walk-through, with no saved inventory | test-plan cases 1, 4, 5, 8, 12, 13, 14, 16, 20, 21 | 31 of 31 | 33 | 32 | none |
| no-index-keyword | A library whose recognition has no household categories | test-plan case 27 | 17 of 17 | 16 | 15 | none |
| receipt-week-corrupt-save | A week with a new receipt and no new photo, and a save that comes back altered | test-plan cases 15, 24, 26 | 13 of 13 | 15 | 14 | none |
| refuse-redate | A request to change the date on a receipt | test-plan case 9 | 3 of 3 | 0 | 0 | none |
| theft-ledger-declines | A break-in with a saved inventory, camera events, and two approvals declined | test-plan cases 10, 19, and the camera step | 19 of 19 | 19 | 18 | none |
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

Failed in Round 1: claim-voice: no instruction is longer than 4,000 characters; claim-voice: no save carries more than ten rows and exhibit lines; claim-voice: the receipt price is on the row: sofa 1,799.99; claim-voice: the receipt price is on the row: fridge 219.99; update-then-ask: no instruction is longer than 4,000 characters; update-then-ask: no save carries more than ten rows and exhibit lines.

Failed in Round 2: claim-voice-a: no instruction is longer than 4,000 characters; claim-voice-a: no save carries more than ten rows and exhibit lines; claim-voice-a: the user is told about the assistant's own model before the first read; claim-voice-b: no instruction is longer than 4,000 characters; claim-voice-b: no save carries more than ten rows and exhibit lines; update-then-ask: no instruction is longer than 4,000 characters; update-then-ask: no save carries more than ten rows and exhibit lines.

Failed in Round 3: claim-voice-a: no instruction is longer than 4,000 characters; claim-voice-a: no save carries more than ten rows and exhibit lines; claim-voice-b: no instruction is longer than 4,000 characters; claim-voice-b: no save carries more than ten rows and exhibit lines; update-then-ask: no instruction is longer than 4,000 characters; update-then-ask: no save carries more than ten rows and exhibit lines.

Failed in Round 4: claim-voice-a: no instruction is longer than 4,000 characters; claim-voice-b: no instruction is longer than 4,000 characters.

## Notes

- Round 1 had a sixth run, the break-in. It is left out: the scripted user answered a question about the camera window with its answer about the exhibit copies, a fault in the mock's script that was fixed before round 2.
- The checks were tightened as the Skill was: the ten-line and 4,000-character checks were added when the Skill set those limits, and every round above is scored with today's checks.
- After the last round, the only change to the package is the AI-tools sentence in `references/disclosures.md`, which no step reads.
