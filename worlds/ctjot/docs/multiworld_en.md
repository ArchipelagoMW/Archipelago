# Chrono Trigger Jets of Time Multiworld Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). 
- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of connecting to SNI
      ([snes9x rr](https://github.com/gocha/snes9x-rr/releases),
       [BizHawk](http://tasvideos.org/BizHawk.html), or
       [RetroArch](https://retroarch.com?page=platforms) 1.10.1 or newer). Or,
    - An SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), or other compatible hardware. **note: 
modded SNES minis are currently not supported by SNI**
- Your US Chrono Trigger SNES ROM.

## Installation Procedures

1. Download and install SNIClient from the link above, making sure to install the most recent version.
   **The installer file is located in the assets section at the bottom of the version information**.

2. If you are using an emulator, you should assign your Lua capable emulator as your default program for launching ROM
   files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .sfc files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for your emulator's `.exe` file and click **Open**. This file should be located inside the folder you
       extracted in step one.

## Create a Config (.yaml) File and ROM (.sfc)

### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

### Where do I get the config and ROM files?

Unlike most Archipelago games, Chrono Trigger: Jets of Time config files are generated with the  
[CTJoT multiworld randomizer site](https://multiworld.ctjot.com/options).  

To generate a ROM/yaml pair:

  - Select the desired settings on the web generator
  - Enter a player name in the "Generate Game" section
  - Click the "Generate Seed" button to create the seed.  This will bring you to the download page
  - Optionally, select any cosmetic/personalization options you want for your game
  - Select your Chrono Trigger ROM file (.sfc file)
  - Download the seed and yaml files

The yaml file will be used by the person generating/hosting your session and the ROM is your patched game.

The ROM and yaml files form a pair that must be used together.  Each time you join a new multiworld session you 
will need to generate another ROM and yaml from the web generator.

## Joining a MultiWorld Game

Use the previous steps to create your config and ROM files.  You will need to provide the .yaml file
to the host.

### Running the Client
