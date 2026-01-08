# Celeste

## What counts as an item/location?

At the moment, the following count as both items and location checks:
- Strawberries
- Cassettes
- Crystal Hearts
- Level Completions


The following are not counted, but may be included in the future:
- Golden Strawberries
- Moon Berry
- PICO-8 Collectables


## How do level unlocks work?

Level unlocks work mostly the same as they would in vanilla Celeste, except that they are triggered by items sent by the
MultiWorld server. This means that levels will typically need to be played out of order, starting with "Chapter 1: 
Forsaken City" (which automatically unlocks after the Tutorial).

For example, "Chapter 2: Old Site A-Side" is unlocked once a Completion item from "Chapter 1: Forsaken City" is found in the 
multi-world and "Chapter 2: Old Site B-Side" is unlocked once the `Cassette (Chapter 2: Old Site A-Side)` item is found in the multi-world.

One key difference is how C-Sides are unlocked, in that they are unlocked once both the A-Side and B-Side Crystal Hearts
are found for a chapter. For example, "Chapter 2: Old Site C-Side" is unlocked once `Crystal Heart (Chapter 2: Old Site A-Side)` and 
`Crystal Heart (Chapter 2: Old Site B-Side)` are both found in the multi-world.

When the world is first started, all of the Chapter Select icons will be visible, but those that have no Sides unlocked
within them will be greyed out. Once any Side is unlocked for a Chapter, the Chapter Select icon will no longer be
greyed out, and instead the Sides that are not unlocked will be individually greyed out within this. Any icon that is
greyed out cannot be pressed, blocking access to Chapters/Sides that are not yet unlocked.

## What is the goal for a Celeste world?

The following goals can be selected for a Celeste world:
- Completing "Chapter 7: The Summit A-Side".
- Completing "Chapter 8: Core A-Side".
- Completing "Chapter 9: Farewell A-Side".

There is a set of options that allow you to configure how many items of different types need to have been collected
prior to accessing the goal level. The required number of Cassettes, Crystal Hearts, Level Completions, and Strawberries can all be configured.

The following goals are currently being planned for addition:
- Completing some set of Sides (e.g., all A-Sides, all A and B-Sides, etc) for all Chapters in-game.

The following configuration options are also being planned:
- Toggle for whether the end-game item checks are based on receiving items from the multi-world or completing location
checks.
- Toggle for including progression items in the item/location pool (i.e., allowing some/all game progression to occur
normally).
- Selector for whether extra Sides should be included in the rotation pool (i.e., removing B and C-Sides from being
playable).
- Selector for how C-Sides are unlocked (e.g., the original unlock method, the new Archipelago unlock method, other
easier methods, etc).
