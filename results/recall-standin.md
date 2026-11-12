# Recall on my real library, with a local stand-in for the NAS

Run 2026-11-12 with `tools/recall_standin.py`. A small vision model running on my own computer (qwen3.5:4b, about four billion parameters, through Ollama) played two parts of the NAS: it tagged each of the 1,749 photos captured before the loss that are stored on the computer with object categories, as the NAS recognition index would, and it answered the Skill's own question for each candidate photo. The library holds 1,769 photos from before the loss; the other 20 are kept only in the cloud and could not be read. Nothing left the computer.

What I chose and what the Skill chose: I set the stand-in index's 25 categories, and the category each line of my claim is searched under, before the run, following the Skill's search-routes reference. The NAS index has its own category list, so its routes can differ. Everything after that follows the Skill as written: one search per category, capped, then a second look at the photos already returned, for the items still unproven.

How the model was chosen: a first run with gemma3:4b named items in photos that do not show them (a bed frame in a photo of trading cards, a console table in a photo of a fence), so before a second run three local models of the same size were asked the Skill's question about three photos whose contents the hand count records. gemma3:4b named an item that was not there, gemma4:e4b missed one, and qwen3.5:4b answered all three correctly; it is the model used here. The gemma3:4b run is not scored.

## Result

**Skill 0.2.0, nine photos spread across the capture dates: the stand-in proved 13 of the 22 items my hand count found in a pre-loss photo on the first pass, worth $6,945 of the $10,915 CAD claimed, and 15 ($7,295) when the owner asks it to continue.** 4 of the 22 are entries the Skill never searches (boxes, bags, bedding, stored items), because it asks the owner to itemize them, so the most it could prove is 18. The first pass cost 310 model reads over 148 photos; continuing, 427 over 253. Beyond the hand count it also proved the stick vacuum (rated only likely), the camera rig (which the hand count found in no photo) and the monitor arm (rated plausible), each with a photo checked by eye.

**Skill 0.1.0, the eight latest matches plus the earliest: 11 on the first pass, 13 continuing.** That was the rule of the first run of this measurement. Its misses showed that the eight latest matches of a busy category all came from 2026 and never reached the older photos that held the proof, so the claim search was changed to spread its nine photos across the capture dates. The change came after that run; both results are kept here and scored the same way. On the first pass the change proved the bed frame, the coffee table, the bookshelf and the floor lamps, and lost the storage shelving and the chrome shelving. The first pass also cited 38 wrong photos instead of 55, and continuing cost 427 model reads instead of 522.

Photos it cited (0.2.0, continuing), every one checked against the hand count or opened and looked at: 39 show the item, 61 do not, 13 cannot settle it. Nothing was left unchecked. A wrong photo never reaches the claim on its own: every row and its photo are shown to the owner to confirm first, and this many wrong photos is why that step exists.

## Why it missed what it missed

Worked out from the run itself (0.2.0, continuing), for each item the hand count found and the Skill searches:

- **Recognition.** The stand-in index never tagged the photos that show the hex side table and the road case with the category searched, so no search could return them.
- **No word for it.** No category names the boot dryer, and the stand-in has no keyword search, so only the second look could reach it.

For the testing day, this says what to watch: how many photos the NAS index returns per category, and how its categories cover a household's things.

This measures the Skill's search and description steps with a small model standing in for the NAS; the NAS's own recognition index will tag photos differently, and the receipt routes were not run.

## Item by item

A cited photo counts when the hand count lists it for that item, or when the photo, opened at full size and compared with the hand count's description of the item, shows it. Each verdict (yes, no or unclear) is in [recall-standin-checks.csv](recall-standin-checks.csv), which also keeps the verdicts on photos cited by earlier runs; the AI assistant that helped build this project made the first pass of these checks, and the list is mine to correct.

