# Contents list format

Use this table for the inventory (update and ask modes) and for the claim (claim mode). The columns follow what home insurers ask for on a contents list: what the item is, how many, what it cost, and the proof of ownership and value.

| # | Item | Description | Room | Qty | Purchase date | Price paid | Replacement value | Pre-loss photo | Receipt | Proof level | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

When a list is passed to an expert inside an instruction, it uses the row format under "Writing an instruction" below. Because the semicolon separates the values there, the notes inside Notes are separated by commas, never by a semicolon.

Column rules:

- **Item**: short noun phrase, for example "Leather reclining sofa, 3-seat".
- **Description**: brand, model, colour, material and size, only as read from a photo or a receipt. Write "not visible" for anything that could not be read.
- **Room**: as seen in the photo. If the user named a different room, keep the photo's room and note the user's in Notes.
- **Qty**: identical items shown side by side are one row with the count here.
- **Purchase date** and **Price paid**: from a matched receipt only, with its currency. Empty otherwise.
- **Replacement value**: from the user only. Empty until the user gives it. Never estimated by the model.
- **Pre-loss photo**: file name and capture date of the clearest photo. In claim mode, captured before the loss time.
- **Receipt**: file name of the matched receipt, or empty.
- **Proof level**: one of `photo and receipt`, `photo only`, `receipt only`, `none`.
- **Notes**: separated by commas: the real path of the pre-loss photo, written as "path: " followed by the path, so a later claim can find it without a search; in claim mode, "first seen: " and "last seen: " followed by the capture dates of the earliest and the latest described pre-loss photos of the item, when more than one shows it; the room the user named when it differs from the photo's; anything the user added; "receipt read from photo text" where that happened; "receipt dated after first photo, confirmed by the owner" for a resolved date conflict; "owner to itemize" for an entry that is not one object; "photo shows damage" where the only photo was flagged; and, in claim mode, "damage photo: " followed by the file name.

Totals:

- Sum **Price paid** and **Replacement value** separately, per currency, only over rows that have a value. State how many rows have no value.

Exhibits (claim mode):

- Below the table, the claim document lists every exhibit in the claim folder (pre-loss photos, damage photos, receipts) with its file name and SHA-256 value, as returned by the file expert. A value is never typed or guessed; a file whose copy did not match its original, or whose name already existed in the claim folder, is listed as not verified. When the copies were declined, the originals are listed by real path with their own SHA-256.
- For a theft, the camera events for the loss window are listed between the table and the exhibits, one line each with time, camera and event type. They are never rows.

Privacy:

- The list names files and belongings only. It holds no street address, account number or policy number unless the user typed it in for the claim heading.

## Writing an instruction

Every instruction in SKILL.md is a template. Before it is sent, each phrase "named in this step", "listed in this step", "given in this step", "confirmed with the user" and "the date of today" is replaced with the actual value, written out inside the single quotes, so the expert receives one self-contained task.

- Routes are written in words, never as a command option.
- A single quote inside a value is written with the standard shell escape. A double quote, as in the inch mark of a 55" screen, is allowed.
- A list of rows (U12, C8, C9) stays on the one line of the instruction: each row begins with the word Row and its number followed by a colon, its twelve values are separated by semicolons in the column order above, and the next row follows after a full stop and a space. The expert is asked to render the rows as a Markdown table with the column names given.
- Inside a value, a semicolon is written as a comma, a pipe as the word or, and an angle bracket as the word under or over.
- Never put a table, a line break, a pipe or an angle bracket inside an instruction.

Worked example: the C4b instruction for one sofa is sent with "the household items listed in this step" replaced by "a brown leather reclining three-seat sofa", "the loss date and time given in this step" replaced by "2026-06-20 02:00 local time", and "the search route named in this step" replaced by "recognized object sofa".
