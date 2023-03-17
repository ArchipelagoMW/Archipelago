# Noita

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Noita is a procedurally generated roguelite. During runs in Noita you will find potions, wands, spells, perks, and
chests. Shop items, chests/hearts hidden in the environment, and pedestal items may be replaced with location checks. 
Orbs and boss drops may optionally give location checks as well. Noita items that can be found in other players' games include perks, orbs, wands, hearts, gold, potions, and other items. Traps may be enabled as well, resulting in randomized negative effects within your game.

## What is the goal of Noita?

The vanilla goal of Noita is to progress through each level and beat the final boss, taking the Sampo
(gear shaped object) through the portal, and interacting with the altar at the end. There are other endings as well which
require you to gather a certain number of orbs and bring the sampo to an alternate altar.
The Archipelago implementation maintains the same goals. While creating your YAML, you will choose which ending your goal will be.
While the sampo's location is not randomized, orbs are added to the randomizer pool based on the number of orbs required for your goal.

Starting a fresh run after death will re-deliver some previously delivered items. The standard wand, potion, and perk pool are unaffected by the multiworld item pools, so this should not present an issue with progression, and will typically make progression easier as the multiworld progresses.

## What Noita items can appear in other players' worlds?

Positive rewards can be:

* `Gold (200 - 1000)`
* `Extra Max HP`
* `Spell Refreshers`
* `Random Wands (Tiers 1 - 6)`
* `Potions`
* `Orbs`
* `Immunity Perks`
* `Extra Lives`
* `Other Helpful Perks`
* `Miscellaneous Other Items`

Traps consist of all "Bad" and "Awful" events from Noita's native stream integration. Examples include:

* `Slow Player`
* `Trailing Lava`
* `Worm Rain`
* `Spawning black holes`

### How many items are there?

The number of items is dependent on the settings you choose. Please check the information boxes next to the settings when setting up your YAML for more information.

## What does another world's item look like in Noita?

Other players' items will look like the Archipelago logo.

## Is Archipelago compatible with other Noita mods?

Yes, most other Noita mods should work, since the Archipelago mod's implementation is non-destructive and
non-conflicting. However, it is possible that some implementations have been overlooked.

The Archipelago implementation makes the following assumptions, so mods that greatly interfere with these may not
work well:

* All the vanilla biomes and Holy Mountains still exist.
* Holy Mountains exist at certain depths (with some tolerance to shifting their depth).
* There must be at least one chest or pedestal available in each of the vanilla biomes they appear normally.
* Biomes are traversed roughly in the vanilla layout, otherwise some items may be out-of-sequence.
* There are spell refreshes and shops in Holy Mountains, each with at least 5 items.
* There is a secret shop, with at least 4 items (it can be anywhere).
* The vanilla bosses and orbs still exist.
* That the player can complete their selected goal.
