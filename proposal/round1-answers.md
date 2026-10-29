# Already Owned

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1.

## 1. One sentence: What does the Skill do?

It keeps an insurance-ready list of what you own, built from the photos and receipts already on your NAS, and turns it into your contents claim after a flood, fire or theft.

## 2. Who is the target user and problem?

Homeowners and renters. My basement flooded twice in six months. Each time my insurer asked for every damaged item with proof I owned it. I rebuilt the June list by hand: 27 items, $10,915. Every photo on it was taken after the water, so none proved ownership before the loss.

## 3. What is your proposed solution?

Two modes. Update (weekly): it finds belongings in new photos, pairs them with receipts, and saves them as a dated album, file tags and a dated list. Claim: given a date and rooms, it finds photos captured before the loss, receipts, damage photos and, for a break-in, camera events, then writes the contents list.

## 4. What is the Core User Flow?

"I had a flood on June 20 in the basement" → Skill confirms rooms and cut-off → finds pre-loss photo and receipt per item → user confirms rows and adds missing values → approves writes → claim document, claim album and tags saved in Home Contents/Claims.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

Inventory apps (Encircle, HomeZada) only help if you photographed or scanned every item into their cloud before the loss. This Skill uses photos you already took, enforces "before the loss" as a hard cut-off, never invents a value, and keeps your belongings, receipts and camera footage at home.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- Photos (photo-agent): object and text search, local vision model to confirm and describe items, albums.
- Documents (document-agent): receipt extraction, claim drafting, translation.
- Knowledge (knowledge-agent): voice walk-through transcription, saving lists.
- Files (file-agent): finding receipts, folders, tags.
- Surveillance (security-monitor-agent): loss-window events, claim mode only.

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

One SKILL.md delegating to five registered experts across seven CLIs, never calling a CLI directly. The model chooses each item's search route (object, label text, receipt date window, room) from what it knows, and falls back once before reporting no result. Each row carries a proof level. All writes need approval; nothing is deleted, moved or overwritten. Local model only; no data leaves the NAS.

## 8. What is the current development status?

Implemented: the full Skill package; the official checker returns static-pass with zero warnings. Pending NAS validation: search recall on real libraries, receipt extraction quality, and album and tag writes.

## 9. What is your final validation plan?

- Core test 1: replay my June 2026 claim with only pre-loss photos loaded; count how many of the 27 items get pre-loss proof, against a filename-and-date search.
- Core test 2: replay my December 2025 claim the same way.
- Edge case: an item with no pre-loss photo must be reported as unproven, never matched to a similar item.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; small or hidden items may never appear in photos. Values exist only when receipts or the user supply them. Skills cannot run on a schedule, so updates are user-started. Camera evidence needs UGREEN cameras covering the room.

## Third-party components

None. The Skill uses only UGREEN NAS capabilities and the NAS local model. No external services, downloads or data flows leave the NAS.

## Entrant

Jonathan Andrei, individual entrant.

Electronic signature: Jonathan Andrei, October 29, 2026
