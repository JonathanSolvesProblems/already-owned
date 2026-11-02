# Verification of the rewritten home-contents-inventory Skill

Second dry run, Nov 2, against `skill/home-contents-inventory/SKILL.md` as committed in 7fd5dea, with its three references, `tests/dry-run/fixture.md` and the capability catalog (ug-photo, ug-document, ug-knowledge, ug-filesystem, ug-filemgr, file-workflow, ug-surveillance). Two roles as before: the Uliya parent fills every template phrase and issues `delegate` calls; the experts answer only from the fixture. Scenario A (claim mode) was run end to end, every instruction filled; scenario B (update mode, first run) more briefly. No file other than this one was changed. Street addresses, policy numbers and claim numbers do not appear in the fixture and do not appear here; the insurer and the order number in a file name are also left out.

Conventions kept from the first run: the loss time is 2026-06-20 02:00 NAS local time; recognition-index hits that the fixture does not describe cannot be confirmed by the vision check and count as "unlisted"; today is 2026-11-02.

---

## 1. The 24 findings, one line each

| # | Status | Where it is covered now, and what still makes a parent stumble |
| --- | --- | --- |
| 1 | Fixed | C6 runs U4, U5 and U6 "with no date limit", adds the affected items to the U6 instruction, applies the U6 fallback and the U7 rules, and keeps inventory receipts. All four delegations are fillable and the sofa receipt photo is found again. |
| 2 | Fixed | U6 has the vision-ocr fallback delegation for an image from U4; C6 says to apply it. The Danby scan is read and the mini-fridge row gets its date and price. (The text carries no currency and nothing says what to do; see new defect 9.) |
| 3 | Fixed | U7 has the Date conflict outcome; in claim mode the sofa row keeps its receipt and is not matched again, so the question is not re-asked. |
| 4 | Partly | The Orchestration paragraph now says to replace the phrases, gives the shell escape, forbids command options, and has a worked example. But its own row rule ("one line per row") contradicts its own ban on line breaks, and C9.2 cannot carry the C8 draft at all under the ban. See new defects 1 and 2. "before today" in C4a is not one of the listed phrases, so a literal parent sends it unfilled. |
| 5 | Partly | C4a describes the damage photos once (5 descriptions, once). C4b groups items per route and room, so the recognized-object pass runs once for eight categories instead of once per item. But the second-pass sentence "for each item still without proof ... delegate once more" reads as one delegation per item, which would reintroduce the per-item re-description. See new defect 3. |
| 6 | Fixed | C3 runs the U2 instruction with "with no date limit"; search-routes row 2 and C4b's second pass add the vision-ask route; the monitor arm is found in the gaming chair photo without a question. Mapping the user's "bookshelf" to the index's "bookcase" is still the parent's call, but either choice is safe. |
| 7 | Fixed | U6b runs the U3 instruction with the text route then the time-window route; in scenario B the power tower photo is found on the first of the two. |
| 8 | Fixed | C3 shows the inventory rows for the affected rooms and asks for anything else lost there. (With more than one affected room it does not ask which room each named item is in; see new defect 12.) |
| 9 | Fixed | claim-list-format Notes carries "path: ..."; search-routes row 1 is the file-name route; C4b puts every inventory row on it. The fixture inventory predates the format and has no path, so the route resolves the five rows by file name in one delegation, which works. |
| 10 | Fixed | U3: same file name on the existing list is the same item; same type in the same room is a possible duplicate asked at U8. |
| 11 | Fixed | Qty rule in search-routes and claim-list-format; the two side tables are one row with Qty 2 without a question. |
| 12 | Partly | C1 collects the language; the C8 instruction names it and asks for approval before any file. The third part of the finding, listing a C8 output file path in the report, is not in the C9 report list. |
| 13 | Fixed | Completion rule distinguishes a second route from another source; search-routes says questions are collected and asked once at U8 or C7. |
| 14 | Fixed | U7 Accessory outcome; the cable is shown as "accessory, keep?" in scenario B and dropped by document-agent in scenario A as not an affected item. |
| 15 | Fixed | C4b and search-routes: entries that do not name one object type get proof level none and "owner to itemize", and C7 asks whether to split. Bedding and the boxes and bags take this path; diploma frames name an object type and are searched. |
| 16 | Fixed | C9 announces three approvals, defines the album as the clearest pre-loss photo per row plus every damage photo, and the report has "photos to attach by hand". |
| 17 | Fixed | C2 finds recordings with file-agent first, pauses, then transcribes the chosen real path. Not exercised (no recording in the fixture). |
| 18 | Fixed | C5 asks for current camera status then the events; C1 fixes the time zone and the earliest-time rule. Not exercised (water loss, no cameras). The "loss window" C5 needs is never defined as a start and an end; see new defect 11. |
| 19 | Partly | U3 flags wet, burnt or broken items and U8 asks "photo shows damage; keep?" when the only photo is flagged. But "clearest" is still the photo naming the most features, with no preference for an unflagged one, so in scenario B the sofa's clearest photo can still be the water-line photo. |
| 20 | Fixed | claim-list-format Room rule: the photo's room is kept and the user's room goes in Notes. The washer and dryer row says laundry room with the user's "basement" noted. |
| 21 | Fixed | Steps say "pause and ask the user"; `waiting_user` is kept for an expert that stops to ask, and the Orchestration paragraph says so. |
| 22 | Fixed | U1: newest by the date in the name, modification date when the names tie. |
| 23 | Fixed | U2 asks which to exclude and skips the question under fifteen categories; scenario B has thirteen and continues without a pause. |
| 24 | No change needed | Every filled instruction that carries a real path would still raise the hardcoded-home warning if the checker ran at runtime. That is inherent and the Skill still passes real paths, which is right. |

