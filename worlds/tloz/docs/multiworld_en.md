# The Legend of Zelda (NES) Multiworld Setup Guide

## Required Software

- The Zelda1Client
    - Bundled with Archipelago: [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
- The BizHawk emulator. Versions 2.3.1 and higher are supported.
    - [BizHawk at TASVideos](https://tasvideos.org/BizHawk)
- Your legally acquired US v1.0 PRG0 ROM file, probably named `Legend of Zelda, The (U) (PRG0) [!].nes`

## Optional Software

- [Map Tracker](https://github.com/Br00ty/tloz_brooty/releases/latest)
    - Used alongside [Poptracker](https://github.com/black-sliver/PopTracker) to keep track of what items/checks you've gotten. Uses auto-tracking by connecting to the Archipelago server. 

## Installation Procedures

1. Download and install the latest version of Archipelago.
    - On Windows, download Setup.Archipelago.<HighestVersion\>.exe and run it.
2. Assign EmuHawk version 2.3.1 or higher as your default program for launching `.nes` files.
    - Extract your BizHawk folder to your Desktop, or somewhere you will remember. Below are optional additional steps
       for loading ROMs more conveniently.
        1. Right-click on a ROM file and select **Open with...**
        2. Check the box next to **Always use this app to open .nes files**.
        3. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**.
        4. Browse for `EmuHawk.exe` located inside your BizHawk folder (from step 1) and click **Open**.
3. (EmuHawk version ≤ 2.8) Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". Then restart EmuHawk. This is required for the Lua script to function correctly.
  **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs** 
  **of newer versions of EmuHawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load** 
  **"NLua+KopiLua" until this step is done.**

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. Player settings page: [The Legend of Zelda Player Settings Page](/games/The%20Legend%20of%20Zelda/player-settings)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/check)

## Generating a Single-Player Game

1. Navigate to the Player Settings page, configure your options, and click the "Generate Game" button.
    - Player Settings page: [The Legend of Zelda Player Settings Page](/games/The%20Legend%20of%20Zelda/player-settings)
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your patch file.
5. Double-click on your patch file, and the Zelda 1 Client will launch automatically, create your ROM from the
   patch file, and open your emulator for you.
6. Since this is a single-player game, you will no longer need the client, so feel free to close it.

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.aptloz` extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should automatically launch the
client, and will also create your ROM in the same place as your patch file.


## Running the Client Program and Connecting to the Server

Once the Archipelago server has been hosted:

1. Navigate to your Archipelago install folder and run `ArchipelagoZelda1Client.exe`.
2. Notice the `/connect command` on the server hosting page. (It should look like `/connect archipelago.gg:*****`
   where ***** are numbers)
3. Type the connect command into the client OR add the port to the pre-populated address on the top bar (it should
   already say `archipelago.gg`) and click `connect`.

### Running Your Game and Connecting to the Client Program

1. Open EmuHawk 2.3.1 or higher and load your ROM OR click your ROM file if it is already associated with the
   extension `*.nes`.
2. Navigate to where you installed Archipelago, then to `data/lua`, and drag+drop the `connector_tloz.lua` script onto
   the main EmuHawk window.
    1. You could instead open the Lua Console manually, click `Script` 〉 `Open Script`, and navigate to
       `connector_tloz.lua` with the file picker.
    2. If it gives a `NLua.Exceptions.LuaScriptException: .\socket.lua:13: module 'socket.core' not found:` exception
       close your emulator entirely, restart it and re-run these steps.
    3. If it says `Must use a version of BizHawk 2.3.1 or higher`, double-check your BizHawk version by clicking **
       Help** -> **About**.

## Play the game

When the client shows both NES and server are connected, you are good to go. You can check the connection status of the
NES at any time by running `/nes`.

### Other Client Commands

All other commands may be found on the [Archipelago Server and Client Commands Guide.](/tutorial/Archipelago/commands/en)
.

## Known Issues

- Triforce Fragments and Heart Containers may be purchased multiple times. It is up to you if you wish to take advantage
of this; logic will not account for or require purchasing any slot more than once. Remote items, no matter what they
are, will always only be sent once.
- Obtaining a remote item will move the location of any existing item in that room. Should this make an item 
inaccessible, simply exit and re-enter the room. This can be used to obtain the Ocean Heart Container item without the
stepladder; logic does not account for this.
- Whether you've purchased from a shop is tracked via Archipelago between sessions: if you revisit a single player game,
none of your shop pruchase statuses will be remembered. If you want them to be, connect to the client and server like 
you would in a multiplayer game.
