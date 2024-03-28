# The Messenger Randomizer Setup Guide

## Quick Links
- [Game Info](/games/The%20Messenger/info/en)
- [Options Page](/games/The%20Messenger/player-options)
- [Courier Github](https://github.com/Brokemia/Courier)
- [The Messenger Randomizer AP Github](https://github.com/alwaysintreble/TheMessengerRandomizerModAP)
- [PopTracker Pack](https://github.com/alwaysintreble/TheMessengerTrackPack)

## Installation

Read changes to the base game on the [Game Info Page](/games/The%20Messenger/info/en)

### Automated Installation

1. Download and install the latest [Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
2. Launch the Archipelago Launcher (ArchipelagoLauncher.exe)
3. Click on "The Messenger"
4. Follow the prompts

These steps can also be followed to launch the game and check for mod updates after the initial setup.

### Manual Installation

1. Download and install Courier Mod Loader using the instructions on the release page
   * [Latest release is currently 0.7.1](https://github.com/Brokemia/Courier/releases)
2. Download and install the randomizer mod
   1. Download the latest TheMessengerRandomizerAP.zip from
[The Messenger Randomizer Mod AP releases page](https://github.com/alwaysintreble/TheMessengerRandomizerModAP/releases)
   2. Extract the zip file to `TheMessenger/Mods/` of your game's install location
      * You cannot have both the non-AP randomizer and the AP randomizer installed at the same time
   3. Optionally, Backup your save game
      * On Windows
        1. Press `Windows Key + R` to open run
        2. Type `%appdata%` to access AppData
        3. Navigate to `AppData/locallow/SabotageStudios/The Messenger`
        4. Rename `SaveGame.txt` to any name of your choice
      * On Linux
        1. Navigate to `steamapps/compatdata/764790/pfx/drive_c/users/steamuser/AppData/LocalLow/Sabotage Studio/The Messenger`
        2. Rename `SaveGame.txt` to any name of your choice

## Joining a MultiWorld Game

1. Launch the game
2. Navigate to `Options > Archipelago Options`
3. Enter connection info using the relevant option buttons
   * **The game is limited to alphanumerical characters, `.`, and `-`.**
   * This defaults to `archipelago.gg` and does not need to be manually changed if connecting to a game hosted on the
website.
   * If using a name that cannot be entered in the in game menus, there is a config file (APConfig.toml) in the game
directory. When using this, all connection information must be entered in the file. 
4. Select the `Connect to Archipelago` button
5. Navigate to save file selection
6. Start a new game
   * If you're already connected, deleting an existing save will not disconnect you and is completely safe. 

## Continuing a MultiWorld Game

At any point while playing, it is completely safe to quit. Returning to the title screen or closing the game will
disconnect you from the server. To reconnect to an in progress MultiWorld, simply load the correct save file for that
MultiWorld.

If the reconnection fails, the message on screen will state you are disconnected. If this happens, the game will attempt
to reconnect in the background. An option will also be added to the in game menu to change the port, if necessary.
