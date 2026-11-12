# Recall on my real library, with a local stand-in for the NAS

Run 2026-11-12 with `tools/recall_standin.py`. A small vision model running on my own computer (qwen3.5:4b, about four billion parameters, through Ollama) played two parts of the NAS: it tagged each of the 1,749 photos captured before the loss with object categories, as the NAS recognition index would, and it answered the Skill's own question for each candidate photo. The Skill's routes and caps were applied as written: one search per category, the eight latest photos before the loss plus the earliest, then a second look at the photos already returned for the items still unproven. Nothing left the computer.

How the model was chosen: a first run with gemma3:4b named items in photos that do not show them (a bed frame in a photo of trading cards, a console table in a photo of a fence), so before a second run three local models of the same size were asked the Skill's question about three photos whose contents the hand count records. gemma3:4b named an item that was not there, gemma4:e4b missed one, and qwen3.5:4b answered all three correctly; it is the model used here. The first run is not scored.

## Result

**First pass: the stand-in proved 11 of the 22 items my hand count found in a pre-loss photo**, each with a photo that shows the item. 4 of the 22 are entries the Skill never searches (boxes, bags, bedding, stored items), because it asks the owner to itemize them, so the most it could prove is 18. It also found a clearer photo of the stick vacuum, an item the hand count had rated only likely.

**Continuing: 13 of 22.** When more photos match than were described, the Skill offers to go on. With the owner turning down the wrong photos and asking to continue up to 4 times per item, the search reached older photos of the storage room and proved the bed frame and the bookshelf from them.

Photos it cited, every one checked against the hand count or opened and looked at: 32 show the item, 81 do not, 14 cannot settle it. Nothing was left unchecked. A wrong photo never reaches the claim on its own: every row and its photo are shown to the owner to confirm first, and this many wrong photos is why that step exists. On the first pass it cited no photo for the camera rig or the iron, the two items the hand count found in no photo; continuing, it cited two screenshots for the camera rig.

## Why it missed what it missed

- **The cap, not the recognition.** The index tagged the December walk-through correctly (bed, bookcase, table, lamp), but 40 photos are tagged bed and 133 lamp, and the eight latest of each are from 2026. The first pass never reached December 2025. Continuing reached the bed frame and the bookshelf; the coffee table, the road case and the floor lamps were still further back.
- **An item counted as found too early.** The hex side table was in a photo the search returned, but a wrong photo had already been cited for it, so the second look never asked about it. The owner would turn that photo down, and the Skill would look again.
- **No word for it.** The boot dryer has no category and the stand-in has no keyword search, so only the second look could reach it, and its one photo was never returned.

For the testing day, this says what to watch: how many photos the NAS index returns per category, and whether the eight-latest cap needs to grow when an item stays unproven.

This measures the Skill's search and description steps with a small model standing in for the NAS; the NAS's own recognition index will tag photos differently, and the receipt routes were not run.

## Item by item

A cited photo counts when the hand count lists it for that item, or when I opened it and saw the item ([recall-standin-checks.csv](recall-standin-checks.csv)).

| # | Item | Hand count | Route | First pass | Continuing | Photos that show it | Wrong photos cited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Leather reclining sofa, 3-seat (brown) | yes | sofa | yes | yes | 20260617_063548.jpg | 4 |
| 2 | Flat-screen TV, about 55 inch | yes | television | yes | yes | 20260617_064156.jpg | 2 |
| 3 | Gaming chair | yes | office or gaming chair | yes | yes | 20260617_063617.jpg, 20260617_063755.jpg, 20260617_063759.jpg | 1 |
| 4 | Wooden armchair | yes | armchair | yes | yes | 20260617_064152.jpg, 20260617_064156.jpg | 2 |
| 5 | Wooden bed frame (oak headboard and footboard) | yes | bed | no | yes | 20260218_085604.jpg, 20260222_155733.jpg | 2 |
| 6 | Wooden console and side tables | yes | table | yes | yes | 20260617_063759.jpg, 20260617_064151.jpg, 20260617_064156.jpg | 1 |
| 7 | Coffee or accent table | yes | table | no | no |   | 3 |
| 8 | Wooden side table (hex) | yes | table | no | no |   | 7 |
| 9 | Pull-up and dip bar (power tower) | yes | exercise equipment | yes | yes | 20260222_155737.jpg, 20260222_155740.jpg, 20260222_155743.jpg, 20260617_063812.jpg | 1 |
| 10 | Adjustable dumbbell set | yes | dumbbell | yes | yes | 20240807_132511.jpg, 20260222_155735.jpg, 20260222_155740.jpg, 20260605_201640.jpg, 20260608_212738.jpg, 20260617_063812.jpg |   |
| 11 | Stored items on shelving (tools, fan, books, household) | yes | owner to itemize | no | no |   |   |
| 12 | Bookshelf (wood) | yes | bookcase | no | yes | 20260218_085604.jpg, 20260222_155733.jpg | 7 |
| 13 | Storage shelving units | yes | shelving unit | yes | yes | 20260617_063812.jpg | 7 |
| 14 | Stick vacuum (Dyson) | likely | vacuum cleaner | yes | yes | 20240805_161215.jpg |   |
| 15 | Flight or AV road case | yes | case or trunk | no | no |   | 7 |
| 16 | Camera rig (shoulder rig, matte box, follow focus) | no | camera | no | no |   | 2 |
| 17 | Metal or chrome shelving unit | yes | shelving unit | yes | yes | 20260617_064159.jpg | 5 |
| 18 | Floor lamps | yes | lamp | no | no |   | 7 |
| 19 | Mini-fridge (Danby) | yes | refrigerator | yes | yes | 20260222_155819.jpg, 20260617_193210.jpg | 4 |
| 20 | Washer and dryer (Amana) | yes | washing machine | yes | yes | 20240810_082300.jpg, 20260506_092504.jpg, 20260617_063925.jpg | 1 |
| 21 | Bedding and blankets (bagged) | yes | owner to itemize | no | no |   |   |
| 22 | Boxes of personal belongings (misc.) | yes | owner to itemize | no | no |   |   |
| 23 | Bagged contents, several bags (clothing, handbags, household) | yes | owner to itemize | no | no |   |   |
| 24 | Boot dryer | yes | keyword | no | no |   |   |
| 25 | Clothes iron or garment steamer | no | clothes iron | no | no |   |   |
| 26 | Monitor desk arm or mount | plausible | computer monitor | no | no |   | 10 |
| 27 | Picture and diploma frames | plausible | picture frame | no | no |   | 8 |
