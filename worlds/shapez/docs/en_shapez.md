# shapez

## What is this game?

shapez is an automation game about cutting, rotating, stacking, and painting shapes, that you extract from randomly
generated patches on an infinite canvas, and sending them to the hub to complete levels. The "tutorial", where you
unlock a new building or game mechanic (almost) each level, lasts until level 26, where you unlock freeplay with 
infinitely more levels, that require a new, randomly generated shape. Alongside the levels, you can unlock upgrades,
that make your buildings work faster.

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure
and export a config file.
There are also some advanced "datapackage settings" that can be changed by following 
[this guide](/tutorial/shapez/datapackage_settings/en).

## What does randomization do to this game?

Buildings and gameplay mechanics, that you normally unlock by completing a level, and upgrade improvements are put 
into the item pool of the multiworld. Also, if enabled, the requirements for completing a level or buying an upgrade are
randomized.

## What is the goal of shapez in Archipelago?

As the game has no actual goal where the game ends, there are (currently) 4 different goals you can choose from in the 
player options:
1. Vanilla: Complete level 26 (the end of the tutorial).
2. MAM: Complete a player-specified level after level 26. It's recommended to build a Make-Anything-Machine (MAM).
3. Even Fasterer: Upgrade everything to a player-specified tier after tier 8.
4. Efficiency III: Deliver 256 blueprint shapes per second to the hub.

## Which items can be in another player's world?

- Unlock different buildings
- Unlock blueprints
- Big upgrade improvements (adds 1 to the multiplier)
- Small upgrade improvements (adds .1 to the multiplier)
- Other unusual upgrade improvements (optional)
- Different shapes bundles
- Inventory draining traps
- Different traps afflicting random buildings and game mechanics

## What is considered a location check?

- Levels (minimum 1-25, up to 499 depending on player options, with additional checks for levels 1 and 20)
- Upgrades (minimum tiers II-VIII (2-8), up to D (500) depending on player options)
- Delivering certain shapes at least once to the hub ("shapesanity", up to 1000 from a 75800 names pool)
- Achievements (up to 45)

## When the player receives an item, what happens?

A pop-up will show, which item(s) were received, with additional information on some of them.

## What do the names of all these shapesanity locations mean?

Here's a cheat sheet:

![image](/static/generated/docs/shapez/shapesanity_full.png)

## Can I use other mods alongside the AP client?

At the moment, compatibility with other mods is not supported, but not forbidden. Gameplay altering mods will most
likely crash the game or disable loading the afflicted mods, while QoL mods might work without problems. Try at your own
risk.
