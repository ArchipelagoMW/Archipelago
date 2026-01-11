# The Legend of Zelda: Oracle of Seasons Setup Guide

## Required Software

- [Oracle of Seasons .apworld](https://github.com/Dinopony/ArchipelagoOoS/releases/latest)
- [Bizhawk 2.10 (x64)](https://tasvideos.org/BizHawk/ReleaseHistory)
- Your legally obtained Oracle of Seasons US ROM file

## Installation Instructions

1. Put your **Oracle of Seasons US ROM** inside your Archipelago install folder (named "Legend of Zelda, The - Oracle of Seasons (USA).gbc")
2. Download the **Oracle of Seasons .apworld file** and double-click it to install it the "custom_worlds/" subdirectory of your Archipelago install directory
3. Generate a seed using your .yaml settings file (see below if you don't know how to get the template)
4. Download the .apoos patch file that was built by the server while generating, this will be used to generate your modified ROM
5. Open this patch file using the Archipelago Launcher
6. If everything went fine, the patched ROM was built in the same directory as the .apoos file, and both Bizhawk and the client launched
7. Connect the Client to the AP Server of your choice, and you can start playing!

## Create a Config (.yaml) File

To get the template YAML file:
1. Install the .apworld file as instructed above
2. If Archipelago Launcher was running on your computer, close it 
3. Run the Archipelago launcher
4. Click on "Generate Template Settings"
5. It should open a directory in file explorer, pick the file named `The Legend of Zelda - Oracle of Seasons.yaml`

## Setting up cosmetic options (sprite, palette...)

Inside the "host.yaml" configuration file that can be found in the Archipelago install folder, you can configure a few cosmetic options for the game.
Under the "tloz_oos_options" item, you can find the following options:
- "**character_sprite**", used to change the sprite for your character
- "**character_palette**", used to change the color of your character
- "**heart_beep_interval**", used to alter the speed of the beeping sound when low on health

Most of those settings are pretty self-explanatory, but sprites need some extra information.
Sprites are files with the ".bin" extension which needs to be placed inside the "data/sprites/oos_ooa/" subfolder inside your Archipelago install.
You need to download the sprites you want to use from [that repository](https://github.com/Dinopony/oracles-sprites/), and place them inside the folder mentioned above.
This means if you placed a file called "goron.bin" in that folder, you then just have to set "goron" as "character_sprite" inside your host.yaml file before patching.
Once this is done, all subsequent patched ROMs will use those cosmetic settings, but you can easily change them by just editing that file again.
