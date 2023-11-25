# DOOM 1993 Randomizer Setup

## Required Software

- [DOOM 1993 (e.g. Steam version)](https://store.steampowered.com/app/2280/DOOM_1993/)
- [Archipelago Crispy DOOM](https://github.com/Daivuk/apdoom/releases)

## Optional Software

- [ArchipelagoTextClient](https://github.com/ArchipelagoMW/Archipelago/releases)
- [PopTracker](https://github.com/black-sliver/PopTracker/)
  - [OZone's APDoom tracker pack](https://github.com/Ozone31/doom-ap-tracker/releases)

## Installing AP Doom
1. Download [APDOOM.zip](https://github.com/Daivuk/apdoom/releases) and extract it.
2. Copy `DOOM.WAD` from your game's installation directory into the newly extracted folder.
   You can find the folder in steam by finding the game in your library,
   right-clicking it and choosing **Manage -> Browse Local Files**.

## Joining a MultiWorld Game

1. Launch apdoom-launcher.exe
2. Select `Ultimate DOOM` from the drop-down
3. Enter the Archipelago server address, slot name, and password (if you have one)
4. Press "Launch DOOM"
5. Enjoy!

To continue a game, follow the same connection steps.
Connecting with a different seed won't erase your progress in other seeds.

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
