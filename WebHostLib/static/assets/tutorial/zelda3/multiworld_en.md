# A Link to the Past Randomizer Setup Guide

## Required Software

- A client, one of:
    - Z3Client: [Z3Client Releases Page](https://github.com/ArchipelagoMW/Z3Client/releases)
    - SNIClient included with Archipelago:
      [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
        - If installing Archipelago, make sure to check the box for SNIClient -> A Link to the Past Patch Setup during
          install, or SNI will not be included
- Super Nintendo Interface (SNI): [SNI Releases Page](https://github.com/alttpo/sni/releases)
    - (Included in both Z3Client and SNIClient)
- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of connecting to SNI, one of:
        -
        snes9x_Multitroid: [snes9x Multitroid Download in Google Drive](https://drive.google.com/drive/folders/1_ej-pwWtCAHYXIrvs5Hro16A1s9Hi3Jz)
        - BizHawk: [BizHawk Official Website](http://tasvideos.org/BizHawk.html)
    - An SD2SNES, FXPak Pro ([FXPak Pro Store page](https://krikzz.com/store/home/54-fxpak-pro.html)), or other
      compatible hardware
- Your Japanese v1.0 ROM file, probably named `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Installation Procedures

1. Download and install your preferred client from the link above, making sure to install the most recent version.
   **The installer file is located in the assets section at the bottom of the version information**.
    - During setup, you will be asked to locate your base ROM file. This is your Japanese Link to the Past ROM file.

2. If you are using an emulator, you should assign your Lua capable emulator as your default program for launching ROM
   files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .sfc files**
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

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. ([Player Settings Page for A Link to the Past](/games/A%20Link%20to%20the%20Past/player-settings))

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validation
page. ([YAML Validation Page](/mysterycheck))

## Generating a Single-Player Game

1. Navigate to the Player Settings page, configure your options, and click the "Generate Game"
   button. ([Player Settings for A Link to the Past](/games/A%20Link%20to%20the%20Past/player-settings))
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your patch file.
5. Double-click on your patch file, and the Z3Client will launch automatically, create your ROM from the patch file, and
   open your emulator for you.
6. Since this is a single-player game, you will no longer need the client, so feel free to close it.

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apbp` extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should automatically launch the
client, and will also create your ROM in the same place as your patch file.

### Connect to the client

#### With an emulator

When the client launched automatically, SNI should have also automatically launched in the background. If this is its
first time launching, you may be prompted to allow it to communicate through the Windows Firewall.

##### snes9x Multitroid

1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Select the connector lua file included with your client
    - Z3Client users should download `sniConnector.lua` from the client download page
    - SNIClient users should look in their Archipelago folder for `/sni/lua`

##### BizHawk

1. Ensure you have the BSNES core loaded. You may do this by clicking on the Tools menu in BizHawk and following these
   menu options:  
   `Config --> Cores --> SNES --> BSNES`  
   Once you have changed the loaded core, you must restart BizHawk.
2. Load your ROM file if it hasn't already been loaded.
3. Click on the Tools menu and click on **Lua Console**
4. Click Script -> Open Script...
5. Select the `Connector.lua` file you downloaded above
    - Z3Client users should download `sniConnector.lua` from the client download page
    - SNIClient users should look in their Archipelago folder for `/sni/lua`
6. Run the script by double-clicking it in the listing

#### With hardware

This guide assumes you have downloaded the correct firmware for your device. If you have not done so already, please do
this now. SD2SNES and FXPak Pro users may download the appropriate
firmware [from the sd2snes releases page](https://github.com/RedGuyyyy/sd2snes/releases). Other hardware may find
helpful information [on the usb2snes supported platforms page](http://usb2snes.com/#supported-platforms).

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

The recommended way to host a game is to use our hosting service on the [seed generation page](/generate). Or check out
the Archipelago website guide for more information: [Archipelago Website Guide](/tutorial/archipelago/using_website/en)