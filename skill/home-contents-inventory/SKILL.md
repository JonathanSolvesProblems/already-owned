---
name: home-contents-inventory
description: A home contents inventory for insurance, built from the photos and receipts already on the NAS, with a pre-loss photo and proof of purchase behind each item, plus an insurer-ready contents list after a flood, fire or theft. Use when the user says "update my home inventory", "file this week's receipts into my inventory", "what do I own in the basement", "I had a flood / fire / break-in, list what I lost", or "prepare my contents claim".
---

# Goal

Keep a running list of the household belongings the user owns, each backed by a real photo taken before any loss and, where one exists, a real receipt, without the user typing or re-photographing anything. When something happens, turn that list into the contents list an insurer asks for, restricted to photos taken before the loss.

The Skill has two modes, chosen from what the user says:

- **Update mode** (routine, about weekly): "update my home inventory", "file this week's receipts".
- **Claim mode** (after a loss): "I had a flood on June 20 in the basement", "prepare my contents claim".

If the request fits neither mode, ask which one the user wants and stop until they answer.

Supported scope: the photo library, documents and receipts of the current user on this NAS, and, in claim mode only, the user's own surveillance events for the time of the loss. Out of scope: estimating market prices, contacting the insurer, and anything outside the NAS. Replacement values come only from receipts or from the user, never from the model.

# Required input

Update mode:

- The date range to cover. Default: from the date of the newest Home contents list in the Home Contents folder to today; on the first run, ask the user how far back to go.

Claim mode:

- Date and time of the loss, and its kind: water, fire, theft or other.
- The affected rooms.
- Optionally, the items the user knows were lost, typed or as a voice recording on the NAS (for example a walk-through of the room).
- The insurer and claim number, if the user wants them on the list.

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

## Update mode

**U1. Find the existing inventory.** Read only.

`delegate --target file-agent --instruction 'Find the folder named Home Contents in the personal space of the current user. If it exists, return its real path, and the real path, modification date and full text of the newest Markdown file in it whose name starts with Home contents list. If the folder does not exist, report that it does not exist. Read only: create, move or change nothing.'`

If the folder does not exist, this is the first run: tell the user, confirm the date range to cover, and continue with an empty inventory.

**U2. Find which kinds of belongings the photos show.** Read only.

`delegate --target photo-agent --instruction 'Using the recognition index of the photo library of the current user, list the recognized object categories that are durable household belongings an insurer would cover: furniture, televisions and screens, computers, phones and tablets, cameras, kitchen and laundry appliances, bicycles, musical instruments, tools, sports equipment, jewellery and artwork. For each category return its name and the number of matching photos taken in the date range confirmed with the user. Exclude people, pets, food, documents and screenshots. If no category matches, return an empty result and say so. Read only.'`

If the result is empty, report no results for this date range and stop update mode. Otherwise show the categories with counts and ask the user which to include (`waiting_user`).

**U3. Find and describe each distinct item.** One delegation per confirmed category. Choose the route for each category with the search-routes reference, then pass the chosen route in the instruction.

`delegate --target photo-agent --instruction 'For the household object category named in this step, search the photos of the current user taken in the confirmed date range, using the search route named in this step (recognized object, text visible in the photo, folder, or a time window). Group photos that show the same physical item. For each distinct item, pick the clearest photo and describe it with the local vision model: item type, brand and model only if readable in the photo, colour, material, approximate size, and the room if it can be seen. Return per item the description, the real path and capture date of the chosen photo, and the real paths of other photos of the same item. Write not visible instead of guessing a brand or model. If nothing is found, return no results for this category. Read only.'`

Items already on the existing list with the same description are matched, not added again.

**U4. Find receipt files.** Read only.

`delegate --target file-agent --instruction 'In the Documents, Downloads and Scans folders of the personal space of the current user, find PDF and image files modified in the confirmed date range whose names or locations suggest receipts, invoices or order confirmations. Return each real path, name and modification date. If none are found, return no results. Read only.'`

**U5. Find receipts that were photographed.** Read only.

