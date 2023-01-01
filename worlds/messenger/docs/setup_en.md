# The Messenger Randomizer Setup Guide

## Quick Links
- [Main Page](../../../../games/The%20Messenger/info/en)
- [Settings Page](../../../../games/The%20Messenger/player-settings)
- [Courier Github](https://github.com/Brokemia/Courier)
- [The Messenger Randomizer Github](https://github.com/minous27/TheMessengerRandomizerMod)
- [Jacksonbird8237's Item Tracker](https://github.com/Jacksonbird8237/TheMessengerItemTracker)

## Required Software

- [The Messenger](https://store.steampowered.com/app/764790/The_Messenger/)
  - Only Steam version is currently supported.
- [Courier Mod Loader](https://github.com/Brokemia/Courier/releases)
- [The Messenger Randomizer Mod](https://github.com/minous27/TheMessengerRandomizerMod/releases)

### Install

1. Download and install Courier Mod Loader using the instructions on the release page
2. Download and install the randomizer mod
   * Download the latest `TheMessengerRandomizer.zip`
   * Place the zip file as is in `TheMessenger/Mods/`
   * Backup your save game
     1. Press `Windows Key + R` to open run
     2. Type `%appdata%` to access AppData
     3. Navigate to `AppData/locallow/SabotageStudios/The Messenger`
     4. Rename `SaveGame.txt`

## Joining a MultiWorld Game

1. Launch the game
2. Navigate to `Options > Third Party Mod Options`
3. Select `Reset Randomizer File Slots`
   * This will setup all of your save slots with new randomizer save files. You
can have up to 3 randomizer files at a time, but must do this step again to
start new runs afterwards.
4. Enter connection info using the relevant option buttons
   * **The game is limited to alphanumerical characters and `-` so when entering
the host name replace `.`s with ` `s and ensure that your player name when
generating a settings file follows these constrictions**
5. Select the `Connect to Archipelago` button
   * If you've connected successfully, the buttons will be removed from the
menu, which you can confirm by leaving and re-entering it.
6. Navigate to save file selection
7. Select a new valid randomizer save
