# Contents list format

## The ledger

The inventory is a set of dated pages in the Home Contents folder, one per update run, each named Home contents list followed by its date, with that same name as its first line. A page holds only the rows added or changed in that run. Nothing is ever rewritten.

- Read the pages oldest first, by the date in their first line. A row on a later page replaces the row with the same number on an earlier page.
- After a page is saved it is read back and compared with the rows that were sent (U12). A page that differs is reported, and the correct rows are saved again as a later page.
- The ledger is read whole on every run. Pages are short and a run with nothing new writes none, so years of use stay small; folding old pages into one is not built.
- New rows are numbered on from the highest number in the ledger. A changed row keeps its number.
- The date of the page where a number first appears is the date the item was recorded. In a claim it goes into Notes as "on the inventory since", because a record made before the loss is evidence in its own right. If that date is on or after the loss date, write "recorded after the loss" instead.
- A receipt line or a new photo that matches a row already in the ledger is decided by the same rules as a new one, using that row's Pre-loss photo date as the first photo. Once the user confirms, the row keeps its number and is saved as a changed row.
- Two runs on the same day: the second page carries the time of day as four digits after the date, and pages of the same date are read in that order.
- Ask mode and claim mode read every page and show one list. The user never has to open the pages one by one.

## The columns

Use this table for the inventory (update and ask modes) and for the claim (claim mode). The columns follow what home insurers ask for on a contents list: what the item is, how many, what it cost, and the proof of ownership and value.

| # | Item | Description | Room | Qty | Purchase date | Price paid | Replacement value | Pre-loss photo | Receipt | Proof level | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

When a list is passed to an expert inside an instruction, it uses the row format under "Writing an instruction" below. Because the semicolon separates the values there, the notes inside Notes are separated by commas, never by a semicolon.

Column rules:

- **Item**: short noun phrase, for example "Leather reclining sofa, 3-seat".
- **Description**: brand, model, colour, material and size, only as read from a photo or a receipt. Write "not visible" for anything that could not be read.
- **Room**: as seen in the photo. If the user named a different room, the match is confirmed with the user first; then keep the photo's room and note the user's in Notes. If no room can be seen, the user is asked once; a row left without one is shown last, under "room not recorded", and is still offered in a claim.
- **Qty**: identical items shown side by side are one row with the count here.
- **Purchase date** and **Price paid**: from a matched receipt only. The purchase date is the date printed on the receipt, never the date in its file name or its modification date. The price is the price of the line as printed, before tax, with its currency, or followed by "currency not printed" until the user names it. Both are empty when no receipt matches.
- **Replacement value**: from the user only. Empty until the user gives it. Never estimated by the model.
- **Pre-loss photo**: file name and capture date of the clearest photo. In claim mode, captured before the loss time.
- **Receipt**: file name of the matched receipt, or empty. Its real path goes into Notes as "receipt path: " followed by the path.
- **Proof level**: one of `photo and receipt`, `photo only`, `receipt only`, `none`.
- **Notes**: separated by commas: the real path of the pre-loss photo, written as "path: " followed by the path, so a later claim can find it without a search; in claim mode, for a row taken from the inventory, "on the inventory since: " followed by the date of the ledger page that first recorded the item, "first seen: " and "last seen: " followed by the capture dates of the earliest and the latest described pre-loss photos of the item (first seen alone when a single photo shows it); the room the user named when it differs from the photo's; anything the user added; "receipt read from photo text" where that happened; "receipt dated after first photo, confirmed by the owner" for a resolved date conflict; "owner to itemize" for an entry that is not one object; "photo shows damage" where the only photo was flagged; "search failed" when the search for the item failed, which is not the same as no proof; "open question: " followed by what was asked, when the user left a question about the row unanswered; "condition: " followed by the owner's own word (new, average, below average) when they give one; and, in claim mode, "damage photo: " followed by the file name.

Totals:

- Sum **Price paid** and **Replacement value** separately, per currency, only over rows that have a value. State how many rows have no value.

Exhibits (claim mode):

- Below the table, the claim document lists every exhibit in the claim folder (pre-loss photos, damage photos, receipts) with its file name, its capture time and camera model as read from the photo metadata when it is a photo, and its SHA-256 value as returned by the file expert. A value is never typed or guessed; a file whose copy did not match its original, or whose name already existed in the claim folder, is listed as not verified. When the copies were declined, the originals are listed by real path with their own SHA-256.
- When the cameras were checked, their events are listed between the table and the exhibits, one line each with time, camera and event type. They are never rows.
- A receipt has no capture time or camera; a photo whose metadata names no camera is listed as "not recorded" in that column.

Privacy:

- The list names files and belongings only. It holds no street address, account number or policy number unless the user typed it in for the claim heading.

## Deciding a row

Step U7, and C6 in claim mode, give every item and every receipt line exactly one outcome:

