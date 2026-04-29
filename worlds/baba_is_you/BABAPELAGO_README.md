# Setup Guide For Baba Is You AP

## You Will Need:
- Baba Is You APWorld (available at the [releases](https://github.com/EmilyEmmi/Babapelago/releases) page)
- Copy of Baba Is You (obviously)
- Latest version of Archipelago (available [here](https://github.com/ArchipelagoMW/Archipelago/releases))

## Basic Instructions

This APWorld is installed just like any other AP World. If you're unfamilar with Archipelago, I would recommend following the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup_en), then following the rest of these instructions:

1. Install the Baba Is You APWorld by double-clicking it, or by opening the Launcher and selecting "Install APWorld". This will also install the Baba Is You AP client.
2. In the Launcher, select Generate Template Options to get template option files for all available games. Scroll down to find Baba Is You. Use this file to set up your options like any other game.
3. Once you have the options ready, the host will need the .yaml file, as well as the Baba Is You APWorld if they don't have it already. The host will host a game like usual.

NOTE: You may have a hard time generating with certain options due to the restrictive nature of this game's logic. You can try:
- Disabling world keys, enabling open map
- Using "medium" logic difficulty instead of "easy"
- Lowering gate requirements
- Adding common words to your starting inventory, like "And"
- Reducing the amount of Blossoms/Blossom Petals
- Playing with level shuffle enabled

## Connecting to the Multiserver

1. Launch the Baba Is You client from the Archipelago Launcher. Make sure you do this BEFORE opening Baba Is You.
2. If prompted to select a folder (meaning that a Steam installation was not detected), navigate to the base installation folder (NOT the "Data" folder). The folder should contain the following file:
    - Windows: Baba Is You.exe
    - Mac: Baba Is You.app
    - Linux: run.sh (?). If unsure, check if the "Data" folder exists and contains the game's Lua files.
3. The levelpack should be automatically installed/updated. To re-install the files, run the /install_pack command in the client. If this doesn't work for some reason, look [here](BABAPELAGO_PACK_INSTALL.md) for the instructions to install the levelpack manually.
4. If you'd like to use a different in-game save slot besides slot 1, use /save_slot [number] on the client. If you need more than 3 slots simultaenously, see the "Advanced Features" section. Make sure you do this BEFORE joining the multiworld!
5. Join the multiworld by entering the IP and port at the top, like how you would join with the normal text client. Enter your slot name and the password (leave blank if there is not a password).
6. Launch the Baba Is You game, and open the Babapelago level pack using the same save slot you selected on the client. If you'd like to continue playing the same multiworld later, make sure you keep the save file and don't erase it.

# Advanced Features

## Offline testing

If you launch the Babapelago levelpack without connecting to an AP World and press M, Manual mode will be activated. This allows you to enable/disable items in the built-in Items submenu in the bottom-left corner of the Pause menu. You can also use this menu in normal play to see your goal and what items you have unlocked.

## Multiple slots at once

To play multiple slots at once, simply open the Baba Is You client multiple times, and use the /save_slot command to select a different in-game save slot for each. You can then simply switch save files in-game to play on another Archipelago slot. If you need to run more than 3 slots at once for some reason, use the extraslot.lua mod included on the GitHub release. Add this file to the game files at Data/Lua, NOT the Lua folder included with the level pack.

## Using a different installation

Use the /filepath command to select a different Baba Is You installation. I don't think there's any practical purpose for this other than if you made the wrong selection before.
