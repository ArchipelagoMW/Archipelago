# Jak And Daxter (ArchipelaGOAL) Setup Guide

## Required Software

- A legally purchased copy of *Jak And Daxter: The Precursor Legacy.*
- [The OpenGOAL Launcher](https://opengoal.dev/)
- [The Jak and Daxter .APWORLD package](https://github.com/ArchipelaGOAL/Archipelago/releases)

At this time, this method of setup works on Windows only, but Linux support is a strong likelihood in the near future as OpenGOAL itself supports Linux.

## Installation via OpenGOAL Launcher

- Follow the installation process for the official OpenGOAL Launcher. See [here](https://opengoal.dev/docs/usage/installation).
    - **You must set up a vanilla installation of Jak and Daxter before you can install mods for it.**
- Follow the setup process for adding mods to the OpenGOAL Launcher. See [here](https://jakmods.dev/).
- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`.
- Under `Available Mods`, click `ArchipelaGOAL`. The mod should begin installing. When it is done, click `Continue` in the bottom right corner.
- Once you are back in the mod menu, click on `ArchipelaGOAL` from the `Installed Mods` list.
- **As a temporary measure, you need to copy the extracted ISO data to the mod directory so the compiler will work properly.**
    - If you have the NTSC version of the game, follow the `The Game Fails To Load The Title Screen` instructions below.
    - If you have the PAL version of the game, follow the `Special PAL Instructions` instructions **instead.**
- **If you installed the OpenGOAL Launcher to a non-default directory, you must now follow these steps.**
    - Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
    - Click the Jak and Daxter logo on the left sidebar.
    - Click `Features` in the bottom right corner, then click `Mods`.
    - Under `Installed Mods`, then click `ArchipelaGOAL`, then click `Advanced` in the bottom right corner, then click `Open Game Data Folder`. You should see a new File Explorer open to that directory.
    - In the File Explorer, go to the parent directory called `archipelagoal`, and you should see the `gk.exe` and `goalc.exe` executables. Take note of this directory.
    - Run the Archipelago Launcher, then click on `Open host.yaml`. You should see a new text editor open that file.
    - Search for `jakanddaxter_options`, then find the `root_directory` entry underneath it. Paste the directory you noted earlier (the one containing gk.exe and goalc.exe) inside the double quotes. 
    - **MAKE SURE YOU CHANGE ALL BACKSLASHES `\ ` TO FORWARD SLASHES `/`.**

```
jakanddaxter_options:
  # Path to folder containing the ArchipelaGOAL mod executables (gk.exe and goalc.exe).
  # Ensure this path contains forward slashes (/) only.
  root_directory: "%programfiles%/OpenGOAL-Launcher/features/jak1/mods/JakMods/archipelagoal"
```

  - Save the file and close it.
- **DO NOT PLAY AN ARCHIPELAGO GAME THROUGH THE OPENGOAL LAUNCHER.** The Jak and Daxter Client should handle everything for you (see below).

## Updates and New Releases via OpenGOAL Launcher

If you are in the middle of an async game, and you do not want to update the mod, you do not need to do this step. The mod will only update when you tell it to.

- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`.
- Under `Installed Mods`, click `ArchipelaGOAL`.
- Click `Update` to download and install any new updates that have been released.
- You can verify your version by clicking `Versions`. The version you are using will say `(Active)` next to it.
- **After the update is installed, you must click `Advanced`, then click `Compile` to make the update take effect.**

## Starting a Game

### New Game

- Run the Archipelago Launcher.
- From the right-most list, find and click `Jak and Daxter Client`.
- 4 new windows should appear:
  - Two powershell windows will open to run the OpenGOAL compiler and the game. They should take about 30 seconds to compile.
      - You should hear a musical cue to indicate the compilation was a success. If you do not, see the Troubleshooting section.
  - The game window itself will launch, and Jak will be standing outside Samos's Hut. 
      - Once compilation is complete, the title intro sequence will start.
  - Finally, the Archipelago text client will open.
      - If you see `The REPL is ready!` and `The Memory Reader is ready!` then that should indicate a successful startup.
- You can *minimize* the 2 powershell windows, **BUT DO NOT CLOSE THEM.** They are required for Archipelago and the game to communicate with each other.
- Use the text client to connect to the Archipelago server while on the title screen. This will communicate your current settings to the game.
- Start a new game in the title screen, and play through the cutscenes.
- Once you reach Geyser Rock, you can start the game!
    - You can leave Geyser Rock immediately if you so choose - just step on the warp gate button.

### Returning / Async Game

- The same steps as New Game apply, with some exceptions: 
    - Connect to the Archipelago server **BEFORE** you load your save file. This is to allow AP to give the game your current settings and all the items you had previously.
    - **THESE SETTINGS AFFECT LOADING AND SAVING OF SAVE FILES, SO IT IS IMPORTANT TO DO THIS FIRST.**
    - Then, instead of choosing `New Game` in the title menu, choose `Load Game`, then choose the save file **CORRESPONDING TO YOUR CURRENT ARCHIPELAGO CONNECTION.** 

## Troubleshooting

### The Game Fails To Load The Title Screen

You may start the game via the Text Client, but it never loads in the title screen. Check the Compiler window and you may see red and yellow errors like this.

```
-- Compilation Error! --
```

If this happens, follow these instructions. If you are using a PAL version of the game, you should skip these instructions and follow `Special PAL Instructions` below.

- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar, then click `Advanced`, then click `Open Game Data Folder`. Copy the `iso_data` folder from this directory.
- Back in the OpenGOAL Launcher, click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- In the bottom right corner, click `Advanced`, then click `Open Game Data Folder`.
- Paste the `iso_data` folder you copied earlier.
- Back in the OpenGOAL Launcher, click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- In the bottom right corner, click `Advanced`, then click `Compile`.

### The Text Client Says "The <gk/goalc> process has died"

If at any point the text client says `The <gk/goalc> process has died`, you will need to restart the appropriate application.

- Run the OpenGOAL Launcher, then click `Features`, then click `Mods`, then click `ArchipelaGOAL`.
- If the gk process died, click `Advanced`, then click `Play in Debug Mode`.
- If the goalc process died, click `Advanced`, then click `Open REPL`.
- Then enter the following commands into the text client to reconnect everything to the game.
    - `/repl connect`
    - `/memr connect`
- Once these are done, you can enter `/repl status` and `/memr status` in the text client to verify.

### The Game Freezes On The Same Two Frames, But The Music Is Still Playing

If the game freezes by replaying the same two frames over and over, but the music still runs in the background, you may have accidentally interacted with the powershell windows in the background. They halt the game if you scroll up in them, highlight text in them, etc.

- To unfreeze the game, scroll to the very bottom of the powershell window and right click. That will release powershell from your control and allow the game to continue.
- It is recommended to keep these windows minimized and out of your way.

### The Client Cannot Open A REPL Connection

If the client cannot open a REPL connection to the game, you may need to ensure you are not hosting anything on ports `8181` and `8112`.

### Special PAL Instructions

PAL versions of the game seem to require additional troubleshooting/setup in order to work properly. Below are some instructions that may help.
If you see `-- Compilation Error! --` after pressing `Compile` or Launching the ArchipelaGOAL mod, try these steps.

- Remove these folders if you have them: 
    - `<opengoal active version directory>/iso_data`
    - `<archipelagoal directory>/iso_data`
    - `<archipelagoal directory>/data/iso_data`
- Place your Jak1 ISO in `<archipelagoal directory>` and rename it to `JakAndDaxter.iso`
- Type `cmd` in Windows search, right click `Command Prompt`, and pick `Run as Administrator`
- Run `cd <archipelagoal directory>`
- Then run `.\extractor.exe --extract --extract-path .\data\iso_data "JakAndDaxter.iso"` 
    - This command should end by saying `Uses Decompiler Config Version - ntsc_v1` or `... - pal`. Take note of this message.
- If you saw `ntsc_v1`:
    - In cmd, run `.\decompiler.exe data\decompiler\config\jak1\jak1_config.jsonc --version "ntsc_v1" data\iso_data data\decompiler_out`
- If you saw `pal`:
    - Rename `<archipelagoal directory>\data\iso_data\jak1` to `jak1_pal`
    - Back in cmd, run `.\decompiler.exe data\decompiler\config\jak1\jak1_config.jsonc --version "pal" data\iso_data data\decompiler_out`
    - Rename `<archipelagoal directory>\data\iso_data\jak1_pal` back to `jak1`
    - Rename `<archipelagoal directory>\data\decompiler_out\jak1_pal` back to `jak1`
- Open a **brand new** Powershell window and launch the compiler:
    - `cd <archipelagoal directory>`
    - `.\goalc.exe --user-auto --game jak1`
    - From the compiler (in the same window): `(mi)`. This should compile the game. **Note that the parentheses are important.** 
    - **Don't close this first terminal, you will need it at the end.**
- Then, open **another brand new** Powershell window and execute the game:
    - `cd <archipelagoal directory>`
    - `.\gk.exe -v --game jak1 -- -boot -fakeiso -debug`
- Finally, **from the first Powershell still in the GOALC compiler**, connect to the game: `(lt)`.

## Known Issues

- The game needs to boot in debug mode in order to allow the REPL to connect to it. We disable debug mode once we connect to the AP server.
- The REPL Powershell window is orphaned once you close the game - you will have to kill it manually when you stop playing.
- The powershell windows cannot be run as background processes due to how the REPL works, so the best we can do is minimize them.
- Orbsanity checks may show up out of order in the text client.
- Large item releases may take up to several minutes for the game to process them all. 
