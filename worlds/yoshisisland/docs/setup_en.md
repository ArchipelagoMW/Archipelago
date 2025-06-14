# Yoshi's Island Archipelago Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).


- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of connecting to SNI such as:
        - snes9x-rr from: [snes9x rr](https://github.com/gocha/snes9x-rr/releases),
        - BizHawk from: [TASVideos](https://tasvideos.org/BizHawk)
        - snes9x-nwa from: [snes9x nwa](https://github.com/Skarsnik/snes9x-emunwa/releases)
        
        NOTE: RetroArch and FXPakPro are not currently supported.
- Your legally obtained Yoshi's Island English 1.0 ROM file, probably named `Super Mario World 2 - Yoshi's Island (U).sfc`


## Installation Procedures

### Windows Setup

1. Download and install Archipelago from the link above, making sure to install the most recent version.
2. During generation/patching, you will be asked to locate your base ROM file. This is your Yoshi's Island ROM file.
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

The Player Options page on the website allows you to configure your personal options and export a config file from
them.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whomever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apyi` extension.

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
    - Look in the Archipelago folder for `/SNI/lua/Connector.lua`.
6. If you see an error while loading the script that states `socket.dll missing` or similar, navigate to the folder of
the lua you are using in your file explorer and copy the `socket.dll` to the base folder of your snes9x install.

##### BizHawk

1. Ensure you have the BSNES core loaded. This is done with the main menubar, under:
    - (≤ 2.8) `Config` 〉 `Cores` 〉 `SNES` 〉 `BSNES`
    - (≥ 2.9) `Config` 〉 `Preferred Cores` 〉 `SNES` 〉 `BSNESv115+`
2. Load your ROM file if it hasn't already been loaded.
   If you changed your core preference after loading the ROM, don't forget to reload it (default hotkey: Ctrl+R).
3. Drag+drop the `Connector.lua` file included with your client onto the main EmuHawk window.
    - Look in the Archipelago folder for `/SNI/lua/x64` or `/SNI/lua/x86` depending on if the
      emulator is 64-bit or 32-bit. Please note the most recent versions of BizHawk are 64-bit only.
    - You could instead open the Lua Console manually, click `Script` 〉 `Open Script`, and navigate to `Connector.lua`
      with the file picker.



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
