# Setup Guide for Mega Man Battle Network 3 Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
  (select `Mega Man Battle Network 3 Client` during installation).
- A US Mega Man Battle Network 3 Blue Rom

## Configuring Bizhawk

Once Bizhawk has been installed, open Bizhawk and change the following settings:

- Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". This is required for the Lua script to function correctly.
  **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs** 
  **of newer versions of Bizhawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load** 
  **"NLua+KopiLua" until this step is done.**
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to
  continue playing in the background, even if another window is selected, such as the Client.
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want
  to disable most of these, which you can do quickly using `Esc`.

It is strongly recommended to associate GBA rom extensions (\*.gba) to the Bizhawk we've just installed.
To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with...", unfold
the list that appears and select the bottom option "Look for another application", then browse to the Bizhawk folder
and select EmuHawk.exe.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?
```
TODO once options are available
```

## Joining a MultiWorld Game

### Obtain your GBA patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apbn3` extension.

Double-click on your `.apbn3` file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically (if you associated the extension
to the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click on the "Tools"
menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/mmbn3/mmbn3_connector.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

And remember, it won't work unless you shout to your computer:

JACK IN!   
[Your name]!   
EXECUTE!
