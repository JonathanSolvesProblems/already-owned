# Ablation: the same items searched by file name and date only

Run 2026-11-02 with `tools/ablation_filename.py` over 210 photos captured before 2026-06-20 00:00 (the June 20, 2026 loss), on the pre-loss photos reachable from this PC. To be re-run on the NAS testing day with `ug-filesystem find` over the full library, which is what a NAS without the AI index offers.

Method: for each of the 27 claim items, a case-insensitive search of its keywords in the photo file names, and separately in the folder names, with no recognition index, no OCR and no vision model. A hit means at least one pre-loss file name or folder name contains a keyword.

**Result: 6 of 27 items found by file name or folder name.**

| # | Item | Keywords | Hits by file name | Hits by folder name | Found |
| --- | --- | --- | --- | --- | --- |
| 1 | Leather reclining sofa, 3-seat (brown) | sofa, couch, recliner | 10 2025-12-08 Wall by the couch.jpg | 0 | yes |
| 2 | Flat-screen TV, about 55 inch | tv, television, screen | 0 | 0 | no |
| 3 | Gaming chair | chair, gaming | 0 | 0 | no |
| 4 | Wooden armchair | armchair, chair | 0 | 0 | no |
| 5 | Wooden bed frame (oak headboard and footboard) | bed, headboard | 0 | 0 | no |
| 6 | Wooden console and side tables | console, side table, table | 01 2025-12-04 14-22 Dining area under the opened ceiling, blanket on floor, hutch, table and chairs.jpg | 0 | yes |
| 7 | Coffee or accent table | coffee table, table | 01 2025-12-04 14-22 Dining area under the opened ceiling, blanket on floor, hutch, table and chairs.jpg | 0 | yes |
| 8 | Wooden side table (hex) | hex, side table, table | 01 2025-12-04 14-22 Dining area under the opened ceiling, blanket on floor, hutch, table and chairs.jpg | 0 | yes |
| 9 | Pull-up and dip bar (power tower) | power tower, pull-up, pullup, dip | 0 | 0 | no |
| 10 | Adjustable dumbbell set | dumbbell, weights, gym | 0 | 0 | no |
| 11 | Stored items on shelving (tools, fan, books, household) | shelving, shelf, storage, tools, fan | 0 | 0 | no |
| 12 | Bookshelf (wood) | bookshelf, bookcase, shelf | 0 | 0 | no |
| 13 | Storage shelving units | shelving, shelf, storage | 0 | 0 | no |
| 14 | Stick vacuum (Dyson) | dyson, vacuum | 0 | 0 | no |
| 15 | Flight or AV road case | flight case, road case, case | 0 | 0 | no |
| 16 | Camera rig (shoulder rig, matte box, follow focus) | rig, matte box, follow focus, camera | 0 | 0 | no |
| 17 | Metal or chrome shelving unit | chrome, wire shelf, shelving | 0 | 0 | no |
| 18 | Floor lamps | lamp, floor lamp | 0 | 0 | no |
| 19 | Mini-fridge (Danby) | fridge, danby, refrigerator | 0 | 0 | no |
| 20 | Washer and dryer (Amana) | washer, dryer, laundry, amana | 0 | 0 | no |
| 21 | Bedding and blankets (bagged) | bedding, blanket, duvet | 01 2025-12-04 14-22 Dining area under the opened ceiling, blanket on floor, hutch, table and chairs.jpg; 02 2025-12-04 14-22 Same, striped wool blanket soaking up water.jpg | 0 | yes |
| 22 | Boxes of personal belongings (misc.) | box, boxes | 05 2025-12-06 11-44 Area rug, towels, rolling cart and boxes.jpg | 0 | yes |
| 23 | Bagged contents, several bags (clothing, handbags, household) | bag, bags, clothing, clothes, handbag | 0 | 0 | no |
| 24 | Boot dryer | boot dryer, boot | 0 | 0 | no |
| 25 | Clothes iron or garment steamer | iron, steamer | 0 | 0 | no |
| 26 | Monitor desk arm or mount | monitor arm, monitor, mount | 0 | 0 | no |
| 27 | Picture and diploma frames | frame, diploma, picture frame | 0 | 0 | no |

Why it comes out this way: phone cameras name files by timestamp (20260617_063812.jpg), so a file name carries no content. Date alone cannot pick an item either, because nothing says which day a given belonging was photographed. Finding belongings in an unlabelled library needs the recognition index, the OCR text and the vision model, which is what the Skill delegates to.

## Verification of the keyword hits, by eye

Every file the keyword search hit was opened and compared with the June claim line. A hit only counts if the photo shows the claimed item.

| # | Item | File hit | Shows the June item? |
| --- | --- | --- | --- |
| 1 | Leather reclining sofa | 10 2025-12-08 Wall by the couch.jpg | No. A wall stain beside the upstairs sofa; the sofa itself is a dark corner of the frame and it is not the basement recliner. |
| 6 | Console and side tables | 01 2025-12-04 14-22 Dining area ... table and chairs.jpg | No. The ground-floor dining table, a different piece. |
| 7 | Coffee table | same file | No. Same dining table. |
| 8 | Hex side table | same file | No. Same dining table. |
| 21 | Bedding and blankets | 01 and 02 2025-12-04 ... blanket ... .jpg | No. The striped wool blanket on the dining floor was the December claim's own item 1, not the bagged basement bedding. |
| 22 | Boxes of belongings | 05 2025-12-06 11-44 Area rug, towels, rolling cart and boxes.jpg | No. Boxes on the dining-room rug in December; the June line is the boxes stored in the basement. |

**Verified result: 0 of 27 items found by file name and date.** The six raw hits all come from photos renamed by hand for the December 2025 claim, which is why the method looks better than it is: it found the previous claim's labels, not the belongings.
