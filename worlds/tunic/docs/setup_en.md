# TUNIC Setup Guide

## Required Software

- [TUNIC](https://tunicgame.com/) for PC (Steam Deck also supported)
- [TUNIC Randomizer Mod](https://github.com/silent-destroyer/tunic-randomizer/releases/latest)
- [BepInEx 6.0.0-pre.1 (Unity IL2CPP x64)](https://github.com/BepInEx/BepInEx/releases/tag/v6.0.0-pre.1)

## Optional Software
- [TUNIC Randomizer Map Tracker](https://github.com/SapphireSapphic/TunicTracker/releases/latest) 
  - Requires [PopTracker](https://github.com/black-sliver/PopTracker/releases)
- [TUNIC Randomizer Item Auto-tracker](https://github.com/radicoon/tunic-rando-tracker/releases/latest)
- [Archipelago Text Client](https://github.com/ArchipelagoMW/Archipelago/releases/latest)

## Installation

### Find Your Relevant Game Directories

Find your TUNIC game installation directory:

- **Steam**: Right click TUNIC in your Steam Library, then *Manage → Browse local files*.<br>
  - **Steam Deck**: Hold down the power button, tap "Switch to Desktop", then launch Steam from Desktop Mode to access the above option.
- **PC Game Pass**: In the Xbox PC app, go to the TUNIC game page from your library, click the [...] button next to "Play", then 
*Manage → Files → Browse...*<br>
- **Other platforms**: Follow a similar pattern of steps as above to locate your specific game directory.

### Install BepInEx

BepInEx is a general purpose framework for modding Unity games, and is used to run the TUNIC Randomizer.

Download [BepInEx 6.0.0-pre.1 (Unity IL2CPP x64)](https://github.com/BepInEx/BepInEx/releases/tag/v6.0.0-pre.1).

If playing on Steam Deck, follow this [guide to set up BepInEx via Proton](https://docs.bepinex.dev/articles/advanced/proton_wine.html).

If playing on Linux, you may be able to add `WINEDLLOVERRIDES="winhttp=n,b" %command%` to your Steam launch options. If this does not work, follow the guide for Steam Deck above.

Extract the contents of the BepInEx .zip file into your TUNIC game directory:<br>
- **Steam**: Steam\steamapps\common\TUNIC<br>
- **PC Game Pass**: XboxGames\Tunic\Content<br>
- **Other platforms**: Place into the same folder that the Tunic_Data or Secret Legend_Data folder is found.

Launch the game once and close it to finish the BepInEx installation.

### Install The TUNIC Randomizer Mod

Download the latest release of the [TUNIC Randomizer Mod](https://github.com/silent-destroyer/tunic-randomizer/releases/latest).

Extract the contents of the downloaded .zip file, and find the folder labeled `Tunic Randomizer`.

Copy the `Tunic Randomizer` folder into `BepInEx/plugins` in your TUNIC game installation directory. 

The filepath to the mod should look like `BepInEx/plugins/Tunic Randomizer/TunicRandomizer.dll`<br>

Launch the game, and if everything was installed correctly you should see `Randomizer Mod Ver. x.y.z` in the top left corner of the title screen!

## Configure Archipelago Options

### Configure Your YAML File

Visit the [TUNIC options page](/games/TUNIC/player-options) to generate a YAML with your selected options.

### Configure Your Mod Settings
Launch the game, and using the menu on the Title Screen select `Archipelago` under `Randomizer Mode`. 

Click the button labeled `Edit AP Config`, and fill in *Player*, *Hostname*, *Port*, and *Password* (if required) with the correct information for your room.

Once you've input your information, click the `Close` button. If everything was configured properly, you should see `Status: Connected!` and your chosen game options will be shown under `World Settings`.

An error message will display if the game fails to connect to the server.

Be sure to also look at the in-game options menu for a variety of additional settings, such as enemy randomization!
