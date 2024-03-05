# TUNIC Setup Guide

## Installation

### Required Software

- [TUNIC](https://tunicgame.com/) for PC (Steam Deck also supported)
- [BepInEx](https://builds.bepinex.dev/projects/bepinex_be/572/BepInEx_UnityIL2CPP_x64_9c2b17f_6.0.0-be.572.zip)
- [TUNIC Randomizer Archipelago Mod](https://github.com/silent-destroyer/tunic-randomizer-archipelago/releases/latest)

### Optional Software
- [TUNIC Randomizer Map Tracker](https://github.com/SapphireSapphic/TunicTracker/releases/latest) (For use with EmoTracker/PopTracker)
- [TUNIC Randomizer Item Auto-tracker](https://github.com/radicoon/tunic-rando-tracker/releases/latest)

### Find Your Relevant Game Directories

Find your TUNIC game installation directory:

- **Steam**: Right click TUNIC in your Steam Library, then *Manage → Browse local files*.<br>
  - **Steam Deck**: Hold down the power button, tap "Switch to Desktop", then launch Steam from Desktop Mode to access the above option.
- **PC Game Pass**: In the Xbox PC app, go to the TUNIC game page from your library, click the [...] button next to "Play", then 
*Manage → Files → Browse...*<br>
- **Other platforms**: Follow a similar pattern of steps as above to locate your specific game directory.

### Install BepInEx

BepInEx is a general purpose framework for modding Unity games, and is used by the TUNIC Randomizer.

Download [BepInEx](https://builds.bepinex.dev/projects/bepinex_be/572/BepInEx_UnityIL2CPP_x64_9c2b17f_6.0.0-be.572.zip).

If playing on Steam Deck, follow this [guide to set up BepInEx via Proton](https://docs.bepinex.dev/articles/advanced/proton_wine.html).

Extract the contents of the BepInEx .zip file into your TUNIC game directory:<br>
- **Steam**: Steam\steamapps\common\TUNIC<br>
- **PC Game Pass**: XboxGames\Tunic\Content<br>
- **Other platforms**: Place into the same folder that the Tunic_Data/Secret Legend_Data folder is found.

Launch the game once and close it to finish the BepInEx installation.

### Install The TUNIC Randomizer Archipelago Client Mod

Download the latest release of the [TUNIC Randomizer Archipelago Mod](https://github.com/silent-destroyer/tunic-randomizer-archipelago/releases/latest).

The downloaded .zip will contain a folder called `Tunic Archipelago`.

Copy the `Tunic Archipelago` folder into `BepInEx/plugins` in your TUNIC game installation directory. 
The filepath to the mod should look like `BepInEx/plugins/Tunic Archipelago/TunicArchipelago.dll`<br>

Launch the game, and if everything was installed correctly you should see `Randomizer + Archipelago Mod Ver. x.y.z` in the top left corner of the title screen!

## Configure Archipelago Options

### Configure Your YAML File

Visit the [TUNIC options page](/games/Tunic/player-options) to generate a YAML with your selected options.

### Configure Your Mod Settings
Launch the game and click the button labeled `Open AP Config` on the Title Screen.
In the menu that opens, fill in *Player*, *Hostname*, *Port*, and *Password* (if required) with the correct information for your room.

Once you've input your information, click on Close. If everything was configured properly, you should see `Status: Connected!` and your chosen game options will be shown under `World Settings`.

An error message will display if the game fails to connect to the server.

Be sure to also look at the in-game options menu for a variety of additional settings, such as enemy randomization!
