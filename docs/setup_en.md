# Wario Land 4 Setup

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
  (select `Wario Land 4 Client` during installation).
- A Wario Land 4 ROM. Either US/Europe or Japanese is acceptable.

## Configuring BizHawk

Once BizHawk has been installed, open BizHawk and change the following settings:

- Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua"
  to "Lua+LuaInterface". Then restart BizHawk. This is required for the Lua script to function
  correctly. **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two**
  **options and reselect it. Fresh installs of newer versions of BizHawk have a tendency to show**
  **"Lua+LuaInterface" as the default selected option but still load "NLua+KopiLua" until this**
  **step is done.**
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the
  5s button. This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This
  will allow you to continue playing in the background, even if another window is selected.
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard.
  You will likely want to disable most of these, which you can do quickly using `Esc`.

It is strongly recommended to associate the GBA ROM extension (\*.gba) to the BizHawk we've just
installed. To do so, we simply have to search any GBA ROM we happened to own, right click and select
"Open with...", unfold the list that appears and select the bottom option "Look for another
application", then browse to the BizHawk folder and select EmuHawk.exe.

An alternative BizHawk setup guide as well as various pieces of troubleshooting advice can be found
[here](https://wiki.ootrandomizer.com/index.php?title=BizHawk).

## Configuring your Config (.yaml) file

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal
settings and export a config file from them: [Wario Land 4 Player Settings Page](/games/Wario%20Land%204/player-settings)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do
so on the YAML Validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whomever is
hosting. Once that is done, the host will provide you with either a link to download your patch
file, or with a zip file containing everyone's patch files. Your patch file should have a `.apwl4`
extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should
automatically launch the client, and will also create your ROM in the same place as your patch file.

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click
on the "Tools" menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua
script.

Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the text field on top and
press enter (if the server uses a password, type in the bottom text field
`/connect <address>:<port> [password]`)

Now you're ready to start looting the Golden Pyramid.

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to
  your players, so they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the
  progress of all players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
