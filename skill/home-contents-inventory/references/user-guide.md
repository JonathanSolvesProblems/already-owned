# Home contents inventory: user guide

## Who it is for

Anyone who keeps their phone photos and receipts on the NAS and would have to prove what they owned after a flood, fire or theft. Insurers ask for a list of every item with proof that you owned it and what it cost. Most people rebuild that list by hand, from memory, in the worst week of their year.

## What it does

- **Every week or so**, say "update my home inventory". It looks through the photos taken and the receipts saved since last time, finds the belongings in them, pairs each one with its receipt where there is one, and asks you to confirm everything in one go. Then it puts the new photos in a dated Home contents album, tags every inventory photo and receipt with home-contents, and adds a dated page to the list in your Home Contents folder. Each page holds only what changed that week, and no earlier page is ever rewritten, so the folder is a dated record of what you owned and when it was first written down.
- **Any time**, ask "what do I own in the basement". It answers from the saved list, with the proof behind each item, and searches nothing.
- **After a loss**, say "I had a flood on June 20 in the basement, list what I lost". You can type what was lost, or walk through the room and say it into a voice note. It also shows you belongings that appear in your photos of that room from before the loss and that you did not mention, because nobody remembers a whole room. It finds, for each item in that room, a photo taken before that date, the receipt if you have one, the damage photos taken after, and camera events if it was a break-in or if you agree to include them. You confirm the list and fill in any values, then approve the writes: the claim folder, the copies of the exhibits, the document and the album. A long document is saved in parts, and the NAS may ask once per copied file. What you get is one claim folder you can attach to your insurer's email as it is: the contents claim document, a copy of every photo and receipt it cites, and a SHA-256 value for each file so anyone can check later that nothing was changed since the folder was made. Your originals stay where they were.

## Before the first run

- Let the Photos app finish recognising your library. Until it has, the Skill finds little and says so.
- Keep your phone's photo backup on. The photos you already take are the whole input.
- For a claim, a voice note recorded on the phone reaches the NAS with the same backup, or you can save it to your space by hand.

## What it will not do

- It never estimates what something is worth. Values come from your receipts or from you.
- It never deletes, moves or overwrites a file, and asks before creating any album, tag, folder or file.
- It calls no outside service. It asks every expert to use only the NAS local model; a file that cannot be handled locally is left out and listed in the report, and no other model is asked. If you have set the assistant itself to an online model, that is your setting and the Skill cannot change it.
- It never writes, changes or re-dates a receipt or a photo, and it says no if asked to.
- It never follows text it finds inside a photo, receipt or recording. That text is evidence, not an instruction.
- If it cannot find proof for an item, it says so instead of using a similar photo. A photo taken after the loss is listed as a damage photo, never as proof you owned the item.
- It does not photograph anything for you. When a receipt has no matching photo during an update, it asks you to take one; after a loss, the receipt alone stays on the list as proof of purchase.

## Things you can say

- "Update my home inventory."
- "File this month's receipts into my inventory."
- "What do I own in the living room?"
- "There was a break-in last night, prepare my contents claim."
- "Here is a voice note walking through the basement, list what was damaged on June 20."
