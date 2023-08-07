# Stardew Valley Randomizer Setup Guide

## Required Software

- Stardew Valley on PC (Recommended: [Steam version](https://store.steampowered.com/app/413150/Stardew_Valley/))
- SMAPI ([Mod loader for Stardew Valley](https://smapi.io/))
- [StardewArchipelago Mod Release 4.x.x](https://github.com/agilbert1412/StardewArchipelago/releases)
    - It is important to use a mod release of version 4.x.x to play seeds that have been generated here. Later releases can only be used with later releases of the world generator, that are not hosted on archipelago.gg yet.

## Optional Software
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (Only for the TextClient)
- Other Stardew Valley Mods [Nexus Mods](https://www.nexusmods.com/stardewvalley)
    - There are [supported mods](https://github.com/agilbert1412/StardewArchipelago/blob/4.x.x/Documentation/Supported%20Mods.md) that you can add to your yaml to include them with the Archipelago randomization

    - It is **not** recommended to further mod Stardew Valley with unsupported mods, although it is possible to do so. Mod interactions can be unpredictable, and no support will be offered for related bugs.
    - The more unsupported mods you have, and the bigger they are, the more likely things are to break.

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your settings by visiting the [Stardew Valley Player Settings Page](/games/Stardew%20Valley/player-settings)

## Joining a MultiWorld Game

### Installing the mod

- Install [SMAPI](https://smapi.io/) by following the instructions on their website
- Download and extract the [StardewArchipelago](https://github.com/agilbert1412/StardewArchipelago/releases) mod into your Stardew Valley "Mods" folder
- *OPTIONAL*: If you want to launch your game through Steam, add the following to your Stardew Valley launch options:
    - "[PATH TO STARDEW VALLEY]\Stardew Valley\StardewModdingAPI.exe" %command%
- Otherwise just launch "StardewModdingAPI.exe" in your installation folder directly
- Stardew Valley should launch itself alongside a console which allows you to read mod information and interact with some of them.

### Connect to the MultiServer

Launch Stardew Valley with SMAPI. Once you have reached the Stardew Valley title screen, create a new farm.

On the new character creation page, you will see 3 new fields, used to link your new character to an archipelago multiworld

![image](https://i.imgur.com/b8KZy2F.png)

You can customize your farm and character as much as desired.

The Server text box needs to have both the address and the port, and your slotname is the name specified in your yaml

`archipelago.gg:38281`

`StardewPlayer`

The password is optional.

Your game will connect automatically to Archipelago, and reconnect automatically when loading the save, later.

You will never need to enter this information again for this character, unless your room changes its ip or port.
If the room's ip or port **does** change, you can follow these instructions to modify the connection information of your save file
- Launch modded Stardew Valley
- While **on the main menu** of the game, enter the follow command **in the SMAPI console**:
- `connect_override ip:port slot password`
- Example: `connect_override archipelago.gg:38281 StardewPlayer`
- Load your save game. The new connection information will be used, instead of the saved one
- Play a full day, sleep, and save the game. This connection information will overwrite the previous one and become permanent.

### Interacting with the MultiWorld from in-game

When you connect, you should see a message in the chat informing you of the `!!help` command. This command will list other Stardew-exclusive chat commands you can use.

Furthermore, you can use the in-game chat box to talk to other players in the multiworld, assuming they are using a game that supports chatting.

Lastly, you can also run Archipelago commands `!help` from the in game chat box, allowing you to request hints on certain items, or check missing locations.

It is important to note that the Stardew Valley chat is fairly limited in its capabilities. For example, it doesn't allow scrolling up to see history that has been pushed off screen. The SMAPI console running alonside your game will have the full history as well and may be better suited to read older messages.
For a better chat experience, you can also use the official Archipelago Text Client, altough it will not allow you to run Stardew-exclusive commands.

### Playing with supported mods

See the [Supported mods documentation](https://github.com/agilbert1412/StardewArchipelago/blob/4.x.x/Documentation/Supported%20Mods.md)

### Multiplayer

You cannot play an Archipelago Slot in multiplayer at the moment. There are no short-terms plans to support that feature.