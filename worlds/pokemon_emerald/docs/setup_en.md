# Pokémon Emerald Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
(Make sure to select `Pokemon Emerald Client` during installation)
- A Pokémon Emerald ROM file (USA/Europe). The Archipelago community cannot provide this.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.8 or later

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- Go to `Config > Customize`. Switch to the Advanced tab, then switch the Lua Core from `NLua+KopiLua` to `Lua+LuaInterface`. Then restart EmuHawk. This is required for the Lua script to function correctly.
- Under Config > Customize, check the "Run in background" box. This will prevent disconnecting from the client while EmuHawk is running in the background.
- Open a `.gba` file in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click `Controllers…` it's because you need to have any `.gba` ROM loaded first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to clear it.

## Optional Software

- [Pokémon Emerald AP Tracker](https://github.com/AliceMousie/emerald-ap-tracker/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generating and Patching a Game

1. Create your settings file (YAML). You can make one on the Pokémon Emerald settings page [here](https://archipelago.gg/games/Pokemon Emerald/player-settings).
2. Follow the general Archipelago instructions for generating a game [here](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game). This will generate an output file for you. Your patch file will have the `.apemerald` file extension.
3. Once you have a patch file, open that patch file with the `PokemonEmeraldClient` program to patch your game. This will create a `.gba` file using your dumped ROM and the patch file. It will also open the client and try to open the newly-created `.gba` file in your emulator. If you want it to automatically open the ROM in BizHawk you need to register `.gba` files with `EmuHawk.exe`.

If you're playing a single-player game, you don't need to do anything else. You can close the client and play the patched ROM offline in whatever emulator you wish. However, even single-player games can benefit from playing online to get hints, cheat in items, and use auto-tracking. If you'd like any of those features, or if you're playing a multiworld game, continue to the next section.

## Connecting to a Server

1. Once the emulator and client are running you need to connect them. In EmuHawk, go to `Tools > Lua Console`. This window needs to stay open while you're playing.
2. In this new window, go to `Script > Open Script…` (you can also press `Ctrl+O` or click the folder icon).
3. Navigate to your Archipelago install folder and open `data/lua/connector_pkmn_emerald.lua`. The Lua Console window should indicate that it connected to the client.
4. To connect the client to the server, put `<address>:<port>` into the top text field and click `Connect`. (If the server uses a password, type `/connect <address>:<port> <password>` into the bottom text field and press enter.)

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect.

If your connection ever stops working, simply save your game, close both the client and emulator, and do these steps again. You will automatically receive any items you might have missed, and send any items you collected as soon as you reconnect. This issue can sometimes happen if emulation is paused for more than a few seconds (e.g. spending time in a menu or resizing the window).

## Auto-Tracking

Pokémon Emerald has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon Emerald AP Tracker](https://github.com/AliceMousie/emerald-ap-tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Open PopTracker, and load the Pokémon Emerald pack. 
3. Click on the "AP" symbol at the top.
4. Enter the AP address, slot name, and password.
