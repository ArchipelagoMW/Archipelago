# Landstalker Setup Guide

## Required Software

- [Landstalker Archipelago Client](https://github.com/Dinopony/randstalker-archipelago/releases) (only available on Windows)
- [RetroArch](https://retroarch.com?page=platforms) with the Genesis Plus GX core
- Your legally obtained Landstalker US ROM file (which can be acquired on [Steam](https://store.steampowered.com/app/71118/Landstalker_The_Treasures_of_King_Nole/))

## Installation Instructions

- Unzip the Landstalker Archipelago Client archive into its own folder
- Put your Landstalker ROM (`LandStalker_USA.SGD` on the Steam release) inside this folder
- To launch the client, launch `randstalker_archipelago.exe` inside that folder

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The [Player Settings Page](../player-settings) on the website allows you to easily configure your personal settings 
and export a config file from them.

## How-to-play

### Connecting to the Archipelago Server

Once the game has been created, you need to connect to the server using the Landstalker Archipelago Client.

To do so, run `randstalker_archipelago.exe` inside the folder you created while installing the software.
A window will open with a few settings to enter:
- **Input ROM file**: This is the path to your original ROM file for the game. If you are using the Steam release ROM 
  and placed it inside this folder as mentioned above, you don't need to change anything.
- **Output ROM path**: This is where the randomized ROMs will be put. No need to change this unless you want them to be 
  created in a very specific folder
- **Host**: Put the server address and port in this field (e.g. `archipelago.gg:12345`)
- **Slot name**: Put the player name you specified in your YAML config file in this field.
- **Password**: If server has a password, put it there.

Once all those fields were filled appropriately, click on the first "**Connect**" button below to try connecting to the
Archipelago server. 

If it turns green saying "Connected", that's good news! Otherwise, double-check the Host, Slot name and
Password provided above.

### ROM Generation

When you connected to the Archipelago server, the client automatically tried to build a randomized ROM. The console log 
on the right half of the window should have notified you if it succeeded or not. 

If it did, locate the randomized ROM file and open it using Retroarch. 

If it didn't, double-check your **Input ROM file** and **Output ROM path**, then retry building a ROM by clicking on 
the **Rebuild ROM** button.

### Connecting to Retroarch

Now that you're connected to the Archipelago server and have a randomized ROM, all we need is to get the client 
connected to the emulator. This way, the client will be able to see what's happening while you play and give you in-game
the items you have received from other players.

Once you have opened the randomized ROM inside RetroArch, you can click on the second "**Connect**" button below.
This will only work if you have already opened the ROM using the Genesis Plus GX core, since the client will try to hook
on that core's memory.

If this didn't work, try the following:
- ensure you have loaded your ROM inside Retroarch
- ensure you are using the Genesis Plus GX and not another core (e.g. BlastEm will not work)
- try launching the client in Administrator Mode (right click on `randstalker_archipelago.exe`, then `Run as administrator`)
- if all else fails, try using RetroArch 1.9.0 and Genesis Plus GX 1.7.4 (it works on all versions tested so far, but you never know...)

### Play the game

If both indicators are green and show "Connected", you're good to go! Just play the game and enjoy the wonders of 
isometric perspective. 
