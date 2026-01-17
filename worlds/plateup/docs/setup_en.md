# PlateUp! Randomizer Setup Guide

## Required Software

- [Archipelago](github.com/ArchipelagoMW/Archipelago/releases/latest)
- [The PlateUp apworld](https://github.com/CazIsABoi/Archipelago/releases), 
  if not bundled with your version of Archipelago
- [PlateUp Archipelago Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=3484431423) 
  available in the Steam workshop as "Archipelago for PlateUp!"
- Be sure to also install any mods that are listed as dependencies. Steam will ask.

## How to play

First, you need a room to connect to. For this, you or someone you know has to generate a game.  
This will not be explained here,
but you can check the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup_en#generating-a-game).

You also need to have [Archipelago](github.com/ArchipelagoMW/Archipelago/releases/latest) installed
and the [The APQuest apworld](https://github.com/CazIsABoi/Archipelago/releases) installed into Archipelago.

## How to install

1. [Recommended] Subscribe to the mod on the Steam Workshop
2. Via GitHub
   1. Download the zip file
   2. Put the unzipped mod folder in the Mods folder (Windows: C:\Program Files (x86)\Steam\steamapps\common\PlateUp\PlateUp\Mods)

## How to connect

After installing the mod, launch PlateUp!. After going into the HQ (Lobby), you can open the menu and click through 
the menu to find the "PlateupAP" menu: Options > PreferenceSystem > PlateupAP

From here, you can use the "Create Config" option to generate a file where you can enter your room's connection info.
This creates a file named `archipelago_config.json`

- Windows: You can find the file by pressing `Windows` + `R` and pasting in the following path: 
   `%AppData%\..\LocalLow\It's Happening\PlateUp`
- Linux and Others: Starting from your Steam install folder, it may be located in a path like: 
    `./Steam/steamapps/compatdata/1599600/pfx/drive_c/users/steamuser/AppData/LocalLow/It%27s%20Happening/PlateUp/PlateUpAPConfig/`

Fill this file out with your room's info. If you don't have a username and/or password, then you can leave these fields 
alone. Save the file and return to the game. Now you can click "Connect" to attempt to connect to the server.