# The Legend of Zelda (NES)

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

All acquirable pickups (except maps and compasses) are shuffled amongst each other. Logic is in place to ensure both
that the game is still completable, as well as ensuring that players aren't forced to enter dungeons undergeared 
(specifically, no dark room navigation, and each level requires one extra Heart Container per level before it, as would 
be the norm in vanilla).

Additionally, shop prices are added and changed to account for added items. In general, the prices
of everything were halved, and formerly non-shop items are priced based on their utility and power. As well, 
the amounts and of the "It's a secret..." money caves have been randomized (between 150% and 250% of their 
original value) and their tiers randomized (so all the former high value caves will still be the same value, but not
necessarily still the highest value). As a result, money management and shop routing will still be important, but
grinding for Rupees in order to proceed shouldn't be necessary.

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

## What does another world's item look like in The Legend of Zelda

All local items appear as normal. All remote items, no matter the game they originate from, will take on the appearance
of a single Rupee. Since the single Rupee never appears as an obtainable item from shops or other item locations, any
single Rupee so found can be known to be a remote item. You'll even still get the one Rupee for picking it up!
