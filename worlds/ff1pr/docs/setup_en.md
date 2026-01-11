# Final Fantasy 1 Pixel Remaster Setup Guide

## Required Software

- [Final Fantasy 1 Pixel Remaster](https://finalfantasypixelremaster.square-enix-games.com/en_US/) for PC
- [FF1 Pixel Remaster AP Randomizer Mod](https://github.com/wildham0/FF1PRAP/releases/latest)
- [BepInEx 6.0.0-pre.2 (Unity IL2CPP x64)](https://github.com/BepInEx/BepInEx/releases/tag/v6.0.0-pre.2)

## Optional Software
- [Archipelago Text Client](https://github.com/ArchipelagoMW/Archipelago/releases/latest)

## Installation

### Find Your Relevant Game Directories

Find your FF1 Pixel Remaster game installation directory:

- **Steam**: Right click FF1 Pixel Remaster in your Steam Library, then *Manage → Browse local files*.<br>
- **PC Game Pass**: In the Xbox PC app, go to the FF1 Pixel Remaster game page from your library, click the [...] button next to "Play", then 
*Manage → Files → Browse...*<br>
- **Other platforms**: Follow a similar pattern of steps as above to locate your specific game directory.

### Install BepInEx

BepInEx is a general purpose framework for modding Unity games, and is used to run the TUNIC Randomizer.

Download [BepInEx 6.0.0-pre.2 (Unity IL2CPP x64)](https://github.com/BepInEx/BepInEx/releases/tag/v6.0.0-pre.2).

If playing on Steam Deck, follow this [guide to set up BepInEx via Proton](https://docs.bepinex.dev/articles/advanced/proton_wine.html).

If playing on Linux, you may be able to add `WINEDLLOVERRIDES="winhttp=n,b" %command%` to your Steam launch options. If this does not work, follow the guide for Steam Deck above.

Extract the contents of the BepInEx .zip file into your FF1 Pixel Remaster game directory:<br>
- **Steam**: Steam\steamapps\common\FINAL FANTASY PR<br>
- **PC Game Pass**: XboxGames\FINAL FANTASY PR\Content<br>
- **Other platforms**: Place into the same folder that the FINAL FANTASY_Data folder is found.

Launch the game once and close it to finish the BepInEx installation.

### Install The FF1 Pixel Remaster AP Randomizer Mod

Download the latest release of the [FF1 Pixel Remaster AP Randomizer Mod](https://github.com/wildham0/FF1PRAP/releases/latest).

Extract the contents of the downloaded .zip file, and find the folder labeled `FF1PRAP`.

Copy the `FF1PRAP` folder into `BepInEx/plugins` in your FF1 Pixel Remaster game installation directory. 

The filepath to the mod should look like `BepInEx/plugins/FF1PRAP/FF1PRAP.dll`<br>

Launch the game, and if everything was installed correctly you should see the Settings Window on the left of the title screen!
 
## Configure Archipelago Options

### Configure Your YAML File

Run the Archipelago Launcher and click on `Generate Template Options` to create a template YAML file in your `Players\Templates` directory or use the included template with the latest release of the FF1 Pixel Remaster AP Mod.

### Configure Your Mod Settings
Launch the game, and using the menu on the Title Screen select `Archipelago` in the `Game Mode` dropdown. 

Click the button labeled `Edit Connection Info`, and fill in *Player*, *Hostname*, *Port*, and *Password* (if required) with the correct information for your room.

Once you've input your information, click the `Connect` button. If everything was configured properly, you should see `Status: Connected!`.

An error message will display if the game fails to connect to the server.