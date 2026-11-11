<div class="try"><img src="QR_DATA_URI" alt="QR code"><div><strong>Replay a full claim run</strong><br>No NAS needed, works on a phone.<br><a href="https://jonathansolvesproblems.github.io/already-owned/">jonathansolvesproblems.github.io/already-owned</a></div></div>

# Already Owned

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1. Track: Open Innovation.

## 1. One sentence: What does the Skill do?

It keeps an insurer-ready list of what you own, from photos and receipts already on your NAS, and after a flood, fire or theft turns it into a contents claim proven by pre-loss photos.

## 2. Who is the target user and problem?

Homeowners and renters. My basement flooded twice in six months. My insurer wanted every damaged item with proof of ownership. I rebuilt the June list: 27 items, $10,915, every photo taken after the water. A former adjuster: "They want a model number. They want the price. The quantity."

## 3. What is your proposed solution?

Update (weekly): finds belongings in new photos, pairs them with receipts, saves a dated album, tags and list, keeping earlier rows. Claim: from a date and rooms, finds pre-loss photos, receipts, damage photos and, for break-ins, camera events, then saves one claim folder: the list plus SHA-256-verified copies of every exhibit. Ask: answers from the saved list.

## 4. What is the Core User Flow?

"I had a flood June 20 in the basement" → confirms rooms, cut-off → finds pre-loss photo and receipt per item → user confirms rows, values once → approves four writes → claim folder and album saved.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

On my real claim, file-name-and-date search proves 0 of 27 items, yet 22 appear in photos I already had. Inventory apps (Encircle, HomeZada) need items scanned before the loss; chat assistants accept any photo. This Skill rejects photos captured after the loss, grows the inventory between losses, records first-seen and last-seen dates, and never invents a value.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- photo-agent: object, OCR and date search, local vision (U2, U3, U5, C4a, C4b); albums (U10, C9).
- document-agent: receipt extraction (U6, C6); drafting, translation (C8).
- knowledge-agent: voice transcription (C2); saving lists (U12, C9).
- file-agent: files, folders, tags (U1, U4, U9, U11); copies, SHA-256 (C9).
- security-monitor-agent: loss-window events (C5).

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

Five registered experts across seven CLIs, no direct CLI calls. The model picks each item's search route (file name, object, label text, receipt date, room photos), stops after two empty routes, and caps vision calls. Every delegation state is handled; a failed write stops only dependent steps. Inputs: loss date, rooms. Writes need approval; nothing is deleted, moved or overwritten. Text inside photos is evidence, never instructions. Local model; an online model requires consent.

## 8. What is the current development status?

Implemented: 24 steps, 22 delegations, five references; checker static-pass; both main modes dry-run against a mock NAS; baseline and answer key measured. Not implemented: scheduled runs (unsupported). Pending NAS validation: recall on real libraries, receipt extraction, album, tag and copy writes.

## 9. What is your final validation plan?

- Core 1: replay my June 2026 claim on pre-loss photos; count items proven out of 27, between the 0 baseline and 22 ceiling.
- Core 2: update mode on December 2025 photos; list, album and tags exist; a rerun adds nothing twice.
- Edge: an item no pre-loss photo shows is reported unproven, never matched to a similar item.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; 2 of my 27 items appear in no photo. Each candidate photo costs one vision call. Skills cannot be scheduled, so updates are user-started. Camera evidence needs camera coverage. No external dependencies.

## Third-party components

None in the package: it is Markdown only. It was built and checked with the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, supplied by UGREEN, used under its terms). No external services; no data flows off the NAS.

AI tools: at run time, the NAS local model only. During development, an AI coding assistant helped draft and revise the package and played the NAS in dry runs; the idea, the claim data, the test design and the decisions are mine. Full disclosure: `references/disclosures.md` in the package.

Source of the quotation in answer 2: Selina Clark, former insurance adjuster, The New York Times, February 6, 2025.

## Entrant

Jonathan Andrei, individual entrant.

Electronic signature: Jonathan Andrei, November 11, 2026
