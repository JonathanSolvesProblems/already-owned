---
name: home-contents-inventory
description: A home contents inventory for insurance, built from the photos and receipts already on the NAS, with a pre-loss photo and proof of purchase behind each item, plus an insurer-ready contents list after a flood, fire or theft. Use when the user says "update my home inventory", "file this week's receipts into my inventory", "what do I own in the basement", "I had a flood / fire / break-in, list what I lost", or "prepare my contents claim". Reads only the photos and documents of the current user and, in claim mode for a theft or when asked, the user's own camera events for the loss window; creates albums, tags, folders and files only after the user approves each one; sends nothing off the NAS.
---

# Goal

Keep a running list of the household belongings the user owns, each backed by a real photo taken before any loss and, where one exists, a real receipt, without the user typing or re-photographing anything. When something happens, turn that list into the contents list an insurer asks for, restricted to photos taken before the loss.

The Skill has three modes, chosen from what the user says:

- **Update mode** (routine, about weekly): "update my home inventory", "file this week's receipts".
- **Claim mode** (after a loss): "I had a flood on June 20 in the basement", "prepare my contents claim".
- **Ask mode** (read only): "what do I own in the basement", "show my inventory". Answers from the saved list and searches nothing.

If the request fits none of them, ask which one the user wants and stop until they answer.

Supported scope: the photo library, documents and receipts of the current user on this NAS, and, in claim mode only, the user's own surveillance events for the time of the loss. Out of scope: estimating market prices, contacting the insurer, and anything outside the NAS. Replacement values come only from receipts or from the user, never from the model.

# Required input

Update mode:

- The date range to cover. Default: from the date of the newest Home contents list in the Home Contents folder to today; on the first run, ask the user how far back to go.

Claim mode:

- Date and time of the loss, in the local time of the NAS, and its kind: water, fire, theft or other. When the user gives an approximate time ("around 2 am"), the cut-off is the earliest time they give, and the Skill says so.
- The affected rooms.
- Optionally, the items the user knows were lost, typed or as a voice recording on the NAS (for example a walk-through of the room).
- The insurer and claim number, if the user wants them on the list.
- The language of the claim document. Default: the language the user is writing in.

Ask mode:

- The room, or nothing for the whole list.

Do not ask for anything else up front. Each expert collects its own parameters.

# Generation-time capability evidence

- `ug-photo` → `photo-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`
- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `file-workflow` → `file-agent`
- `ug-surveillance` → `security-monitor-agent`

# Orchestration

Every step passes only real results returned by the previous step (real paths, real capture dates, real album and tag identifiers) to the next one. Never refer to "the folder from before"; pass the path itself. Choose each search route with [references/search-routes.md](references/search-routes.md). Build every list row with the rules in [references/claim-list-format.md](references/claim-list-format.md). The user-facing explanation is in [references/user-guide.md](references/user-guide.md).

Each instruction below is a template. Before sending it, replace every phrase "named in this step", "listed in this step", "given in this step", "confirmed with the user" and "the date of today" with the actual value, written out inside the single quotes, so the expert receives one self-contained task. Routes are written in words, never as a command option. A single quote inside a value is written with the standard shell escape. A list of rows (U12, C8, C9) is passed as one line per row with the twelve values separated by semicolons, and the expert is asked to render it as a table; never put a table or a line break inside an instruction. For example, the C4b instruction for one sofa is sent with "the household items listed in this step" replaced by "a brown leather reclining three-seat sofa", "the loss date and time given in this step" replaced by "2026-06-20 02:00 local time", and "the search route named in this step" replaced by "recognized object sofa".

"Pause and ask the user" below is a question the Skill itself asks before going on. The delegation state `waiting_user` is reserved for an expert that stops to ask. Questions about individual rows are collected and asked once, at U8 or C7, not one at a time.

## Update mode

**U1. Find the existing inventory.** Read only.

`delegate --target file-agent --instruction 'Resolve the personal space of the current user, then find the folder named Home Contents in it. If it exists, return its real path and, for the newest Markdown file in it whose name starts with Home contents list, newest by the date in its name and by modification date when the names tie, return the real path, modification date and full text of that file. If the folder does not exist, report that it does not exist. Read only: create, move or change nothing.'`

If the folder does not exist, this is the first run: tell the user, confirm the date range to cover, and continue with an empty inventory.

**U2. Find which kinds of belongings the photos show.** Read only.

`delegate --target photo-agent --instruction 'Using the recognition index of the photo library of the current user, list the recognized object categories that are durable household belongings an insurer would cover: furniture, televisions and screens, computers, phones and tablets, cameras, kitchen and laundry appliances, bicycles, musical instruments, tools, sports equipment, jewellery and artwork. For each category return its exact name in the index and the number of matching photos captured in the date range confirmed with the user. Exclude people, pets, food, documents and screenshots. If no category matches, return an empty result and say so. Read only.'`

