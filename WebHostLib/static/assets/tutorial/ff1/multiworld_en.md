# Final Fantasy 1 (NES) Multiworld Setup Guide

## Required Software
- The FF1Client which is bundled with [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- The [BizHawk](http://tasvideos.org/BizHawk.html) emulator. Versions 2.3.1 and higher are supported. 
  Version 2.7 is recommended
- Your Final Fantasy (USA Edotopm) ROM file, probably named `Final Fantasy (USA).nes`

## Installation Procedures
1. Download and install the latest version of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
2. Assign Bizhawk version 2.3.1 or higher as your default program for launching `.nes` files.
    1. Extract your Bizhawk folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .nes files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for `EmuHawk.exe` located inside your Bizhawk folder (from step 1) and click **Open**.

## Playing a Multiworld
Playing a multiworld on Archipelago.gg has 3 key components:
1. The Server which is hosting a game for all players.
2. The Client Program. For Final Fantasy 1 it is a standalone program but other randomizers may build it in.
3. The Game itself, in this case running on Bizhawk, which then connects to the Client running on your computer.

To set this up the following steps are required:
1. (Each Player) Generate your own yaml file and randomized ROM
2. (Host Only) Generate a randomized game with you and 0 or more players using Archipelago
3. (Host Only) Run the Archipelago Server
4. (Each Player) Run your client program and connect it to the Server
5. (Each Player) Run your game and connect it to your client program
6. (Each Player) Play the game and have fun!

### Obtaining your Archipelago yaml file and randomized ROM
Unlike most other Archipelago.gg games Final Fantasy 1 is randomized by the 
[main randomizer](https://finalfantasyrandomizer.com/). Generate a game by going to the site and performing the
following steps
1. Select the randomization options (also known as `Flags` in the community) of your choice. If you do not know what 
you prefer, or it is your first time playing select the "Archipelago" preset on the main page.
2. Go to the `Beta` tab and ensure `Archipelago` is enabled. Set your player name to any name that represents you.
3. Upload you `Final Fantasy(USA).nes` (and click `Remember ROM` for the future!)
4. Press the `NEW` button below `Seed` a few times
5. Click `GENERATE ROM`

It should download two files. One is the `*.nes` file which your emulator will run and the other is the yaml file
required by Archipelago.gg

### Generating the Multiworld and Starting the Server
The game can be generated locally or by Archipelago.gg.

#### Generating on Archipelago.gg (Recommended)
1. Gather all yaml files
2. Create a zip file containing all of the yaml files. Make sure it is a `*.zip` not a `*.7z` or a `*.rar`
3. Navigate to the [Generate Page](https://archipelago.gg/generate) and click `Upload File`
   1. For your first game keep `Forfeit Permission` as `Automatic on goal completion`. Forfeiting actually means
      giving out all of the items remaining in your game in this case so you do not block anyone else.
   2. For your first game keep `Hint Cost` at 10%
4. Select your zip file

#### Generating Locally
1. Navigate to your Archipelago install directory
2. Empty the `Players` directory then fill it with one yaml per player including your own which you got from the 
   finalfantasyrandomizer website above
3. Run `ArchipelagoGenerate.exe` (double-click it in File Explorer)
4. You will find your generated game in the `output` directory

#### Starting the server
If you generated on Archipelago.gg click `Create New Room` on the results page to start your server
If you generated locally simply navigate to the [Host Game Page](https://archipelago.gg/uploads) and upload the file
in the `output` directory

### Running the Client Program and Connecting to the Server
1. Navigate to your Archipelago install folder and run `ArchipelagoFF1Client.exe`
2. Notice the `/connect command` on the server hosting page (It should look like `/connect archipelago.gg:*****` where 
   ***** are numbers)
3. Type the connect command into the client OR add the port to the pre-populated address on the top bar (it should
   already say `archipelago.gg`) and click `connect`
4. Enter your **Slot Name** which is what you choose during Step 2 of the Obtaining ROM step as your **Player Name**

#### Running Your Game and Connecting to the Client Program
1. Open Bizhawk 2.3.1 or higher and load your ROM OR 
   click your ROM file if it is already associated with the extension `*.nes`
2. Click on the Tools menu and click on **Lua Console**
3. Click the folder button to open a new Lua script. (CTL-O or **Script** -> **Open Script**)
4. Navigate to the location you installed Archipelago to. Open data/lua/FF1/ff1_connector.lua
   1. If it gives a `NLua.Exceptions.LuaScriptException: .\socket.lua:13: module 'socket.core' not found:` exception
   close your emulator entirely, restart it and re-run these steps
   2. If it says `Must use a version of bizhawk 2.3.1 or higher`, double check your Bizhawk version by clicking 
   **Help** -> **About**

### Play the game
When the client shows both NES and server are connected you are good to go. You can check the connection status of the
NES at any time by running `/nes`

### Helpful Commands
`/nes` Shows the current status of the NES connection
`/received` Displays all the items you have found or been sent
`/missing` Displays all the locations along with their current status (checked/missing)
`!hint <item name>` Tells you at which location in whose game your Item is. Note you need to have checked some locations
to earn a hint. You can check how many you have by just running `!hint`
`!forfeit` If you didn't turn on auto-forfeit or you allowed forfeiting prior to goal completion. Remember that
"forfeiting" actually means sending out your remaining items in your world
`/disconnect` if you accidentally connected to the wrong port run this to disconnect and then reconnect using
`/connect <address with port number>` connect to the multiworld server

Just typing anything will broadcast a message to all players

HOST ONLY ON THE WEBSITE
`/forfeit <Player Name>` Forfeits someone regardless of settings and game completion status
