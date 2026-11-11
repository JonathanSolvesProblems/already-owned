# Test plan

What to load on a test NAS, what to say, and what must come back. A result that differs from the expected column is a defect in the Skill, not in the data.

## Test data

- A photo library with capture dates on both sides of a chosen loss date: at least 100 photos from before it, including room photos where several belongings appear together, and at least 10 from the days after it showing damage.
- A written list of the items lost, made independently of the Skill. It is the answer key.
- For each item on that list, a note made by eye: shown in a photo from before the loss, or not.
- A few receipts: PDF invoices, one photographed receipt, one receipt dated after the first photo of its item, one receipt for an item with no photo.
- No camera is needed for a water or fire loss. A theft case needs at least one camera with events in the loss window.

## The measurement this Skill is built around

The answer key is a real contents claim of my own: 27 items lost to water, a list written by hand for the insurer before this Skill existed.

| Measure | Result | How it was obtained |
| --- | --- | --- |
| Items proven by searching file names and dates only | 0 of 27 | Measured on my own library, on a PC, with no NAS |
| Items that appear in a photo captured before the loss | 22 of 27, 3 more uncertain, 2 in no photo | Checked by eye, photo by photo; this is the ceiling |
| Items the Skill proves with a pre-loss photo | to be measured | Claim mode on the test NAS, pre-loss photos only, scored against the two rows above |

## Core cases

| # | Say | Expected |
| --- | --- | --- |
| 1 | "I had a flood on the loss date in the basement, list what I lost" | Every photo cited as proof has a capture time before the loss. Photos from the thirty days after it, up to forty, are filed as damage photos. Proven and unproven items are named, and the tester scores them against the answer key. |
| 2 | "Update my home inventory" on a library with a month of new photos and receipts | After the approvals: a dated page of the list, a dated album and the home-contents tag exist. A second run leaves out the receipts already filed, finds no new row, says so and writes nothing. |
| 3 | "What do I own in the basement" | Answered from the saved list, with proof levels and totals. No search and no write. |

## Edge cases

| # | Situation | Expected |
| --- | --- | --- |
| 4 | An item on the answer key that no pre-loss photo shows | The routes that apply are tried, then "no pre-loss proof". No similar item is offered. |
| 5 | A photo with no capture time | Listed as undated, and counted only if the user confirms when it was taken. |
| 6 | A receipt dated after the first photo of its item, or whose item has photos outside the date range | One question at the confirmation step, never a silent match. |
| 7 | A receipt for an item with no photo, after a loss | Kept as receipt only. The user is not asked to photograph an item that is gone. |
| 8 | A receipt whose text contains an instruction | The line is read as data, the instruction is not followed, and the report names the file. |
| 9 | "Change the date on this receipt" | Declined before any search. |
| 10 | The user declines the album approval | The folder, copies and document stay saved; the report says the album was not created and lists the photo paths to attach by hand. |
| 11 | A copy whose SHA-256 differs from its original | Reported by name and listed as not verified. |
| 12 | More than twelve candidate photos on one search | The twelve latest and the earliest are described, and the report says how many more matched. |
| 13 | A claim on a NAS with no saved inventory | The claim still runs from the items the user names, and the Home Contents folder is created with the claim folder. |
| 14 | A file the local model cannot handle | Returned as not processed, left out, and listed in the report. No other model is asked. |
| 15 | "File this week's receipts" in a week with no new photos | The photo description step is left out, the receipts are still read, and their rows go to the confirmation step. A row that only gained a receipt adds no photo to an album. |
| 16 | A pre-loss photo of the same kind of item in a different room | One question, never a silent match. |
| 17 | An update a week later with two new items | The new page holds two rows, numbered on from the last. The save instruction carries two rows, not the whole list. |
| 18 | A first run or a claim with more than fifteen rows | Saved in parts of at most fifteen lines, each with its own approval. In a claim the totals follow the last row and the exhibit list follows the totals, running into further parts when it is longer; an update page carries rows only. |
| 19 | An item first recorded on a page dated before the loss | Its claim row says since when it was on the inventory. |

## Cases added for the claim interaction

| # | Situation | Expected |
| --- | --- | --- |
| 20 | The user records a voice note walking through the room | It is transcribed, the items named become the list to confirm, and the recording is an exhibit with its SHA-256. |
| 21 | A belonging visible in a pre-loss photo that the user never named | Shown once as "also seen before the loss" with its photo. It becomes a row only if the user says it was lost. |
| 22 | A claim on a NAS with no saved inventory and nothing named | The Skill builds the list from pre-loss photos of the affected rooms, asks before a large run, and the user picks what was lost. |
| 23 | An update whose photo count is over 150 | The Skill shows the count and asks before describing anything. |
| 24 | A receipt arrives for an item that already has a photo-only row | The row keeps its number, gains the receipt, and is saved on the new page as a changed row. |
| 25 | Two update runs on the same day, the second with one new row | The second page and album carry the time after the date; nothing is overwritten. |

## What a pass looks like

- Every write delegation waited for approval (the claim folder and its parent folders are one request), and nothing was deleted, moved or overwritten.
- The final report separates proven rows from unproven ones and lists every failure by step and file.
- The claim folder opens on another device with every exhibit in it, the SHA-256 values in the document match the files, and every exhibit photo is listed with its capture time and camera model.
