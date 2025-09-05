# DOOM 1993 Randomizer Setup

## Required Software

- [DOOM 1993 (e.g. Steam version)](https://store.steampowered.com/app/2280/DOOM__DOOM_II/)
- [Archipelago Crispy DOOM](https://github.com/Daivuk/apdoom/releases)

## Optional Software

- [ArchipelagoTextClient](https://github.com/ArchipelagoMW/Archipelago/releases)
- [PopTracker](https://github.com/black-sliver/PopTracker/)
  - [OZone's APDoom tracker pack](https://github.com/Ozone31/doom-ap-tracker/releases)

## Installing AP Doom
1. Download [APDOOM.zip](https://github.com/Daivuk/apdoom/releases) and extract it.
2. Copy `DOOM.WAD` from your game's installation directory into the newly extracted folder.
   You can find the folder in steam by finding the game in your library,
   right-clicking it and choosing **Manage -> Browse Local Files**. The WAD file is in the `/base/` folder.

## Joining a MultiWorld Game (via Launcher)

1. Launch apdoom-launcher.exe
2. Select `Ultimate DOOM` from the drop-down
3. Enter the Archipelago server address, slot name, and password (if you have one)
4. Press "Launch DOOM"
5. Enjoy!

To continue a game, follow the same connection steps.
Connecting with a different seed won't erase your progress in other seeds.

## Joining a MultiWorld Game (via command line)

1. In your command line, navigate to the directory where APDOOM is installed.
2. Run `crispy-apdoom -game doom -apserver <server> -applayer <slot name>`, where:
    - `<server>` is the Archipelago server address, e.g. "`archipelago.gg:38281`"
    - `<slot name>` is your slot name; if it contains spaces, surround it with double quotes
    - If the server has a password, add `-password`, followed by the server password
3. Enjoy!

Optionally, you can override some randomization settings from the command line:
- `-apmonsterrando 0` will disable monster rando.
- `-apitemrando 0` will disable item rando.
- `-apmusicrando 0` will disable music rando.
- `-apfliplevels 0` will disable flipping levels.
- `-apresetlevelondeath 0` will disable resetting the level on death.
- `-apdeathlinkoff` will force DeathLink off if it's enabled.
- `-skill <1-5>` changes the game difficulty, from 1 (I'm too young to die) to 5 (Nightmare!)

## Archipelago Text Client

We recommend having Archipelago's Text Client open on the side to keep track of what items you receive and send.
APDOOM has in-game messages,
but they disappear quickly and there's no reasonable way to check your message history in-game.

### Hinting

To hint from in-game, use the chat (Default key: 'T'). Hinting from DOOM can be difficult because names are rather long and contain special characters. For example:
```
!hint Toxin Refinery (E1M3) - Computer area map
```
The game has a hint helper implemented, where you can simply type this:
```
!hint e1m3 map
```
For this to work, include the map short name (`E1M1`), followed by one of the keywords: `map`, `blue`, `yellow`, `red`.

## Auto-Tracking

APDOOM has a functional map tracker integrated into the level select screen.
It tells you which levels you have unlocked, which keys you have for each level, which levels have been completed,
and how many of the checks you have completed in each level.

For better tracking, try OZone's poptracker package: https://github.com/Ozone31/doom-ap-tracker/releases .
Requires [PopTracker](https://github.com/black-sliver/PopTracker/).