`delegate --target photo-agent --instruction 'Search the photos of the current user taken in the confirmed date range for receipts and invoices, using the text recognized in the photo (words such as total, subtotal, receipt, invoice, tax). Return the real path and capture date of each photo that shows a receipt, and the full recognized text of each one. If none are found, return no results. Read only.'`

**U6. Extract the purchase lines.** Read only. Pass the union of real paths from U4 and U5. If both returned no results, go to U7 with no receipts.

`delegate --target document-agent --instruction 'Extract the purchased line items from the receipt and invoice files at the real paths listed in this step: merchant, purchase date, item description, brand and model if printed, quantity, price paid and currency, and the source path. Keep text in its original language and add a short English item description. Ignore groceries, restaurants, fuel, services and subscriptions. Report each file that could not be read as a failure with its path. If no durable household item is found, return an empty result. Read only.'`

If `document-agent` reports a photographed receipt as a failure, use the recognized text that U5 returned for that photo instead: read the merchant, date, item lines and prices from that text, mark those rows "receipt read from photo text", and show them to the user in U8 like every other row. Never fill a line that is not in the text.

**U7. Match and decide each row.** Done by this Skill, not by an expert. For every item and every receipt line, decide one of:

- **Photo and receipt**: the receipt line names the same type of item, matching brand or model text where readable, and the first photo of the item is on or after the purchase date.
- **Photo only**: no receipt matches. Value to be supplied by the owner.
- **Receipt only**: a receipt for a durable good with no photo. Ask the user to take one photo so ownership is shown.
- **Ambiguous**: two receipts or two items compete. Ask the user (`waiting_user`); never pick one silently.

**U8. Confirm with the user.** Show the new and changed rows in the format from the claim-list-format reference and ask the user to confirm, remove or correct rows, and to add replacement values for photo-only rows if they wish (`waiting_user`). Nothing is written before this confirmation.

**U9. Create the folder if needed.** Only on a first run.

`delegate --target file-agent --instruction 'Create a folder named Home Contents in the personal space of the current user. This is a write, so request user approval first. Return the real path of the created folder.'`

**U10. Add the item photos to the album.** Pass the real paths of the confirmed rows only.

`delegate --target photo-agent --instruction 'Create an album named Home contents followed by the date of today in the library of the current user, containing exactly the photos at the real paths listed in this step. Add no other photo. This changes the library, so request user approval first, and return the real album identifier and the number of photos added.'`

Each update run makes its own dated album, because the public album capability creates albums and does not add to an existing one. The file tag from U11 is what links every inventory photo across runs.

**U11. Tag the photos and receipts.**

`delegate --target file-agent --instruction 'Make sure a file tag named home-contents exists, creating it only if it is missing, then attach that tag to each file at the real paths listed in this step (item photos and receipt files of the confirmed rows). These are writes, so request user approval first. Return the tag identifier and, per path, whether tagging succeeded.'`

**U12. Save the updated list.**

`delegate --target knowledge-agent --instruction 'Save the Markdown text given in this step as a new file in the folder at the real path given in this step, with a file name starting with Home contents list followed by the date of today. Do not overwrite or delete any existing file. Return the real path of the saved file and confirm it was verified.'`

Report: rows added, rows changed, photo-only rows still without a value, receipt-only rows still without a photo, and the path of the saved list.

## Claim mode

**C1. Collect the loss.** Confirm the date and time of the loss, its kind, the affected rooms, the insurer and claim number if wanted. The cut-off for evidence is the loss time: only photos captured before it count as proof of ownership.

**C2. Transcribe a voice walk-through, if the user gave one.** Read only.

`delegate --target knowledge-agent --instruction 'Transcribe the audio recording at the real path given by the user in this step and return the transcript text and its segments. If the recording cannot be read, return a failure with the path. Read only.'`

From the transcript, list each belonging the user mentions with the room. Show the list to the user to confirm (`waiting_user`).

**C3. Read the existing inventory.** Same instruction as U1. If there is no inventory, continue from the items named in C1 or C2 alone and tell the user.

