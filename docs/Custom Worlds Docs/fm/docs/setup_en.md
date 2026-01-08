# Yu-Gi-Oh! Forbidden Memories Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Please use version 0.4.4 or later for integrated
BizHawk support.
- Yu-Gi-Oh! Forbidden Memories NTSC: ISO or BIN/CUE. Card-drop mods are expressly supported. The Archipelago
implementation tries to be agnostic toward mods, but mods that alter drop tables will create unsupported logic. You do
not have to patch your ROM with Archipelago for it to work. Just make sure you launch a "New Game" for each seed.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later. Other emulators are not supported.
- The latest `fm.apworld` file. You can find this on the [Releases page](https://github.com/sg4e/Archipelago/releases/latest). Put this in your `Archipelago/lib/worlds` folder.

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open any PlayStation game in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, it's because you need to load a game first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Generating a Game

1. Create your options file (YAML). After installing the `fm.apworld` file, you can generate a template within the Archipelago Launcher by clicking `Generate Template Settings`.
2. Follow the general Archipelago instructions for [generating a game](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game).
3. Open `ArchipelagoLauncher.exe`
4. Select "BizHawk Client" in the right-side column. On your first time opening BizHawk Client, you will also be asked to
locate `EmuHawk.exe` in your BizHawk install.

## Connecting to a Server

1. If EmuHawk didn't launch automatically, open it manually.
2. Open your Yu-Gi-Oh! Forbidden Memories NTSC ISO or CUE file in EmuHawk.
3. Go to "New Game" and keep resetting until you're happy with your starter deck. **You need to commit to a starter deck
before connecting to the multiworld.**
4. When you're happy with your deck, save. From here on, you will **never** enter Campaign mode again.
You will duel exclusively in Free Duel mode.
5. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing. Be careful to avoid clicking "TAStudio" below it in the menu, as this is known to delete your savefile.
6. In the Lua Console window, go to `Script > Open Script…`.
7. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
8. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
connected and recognized Yu-Gi-Oh! Forbidden Memories.
9. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## A Note to New Players of Yu-Gi-Oh! Forbidden Memories

Yu-Gi-Oh! Forbidden Memories has a vibrant romhacking community. One of the most popular mods is called
*Card Drop Mod*, which increases the number of cards that the player wins at the end of the duel. The
World Record speedrun for acquiring all the cards in the library for the unmodded game is about 70 hours,
so you'll likely want to play with a high Card Drop Mod variation if you're new to the game. 15 Card Mod
is recommended. Even then, this game is much more suited for an async multiworld.

The Forbidden Memories community is very friendly and has all the resources to help you get started,
including how to patch your game for Card Drop Mod. [You can connect with them via Discord.](https://discord.gg/ygofm)

Here's a particularly useful resource with all duelists' drop tables: [Pocket Duelist](https://pd.ygo.fm/).

## Notes and Limitations

1. Only cards in chest count as checks (not fusions, rituals, etc.).
2. Starchips are out of logic. The logic never expects you to buy a card with starchips. Consequently, starchip-only
cards never gate progression.
3. A card has to be in your chest at least temporarily to count as a check. Therefore, cards in your starter deck
won't be "checked" until you swap them out into your chest. Your chest memory isn't refreshed until you leave the
"Build Deck" screen, so you can't quickly swap a card in and out of your deck to check it. This is a limitation
with how the game writes to chest memory.
4. Only card drops are considered for logic (since acquiring a card is the only way to get it in your chest).
5. If you get a Progressive Duelist item while on the Free Duel screen, you'll have to back out and re-enter to
refresh the available duelists.
6. Make sure to save at the end of every play session. The server will remember your duelists and card checks, but
will not save your card inventory. Your local save file is responsible for that.