Count: 19 fixed, 4 partly fixed (4, 5, 12, 19), 0 not fixed, 1 needing no change (24).

---

## 2. New defects introduced or left by the rewrite, most serious first

Status, Nov 2: all twelve numbered defects below and the smaller stumbles are applied in SKILL.md and the references (rows stay on one line with "Row n:" and a full stop between rows, separators escaped inside values; C9 saves the flattened document with the table re-rendered from the rows; the second pass is one delegation per room; the room route is the vision-ask over returned photos; C4a is bounded to thirty days or the user's end date; C6 drives a photo search from what it finds and keeps receipt-only rows after a loss; Notes uses commas; missing currency is a collected question; ask mode matches the user-named room; C1 collects a theft window; C3 collects the room per item and skips the exclude question; route order when brand and category both apply; damage photos that fit two rows are a question; U6b stays inside the confirmed range).

### 1. The row format contradicts the line-break ban, so U12, C8 and C9 cannot be filled as written

**Step:** Orchestration paragraph, applied at U12, C8, C9.2. **Quoted:** "A list of rows (U12, C8, C9) is passed as one line per row with the twelve values separated by semicolons, and the expert is asked to render it as a table; never put a table or a line break inside an instruction."

**What goes wrong:** 26 rows on "one line per row" is 25 line breaks inside the single-quoted instruction, which the same sentence forbids. A parent obeying the first half breaks the second; a parent obeying the second half has no way to pass the rows. The finding 4 replacement text carried the same contradiction and was applied verbatim. The kit checker parses one delegate per line, so the multi-line form is the `DELEGATE_FORMAT_INVALID` case the first run found.

**Replacement:** "A list of rows (U12, C8, C9) stays on the one line of the instruction: each row begins with the word Row and its number followed by a colon, its twelve values are separated by semicolons, and the next row follows after a full stop and a space; the expert is asked to render the rows as a Markdown table with the column names given. Never put a table, a line break, a pipe or an angle bracket inside an instruction."

### 2. C9.2 has to carry the C8 draft, which is a multi-line Markdown document with a table

**Step:** C9.2. **Quoted:** "Save the claim document text given in this step as a new Markdown file in the claim folder at the real path given in this step".

**What goes wrong:** C8 returns the draft "with the list rendered as a table", that is, a document of several paragraphs and a pipe table. "Given in this step" means the parent writes that text inside the instruction, which puts line breaks and pipes inside it. The row rule above does not help, because what C9.2 saves is the draft, not the row list. The catalog gives no way round it: `ug-document writing` has no output path parameter, so letting C8 write the file would put it wherever the expert chooses, and `ug-knowledge save-text` takes `content` or `content-ref`, and nothing in the catalog says a C8 draft can be referred to by ref. In scenario A the parent had to flatten the draft on its own initiative.

**Replacement:** "C9.2 passes the document flattened on one line: the heading as one sentence, the summary as one or two sentences, the confirmed rows in the row format with the column names, and the attachment list as one sentence naming each file; it asks knowledge-agent to render the rows as a Markdown table and save the whole as one file. The C8 draft is used for the wording of the heading and the summary; the table is rendered again from the confirmed rows so no value changes."

### 3. C4b's second pass reads as one delegation per item

**Step:** C4b, second paragraph. **Quoted:** "After the first pass, for each item still without proof whose room already has returned photos, delegate once more with the route 'ask the vision model about the photos at the real paths listed in this step' before any new search."

**What goes wrong:** "for each item ... delegate once more" is a loop over items. In scenario A twelve items are still without proof after the first pass, so a literal parent sends twelve delegations that each describe the same seven basement photos: 84 descriptions, twelve per photo, which is most of what the C4 split was meant to remove. The first-pass rule "One delegation per route and room, listing every item on that route" is not restated for the second pass, and the template's plural "items listed in this step" is the only hint that batching is allowed.

**Replacement:** "After the first pass, send one more delegation per room, listing every item of that room still without proof and the real paths of every photo the room has returned, with the route 'ask the vision model about the photos at the real paths listed in this step'. This counts as one route for each item listed."

### 4. "Room first for the rest" is not a route in the reference, and the reference's room route cannot be used in the first pass

**Step:** C4b, first paragraph, with search-routes row 6. **Quoted:** "time window for items with a receipt date; room first for the rest." and the reference's "Only the room | Time window of the room's other photos, then recognized object".

**What goes wrong:** The parent has to guess that "room first" means the reference's "only the room" route. That route needs the capture dates of the room's other photos, which exist only after the file-name and recognized-object delegations have returned, so it cannot be sent in the same pass, and nothing says to send the routes in order. It also has no window width: the parent invents "the same day as each known basement photo". In scenario A that search returns the same seven photos the second pass then describes again, so the whole delegation is redundant. The recognized-object half of the route is unusable for these items by construction (boot dryer, garment steamer, camera rig, flight case, shelving, diploma frames have no category).

**Replacement:** In C4b: "Items with none of the above wait for the first pass to return and take only the second-pass route below; they are not searched by time window." In search-routes row 6: "Only the room | Ask the vision model about the room's photos returned for other items (row 2); if the room has returned none, no results | ...".

### 5. C4a describes every photo taken since the loss, with no upper bound

**Step:** C4a. **Quoted:** "Find photos in the library of the current user captured after the loss date and time given in this step and before today. Describe each once with the local vision model".

**What goes wrong:** The loss is four and a half months before today; on the fixture library (2,140 photos over 33 months) that is roughly 290 photos sent one by one to the local vision model in a single delegation, for five that matter. The fixture lets the expert return the five directly, so the dry run did not feel it, but a real device would spend most of the Skill's running time here, and a loss a year old would be worse. "before today" is also not one of the five template phrases, so a literal parent sends it unfilled (the expert can read a clock, so it does not fail).

**Replacement:** "Find photos in the library of the current user captured in the thirty days after the loss date and time given in this step, or up to the end date given in this step if the user named one. Describe each once with the local vision model".

### 6. C4b's receipt-date and text routes never see what C6 finds, because C6 runs after C4b

**Step:** C4b with C6. **Quoted:** "text visible in the photo for items with a readable brand or model; time window for items with a receipt date".

**What goes wrong:** At C4b the only receipt dates and printed text the parent holds come from inventory rows, and those rows are already on the file-name route, so both routes are empty in scenario A. The receipt C6 then finds for the mini-fridge (a date and the word DANBY) can never drive a photo search, and the "stop after two routes with no results" rule has already closed the item. In the fixture the mini-fridge is found by category anyway; a camera rig with an invoice and no category would end with proof level none although its unboxing photo is on the NAS. U6b does exactly this in update mode and has no claim-mode counterpart.

**Replacement:** In C6, after the U7 rules: "For an affected item that C6 gives a purchase date or printed text and that still has no pre-loss photo, run the C4b instruction once more for that item with the route 'text visible in the photo' and the printed words, and if that returns no results once more with 'time window from the purchase date to 60 days after'. These two do not count against the two-route stop."

### 7. The U7 receipt-only outcome, applied in claim mode, asks the user to photograph a lost item

**Step:** C6 ("Apply ... the U7 rules to every line returned") with U7. **Quoted:** "Receipt only: a receipt for a durable good with no photo after U6b. Ask the user to take one photo so ownership is shown."

**What goes wrong:** After a flood the item is gone. If the Danby receipt had matched no photo, a literal parent would ask the user to photograph the mini-fridge they just lost. The user guide promises "When a receipt has no matching photo, it asks you to take one", which is right for update mode only.

**Replacement:** In C6: "In claim mode a receipt-only row is kept as proof of purchase with proof level receipt only, and the user is not asked for a photo."

### 8. Semicolons inside Notes break the semicolon-separated row

**Step:** Orchestration paragraph and claim-list-format Notes rule. **Quoted:** "the twelve values separated by semicolons" and Notes: "the real path of the pre-loss photo ... ; anything the user added; 'receipt read from photo text' ... ; and, in claim mode, 'damage photo: ' followed by the file name."

**What goes wrong:** Notes is a list of notes, and the natural separator between notes is a semicolon; the fixture's inventory row 1 already contains two of them. A row whose Notes holds "path: ...; receipt read from photo text; damage photo: ..." has fourteen semicolons, and the expert cannot tell the twelve values apart.

**Replacement:** In claim-list-format: "Separate the notes inside Notes with commas, never with a semicolon, because the semicolon separates the twelve values when the row is passed to an expert." In the Orchestration paragraph: "inside a value, a semicolon is written as a comma".

### 9. Text read from a photographed or scanned receipt has no currency, and the totals are per currency

**Step:** U6 fallback, C7 and claim-list-format totals. **Quoted:** "Then read the merchant, date, item lines and prices from that text ... Never fill a line that is not in the text."

**What goes wrong:** The Danby text reads "219.99 ... TOTAL 252.93" with no currency symbol, and the merchant is not in it either. The parent may not invent CAD, so Price paid is a number with no currency and the per-currency total has nowhere to put it. The same happens for the sofa receipt photo (the text has tax names that imply a country but no currency word).

**Replacement:** Add to the fallback: "If the text names no currency, leave the currency empty and add it to the questions asked at U8 or C7."

### 10. Ask mode matches the room against the photo's room only

**Step:** A1 with the claim-list-format Room rule. **Quoted:** "show the rows for the room the user asked about".

**What goes wrong:** Room holds the room seen in the photo; the user's own name for it goes in Notes. The washer and dryer are listed under "Laundry room" with "basement" in Notes, so "what do I own in the basement" does not show them.

**Replacement:** "show the rows whose Room, or whose user-named room in Notes, is the room the user asked about".

### 11. C5 needs a loss window; C1 collects a point in time

**Step:** C1, C5. **Quoted:** C1 "Confirm the date and time of the loss"; C5 "return the events recorded in the loss window given in this step".

**What goes wrong:** `event-timeline` requires a start and an end. For a break-in the user usually gives a span ("between 11 pm and 6 am"), but C1 does not ask for one, and nothing says what the window is when the user gives one time. Not exercised in the fixture.

**Replacement:** In C1: "For a theft or break-in also confirm the window to search, from the last time the place was known to be untouched to the time the loss was found; the cut-off for photos is the start of that window."

### 12. With several affected rooms, C3 does not learn which room each named item is in

**Step:** C3, C4b. **Quoted:** "pause and ask the user to confirm them and name anything else lost in those rooms" and "One delegation per route and room".

**What goes wrong:** Per-room delegations and the per-room second pass need a room per item; C3 asks for items, not their rooms. One affected room in the fixture hides it.

**Replacement:** "name anything else lost in those rooms, and, when more than one room is affected, the room of each item".

### 13. Smaller stumbles, one line each

- Orchestration paragraph: the ban names tables and line breaks, not a bare pipe or an angle bracket; a user note such as "sofa | brown" or "TV <55 inch>" passes the Skill's rule and trips the checker's format and unresolved-placeholder patterns.
- C3: "run the U2 instruction once" is clear, but the U2 text that follows the instruction (show counts, ask which to exclude) is one line below it, and a literal parent may ask the exclude question in claim mode, a pause with no purpose.
- C4b: "items with a readable brand or model" does not say whether the user's own words (Danby, Amana) count as readable; the reference says "from a receipt line or from the user", and the list in C4b puts recognized object before text while the reference puts text before recognized object. The two orders give different first routes for the mini-fridge and the washer. Both reach the washer; only the category route reaches the mini-fridge (no photo carries the word Danby).
- C7: "Match the damage photos from C4a to rows by room and by the items named in their descriptions": the vision model named no room for any of the five damage photos, so only the item names match, and "camera rig in a wet case" could belong to the camera rig row, the flight case row or both. Nothing says to ask; I asked at C7.
- C9: "the clearest pre-loss photo of every row" relies on the definition of clearest that lives in U3; C4b does not restate it.
- U6b second route and search-routes row 5: a receipt modified in the confirmed range can be dated before it (an old receipt scanned recently), so the 60-day window can search outside the confirmed range, which the Completion rule calls widening without asking.
- C8 instruction: the Item value `Flat-screen TV, about 55"` carries a double quote, which is legal inside the single quotes, but nothing says so; a nervous parent may drop the inch mark.

---

## 3. Delegation and description counts

### Scenario A, claim mode, 26 rows (5 inventory rows plus 20 user entries, washer and dryer as two rows)

| Step | Delegations now | What they were | Notes |
| --- | --- | --- | --- |
| C3 | 2 | 1 | U1, then the U2 instruction with no date limit (13 categories returned) |
| C4a | 1 | (inside C4) | 5 damage photos, each described once |
| C4b | 4 | 26 | file name (rows 1 to 5, 4 photos); recognized object (8 categories in one delegation: chair, bed, table, dumbbell, bookcase, lamp, refrigerator, washing machine); room time window for the rest (new defect 4); second pass vision-ask for 12 items over 7 photos |
| C5 | 0 | 0 | water loss, not asked |
| C6 | 4 | 2 | U4, U5, U6, vision-ocr fallback for the Danby scan; both receipts the first run lost are recovered |
| C7 | 0 | 0 | questions collected: floor lamp count, split bedding and boxes, mini-fridge currency, which row the wet case belongs to |
| C8 | 1 | 1 | |
| C9 | 3 | 3 | folder, document, album (8 pre-loss plus 5 damage photos) |
| **Total** | **15** | **33** | |

Readings that change the count: 14 if the redundant room time-window delegation is dropped (new defect 4); 26 if the second pass is read per item (new defect 3).

Outcome per row, same as the first run except where noted: 4 rows photo and receipt (sofa, stick vacuum, pull-up and dip station, and now the mini-fridge); 9 photo only (TV, gaming chair, side tables, dumbbell set, floor lamps, washer, dryer, monitor arm found by the second pass without a question, mini-fridge moved up); 13 none, of which coffee table and camera rig have a damage photo.

### Vision-model descriptions of the same photo

- 20240815_190211.jpg (the sofa, TV and side tables photo): described 4 times (file-name route, recognized-object route via "table", room time window, second pass), against up to 25 in the first run. 3 if the room time-window delegation is dropped; 15 under the per-item reading of the second pass.
- The five damage photos: once each (were re-derived in every one of the 26 C4 delegations).
- All fixture photos together: 31 descriptions of 15 distinct photos across C4a and C4b, plus about 70 descriptions of index hits the fixture does not describe (the chair, bed, table, bookcase and lamp categories), described once each instead of once per item that shares the category.

### Scenario B, update mode, first run, range two years (2024-11-02 to today)

24 delegations (U1, U2, U3 x13, U4, U5, U6, vision-ocr fallback, U6b x1, U9, U10, U11, U12), against 22 in the first run; the two extra ones recover the Danby receipt and find the power tower photo, so the inventory ends with 4 rows photo and receipt (sofa, pull-up and dip station, mini-fridge and the Dyson only if the user keeps the flagged photo) instead of 2, and no row is receipt only. The Dyson invoice (modified 2024-09-02) falls outside the two-year range, as it did before. U2 returns 13 categories and the exclude question is skipped. The stick vacuum and the floor lamps still have only post-loss photos in range and are shown at U8 as "photo shows damage; keep?"; the sofa row's clearest photo can still be the water-line photo (finding 19, partly). The USB cable is shown as "accessory, keep?". U12 hits new defects 1 and 8 exactly as C8 and C9.2 do.

---

## 4. Verdict

As written, the Skill now runs from the first sentence to the confirmation step on a device whose experts behave like the catalog says: every read delegation in C3, C4a, C4b and C6 can be filled from values the parent actually holds, uses only catalog actions (get-user-dir, find, cat, albums and search-picture with file-name-contains, ai-object-name, ocr-contains and time, vision-vlm, vision-ocr, extract), and the claim-mode defects that stopped the first run (C6, the lost scanned receipt, the sofa date conflict, the guessed categories, the unreachable monitor arm) are gone, at 15 delegations instead of 33 and 4 descriptions of the busiest photo instead of 25. It does not run to the end: the three writes that carry the list (U12, C8, C9.2) are governed by a sentence that contradicts itself about line breaks, by a field separator that the Notes column also uses, and in C9.2 by a document that cannot be passed inside one line at all, so a literal parent stops at the first save or breaks the rule to get past it. Those are three sentences to fix, plus the C4b route wording that a parent would otherwise read as twelve more delegations. With those four changes the Skill would run on the real device; without them it reaches the user's confirmed list and cannot save it.