**C4. Find pre-loss proof for each affected item.** One delegation per item: every inventory row in an affected room, plus every item the user named that is not on the inventory. Choose the route per item with the search-routes reference.

`delegate --target photo-agent --instruction 'Find photos of the household item described in this step in the library of the current user, captured strictly before the loss date and time given in this step, using the search route named in this step. Confirm with the local vision model that the item is visible in each returned photo, and describe it: type, brand and model only if readable, colour, material and room. Return the real path and capture date of the clearest pre-loss photo and of up to three others. Then separately return the real paths of photos of the same room captured after the loss time, as damage photos. If no pre-loss photo shows the item, return no results for pre-loss proof and say so; do not substitute a similar item.'`

**C5. Check the cameras, only for a theft or break-in, or if the user asks.** Read only.

`delegate --target security-monitor-agent --instruction 'List the cameras of the current user that are online or recorded during the loss window given in this step. For cameras covering the affected rooms or entrances, return the events in that window for people, unknown faces, vehicles and packages, with time, camera and event type, and one snapshot per event as evidence for user review. Report unknown people as unknown; do not attempt to name anyone the system has not already identified. If no camera covers these places, or there are no events, return no results and say so. Read only.'`

**C6. Find receipts for the affected items.** Run U4 and U6 with no date limit, restricted to the affected items; reuse rows already on the inventory.

**C7. Build and confirm the contents list.** Build one row per affected item with the claim-list-format reference. Mark each row's proof level. Never fill a replacement value the receipts or the user did not give. Show the list to the user and ask them to confirm and fill values (`waiting_user`).

**C8. Write the claim document.**

`delegate --target document-agent --instruction 'Draft a contents claim document from the confirmed table given in this step, in a professional style: a heading with the claim details given in this step, a two-sentence summary of the loss, the table unchanged, and a closing list of attached photos and receipts by file name. Do not change any value in the table and do not add items. Write it in the language given in this step. Return the draft text and output file if one is produced.'`

If the insurer works in another language than the receipts, the user may ask for a translated copy:

`delegate --target document-agent --instruction 'Translate the claim document text given in this step into the target language given in this step, keeping the table, numbers, dates and file names unchanged. Return the translated text.'`

**C9. Save the claim pack.**

`delegate --target file-agent --instruction 'Create a folder named Claims inside the Home Contents folder at the real path given in this step if it does not exist, and inside it a folder named with the loss date and kind given in this step. These are writes, so request user approval first. Return the real path of the claim folder.'`

`delegate --target knowledge-agent --instruction 'Save the claim document text given in this step as a new Markdown file in the claim folder at the real path given in this step, with a file name starting with Contents claim followed by the loss date. Do not overwrite any file. Return the real path of the saved file and confirm it was verified.'`

`delegate --target photo-agent --instruction 'Create an album named Claim followed by the loss date given in this step, containing exactly the pre-loss photos and damage photos at the real paths listed in this step. This changes the library, so request user approval first. Return the real album identifier.'`

Report: items with pre-loss photo and receipt, items with pre-loss photo only, items with no pre-loss proof, total of the values the user confirmed, and the paths of the saved document and album.

# Completion and failure

Handle each delegation state explicitly:

- `completed`: use only the real result returned. An expert that completes with no results means nothing was found: say so plainly for that item or category, and do not widen the date range, swap in a similar item, or search another source without asking.
- `failed`: report which step failed and why, keep every result already obtained, and stop the steps that depend on it. For example, if U10 fails, U11 and U12 still run but the report says the album was not updated.
- `cancelled`: stop the mode, report what was already written (album, tags, files) and what was not.
- `waiting_user`: show the question to the user and wait. Do not continue on an assumption.
- `waiting_approval`: tell the user which write is waiting (folder, album, tag or file) and wait. Never report a write as done before the expert returns `completed`.

Partial results are normal: some receipts are unreadable, some items have no pre-loss photo. The final report always separates proven rows from unproven ones and lists every failure by step and file. Nothing is deleted, moved or overwritten by this Skill, and no data leaves the NAS.
