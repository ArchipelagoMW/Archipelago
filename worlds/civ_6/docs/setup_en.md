# Setup Guide for Civilization VI Archipelago

This guide is meant to help you get up and running with Civilization VI in Archipelago. Note that this requires you to have both Rise & Fall and Gathering Storm installed. This will not work unless both of those DLCs are enabled.

## Requirements

The following are required in order to play Civ VI in Archipelago:

- Windows OS (Firaxis does not support the necessary tooling for MacOS or Linux).

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).

- The latest version of the [Civ VI AP Mod](https://github.com/hesto2/civilization_archipelago_mod/releases/latest).

- A copy of the game `Civilization VI` including the two expansions `Rise & Fall` and `Gathering Storm` (both the Steam and Epic version should work).

## Mod Installation

1. Download and unzip the latest release of the mod from [GitHub](https://github.com/hesto2/civilization_archipelago_mod/releases/latest).

2. Copy the folder containing the mod files to your Civ VI mods folder. On Windows, this is usually located at `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods`. If you use OneDrive, check if the folder is instead located in your OneDrive file structure, and use that path when relevant in future steps.

3. Remember this file path, as you will be returning here to install the patch you get from either the Archipelago Multiworld room. The mod will not function without the patch files.

## Installing the Patch

1. You get your patch file either by downloading it from the Archipelago Multiworld room you are about to play in or by getting it directly from the generation output zip file. The format of the file is `.apcivvi`. It is important to note that every room has its own patch file, and the appropriate patch must be installed for each room.

2. Once you have the `.apcivvi` file, you need the files that are inside it, as the `.apcivvi` file is a container. You can extract the files using one of two methods:
    - The first method is by opening it as a zip file. You can do this by either right-clicking it and opening it with a program that handles zip files (If you associate the file type with that program, future `.apcivvi` files will open with it when you double-click them), or by right-clicking and renaming the file extension from `apcivvi` to `zip` (file extensions must be displayed). 
    - You can also associate the file with the Archipelago Launcher and double-click it; doing so will create a folder containing the mod files.

5. Copy the contents of the zip file or folder it generated (the name of the folder should be the same as the apcivvi file) into your Civilization VI Archipelago Mod folder (there should be five files placed there from the `.apcivvi` file, overwrite if asked). It is very important that all five files are placed directly in the `civilization_archipelago_mod` folder.

6. Your mod path should look something like `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods\civilization_archipelago_mod`. If everything was done correctly, you can now connect to the game.

## Connecting to a game

1. In the main menu, navigate to the "Game Options" page. On the "Game" menu, make sure that "Tuner (disables achievements)" is enabled. Restart Civ VI after enabling the tuner.

2. In the main menu, navigate to the "Additional Content" page, then go to "Mods" and make sure the Archipelago mod is enabled. 

3. When starting the game, make sure you are on the Gathering Storm ruleset in a Single Player game. Additionally, you must start in the ancient era, other settings and game modes can be customised to your own liking. An important thing to note is that settings preset saves the mod list from when you created it, so if you want to use a setting preset with this you must create it after installing the Archipelago mod.

4. Start a new Civ VI game. Civ VI is very persistent with mods in the save files. You can reload a game if you have the correct patch files for the save, but don't load an existing save with different patch files or selected mods. 

5. To connect to the room, open the Archipelago Launcher. From there, open the Civ6 client and connect to the room. Once connected to the room enter your slot name and if everything went right you should now be connected.

## Troubleshooting

- If it does not work, make sure you followed the setup instructions exactly as written, if anything is wrong with the folders or where the files were placed it will not work.

- If you get an error when trying to start a game saying `Error - One or more Mods failed to load content`, make sure the files from the `.apcivvi` file are placed directly into the `civilization_archipelago_mod` folder as loose files and not as a folder.

- If you have troubles with file extensions, make sure Windows shows file extensions as they are turned off by default. If you don't know how to turn them on it a quick Google search should help.

- If you are not sending or receiving items, make sure the tuner is enabled.

- If your game enters a state where where someone has sent you items or you have sent locations but these are not correctly sent to the multiworld, you can run `/resync` from the Civ 6 client. This may take up to a minute depending on how many items there are. This can resend certain items to you, like one time bonuses.

- If the archipelago mod does not appear in the mod selector in the game, make sure the mod is correctly placed as a folder in the `Sid Meier's Civilization VI\Mods` folder, there should not be any loose files in there, only folders. As in the path should look something like `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods\civilization_archipelago_mod`.

- If it still does not appear, make sure you have the right folder, one way to verify you are in the right place is to find the general folder area where your Civ VI save files are located.

- If you still have any errors make sure the two expansions Rise & Fall and Gathering Storm are active in the mod selector (all official DLC works without issues but Rise & Fall and Gathering Storm are required for the mod).

- If boostsanity is enabled and those items are not being sent out but regular techs are, make sure you placed the files from your new room in the mod folder and that you started a new Civ VI game.

- If you are neither receiving or sending items, make sure you have the correct client open. The client should be the Civ6 and NOT the Text Client.

- This should be compatible with a lot of other mods, but if you are having issues try disabling all mods other than the Archipelago mod and see if the problem still persists. 

