# Setup Guide for Pokémon Red and Blue: Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
  (select `Pokemon Client` during installation).
- Pokémon Red and/or Blue ROM files. The Archipelago community cannot provide these.

## Optional Software

- [Pokémon Red and Blue Archipelago Map Tracker](https://github.com/j-imbo/pkmnrb_jim/releases/latest), for use with [PopTracker](https://github.com/black-sliver/PopTracker/releases)


## Configuring Bizhawk

Once Bizhawk has been installed, open Bizhawk and change the following settings:

- Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". Then restart Bizhawk. This is required for the Lua script to function correctly.
  **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs** 
  **of newer versions of Bizhawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load** 
  **"NLua+KopiLua" until this step is done.**
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" box. This will prevent disconnecting from the client while
BizHawk is running in the background.

It is strongly recommended to associate GB rom extensions (\*.gb) to the Bizhawk we've just installed.
To do so, we simply have to search any Gameboy rom we happened to own, right click and select "Open with...", unfold
the list that appears and select the bottom option "Look for another application", then browse to the Bizhawk folder
and select EmuHawk.exe.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the [Pokemon Red and Blue Player Settings Page](/games/Pokemon%20Red%20and%20Blue/player-settings)

It is important to note that the `game_version` option determines the ROM file that will be patched.
Both the player and the person generating (if they are generating locally) will need the corresponding ROM file.

For `trainer_name` and `rival_name` the following regular characters are allowed:

* `‘’“”·… ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyzé'-?!.♂$×/,♀0123456789`

And the following special characters (these each take up one character):
* `<'d>`
* `<'l>`
* `<'t>`
* `<'v>`
* `<'r>`
* `<'m>`
* `<PK>`
* `<MN>`
* `<MALE>` alias for `♂`
* `<FEMALE>` alias for `♀`

## Joining a MultiWorld Game

### Obtain your Pokémon patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apred` or `.apblue` extension.

Double-click on your patch file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically (if you associated the extension
to the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click on the "Tools"
menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/connector_pkmn_rb.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

Now you are ready to start your adventure in Kanto.

## Auto-Tracking

Pokémon Red and Blue has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon Red and Blue Archipelago Map Tracker](https://github.com/j-imbo/pkmnrb_jim/releases/latest) and [PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Open PopTracker, and load the Pokémon Red and Blue pack. 
3. Click on the "AP" symbol at the top.
4. Enter the AP address, slot name and password. 

The rest should take care of itself! Items and checks will be marked automatically, and it even knows your settings - It will hide checks & adjust logic accordingly.
