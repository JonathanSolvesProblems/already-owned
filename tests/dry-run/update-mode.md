# Dry run B: update mode, first run

Fixture: `tests/dry-run/fixture.md`, scenario B (no Home Contents folder). Skill: `skill/home-contents-inventory/SKILL.md`. Today is 2026-11-02. Current user `me`. The same conventions as `claim-mode.md` apply: templates are filled with real values before sending, index hits the fixture does not describe cannot be confirmed by the vision check, and the five status words are the platform's.

Update mode has no notion of a loss, so the post-loss photos of June 2026 are ordinary library photos here.

---

## U1. Find the existing inventory

**User:** "Update my home inventory."

**Parent:** update mode. Issues U1 verbatim.

```text
delegate --target file-agent --instruction 'Find the folder named Home Contents in the personal space of the current user. If it exists, return its real path, and the real path, modification date and full text of the newest Markdown file in it whose name starts with Home contents list. If the folder does not exist, report that it does not exist. Read only: create, move or change nothing.'
```

**Expert file-agent, completed.** [file-workflow get-user-dir; ug-filesystem find --path /home/me --pattern "Home Contents" --type dir] The folder Home Contents does not exist in `/home/me`.

**Parent next:** first run. Tells the user and asks the date range:

> You have no Home Contents folder yet, so this is the first run and the inventory starts empty. How far back should I look through your photos and receipts?

**Status:** waiting_user (parent-level).

**User:** "two years"

**Parent next:** confirmed date range 2024-11-02 to 2026-11-02. (The Dyson invoice of 2024-09-02 and the August 2024 sofa photos fall outside it.)

---

## U2. Find which kinds of belongings the photos show

```text
delegate --target photo-agent --instruction 'Using the recognition index of the photo library of the current user, list the recognized object categories that are durable household belongings an insurer would cover: furniture, televisions and screens, computers, phones and tablets, cameras, kitchen and laundry appliances, bicycles, musical instruments, tools, sports equipment, jewellery and artwork. For each category return its name and the number of matching photos taken between 2024-11-02 and 2026-11-02. Exclude people, pets, food, documents and screenshots. If no category matches, return an empty result and say so. Read only.'
```

**Expert photo-agent, completed.** [ug-photo object-albums for the category list; ug-photo search-picture --ai-object-name per category --start-time 2024-11-02 --end-time 2026-11-02 --total-judge for counts]
- Categories kept: sofa, television, chair, bed, table, bicycle, dumbbell, vacuum cleaner, refrigerator, washing machine, lamp, bookcase, suitcase (13). Excluded: person, dog, food, document, screenshot.
- Counts: the fixture only gives counts "before 2026-06-20" (sofa 14, television 9, chair 31, bed 6, table 22, bicycle 3, dumbbell 2, vacuum cleaner 1, refrigerator 4, washing machine 2, lamp 7, bookcase 5, suitcase 3); the expert reports those as the best available figure and says so.

**Parent next:** shows the 13 categories with counts and asks which to include.

**Status:** waiting_user (parent-level).

**User:** "All of them."

---

## U3. Find and describe each distinct item (13 delegations)

For a category the search-routes table always gives "recognized object" (a common object type), so the route clause is the same in every delegation; only the category changes. The first delegation is shown in full; the others differ only in the category name and are listed with their results.

### U3.1 sofa

```text
delegate --target photo-agent --instruction 'For the household object category sofa, search the photos of the current user taken between 2024-11-02 and 2026-11-02, using the search route recognized object, object name sofa. Group photos that show the same physical item. For each distinct item, pick the clearest photo and describe it with the local vision model: item type, brand and model only if readable in the photo, colour, material, approximate size, and the room if it can be seen. Return per item the description, the real path and capture date of the chosen photo, and the real paths of other photos of the same item. Write not visible instead of guessing a brand or model. If nothing is found, return no results for this category. Read only.'
```

**Expert photo-agent, completed.** [search-picture --ai-object-name sofa --start-time --end-time; vision-vlm on each hit]
- One distinct sofa, 3 confirmed photos: `/home/me/Photos/Camera/20260601_201500.jpg` (2026-06-01 20:15, chosen: sofa fully in frame with the TV), `/home/me/Photos/Camera/20260410_083012.jpg` (2026-04-10, sofa beside a dumbbell set, basement floor), `/home/me/Photos/Camera/20260622_023921.jpg` (2026-06-22, sofa and TV, water line on the base).
- Description: sofa; brand, model, colour and material not visible in these photos; room basement.