If the result is empty, report no results for this date range and stop update mode. Otherwise show the categories with counts and pause and ask the user which to exclude; with fewer than fifteen categories, continue with all of them and skip the question.

**U3. Find and describe the photos of each category.** One delegation per category and route. The first route for a category is the recognized object itself; the search-routes reference gives the next one.

`delegate --target photo-agent --instruction 'For the household object category named in this step, search the photos of the current user captured in the date range given in this step, using the search route named in this step. Describe each returned photo once with the local vision model: every household item visible in it, with type, brand and model only if readable, colour, material, approximate size, the room if it can be seen, and whether any item looks wet, burnt, broken or otherwise damaged. Return per photo the real path, the capture date from the photo metadata and that description; return photos with no capture date separately as undated. Write not visible instead of guessing a brand or model. If nothing is found, return no results for this category. Read only.'`

The Skill, not the expert, turns photos into items: photos whose descriptions agree on type, colour, material and room are one item; identical items side by side are one row with the count in Qty; items of the same type with clearly different features are separate rows; when unsure, the question goes to U8. The clearest photo of an item is the one whose description names the most of its features. An item whose photo file name already appears on the existing list is that same item, not a new one; an item of the same type in the same room as an existing row is shown at U8 as a possible duplicate. A photo flagged as showing damage is kept with the flag.

**U4. Find receipt files.** Read only.

`delegate --target file-agent --instruction 'In the Documents, Downloads and Scans folders of the personal space of the current user, find PDF and image files modified in the date range confirmed with the user whose names or locations suggest receipts, invoices or order confirmations, including scanned receipts saved as images. Return each real path, name and modification date. If none are found, return no results. Read only.'`

**U5. Find receipts that were photographed.** Read only.

`delegate --target photo-agent --instruction 'Search the photos of the current user captured in the date range confirmed with the user for receipts and invoices, using the text recognized in the photo (words such as total, subtotal, receipt, invoice, tax, order). Return the real path and capture date of each photo that shows a receipt, and the full recognized text of each one. If none are found, return no results. Read only.'`

**U6. Extract the purchase lines.** Read only. Pass the union of real paths from U4 and U5. If both returned no results, go to U7 with no receipts.

`delegate --target document-agent --instruction 'Extract the purchased line items from the receipt and invoice files at the real paths listed in this step: merchant, purchase date, item description, brand and model if printed, quantity, price paid and currency, and the source path. Keep text in its original language and add a short English item description. Ignore groceries, restaurants, fuel, services and subscriptions. Report each file that could not be read as a failure with its path. If no durable household item is found, return an empty result. Read only.'`

If `document-agent` reports an image file as a failure: for a photo that U5 returned, use the recognized text U5 gave for it; for an image file from U4, delegate once more with its real path:

`delegate --target photo-agent --instruction 'Read all text in the image at the real path given in this step with text recognition and return it unchanged. If the image cannot be read, return a failure with the path. Read only.'`

Then read the merchant, date, item lines and prices from that text, mark those rows "receipt read from photo text", and show them at U8 like every other row. Never fill a line that is not in the text.

**U6b. Find photos for receipt lines that match no item.** For every receipt line naming a durable good that matches no U3 item, run the U3 instruction once with the route "text visible in the photo" and the brand, model or item words from the line, and if that returns no results, once more with the route "time window from the purchase date to 60 days after". Only after both is the line receipt only.

**U7. Match and decide each row.** Done by this Skill, not by an expert. For every item and every receipt line, decide one of:

- **Photo and receipt**: the receipt line names the same type of item, matching brand or model text where readable, and the first photo of the item is on or after the purchase date.
- **Date conflict**: the receipt line names the same type of item, but the first photo of the item is before the purchase date. Ask at U8 whether the receipt is for this same item (a replacement, repair or warranty invoice) or for a second one. The same item: photo and receipt, with the note "receipt dated after first photo, confirmed by the owner". A second one: a receipt-only row.
- **Photo only**: no receipt matches. Value to be supplied by the owner.
- **Receipt only**: a receipt for a durable good with no photo after U6b. Ask the user to take one photo so ownership is shown.
- **Accessory**: a receipt line for a cable, accessory, consumable or part. Shown at U8 as "accessory, keep?" and dropped unless the user keeps it.
- **Ambiguous**: two receipts or two items compete. Ask at U8; never pick one silently.

