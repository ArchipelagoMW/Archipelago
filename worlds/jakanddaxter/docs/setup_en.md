# Jak And Daxter (ArchipelaGOAL) Setup Guide

## Required Software

- A legally purchased copy of *Jak And Daxter: The Precursor Legacy.*
- [The OpenGOAL Mod Launcher](https://jakmods.dev/)
- [The Jak and Daxter .APWORLD package](https://github.com/ArchipelaGOAL/Archipelago/releases)

At this time, this method of setup works on Windows only, but Linux support is a strong likelihood in the near future. 
(OpenGOAL itself supports Linux, and the mod launcher is runnable with Python.)

## Preparations

- Dump your copy of the game as an ISO file to your PC.
- Install the Mod Launcher.
- If you are prompted by the Mod Launcher at any time during setup, provide the path to your ISO file.

## Installation

***OpenGOAL Mod Launcher***

- Run the Mod Launcher and click `ArchipelaGOAL` in the mod list.
- Click `Install` and wait for it to complete.
  - If you have yet to be prompted for the ISO, click `Re-Extract` and provide the path to your ISO file.
- Click `Recompile`. This may take between 30-60 seconds. It should run to 100% completion. If it does not, see the Troubleshooting section.
- Click `View Folder`. 
  - In the new file explorer window, take note of the current path. It should contain `gk.exe` and `goalc.exe`.
- Verify that the mod launcher copied the extracted ISO files to the mod directory:
  - `C:\Users\<YourName>\AppData\Roaming\OpenGOAL-Mods\archipelagoal\iso_data` should have *all* the same files as
  - `C:\Users\<YourName>\AppData\Roaming\OpenGOAL-Mods\_iso_data`, if it doesn't, copy those files over manually.
  - And then `Recompile` if you needed to copy the files over.
- **DO NOT PLAY AN ARCHIPELAGO GAME THROUGH THE MOD LAUNCHER.** It will run in retail mode, which is incompatible with Archipelago. We need it to run in debug mode (see below).

***Archipelago Launcher***

- Copy the `jakanddaxter.apworld` file into your `Archipelago/custom_worlds` directory.
  - Reminder: the default installation location for Archipelago is `C:\ProgramData\Archipelago`.
- Run the Archipelago Launcher.
- From the left-most list, click `Generate Template Options`.
- Select `Jak and Daxter The Precursor Legacy.yaml`. In the text file that opens, enter the name you want and remember it for later.
- Save this file in `Archipelago/players`. You can now close the file.
- Back in the Launcher, from the left-most list, click `Generate`. A window will appear to generate your seed and close itself.
- If you plan to host the game yourself, from the left-most list, click `Host`.
  - When asked to select your multiworld seed, navigate to `Archipelago/output` and select the zip file containing the seed you just generated.
  - You can sort by Date Modified to make it easy to find.

## Updates and New Releases

***OpenGOAL Mod Launcher***

- Run the Mod Launcher and click `ArchipelaGOAL` in the mod list.
- Click `Launch` to download and install any new updates that have been released.
- You can verify your version once you reach the title screen menu by navigating to `Options > Game Options > Miscellaneous > Speedrunner Mode`.
- Turn on `Speedrunner Mode` and exit the menu. You should see the installed version number in the bottom left corner. Then turn `Speedrunner Mode` back off.
- Once you've verified your version, you can close the game. Remember, this is just for downloading updates. **DO NOT PLAY AN ARCHIPELAGO GAME THROUGH THE MOD LAUNCHER.**
 
***Archipelago Launcher***

- Copy the latest `jakanddaxter.apworld` file into your `Archipelago/custom_worlds` directory.

## Starting a Game

***New Game***

- Run the Archipelago Launcher.
- From the right-most list, find and click `Jak and Daxter Client`.
- 4 new windows should appear:
  - A powershell window will open to run the OpenGOAL compiler. It should take about 30 seconds to compile the game.
    - As before, it should run to 100% completion, and you should hear a musical cue to indicate it is done. If it does not run to 100%, or you do not hear the musical cue, see the Troubleshooting section.
  - Another powershell window will open to run the game.
  - The game window itself will launch, and Jak will be standing outside Samos's Hut.
  - Finally, the Archipelago text client will open.
    - You should see several messages appear after the compiler has run to 100% completion. If you see `The REPL is ready!` and `The Memory Reader is ready!` then that should indicate a successful startup.
    - The game should then load in the title screen.
- You can *minimize* the 2 powershell windows, **BUT DO NOT CLOSE THEM.** They are required for Archipelago and the game to communicate with each other.
- Start a new game in the title screen, and play through the cutscenes.
- Once you reach Geyser Rock, you can connect to the Archipelago server.
  - Provide your slot/player name and hit Enter, and then start the game!
  - You can leave Geyser Rock immediately if you so choose - just step on the warp gate button.

***Returning / Async Game***

- One important note is to connect to the Archipelago server **AFTER** you load your save file. This is to allow AP to give you all the items you had previously.
- Otherwise, the same steps as New Game apply.

## Troubleshooting

***Installation Failure***

- If you encounter errors during extraction or compilation of the game when using the Mod Launcher, you may see errors like this:
```
-- Compilation Error! -- 
Input file iso_data/jak1/MUS/TWEAKVAL.MUS does not exist.
```
  - If this occurs, you may need to copy the extracted data to the mod folder manually.
    - From a location like this: `C:\Users\<YourName>\AppData\Roaming\OpenGOAL-Mods\_iso_data`
    - To a location like this: `C:\Users\<YourName>\AppData\Roaming\OpenGOAL-Mods\archipelagoal\iso_data`
    - Then try clicking `Recompile` in the Mod Launcher (ensure you have selected the right mod first!)

***Game Failure***

- If at any point the text client says `The <gk/goalc> process has died`, you will need to restart the appropriate 
  application:
  - Open a new powershell window.
  - Navigating to the directory containing `gk.exe` and `goalc.exe` via `cd`.
  - Run the command corresponding to the dead process:
    - `.\gk.exe --game jak1 -- -v -boot -fakeiso -debug`
    - `.\goalc.exe --game jak1`
  - Then enter the following commands into the text client to reconnect everything to the game.
    - `/repl connect`
    - `/memr connect`
  - Once these are done, you can enter `/repl status` and `/memr status` to verify.
- If the game freezes by replaying the same two frames over and over, but the music still runs in the background, you may have accidentally interacted with the powershell windows in the background - they halt the game if you:scroll up in them, highlight text in them, etc.
  - To unfreeze the game, scroll to the very bottom of the log output and right click. That will release powershell from your control and allow the game to continue.
  - It is recommended to keep these windows minimized and out of your way.

### Known Issues

- The game needs to run in debug mode in order to allow the repl to connect to it. We hide the debug text on screen and play the game's introductory cutscenes properly.
- The powershell windows cannot be run as background processes due to how the repl works, so the best we can do is minimize them.
- The client is currently not very robust and doesn't handle failures gracefully. This may result in items not being delivered to the game, or location checks not being delivered to the server.
