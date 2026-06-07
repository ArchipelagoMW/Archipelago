# Stardew Valley Randomizer Setup Guide

## Required Software

- Stardew Valley 1.6 on PC (Recommended: [Steam version](https://store.steampowered.com/app/413150/Stardew_Valley/))
- SMAPI ([Mod loader for Stardew Valley](https://smapi.io/) ([Nexus](https://www.nexusmods.com/stardewvalley/mods/2400?tab=files) | [Github](https://github.com/Pathoschild/SMAPI/releases))
- [StardewArchipelago Mod Release 7.x.x](https://github.com/agilbert1412/StardewArchipelago/releases)
    - It is important to use a mod release of version 7.x.x to play seeds that have been generated here. Later releases 
  can only be used with later releases of the world generator, that are not hosted on archipelago.gg yet.

## Optional Software
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    * This provides access to various built-in tools, text client, and local generation and hosting
- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker)
    * If you installed Archipelago, you can use a custom Stardew Tracker that depends on Universal Tracker.
- Other Stardew Valley Mods [Nexus Mods](https://www.nexusmods.com/stardewvalley)
    * There are [supported mods](https://github.com/agilbert1412/StardewArchipelago/blob/7.x.x/Documentation/Supported%20Mods.md) 
  that you can add to your yaml to include them with the Archipelago randomization

    * It is **not** recommended to further mod Stardew Valley with unsupported mods, although it is possible to do so. 
  Mod interactions can be unpredictable, and no support will be offered for related bugs.
    * The more unsupported mods you have, and the bigger they are, the more likely things are to break.

## Configuring your Multiworld

### Customizing my options

You can customize your options by visiting the [Stardew Valley Player Options Page](/games/Stardew%20Valley/player-options)

From there, you can customize all your options, or use a preset. Then, you can either Generate a single player game, or export a yaml file.

### What is a YAML file and do I need one?

A yaml file serves to configure your game in the multiworld. If you play a solo game, you can skip it entirely.

If you intend to play in a multiworld, you will need to provide your yaml file to the person who is hosting the multiworld.

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Creating a room

If you hosted your own game, you can now click "Create Room" and your multiworld will be ready for play!

## Joining a MultiWorld Game

Note that even if you play a solo game, you still connect to a server to play. Hosting on archipelago.gg is free and the easiest option, but you can also host it locally.

### Installing the mod

- Install [SMAPI](https://www.nexusmods.com/stardewvalley/mods/2400?tab=files) by following the instructions on the mod page
- Download and extract the [StardewArchipelago](https://github.com/agilbert1412/StardewArchipelago/releases) mod into 
your Stardew Valley "Mods" folder
- *OPTIONAL*: If you want to launch your game through Steam, add the following to your Stardew Valley launch options: `"[PATH TO STARDEW VALLEY]\Stardew Valley\StardewModdingAPI.exe" %command%`
- Otherwise just launch "StardewModdingAPI.exe" in your installation folder directly
- Stardew Valley should launch itself alongside a console which allows you to read mod information and interact with some of them.

### Connect to the Multiworld

Launch Stardew Valley with SMAPI. Once you have reached the Stardew Valley title screen, create a new farm.

On the new character creation page, you will see 3 new fields, used to link your new character to an archipelago multiworld

![image](https://i.imgur.com/b8KZy2F.png)

You can customize your farm and character as much as desired.

The Server text box needs to have both the address and the port, and your slotname is the name specified in your options. You can also see the name on the room page.

`archipelago.gg:38281`

`StardewPlayer`

The password is optional.

Your game will connect automatically to Archipelago, and reconnect automatically when loading the save, later.

You will never need to enter this information again for this character, unless your room changes its ip or port.
If the room's ip or port **does** change, you will be prompted, after the connection fails, to enter new values and try again.

### Interacting with the MultiWorld from in-game

When you connect, you should see a message in the chat informing you of the `!!help` command. This command will list other 
Stardew-exclusive chat commands you can use.

Furthermore, you can use the in-game chat box to talk to other players in the multiworld, assuming they are using a game 
that supports chatting.

Lastly, you can also run Archipelago commands `!help` from the in game chat box, allowing you to request hints on certain 
items, or check missing locations.

It is important to note that the Stardew Valley chat is fairly limited in its capabilities. For example, it doesn't allow 
scrolling up to see history that has been pushed off screen. The SMAPI console running alongside your game will have the 
full history as well and may be better suited to read older messages.
For a better chat experience, you can also use the official Archipelago Text Client, although it will not allow you to run 
Stardew-exclusive commands.

### Playing with supported mods

See the [Supported mods documentation](https://github.com/agilbert1412/StardewArchipelago/blob/7.x.x/Documentation/Supported%20Mods.md)

### Multiplayer

You cannot play an Archipelago Slot in multiplayer at the moment. There are no short-term plans to support that feature.