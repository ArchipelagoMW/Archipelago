# Castlevania: Circle of the Moon Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest).
- A Castlevania: Circle of the Moon ROM of the US version specifically. The Archipelago community cannot provide this.
The Castlevania Advance Collection ROM can be used, but it has no audio. The Wii U Virtual Console ROM does not work.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later.

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open a `.gba` file in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, load any `.gba` ROM first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Optional Software

- [Castlevania: Circle of the Moon AP Tracker](https://github.com/BowserCrusher/Circle-of-the-Moon-AP-Tracker/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases).

## Generating and Patching a Game

1. Create your settings file (YAML). You can make one on the [Castlevania: Circle of the Moon options page](../../../games/Castlevania%20-%20Circle%20of%20the%20Moon/player-options).
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have the `.apcvcotm` file extension.
3. Open `ArchipelagoLauncher.exe`.
4. Select "Open Patch" on the left side and select your patch file.
5. If this is your first time patching, you will be prompted to locate your vanilla ROM.
6. A patched `.gba` file will be created in the same place as the patch file.
7. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

If you're playing a single-player seed, and you don't care about hints, you can stop here, close the client, and load
the patched ROM in any emulator of your choice. However, for multiworlds and other Archipelago features,
continue below using BizHawk as your emulator.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Castlevania: Circle of the Moon uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator may freeze every few seconds until it manages to connect to the client. This is expected. The BizHawk
Client window should indicate that it connected and recognized Castlevania: Circle of the Moon.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Auto-Tracking

Castlevania: Circle of the Moon has a fully functional map tracker that supports auto-tracking.

1. Download [Castlevania: Circle of the Moon AP Tracker](https://github.com/BowserCrusher/Circle-of-the-Moon-AP-Tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into `packs/` in your PopTracker install.
3. Open PopTracker, and load the Castlevania: Circle of the Moon pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password.
