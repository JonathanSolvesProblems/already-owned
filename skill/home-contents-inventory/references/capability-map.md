# Capability map

Every step of the Skill, the registered expert it delegates to, and the actions of catalog 2.0.0 that stand behind it. The Skill never names an action in an instruction and never calls a CLI: it describes the task, and the expert chooses the action. This map exists so a reviewer can check that nothing is asked of the platform that it does not offer.

Effect and approval are the catalog's own values. Read steps need no approval. Every write below is requested with the words "request user approval first" in its instruction.

| Step | Expert | Catalog actions behind the step | Effect | Approval |
| --- | --- | --- | --- | --- |
| U1, A1, C3 read the ledger | `file-agent` | `file-workflow` get-user-dir, `ug-filesystem` find, ls, cat | read | none |
| U2, C3 category names | `photo-agent` | `ug-photo` object-albums, search-classify, search-picture | read | none |
| U3 photos per category, and C3 when no inventory exists | `photo-agent` | `ug-photo` search-picture by recognized object, by text in the photo, by capture time, vision-vlm, meta | read | none |
| U4, C6 receipt files | `file-agent` | `file-workflow` get-user-dir, `ug-filesystem` find by type and date; in C6 also `ug-filemgr` tag-get-by-name and tag-list-file, to try tagged receipts first | read | none |
| U5, C6 photographed receipts | `photo-agent` | `ug-photo` search-picture by text in the photo, vision-ocr | read | none |
| U6, C6 purchase lines | `document-agent` | `ug-document` extract with the receipt and invoice schemas | read | none |
| U6 fallback for an image | `photo-agent` | `ug-photo` vision-ocr | read | none |
| U9 folder | `file-agent` | `ug-filesystem` mkdir | state change | gateway |
| U10 dated album | `photo-agent` | `ug-photo` create-album | state change | workflow |
| U11 tag | `file-agent` | `ug-filemgr` tag-get-by-name, tag-add, tag-add-file | state change | gateway, conditional |
| U12 ledger page | `knowledge-agent` | `ug-knowledge` save-text | state change | workflow |
| C2 find and transcribe a recording | `file-agent`, `knowledge-agent` | `file-workflow` get-user-dir, `ug-filesystem` find by type and date, `ug-knowledge` audio-transcription | read | none |
| C4a damage photos | `photo-agent` | `ug-photo` search-picture by capture time, vision-vlm, meta | read | none |
| C4b pre-loss proof | `photo-agent` | `ug-photo` search-picture by file name, recognized object, text in the photo, capture time, vision-vlm, meta | read | none |
| C4b second pass | `photo-agent` | `ug-photo` vision-vlm and meta on paths already returned | read | none |
| U6b, C6 receipt-first photo search | `photo-agent` | `ug-photo` search-picture by text in the photo and by capture time, vision-vlm, meta | read | none |
| C5 camera events | `security-monitor-agent` | `ug-surveillance` cameras, event-timeline, event-evidence with snapshots for user review | read | none |
| C8 opening draft, translated copy | `document-agent` | `ug-document` writing, translate | mixed | gateway |
| C9 claim folder | `file-agent` | `ug-filesystem` mkdir | state change | gateway |
| C9 exhibit copies, the voice note included | `file-agent` | `ug-filesystem` cpmv as a copy, then sha256sum on each original and each copy | state change, then read | gateway |
| C9 hashes when copies are declined | `file-agent` | `ug-filesystem` sha256sum | read | none |
| C9 claim document | `knowledge-agent` | `ug-knowledge` save-text | state change | workflow |
| C9 claim album | `photo-agent` | `ug-photo` create-album | state change | workflow |

Seven of the nine published CLIs are used, through five of the registered experts. The two not used are the music and video players, which have nothing to say about what a household owns.

## Actions the Skill deliberately never asks for

| Catalog action | Why it is never used |
| --- | --- |
| `ug-filesystem` del, rename, chtimes, restore, and cpmv as a move | The Skill deletes, renames, re-dates and moves nothing. Changing a file time would damage the very evidence it collects. |
| `ug-filesystem` echo in overwrite or patch mode | No existing file is rewritten. A ledger page is always a new file. |
| `file-workflow` run, batch-del, batch-move | No bulk reorganising of the user's files. |
| `ug-filemgr` tag-delete, tag-delete-file | Tags are only added. |
| `ug-surveillance` identity-resolve, faces, vehicle-plates | The Skill reports unknown people as unknown and never tries to identify anyone. |

## What the catalog does not support, and what the Skill does instead

| Wanted | Catalog 2.0.0 | What the Skill does |
| --- | --- | --- |
| Add a photo to an existing album | create-album only | One dated album per run, and one file tag that links every inventory photo across runs |
| Run on a schedule | no scheduler | The weekly update is started by the user |
| Choose or confirm the model for every expert | no action covers every expert | Every reading instruction says to use only the local model and to return what it cannot handle as not processed; those files are left out and listed, and no other model is asked |
| Read purchase lines from a photographed receipt | extract takes document files | The recognized text of the photo is read instead, and the row is marked "receipt read from photo text" |
| Read a price off the market | none, and out of scope | Values come from a receipt or from the user, never from a model |