### U3.2 television

Same instruction with "category television" and "object name television".

**Completed.** One TV: chosen `/home/me/Photos/Camera/20260601_201500.jpg` (2026-06-01, TV switched on); other `/home/me/Photos/Camera/20260622_023921.jpg`. Brand and size not visible; room basement.

### U3.3 chair

Same instruction with "category chair" and "object name chair".

**Completed.** Two distinct items. (a) Gaming chair: chosen `/home/me/Photos/Camera/20250118_164002.jpg` (2025-01-18 16:40, at a desk, monitor on a desk arm); other `/home/me/Photos/Camera/20260621_093406.jpg` (2026-06-21, in standing water with a coffee table); brand not visible, room not visible. (b) Dining chairs: `/home/me/Photos/Camera/20251204_142223.jpg` (2025-12-04 14:22, dining area, ground floor, with a hutch and a table); number of chairs not clear; brand not visible.

### U3.4 bed

Same instruction with "category bed" and "object name bed".

**Completed, no results for this category.** 6 index hits, none described by the fixture; the vision check confirmed a bed in none.

### U3.5 table

Same instruction with "category table" and "object name table".

**Completed.** Two distinct items. (a) Dining table: `/home/me/Photos/Camera/20251204_142223.jpg` (2025-12-04, dining area, ground floor; a hutch is also visible); material not visible. (b) Coffee table: `/home/me/Photos/Camera/20260621_093406.jpg` (2026-06-21 09:34, in standing water beside the gaming chair); material not visible; room not visible.

### U3.6 bicycle

**Completed, no results for this category.** 3 index hits, none confirmed.

### U3.7 dumbbell

**Completed.** One adjustable dumbbell set: `/home/me/Photos/Camera/20260410_083012.jpg` (2026-04-10 08:30, basement floor beside the sofa); marking 52.5 LB readable; brand not visible.

### U3.8 vacuum cleaner

**Completed.** One stick vacuum: `/home/me/Photos/Camera/20260622_121507.jpg` (2026-06-22 12:15, with two floor lamps, wet); no brand text readable in this photo, so brand not visible; room not visible. (The 2024-09-03 photo with the Dyson box is outside the confirmed range.)

### U3.9 refrigerator

**Completed.** One mini-fridge: chosen `/home/me/Photos/Camera/20260601_201500.jpg` (2026-06-01, in the corner of the basement room); other `/home/me/Photos/Camera/20260622_182035.jpg` (2026-06-22, on its side). Brand not visible.

### U3.10 washing machine

**Completed.** Two distinct items side by side in `/home/me/Photos/Camera/20260517_142210.jpg` (2026-05-17 14:22, laundry room): a washer and a dryer, brand Amana readable on the control panel, models not readable.

### U3.11 lamp

**Completed.** Two floor lamps side by side in `/home/me/Photos/Camera/20260622_121507.jpg` (2026-06-22, wet, with the stick vacuum); brand not visible; room not visible. (The 2024-08-15 photo of one lamp is outside the range.)

### U3.12 bookcase

**Completed, no results for this category.** 5 index hits, none confirmed.

### U3.13 suitcase

**Completed, no results for this category.** 3 index hits, none confirmed.

**Parent next:** 12 items found (sofa, TV, gaming chair, dining chairs, dining table, coffee table, dumbbell set, stick vacuum, mini-fridge, washer, dryer, floor lamps x2). The existing list is empty, so "already on the existing list" matches nothing. Goes to U4.

---

## U4. Find receipt files

```text
delegate --target file-agent --instruction 'In the Documents, Downloads and Scans folders of the personal space of the current user, find PDF and image files modified between 2024-11-02 and 2026-11-02 whose names or locations suggest receipts, invoices or order confirmations. Return each real path, name and modification date. If none are found, return no results. Read only.'
```

**Expert file-agent, completed.** [get-user-dir; ug-filesystem find per folder --type documents and --type image with --date-type for modification time, --start-timestamp, --end-timestamp]
- `/home/me/Downloads/Amazon-order-112-4471-2025-04-08.pdf` (modified 2025-04-08).
- `/home/me/Scans/danby-mini-fridge-2025-11-22.jpg` (modified 2025-11-22).
- The Dyson invoice (modified 2024-09-02) is outside the range and not returned.

---

## U5. Find receipts that were photographed

