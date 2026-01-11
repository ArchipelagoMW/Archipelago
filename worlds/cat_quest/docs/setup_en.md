# Cat Quest Multiworld Setup Guide

## Required Software

- Cat Quest from: [Steam](https://store.steampowered.com/app/593280/Cat_Quest/)
    - Games from other storefronts may work, but only if it's the 32 bit version. (EGS, Amazon and GOG are confirmed to be the 64 bit version unfortunately) 
- BepInEx from: [GitHub](https://github.com/BepInEx/BepInEx/releases)
- Cat Quest Randomizer from: [GitHub](https://github.com/Nikkilites/CatQuest-Randomizer/releases)
- Cat Quest World from: [GitHub](https://github.com/Nikkilites/Archipelago-CatQuest/releases)

## Installation

1. Download and install BepInEx 5 (x86, version 5.4.20 or newer) into your Cat Quest root folder. (Don't use the pre-release of 6)

2. Start Cat Quest once, so that BepInEx can create its required configuration files.

3. After BepInEx has been installed and configured, download the Cat Quest Randomizer zip file, move it to the Cat Quest root folder alongside Cat Quest.exe, right click and select "Extract Here" or the equivalent for your extraction software.
   After this, you can delete the .zip file

## Connecting

You connect by opening `...\ArchipelagoRandomizer\SaveData\RoomInfo.json` from your Cat Quest root folder, and adding your player and room information.
It should follow the format that the file already has. Then the connection should be established once you start your save. 

You start a new game by picking New Game in your menu. 

If you already beat the game and only have New Game +. choose this, and then pick New Archipelago Game within that menu (Do not play using Mew Game or New Game +). 

You can continue your saved game by clicking Continue like in vanilla Cat Quest. (Do not click continue on an old savefile, it will send checks to the server for everything done in that old file)
