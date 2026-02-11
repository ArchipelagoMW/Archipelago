## Simple Setup Guide

[In depth Setup Guide](https://tinyurl.com/mrz7juwe)

## 1. Setup Archipelago Twilight Princess

Install Archipelago v0.6.1 or higher
Install the latest version of [Twilight Princess APWorld](https://tinyurl.com/5e5nkvz5)
Install Dolphin Emulator
Have a Twilight Princess ISO copy in US version

Download the [APTest seed](https://tinyurl.com/3rzz7ksh) and the [REL Loader](https://tinyurl.com/2y32pd6n)
Put the APTest seed and REL Loader in the dolphin save data
Put the RandomizerAP.us.gci you get from the apworld.zip in the dolphin sava data too
Check that there are no vanilla Twilight Princess saves in the save folder
In Dolphin, go to Config -> GameCube -> Slot A, and select GCI Folder. If you press on the 3 dots on the right you can select the path to your Dolphin save data folder (if not changed you can see the standard one there)

## 2. Setup a Multiworld

The Host should gather all player's YAMLs and put them into the Players folder from Archipelago
The Host Generates the game. In the output zip, there will be a file that ends with .aptp. This file is for debug only, so you can just ignore it
After the Multiworld was generated, the .zip is needed to host a room

## 3. Connect to a new Multiworld

Open the Twilight Princess Client via the Archipelago Launcher
Launch the Game and select file 3 which should be called Rel Loader (only once)
The Game will restart and a window should pop up. If you see Archipelago at the top and a seed at the bottom of that screen, everything should be set up
Load a new file. You can ignore the naming part of Link as we do it in the next step
Go in the TPClient and Dolphin should be connected already
Type in TPClient `/name "[Your Slot Name]"` or `/name [Your_Slot_Name]`
After that, type in the Host IP and Port at the top and click connect
Save your game, so you don't have to do the /name part again

## 4. Connect to a running Multiworld

Same as in Step 3:
Open TPClient, Open Game, Load Rel Loader (only once)
This time you can just select your save file from earlier
Connect to the Multiworld

## Twilight Princess v0.3.0

This is the glitched logic update. This setting will now work when choosing it.

### Important info

With the update to AP v0.6.1 you should remove the dolphin memory engine that was added to your lib folder from this apworld.

### What's new

- Added Glitched logic
- Fixed location exclusion to properly work
- Updated to use Archipelago v0.6.1 and its privided Dolphin memory engine
- sky characters are now placed in their vanilla location when not shuffled (places 1 character in starting inventory)
- Added the dungeon rewards are progession option to make heart conatiners and dungeon rewards contain important items
  - This overides dungeons shuffled option
- The small keys on bosses setting has been implemented to force small keys to not be placed on bosses.

### Known Bugs

- Choosing to not shuffle overworld locations can lead to generation failing, as logic is more restrictive
