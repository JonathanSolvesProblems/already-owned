# Disclosures, version and lifecycle

## Version

- Skill `home-contents-inventory`, version 0.1.0, the Round 1 pre-test package of the UGREEN Hackathon 2026 on AI NAS.
- Written against the UGOS Skill Creation Tool `uliya-skill-kit` 0.7.3 and its capability catalog 2.0.0. Every capability the Skill asks an expert for is an action in that catalog.
- The inventory is a ledger of dated pages. Each run adds a page with what changed and rewrites none, so every earlier state of the inventory stays readable.

## Principal functionality developed for this Hackathon

All of it. The Skill, its three modes (update, ask, claim), the search-route rules, the contents list format and the user guide were written during the Hackathon. The idea comes from two contents claims of my own; no earlier Skill, code or submission material is reused.

## Third-party components and open source libraries

None are in the package. It is Markdown only: no script, executable, library, model weight or dataset.

The one tool it was built with is the official UGOS Skill Creation Tool (`uliya-skill-kit`, supplied by UGREEN for the Hackathon and used under its terms). Its checker reports static-pass with no errors and no warnings for this package.

## External services, credentials and data flows

- No external service is called and no data leaves the NAS. Every instruction that reads a photo, a document or a recording tells the expert to use only the NAS local model and to return what it cannot handle as not processed; the Skill then pauses and asks the user before any other model is used.
- The Skill needs no account, key, token or password, and stores none.
- It reads only the photos, documents and, in claim mode, the camera events of the current user.
- It writes only what the user approves, one approval per write: one folder (Home Contents, with a Claims folder inside it and one folder per loss inside that), dated Markdown lists and claim documents in those folders, copies of the cited photos and receipts inside the folder of each loss, dated albums, and one file tag (home-contents).

## AI tools used and their principal uses

- At run time: the NAS local model only, through the registered experts (photo recognition and description, text recognition, receipt extraction, drafting, translation, transcription). No third-party model.
- During development: an AI coding assistant helped draft and revise the Markdown of this package, ran the kit checker, and played the NAS in dry runs of the workflow against a mock library to find defects. The idea, the claim data, the test design, the review of every line and the decisions are mine.
- Outside the package: the drawings on the project's proposal and replay page were made with an image model run on my own computer (Z-Image Turbo, Apache 2.0). They stand in for my own photos. No image is in this package.

## Install, set up, test, remove

- **Install**: add the package to the NAS the way UGOS installs any Skill package. It is one folder with SKILL.md and seven references; there is nothing to compile or configure, and it depends on nothing outside the NAS.
- **Set up**: none. The first update run asks how far back to look and creates the Home Contents folder after approval.
- **Test**: the cases, the data they need and the expected results are in the test plan reference. In short, three requests cover the modes. "Update my home inventory" must end with a dated list, a dated album and tagged files. "What do I own in the basement" must answer from the saved list without searching. "I had a flood on a given date in the basement, list what I lost" must return only photos captured before that date as proof, and report an item with no such photo as unproven.
- **Remove**: uninstall the Skill. It leaves no background task, setting or credential. What it created stays, because it belongs to the user: the Home Contents folder with its lists, claim documents and exhibit copies, the dated albums and the home-contents tag. Each can be deleted by hand in Files and Photos; the Skill itself never deletes anything.
