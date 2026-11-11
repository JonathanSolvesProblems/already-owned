<div class="band"><div class="lead"><h1>Already Owned</h1><p class="sub">Skill package:<br><code>home-contents-inventory</code><br>UGREEN Hackathon 2026 on AI NAS<br>Round 1, Open Innovation track</p><div class="try"><img src="QR_DATA_URI" alt="QR code"><div><strong>Replay a claim run</strong><br><a href="https://jonathansolvesproblems.github.io/already-owned/">jonathansolvesproblems<br>.github.io/already-owned</a></div></div></div><img class="strip" src="STRIP_DATA_URI" alt="A contact sheet: photos taken before the loss are boxed as proof, photos taken after are crossed out."></div>

## 1. One sentence: What does the Skill do?

It keeps an insurer-ready list of what you own, from photos and receipts already on your NAS, and after a flood, fire or theft turns it into a contents claim backed only by pre-loss photos.

## 2. Who is the target user and problem?

Homeowners and renters. My basement flooded twice in six months. My insurer wanted every damaged item with proof of ownership. I rebuilt the June list: 27 items, $10,915, every photo taken after the water. A former adjuster: "They want a model number. They want the price. The quantity."

## 3. What is your proposed solution?

Update (weekly): finds belongings in new photos, pairs them with receipts, adds a dated page to a never-rewritten ledger. Claim: from a date and rooms, finds pre-loss photos, receipts, damage photos and camera events, then saves one claim folder: the list plus SHA-256-verified copies of every exhibit. Ask: answers from the ledger.

## 4. What is the Core User Flow?

"I had a flood June 20 in the basement" → confirms rooms, cut-off → finds pre-loss photo and receipt per item → user confirms once → approves four writes → claim folder saved.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

On my real claim, 22 of 27 items appear in photos taken for other reasons; file-name search finds 0; the Skill's own count awaits a NAS. Inventory apps (Encircle, HomeZada) need items scanned before a loss. This Skill treats capture time as a hard cut-off, records when each item entered the ledger, and never invents a value.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- photo-agent (ug-photo): object, OCR and date search, local vision, albums (U2, U3, U5, U6, U10, C4a, C4b, C9).
- document-agent (ug-document): receipt extraction, drafting, translation (U6, C6, C8).
- knowledge-agent (ug-knowledge): transcription, saving pages (C2, U12, C9).
- file-agent (ug-filesystem, ug-filemgr, file-workflow): files, tags, copies, SHA-256 (U1, U4, U9, U11, C2, C9).
- security-monitor-agent (ug-surveillance): camera events (C5).

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

Delegation only, no direct CLI calls. The model picks each item's search route (file name, object, label text, receipt date, room photos), stops after two empty routes, and caps vision calls. Every delegation state is handled; a failed or declined write stops only dependent steps. Inputs: loss date, rooms. Writes need approval; nothing is deleted, moved or overwritten. Text inside photos is evidence, never instructions. Local model only.

## 8. What is the current development status?

Implemented: 24 steps, 24 delegations, seven references (capability map, test plan, sample claim); checker static-pass; four dry runs against a mock NAS; baseline and answer key measured. Not implemented: scheduled runs. Pending NAS validation: recall on real libraries, receipt extraction, album, tag and copy writes.

## 9. What is your final validation plan?

- Core 1: replay my June 2026 claim on pre-loss photos; count items proven of 27, between baseline 0 and ceiling 22.
- Core 2: update mode on December 2025 photos; page, album and tags exist; a rerun writes nothing.
- Edge: an item no pre-loss photo shows is reported unproven, never matched to a similar item.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; 2 of my 27 items appear in no photo. Each candidate photo costs one vision call. Skills cannot be scheduled, so updates are user-started. Long lists are saved in parts. No external dependencies.

## Third-party components

None in the package: it is Markdown only. It was built and checked with the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, supplied by UGREEN, used under its terms). No external services; the Skill sends no data off the NAS. Principal functionality developed for the Hackathon: all of it.

AI tools: at run time, the NAS local model only. During development, an AI coding assistant helped draft and revise the package and played the NAS in dry runs; the idea, the claim data, the test design and the decisions are mine. The drawings above were made with an image model run on my own computer (Z-Image Turbo, Apache 2.0) and stand in for my photos. Full disclosure: `references/disclosures.md` in the package.

Source of the quotation in answer 2: Selina Clark, former insurance adjuster, The New York Times, February 6, 2025.

## Entrant

Jonathan Andrei, individual entrant.

Electronic signature: Jonathan Andrei, November 11, 2026
