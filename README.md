# [Archipelago](https://archipelago.gg) ![Discord Shield](https://discordapp.com/api/guilds/731205301247803413/widget.png?style=shield) | [Install](https://github.com/ArchipelagoMW/Archipelago/releases)

## Symphony of the Night
Symphony of the Night is a metroidvania from playstation 1

### Requirements
* Arquipelago 0.5.1 or later
* Bizhawk 2.7 or 2.8 or 2.9.1

### Instalation
Download the last apworld version from releases page.
Download error recalc software .exe for windows platform and no extension for linux platform and place in your 'lib' folder on archipelago main directory. Default is C:\ProgramData\Archipelago\lib
Run ArchipelagoLauncher and choose Install APWorld, select your downloaded sotn.apworld, restart if asked.

### Playing
## Generate
Place your options file along with all others players yalm in your players folder. You can get an default yalm for SOTN on ArchipelagoLauncher and choose Generate Template Options.
Run ArquipelagoGenerate, your seed will be on output directory
Since this is an unsupported apworld is required to generate locally. You can open the zipped seed to get the patches for all unsuported games SOTN extension is .apsotn. You can send the file to Archipelago website to host.
## Running
Select Open Patch from ArchipelagoLauncher. PAY ATTENTION TO FILE DIALOG. During the process will be asked for Castlevania - Symphony of the Night (USA) (Track 1).bin or ROM File and Castlevania - Symphony of the Night (USA) (Track 2).bin or Audio File if error recalc software isn't found on lib folder you will be asked for an Error recalc binary during this process. You could be asked for a bizhawk binary also. You might get No handler found during Sony and Playstation logos. Don't forget to enter your server address and click connect after getting Symphony of the Night handler.
If you prefer to open manually, run the game with AP_SEED_PLAYER.cue, chooose Bizhawk client from ArchipelagoLauncher, on Bizhawk choose Tools->Lua Console, on Lua console choose Script->Open script and select connector_bizhawk_generic.lua from data\lua directory. Don't forget to enter your server address and click connect after getting Symphony of the Night handler.
## Customize
You can tweak some option in your default yalm:
# Tweaks
* open_no4: Open the back door of Underground Caverns, after entering Alchemy Laboratory.
* early_open_no4: Open the back door from the start. You gonna skip Death after entering Underground Caverns.
* open_are: Open Colosseum back door.
* extension: Choose which location will be added to the pool.
* randomize_items: Will randomize items not in the seed pool.
# Quality of Life
* infinite_wing: Your bat wing smash spell will remain.
* extra_pool: Will try to add more powerful items to the pool.

![map_normal](https://github.com/user-attachments/assets/0c523853-4244-4d96-be82-05b981ec4739)
![map_inverted](https://github.com/user-attachments/assets/04c78e2d-ea8b-46da-88cf-45c0ba860c01)
![teste](https://github.com/user-attachments/assets/89bc0ec7-3231-47bf-b086-d11f474004e6)

## The game
Be careful to not load the wrong save file. You can't receive items with the pause screen open.
Your received items will appear on the lower left corner of the screen.
Items on breakable walls could be an empty hand, that means is an offworld item and will be send as soon you break the wall. Items for your game would fall in the floor if you did not loot before it vanish you lost it.
Items on the floor could be your item or a bag of gold. The color of the bag is red for useful items, yellow for filler ones and blue for progression.
