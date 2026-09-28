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
- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases/latest)

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

Download [BepInEx 6.0.0-pre.1 (Unity IL2CPP x64)](https://github.com/BepInEx/BepInEx/releases/download/v6.0.0-pre.1/BepInEx_UnityIL2CPP_x64_6.0.0-pre.1.zip).

If playing on Steam Deck, follow this [guide to set up BepInEx via Proton](https://docs.bepinex.dev/articles/advanced/proton_wine.html).

If playing on Linux, you may be able to add `WINEDLLOVERRIDES="winhttp=n,b" %command%` to your Steam launch options. If this does not work, follow the guide for Steam Deck above.

Extract the contents of the BepInEx .zip file **directly** into your TUNIC game directory:<br>
- **Steam**: Steam\steamapps\common\TUNIC<br>
- **PC Game Pass**: XboxGames\Tunic\Content<br>
- **Other platforms**: Extract to the folder where a `Tunic_Data` or `Secret Legend_Data` folder is found.

Your TUNIC folder should now look close to this:
- TUNIC/
  - BepInEx/
  - mono/
  - Tunic_Data/
  - baselib.dll
  - changelog.txt
  - doorstop_config.ini
  - GameAssembly.dll
  - Tunic.exe
  - UnityCrashHandler64.exe
  - UnityPlayer.dll
  - winhttp.dll

Launch the game once and close it to finish the BepInEx installation.

You should now have a `plugins` folder in your `BepInEx` folder along with several other new folders. 

If you do not have a `plugins` folder, **do not** manually create one. See the [troubleshooting](#troubleshooting) section below.

### Install The TUNIC Randomizer Mod

Download the latest release of the [TUNIC Randomizer Mod](https://github.com/silent-destroyer/tunic-randomizer/releases/latest).

Extract the contents of the downloaded .zip file, and find the folder labeled `Tunic Randomizer`.

Copy the `Tunic Randomizer` folder into `BepInEx/plugins` in your TUNIC game installation directory.

The filepath to the mod should look like `<TUNIC Game Folder>/BepInEx/plugins/Tunic Randomizer/TunicRandomizer.dll`<br>

Launch the game, and if everything was installed correctly you should see `Randomizer Mod Ver. x.y.z` in the top left corner of the title screen!

If you do not see the Randomizer interface, see the [troubleshooting](#troubleshooting) section below.

## Configure Archipelago Options

### Configure Your YAML File

Visit the [TUNIC options page](/games/TUNIC/player-options) to generate a YAML with your selected options.

### Configure Your Mod Settings
Launch the game, and using the menu on the Title Screen select `Archipelago` under `Randomizer Mode`. 

Click the button labeled `Edit Connection Info`, and fill in *Player*, *Hostname*, *Port*, and *Password* (if required) with the correct information for your room.

Once you've input your information, click the `Close Connection Info` button. If everything was configured properly, you should see `Status: Connected!` and your chosen game options will be shown under `World Settings`.

An error message will display if the game fails to connect to the server.

Death Link and Trap Link are supported and can be enabled from the main menu. A variety of additional features can also be enabled from the main menu, such as randomized enemies and customized fox colors.

## Troubleshooting

### BepInEx did not create a plugins folder.
- Make sure you downloaded the correct version of BepInEx: [BepInEx UnityIL2CPP x64 6.0.0-pre.1](https://github.com/BepInEx/BepInEx/releases/download/v6.0.0-pre.1/BepInEx_UnityIL2CPP_x64_6.0.0-pre.1.zip)
  - Newer versions of BepInEx 6.0.0 will **not** work, nor will **any** version of BepInEx 5.
- Make sure you extracted the BepInEx files directly into your TUNIC folder and not into their own folder within the TUNIC folder. Your TUNIC folder should look **exactly** as described in the [Install BepInEx](#install-bepinex) section.
- Check if there is a `preloader_<timestamp>.log` in your TUNIC folder. This indicates that BepInEx could not finish installing properly, and is commonly due to it being blocked by another process on your PC. Try disabling any antivirus or anti-cheat software you have before trying again.