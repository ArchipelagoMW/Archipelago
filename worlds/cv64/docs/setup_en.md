# Castlevania 64 Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- A Castlevania 64 ROM of the US 1.0 version specifically. The Archipelago community cannot provide this.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open a `.z64` file in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, load any `.z64` ROM first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.
- All non-Japanese versions of the N64 Castlevanias require a Controller Pak to save game data. To enable this, while
you still have the `.z64` ROM loaded, go to `N64 > Controller Settings...`, click the dropdown by `Controller 1`, and
click `Memory Card`. You must then restart EmuHawk for it to take effect.
- After enabling the `Memory Card` setting, next time you boot up your Castlevania 64 ROM, you will see the 
No "CASTLEVANIA" Note Found screen. Pick `Create "CASTLEVANIA" Note Now > Yes` to create save data and enable saving at
the White Jewels.


## Generating and Patching a Game

1. Create your options file (YAML). You can make one on the
[Castlevania 64 options page](../../../games/Castlevania%2064/player-options).
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have the `.apcv64` file extension.
3. Open `ArchipelagoLauncher.exe`
4. Select "Open Patch" on the left side and select your patch file.
5. If this is your first time patching, you will be prompted to locate your vanilla ROM.
6. A patched `.z64` file will be created in the same place as the patch file.
7. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

If you're playing a single-player seed, and you don't care about hints, you can stop here, close the client, and load
the patched ROM in any emulator or EverDrive of your choice. However, for multiworlds and other Archipelago features,
continue below using BizHawk as your emulator.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Castlevania 64 uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator may freeze every few seconds until it manages to connect to the client. This is expected. The BizHawk
Client window should indicate that it connected and recognized Castlevania 64.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.
