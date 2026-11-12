# Disclosures, version and lifecycle

## Version

- Skill `home-contents-inventory`, version 0.2.0, the Round 1 pre-test package of the UGREEN Hackathon 2026 on AI NAS.
- 0.2.0, 12 November 2026: every saved page and claim document is read back and compared; unanswered questions decide nothing and are listed; a receipt price keeps its number when no currency is printed; names are written out in every template; the model notice is a step; an instruction carries at most ten rows and exhibit lines, and a claim part at most six rows; no request asks an expert for more than about ten model reads; a keyword route for things the recognition index has no category for; one question before many copy approvals; the date comes from the NAS. 0.1.0, 11 November 2026: first complete package.
- Written against the UGOS Skill Creation Tool `uliya-skill-kit` 0.7.3 and its capability catalog 2.0.0. Every capability the Skill asks an expert for is an action in that catalog.
- The inventory is a ledger of dated pages. Each run adds a page with what changed and rewrites none, so every earlier state of the inventory stays readable.

## Principal functionality developed for this Hackathon

All of it. The Skill, its three modes (update, ask, claim), the search-route rules, the contents list format and the user guide were written during the Hackathon. The idea comes from two contents claims of my own; no earlier Skill, code or submission material is reused.

## Third-party components and open source libraries

None are in the package. It is Markdown only: no script, executable, library, model weight or dataset.

The one tool the package depends on is the official UGOS Skill Creation Tool (`uliya-skill-kit` 0.7.3, the version in the name of the download UGREEN supplies for the Hackathon, used under its terms). Its checker reports static-pass with no errors and no warnings for this package.

## External services, credentials and data flows

- The Skill calls no external service. Every instruction that reads a photo, a document or a recording asks for the NAS local model and tells the expert to return what it cannot handle as not processed; such files are left out and listed in the report. The Skill never asks for another model. What the experts return is read by the assistant's own model. If the owner has set the assistant to an online model, that text passes through it; the Skill cannot override that choice, so it tells the user before the first read.
- The Skill needs no account, key, token or password, and stores none.
- It reads only the photos, documents and voice notes of the current user and, in claim mode for a theft or when the user agrees, the user's own camera events.
- It writes only what the user approves, and every write delegation asks for approval first: one folder (Home Contents, with a Claims folder inside it and one folder per loss inside that), dated Markdown lists and claim documents in those folders, copies of the cited photos, receipts and voice note inside the folder of each loss, dated albums, and one file tag (home-contents).

## AI tools used and their principal uses

- At run time: the Skill asks for the NAS local model only, through the registered experts (photo recognition and description, text recognition, receipt extraction, drafting, translation, transcription). It names no third-party model and calls none.
- During development: an AI coding assistant helped draft and revise the Markdown of this package, ran the kit checker, and played the NAS in dry runs of the workflow against a mock library to find defects. A smaller model played the NAS assistant in the scripted rehearsal, following this package against a mock NAS and a made-up library; the runs and their checks are published with the project. The idea, the claim data, the test design, the review of every line and the decisions are mine.
- Outside the package: the recall measurement on my own photos used Qwen3.5 (4B, by the Qwen team at Alibaba, Apache 2.0), run on my own computer through Ollama (MIT licence), standing in for the NAS recognition index and vision expert; Gemma 3 and Gemma 4 (4B, by Google, Gemma Terms of Use) were tried while choosing it. No photo left the computer.
- Outside the package: the drawings on the project's proposal and replay page were made with an image model run on my own computer (Z-Image Turbo by Tongyi-MAI, Apache 2.0, through ComfyUI, GPL-3.0). They stand in for my own photos. No image is in this package.

## Install, set up, test, remove

- **Install**: add the package to the NAS the way UGOS installs any Skill package. It is one folder with SKILL.md and seven references; there is nothing to compile or configure, and it depends on nothing outside the NAS.
- **Set up**: nothing to configure in the Skill. Two things on the NAS must be ready, or the searches return nothing: the Photos app must have finished recognizing the library (objects and text), and the phone's photos must be backed up to the NAS. The first update run asks how far back to look and creates the Home Contents folder after approval. A voice walk-through is recorded on the phone and saved to the user's space with the UGREEN app; photo backup does not carry recordings on every phone, so the Skill looks for the recording and asks which one it is.
- **Test**: the cases, the data they need and the expected results are in the test plan reference. In short, three requests cover the modes. "Update my home inventory" must end with a dated list, a dated album and tagged files. "What do I own in the basement" must answer from the saved list without searching. "I had a flood on a given date in the basement, list what I lost" must return only photos captured before that date as proof, and report an item with no such photo as unproven.
- **Remove**: uninstall the Skill. It leaves no background task, setting or credential. What it created stays, because it belongs to the user: the Home Contents folder with its lists, claim documents and exhibit copies, the dated albums and the home-contents tag. Each can be deleted by hand in Files and Photos; the Skill itself never deletes anything.
