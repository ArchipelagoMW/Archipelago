# A Link Between Worlds Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- A decrypted, North American A Link Between Worlds `.cci` ROM (if you have a `.3ds` ROM, just rename it). Instructions for dumping your ROM can be found [here](https://wiki.hacks.guide/wiki/3DS:Dump_titles_and_game_cartridges). **Make sure to select "decrypt" when dumping.**
- To play on emulator: [Azahar](https://azahar-emu.org/pages/download/)
- To play on 3ds: [Luma3DS](https://3ds.hacks.guide/) and LittleCube's [plugin.3gx](https://github.com/LittleCube-hax/albw-ap-plugin/releases/latest)
- **The game must be played with the language set to English.**

## Installation

1. Install the latest version of Archipelago.
2. Download `albw.apworld` and put it in your `Archipelago/custom_worlds/` folder.

## Setup (Emulator)

1. In Azahar, select `File > Open Azahar Folder`. Create a `load` folder inside this folder, and inside the `load` folder create a `mods` folder.
2. Also in Azahar, select `Emulation > Configure`. Then, in the general section, on the top, select `Debug`. Finally, at the bottom, ensure that the `Enable RPC Server` option is enabled.

## Setup (3DS)

1. Install Luma3DS, following the guide at https://3ds.hacks.guide/
2. On the Luma3DS configuration screen after power-up (if this screen does not show up, hold SELECT during power-up):
	1. _Make sure_ that `Enable loading external FIRMs and modules` does **NOT** have an x next to it. If so, disable it.
	2. Turn `Enable game patching` on and make sure it **DOES** have an x next to it.
	3. Press Start or choose `Save and exit`.
3. Press L+DPadDown+Select to open the Rosalina menu, and make sure that `Plugin loader` is set to `[Enabled]`.
4. Download [plugin.3gx](https://github.com/LittleCube-hax/albw-ap-plugin/releases/latest) and copy it to `/luma/plugins/00040000000EC300/` on your SD card.

## Generating a Game

1. Create your player options YAML file. A sample YAML is included.
2. Gather the YAMLs of all players into the `Archipelago/Players` folder.
3. Run the Archipelago Launcher and select Generate.
4. A zip file will be created in the `Archipelago/output` folder. Upload this to [the Archipelago website](https://archipelago.gg/uploads) to host your game.
5. Inside the zip file is a `.apalbw` file. You will need this file to play the game.

## Playing a Game (Emulator)

1. The host will give you a `.apalbw` file. Drag and drop this file onto the Archipelago Launcher. Alternatively, run the Launcher, click Open Patch, and select your `.apalbw` file.
2. Enter the path to your A Link Between Worlds ROM when prompted. Wait about 20 seconds for the game to patch.
3. This will do two things. First, it will open the A Link Between Worlds client. Second, it will create a zip file with the same name and directory as the patch file. Unzip this file; it contains a folder named `00040000000EC300`.
4. Place the `00040000000EC300` folder inside the `load/mods/` folder you created. (If there is already a folder with this name from a previous randomizer, delete it first.)
5. Run A Link Between Worlds in the emulator. The client should automatically connect to the emulator.
6. Enter the server URL into the client and press Connect.

## Playing a Game (3DS)

1. The host will give you a `.apalbw` file. Drag and drop this file onto the Archipelago Launcher. Alternatively, run the Launcher, click Open Patch, and select your `.apalbw` file.
2. Enter the path to your A Link Between Worlds ROM when prompted. Wait about 20 seconds for the game to patch.
3. This will do two things. First, it will open the A Link Between Worlds client. Second, it will create a zip file with the same name and directory as the patch file. Unzip this file; it contains a folder named `00040000000EC300`.
4. Copy the `00040000000EC300` folder to `/luma/titles/` on your SD card.
5. Re-insert your SD card into your 3DS and power it on.
6. Run A Link Between Worlds. At the end of the red 3DS loading screen, you should see a blue flash. This means the plugin has loaded successfully.
7. Run the command on-screen into your ALBW client.
8. Enter the server URL into the client and press Connect.

## Resuming a Game

1. Run the Archipelago Launcher and select the A Link Between Worlds client.
2. Do steps 5-6 under Playing a Game (Emulator) or steps 6-8 under Playing a Game (3DS).
