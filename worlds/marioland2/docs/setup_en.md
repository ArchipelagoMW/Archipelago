# Setup Guide for Super Mario Land 2: 6 Golden Coins

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- BizHawk: [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.9.1 is recommended.
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
- A Super Mario Land 2: 6 Golden Coins version 1.0 ROM file. The Archipelago community cannot provide this.

## Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" box. This will prevent disconnecting from the client while
EmuHawk is running in the background.

It is strongly recommended to associate Game Boy ROM extensions (\*.gb) to the EmuHawk we've just installed.
To do so, we simply have to search any Game Boy ROM we happened to own, right click and select "Open with...", unfold
the list that appears and select the bottom option "Look for another application", then browse to the BizHawk folder
and select EmuHawk.exe.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the [Super Mario Land 2 Player Options Page](/games/Super%20Mario%20Land%202/player-options)

## Joining a MultiWorld Game

### Generating and Patching a Game

1. Create your options file (YAML).
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have a `.apsml2` file extension.
3. Open `ArchipelagoLauncher.exe`
4. Select "Open Patch" on the left side and select your patch file.
5. If this is your first time patching, you will be prompted to locate your vanilla ROM.
6. A patched `.gb` file will be created in the same place as the patch file.
7. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

You must connect Super Mario Land 2 to a server, even for a single player game, or progress cannot be made.

### Connect to the Multiserver

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Super Mario Land 2 uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your
game, you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator may freeze every few seconds until it manages to connect to the client. This is expected. The BizHawk
Client window should indicate that it connected and recognized Super Mario Land 2.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)