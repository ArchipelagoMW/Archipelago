# Setup Guide for MegaMan Battle Network 3 Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.7.0 and later are supported.
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases).
- A US MegaMan Battle Network 3 Blue Rom. If you have the [MegaMan Battle Network Legacy Collection Vol. 1](https://store.steampowered.com/app/1798010/Mega_Man_Battle_Network_Legacy_Collection_Vol_1/)
on Steam, you can obtain a copy of this ROM from the game's files, see instructions below.

## Configuring Bizhawk

Once Bizhawk has been installed, open Bizhawk and change the following settings:

- **If you are using a version of BizHawk older than 2.9**, you will need to modify the Lua Core.
  Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". This is required for the Lua script to function correctly.  
  **NOTE:** Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs 
  of newer versions of Bizhawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load 
  "NLua+KopiLua" until this step is done.
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to
  continue playing in the background, even if another window is selected, such as the Client.
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want
  to disable most of these, which you can do quickly using `Esc`.

The first time you open a `.apbn3` patch file, the client will ask you to locate `EmuHawk.exe` inside your BizHawk
install. After that, the client remembers it and launches BizHawk for you automatically.

## Extracting a ROM from the Legacy Collection

The Steam version of the Battle Network Legacy Collection contains unmodified GBA ROMs in its files. You can extract these for use with Archipelago.

1. Open the Legacy Collection Vol. 1's Game Files (Right click on the game in your Library, then open Properties -> Installed Files -> Browse)
2. Open the file `exe/data/exe3b.dat` in a zip-extracting program such as 7-Zip or WinRAR.
3. Extract the file `rom_b_e.srl` somewhere and rename it to `Mega Man Battle Network 3 - Blue Version (USA).gba`

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your options by visiting the 
[MegaMan Battle Network 3 Player Options Page](/games/MegaMan%20Battle%20Network%203/player-options)

## Joining a MultiWorld Game

### Obtain your GBA patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apbn3` extension.

Double-click on your `.apbn3` file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the MMBN3 Client and BizHawk will be started automatically. BizHawk loads the patched ROM and
the `connector_mmbn3.lua` script for you — you do **not** need to open the Lua Console yourself.

### Connect to the Multiserver

To connect the client to the multiserver, put `<address>:<port>` in the textfield at the top of the MMBN3 Client and
press enter (if the server uses a password, type `/connect <address>:<port> [password]` in the bottom textfield).

The client and BizHawk connect to each other automatically once both are running. The client window will indicate when
it has recognized MMBN3.

### Reconnecting / manual connection

If you ever close BizHawk or the client mid-game, reopen the client from the Archipelago Launcher and make sure BizHawk
is running the patched ROM with the connector loaded. If BizHawk was started without the connector (for example, you
opened the ROM by hand), connect it manually:

1. In BizHawk, click the "Tools" menu and select "Lua Console". Click the folder button or press Ctrl+O.
2. Navigate to your Archipelago install folder and open `data/lua/connector_mmbn3.lua`.

**NOTE:** The MMBN3 Lua file depends on other shared Lua files inside the `data` directory in the Archipelago
installation. Do not move this Lua file from its default location or you may run into issues connecting.

Don't forget to start manipulating RNG early by shouting during generation:

```
JACK IN!
[Your name]!   
EXECUTE!
```
