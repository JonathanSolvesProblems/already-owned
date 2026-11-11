# Contents list format

## The ledger

The inventory is a set of dated pages in the Home Contents folder, one per update run, each named Home contents list followed by its date. A page holds only the rows added or changed in that run. Nothing is ever rewritten.

- Read the pages oldest first. A row on a later page replaces the row with the same number on an earlier page.
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
- **Purchase date** and **Price paid**: from a matched receipt only, with its currency. Empty otherwise.
- **Replacement value**: from the user only. Empty until the user gives it. Never estimated by the model.
- **Pre-loss photo**: file name and capture date of the clearest photo. In claim mode, captured before the loss time.
- **Receipt**: file name of the matched receipt, or empty. Its real path goes into Notes as "receipt path: " followed by the path.
- **Proof level**: one of `photo and receipt`, `photo only`, `receipt only`, `none`.
- **Notes**: separated by commas: the real path of the pre-loss photo, written as "path: " followed by the path, so a later claim can find it without a search; in claim mode, "on the inventory since: " followed by the date of the ledger page that first recorded the item, "first seen: " and "last seen: " followed by the capture dates of the earliest and the latest described pre-loss photos of the item, when more than one shows it; the room the user named when it differs from the photo's; anything the user added; "receipt read from photo text" where that happened; "receipt dated after first photo, confirmed by the owner" for a resolved date conflict; "owner to itemize" for an entry that is not one object; "photo shows damage" where the only photo was flagged; and, in claim mode, "damage photo: " followed by the file name.

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

- **Photo and receipt**: the receipt line names the same type of item, matching brand or model text where readable, and the first photo of the item is on or after the purchase date. If more photos matched than were described, or the date range starts less than a year before the purchase date, the first photo is not known for certain: ask instead of matching.
- **Date conflict**: the receipt names the same type of item, but the first photo of the item is before the purchase date. Ask whether the receipt is for this same item (a replacement, repair or warranty invoice) or for a second one. The same item: photo and receipt, with the note "receipt dated after first photo, confirmed by the owner". A second one: a receipt-only row.
- **Photo only**: no receipt matches. The value is for the owner to supply.
- **Receipt only**: a receipt for a durable good with no photo after the receipt-first search. In update mode, ask the user to take one photo so ownership is shown. In claim mode the row is kept as proof of purchase and no photo is asked for.
- **Accessory**: a receipt line for a cable, accessory, consumable or part. Shown as "accessory, keep?" and dropped unless the user keeps it.
- **Ambiguous**: two receipts or two items compete. Ask; never pick one silently.

## The claim pack

One folder per loss, inside Home Contents / Claims, that the user can hand over as it is.

- Exhibits: the clearest pre-loss photo of each row, every damage photo, every matched receipt, and the voice walk-through if one was used. Each is a copy. The original stays where it is, and Notes always keep the original path.
- A file whose copy does not match its original, or whose name already existed in the claim folder, is reported by name and listed as not verified.
- The document is sent in this order: the heading as one sentence; the summary as one or two sentences, both taken from the draft; the confirmed rows in the row format with the column names; the camera events as one sentence each, when the cameras were checked; the exhibit list as one sentence per file with its name, its capture time and camera model when it is a photo, and its SHA-256 value.
- A declined or failed write does not end the run. Folder declined or failed: stop and give the user the draft as text. Copies declined or failed: hash the originals with the read-only delegation, list them as exhibits by real path, and say the pack holds no copies. Album declined or failed: the report lists the photo paths to attach by hand.

## Writing an instruction

Every instruction in SKILL.md is a template. Before it is sent, each phrase "named in this step", "listed in this step", "given in this step", "confirmed with the user" and "the date of today" is replaced with the actual value, written out inside the single quotes, so the expert receives one self-contained task.

- Routes are written in words, never as a command option.
- A single quote inside a value is written with the standard shell escape. A double quote, as in the inch mark of a 55" screen, is allowed.
- A list of rows (U12, C8, C9) stays on the one line of the instruction: each row is the word Row, a colon, then its twelve values separated by semicolons in the column order above, the row number being the first value, and it ends with a full stop and a space. The expert is asked to render the rows as a Markdown table with the column names given.
- A long value (rows, exhibits, paths) is never written in the middle of a sentence. The template phrase is replaced with "listed at the end of this instruction", and the list follows the last sentence after a label: Rows, Exhibits or Paths.
- Inside a value, a semicolon is written as a comma, a pipe as the word or, and an angle bracket as the word under or over.
- Never put a table, a line break, a pipe or an angle bracket inside an instruction.
- An instruction carries at most fifteen rows, or thirty exhibit lines, or forty paths, so its length stays bounded (about 3,000 characters). A longer page or claim is sent in parts, each part its own delegation, its own file and its own approval, with the part number after the date in the file name. In a claim, part 1 carries the heading and the summary, and the last part carries the totals, the camera events and the exhibit list. Whether the NAS accepts longer instructions is checked on real hardware before these limits are raised.

Worked example: the C4b instruction for one sofa is sent with "the household items listed in this step" replaced by "a brown leather reclining three-seat sofa", "the loss date and time given in this step" replaced by "2026-06-20 02:00 local time", and "the search route named in this step" replaced by "recognized object sofa".
