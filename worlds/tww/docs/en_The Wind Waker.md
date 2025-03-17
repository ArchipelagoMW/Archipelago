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
