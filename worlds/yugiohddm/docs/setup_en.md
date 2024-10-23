# Yu-Gi-Oh! Dungeon Dice Monsters Setup Guide

## Playing YGO DDM in the Multiworld
- The game will play out solely in Free Duel. Do not enter any tournaments!

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Please use version 0.4.4 or later for integrated
BizHawk support.
- Yu-Gi-Oh! Dungeon Dice Monsters .GBA rom.
- Make sure to launch a "New Game" for each seed you play.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later. Other emulators are not supported.
- The latest `ygoddm.apworld` file. You can find this on the [Releases page](https://github.com/JustinMarshall98/Archipelago/releases/latest). Put this in your `Archipelago/lib/worlds` folder.

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open any Gameboy game in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, it's because you need to load a game first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Generating a Game

1. Create your options file (YAML). After installing the `ygoddm.apworld` file, you can generate a template within the Archipelago Launcher by clicking `Generate Template Settings`.
2. Follow the general Archipelago instructions for [generating a game](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game).
3. Open `ArchipelagoLauncher.exe`
4. Select "BizHawk Client" in the right-side column. On your first time opening BizHawk Client, you will also be asked to
locate `EmuHawk.exe` in your BizHawk install.

## Connecting to a Server

1. If EmuHawk didn't launch automatically, open it manually.
2. Open your Yu-Gi-Oh! Dungeon Dice Monsters .gba file in EmuHawk.
3. Create a new save file (New Game) and keep resetting until you're happy with your starter dice pool. **You need to have created
the new save and committed to a starting dice pool before connecting to the multiworld.**
4. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing. Be careful to avoid clicking "TAStudio" below it in the menu, as this is known to delete your savefile.
5. In the Lua Console window, go to `Script > Open Script…`.
6. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
7. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
connected and recognized Yu-Gi-Oh! Dungeon Dice Monsters.
8. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Notes and Limitations

1. Only defeating duelists in free play counts as checks. Unlocking more duelists through tournament play is vanilla
game functionality but these unlocks are expected to be given as checks to you by the players in the multiworld,
so **do not enter tournaments.**
2. If you get Dice items while modifying your Dice Pool you may need to back out of editing it and re-enter that screen to
have your dice inventory updated.
3. If you get a Duelist Unlock item while on the Free Duel screen, you just need to scroll up or down enough to make the screen
move to get the game to display the new duelist.