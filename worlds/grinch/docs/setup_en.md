# The Grinch - Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Please use version 0.6.2 or later for integrated
BizHawk support.
- Legally obtained NTSC Bin ROM file, probably named something like `Grinch, The (USA) (En,Fr,Es).bin`.
- CUE files may work, but I have not tested this.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) Version 2.9.1 is supported, but I can't promise if any version is stable or not.
- The latest `grinch.apworld` file. You can find this on the [Releases page](https://github.com/MarioSpore/Grinch-AP/releases/latest). Put this in your `Archipelago/custom_worlds` folder.

## Configuring BizHawk
Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Under `Config > Preferred Cores > PSX`, select NymaShock.
- Open any PlayStation game in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, it's because you need to load a game first.
- Ape Escape is very particular about its analog setup: go to `PSX > Settings` and select `Sync Settings`. Change Virtual
Port 1 to Dual Analog to help prevent deadzone issues.
You may need to invert Sensitivity for the up/down axis to -100%.
This can be found under Analog Controls through `Config > Controllers…`.
Depending on your controller, you may also want to tweak the Deadzone. Something like 6% is recommended for a DualShock 4.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Generating a Game

1. Create your options file (YAML). After installing the `grinch.apworld` file, you can generate a template within the Archipelago Launcher by clicking `Generate Template Settings`.
2. Follow the general Archipelago instructions for [generating a game](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game).
3. Open `ArchipelagoLauncher.exe`
4. Select "BizHawk Client" in the right-side column. On your first time opening BizHawk Client, you will also be asked to
locate `EmuHawk.exe` in your BizHawk install.

### Connect to the Multiserver

Once both the client and the emulator are started, they must be connected. **This should happen automatically.**
However, if the lua script window doesn't appear, then within the emulator click
on the "Tools" menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua
script. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the text field on top and
press enter (if the server uses a password, type in the bottom text field
`/connect <address>:<port> [password]`)