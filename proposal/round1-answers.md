<div class="band"><div class="lead"><h1>Already Owned</h1><div class="try"><img src="QR_DATA_URI" alt="QR code"><div><strong>Practice run:</strong><br><a href="https://jonathansolvesproblems.github.io/already-owned/">jonathansolvesproblems<br>.github.io/already-owned</a></div></div></div><img class="strip" src="STRIP_DATA_URI" alt="A contact sheet: photos taken before the loss are boxed as proof, photos taken after are crossed out."></div>

## 1. One sentence: What does the Skill do?

After a flood, fire or theft it turns the photos and receipts on your NAS into the insurer's contents claim: proof you owned each item before the loss, plus the belongings you forgot to list.

## 2. Who is the target user and problem?

Homeowners and renters. My basement flooded twice in six months; the insurer wanted proof I owned every damaged item. My June claim: 27 items, $10,915, every photo I sent taken after the water. A former adjuster: "They want a model number. They want the price. The quantity."

## 3. What is your proposed solution?

Update: finds belongings in new photos, pairs them with receipts, adds a dated page to a never-rewritten ledger. Claim: finds a pre-loss photo and receipt per lost item, then saves one claim folder with hashed copies of every exhibit. Ask: answers from the ledger.

## 4. What is the Core User Flow?

"Flood, June 20, basement" → I walk the room with a voice note → it finds each item in photos from before June 20, adds what I forgot → I confirm once → approve writes → claim folder saved.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

Walk the damaged room recording a voice note: the NAS transcribes it, matches each item to photos taken earlier for other reasons, and shows belongings in them you forgot. On my real claim such photos hold 22 of 27 items (hand-counted); file-name search finds 0. Inventory apps (Encircle, HomeZada) need items scanned beforehand.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

U: update steps. C: claim steps.

- photo-agent (ug-photo): object, label-text and capture-date search, local vision, albums (U2-U3, U5-U6b, U10, C3-C4b, C6, C9).
- document-agent (ug-document): receipt lines, claim opening, translation (U6, C6, C8).
- knowledge-agent (ug-knowledge): voice-note transcription, ledger pages, claim document (C2, U12, C9).
- file-agent (ug-filesystem, ug-filemgr, file-workflow): receipts, recordings, tags, copies, SHA-256 (U1, U4, U9, U11, C2, C9).
- security-monitor-agent (ug-surveillance): camera events (C5).

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

Delegation only. Each item gets a search route (recognized object, label text, receipt-date window), a second look at found photos, then one more route. All five delegation states handled; a declined write stops only its dependents. Inputs: date range, or loss time, kind, rooms. Writes need approval; nothing is deleted, moved or overwritten. Text in photos is evidence, never instructions. Reading experts are told: local model only.

## 8. What is the current development status?

Implemented: 24 delegation templates, seven references; checker static-pass. Five paper dry runs (AI as NAS): 69 defects found and fixed. Its 25-case test plan on paper: 22 pass, 3 partial, 0 fail; 4 of 4 safety probes. Not built: video evidence, shared libraries, scheduling. Pending NAS validation: the Skill's own count, receipt extraction, every write.

## 9. What is your final validation plan?

- Core 1: replay my June 2026 claim on pre-loss photos; count items proven of 27, between baseline 0 and ceiling 22-25.
- Core 2: update on a month of photos; page, album, tags exist; a rerun writes nothing.
- Edge: an item in no pre-loss photo is reported unproven, never swapped for a similar one.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; 3 of my 27 items are unclear in photos, 2 in none. Instruction length is untested on hardware; long lists go in parts. No outside dependencies.

## Third-party components

None in the package: it is Markdown only. It was built and checked with the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, supplied by UGREEN, used under its terms). External services and data flows: none. The Skill asks for the NAS local model and cannot override an owner's choice of an online one. Principal functionality developed for the Hackathon: all of it. Fonts in this PDF: Besley and Hanken Grotesk, SIL Open Font License.

AI tools: at run time, the Skill asks for the NAS local model only. During development, an AI coding assistant helped draft and revise the package and played the NAS in dry runs; the idea, the claim data, the test design and the decisions are mine, and I reviewed every line. The drawings above were made with an image model run on my own computer (Z-Image Turbo by Tongyi-MAI, Apache 2.0, through ComfyUI, GPL-3.0) and stand in for my photos. The linked practice run uses a made-up library. Full disclosure: `references/disclosures.md` in the package.

Source of the quotation in answer 2: Selina Clark, former insurance adjuster, The New York Times, February 6, 2025.

## Entrant

Jonathan Andrei, individual entrant.

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1. Track: Open Innovation.

Electronic signature: Jonathan Andrei, November 11, 2026
