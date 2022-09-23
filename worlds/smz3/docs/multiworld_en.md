# SMZ3 Setup Guide

## Required Software

- One of the client programs:
  - [SNIClient](https://github.com/ArchipelagoMW/Archipelago/releases), included with the main 
  Archipelago install. Make sure to check the box for `SNI Client - Super Metroid Patch Setup` and 
  `SNI Client - A Link to the Past Patch Setup`
- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of connecting to SNI such as:
        - snes9x-rr from: [snes9x rr](https://github.com/gocha/snes9x-rr/releases),
        - BizHawk from: [BizHawk Website](http://tasvideos.org/BizHawk.html), or
        - RetroArch 1.10.3 or newer from: [RetroArch Website](https://retroarch.com?page=platforms). Or,
    - An SD2SNES, FXPak Pro ([FXPak Pro Store Page](https://krikzz.com/store/home/54-fxpak-pro.html)), or other
      compatible hardware
- Your legally obtained Super Metroid ROM file, probably named `Super Metroid (Japan, USA).sfc` and
  Your Japanese Zelda3 v1.0 ROM file, probably named `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Installation Procedures

### Windows Setup

1. During the installation of Archipelago, you will have been asked to install the SNI Client. If you did not do this,
   or you are on an older version, you may run the installer again to install the SNI Client.
2. During setup, you will be asked to locate your base ROM files. This is your Super Metroid and Zelda3 ROM files.
3. If you are using an emulator, you should assign your Lua capable emulator as your default program for launching ROM
   files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .sfc files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for your emulator's `.exe` file and click **Open**. This file should be located inside the folder you
       extracted in step one.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. Player settings page: [SMZ3 Player Settings Page](/games/SMZ3/player-settings)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Generating a Single-Player Game

1. Navigate to the Player Settings page, configure your options, and click the "Generate Game" button.
    - Player Settings page: [SMZ3 Player Settings Page](/games/SMZ3/player-settings)
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your patch file.
5. Double-click on your patch file, and the SMZ3 Client will launch automatically, create your ROM from the
   patch file, and open your emulator for you.
6. Since this is a single-player game, you will no longer need the client, so feel free to close it.

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apsmz3` extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should automatically launch the
client, and will also create your ROM in the same place as your patch file.

### Connect to the client

#### With an emulator

When the client launched automatically, SNI should have also automatically launched in the background. If this is its
first time launching, you may be prompted to allow it to communicate through the Windows Firewall.

##### snes9x-rr

1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Select the connector lua file included with your client
    - Look in the Archipelago folder for `/SNI/lua/x64` or `/SNI/lua/x86` depending on if the
      emulator is 64-bit or 32-bit.
6. If you see an error while loading the script that states `socket.dll missing` or similar, navigate to the folder of 
the lua you are using in your file explorer and copy the `socket.dll` to the base folder of your snes9x install.

##### BizHawk

1. Ensure you have the BSNES core loaded. You may do this by clicking on the Tools menu in BizHawk and following these
   menu options:  
   `Config --> Cores --> SNES --> BSNES`  
   Once you have changed the loaded core, you must restart BizHawk.
2. Load your ROM file if it hasn't already been loaded.
3. Click on the Tools menu and click on **Lua Console**
4. Click the button to open a new Lua script.
5. Select the `Connector.lua` file included with your client
    - Look in the Archipelago folder for `/SNI/lua/x64` or `/SNI/lua/x86` depending on if the
      emulator is 64-bit or 32-bit. Please note the most recent versions of BizHawk are 64-bit only.

##### RetroArch 1.10.3 or newer

You only have to do these steps once. Note, RetroArch 1.9.x will not work as it is older than 1.10.3.

1. Enter the RetroArch main menu screen.
2. Go to Settings --> User Interface. Set "Show Advanced Settings" to ON.
3. Go to Settings --> Network. Set "Network Commands" to ON. (It is found below Request Device 16.) Leave the default
   Network Command Port at 55355.

![Screenshot of Network Commands setting](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)
4. Go to Main Menu --> Online Updater --> Core Downloader. Scroll down and select "Nintendo - SNES / SFC (bsnes-mercury
   Performance)".

When loading a ROM, be sure to select a **bsnes-mercury** core. These are the only cores that allow external tools to
read ROM data.

#### With hardware

This guide assumes you have downloaded the correct firmware for your device. If you have not done so already, please do
this now. SD2SNES and FXPak Pro users may download the appropriate firmware on the SD2SNES releases page. SD2SNES
releases page: [SD2SNES Releases Page](https://github.com/RedGuyyyy/sd2snes/releases)

Other hardware may find helpful information on the usb2snes platforms
page: [usb2snes Supported Platforms Page](http://usb2snes.com/#supported-platforms)

1. Close your emulator, which may have auto-launched.
2. Power on your device and load the ROM.

### Connect to the Archipelago Server

The patch file which launched your client should have automatically connected you to the AP Server. There are a few
reasons this may not happen however, including if the game is hosted on the website but was generated elsewhere. If the
client window shows "Server Status: Not Connected", simply ask the host for the address of the server, and copy/paste it
into the "Server" input field then press enter.

The client will attempt to reconnect to the new server address, and should momentarily show "Server Status: Connected".

### Play the game

When the client shows both SNES Device and Server as connected, you're ready to begin playing. Congratulations on
successfully joining a multiworld game!

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
