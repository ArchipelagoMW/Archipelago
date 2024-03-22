# Noita

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Noita is a procedurally generated action roguelike. During runs in Noita you will find potions, wands, spells, perks,
chests, etc. Shop items, chests/hearts hidden in the environment, and pedestal items will be replaced with location
checks. Orbs and boss drops can give location checks as well, if their respective options are enabled.
Noita items that can be found in other players' games include specific perks, orbs (optional), wands, hearts, gold,
potions, and other items. If traps are enabled, some randomized negative effects can affect your game when found.

## What is the goal of Noita?

The vanilla goal of Noita is to progress through each level and beat the final boss, taking the Sampo
(gear shaped object) through the portal, and interacting with the altar at the end. There are other endings as well
which require you to gather a certain number of orbs and bring the sampo to an alternate altar.
The Archipelago implementation maintains the same goals. While creating your YAML, you will choose your goal.
While the sampo's location is not randomized, orbs are added to the randomizer pool based on the number of orbs
required for your goal.

Starting a fresh run after death will re-deliver *some* previously delivered items. The standard wand and potion pools
are unaffected by the multiworld item pools. This will not present an issue with progression, and will make
progression easier as the multiworld progresses.

## What Noita items can appear in other players' worlds?

Positive rewards can be:

* `Gold (200 or 1000)`
* `Extra Max HP`
* `Spell Refresher`
* `Random Wand (Tier 1 - 6)`
* `Potion`
* `Orb`
* `Immunity Perk`
* `Extra Life`
* `Other Helpful Perks`
* `Miscellaneous Other Items`

Traps consist of all "Bad" and "Awful" events from Noita's native stream integration. Examples include:

* `Slow Player`
* `Trailing Lava`
* `Worm Rain`
* `Giga Black Holes`

## How many location checks are there?

When using the default options, there are 109 location checks. The number of checks in the game is dependent on the options that you choose.
Please check the information boxes next to the options when setting up your YAML to see how many checks the individual options add.
There are always 42 Holy Mountain checks and 4 Secret Shop checks in the pool which are not affected by your YAML options.

## What does another world's item look like in Noita?

Other players' items will look like the Archipelago logo.

## Is Archipelago compatible with other Noita mods?

Yes, most other Noita mods *should* work. However, most have not been tested.
