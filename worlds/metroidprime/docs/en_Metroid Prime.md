# Metroid Prime Archipelago

An Archipelago implementation of Metroid Prime multiworld randomizer using [randomprime](https://github.com/randovania/randomprime/).

## What does randomization do to this game?

In Metroid Prime, all suit upgrades and expansion items are shuffled into the multiworld, adding variety to the routes available for completing the game's objectives.

## What is the goal of Metroid Prime when randomized?

The end goal of the randomizer game can consist of:

- Collecting the required amount of Artifacts (amount is configurable)
- Defeating Ridley (configurable)
- Defeating Metroid Prime (configurable)

The end goal can be scanned in the Temple Security station.

## Which items can be in another player's world?

All suit upgrades and expansion items can be shuffled in other players' worlds, excluding Power Suit and Combat Visor.

## What does another world's item look like in Metroid Prime?

Multiworld items appear as one of the following:

- Progression Item: Cog
- Useful Item or Trap: Zoomer Model with a random texture
- Filler Item: Metroid Model with a random texture

## What versions of the Metroid Prime are supported?

All GameCube versions of the game are supported.
The Wii and Switch versions of the game are _not_ supported.

## When the player receives an item, what happens?

The player will immediately have their suit inventory updated and receive a notification in the Client and a HUD message during gameplay.

## FAQs

### Can I teleport to the starting room?

To warp to the starting location,

1. Enter a Save Station
2. When prompted to Save, choose No
3. While choosing No, simultaneously hold down the L and R buttons.

### When fighting Ridley my screen keeps changing width, what's going on?

This is an issue with having aspect ratio set to `auto`. Forcing it to `4:3` should resolve the issue.

### What Metroid Prime mods/tools does this work with?

It is recommended to use a vanilla ISO with the latest release of [Dolphin](https://dolphin-emu.org/download/#).

- Not thoroughly tested; but some users report that these work
  - [PrimeHack](https://forums.dolphin-emu.org/Thread-fork-primehack-fps-controls-and-more-for-metroid-prime)
  - [Widescreen HUD Mod](<https://wiki.dolphin-emu.org/index.php?title=Metroid_Prime_(GC)#16:9_HUD_Mod>) (0-00 USA only)
  - [MPItemTracker](https://github.com/UltiNaruto/MPItemTracker)
- Not compatible
  - Practice Mod (The AP client is unable to connect to the game with this mod present.)

### Can tricks be included in logic?

You can select a general difficulty of tricks you want to be allowed as well as explicitly include or exclude certain tricks via the options as well. For a comprehensive list of tricks and their associated difficulties, take a look at [this document](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/metroidprime/data/Tricks.py)

### Aside from item locations being shuffled, how does this differ from the vanilla game?

Some of the changes include:

- Layout Changes
  - The game skips the Space Pirate Frigate introduction sequence, automatically placing you into the Starting Room (default: Tallon Overworld - Landing Site)
  - Starting Room can optionally be randomized.
  - Elevator destinations can optionally be randomized.
  - In Main Plaza, Chozo Ruins, the upper ledge door to Vault is no longer locked.
  - Traversing "backwards" through the Pirate Labs in Phendrana is now possible:
    In Research Lab Hydra, the switch to disable the force field can be scanned from behind the force field.
  - Traversing "backwards" through the Crashed Frigate is now possible:
    In Main Ventilation Shaft Section B, the door will be powered up and openable when approached from behind.
  - Traversing "backwards" through Upper Phazon Mines can be possible (configurable):
    In Main Quarry, the barrier is automatically disabled when entering from Mine Security Station.
  - In Elite Research, Phazon Mines, the fight with Phazon Elite can now be started without needing to collect the item in Central Dynamo.
- QOL Changes:
  - When Morph Ball Bomb is acquired, Spring Ball can be used.
    To use Spring Ball, tilt the C-Stick Up.
- Options for Progressive Beams:
  - Each beam is broken up into 3 "Progressive {beam name}" items. They will unlock the beam, the ability to charge it, then the associated beam/missile combo
