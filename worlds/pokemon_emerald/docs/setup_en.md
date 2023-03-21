# Setup Guide for Pokémon Emerald: Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.7 and later is supported. **This may be a different requirement than what you use for some other games.**
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
(select `Pokemon Emerald Client` during installation).
- A Pokémon Emerald ROM file. The Archipelago community cannot provide these.

## Optional Software

- [Pokémon Emerald AP Tracker](https://github.com/AliceMousie/emerald-ap-tracker/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Configuring Bizhawk

Once Bizhawk has been installed, open Bizhawk and change the following settings:

- Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to "Lua+LuaInterface".
Then restart Bizhawk. This is required for the Lua script to function correctly.
**NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it.**
**Fresh installs of newer versions of Bizhawk have a tendency to show "Lua+LuaInterface" as the default selected option**
**but still load "NLua+KopiLua" until this step is done.**
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" box. This will prevent disconnecting from the client while
BizHawk is running in the background.

It is strongly recommended to associate `*.gba` files with the Bizhawk we've just installed. To do so, we simply have to
find any GBA ROM we happen to own, right click and select "Open with...", unfold the list that appears and select
the bottom option "Look for another application", then browse to the Bizhawk folder and select `EmuHawk.exe`.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the
[Pokemon Emerald Player Settings Page](/games/Pokemon%20Emerald/player-settings)

## Joining a MultiWorld Game

### Obtain your patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apemerald` extension.

Double-click on your `.apemerald` file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically (if you associated the extension with
the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click on the "Tools" menu
and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/POKEMON_EMERALD/pokemon_emerald_connector.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`).

## Auto-Tracking

Pokémon Emerald has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon Emerald AP Tracker](https://github.com/AliceMousie/emerald-ap-tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Open PopTracker, and load the Pokémon Emerald pack. 
3. Click on the "AP" symbol at the top.
4. Enter the AP address, slot name and password.
