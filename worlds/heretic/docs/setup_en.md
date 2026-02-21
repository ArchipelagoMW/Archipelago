# Heretic Randomizer Setup

## Required Software

- [Heretic (e.g. Steam version)](https://store.steampowered.com/app/3286930/Heretic__Hexen/)
- [Archipelago Doom 2.0](https://github.com/ArchipelagoDoom/APDoom/releases)

## Installing Archipelago Doom

1. Download [Archipelago Doom 2.0](https://github.com/ArchipelagoDoom/APDoom/releases). On Windows, you will need to extract the zip file somewhere.
2. If you have the Steam version of Heretic + Hexen installed, Archipelago Doom can likely detect it and use the game files from it without needing any further work.
   If this is not the case, however, copy `HERETIC.WAD` from your game's installation directory into the same folder you extracted or installed Archipelago Doom into.

For the Steam version of Heretic + Hexen, you can find the game files by finding the game in your Steam library, right-clicking it and choosing **Manage -> Browse Local Files**. The WAD file you need is in the `/dos/base/` folder.

## Joining a MultiWorld Game (via Launcher)

1. Launch the Archipelago Doom launcher. (`apdoom-launcher.exe` on Windows)
2. Select "Connect to Game".
3. Choose "Select Game..." and then choose "Heretic".
4. Enter the Archipelago server address, slot name, and (if you have one) password.
5. Select "Connect to Server" and wait for the game to start.
6. Enjoy!

The launcher keeps track of the previous games you've played; you can continue a game at any time by selecting "Load Previous Game".

## Joining a MultiWorld Game (via command line)

1. In your command line, navigate to the directory where Archipelago Doom is installed.
2. Run `apdoom-launcher.exe -game heretic -apserver <server> -applayer <slot name>`, where:
    - `<server>` is the Archipelago server address, e.g. "`archipelago.gg:38281`"
    - `<slot name>` is your slot name; if it contains spaces, surround it with double quotes
    - If the server has a password, add `-password`, followed by the server password
3. Enjoy!

To continue a game, reconnect with the same command; Archipelago Doom will automatically load the proper save file.

Optionally, you can override some randomization settings from the command line:
- `-apmonsterrando 0` will disable monster rando.
- `-apitemrando 0` will disable item rando.
- `-apmusicrando 0` will disable music rando.
- `-apresetlevelondeath 0` will disable resetting the level on death.
- `-apdeathlinkoff` will force DeathLink off if it's enabled.
- `-skill <1-5>` changes the game difficulty, from 1 (thou needeth a wet-nurse) to 5 (black plague possesses thee)

## Archipelago Text Client

We recommend having Archipelago's Text Client open on the side to keep track of what items you receive and send.
Archipelago Doom has in-game messages, but they disappear quickly and there's no reasonable way to check your message history in-game.

### Hinting

To hint from in-game, use the in-game chat (Default key: 'T').

As many item names can be long, the following short item name groups are available to use on all clients:

- `!hint E1M6`: will hint the level unlock item for that level (`The Cathedral (E1M6)`).
- `!hint E1M6 Map`: will hint the Map scroll item that corresponds to that level (`The Cathedral (E1M6) - Map scroll`).
- `!hint E1M6 Yellow` (or `Green`, `Blue`): will hint the corresponding key for that level, if it exists (`The Cathedral (E1M6) - Yellow key`).
- `!hint E1M6 Keys`: will hint all keys for that level simultaneously.

## Auto-Tracking

Archipelago Doom has a functional map tracker integrated into the level select screen.
It tells you which levels you have unlocked, which keys you have for each level, which levels have been completed,
and how many of the checks you have completed in each level.