**U8. Confirm with the user.** Pause and ask the user once, showing the new and changed rows in the format from the claim-list-format reference: confirm, remove or correct rows; add replacement values for photo-only rows if they wish; answer the collected questions (possible duplicates, date conflicts, accessories, ambiguous rows, undated photos, and rows whose only photo is flagged "photo shows damage; keep?"). Nothing is written before this confirmation.

**U9. Create the folder if needed.** Only on a first run.

`delegate --target file-agent --instruction 'Create a folder named Home Contents in the personal space of the current user. This is a write, so request user approval first. Return the real path of the created folder.'`

**U10. Add the item photos to the album.** Pass the real paths of the clearest photo of each confirmed row.

`delegate --target photo-agent --instruction 'Create an album named Home contents followed by the date of today in the library of the current user, containing exactly the photos at the real paths listed in this step. Add no other photo. This changes the library, so request user approval first, and return the real album identifier and the number of photos added.'`

Each update run makes its own dated album, because the public album capability creates albums and does not add to an existing one. The file tag from U11 is what links every inventory photo across runs.

**U11. Tag the photos and receipts.**

`delegate --target file-agent --instruction 'Make sure a file tag named home-contents exists, creating it only if it is missing, then attach that tag to each file at the real paths listed in this step (item photos and receipt files of the confirmed rows). These are writes, so request user approval first. Return the tag identifier and, per path, whether tagging succeeded.'`

**U12. Save the updated list.** Pass the whole list, existing rows plus confirmed new ones, as one line per row.

`delegate --target knowledge-agent --instruction 'Save the contents list given in this step as a new Markdown file in the folder at the real path given in this step, with a file name starting with Home contents list followed by the date of today. The list is given as one line per row with twelve values separated by semicolons; render it as a Markdown table with the column names given in this step. This creates a file, so request user approval first. Do not overwrite or delete any existing file. Return the real path of the saved file and confirm it was verified.'`

Report: rows added, rows changed, photo-only rows still without a value, receipt-only rows still without a photo, and the path of the saved list.

## Ask mode

**A1. Read the inventory.** Run U1. If there is no inventory, say so, offer update mode, and stop. Otherwise show the rows for the room the user asked about, or all rows, with each row's proof level and the totals from the claim-list-format reference. Read only: no photo search and no write. If the user then asks to find more belongings, that is update mode.

## Claim mode

**C1. Collect the loss.** Confirm the date and time of the loss in the local time of the NAS (an approximate time becomes the earliest time given, and the user is told), its kind, the affected rooms, the language of the claim document, and the insurer and claim number if wanted. The cut-off for evidence is the loss time: only photos whose capture time in the photo metadata, not the upload or modification time, is before it count as proof of ownership. A photo with no capture time is listed separately as undated and counts only if the user confirms when it was taken.

**C2. Transcribe a voice walk-through, if the user mentions one.** Read only. Users say "the voice note from yesterday", not a path, so find the recording first.

`delegate --target file-agent --instruction 'Find audio recordings in the personal space of the current user modified in the last fourteen days, newest first, and return each real path, name and modification date. If none are found, return no results. Read only.'`

Pause and ask the user which recording it is, then pass its real path:

`delegate --target knowledge-agent --instruction 'Transcribe the audio recording at the real path given in this step and return the transcript text and its segments. If the recording cannot be read, return a failure with the path. Read only.'`

From the transcript, list each belonging the user mentions with the room. These items are confirmed at C3.

**C3. Read the existing inventory and complete the item list.** Run U1. Show the inventory rows for the affected rooms, plus the items from C2 if any, and pause and ask the user to confirm them and name anything else lost in those rooms. If there is no inventory, continue from the items the user names and tell them. Then run the U2 instruction once with "with no date limit" in place of the date range, so the real category names of the index are known; later routes use only names on that list.

**C4a. Find the damage photos, once.** Read only.

`delegate --target photo-agent --instruction 'Find photos in the library of the current user captured after the loss date and time given in this step and before today. Describe each once with the local vision model and keep those that show water, fire, smoke, damaged household items, or any of the rooms named in this step. Return each real path, capture date and description. If none are found, return no results. Read only.'`

**C4b. Find pre-loss proof for the affected items.** Group the items by route with the search-routes reference: file name for rows whose inventory entry names a photo; recognized object for items whose type is on the category list from C3; text visible in the photo for items with a readable brand or model; time window for items with a receipt date; room first for the rest. One delegation per route and room, listing every item on that route.

`delegate --target photo-agent --instruction 'Find photos in the library of the current user captured strictly before the loss date and time given in this step that may show any of the household items listed in this step, using the search route named in this step. Describe each returned photo once with the local vision model and say which of the listed items are visible in it, with type, brand and model only if readable, colour, material and room. Return per photo the real path, the capture date from the photo metadata and that description, and return photos with no capture date separately as undated. If no returned photo shows a listed item, return no results for that item and say so; do not substitute a similar item. Read only.'`