- **Photo and receipt**: the receipt line names the same type of item, matching brand or model text where readable, and the first photo of the item is on or after the purchase date. Every search describes its earliest match, so the first photo within the searched dates is known. Only when the searched dates start after the purchase date is the first photo not known for certain: then ask instead of matching.
- **Date conflict**: the receipt names the same type of item, but the first photo of the item is before the purchase date. Ask whether the receipt is for this same item (a replacement, repair or warranty invoice) or for a second one. The same item: photo and receipt, with the note "receipt dated after first photo, confirmed by the owner". A second one: a receipt-only row.
- **Photo only**: no receipt matches. The value is for the owner to supply.
- **Receipt only**: a receipt for a durable good with no photo after the receipt-first search. In update mode, ask the user to take one photo so ownership is shown. In claim mode the row is kept as proof of purchase and no photo is asked for.
- **Accessory**: a receipt line for a cable, accessory, consumable or part. Shown as "accessory, keep?" and dropped unless the user keeps it.
- **Ambiguous**: two receipts or two items compete. Ask; never pick one silently.

## The claim pack

One folder per loss, inside Home Contents / Claims, that the user can hand over as it is.

- Exhibits: the clearest pre-loss photo of each row, every damage photo, every matched receipt, and the voice walk-through if one was used. Each is a copy. The original stays where it is, and Notes always keep the original path.
- A file whose copy does not match its original, or whose name already existed in the claim folder, is reported by name and listed as not verified.
- The document is sent in this order: the heading as one sentence; the summary as the two sentences of the draft; the confirmed rows in the row format with the column names; the camera events as one sentence each, when the cameras were checked; the exhibit list as one sentence per file with its name, its capture time and camera model when it is a photo, and its SHA-256 value.
- Before the copies, the user chooses: copies in the folder (the NAS may ask once per file), or originals left in place with the SHA-256 of each recorded.
- Each saved part of the document is read back and compared with what was sent, every value and every SHA-256, before the pack is reported as saved.
- A declined or failed write does not end the run. Folder declined or failed: stop and give the user the draft as text. Copies declined or failed: hash the originals with the read-only delegation, list them as exhibits by real path, and say the pack holds no copies. Album declined or failed: the report lists the photo paths to attach by hand.

## Writing an instruction

Every instruction in SKILL.md is a template with slots in braces, such as {paths}, {loss time} or {rows}. Before it is sent, each slot is replaced with the real value, written out inside the single quotes, so the expert receives one self-contained task. No brace is ever sent.

- {date range} is written as words the sentence can carry: "between 2026-05-01 and 2026-06-01", or "at any date".
- {today} is the date of the run, as U1 returned it from the NAS. It carries the time of day as four digits after the date when a page of that date already exists, and the word part and a digit when the list is sent in parts. {loss date} in a claim file name carries the part the same way.
- {route} is written in words ("recognized object sofa", "text visible in the photo: the model name"), never as a command option.
- An apostrophe inside a value is left out (owners manual). A double quote, as in the inch mark of a 55" screen, is allowed.
- {rows} stays on the one line of the instruction: each row is the word Row, a colon, then its twelve values separated by semicolons in the column order above, the row number being the first value; a row ends where the next Row begins, so a full stop inside a file name is harmless. The expert is asked to render the rows as a Markdown table with the column names given.
- A long value (rows, exhibits) is never written in the middle of a sentence. Its slot sits at the end of the instruction after a label: Heading, Summary, Rows, Totals, Camera events or Exhibits. A label that has nothing to carry is left out with its slot; the sentence that lists the parts stays as written.
- {column names} is written as: #, Item, Description, Room, Qty, Purchase date, Price paid, Replacement value, Pre-loss photo, Receipt, Proof level, Notes.
- {exhibits} stays on the one line: each exhibit is the word Exhibit, a colon, then its file name, capture time, camera and SHA-256 separated by semicolons; an exhibit ends where the next Exhibit begins.
- Inside a value, a semicolon is written as a comma, a pipe as the word or, and an angle bracket as the word under or over. That is for words. A real path is never rewritten: a file whose path holds an apostrophe, a semicolon, a pipe or an angle bracket cannot be passed faithfully, so it is left out and listed in the report as "path cannot be passed".
- Never put a table, a line break, a pipe or an angle bracket inside an instruction.
- An instruction carries at most ten lines, counting rows and exhibit lines together (the heading, summary, totals and camera events are not counted), and at most six rows when it saves a claim, whose rows carry longer notes. That keeps an instruction under about 4,000 characters, which is as long as an instruction should get. A longer page or claim is sent in parts, each part its own delegation, its own file and its own approval. In a claim, part 1 carries the heading and the summary; the rows follow in order; then come the totals, the camera events and the exhibit lines, continuing into further parts as needed.
- {paths} carries at most forty paths, and at most ten when the expert has to read each file with a model (describe, read text, extract). Copies, hashes and reads continue in further delegations. An album takes the first forty photos, pre-loss photos first, and the report says how many were left out.
- Whether the NAS accepts longer instructions is checked on real hardware before these limits are raised.

Worked example: the C4b instruction for one sofa is sent with {loss time} replaced by "2026-03-14 07:30 local time", {items} by "a brown leather reclining three-seat sofa", and {route} by "recognized object sofa".
