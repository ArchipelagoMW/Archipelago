# Setup Guide for A Hat in Time in Archipelago

## Required Software
- [Steam release of A Hat in Time](https://store.steampowered.com/app/253230/A_Hat_in_Time/)

- [Archipelago Workshop Mod for A Hat in Time](https://steamcommunity.com/sharedfiles/filedetails/?id=3026842601)


## Optional Software
- [A Hat in Time Archipelago Map Tracker](https://github.com/Mysteryem/ahit-poptracker/releases), for use with [PopTracker](https://github.com/black-sliver/PopTracker/releases)


## Instructions

1. **BACK UP YOUR SAVE FILES IN YOUR MAIN INSTALL IF YOU CARE ABOUT THEM!!!**  
   Go to `steamapps/common/HatinTime/HatinTimeGame/SaveData/` and copy everything inside that folder over to a safe place.
   **This is important! Changing the game version CAN and WILL break your existing save files!!!**


2. In your Steam library, right-click on **A Hat in Time** in the list of games and click on **Properties**.


3. Click the **Betas** tab. In the **Beta Participation** dropdown, select `tcplink`.  
   While it downloads, you can subscribe to the [Archipelago workshop mod](https://steamcommunity.com/sharedfiles/filedetails/?id=3026842601).


4. Once the game finishes downloading, start it up.  
   In Game Settings, make sure **Enable Developer Console** is checked.


5. You should now be good to go. See below for more details on how to use the mod and connect to an Archipelago game.


## Connecting to the Archipelago server

To connect to the multiworld server, simply run the **Archipelago AHIT Client** from the Launcher
and connect it to the Archipelago server. 
The game will connect to the client automatically when you create a new save file.


## Console Commands

Commands will not work on the title screen, you must be in-game to use them. To use console commands, 
make sure ***Enable Developer Console*** is checked in Game Settings and press the tilde key or TAB while in-game.

`ap_say <message>` - Send a chat message to the server. Supports commands, such as `!hint` or `!release`.

`ap_deathlink` - Toggle Death Link.


## FAQ/Common Issues

### The game is crashing on startup repeatedly!
This is a common issue on older versions of the game, caused by the game failing to interface with the Steam Workshop. 
To fix it you can try the following (from least to most effort required)
- Subscribe to any random workshop mod, then unsubscribe from it
- Restart Steam
- Restart your computer
- Delete the game's config directory from the files `steamapps/common/HatinTime/HatinTimeGame/Config` then verify the game files
- Reinstall the game

### Why do relics disappear from the stands in the Spaceship after they're completed?
This is intentional behaviour. Because of how randomizer logic works, there is no way to predict the order that 
a player will place their relics. Since there are a limited amount of relic stands in the Spaceship, relics are removed 
after being completed to allow for the placement of more relics without being potentially locked out. 
The level that the relic set unlocked will stay unlocked.
