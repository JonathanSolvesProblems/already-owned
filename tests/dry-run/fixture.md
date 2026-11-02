# Dry-run fixture: a mock NAS for walking the Skill without the hardware

This describes the state of a UGREEN NAS for one user, so that a model playing the Uliya parent can walk `skill/home-contents-inventory/SKILL.md` end to end and a second role can answer each delegation from this state. The state is modelled on a real June 2026 basement flood (items, quantities and prices are the real claim lines; file names are the real phone file names), with every address, policy and claim number left out.

Nothing in this file is a path or identifier the Skill may assume at runtime. The Skill only learns these values through delegation results.

## User and personal space

- Current user: `jon`. Personal space root as returned by `file-workflow get-user-dir`: `/home/me`.
- Folders: `/home/me/Documents`, `/home/me/Documents/Receipts`, `/home/me/Downloads`, `/home/me/Scans`, `/home/me/Photos` (the library, indexed), `/home/me/Photos/Camera` (phone backup, 2,140 photos from 2024-02 to 2026-11).
- Scenario A (claim mode) has `/home/me/Home Contents/Home contents list 2026-05-30.md` present (contents below). Scenario B (update mode, first run) has no `Home Contents` folder.

## Photo library index: recognized object categories (counts of photos before 2026-06-20)

sofa 14, television 9, chair 31, bed 6, table 22, bicycle 3, dumbbell 2, vacuum cleaner 1, refrigerator 4, washing machine 2, lamp 7, bookcase 5, suitcase 3, person 410, dog 52, food 118, document 36, screenshot 220.

No category exists for: power tower, boot dryer, garment steamer, monitor arm, camera rig, road case, picture frame, shelving.

## Photos that matter (path, capture time, what is visible, OCR text if any)

Pre-loss (before 2026-06-20 00:00):

| Path | Captured | Visible | OCR text |
| --- | --- | --- | --- |
| /home/me/Photos/Camera/20240815_190211.jpg | 2024-08-15 19:02 | basement: brown leather reclining sofa, 55" TV on a stand, two curved-leg side tables | none |
| /home/me/Photos/Camera/20240815_190230.jpg | 2024-08-15 19:02 | same sofa from the side, floor lamp with round base | none |
| /home/me/Photos/Camera/20240903_121544.jpg | 2024-09-03 12:15 | Dyson stick vacuum on its wall dock, box beside it | "dyson V11" on the box |
| /home/me/Photos/Camera/20250118_164002.jpg | 2025-01-18 16:40 | gaming chair at a desk, monitor on a desk arm | none |
| /home/me/Photos/Camera/20250301_121500.jpg | 2025-03-01 12:15 | a paper receipt, photographed on a table | "LEON'S  ... RECLINER SOFA 3S BROWN LEATHER 1,799.99 ... SUBTOTAL 1,799.99 HST 234.00 TOTAL 2,033.99 ... 2025-03-01" |
| /home/me/Photos/Camera/20250412_101233.jpg | 2025-04-12 10:12 | power tower (pull-up and dip station) being assembled, instruction sheet | "POWER TOWER" on the box |
| /home/me/Photos/Camera/20251204_142223.jpg | 2025-12-04 14:22 | dining area (ground floor): hutch, table, chairs, blanket on wet floor | none |
| /home/me/Photos/Camera/20260410_083012.jpg | 2026-04-10 08:30 | adjustable dumbbell set on the basement floor beside the sofa | "52.5 LB" on the dumbbell |
| /home/me/Photos/Camera/20260517_142210.jpg | 2026-05-17 14:22 | washer and dryer pair in the laundry room | "amana" on the control panel |
| /home/me/Photos/Camera/20260601_201500.jpg | 2026-06-01 20:15 | friends on the sofa, TV on, mini-fridge visible in the corner | none |

Post-loss (damage photos, after 2026-06-20 00:00):

| Path | Captured | Visible |
| --- | --- | --- |
| /home/me/Photos/Camera/20260621_093406.jpg | 2026-06-21 09:34 | gaming chair and coffee table in standing water |
| /home/me/Photos/Camera/20260622_023921.jpg | 2026-06-22 02:39 | sofa and TV, water line on the sofa base |
| /home/me/Photos/Camera/20260622_121507.jpg | 2026-06-22 12:15 | Dyson vacuum and two floor lamps, wet |
| /home/me/Photos/Camera/20260622_182035.jpg | 2026-06-22 18:20 | mini-fridge on its side |
| /home/me/Photos/Camera/20260623_154028.jpg | 2026-06-23 15:40 | camera rig in a wet case |

