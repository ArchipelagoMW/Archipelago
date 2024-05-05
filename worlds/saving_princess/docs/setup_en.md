# Saving Princess Setup Guide

## Quick Links
- [Game Info](/games/Saving%20Princess/info/en)
- [Options Page](/games/Saving%20Princess/player-options)
- [Saving Princess Archipelago GitHub](https://github.com/LeonarthCG/saving-princess-archipelago)

## Installation Procedures

### Automated Installation

1. Purchase and download [Saving Princess](https://brainos.itch.io/savingprincess)
2. Download and install the latest [Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
3. Launch `ArchipelagoLauncher` or `ArchipelagoSavingPrincessClient` from your Archipelago installation folder
4. If you launched `ArchipelagoLauncher`, click on "Saving Princess Client"
   * You will probably need to scroll down on the Clients column to see it
5. Follow the prompts
   * On Linux, you will need one of either Wine or 7z for the automated installation

Once everything is set up, it is recommended to continue launching the game through this method, as it will check for any updates and automatically apply them.

### Manual Windows Installation

Required software:
- Saving Princess, found at its [itch.io Store Page](https://brainos.itch.io/savingprincess)
- `saving_princess_basepatch.bsdiff4` and `gm-apclientpp.dll`, from [saving_princess_archipelago.zip](https://github.com/LeonarthCG/saving-princess-archipelago/releases/latest)
- Software that can decompress the previous files, such as [7-zip](https://www.7-zip.org/download.html)
- A way to apply `.bsdiff4` patches, such as [bspatch](https://www.romhacking.net/utilities/929/)

Steps:
1. Extract all files from `Saving Princess.exe`, as if it were a `.7z` file
   * Feel free to rename `Saving Princess.exe` to `Saving Princess.exe.7z` if needed
   * If installed through the itch app, you can find the installation directory from the game's page, pressing the cog button, then "Manage" and finally "Open folder in explorer"
2. Extract all files from `saving_princess_archipelago.zip` into the same directory as the files extracted in the previous step
   * This should include, at least, `saving_princess_basepatch.bsdiff4` and `gm-apclientpp.dll`
3. If you don't have `original_data.win`, copy `data.win` and rename its copy to `original_data.win`
   * By keeping an unmodified copy of `data.win`, you will have an easier time updating in the future
4. Apply the `saving_princess_basepatch.bsdiff4` patch using your patching software
5. To launch the game, run `Saving Princess v0_8.exe`

### Manual Linux Installation

The game does run mostly well through Wine, so it is possible to play on Linux, although there are some minor sprite displacement and sound issues from time to time.

You can follow the instructions for Windows with very few changes:

* Using the p7zip package to decompress the file.
```
7z e 'Saving Princess.exe'
```
* And the bsdiff package for patching.
```
bspatch original_data.win data.win saving_princess_basepatch.bsdiff4
```

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en).

### Where do I get a YAML file?

You can customize your options by visiting the [Saving Princess Player Options Page](/games/Saving Princess/player-options).

### Verifying your YAML file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/check).

## Joining a MultiWorld Game

### Set up the connection details

After launching the game, enter the Archipelago options menu through the in-game button with the Archipelago icon.
From here, enter the different menus and type in the **server:port**, **slot**, as well as the **password**, if one is required.

This configuration persists through launches and even updates.

### Connect to the Archipelago Server

To start a connection attempt, simply press on "CONNECT!".

Once connected, the button will become one of either "NEW GAME" or "CONTINUE".
The game automatically keeps a save file for each seed and slot combination, so you do not need to manually move or delete save files.

All that's left is pressing on the button again to start playing. If you are waiting for a countdown, press "NEW GAME" when the countdown finishes.

## Gameplay Questions

### Do I need to save the game before I stop playing?

It is safe to close the game at any point while playing, your progress will be kept.

### What happens if I lose connection?

If a disconnection occurs, you will see the HUD connection indicator go grey.
From here, the game will automatically try to reconnect.
You can tell it succeeded if the indicator regains its color.

If the game is unable to reconnect, save and restart.

Although you can keep playing while disconnected, you won't get any items until you reconnect, not even items found in your own game.
Once reconnected, however, all of your progress should sync up.

### I got an item, but it did not say who sent it to me

Items sent to you by yourself do not list the sender.

Additionally, if you get an item while already having the max for that item (for example, you have 9 ammo and you get sent a Clip Extension) or if the item is cheated in through server commands, no message will be shown at all.

### I pressed the release/collect button, but nothing happened

It is likely that you do not have release or collect permissions, or that there is nothing to release or collect.
Another option is that your connection was interrupted.

If you would still like to use release or collect, refer to [this section of the server commands page](https://archipelago.gg/tutorial/Archipelago/commands/en#collect/release).

You may use the in-game console to execute the commands, if your slot has permissions to do so.
