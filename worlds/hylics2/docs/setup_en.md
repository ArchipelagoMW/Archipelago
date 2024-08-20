# Hylics 2 Randomizer Setup Guide

## Required Software

- Hylics 2 from: [Steam](https://store.steampowered.com/app/1286710/Hylics_2/) or [itch.io](https://mason-lindroth.itch.io/hylics-2)
- BepInEx from: [GitHub](https://github.com/BepInEx/BepInEx/releases)
- Archipelago Mod for Hylics 2 from: [GitHub](https://github.com/TRPG0/ArchipelagoHylics2)

## Instructions (Windows)

1. Download and install BepInEx 5 (32-bit, version 5.4.20 or newer) to your Hylics 2 root folder. *Do not use any pre-release versions of BepInEx 6.*

2. Start Hylics 2 once so that BepInEx can create its required configuration files.

3. Download the latest version of ArchipelagoHylics2 from the [Releases](https://github.com/TRPG0/ArchipelagoHylics2/releases) page and extract the contents of the zip file into `BepInEx\plugins`.

4. Start Hylics 2 again. To verify that the mod is working, begin a new game or load a save file.

## Connecting

To connect to an Archipelago server, open the in-game console (default key: `/`) and use the command `/connect [address:port] [name] [password]`. The port and password are both optional - if no port is provided then the default port of 38281 is used.
**Make sure that you have connected to a server at least once before attempting to check any locations.**

## Other Commands

There are a few additional commands that can be used while playing Hylics 2 randomizer:

- `/disconnect` - Disconnect from an Archipelago server.
- `/popups` - Enables or disables in-game messages when an item is found or recieved.
- `/airship` - Resummons the airship at the dock above New Muldul and teleports Wayne to it, in case the player gets stuck. Player must have the DOCK KEY to use this command.
- `/respawn` - Moves Wayne back to the spawn position of the current area in case you get stuck. `/respawn home` will teleport Wayne back to his original starting position.
- `/checked [region]` - States how many locations have been checked in a given region. If no region is given, then the player's location will be used.
- `/deathlink` - Enables or disables DeathLink.
- `/help [command]` - Lists a command, it's description, and it's required arguments (if any). If no command is given, all commands will be displayed.
- `![command]` - Entering any command with an `!` at the beginning allows for remotely sending commands to the server.