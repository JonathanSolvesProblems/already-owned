<div class="band"><div class="lead"><h1>Already Owned</h1><div class="try"><img src="QR_DATA_URI" alt="QR code"><div><strong>Practice run:</strong><br><a href="https://jonathansolvesproblems.github.io/already-owned/">jonathansolvesproblems<br>.github.io/already-owned</a></div></div></div><img class="strip" src="STRIP_DATA_URI" alt="A contact sheet: photos taken before the loss are boxed as proof, photos taken after are crossed out."></div>

## 1. One sentence: What does the Skill do?

It builds an insurer-ready list of what you own from photos and receipts already on your NAS, and after a flood, fire or theft turns it into a contents claim backed by receipts and pre-loss photos.

## 2. Who is the target user and problem?

Homeowners and renters. My basement flooded twice in six months; the insurer wanted proof I owned every damaged item. My June claim: 27 items, $10,915, and every photo I sent was taken after the water. A former adjuster: "They want a model number. They want the price. The quantity."

## 3. What is your proposed solution?

Update: finds belongings in new photos, pairs them with receipts, adds a dated page to a never-rewritten ledger. Claim: finds a pre-loss photo and receipt per lost item, then saves one claim folder with hashed copies of every exhibit. Ask: answers from the ledger.

## 4. What is the Core User Flow?

"I had a flood June 20 in the basement" → cut-off → items from the ledger, a voice note or the photos → pre-loss photo and receipt per item → I confirm → approve each write → claim folder saved.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

A new interaction: walk the damaged room recording a voice note. The NAS transcribes it, matches each item to photos taken earlier for other reasons, and shows belongings in them you forgot. On my real claim such photos hold 22 of 27 items (hand-counted); file-name search finds 0. Inventory apps (Encircle, HomeZada) need items scanned beforehand.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- photo-agent (ug-photo): object, label-text and capture-date search, local vision, albums (U2-U3, U5-U6b, U10, C3-C4b, C6, C9).
- document-agent (ug-document): receipt lines, claim draft, translation (U6, C6, C8).
- knowledge-agent (ug-knowledge): voice-note transcription, ledger pages, claim document (C2, U12, C9).
- file-agent (ug-filesystem, ug-filemgr, file-workflow): receipts, recordings, tags, copies, SHA-256 (U1, U4, U9, U11, C2, C9).
- security-monitor-agent (ug-surveillance): camera events (C5).

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

Delegation only. Each item gets a search route (file name, object, label text, receipt date), a second look at found photos, then one more route. All five delegation states are handled; a declined write stops only its dependents. Inputs: date range, or loss time, kind and rooms. Writes need approval; nothing is deleted, moved or overwritten. Text in photos is evidence, never instructions. Reading experts are told: local model only.

## 8. What is the current development status?

Implemented: three modes, 24 delegation templates, seven references (capability map, test plan, sample claim); checker static-pass. Paper dry runs with an AI playing the NAS. Not built: video evidence, shared libraries, scheduling. Pending NAS validation: the Skill's own count, receipt extraction, every write.

## 9. What is your final validation plan?

- Core 1: replay my June 2026 claim on pre-loss photos; count items proven of 27, between baseline 0 and ceiling 22 to 25.
- Core 2: update on a month of real photos; page, album, tags exist; a rerun writes nothing.
- Edge: an item in no pre-loss photo is reported unproven, never swapped for a similar one.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; 3 of my 27 items are unclear in photos, 2 in none. Skills cannot be scheduled; updates are user-started. Instruction length is untested on hardware; long lists go in parts.

## Third-party components

None in the package: it is Markdown only. It was built and checked with the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, supplied by UGREEN, used under its terms). The Skill calls no external service. Every reading instruction asks for the NAS local model and skips files it cannot handle; if the owner has set the assistant to an online model, the Skill cannot override that. Principal functionality developed for the Hackathon: all of it.

AI tools: at run time, the Skill asks for the NAS local model only. During development, an AI coding assistant helped draft and revise the package and played the NAS in dry runs; the idea, the claim data, the test design and the decisions are mine. The drawings above were made with an image model run on my own computer (Z-Image Turbo by Tongyi-MAI, Apache 2.0, through ComfyUI, GPL-3.0) and stand in for my photos. The linked practice run uses a made-up library. Full disclosure: `references/disclosures.md` in the package.

Source of the quotation in answer 2: Selina Clark, former insurance adjuster, The New York Times, February 6, 2025.

## Entrant

Jonathan Andrei, individual entrant.

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1. Track: Open Innovation.

Electronic signature: Jonathan Andrei, November 11, 2026
