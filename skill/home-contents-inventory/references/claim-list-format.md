# Contents list format

Use this table for the inventory (update mode) and for the claim (claim mode). The columns follow what home insurers ask for on a contents list: what the item is, how many, what it cost, and the proof of ownership and value.

| # | Item | Description | Room | Qty | Purchase date | Price paid | Replacement value | Pre-loss photo | Receipt | Proof level | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Column rules:

- **Item**: short noun phrase, for example "Leather reclining sofa, 3-seat".
- **Description**: brand, model, colour, material and size, only as read from a photo or a receipt. Write "not visible" for anything that could not be read.
- **Purchase date** and **Price paid**: from a matched receipt only, with its currency. Empty otherwise.
- **Replacement value**: from the user only. Empty until the user gives it. Never estimated by the model.
- **Pre-loss photo**: file name and capture date of the clearest photo. In claim mode, captured before the loss time.
- **Receipt**: file name of the matched receipt, or empty.
- **Proof level**: one of `photo and receipt`, `photo only`, `receipt only`, `none`.
- **Notes**: anything the user added, and "damage photo: file name" in claim mode.

Totals:

- Sum **Price paid** and **Replacement value** separately, per currency, only over rows that have a value. State how many rows have no value.

Privacy:

- The list names files and belongings only. It holds no street address, account number or policy number unless the user typed it in for the claim heading.
