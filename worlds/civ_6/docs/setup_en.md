# Setup Guide for Civilization VI Archipelago

This guide is meant to help you get up and running with Civilization VI in Archipelago. Note that this requires you to have both Rise & Fall and Gathering Storm installed. This will not work unless both of those DLCs are enabled.

## Requirements

The following are required in order to play Civ VI in Archipelago:

- Windows OS (Firaxis does not support the necessary tooling for Mac, or Linux)

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.5 or higher.

- The latest version of the [Civ VI AP Mod](https://github.com/hesto2/civilization_archipelago_mod/releases/latest).

## Enabling the tuner

Depending on how you installed Civ 6 you will have to navigate to one of the following:

- `YOUR_USER/Documents/My Games/Sid Meier's Civilization VI/AppOptions.txt`
- `YOUR_USER/AppData/Local/Firaxis Games/Sid Meier's Civilization VI/AppOptions.txt`

Once you have located your `AppOptions.txt`, do a search for `Enable FireTuner`. Set `EnableTuner` to `1` instead of `0`. **NOTE**: While this is active, achievements will be disabled.

## Mod Installation

1. Download and unzip the latest release of the mod from [GitHub](https://github.com/hesto2/civilization_archipelago_mod/releases/latest).

2. Copy the folder containing the mod files to your Civ VI mods folder. On Windows, this is usually located at `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods`.

3. After the Archipelago host generates a game, you should be given a `.apcivvi` file. Associate the file with the Archipelago Launcher and double click it.

4. Copy the contents of the new folder it generates (it will have the same name as the `.apcivvi` file) into your Civilization VI Archipelago Mod folder.

5. Your finished mod folder should look something like this:

- Civ VI Mods Directory
  - civilization_archipelago_mod
    - NewItems.xml
    - InitOptions.lua
    - Archipelago.modinfo
    - All the other mod files, etc.

## Configuring your game

When configuring your game, make sure to start the game in the Ancient Era and leave all settings related to starting technologies and civics as the defaults. Other than that, configure difficulty, AI, etc. as you normally would.

## Troubleshooting

- If you are getting an error: "The remote computer refused the network connection", or something else related to the client (or tuner) not being able to connect, it likely indicates the tuner is not actually enabled. One simple way to verify that it is enabled is, after completing the setup steps, go to Main Menu &rarr; Options &rarr; Look for an option named "Tuner" and verify it is set to "Enabled"

- If your game gets in a state where someone has sent you items or you have sent locations but these are not correctly sent to the multiworld, you can run `/resync` from the Civ 6 client. This may take up to a minute depending on how many items there are.
