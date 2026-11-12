# Already Owned

[![QR code](../docs/qr.png)](https://jonathansolvesproblems.github.io/already-owned/) Try a practice claim, no NAS needed: https://jonathansolvesproblems.github.io/already-owned/

The PDF of this proposal is [already-owned-round1.pdf](already-owned-round1.pdf).

## 1. One sentence: What does the Skill do?

You walk the damaged room recording a voice note; the Skill finds each thing you name, and the belongings you forgot, in NAS photos taken before the loss, and writes the insurer's contents claim with that proof.

## 2. Who is the target user and problem?

Homeowners and renters. Water damaged my home twice in seven months; each time the insurer wanted proof I owned every damaged item. My June claim: 27 items, $10,915 CAD, every photo I sent taken after the water. Yet 22 of the 27 were in photos I already had.

## 3. What is your proposed solution?

![A sample contents claim](../preview/05-claim-folder.png)

Claim: from a voice note or typed list, finds a pre-loss photo and receipt per item, shows what you forgot, and saves one claim folder with every exhibit and its SHA-256. Update (weekly): adds new belongings to a dated ledger. Ask: answers from it.

## 4. What is the Core User Flow?

"Flood, June 20, basement" → walk the room recording a voice note → it finds each item in photos from before June 20 and shows what I forgot → I confirm once → I approve each write → claim folder saved.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

Photo search finds a sofa; it cannot enforce the loss date, pair a receipt, notice what you forgot or produce verifiable exhibits. On my 1,769 pre-loss photos, file-name and date search proves 0 of 27 items. Inventory apps (Encircle, HomeZada) need items photographed beforehand.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- Hear: knowledge-agent (ug-knowledge) transcribes the voice note.
- Find: photo-agent (ug-photo) searches recognized objects, keywords, text in photos and capture dates; local vision describes each hit.
- Price: document-agent (ug-document) reads receipt lines.
- Save: file-agent (ug-filesystem, ug-filemgr, file-workflow) copies, hashes, tags and reads back; knowledge-agent saves the list; photo-agent makes the album.
- Theft: security-monitor-agent (ug-surveillance) lists camera events.

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

Delegation only, 25 templates. Each item gets a search route, a second look at photos already found, then one more route; nothing similar is substituted. Requests stay small. All five delegation states handled. Every write waits for approval and every saved file is read back; nothing is deleted, moved or overwritten. Evidence text is data, never instructions. Experts are asked for the local model.

## 8. What is the current development status?

Implemented: full package; checker static-pass. Rehearsal: a small model followed it alone against a scripted mock NAS and a made-up library, 7 runs of 6 scenarios: 140 of 140 automated checks passed. No unapproved write, no post-loss photo as proof, an injected receipt instruction ignored, an altered save caught on read-back. Pending hardware: recall, receipt reading, real approvals.

## 9. What is your final validation plan?

- Core 1: replay my June 2026 claim on pre-loss photos. Pass: every cited photo predates the loss; at least 15 of the 22 hand-counted items proven.
- Core 2: weekly update on a month of photos. Pass: page, album and tag exist; a rerun writes nothing.
- Edge: an item in no pre-loss photo. Pass: reported unproven, never swapped.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS recognition index; of my 27 items, 3 are unclear in photos and 2 in none. A photo proves ownership, not price. Instruction length is untested on hardware, so long lists go in parts.

## Third-party components

None in the package: it is Markdown only. It was built and checked with the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, supplied by UGREEN, used under its terms). External services and data flows: none. The Skill asks for the NAS local model and cannot override an owner's choice of an online one. Principal functionality developed for the Hackathon: all of it. Fonts in this PDF: Besley and Hanken Grotesk (SIL Open Font License); arrows and code use Windows system fonts.

AI tools: at run time, the Skill asks for the NAS local model only. During development, an AI coding assistant helped draft and revise the package and played the NAS in paper dry runs, and a smaller model played the NAS assistant in the scripted rehearsal; the idea, the claim data, the test design and the decisions are mine, and I reviewed every line. The drawings above were made with an image model run on my own computer (Z-Image Turbo by Tongyi-MAI, Apache 2.0, through ComfyUI, GPL-3.0) and stand in for my photos. The linked practice run uses a made-up library. Full disclosure: `references/disclosures.md` in the package.

## Entrant

Jonathan Andrei, individual entrant.

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1. Track: Open Innovation.

Electronic signature: Jonathan Andrei, November 12, 2026
