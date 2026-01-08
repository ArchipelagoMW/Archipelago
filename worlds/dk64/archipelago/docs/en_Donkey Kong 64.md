# Donkey Kong 64

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

The level entrances from DK Isles have also been swapped around. This means that you may find Creepy Castle where the entrance for Jungle Japes normally is, and so on.

Due to some current technical constraints brought on by the Archipelago framework, a number of randomizer settings cannot be changed, including:

- Purchases from shopkeepers (Cranky/Funky/Candy) are forced to cost 0 coins
- B. Lockers' costs are 0 Golden Bananas for all levels, except for Hideout Helm which needs 60 Golden Bananas
- Banana Medal checks are sent after collecting 40 of the same colored bananas in a world, down from 75

These restrictions may be lifted in future updates to this APWorld.

In addition, Tag Anywhere is considered in logic for collecting items.

## What is the goal of Donkey Kong 64 when randomized?

Currently, two goals can be selected:

- Defeat King K. Rool
- Find all the Keys for K. Lumsy's cage

## What items and locations get shuffled?

The locations of the following items will be shuffled:

- Playable Kongs
- Golden Bananas
- Banana Fairies
- Banana Medals
- Battle Crowns
- All Keys for K. Lumsy's cage, except Key 8
- Blueprints
- Instruments, guns and respective upgrades
- Training Grounds moves
- Moves purchased from shops
- The Banana Fairy Camera
- The Shockwave attack
- The Bean in Fungi Forest
- The Pearls in Gloomy Galleon
- The Nintendo and Rareware coins

## Which items can be in another player's world?

All of the items listed above can be randomized into other games.

In addition, there are filler items that refill your health or consumable "ammo" for certain moves, including gun ammo, Orange Grenades, Crystal Coconuts, Banana Camera film, and instrument energy.

Traps are also available in the item pool, but trap spawning can be reduced or disabled entirely in your YAML settings.

The rewards for returning blueprints to Snide will always be Golden Bananas.

## What does another world's item look like in Donkey Kong 64?

Items from other games will appear as an Archipelago icon. When you collect them, a message will appear on screen showing the item's name and who it is for.

## When somebody playing Donkey Kong 64 receives an item, what happens?

By default, a message will appear on screen showing what item you received and who sent it.

You can change how fast or for which classes of items that these messages will appear for with the `receive_notifications`  option in your YAML settings.