```text
delegate --target photo-agent --instruction 'Search the photos of the current user taken between 2024-11-02 and 2026-11-02 for receipts and invoices, using the text recognized in the photo (words such as total, subtotal, receipt, invoice, tax). Return the real path and capture date of each photo that shows a receipt, and the full recognized text of each one. If none are found, return no results. Read only.'
```

**Expert photo-agent, completed.** [search-picture --ocr-contains total, --ocr-contains subtotal, --ocr-contains receipt, --ocr-contains invoice, --ocr-contains tax, with --start-time and --end-time; vision-ocr on each hit]
- `/home/me/Photos/Camera/20250301_121500.jpg` (2025-03-01 12:15): a paper receipt on a table. Recognized text: "LEON'S ... RECLINER SOFA 3S BROWN LEATHER 1,799.99 ... SUBTOTAL 1,799.99 HST 234.00 TOTAL 2,033.99 ... 2025-03-01".
- No other photo in the range carries receipt words.

---

## U6. Extract the purchase lines

Union of U4 and U5 paths: three files.

```text
delegate --target document-agent --instruction 'Extract the purchased line items from the receipt and invoice files at these real paths: /home/me/Downloads/Amazon-order-112-4471-2025-04-08.pdf, /home/me/Scans/danby-mini-fridge-2025-11-22.jpg and /home/me/Photos/Camera/20250301_121500.jpg: merchant, purchase date, item description, brand and model if printed, quantity, price paid and currency, and the source path. Keep text in its original language and add a short English item description. Ignore groceries, restaurants, fuel, services and subscriptions. Report each file that could not be read as a failure with its path. If no durable household item is found, return an empty result. Read only.'
```

**Expert document-agent, completed with two file failures.** [ug-document extract --schema receipt --file per path]
- Amazon.ca, 2025-04-08: Power Tower Pull Up Dip Station, qty 1, 389.00 CAD; USB cable, qty 2, 9.99 CAD each. Source Amazon-order-112-4471-2025-04-08.pdf.
- Failure: `/home/me/Scans/danby-mini-fridge-2025-11-22.jpg`, unsupported file type: image.
- Failure: `/home/me/Photos/Camera/20250301_121500.jpg`, unsupported file type: image.

**Parent next, applying the U6 fallback:**
- 20250301_121500.jpg is a photographed receipt that U5 returned, so the parent reads the U5 text: merchant LEON'S, date 2025-03-01, one line RECLINER SOFA 3S BROWN LEATHER 1,799.99, currency CAD (HST on the receipt). Row marked "receipt read from photo text". Nothing not in the text is filled.
- danby-mini-fridge-2025-11-22.jpg was returned by U4, not U5; it is a scan in the Scans folder, not a library photo, so no recognized text exists for it. The fallback cannot apply. Recorded as a failure (step U6, path above). The mini-fridge row stays without a purchase date or price even though the fixture says the photo expert's text recognition could read this file.

