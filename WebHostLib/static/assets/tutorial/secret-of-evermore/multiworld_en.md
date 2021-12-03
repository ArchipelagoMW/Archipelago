# Secret of Evermore Setup Guide

## Required Software
- SNI from: [https://github.com/alttpo/sni/releases](https://github.com/alttpo/sni/releases)
  - v0.0.59 or newer (included in Archipelago 0.2.1 setup)
- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of connecting to SNI with ROM access. Any one of the following will work:
        - snes9x-rr from: [https://github.com/gocha/snes9x-rr/releases](https://github.com/gocha/snes9x-rr/releases)
        - BizHawk from: [http://tasvideos.org/BizHawk.html](http://tasvideos.org/BizHawk.html)
        - bsnes-plus-nwa from: [https://github.com/black-sliver/bsnes-plus](https://github.com/black-sliver/bsnes-plus)
    - Or SD2SNES, FXPak Pro ([https://krikzz.com/store/home/54-fxpak-pro.html](https://krikzz.com/store/home/54-fxpak-pro.html)), or other compatible hardware.
- Your legally obtained Secret of Evermore US ROM file, probably named `Secret of Evermore (USA).sfc`

## Create a Config (.yaml) File

### What is a config file and why do I need one?
See the guide on setting up a basic YAML at the Archipelago setup guide: [click here](/tutorial/archipelago/setup/en)

### Where do I get a config file?
The Player Settings page on the website allows you to configure your personal settings and export a config file from them. Player settings page: [click here](/games/Secret%20of%20Evermore/player-settings)

### Verifying your config file
If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page: [click here](/mysterycheck)

## Generating a Single-Player Game
Stand-alone "Evermizer" has a way of balancing single-player games, but may not always be on par feature-wise. Head over to [https://evermizer.com](https://evermizer.com) if you want to try the official stand-alone, otherwise read below.

1. Navigate to the Player Settings page, configure your options, and
   click the "Generate Game" button.
    - Player Settings page: [click here](/games/Secret%20of%20Evermore/player-settings)
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your patch file.
5. Run your patch file through the apbpatch on evermizer.com and load it in your emulator or console.
    * apbpatch page: [click here](https://evermizer.com/apbpatch)

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM
When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done, the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch files. Your patch file should have a `.apsoe` extension.

Put your patch file on your desktop or somewhere convenient, open the apbpatch page on evermizer.com and generate your ROM from it. Load the ROM file in your emulator or console. apbpatch page: [https://evermizer.com/apbpatch](https://evermizer.com/apbpatch)

### Connect to SNI

#### With an emulator
Start SNI either from the Archipelago install folder or the stand-alone version. If this is its first time launching, you may be prompted to allow it to communicate through the Windows Firewall.

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
1. Ensure you have the BSNES core loaded. You may do this by clicking on the Tools menu in BizHawk and following
   these menu options:  
   `Config --> Cores --> SNES --> BSNES`  
   Once you have changed the loaded core, you must restart BizHawk.
2. Load your ROM file if it hasn't already been loaded.
3. Click on the Tools menu and click on **Lua Console**
4. Click the button to open a new Lua script.
5. Select any `Connector.lua` file from your SNI installation

##### bsnes-plus-nwa
This should automatically connect to SNI.
If this is its first time launching, you may be prompted to allow it to communicate through the Windows Firewall. 

#### With hardware
This guide assumes you have downloaded the correct firmware for your device. If you have not done so already, please do this now. SD2SNES and FXPak Pro users may download the appropriate firmware on the SD2SNES releases page. SD2SNES releases page: [https://github.com/RedGuyyyy/sd2snes/releases](https://github.com/RedGuyyyy/sd2snes/releases)

Other hardware may find helpful information on the usb2snes platforms page: [http://usb2snes.com/#supported-platforms](http://usb2snes.com/#supported-platforms)

1. Copy the ROM file to your SD card.
2. Load the ROM file from the menu.

### Open the client
Open ap-soeclient ([http://evermizer.com/apclient](http://evermizer.com/apclient)) in a modern browser. Do not switch tabs, open it in a new window if you want to use the browser while playing. Do not minimize the window with the client.

The client should automatically connect to SNI, the "SNES" status should change to green.

### Connect to the Archipelago Server
Enter `/connect server:port` in the client's command prompt and press enter. You'll find `server:port` on the same page that had the patch file.

### Play the game
When the game is loaded but not yet past the intro cutscene, the "Game" status is yellow. When the client shows "AP" as green and "Game" as yellow, you're ready to play. The intro can be skipped pressing the START button and "Game" should change to green. Congratulations on successfully joining a multiworld game!

## Hosting a MultiWorld game
The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the generate page.
   - Generate page: [click here](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players,
   so they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
