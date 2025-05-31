# Secret of Evermore Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) (optional, but recommended).
- [SNI](https://github.com/alttpo/sni/releases). This is automatically included with your Archipelago installation above.
- SNI is not compatible with (Q)Usb2Snes.
- Hardware or software capable of loading and playing SNES ROM files, including:
    - An emulator capable of connecting to SNI
      ([snes9x-nwa](https://github.com/Skarsnik/snes9x-emunwa/releases), [snes9x-rr](https://github.com/gocha/snes9x-rr/releases),
      [BSNES-plus](https://github.com/black-sliver/bsnes-plus),
      [BizHawk](http://tasvideos.org/BizHawk.html), or
      [RetroArch](https://retroarch.com?page=platforms) 1.10.1 or newer)
    - An SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), or other compatible hardware. **note:
      modded SNES minis are currently not supported by SNI. Some users have claimed success with QUsb2Snes for this system,
      but it is not supported.**
- A modern web browser to run the client.
- Your legally obtained Secret of Evermore US ROM file, probably named `Secret of Evermore (USA).sfc`

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them. Player options page: [Secret of Evermore Player Options Page](/games/Secret%20of%20Evermore/player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator
page: [YAML Validation page](/check)

## Generating a Single-Player Game

Stand-alone "Evermizer" has a way of balancing single-player games, but may not always be on par feature-wise. Head over
to the [Evermizer Website](https://evermizer.com) if you want to try the official stand-alone, otherwise read below.

1. Navigate to the Player Options page, configure your options, and click the "Generate Game" button.
    - Player Options page: [Secret of Evermore Player Options Page](/games/Secret%20of%20Evermore/player-options)
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your patch file.
5. Run your patch file through the apbpatch on evermizer.com and load it in your emulator or console.
    * apbpatch page: [Evermizer apbpatch Page](https://evermizer.com/apbpatch)

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apsoe` extension.

Put your patch file on your desktop or somewhere convenient, open the apbpatch page on evermizer.com and generate your
ROM from it. Load the ROM file in your emulator or console. apbpatch
page: [Evermizer apbpatch Page](https://evermizer.com/apbpatch)

### Connect to SNI

Start SNI either from the Archipelago install folder or the stand-alone version. If this is its first time launching,
you may be prompted to allow it to communicate through the Windows Firewall.

#### With an emulator

##### snes9x-nwa

1. Click on the Network Menu and check **Enable Emu Network Control**
2. Load your ROM file if it hasn't already been loaded.

##### snes9x-rr

1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Select the `Connector.lua` file from your SNI installation:
    * `SNI/lua/x86/Connector.lua` for 32bit snes9x-rr or
    * `SNI/lua/x64/Connector.lua` for "x64" snes9x-rr
6. Leave the Lua window open while you are playing.

* If the script window complains about missing `socket.dll` make sure it is in the lua directory.
* If the script window complains about "Bad EXE format", use the other Connector above (x86 <-> x64)

##### BizHawk

1. Ensure you have the BSNES core loaded. This is done with the main menubar, under:
    - (≤ 2.8) `Config` 〉 `Cores` 〉 `SNES` 〉 `BSNES`
    - (≥ 2.9) `Config` 〉 `Preferred Cores` 〉 `SNES` 〉 `BSNESv115+`
2. Load your ROM file if it hasn't already been loaded.
   If you changed your core preference after loading the ROM, don't forget to reload it (default hotkey: Ctrl+R).
3. Drag+drop the `Connector.lua` file from your SNI installation onto the main EmuHawk window.
    - You could instead open the Lua Console manually, click `Script` 〉 `Open Script`, and navigate to `Connector.lua`
      with the file picker.

##### bsnes-plus-nwa

This should automatically connect to SNI. If this is its first time launching, you may be prompted to allow it to
communicate through the Windows Firewall.

##### RetroArch

You only have to do these steps once.

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

1. Copy the ROM file to your SD card.
2. Load the ROM file from the menu.

### Open the client

Open ap-soeclient ([Evermizer Archipelago Client Page](http://evermizer.com/apclient)) in a modern browser.

The client should automatically connect to SNI, the "SNES" status should change to green.

### Connect to the Archipelago Server

Enter `/connect server:port` in the client's command prompt and press enter. You'll find `server:port` on the same page
that had the patch file.

### Play the game

When the game is loaded but not yet past the intro cutscene, the "Game" status is yellow. When the client shows "AP" as
green and "Game" as yellow, you're ready to play. The intro can be skipped pressing the START button and "Game" should
change to green. Congratulations on successfully joining a multiworld game!

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service on the [seed generation page](/generate). Or check out
the Archipelago website guide for more information: [Archipelago Setup Guide](/tutorial/Archipelago/setup/en)
