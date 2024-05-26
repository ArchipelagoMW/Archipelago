# The Legend of Zelda (NES)

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

All acquirable pickups (except maps and compasses) are shuffled among each other. Logic is in place to ensure both
that the game is still completable, and that players aren't forced to enter dungeons under-geared.

Shops can contain any item in the game, with prices added for the items unavailable in stores. Rupee caves are worth
more while shops cost less, making shop routing and money management important without requiring mindless grinding.

## What items and locations get shuffled?

In general, all item pickups in the game. More formally:

- Every inventory item.
- Every item found in the five kinds of shops.
- Optionally, Triforce Fragments can be shuffled to be within dungeons, or anywhere.
- Optionally, enemy-held items and dungeon floor items can be included in the shuffle, along with their slots
- Maps and compasses have been replaced with bonus items, including Clocks and Fairies.

## What items from The Legend of Zelda can appear in other players' worlds?

All items can appear in other players' worlds.

## What does another world's item look like in The Legend of Zelda?

All local items appear as normal. All remote items, no matter the game they originate from, will take on the appearance
of a single Rupee. These single Rupees will have variable prices in shops: progression and trap items will cost more, 
filler and useful items will cost less, and uncategorized items will be in the middle.

## Are there any other changes made?

- The map and compass for each dungeon start already acquired, and other items can be found in their place.
- The Recorder will warp you between all eight levels regardless of Triforce count
  - It's possible for this to be your route to level 4!
- Pressing Select will cycle through your inventory.
- Shop purchases are tracked within sessions, indicated by the item being elevated from its normal position.
- What slots from a Take Any Cave have been chosen are similarly tracked.

## Local Unique Commands

The following commands are only available when using the Zelda1Client to play with Archipelago.

- `/nes` Check NES Connection State
- `/toggle_msgs` Toggle displaying messages in EmuHawk
