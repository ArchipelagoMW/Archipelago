# Wargroove 2 Setup Guide

## Required Files

- Wargroove 2 installed through Steam on Windows
  - Only the Steam Windows version is supported. MAC and Switch are not supported.
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases/latest)

## Backup playerProgress files
`playerProgress` and `playerProgress.bak` contain save data for all of your Wargroove 2 campaigns. 
Backing up these files is strongly recommended in case they become corrupted.
1. Type `%appdata%\Chucklefish\Wargroove2\save` in the file browser and hit enter.
2. Copy the `playerProgress` and `playerProgress.bak` files and paste them into a backup directory.

## Update host.yaml to include the Wargroove 2 root directory

1. Look for your Archipelago install files. By default, the installer puts them in `C:\ProgramData\Archipelago`.
2. Open the `host.yaml` file in your favorite text editor (Notepad will work).
3. Put your Wargroove 2 root directory in the `root_directory:` under the `wargroove2_options:` section.
   - The Wargroove 2 root directory can be found by going to 
   `Steam->Right Click Wargroove 2->Properties->Installed Files->Browse` and copying the path in the address bar.
   - Paste the path in between the quotes next to `root_directory:` in the `host.yaml`.
   - You may have to replace all single \\ with \\\\.
4. Start the Wargroove 2 client.

## Installing the Archipelago Wargroove 2 Mod and Campaign files

1. Shut down Wargroove 2 if it is open.
2. Start the ArchipelagoWargroove2Client.exe from the Archipelago installation. 
This should install the mod and campaign for you.
3. Start Wargroove 2.

## Verify the campaign can be loaded

1. Start Wargroove 2 from Steam.
2. Go to `Story->Campaign->Custom->Archipelago 2` and click play. You should see the first level.

## Starting a Multiworld game

1. Start the Wargroove 2 Client and connect to the server. Enter your username from your 
[options file.](/games/Wargroove/player-options)
2. Start Wargroove 2 and play the Archipelago 2 campaign by going to `Story->Custom->Archipelago 2`.

## Ending a Multiworld game
It is strongly recommended that you delete your campaign progress after finishing a multiworld game.
This can be done by going to the level selection screen in the Archipelago 2 campaign, hitting `ESC` and clicking the 
`Delete Progress` button. The main menu should now be visible.

## Updating to a new version of the Wargroove 2 mod or downloading new campaign files
First, delete your campaign progress by going to the level selection screen in the Archipelago campaign, 
hitting `ESC` and clicking the `Delete Progress` button.
Next, go to `Custom Content->Create->Campaign`, click the `Archipelago 2` campaign and click the `Delete` button.

Follow the `Installing the Archipelago Wargroove 2 Mod and Campaign files` steps again, but look for the latest version 
to download. In addition, follow the steps outlined in 
`Wargroove 2 crashes when trying to run the Archipelago 2 campaign` when attempting to update the 
campaign files and the mod.

## Troubleshooting

### The game is too hard
`Go to the campaign overview screen->Hit escape on the keyboard->Click adjust difficulty->Adjust the setttings`

### The mod doesn't load
Double-check the mod installation under `%appdata%\Chucklefish\Wargroove2\mods`. There should be 3 `.dat` files in 
`%appdata%\Chucklefish\Wargroove2\mods\ArchipelagoMod`. Otherwise, follow 
`Installing the Archipelago Wargroove 2 Mod and Campaign files` steps once more.

### Wargroove 2 crashes or there is a lua error
Wargroove 2 is finicky, but there could be several causes for this. If it happens often or can be reproduced, 
please submit a bug report in the tech-support channel on the [discord](https://discord.gg/archipelago).
Wargroove 2 may report an error when retrying a level. This is currently a bug in the game and not the mod.

### Wargroove 2 crashes when trying to run the Archipelago 2 campaign
This is caused by not deleting campaign progress before updating the mod and campaign files.
1. Go to `Custom Content->Create->Campaign->Archipelago 2->Edit` and attempt to update the mod.
2. Wargroove 2 will give an error message.
3. Go back to `Custom Content->Create->Campaign->Archipelago 2->Edit` and attempt to update the mod again.
4. Wargroove 2 crashes.
5. Go back to `Custom Content->Create->Campaign->Archipelago 2->Edit` and attempt to update the mod again.
6. In the edit menu, hit `ESC` and click `Delete Progress`.
7. In the edit menu, hit `ESC` and click `Mods`.
8. Uncheck the `Archipelago Mod` box, check it again and then click `Save and Reload Map`
9. If the above steps do not allow you to start the campaign from `Story->Campaign->Custom->Archipelago 2` replace 
`playerProgress` and `playerProgress.bak` with your previously backed up files.

### Mod is out of date when trying to run the Archipelago campaign
Please follow the above steps in `Wargroove 2 crashes when trying to run the Archipelago 2 campaign`.

### Using undo turn ignores the income boost or causes bugs
Undoing a turn is bugged in Wargroove 2 and not supported in the randomizer.
There is no way to change how many times the undo action can be used.