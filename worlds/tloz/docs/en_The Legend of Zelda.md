# The Legend of Zelda (NES)

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

All acquirable pickups (except maps and compasses) are shuffled amongst each other. Logic is in place to ensure both
that the game is still completable, as well as ensuring that players aren't forced to enter dungeons undergeared.

Shops can contain any item in the game, with prices added for the items unavailable in stores. Rupee caves are worth
more while shops will cost less, making shop routing and money management important without requiring mindless grinding.

## What items and locations get shuffled?

In general, all item pickups in the game. More formally:

- Every inventory item.
- Every item found in the five kinds of shops.
- The Heart Containers and Waters of Life found in Take Any caves.
- Optionally, Triforce Fragments can be shuffled to be within dungeons, or anywhere.
- Optionally, enemy-held items and room clear items (except maps and compasses) can be included in the shuffle, along 
with their slots

## What items from The Legend of Zelda can appear in other players' worlds?

All items can appear in other players' worlds.

## What does another world's item look like in The Legend of Zelda?

All local items appear as normal. All remote items, no matter the game they originate from, will take on the appearance
of a single Rupee. These single Rupees will have variable prices in shops: progression and trap items will cost more, 
filler and useful items will cost less, and uncategorized items will be in the middle.

## Are there any other changes made?

Yes. The map and compass for each dungeon start already acquired, and the Recorder will warp you between all eight
levels regardless of Triforce count (note: it's possible for this to be your route to level 4!). Finally, to reduce
frustration, there is an extra copy each of the Sword and the Silver Arrow in the pool.

## Is the randomized game compatible with any other Zelda 1 hacks?

None have been tested, though in theory minor graphical mods should work without issue. Limited testing has been 
performed with the Infinite Hyrule program, and the client correctly accounts for this, but nothing is guaranteed;
should you wish to mix and match hacks, any problems that arise are yours to handle.