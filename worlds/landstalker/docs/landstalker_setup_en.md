# Landstalker Setup Guide

## Required Software

- [Landstalker Archipelago Client](https://github.com/Dinopony/randstalker-archipelago/releases) (only available on Windows)
- A compatible emulator to run the game
  - [RetroArch](https://retroarch.com?page=platforms) with the Genesis Plus GX core
  - [Bizhawk 2.9.1 (x64)](https://tasvideos.org/BizHawk/ReleaseHistory) with the Genesis Plus GX core
- A Landstalker US ROM file dumped from the original cartridge

## Installation Instructions

- Unzip the Landstalker Archipelago Client archive into its own folder
- Put your Landstalker ROM (`LandStalker_USA.SGD` on the Steam release) inside this folder
- To launch the client, launch `randstalker_archipelago.exe` inside that folder

Be aware that you might get antivirus warnings about the client program because one of its main features is to spy
on another process's memory (your emulator). This is something antiviruses obviously dislike, and sometimes mistake
for malicious software. 

If you're not trusting the program, you can check its [source code](https://github.com/Dinopony/randstalker-archipelago/)
or test it on a service like Virustotal.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?


The [Player Options Page](/games/Landstalker%20-%20The%20Treasures%20of%20King%20Nole/player-options) on the website allows
you to easily configure your personal options. 


## How-to-play

### Connecting to the Archipelago Server

Once the game has been created, you need to connect to the server using the Landstalker Archipelago Client.

To do so, run `randstalker_archipelago.exe` inside the folder you created while installing the software.

A window will open with a few settings to enter:
- **Host**: Put the server address and port in this field (e.g. `archipelago.gg:12345`)
- **Slot name**: Put the player name you specified in your YAML config file in this field.
- **Password**: If the server has a password, put it there.

![Landstalker Archipelago Client user interface](/static/generated/docs/Landstalker%20-%20The%20Treasures%20of%20King%20Nole/ls_guide_ap.png)

Once all those fields were filled appropriately, click on the `Connect to Archipelago` button below to try connecting to
the Archipelago server.

If this didn't work, double-check your credentials. An error message should be displayed on the console log to the 
right that might help you find the cause of the issue.

### ROM Generation

When you connected to the Archipelago server, the client fetched all the required data from the server to be able to
build a randomized ROM.

You should see a window with settings to fill:
- **Input ROM file**: This is the path to your original ROM file for the game. If you are using the Steam release ROM 
  and placed it inside the client's folder as mentioned above, you don't need to change anything.
- **Output ROM directory**: This is where the randomized ROMs will be put. No need to change this unless you want them 
  to be created in a very specific folder.

![Landstalker Archipelago Client user interface](/static/generated/docs/Landstalker%20-%20The%20Treasures%20of%20King%20Nole/ls_guide_rom.png)

There also a few cosmetic options you can fill before clicking the `Build ROM` button which should create your 
randomized seed if everything went right.

If it didn't, double-check your `Input ROM file` and `Output ROM path`, then retry building the ROM by clicking 
the same button again.

### Connecting to the emulator

Now that you're connected to the Archipelago server and have a randomized ROM, all we need is to get the client 
connected to the emulator. This way, the client will be able to see what's happening while you play and give you in-game
the items you have received from other players.

You should see the following window:

![Landstalker Archipelago Client user interface](/static/generated/docs/Landstalker%20-%20The%20Treasures%20of%20King%20Nole/ls_guide_emu.png)

As written, you have to open the newly generated ROM inside either Retroarch or Bizhawk using the Genesis Plus GX core. 
Be careful to select that core, because any other core (e.g. BlastEm) won't work.

The easiest way to do so is to:
- open the emu of your choice
- if you're using Retroarch and it's your first time, download the Genesis Plus GX core through Retroarch user interface
- click the `Show ROM file in explorer` button
- drag-and-drop the shown ROM file on the emulator window
- press Start to reach file select screen (to ensure game RAM is properly set-up)

Then, you can click on the `Connect to emulator` button below and it should work.

If this didn't work, try the following:
- ensure you have loaded your ROM and reached the save select screen
- ensure you are using Genesis Plus GX and not another core (e.g. BlastEm will not work)
- try launching the client in Administrator Mode (right-click on `randstalker_archipelago.exe`, then 
 `Run as administrator`)
- if all else fails, try using one of those specific emulator versions:
  - RetroArch 1.9.0 and Genesis Plus GX 1.7.4
  - Bizhawk 2.9.1 (x64)

### Play the game

If all indicators are green and show "Connected," you're good to go! Play the game and enjoy the wonders of isometric 
perspective. 

The client is packaged with both an **automatic item tracker** and an **automatic map tracker** for your comfort. 

If you don't know all checks in the game, don't be afraid: you can click the `Where is it?` button that will show 
you a screenshot of where the location actually is.

![Landstalker Archipelago Client user interface](/static/generated/docs/Landstalker%20-%20The%20Treasures%20of%20King%20Nole/ls_guide_client.png)

Have fun!