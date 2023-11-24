# DOOM II Randomizer Setup

## Required Software

- [DOOM II (e.g. Steam version)](https://store.steampowered.com/app/2300/DOOM_II/)
- [Archipelago Crispy DOOM](https://github.com/Daivuk/apdoom/releases)

## Optional Software

- [ArchipelagoTextClient](https://github.com/ArchipelagoMW/Archipelago/releases)

## Installing AP Doom
1. Download [APDOOM.zip](https://github.com/Daivuk/apdoom/releases) and extract it.
2. Copy DOOM2.WAD from your steam install into the extracted folder.
   You can find the folder in steam by finding the game in your library,
   right clicking it and choosing *Manage→Browse Local Files*.

## Joining a MultiWorld Game

1. Launch apdoom-launcher.exe
2. Select `DOOM II` from the drop-down
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

To hint from in-game, use the chat (Default key: 'T'). Hinting from DOOM II can be difficult because names are rather long and contain special characters. For example:
```
!hint Underhalls (MAP02) - Red keycard
```
The game has a hint helper implemented, where you can simply type this:
```
!hint map02 red
```
For this to work, include the map short name (`MAP01`), followed by one of the keywords: `map`, `blue`, `yellow`, `red`.

## Auto-Tracking

APDOOM has a functional map tracker integrated into the level select screen.
It tells you which levels you have unlocked, which keys you have for each level, which levels have been completed,
and how many of the checks you have completed in each level.
