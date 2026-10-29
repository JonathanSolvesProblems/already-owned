# Choosing a search route

Read this before steps U3 and C4. Choose the route from what is actually known about the item at that moment, and name it in the instruction to `photo-agent`. Try the first route that applies; if it returns no results, try the next one that applies, and stop after two routes with no results.

| What is known about the item | Route | Why |
| --- | --- | --- |
| A brand, model or text printed on it (from a receipt line or from the user) | Text visible in the photo | Labels, boxes and screens carry the model text; recognized objects do not. |
| A common object type (sofa, television, bicycle, washer) | Recognized object | The library index already labels these. |
| A purchase date from a matched receipt | Time window from the purchase date to 60 days after | New things get photographed soon after they arrive (unboxing, setup, first use). |
| Only the room | Folder or location, then recognized object | Room photos often sit together by date or folder. |
| Nothing but the user's words | Recognized object for the type the user named, then ask the user | Never guess a brand to search for. |

Rules for every route:

- In claim mode the capture date must be before the loss time. A photo after the loss is a damage photo, never proof of ownership.
- Each returned photo is checked by the local vision model for the item actually being visible. A photo that only shows the room is not proof for the item.
- Two different physical items of the same type (two chairs) are two rows only when the photos show them side by side or with clearly different features; otherwise ask the user how many there are.
- If two routes return no results, report no results for that item and move on. Do not substitute a similar item.
