# Already Owned

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1.

## 1. One sentence: What does the Skill do?

It keeps an insurance-ready list of what you own, built from the photos and receipts already on your NAS, and turns it into your contents claim after a flood, fire or theft.

## 2. Who is the target user and problem?

Homeowners and renters. My basement flooded twice in six months. Each time my insurer asked for every damaged item with proof I owned it. I rebuilt the June list by hand: 27 items, $10,915. Every photo on it was taken after the water, so none proved prior ownership.

## 3. What is your proposed solution?

Three modes. Update (weekly): it finds belongings in new photos, pairs them with receipts, and saves them as a dated album, file tags and a dated list. Claim: given a date and rooms, it finds photos captured before the loss, receipts, damage photos and, for a break-in, camera events, then writes the contents list. Ask: reads the saved list.

## 4. What is the Core User Flow?

"I had a flood on June 20 in the basement" → Skill confirms rooms and cut-off → finds pre-loss photo and receipt per item → user confirms rows, adds missing values → approves writes → claim document and album saved in Home Contents/Claims.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

Searching my own library by file name finds 0 of the 27 items. Inventory apps (Encircle, HomeZada) only help if you scanned every item into their cloud before the loss. This Skill uses photos you already took, enforces "before the loss" as a hard cut-off, never invents a value, and keeps everything on the NAS.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- photo-agent: object and OCR search, local vision model confirming and describing items (U2, U3, U5, C4a, C4b); albums (U10, C9).
- document-agent: receipt extraction (U6, C6), claim drafting and translation (C8).
- knowledge-agent: walk-through transcription (C2), saving lists (U12, C9).
- file-agent: receipts, folders, tags (U1, U4, U9, U11, C9).
- security-monitor-agent: loss-window events (C5, theft cases).

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

Five registered experts across seven CLIs, never calling a CLI directly. The model chooses each item's search route (object, label text, receipt date, room) and falls back once before reporting no result. Each row carries a proof level; every delegation state is handled; a failed write stops only dependent steps. All writes need approval; nothing is deleted, moved or overwritten. Local vision model; the Skill sends nothing outside the NAS.

## 8. What is the current development status?

Implemented: 24 steps, 21 delegations, three references; checker static-pass; both modes dry-run against a mock NAS. Pending NAS validation: search recall on real libraries, receipt extraction quality, and album and tag writes.

## 9. What is your final validation plan?

- Core test 1: replay my June 2026 claim with only pre-loss photos loaded; count how many of the 27 items get pre-loss proof, against a filename-and-date search.
- Core test 2: update mode on December 2025 photos and receipts; album, tags and list must exist after approval.
- Edge case: an item with no pre-loss photo is reported unproven, never matched to a similar item.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; small or hidden items may never appear in photos. Skills cannot run on a schedule, so updates are user-started. Camera evidence needs cameras covering the room.

## Third-party components

None. The Skill uses only UGREEN NAS capabilities and the NAS local model. No external services, downloads or data flows leave the NAS.

## Entrant

Jonathan Andrei, individual entrant.

Electronic signature: Jonathan Andrei, November 2, 2026
