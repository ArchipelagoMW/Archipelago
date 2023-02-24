# Noita

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Noita is a procedurally generated roguelite. During runs in Noita you will find potions, wands, spells, perks, and
chests. For purposes of Archipelago multiworld functionality, collecting chests, results in an item check. Noita items 
that can be found in other players' games include, gold, max health increase, spell refresh, wands, and perks. 
Additionally, within your player settings YAML you can enable traps in the pool, resulting in negative effects on 
the Noita world.

Because chests are quite rare in Noita, the Archipelago Noita mod allows you to set a kill count to spawn chests. 

## What is the goal of Noita?

The vanilla goal of Noita is to progress through each level and beat the final boss, taking the Sampo
(gear shaped object) through the portal and interacting with the end. 
In the Archipelago implementation, however, you play an "endless run"; when you die or beat the final boss, you
continue playing from the beginning until all locations have been checked.

Starting a fresh run after death or unlocking one of the endings can re-deliver previous rewards (excluding potions
and traps). The standard wand, potion, and perk pool are unaffected by the multiworld item pools, so this should not
present an issue with progression.

## What Noita items can appear in other players' worlds?

Positive rewards can be:

* `Gold (200 - 1000)`
* `Extra Max HP`
* `Spell Refresher`
* `Random Wand (Tiers 1 - 6)`
* `Potion`

Traps consist of all "Bad" and "Awful" events from the native stream integration, some examples:

* `Slow Player`
* `Trailing Lava`
* `Worm Rain`
* `Spawning black holes`

### How many items are there?

You can configure the number of item checks that will be present in the Noita world within the player settings yaml, by
default this is set to 100. After all checks are completed any further chests opened will be empty. For high location 
counts it is recommended to use a lower setting for number of kills required to spawn a chest.

## What does another world's item look like in Noita?

All chests in the game will perform an item check and drop a banner featuring the archipelago logo, the in game console
will confirm what items was sent or received when collecting.

## Is Archipelago compatible with other Noita mods?

Yes, most other Noita mods should work, since the Archipelago mod's implementation is non-destructive and
non-conflicting. However, it is possible that some implementations are overlooked.

The Archipelago implementation makes the following assumptions, so mods that greatly interfere with these may not
work well:

* All the vanilla biomes and Holy Mountains still exist.
* Holy Mountains exist at certain depths (with some tolerance to shifting their depth).
* There must be at least one chest or pedestal available in each of the vanilla biomes they appear normally.
* Biomes are traversed roughly in the vanilla layout, otherwise some items may be out-of-sequence.
* There are spell refreshes and shops in Holy Mountains, each with at least 5 items.
* There is a secret shop, with at least 4 items (it can be anywhere).
* That the player can complete their selected goal (i.e. kill a boss).
