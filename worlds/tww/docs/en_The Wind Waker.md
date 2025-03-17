# The Wind Waker

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items get shuffled between the different locations in the game, so each playthrough is unique. Randomized locations
include chests, items received from NPC, and treasure salvaged from the ocean floor. The randomizer also includes
quality-of-life features such as a fully opened world, removing many cutscenes, increased sailing speed, and more.

## Which locations get shuffled?

Only locations put into logic by the world's settings will be randomized. The remaining locations in the game will have
a yellow Rupee, which includes a message that the location is not randomized.

## What is the goal of The Wind Waker?

Reach and defeat Ganondorf atop Ganon's Tower. This will require all eight shards of the Triforce of Courage, the
fully-powered Master Sword (unless it's swordless mode), Light Arrows, and any other items necessary to reach Ganondorf.

## What does another world's item look like in TWW?

Items belonging to other non-TWW worlds are represented by Father's Letter (the letter Medli gives you to give to
Komali), an unused item in the randomizer.

## When the player receives an item, what happens?

When the player receives an item, it will automatically be added to Link's inventory. Unlike many other Zelda
randomizers, Link **will not** hold the item above his head.

## I need help! What do I do?

Refer to the [FAQ](https://lagolunatic.github.io/wwrando/faq/) first. Then, try the troubleshooting steps in the
[setup guide](/tutorial/The%20Wind%20Waker/setup/en). If you are still stuck, please ask in the Wind Waker channel in
the Archipelago server.

## Known issues

- Randomized freestanding rupees, spoils, and bait will also be given to the player picking up the item. The item will
  be sent properly, but the collecting player will receive an extra copy.
- Demo items (items which are held over Link's head) which are **not** randomized, such as rupees from salvages from
  random light rings or rewards from minigames, will not work.
- Item get messages for progressive items received on locations that send earlier than intended will be incorrect. This
  does not affect gameplay.
- The Heart Piece count in item get messages will be off by one. This does not affect gameplay.
- It has been reported that item links can be buggy. Nothing game-breaking, but do be aware of it.

Feel free to report any other issues or suggest improvements in the Wind Waker channel in the Archipelago server!

## Tips and Tricks

### Where are dungeon secrets found in the dungeons?

[This document](https://docs.google.com/document/d/1LrjGr6W9970XEA-pzl8OhwnqMqTbQaxCX--M-kdsLos/edit?usp=sharing) has
images of each of the dungeon secrets.

### What exactly do the obscure and precise difficulty options do?

The `logic_obscurity` and `logic_precision` options modify the randomizer's logic to put various tricks and techniques
into logic.
[This document](https://docs.google.com/spreadsheets/d/14ToE1SvNr9yRRqU4GK2qxIsuDUs9Edegik3wUbLtzH8/edit?usp=sharing)
neatly lists the changes that are made. The options are progressive, so, for instance, hard obscure difficulty includes
both normal and hard obscure tricks. Some changes require a combination of both options. For example, to put having the
Forsaken Fortress cannons blow the door up for you into logic requires both obscure and precise difficulty to be set to
at least normal.

### What are the different options presets?

A few presets are available on the [player options page](../player-options) for your convenience.

- **Tournament S7**: These are (as close to as possible) the settings used in the WWR Racing Server's
  [Season 7 Tournament](https://docs.google.com/document/d/1mJj7an-DvpYilwNt-DdlFOy1fz5_NMZaPZvHeIekplc).
  The preset features 3 required bosses and hard obscurity difficulty, and while the list of enabled progression options
  may seem intimidating, the preset also excludes several locations.
- **Miniblins 2024**: These are the settings used in the WWR Racing Server's
  [2024 Season of Minblins](https://docs.google.com/document/d/1vasz1dzEeOIkm8dBN0YhQqAw9bT0H9bpyUl8_co-dBs). This
  preset is great if you're new to Wind Waker! There aren't too many locations in the world, and you only need to
  complete two dungeons. You also start with many convenience items such as double magic, an Empty Bottle, and six
  hearts.
- **Mixed Pools**: These are the settings used in the WWR Racing Server's
  [Mixed Pools Co-op Tournament](https://docs.google.com/document/d/1YGPTtEgP978TIi0PUAD792OtZbE2jBQpI8XCAy63qpg). This
  preset features full entrance rando and includes many locations behind a randomized entrance. There are also a bunch
  of overworld locations, as these settings were intended to be played in a two-person co-op team. The preset also has 6
  required bosses, but since entrance pools are randomized, the bosses could be found anywhere! Check your Sea Chart to
  find out which island the bosses are on.

## Planned Features

- Dynamic CTMC based on enabled options
- Hint implementation from base randomizer (hint placement options and hint types)
- Integration with Archipelago's hint system (e.g., auction hints)
- EnergyLink support
- Swift Sail logic as an option
- Continued bugfixes

## Credits

This randomizer would not be possible without the help from:

- BigSharkZ: (icon artwork)
- Celeste (Maëlle): (logic and typo fixes, additional programming)
- Chavu: (logic difficulty document)
- CrainWWR: (multiworld and Dolphin memory assistance, additional programming)
- Cyb3R: (reference for `TWWClient`)
- DeamonHunter: (additional programming)
- Dev5ter: (initial TWW AP implmentation)
- Gamma / SageOfMirrors: (additional programming)
- LagoLunatic: (base randomizer, additional assistance)
- Lunix: (Linux support, additional programming)
- Mysteryem: (tracker support, additional programming)
- Necrofitz: (additional documentation)
- Ouro: (tracker support)
- tal (matzahTalSoup): (dungeon secrets guide)
- Tubamann: (additional programming)

The Archipelago logo © 2022 by Krista Corkos and Christopher Wilson, licensed under
[CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/).