| # | Item | Hand count | Route | 0.1.0 first pass | 0.1.0 continuing | 0.2.0 first pass | 0.2.0 continuing | Photos that show it (0.2.0) | Wrong photos cited |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Leather reclining sofa, 3-seat (brown) | yes | sofa | yes | yes | yes | yes | 20241006_165733.jpg, 20260218_085804.jpg | 1 |
| 2 | Flat-screen TV, about 55 inch | yes | television | yes | yes | yes | yes | 20240806_131646.jpg, 20251223_120538.jpg, 20260617_064156.jpg |   |
| 3 | Gaming chair | yes | office or gaming chair | yes | yes | yes | yes | 20260218_085807.jpg | 3 |
| 4 | Wooden armchair | yes | armchair | yes | yes | yes | yes | 20251211_160058.jpg, 20260617_064156.jpg | 3 |
| 5 | Wooden bed frame (oak headboard and footboard) | yes | bed | no | yes | yes | yes | 20251211_160200.jpg, 20260218_085604.jpg |   |
| 6 | Wooden console and side tables | yes | table | yes | yes | yes | yes | 20251211_160058.jpg, 20260222_155812.jpg, 20260617_064156.jpg |   |
| 7 | Coffee or accent table | yes | table | no | no | yes | yes | 20251211_160058.jpg | 2 |
| 8 | Wooden side table (hex) | yes | table | no | no | no | no |   | 6 |
| 9 | Pull-up and dip bar (power tower) | yes | exercise equipment | yes | yes | yes | yes | 20260218_085601.jpg, 20260222_155733.jpg, 20260222_155737.jpg, 20260617_063812.jpg | 1 |
| 10 | Adjustable dumbbell set | yes | dumbbell | yes | yes | yes | yes | 20240807_132511.jpg, 20260222_155740.jpg, 20260605_201640.jpg, 20260617_063812.jpg |   |
| 11 | Stored items on shelving (tools, fan, books, household) | yes | owner to itemize | no | no | no | no |   |   |
| 12 | Bookshelf (wood) | yes | bookcase | no | yes | yes | yes | 20251211_160200.jpg | 4 |
| 13 | Storage shelving units | yes | shelving unit | yes | yes | no | yes | 20241024_153611.jpg | 14 |
| 14 | Stick vacuum (Dyson) | likely | vacuum cleaner | yes | yes | yes | yes | 20240805_161215.jpg, 20241217_185953.jpg, 20251019_152148(0).jpg |   |
| 15 | Flight or AV road case | yes | case or trunk | no | no | no | no |   | 3 |
| 16 | Camera rig (shoulder rig, matte box, follow focus) | no | camera | no | no | yes | yes | 20240810_082331.jpg | 2 |
| 17 | Metal or chrome shelving unit | yes | shelving unit | yes | yes | no | yes | 20260113_131255.jpg | 11 |
| 18 | Floor lamps | yes | lamp | no | no | yes | yes | 20260113_131012.jpg | 1 |
| 19 | Mini-fridge (Danby) | yes | refrigerator | yes | yes | yes | yes | 20250114_080145.jpg, 20260222_155819.jpg, 20260617_193210.jpg | 1 |
| 20 | Washer and dryer (Amana) | yes | washing machine | yes | yes | yes | yes | 20240810_082300.jpg, 20260222_155753.jpg, 20260309_115512.jpg, 20260310_131524.jpg, 20260617_063925.jpg |   |
| 21 | Bedding and blankets (bagged) | yes | owner to itemize | no | no | no | no |   |   |
| 22 | Boxes of personal belongings (misc.) | yes | owner to itemize | no | no | no | no |   |   |
| 23 | Bagged contents, several bags (clothing, handbags, household) | yes | owner to itemize | no | no | no | no |   |   |
| 24 | Boot dryer | yes | keyword | no | no | no | no |   |   |
| 25 | Clothes iron or garment steamer | no | clothes iron | no | no | no | no |   |   |
| 26 | Monitor desk arm or mount | plausible | computer monitor | no | no | yes | yes | 20240815_090704.jpg | 3 |
| 27 | Picture and diploma frames | plausible | picture frame | no | no | no | no |   | 6 |