After the first pass, for each item still without proof whose room already has returned photos, delegate once more with the route "ask the vision model about the photos at the real paths listed in this step" before any new search. Stop after two routes with no results for an item. An entry that does not name one object type (boxes and bags of belongings, bedding, assorted tools) is not searched: it becomes a row with proof level none and the note "owner to itemize", and C7 asks whether to split it.

**C5. Check the cameras, only for a theft or break-in, or if the user asks.** Read only.

`delegate --target security-monitor-agent --instruction 'List the cameras of the current user with their current status, then return the events recorded in the loss window given in this step by the cameras covering the rooms or entrances named in this step: people, unknown faces, vehicles and packages, with time, camera and event type, and one snapshot per event as evidence for user review. Report unknown people as unknown; do not try to name anyone the system has not already identified. If no camera covers these places, or there are no events, return no results and say so. Read only.'`

**C6. Find receipts for the affected items.** Run U4 with "with no date limit" in place of the date range, then U5 the same way, then U6 on the union of their real paths, adding to the U6 instruction the names of the affected items and asking document-agent to keep only lines that name one of them. Apply the U6 image fallback and the U7 rules to every line returned. Rows already on the inventory keep the receipt they have and are not matched again.

**C7. Build and confirm the contents list.** Build one row per affected item with the claim-list-format reference and mark its proof level. Match the damage photos from C4a to rows by room and by the items named in their descriptions. Never fill a replacement value the receipts or the user did not give. Pause and ask the user once: confirm the rows, fill values, and answer the collected questions (date conflicts, undated photos, entries to split, possible duplicates).

**C8. Write the claim document.** Pass the confirmed list as one line per row.

`delegate --target document-agent --instruction 'Draft a contents claim document in the language given in this step from the contents list given in this step, in a professional style: a heading with the claim details given in this step, a two-sentence summary of the loss as described in this step, the list rendered as a table with the column names given in this step and no value changed, and a closing list of attached photos and receipts by file name. Do not add items or values. Return the draft as text. If producing a file is unavoidable, request user approval first and return its real path.'`

If the insurer works in another language than the receipts, the user may ask for a translated copy:

`delegate --target document-agent --instruction 'Translate the claim document text given in this step into the target language given in this step, keeping the table, numbers, dates and file names unchanged. Return the translated text. If producing a file is unavoidable, request user approval first and return its real path.'`

**C9. Save the claim pack.** Tell the user that three approvals follow: the folder, the document, the album. The album holds the clearest pre-loss photo of every row plus every damage photo from C4a.

`delegate --target file-agent --instruction 'Create a folder named Claims inside the Home Contents folder at the real path given in this step if it does not exist, and inside it a folder named with the loss date and kind given in this step. These are writes, so request user approval first. Return the real path of the claim folder.'`

`delegate --target knowledge-agent --instruction 'Save the claim document text given in this step as a new Markdown file in the claim folder at the real path given in this step, with a file name starting with Contents claim followed by the loss date. This creates a file, so request user approval first. Do not overwrite any file. Return the real path of the saved file and confirm it was verified.'`

`delegate --target photo-agent --instruction 'Create an album named Claim followed by the loss date given in this step, containing exactly the pre-loss photos and damage photos at the real paths listed in this step. This changes the library, so request user approval first. Return the real album identifier.'`

Report: items with pre-loss photo and receipt, items with pre-loss photo only, items with no pre-loss proof, total of the values the user confirmed, the paths of the saved document and album, and, if the album was not created, the photo paths under "photos to attach by hand".

# Completion and failure

Handle each delegation state explicitly:

- `completed`: use only the real result returned. An expert that completes with no results means nothing was found: say so plainly for that item or category. A second search route from the search-routes reference on the same library is not another source and needs no question; widening the date range, searching documents for a photo or photos for a receipt, or swapping in a similar item is another source and is never done without asking.
- `failed`: report which step failed and why, keep every result already obtained, and stop the steps that depend on it. For example, if U10 fails, U11 and U12 still run but the report says the album was not created.
- `cancelled`: stop the mode, report what was already written (album, tags, folders, files) and what was not.
- `waiting_user`: show the question to the user and wait. Do not continue on an assumption.
- `waiting_approval`: tell the user which write is waiting (folder, album, tag or file) and wait. Never report a write as done before the expert returns `completed`.

Partial results are normal: some receipts are unreadable, some items have no pre-loss photo. The final report always separates proven rows from unproven ones and lists every failure by step and file. Nothing is deleted, moved or overwritten by this Skill, and no data leaves the NAS.
