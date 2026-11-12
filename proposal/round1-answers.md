# Already Owned

[![QR code](../docs/qr.png)](https://jonathansolvesproblems.github.io/already-owned/) Try a practice claim, no NAS needed: https://jonathansolvesproblems.github.io/already-owned/

The PDF of this proposal is [already-owned-round1.pdf](already-owned-round1.pdf).

## 1. One sentence: What does the Skill do?

You walk the damaged room recording a voice note; the Skill finds each thing you name, and the belongings you forgot, in NAS photos taken before the loss, and writes the insurer's contents claim with that proof.

## 2. Who is the target user and problem?

Homeowners and renters. Water damaged my home twice in seven months; the insurer wanted proof of every item. My June claim: 27 items, $10,915 CAD, every photo taken after the water. Yet 22 already sat in my photos from before: shots for a contractor, the first claim, everyday life.

## 3. What is your proposed solution?

![A sample contents claim](../preview/05-claim-folder.png)

From a voice note or typed list, it writes the insurer's contents table: per item, a pre-loss photo and capture date, any receipt price, and a proof level or "no proof". You confirm every row. An optional weekly update keeps a dated ledger.

## 4. What is the Core User Flow?

"Flood, June 20, 2 am, basement" → I record a voice note walking the room → it finds each item in photos before 2 am, asks about things I never named → I confirm once → I approve each write.

## 5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?

44% of U.S. residents never made a home inventory (Farmers Insurance), so a claim starts from memory. A photo app finds a sofa, not a claim. Here you walk the room talking; it applies the cut-off, pairs receipts and asks about belongings the photos show you never named.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?

- Hear: knowledge-agent (ug-knowledge) transcribes the voice note.
- Find: photo-agent (ug-photo) searches recognized objects, keywords, text in photos and capture dates; local vision describes each hit.
- Price: document-agent (ug-document) reads receipt lines.
- Save: file-agent (ug-filesystem, ug-filemgr, file-workflow) copies, hashes, tags and reads back; knowledge-agent saves the list; photo-agent makes the album.
- Theft: security-monitor-agent (ug-surveillance) lists camera events.

## 7. What was your technical approach? Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable.

You give the loss date, time, rooms and a voice note or list. The Skill only delegates: 25 instruction templates, five experts. Each item is searched by recognized object, keyword or receipt text, then found photos are described again; two empty searches mean "no proof". Every write waits for approval and is read back. Experts are asked for the local model.

## 8. What is the current development status?

Implemented: package, checker static-pass. Recall, a local 4B vision model standing in for the NAS on my 1,749 pre-loss photos: the Skill proved 13 of the 22 hand-counted items ($6,945 of $10,915), 15 when continued, plus one my hand count missed. Rehearsal: a small model drove a scripted NAS: 140 of 140 checks. Pending: the NAS index.

## 9. What is your final validation plan?

- Core 1: replay my June 2026 claim on pre-loss photos. Pass: every cited photo predates the loss; at least 15 of the 22 hand-counted items proven.
- Core 2: weekly update on a month of photos. Pass: page, album and tag exist; a rerun writes nothing.
- Edge: an item in no pre-loss photo. Pass: reported unproven, never swapped.

## 10. Are there any known limitations of your Project?

Recall depends on the NAS index: the stand-in never tagged 2 of the missed items; 4 more are boxes you itemize. A photo proves ownership, not price. Copies may need one approval each, so large claims hash exhibits in place.

## Third-party components

None in the package: it is Markdown only. It was built and checked with the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, supplied by UGREEN, used under its terms). External services: none. Data flows: photos, receipts and voice notes are read on the NAS by its experts, which are asked for the local model; what they return is read by the assistant's own model, and since the Skill cannot override an owner's choice of an online one, it says so before the first read. Principal functionality developed for the Hackathon: all of it. Fonts in this PDF and its images: Besley, Hanken Grotesk, Shantell Sans and Red Hat Mono (SIL Open Font License); arrows and code use Windows system fonts.

AI tools: at run time, the Skill asks for the NAS local model only. During development, an AI coding assistant helped draft and revise the package, played the NAS in paper dry runs and made the first pass of the eye checks of the photos the recall measurement cited, and a smaller model played the NAS assistant in the scripted rehearsal; the recall measurement ran Qwen3.5 4B (Alibaba Qwen team, Apache 2.0) on my own computer through Ollama (MIT), standing in for the NAS; the idea, the claim data, the test design and the decisions are mine, and I reviewed every line. The drawings above were made with an image model run on my own computer (Z-Image Turbo by Tongyi-MAI, Apache 2.0, through ComfyUI, GPL-3.0) and stand in for my photos. The linked practice run uses a made-up library. Full disclosure: `references/disclosures.md` in the package.

## Entrant

Jonathan Andrei, individual entrant.

Skill package: `home-contents-inventory`. UGREEN Hackathon 2026 on AI NAS, Round 1. Track: Open Innovation.

Electronic signature: Jonathan Andrei, November 12, 2026
