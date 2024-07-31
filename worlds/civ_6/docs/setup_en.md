# Setup Guide for Civilization VI Archipelago

This guide is meant to help you get up and running with Civlization VI in your Archipelago run. Note that this requires you to have both Rise & Fall as well as Gathering Storm installed. This will not work unless both of those DLCs are enabled.

## Requirements

The following are required in order to play Civ VI in Archipelago

- Windows OS (Firaxis does not support the necessary tooling for Mac, Linux is yet to bet verified)

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.5 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**

- The latest version of the [Civ VI AP Mod](https://github.com/hesto2/civilization_archipelago_mod).

- Tuner setting enabled so the archipelago client can communicate with the game

## Enabling the tuner
Depending on how you installed Civ 6 you will have to navigate to one of the following:
- `YOUR_USER/Documents/My Games/Sid Meier's Civilization VI/AppOptions.txt`
- `YOUR_USER/AppData/Local/Firaxis Games/Sid Meier's Civilization VI/AppOptions.txt`

Once you have located your `AppOptions.txt`, do a search for `Enable FireTuner`. Set `EnableTuner` to `1` instead of `0`. __NOTE__: While this is active, achievments will be disabled.

## Mod Installation

1. Download and unzip the latest release of the mod from [github](https://github.com/hesto2/civilization_archipelago_mod/releases).

2. Copy the folder containing the mod files to your Civ VI mods folder. On Windows, this is usually located at `C:\Users\YOUR_USER\Documents\My Games\Sid Meier's Civilization VI\Mods`

3. After the Archipelago host generates a game, you should be given another zip file titled `AP-{playername}....zip`. Unzip this and copy all of its contents into your mod folder.

4. Your finished mod folder should look something like this:
- Civ VI Mods Directory
  - civilization_archipelago_mod
    - NewItems.xml
    - InitOptions.lua
    - Archipelago.modinfo
    - All the other mod files, etc.

## Configuring your game

When configuring your game, make sure to start the game in the Ancient Era and leave all settings related to starting technologies and civics as the defaults. Other than that, configure difficulty, AI, etc. as you normally would.

## Troubleshooting

- If you are getting an error: `The remote computer refused the network connection`, or something else related to the client (or tuner) not being able to connect, it likely indicates the tuner is not actually enabled. One simple way to verify that it is enabled is, after completing the setup steps, to go Main Menu -> Options -> Look for an option named "Tuner" and verify it is set to "Enabled"

- If your game gets in a state where someone has sent you items or you have sent locations but these are not correctly replicated to the multiworld, you can run `/resync` from the Civ 6 client. This may take up to a minute depending on how many items there are.