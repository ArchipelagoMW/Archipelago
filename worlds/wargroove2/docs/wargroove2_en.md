# Wargroove 2 Setup Guide

## Required Files

- Wargroove 2 installed through Steam on Windows.
  - Only the Steam Windows version is supported. MAC and Switch are not supported.
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases/latest).

## Installing the Archipelago Wargroove 2 Mod and Campaign files

1. Shut down Wargroove 2 if it is open.
2. Start the ArchipelagoWargroove2Client.exe from the Archipelago installation. 
This should install the mod and campaign for you.
3. Start Wargroove 2.

## Verify the campaign can be loaded

1. Start Wargroove 2 from Steam.
2. Go to `Story` &rarr; `Campaign` &rarr; `Custom` &rarr; `Archipelago 2` and click play. You should see the first level.

## Starting a Multiworld game

1. Start the Wargroove 2 Client and connect to the server. Enter your username from your 
[options file](/games/Wargroove/player-options).
2. Start Wargroove 2 and play the Archipelago 2 campaign by going to `Story` &rarr; `Custom` &rarr; `Archipelago 2`.

## Ending a Multiworld game
It is strongly recommended that you delete your campaign progress after finishing a multiworld game.
This can be done by going to the level selection screen in the Archipelago 2 campaign, hitting `ESC` and clicking the 
`Delete Progress` button. The main menu should now be visible.

## Updating to a new version of the Wargroove 2 mod or downloading new campaign files
First, delete your campaign progress by going to the level selection screen in the Archipelago campaign, 
hitting `ESC` and clicking the `Delete Progress` button.
Next, go to `Custom Content` &rarr; `Create` &rarr; `Campaign`, click the `Archipelago 2` campaign and click the `Delete` button.

Follow the 
[Installing the Archipelago Wargroove 2 Mod and Campaign files](#installing-the-archipelago-wargroove-2-mod-and-campaign-files) 
steps again, but look for the latest version 
to download. In addition, follow the steps outlined in 
[Wargroove 2 crashes when trying to run the Archipelago 2 campaign](#wargroove-2-crashes-when-trying-to-run-the-archipelago-2-campaign) 
when attempting to update the 
campaign files and the mod.

## Troubleshooting

### The game is too hard
Go to the campaign overview screen &rarr; Hit escape on the keyboard &rarr; Click adjust difficulty &rarr; Adjust the settings.

### The mod doesn't load
Double-check the mod installation under `%appdata%\Chucklefish\Wargroove2\mods`. There should be 3 `.dat` files in 
`%appdata%\Chucklefish\Wargroove2\mods\ArchipelagoMod`. Otherwise, follow 
[Installing the Archipelago Wargroove 2 Mod and Campaign files](#installing-the-archipelago-wargroove-2-mod-and-campaign-files) 
steps once more.

### Wargroove 2 crashes or there is a lua error
Wargroove 2 is finicky, but there could be several causes for this. If it happens often or can be reproduced, 
please submit a bug report in the bug-reports channel on the [discord](https://discord.gg/archipelago).
Wargroove 2 may report an error when retrying a level. This is currently a bug in the game and not the mod.

### Wargroove 2 crashes when trying to run the Archipelago 2 campaign
This is caused by not deleting campaign progress before updating the mod and campaign files.
1. Go to `Custom Content` &rarr; `Create` &rarr; `Campaign` &rarr; `Archipelago 2` &rarr; `Edit` and attempt to update the mod.
2. Wargroove 2 will give an error message.
3. Go back to `Custom Content` &rarr; `Create` &rarr; `Campaign` &rarr; `Archipelago 2` &rarr; `Edit` and attempt to update the mod again.
4. Wargroove 2 crashes.
5. Go back to `Custom Content` &rarr; `Create` &rarr; `Campaign` &rarr; `Archipelago 2` &rarr; `Edit` and attempt to update the mod again.
6. In the edit menu, hit `ESC` and click `Delete Progress`.
7. In the edit menu, hit `ESC` and click `Mods`.
8. Uncheck the `Archipelago Mod` box, check it again and then click `Save and Reload Map`.
9. If the above steps do not allow you to start the campaign from `Story` &rarr; `Campaign` &rarr; `Custom` &rarr; `Archipelago 2` replace 
`playerProgress` and `playerProgress.bak` with your previously backed up files.

### Mod is out of date when trying to run the Archipelago campaign
Please follow the above steps in 
[Wargroove 2 crashes when trying to run the Archipelago 2 campaign](#wargroove-2-crashes-when-trying-to-run-the-archipelago-2-campaign).

### Using undo turn ignores the income boost or causes bugs
Undoing a turn is bugged in Wargroove 2 and not supported in the randomizer.
There is no way to change how many times the undo action can be used.