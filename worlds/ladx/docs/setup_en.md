# Links Awakening DX Multiworld Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Make sure to check the box for `Links Awakening DX`
- Software capable of loading and playing GBC ROM files
    - [RetroArch](https://retroarch.com?page=platforms) 1.10.3 or newer.
    - [BizHawk](https://tasvideos.org/BizHawk) 2.8 or newer.
- Your American 1.0 ROM file, probably named `Legend of Zelda, The - Link's Awakening DX (USA, Europe) (SGB Enhanced).gbc`

## Installation Procedures

1. Download and install LinksAwakeningClient from the link above, making sure to install the most recent version.
   **The installer file is located in the assets section at the bottom of the version information**.
    - During setup, you will be asked to locate your base ROM file. This is your Links Awakening DX ROM file.

2. You should assign your emulator as your default program for launching ROM
   files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .gbc files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for your emulator's `.exe` file and click **Open**. This file should be located inside the folder you
       extracted in step one.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

### Where do I get a config file?

The [Player Settings](/games/Links%20Awakening%20DX/player-settings) page on the website allows you to configure
your personal settings and export a config file from them.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the
[YAML Validator](/check) page.

## Generating a Single-Player Game

1. Navigate to the [Player Settings](/games/Links%20Awakening%20DX/player-settings) page, configure your options,
   and click the "Generate Game" button.
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your patch file.
5. Double-click on your patch file, and Links Awakening DX will launch automatically, and create your ROM from the patch file.
6. Since this is a single-player game, you will no longer need the client, so feel free to close it.

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apladx` extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should automatically launch the
client, and will also create your ROM in the same place as your patch file.

### Connect to the client

#### RetroArch 1.10.3 or newer

You only have to do these steps once. Note, RetroArch 1.9.x will not work as it is older than 1.10.3.

1. Enter the RetroArch main menu screen.
2. Go to Settings --> User Interface. Set "Show Advanced Settings" to ON.
3. Go to Settings --> Network. Set "Network Commands" to ON. (It is found below Request Device 16.) Leave the default
   Network Command Port at 55355.

![Screenshot of Network Commands setting](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)
4. Go to Main Menu --> Online Updater --> Core Downloader. Scroll down and select "Nintendo - Gameboy / Color (SameBoy)".

#### BizHawk 2.8 or newer (older versions untested)

1. Load the ROM.
2. Navigate to the folder Archipelago is installed in, then `data/lua`, and drag+drop `connector_ladx_bizhawk.lua` onto
   the main EmuHawk window.
    - You could instead open the Lua Console manually, click `Script` 〉 `Open Script`, and navigate to
      `connector_ladx_bizhawk.lua` with the file picker.
3. Keep the Lua Console open during gameplay (minimizing it is fine!)

### Connect to the Archipelago Server

The patch file which launched your client should have automatically connected you to the AP Server. There are a few
reasons this may not happen, however, including if the game is hosted on the website but was generated elsewhere. If the
client window shows "Server Status: Not Connected", simply ask the host for the address of the server, and copy/paste it
into the "Server" input field then press enter.

The client will attempt to reconnect to the new server address, and should momentarily show "Server Status: Connected".

### Play the game

When the client shows both Retroarch and Server as connected, you're ready to begin playing. Congratulations on
successfully joining a multiworld game! You can execute various commands in your client. For more information regarding
these commands you can use `/help` for local client commands and `!help` for server commands.