Receipt lines going into U7: sofa (LEON'S, 2025-03-01, 1,799.99 CAD, from photo text), Power Tower (Amazon.ca, 2025-04-08, 389.00 CAD), USB cable x2 (Amazon.ca, 2025-04-08, 9.99 CAD each).

---

## U7. Match and decide each row (done by the Skill)

| Item or line | Decision | Reason |
| --- | --- | --- |
| Sofa (U3.1) and the LEON'S line | photo and receipt | same type of item; the receipt line's brown leather 3-seat recliner is allowed in Description as read from a receipt; first photo in the confirmed range is 2026-04-10, on or after the purchase date 2025-03-01. (The true first photo, 2024-08-15, is outside the range, so the date rule is passed here only because the range hides it; see findings item 3.) |
| Power Tower line | receipt only | no U3 item matches: the index has no category for it and U3 only searched categories. The photo 20250412_101233.jpg with POWER TOWER readable on the box exists on the NAS but no update-mode step reaches it (findings item 7). User to be asked to take one photo. |
| USB cable line | receipt only | a durable good with no photo, by the rule. User to be asked to take one photo of a cable (findings item 14). |
| TV, gaming chair, dining chairs, dining table, coffee table, dumbbell set, stick vacuum, mini-fridge, washer, dryer, floor lamps | photo only | no receipt line matches. |
| Ambiguous | none | no two receipts or two items compete. |

---

## U8. Confirm with the user

**Parent:** shows 14 rows in the list format and asks:

> Confirm, remove or correct these rows, and add a replacement value to any photo-only row if you wish. Two questions: how many dining chairs are there (the photo does not show them all), and can you take one photo each of the pull-up and dip station and the USB cables, which have receipts but no photo? Nothing is written until you confirm.

**Status:** waiting_user (parent-level).

**User:** "Confirm all rows as they are. I am not sure about the chairs, leave the quantity empty. I will take the photos later. No values for now."

**Parent next:** 14 rows confirmed, no values. Goes to U9.

---

## U9. Create the folder (first run)

```text
delegate --target file-agent --instruction 'Create a folder named Home Contents in the personal space of the current user. This is a write, so request user approval first. Return the real path of the created folder.'
```

**Expert file-agent, waiting_approval.** [get-user-dir; ug-filesystem mkdir]

> **Shown to the user:** The file expert is waiting for your approval to create the folder Home Contents in your personal space. Nothing has been written yet.

**User approves.**

**Expert file-agent, completed.** Created `/home/me/Home Contents`.

---

## U10. Add the item photos to the album

The confirmed rows have 7 distinct chosen photos.

```text
delegate --target photo-agent --instruction 'Create an album named Home contents 2026-11-02 in the library of the current user, containing exactly the photos at these real paths: /home/me/Photos/Camera/20260601_201500.jpg, /home/me/Photos/Camera/20250118_164002.jpg, /home/me/Photos/Camera/20251204_142223.jpg, /home/me/Photos/Camera/20260621_093406.jpg, /home/me/Photos/Camera/20260410_083012.jpg, /home/me/Photos/Camera/20260622_121507.jpg, /home/me/Photos/Camera/20260517_142210.jpg. Add no other photo. This changes the library, so request user approval first, and return the real album identifier and the number of photos added.'
```

**Expert photo-agent, waiting_approval.** [ug-photo create-album --album-name --add-item per path]

> **Shown to the user:** The photo expert is waiting for your approval to create the album "Home contents 2026-11-02" with 7 photos. The folder is created; the album, tags and list are not written yet.

**User approves.**

**Expert photo-agent, completed.** Album `alb-7f3a`, 7 photos added.

---

## U11. Tag the photos and receipts

Paths: the 7 item photos, the receipt photo and the Amazon PDF (9 files). The Danby scan is not tagged: it produced no confirmed row.

```text
delegate --target file-agent --instruction 'Make sure a file tag named home-contents exists, creating it only if it is missing, then attach that tag to each file at these real paths: /home/me/Photos/Camera/20260601_201500.jpg, /home/me/Photos/Camera/20250118_164002.jpg, /home/me/Photos/Camera/20251204_142223.jpg, /home/me/Photos/Camera/20260621_093406.jpg, /home/me/Photos/Camera/20260410_083012.jpg, /home/me/Photos/Camera/20260622_121507.jpg, /home/me/Photos/Camera/20260517_142210.jpg, /home/me/Photos/Camera/20250301_121500.jpg, /home/me/Downloads/Amazon-order-112-4471-2025-04-08.pdf. These are writes, so request user approval first. Return the tag identifier and, per path, whether tagging succeeded.'
```

**Expert file-agent, waiting_approval.** [ug-filemgr tag-get-by-name home-contents: not found; ug-filemgr tag-add; ug-filemgr tag-add-file per path]

> **Shown to the user:** The file expert is waiting for your approval to create the tag home-contents and attach it to 9 files.

**User approves.**

**Expert file-agent, completed.** Tag `tag-12` created; 9 of 9 paths tagged.

---

## U12. Save the updated list

```text
delegate --target knowledge-agent --instruction 'Save the Markdown text given below as a new file in the folder at the real path /home/me/Home Contents, with a file name starting with Home contents list followed by the date of today, 2026-11-02. Do not overwrite or delete any existing file. Return the real path of the saved file and confirm it was verified. The text follows.
# Home contents list 2026-11-02
Range covered: 2024-11-02 to 2026-11-02 (first run).
| # | Item | Description | Room | Qty | Purchase date | Price paid | Replacement value | Pre-loss photo | Receipt | Proof level | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
... the 14 rows exactly as in the table below ...
Totals: Price paid 2,208.97 CAD over 3 rows. Replacement value: none given. 11 rows have no price.'
```

(The real instruction carries all 14 rows; they are shown once in the table below. The instruction spans lines and contains Markdown pipes; see findings item 4.)

**Expert knowledge-agent, waiting_approval.** [ug-knowledge save-text --path --content --filename-hint]

> **Shown to the user:** The knowledge expert is waiting for your approval to save `Home contents list 2026-11-02.md` in `/home/me/Home Contents`.

**User approves.**

**Expert knowledge-agent, completed.** Saved `/home/me/Home Contents/Home contents list 2026-11-02.md`, verified true.

---

## Final report (as the Skill says to give it)

- Rows added: 14. Rows changed: 0 (first run).
- Photo-only rows still without a value: 11 (sofa has a price; the TV, gaming chair, dining chairs, dining table, coffee table, dumbbell set, stick vacuum, mini-fridge, washer, dryer and floor lamps have none).
- Receipt-only rows still without a photo: 2 (pull-up and dip station; USB cable x2).
- Saved list: `/home/me/Home Contents/Home contents list 2026-11-02.md`.
- Album: Home contents 2026-11-02 (`alb-7f3a`), 7 photos. Tag: home-contents (`tag-12`), 9 files.
- Failures by step and file: U6, `/home/me/Scans/danby-mini-fridge-2025-11-22.jpg`, unsupported file type: image (no row could be made from it). U6, `/home/me/Photos/Camera/20250301_121500.jpg`, unsupported file type: image, recovered from the photo text.
- Nothing was deleted, moved or overwritten. No data left the NAS.

## Inventory table (confirmed in U8, saved in U12)

| # | Item | Description | Room | Qty | Purchase date | Price paid | Replacement value | Pre-loss photo | Receipt | Proof level | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Reclining sofa, 3-seat | brown leather, 3-seat recliner (from the receipt); brand and model not visible | Basement | 1 | 2025-03-01 | 1,799.99 CAD | | 20260601_201500.jpg (2026-06-01) | 20250301_121500.jpg | photo and receipt | receipt read from photo text; other photos 20260410_083012.jpg, 20260622_023921.jpg |
| 2 | Television | brand and size not visible | Basement | 1 | | | | 20260601_201500.jpg (2026-06-01) | | photo only | other photo 20260622_023921.jpg |
| 3 | Gaming chair | brand not visible | not visible | 1 | | | | 20250118_164002.jpg (2025-01-18) | | photo only | other photo 20260621_093406.jpg |
| 4 | Dining chairs | brand not visible | Dining area, ground floor | | | | | 20251204_142223.jpg (2025-12-04) | | photo only | quantity left empty by the owner |
| 5 | Dining table | material not visible | Dining area, ground floor | 1 | | | | 20251204_142223.jpg (2025-12-04) | | photo only | a hutch is visible in the same photo and has no category |
| 6 | Coffee table | material not visible | not visible | 1 | | | | 20260621_093406.jpg (2026-06-21) | | photo only | photo shows standing water |
| 7 | Adjustable dumbbell set | marking 52.5 LB readable; brand not visible | Basement | 1 | | | | 20260410_083012.jpg (2026-04-10) | | photo only | |
| 8 | Stick vacuum | brand not visible | not visible | 1 | | | | 20260622_121507.jpg (2026-06-22) | | photo only | photo shows the vacuum wet |
| 9 | Mini-fridge | brand not visible | Basement | 1 | | | | 20260601_201500.jpg (2026-06-01) | | photo only | other photo 20260622_182035.jpg; receipt scan could not be read |
| 10 | Washer | Amana, readable on the control panel | Laundry room | 1 | | | | 20260517_142210.jpg (2026-05-17) | | photo only | |
| 11 | Dryer | Amana, readable on the control panel | Laundry room | 1 | | | | 20260517_142210.jpg (2026-05-17) | | photo only | same photo as the washer |
| 12 | Floor lamps | brand not visible | not visible | 2 | | | | 20260622_121507.jpg (2026-06-22) | | photo only | two lamps side by side |
| 13 | Pull-up and dip station | Power Tower Pull Up Dip Station (from the receipt) | | 1 | 2025-04-08 | 389.00 CAD | | | Amazon-order-112-4471-2025-04-08.pdf | receipt only | owner asked to take one photo |
| 14 | USB cable | from the receipt | | 2 | 2025-04-08 | 9.99 CAD each | | | Amazon-order-112-4471-2025-04-08.pdf | receipt only | owner asked to take one photo |

Totals: Price paid 2,208.97 CAD over 3 rows (1,799.99 + 389.00 + 19.98). Replacement value: none given. 11 rows have no price.
