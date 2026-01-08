# Super Smash Bros. Melee Archipelago Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).


- Dolphin    
- A legally obtained ISO of Super Smash Bros. Melee, Revision 2, USA release.

## Installation Procedures

### Windows Setup

1. Download and install Archipelago from the link above, making sure to install the most recent version.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whomever is hosting. Once that is done,
the room will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.xml` extension.

In Dolphin, Melee should be located in the Games list in the main window. Select the game with right click, and select "Start with Riivolution Patches"
In this menu, use "Open Riivolution XML" and select your patch file. For convenience, you can place the patch in Dolphin Emulator/Load/Riivolution, as it will automatically open this folder when selecting a patch.
You should see a mod labeled the "SSBM Archipelago Mod", some data about the multiworld, and it should be enabled. Click Start.
If it is your first time launching this patch, it should prompt you to make a new save file. You are now playing successfully.

NOTE: Different seeds will have different save files, but not different savestates.

### Connect to the client
Launch the Super Smash Bros. Melee Client from the Archipelago Launcher. If your game is running from the previous step, it should automatically connect.
Then, input and connect to your multiworld room.



### Connect to the Archipelago Server

The patch file which launched your client should have automatically connected you to the AP Server. There are a few
reasons this may not happen however, including if the game is hosted on the website but was generated elsewhere. If the
client window shows "Server Status: Not Connected", simply ask the host for the address of the server, and copy/paste it
into the "Server" input field then press enter.

The client will attempt to reconnect to the new server address, and should momentarily show "Server Status: Connected".

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
