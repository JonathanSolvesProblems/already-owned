# Choosing a search route

Read this before steps U3, U6b and C4b. Choose the route from what is actually known about the item at that moment, and name it in words in the instruction to `photo-agent`. Try the first route that applies; if it returns no results, try the next one that applies, and stop after two routes with no results.

| What is known about the item | Route | Why |
| --- | --- | --- |
| A photo file name from an inventory row | File name | One lookup; the vision model only confirms the item is visible. No search needed. |
| Photos of the same room already returned for other items | Ask the vision model about those real paths | One description per photo and no new search; most basement items share the same few photos. |
| A brand, model or text printed on it (from a receipt line or from the user) | Text visible in the photo | Labels, boxes and screens carry the model text; recognized objects do not. |
| A common object type whose name is on the index category list (sofa, television, bicycle, washing machine) | Recognized object, using the exact category name | The library index already labels these. Never guess a category name that is not on the list from U2 or C3. |
| A purchase date from a matched receipt | Time window from the purchase date to 60 days after | New things get photographed soon after they arrive (unboxing, setup, first use). |
| Only the room | Time window of the room's other photos, then recognized object | Room photos often sit together by date or folder. |
| Nothing but the user's words | Recognized object for the type the user named if it is on the category list, then ask the user at U8 or C7 | Never guess a brand to search for. |

Rules for every route:

- The date that counts is the capture time in the photo metadata, never the upload or modification time. In claim mode the capture time must be before the loss time. A photo after the loss is a damage photo, never proof of ownership. A photo with no capture time is reported as undated and counts only when the user confirms when it was taken.
- Each returned photo is described once by the local vision model, naming every listed item visible in it. A photo that only shows the room is not proof for the item.
- Identical items of the same type shown side by side are one row with the count in Qty. Items of the same type with clearly different features are separate rows. Otherwise ask the user how many there are.
- An entry that does not name one object type (boxes and bags, bedding, assorted tools) is never searched; it gets proof level none and the note "owner to itemize".
- If two routes return no results, report no results for that item and move on. Do not substitute a similar item.
- Questions about individual items are collected and asked once, at U8 or C7, never one pause per item.