## Receipt files

| Path | Modified | Content when extracted |
| --- | --- | --- |
| /home/me/Documents/Receipts/Dyson-V11-invoice-2024-09-02.pdf | 2024-09-02 | Dyson Canada, 2024-09-02, "Dyson V11 Torque Drive" qty 1, 799.99 CAD |
| /home/me/Downloads/Amazon-order-112-4471-2025-04-08.pdf | 2025-04-08 | Amazon.ca, 2025-04-08, "Power Tower Pull Up Dip Station" qty 1, 389.00 CAD; "USB cable" qty 2, 9.99 CAD |
| /home/me/Scans/danby-mini-fridge-2025-11-22.jpg | 2025-11-22 | a scanned paper receipt: `ug-document extract` fails on it ("unsupported file type: image"); `vision-ocr` reads "DANBY 3.3 CU FT COMPACT REFRIGERATOR 219.99 ... TOTAL 252.93 ... 2025-11-22" |

## Surveillance

No cameras are registered for this user. `ug-surveillance cameras` returns an empty list.

## Existing inventory (scenario A only): /home/me/Home Contents/Home contents list 2026-05-30.md

| # | Item | Description | Room | Qty | Purchase date | Price paid | Replacement value | Pre-loss photo | Receipt | Proof level | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Leather reclining sofa, 3-seat | brown leather, 3-seat, recliner | Basement | 1 | 2025-03-01 | 1,799.99 CAD | | 20240815_190211.jpg (2024-08-15) | 20250301_121500.jpg | photo and receipt | receipt read from photo text; photo predates receipt date, user confirmed it is the same sofa bought earlier and the receipt is a replacement mechanism invoice |
| 2 | Flat-screen TV, about 55" | brand not visible, black | Basement | 1 | | | | 20240815_190211.jpg (2024-08-15) | | photo only | |
| 3 | Stick vacuum | Dyson V11 | Basement | 1 | 2024-09-02 | 799.99 CAD | | 20240903_121544.jpg (2024-09-03) | Dyson-V11-invoice-2024-09-02.pdf | photo and receipt | |
| 4 | Pull-up and dip station | power tower, black steel | Basement | 1 | 2025-04-08 | 389.00 CAD | | 20250412_101233.jpg (2025-04-12) | Amazon-order-112-4471-2025-04-08.pdf | photo and receipt | |
| 5 | Gaming chair | black and red, not visible brand | Basement | 1 | | | | 20250118_164002.jpg (2025-01-18) | | photo only | |

## The user's words

Scenario A, claim mode: "I had a flood on June 20 around 2 am in the basement. List what I lost. Insurer Northgate Insurance, no claim number yet." When asked for items beyond the inventory, the user names: wooden armchair, oak bed frame, two side tables, coffee table, hex side table, dumbbell set, bookshelf, two storage shelving units, flight case, camera rig, chrome shelving, two floor lamps, Danby mini-fridge, Amana washer and dryer, boot dryer, garment steamer, monitor arm, diploma frames, bedding, boxes and bags of belongings. The user confirms every row shown and supplies replacement values only when asked at the confirm step (sofa 1,800; TV 700; chair 300; the rest left empty for the dry run).

Scenario B, update mode, first run: "Update my home inventory." When asked how far back to go: "two years".

## Behaviour of the experts in this dry run

- Every expert answers only from this fixture. Anything not listed here does not exist and returns no results.
- Reads return `completed`. Writes return `waiting_approval` first, then `completed` once the user approves, with a real identifier (album uuid `alb-7f3a`, tag id `tag-12`, folder and file paths under `/home/me/Home Contents`).
- `ug-document extract` on `/home/me/Scans/danby-mini-fridge-2025-11-22.jpg` returns `failed` with "unsupported file type: image".
- `vision-vlm` describes exactly what the Visible column says and nothing more; brand text is readable only where the OCR column has it.
