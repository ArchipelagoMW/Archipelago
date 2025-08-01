# Setup Guide for Civilization VI Archipelago

This guide is meant to help you get up and running with Civilization VI in Archipelago. Note that this requires you to have both Rise & Fall and Gathering Storm installed. This will not work unless both of those DLCs are enabled.

## Requirements

The following are required in order to play Civ VI in Archipelago:

- Windows OS (Firaxis does not support the necessary tooling for Mac, or Linux).

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).

- The latest version of the [Civ VI AP Mod](https://github.com/hesto2/civilization_archipelago_mod/releases/latest).

- A copy of the game `Civilization VI` including the two expansions `Rise & Fall` and `Gathering Storm` (both the Steam and Epic version should work).

## Enabling the tuner

In the main menu, navigate to the "Game Options" page. On the "Game" menu, make sure that "Tuner (disables achievements)" is enabled.

## Mod Installation

1. Download and unzip the latest release of the mod from [GitHub](https://github.com/hesto2/civilization_archipelago_mod/releases/latest).

2. Copy the folder containing the mod files to your Civ VI mods folder. On Windows, this is usually located at `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods`. If you use OneDrive, check if the folder is instead located in your OneDrive file structure, and use that path when relevant in future steps.

3. After the Archipelago host generates a game, you should be given a `.apcivvi` file. Associate the file with the Archipelago Launcher and double click it.

4. Copy the contents of the new folder it generates (it will have the same name as the `.apcivvi` file) into your Civilization VI Archipelago Mod folder. If double clicking the `.apcivvi` file doesn't generate a folder, you can instead open it as a zip file. You can do this by either right clicking it and opening it with a program that handles zip files, or by right clicking and renaming the file extension from `apcivvi` to `zip`.

5. Place the files generated from the `.apcivvi` in your archipelago mod folder (there should be five files placed there from the apcivvi file, overwrite if asked). Your mod path should look something like `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods\civilization_archipelago_mod`. 

## Configuring your game

Make sure you enable the mod in the main title under Additional Content > Mods. When configuring your game, make sure to start the game in the Ancient Era and leave all settings related to starting technologies and civics as the defaults. Other than that, configure difficulty, AI, etc. as you normally would.

## Troubleshooting

- If you have troubles with file extension related stuff, make sure Windows shows file extensions as they are turned off by default. If you don't know how to turn them on it is just a quick google search away.

- If you are getting an error: "The remote computer refused the network connection", or something else related to the client (or tuner) not being able to connect, it likely indicates the tuner is not actually enabled. One simple way to verify that it is enabled is, after completing the setup steps, go to Main Menu &rarr; Options &rarr; Look for an option named "Tuner" and verify it is set to "Enabled"

- If your game gets in a state where someone has sent you items or you have sent locations but these are not correctly sent to the multiworld, you can run `/resync` from the Civ 6 client. This may take up to a minute depending on how many items there are. This can resend certain items to you, like one time bonuses.

- If the archipelago mod does not appear in the mod selector in the game, make sure the mod is correctly placed as a folder in the `Sid Meier's Civilization VI\Mods` folder, there should not be any loose files in there only folders. As in the path should look something like `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods\civilization_archipelago_mod`.

- If it still does not appear make sure you have the right folder, one way to verify you are in the right place is to find the general folder area where your Civ VI save files are located.

- If you get an error when trying to start a game saying `Error - One or more Mods failed to load content`, make sure the files from the `.apcivvi` are placed into the `civilization_archipelago_mod` as loose files and not as a folder.

- If you still have any errors make sure the two expansions Rise & Fall and Gathering Storm are active in the mod selector (all the official DLC works without issues but Rise & Fall and Gathering Storm are required for the mod).

- If boostsanity is enabled and those items are not being sent out but regular techs are, make sure you placed the files from your new room in the mod folder.
