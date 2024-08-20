# Wargroove Setup Guide

## Required Files

- Wargroove with the Double Trouble DLC installed through Steam on Windows
  - Only the Steam Windows version is supported. MAC, Switch, Xbox, and Playstation are not supported.
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)

## Backup playerProgress files
`playerProgress` and `playerProgress.bak` contain save data for all of your Wargroove campaigns. Backing up these files
is strongly recommended in case they become corrupted.
1. Type `%appdata%\Chucklefish\Wargroove\save` in the file browser and hit enter.
2. Copy the `playerProgress` and `playerProgress.bak` files and paste them into a backup directory.

## Update host.yaml to include the Wargroove root directory

1. Look for your Archipelago install files. By default, the installer puts them in `C:\ProgramData\Archipelago`.
2. Open the `host.yaml` file in your favorite text editor (Notepad will work).
3. Put your Wargroove root directory in the `root_directory:` under the `wargroove_options:` section.
   - The Wargroove root directory can be found by going to 
   `Steam->Right Click Wargroove->Properties->Installed Files->Browse` and copying the path in the address bar.
   - Paste the path in between the quotes next to `root_directory:` in the `host.yaml`.
   - You may have to replace all single \\ with \\\\.
4. Start the Wargroove client.

## Installing the Archipelago Wargroove Mod and Campaign files

1. Shut down Wargroove if it is open.
2. Start the ArchipelagoWargrooveClient.exe from the Archipelago installation. 
This should install the mod and campaign for you.
3. Start Wargroove.

## Verify the campaign can be loaded

1. Start Wargroove from Steam.
2. Go to `Story->Campaign->Custom->Archipelago` and click play. You should see the first level.

## Starting a Multiworld game

1. Start the Wargroove Client and connect to the server. Enter your username from your 
[options file.](/games/Wargroove/player-options)
2. Start Wargroove and play the Archipelago campaign by going to `Story->Campaign->Custom->Archipelago`.

## Ending a Multiworld game
It is strongly recommended that you delete your campaign progress after finishing a multiworld game.
This can be done by going to the level selection screen in the Archipelago campaign, hitting `ESC` and clicking the 
`Delete Progress` button. The main menu should now be visible.

## Updating to a new version of the Wargroove mod or downloading new campaign files
First, delete your campaign progress by going to the level selection screen in the Archipelago campaign, 
hitting `ESC` and clicking the `Delete Progress` button.

Follow the `Installing the Archipelago Wargroove Mod and Campaign files` steps again, but look for the latest version
 to download. In addition, follow the steps outlined in `Wargroove crashes when trying to run the Archipelago campaign`
when attempting to update the campaign files and the mod.

## Troubleshooting

### The game is too hard
`Go to the campaign overview screen->Hit escape on the keyboard->Click adjust difficulty->Adjust the setttings`

### The mod doesn't load
Double-check the mod installation under `%appdata%\Chucklefish\Wargroove\mods`. There should be 3 `.dat` files in 
`%appdata%\Chucklefish\Wargroove\mods\ArchipelagoMod`. Otherwise, follow 
`Installing the Archipelago Wargroove Mod and Campaign files` steps once more.

### Wargroove crashes or there is a lua error
Wargroove is finicky, but there could be several causes for this. If it happens often or can be reproduced, 
please submit a bug report in the tech-support channel on the [discord](https://discord.gg/archipelago).

### Wargroove crashes when trying to run the Archipelago campaign
This is caused by not deleting campaign progress before updating the mod and campaign files.
1. Go to `Custom Content->Create->Campaign->Archipelago->Edit` and attempt to update the mod.
2. Wargroove will give an error message.
3. Go back to `Custom Content->Create->Campaign->Archipelago->Edit` and attempt to update the mod again.
4. Wargroove crashes.
5. Go back to `Custom Content->Create->Campaign->Archipelago->Edit` and attempt to update the mod again.
6. In the edit menu, hit `ESC` and click `Delete Progress`.
7. If the above steps do not allow you to start the campaign from `Story->Campaign->Custom->Archipelago` replace 
`playerProgress` and `playerProgress.bak` with your previously backed up files.

### Mod is out of date when trying to run the Archipelago campaign
Please follow the above steps in `Wargroove crashes when trying to run the Archipelago campaign`.