# Stardew Valley Randomizer Setup Guide

## Required Software

- Stardew Valley on PC (Recommended: [Steam version](https://store.steampowered.com/app/413150/Stardew_Valley/))
- SMAPI ([Mod loader for Stardew Valley](https://smapi.io/))
- [StardewArchipelago Mod](https://github.com/agilbert1412/StardewArchipelago/releases)

## Optional Software
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (Only for the TextClient)
- Other Stardew Valley Mods [Nexus Mods](https://www.nexusmods.com/stardewvalley)
    - It is **not** recommended to further mod Stardew Valley, altough it is possible to do so. Mod interactions can be unpredictable, and no support will be offered for related bugs.
    - The more mods you have, and the bigger they are, the more likely things are to break.

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your settings by visiting the [Stardew Valley Player Settings Page](/games/Stardew Valley/player-settings)

## Joining a MultiWorld Game

### Installing the mod

- Install [SMAPI](https://smapi.io/) by following the instructions on their website
- Download and extract the [StardewArchipelago](https://github.com/agilbert1412/StardewArchipelago/releases) mod into your Stardew Valley "Mods" folder
- If you want to launch your game through Steam, add the following to your Stardew Valley launch options:
    - "[PATH TO STARDEW VALLEY]\Stardew Valley\StardewModdingAPI.exe" %command%
- Otherwise just launch "StardewModdingAPI.exe" in your installation folder directly
- Stardew Valley should launch itself alongside a console which allows you to read mod information and interact with some of them.

### Connect to the MultiServer

Launch Stardew Valley with SMAPI. Once you have reached the Stardew Valley title screen, create a new farm.

On the new character creation page, you will see 3 new fields, used to link your new character to an archipelago multiworld

![image](https://i.imgur.com/b8KZy2F.png)

You can customize your farm and character as much as desired.

The Server needs to have both the address and the port, and your slotname is the name specified in your yaml

`archipelago.gg:38281`

`StardewPlayer`

The password is optional.

Your game will connect automatically to Archipelago, and reconnect automatically when loading the save, later.

You will never need to enter this information again for this character.

### Multiplayer

You cannot play an Archipelago Slot in multiplayer at the moment. There is no short-terms plans to support that feature.