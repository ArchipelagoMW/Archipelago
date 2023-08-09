# TUNIC Setup Guide

## Installation

### Required Software

- [TUNIC](https://tunicgame.com/) for PC (Steam Deck also supported)
- [BepInEx](https://builds.bepinex.dev/projects/bepinex_be/572/BepInEx_UnityIL2CPP_x64_9c2b17f_6.0.0-be.572.zip)
- [TUNIC Randomizer Archipelago Mod](https://github.com/silent-destroyer/tunic-randomizer-archipelago/releases/latest)

### Optional Software
- TUNIC Randomizer Map Tracker (Available via EmoTracker)
- [TUNIC Randomizer Item Auto-tracker](https://github.com/radicoon/tunic-rando-tracker/releases/latest)

### Find Your Relevant Game Directories

Find your TUNIC game installation directory:

- **Steam**: Right click TUNIC in your Steam Library, then *Manage → Browse local files*<br>
- **PC Game Pass**: In the Xbox PC app, go to the TUNIC game page from your library, click the [...] button next to "Play", then 
*Manage → Files → Browse...*<br>
**Other platforms**: Follow a similar pattern of steps as above to locate your specific game directory.

Find your TUNIC AppData directory by copying and pasting this path into file explorer: `%localappdata%low\Andrew Shouldice\Secret Legend`<br>
On Steam Deck, the AppData folder is located at `/home/deck/.local/share/Steam/steamapps/compatdata/553420/pfx/drive_c/users/steamuser/AppData/LocalLow/Andrew Shouldice/Secret Legend`

### Install BepInEx

BepInEx is a general purpose framework for modding Unity games, and is used by the Tunic Randomizer.

Download this version of [BepInEx](https://builds.bepinex.dev/projects/bepinex_be/572/BepInEx_UnityIL2CPP_x64_9c2b17f_6.0.0-be.572.zip).

If playing on Steam Deck, follow this [guide to set up BepInEx via Proton](https://docs.bepinex.dev/articles/advanced/proton_wine.html).

Extract the contents of the BepInEx .zip file into your TUNIC game directory:<br>
- **Steam**: Steam\steamapps\common\TUNIC<br>
- **PC Game Pass**: XboxGames\Tunic\Content<br>
- **Other platforms**: Place into the same folder that the Tunic_Data/Secret Legend_Data folder is found.

Launch the game once and close it to finish the BepInEx installation.

### Install The Tunic Randomizer Archipelago Client Mod

Download the latest release of the [Tunic Randomizer Archipelago Mod](https://github.com/silent-destroyer/tunic-randomizer-archipelago/releases/latest).

The downloaded .zip will contain two folders: `plugins` and `Randomizer`.

Copy the `plugins` folder into the `BepInEx` folder of your TUNIC game installation directory.<br>
Copy the `Randomizer` folder into your TUNIC AppData directory.

Launch the game, and if everything was installed correctly you should see `Randomizer + Archipelago Mod Ver. x.y.z` in the top left corner of the title screen!

## Configure Archipelago Settings

### Configure Your YAML File

Visit the [TUNIC settings page](/games/Tunic/player-settings) to generate a YAML with your selected settings.

### Configure Your Mod Settings
In the `Randomizer` folder you downloaded earlier, there will be a file called `ArchipelagoSettings.json`. 
Open this file in a text editor and look for `ConnectionSettings` at the top. Fill in *Player*, *Hostname*, *Port*, and *Password* with the correct
information for your room. The rest of the settings in this file can be viewed and toggled through the in-game options menu.

Once your player settings have been saved, launch the game. The game should automatically connect to the room when you reach the title screen 
(or, if the game is already running, press *Reload Settings* and then *Connect* on the title screen). An error message will display if
the game fails to connect to the server.

Be sure to also look at the in-game options menu for a variety of additional settings, such as enemy randomization!
