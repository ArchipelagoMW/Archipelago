# Zillion Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Make sure to check the box for `Zillion Client - Zillion Patch Setup`

- RetroArch 1.10.3 or newer from: [RetroArch Website](https://retroarch.com?page=platforms).

- Your legally obtained Zillion ROM file, named `Zillion (UE) [!].sms`

## Installation Procedures

### RetroArch

RetroArch 1.9.x will not work, as it is older than 1.10.3.

1. Enter the RetroArch main menu screen.
2. Go to Main Menu --> Online Updater --> Core Downloader. Scroll down and install one of these cores:
   - "Sega - MS/GG (SMS Plus GX)"
   - "Sega - MS/GG/MD/CD (Genesis Plus GX)
3. Go to Settings --> User Interface. Set "Show Advanced Settings" to ON.
4. Go to Settings --> Network. Set "Network Commands" to ON. (It is found below Request Device 16.) Leave the default
   Network Command Port at 55355.

![Screenshot of Network Commands setting](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)

### Linux Setup

Put your Zillion ROM file in the Archipelago directory in your home directory.

### Windows Setup

1. During the installation of Archipelago, install the Zillion Client. If you did not do this,
   or you are on an older version, you may run the installer again to install the Zillion Client.
2. During setup, you will be asked to locate your base ROM file. This is the Zillion ROM file mentioned above in Required Software.

---
# Play

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The [player settings page](/games/Zillion/player-settings) on the website allows you to configure your personal settings and export a config file from
them.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the [YAML Validator page](/check).

## Generating a Single-Player Game

1. Navigate to the [player settings page](/games/Zillion/player-settings), configure your options, and click the "Generate Game" button.
2. A "Seed Info" page will appear.
3. Click the "Create New Room" link.
4. A server page will appear. Download your patch file from this page.
5. Patch your ROM file.
    - Linux
       - In the launcher, choose "Open Patch" and select your patch file.
    - Windows
       - Double-click on your patch file.
   The Zillion Client will launch automatically, and create your ROM in the location of the patch file.
6. Open the ROM in RetroArch using the core "SMS Plus GX" or "Genesis Plus GX".
    - For a single player game, any emulator (or a Sega Master System) can be used, but there are additional features with RetroArch and the Zillion Client.
       - If you press reset or restore a save state and return to the surface in the game, the Zillion Client will keep open all the doors that you have opened.

## Joining a MultiWorld Game

1. Provide your config (yaml) file to the host and obtain your patch file.
    - When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done, the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch files. Your patch file should have a `.apzl` extension.
       - If you activate the "room generation" option in your config (yaml), you might want to tell your host that the generation will take longer than normal. It takes approximately 20 seconds longer for each Zillion player that enables this option.
2. Create your ROM.
    - Linux
       - In the Archipelago Launcher, choose "Open Patch" and select your `.apzl` patch file.
    - Windows
       - Put your patch file on your desktop or somewhere convenient, and double click it.
    - This should automatically launch the client, and will also create your ROM in the same place as your patch file.
3. Connect to the client.
    - Use RetroArch to open the ROM that was generated.
    - Be sure to select the **SMS Plus GX** core or the **Genesis Plus GX** core. These cores will allow external tools to read RAM data.
4. Connect to the Archipelago Server.
    - The patch file which launched your client should have automatically connected you to the AP Server. There are a few reasons this may not happen however, including if the game is hosted on the website but was generated elsewhere. If the client window shows "Server Status: Not Connected", simply ask the host for the address of the server, and copy/paste it into the "Server" input field then press enter.
    - The client will attempt to reconnect to the new server address, and should momentarily show "Server Status: Connected".
5. Play the game.
    - When the client shows both Game and Server as connected, you're ready to begin playing. Congratulations on successfully joining a multiworld game!

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the [Generation page](/generate).
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, a "Seed Info" page will appear.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
