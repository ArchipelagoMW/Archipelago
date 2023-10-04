# Pokémon Emerald Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- An English Pokémon Emerald ROM. The Archipelago community cannot provide this.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later

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

- [Pokémon Emerald AP Tracker](https://github.com/AliceMousie/emerald-ap-tracker/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generating and Patching a Game

1. Create your settings file (YAML). You can make one on the
[Pokémon Emerald settings page](../../../games/Pokemon%20Emerald/player-settings).
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have the `.apemerald` file extension.
3. Open `ArchipelagoLauncher.exe`
4. Select "Open Patch" on the left side and select your patch file. (You may also be prompted to select your vanilla ROM
the first time you do this.)
5. This will create a patched `.gba` file using your vanilla ROM. It will also open the client and try to run the
newly-created `.gba` file in your emulator. If you want it to automatically open the ROM in BizHawk you need to register
`.gba` files with `EmuHawk.exe`.

If your install was configured correctly, double-clicking the patch file should automatically open the patch with
Archipelago, doing steps 3-5 for you.

If you're playing a single-player seed and you don't care about autotracking or hints, you can stop here, close the
client, and load the patched ROM in any emulator. However, for multiworlds and other Archipelago features, continue
below using BizHawk as your emulator.

## Connecting to a Server

1. Pokemon Emerald uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator may freeze every few seconds until it manages to connect to the client. This is expected. The BizHawk
Client window should indicate that it connected and recognized Pokemon Emerald.
7. To connect the client to the server, enter your room's `<address>:<port>` into the top text field of the client and
click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

If you're feeling adventurous in the future, you can drag the lua script directly onto the emulator screen to open it.
Or, from the Lua Console window, you can use `File > Recent Scripts` to quickly open a script you've used before.

## Auto-Tracking

Pokémon Emerald has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon Emerald AP Tracker](https://github.com/AliceMousie/emerald-ap-tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into packs/ in your PopTracker install.
3. Open PopTracker, and load the Pokémon Emerald pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the AP address, slot name, and password.
