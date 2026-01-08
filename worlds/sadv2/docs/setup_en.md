# Sonic Advance 2 Setup Guide

## Required Software

- Archipelago
- A North American copy of Sonic Advance 2 (A2NE should be printed on the bottom right of the cartridge label)
- Bizhawk 2.7 or later (Alternatively, you can use mGBA with Zunawe's mGBA connector script)

### Configuring Bizhawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open a `.gba` file in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, load any `.gba` ROM first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.
- If you have a save file you're attached to, I'd recommend going into `./GBA/SaveRAM/` and making a copy of your Sonic Advance 2 save file to a different directory. The client will indirectly modify your save file.

## Connecting to a server

1. Sonic Advance 2 uses Archipelago's Bizhawk Client, which can be found in the Archipelago Launcher
2. Open EmuHawk and run your Sonic Advance 2 rom. Make sure the game opens to the title screen. If it opens to the language select screen, select your language and enter your name so that the game loads to the title screen.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script...`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator and client will connect to each other. The client will tell you it connected to Sonic Advance 2 when successful.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the top text field of the client and click connect. When prompted to enter your slot name, enter it in the bottom text field.

Once connected, you can send and receive items. You'll need to do these steps every time you reconnect. Make sure you're connected before playing, as Sonic Advance 2 has no way to know what progress was made offline. However, this will not make any checks missable, so simply checking the location again once connected is enough to send the check.