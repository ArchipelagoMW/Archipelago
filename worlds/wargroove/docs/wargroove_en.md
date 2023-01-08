# Wargroove Setup Guide

## Required Files

Only the Steam Windows version is supported. MAC, Switch, Xbox, Playstation, are all not supported.
The custom campaign must be downloaded, the vanilla and Double Trouble campaigns will not work with Archipelago.

- Wargroove with the Double Trouble DLC installed through Steam on Windows
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)
- Download the `ArchipelagoMod.zip`, `(REALLY_LONG_FILENAME).cmp` and 
`(REALLY_LONG_FILENAME).cmp.bak` files from
  the latest release in [Fly Sniper's GitHub](https://github.com/FlySniper/WargrooveArchipelagoMod/releases)

## Installing the Archipelago Wargroove Mod and Campaign files

1. Open file explorer and type `%appdata%\Chucklefish\Wargroove` in the address bar.
2. Create a `mods` folder if not already present.
3. It is strongly recommended to copy your `playerProgress` and `playerProgress.bak` files found in the `save`
directory to another directory where they can be referenced later. This preserves your save data in case of an 
emergency.
4. Copy the `(REALLY_LONG_FILENAME).cmp` and `(REALLY_LONG_FILENAME).cmp.bak` files into the 
`%appdata%\Chucklefish\Wargroove\save` directory.
5. Unzip `ArchipelagoMod.zip`. Enter the folder named `ArchipelagoMod`. If there is another folder inside also named 
`ArchipelagoMod`, then copy the inside folder to `%appdata%\Chucklefish\Wargroove\mods`, otherwise if there are a bunch 
of `.dat` files inside the `ArchipelagoMod` folder then copy that folder to `%appdata%\Chucklefish\Wargroove\mods`.
Do not install the `ArchipelagoMod.zip` into the mods folder. Do not install an `ArchipelagoMod` folder that has no
`.dat` files inside of it. Do install the `ArchipelagoMod` folder that does have `.dat` files in it.

## Update host.yaml to include the Wargroove root directory

1. Look for your archipelago install files. Typically, they're found in `C:\ProgramData\Archipelago`.
2. Open the `host.yaml` file in your favorite text editor (Notepad will work).
3. Put your Wargroove root directory in the `root_directory:` under the `wargroove_options:` section.
   - The Wargroove root directory can be found by going to 
   `Steam->Right Click Wargroove->Properties->Local Files->Browse Local Files` and copying the path in the address bar.
   - Paste the path in between the quotes next to `root_directory:` in the `host.yaml`
   - You may have to replace all single \\ with \\\\
4. Start the Wargroove client. It should start with no errors, if it does go back to step 1.

## Start Wargroove and verify the campaign can be loaded
1. Start Wargroove from Steam
2. Go to `Story->Campaign->Custom->Archipelago` and click play. You should see the first level

## Starting a Multiworld game
1. Start the Wargroove Client and connect to the server. Enter your username from your 
[settings file](/games/Wargroove/player-settings)
2. Start Wargroove and play the Archipelago campaign by going to `Story->Campaign->Custom->Archipelago`

## Ending a Multiworld game
It is strongly recommended that after finishing a multiworld game to delete campaign progress.
This can be done by going to the level selection screen in the Archipelago campaign, hitting `ESC` and clicking the 
`Delete Progress` button. The main menu should now be visible.

## Updating to a new version of the Wargroove mod or downloading new campaign files
Please delete your campaign progress by going to the level selection screen in the Archipelago campaign, 
hitting `ESC` and clicking the `Delete Progress` button.

Follow the `Installing the Archipelago Wargroove Mod and Campaign files` steps again, but look for the latest version
 to download. In addition, follow the steps outlined in `Wargroove crashes when trying to run the Archipelago campaign`
when attempting to update the campaign files and the mod.

## Troubleshooting

### The game is too hard
`Go to the campaign overview screen->Hit escape on the keyboard->Click adjust difficulty->Adjust the setttings`

### The mod doesn't load
Double-check the mod installation under `%appdata%\Chucklefish\Wargroove\mods` there should be 3 `.dat` files in 
`%appdata%\Chucklefish\Wargroove\mods\ArchipelagoMod`. Otherwise, follow 
`Installing the Archipelago Wargroove Mod and Campaign files` steps once more.

### Wargroove crashes or there is a lua error
Wargroove is finicky, but there could be several causes for this. If it happens often or can be reproduced, 
please submit a bug report.

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
This happens when mod is updated to a new version.
To fix this go to `Custom Content->Create->Campaign->Archipelago->Edit` and click the `Update` button