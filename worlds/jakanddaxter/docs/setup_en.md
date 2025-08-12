# Jak And Daxter (ArchipelaGOAL) Setup Guide

## Required Software

- A legally purchased copy of *Jak And Daxter: The Precursor Legacy.*
- [The OpenGOAL Launcher](https://opengoal.dev/)

At this time, this method of setup works on Windows only, but Linux support is a strong likelihood in the near future as OpenGOAL itself supports Linux.

## Installation via OpenGOAL Launcher

**You must set up a vanilla installation of Jak and Daxter before you can install mods for it.**

- Follow the installation process for the official OpenGOAL Launcher. See [here](https://opengoal.dev/docs/usage/installation). 
- Follow the setup process for adding mods to the OpenGOAL Launcher. See [here](https://jakmods.dev/).
- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`.
- Under `Available Mods`, click `ArchipelaGOAL`. The mod should begin installing. When it is done, click `Continue` in the bottom right corner.
- **DO NOT PLAY AN ARCHIPELAGO GAME THROUGH THE OPENGOAL LAUNCHER.** The Archipelago Client should handle everything for you.

### For NTSC versions of the game, follow these steps.

- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- In the bottom right corner, click `Advanced`, then click `Compile`.

### For PAL versions of the game, follow these steps.

PAL versions of the game seem to require additional troubleshooting/setup in order to work properly.
Below are some instructions that may help. 
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
- Open a **brand new** console window and launch the compiler:
    - `cd <archipelagoal directory>`
    - `.\goalc.exe --user-auto --game jak1`
    - From the compiler (in the same window): `(mi)`. This should compile the game. **Note that the parentheses are important.** 
    - **Don't close this first terminal, you will need it at the end.**
- Then, open **another brand new** console window and execute the game:
    - `cd <archipelagoal directory>`
    - `.\gk.exe -v --game jak1 -- -boot -fakeiso -debug`
- Finally, **from the first console still in the GOALC compiler**, connect to the game: `(lt)`.

## Updates and New Releases via OpenGOAL Launcher

If you are in the middle of an async game, and you do not want to update the mod, you do not need to do this step. The mod will only update when you tell it to.

- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- Click `Update` to download and install any new updates that have been released.
- You can verify your version by clicking `Versions`. The version you are using will say `(Active)` next to it.
- **Then you must click `Advanced`, then click `Compile` to make the update take effect.**

## Starting a Game

### New Game

- Run the Archipelago Launcher.
- From the client list, find and click `Jak and Daxter Client`.
- 3 new windows should appear:
    - The OpenGOAL compiler will launch and compile the game. They should take about 30 seconds to compile.
        - You should hear a musical cue to indicate the compilation was a success. If you do not, see the Troubleshooting section.
        - You can **MINIMIZE** the Compiler window, **BUT DO NOT CLOSE IT.** It is required for Archipelago and the game to communicate with each other.
    - The game window itself will launch, and Jak will be standing outside Samos's Hut. 
        - Once compilation is complete, the title sequence will start.
    - Finally, the Archipelago text client will open.
        - If you see **BOTH** `The REPL is ready!` and `The Memory Reader is ready!` then that should indicate a successful startup. If you do not, see the Troubleshooting section.
- Once you see `CONNECT TO ARCHIPELAGO NOW` on the title screen, use the text client to connect to the Archipelago server. This will communicate your current settings and slot info to the game.
- If you see `RECEIVING ITEMS, PLEASE WAIT...`, the game is busy receiving items from your starting inventory, assuming you have some.
- Once you see `READY! PRESS START TO CONTINUE` on the title screen, you can press Start.
- Choose `New Game`, choose a save file, and play through the opening cutscenes.
- Once you reach Geyser Rock, the game has begun!
    - You can leave Geyser Rock immediately if you so choose - just step on the warp gate button.

### Returning / Async Game
The same steps as New Game apply, with some exceptions: 

- Once you reach the title screen, connect to the Archipelago server **BEFORE** you load your save file. 
    - This is to allow AP to give the game your current settings and all the items you had previously.
    - **THESE SETTINGS AFFECT LOADING AND SAVING OF SAVE FILES, SO IT IS IMPORTANT TO DO THIS FIRST.**
- Once you see `READY! PRESS START TO CONTINUE` on the title screen, you can press Start. 
- Instead of choosing `New Game` in the title menu, choose `Load Game`, then choose the save file **THAT HAS YOUR CURRENT SLOT NAME.**
    - To help you find the correct save file, highlighting a save will show you that save's slot name and the first 8 digits of the multiworld seed number.

## Troubleshooting

### The Text Client Says "Unable to locate the OpenGOAL install directory"

Normally, the Archipelago client should be able to find your OpenGOAL installation automatically. 

If it cannot, you may have to tell it yourself. Follow these instructions.

- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- Click `Advanced` in the bottom right corner, then click `Open Game Data Folder`. You should see a new File Explorer open to that directory.
- In the File Explorer, go to the parent directory called `archipelagoal`, and you should see the `gk.exe` and `goalc.exe` executables. Copy this path.
- Run the Archipelago Launcher, then click on `Open host.yaml`. You should see a new text editor open that file.
- Search for `jakanddaxter_options`, and you will need to make 2 changes here.
- First, find the `root_directory` entry. Paste the path you noted earlier (the one containing gk.exe and goalc.exe) inside the double quotes. 
- **MAKE SURE YOU CHANGE ALL BACKSLASHES `\ ` TO FORWARD SLASHES `/`.**

```yaml
  root_directory: "%programfiles%/OpenGOAL-Launcher/features/jak1/mods/JakMods/archipelagoal"
```

- Second, find the `root_directory` entry. Change this to `false`. You do not need to use double quotes.

```yaml
  auto_detect_root_directory: true
```

- Save the file and close it.

### The Game Fails To Load The Title Screen

You may start the game via the Text Client, but it never loads in the title screen. Check the Compiler window: you may see red and yellow errors like this.

```
-- Compilation Error! --
```

If this happens, follow these instructions. If you are using a PAL version of the game, you should skip these instructions and follow the `Special PAL Instructions` above.

- Run the OpenGOAL Launcher (if you had it open before, close it and reopen it).
- Click the Jak and Daxter logo on the left sidebar, then click `Advanced`, then click `Open Game Data Folder`. Copy the `iso_data` folder from this directory.
- Back in the OpenGOAL Launcher, click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- In the bottom right corner, click `Advanced`, then click `Open Game Data Folder`.
- Paste the `iso_data` folder you copied earlier.
- Back in the OpenGOAL Launcher, click the Jak and Daxter logo on the left sidebar.
- Click `Features` in the bottom right corner, then click `Mods`, then under `Installed Mods`, click `ArchipelaGOAL`.
- In the bottom right corner, click `Advanced`, then click `Compile`.

### The Text Client Says "Error reading game memory!" or "Error sending data to compiler"

If at any point the text client says this, you will need to restart the **all** of these applications.

- Close all open windows: the client, the compiler, and the game.
- Run the OpenGOAL Launcher, then click `Features`, then click `Mods`, then click `ArchipelaGOAL`.
- Click `Advanced`, then click `Play in Debug Mode`.
- Click `Advanced`, then click `Open REPL`.
- Then close and reopen the Jak and Daxter Client from the Archipelago Launcher.
- Once these are done, you can enter `/repl status` and `/memr status` in the text client to verify.

### The Client Cannot Open A REPL Connection

If the client cannot open a REPL connection to the game, you may need to check the following steps:

- Ensure you are not hosting anything on ports `8181` and `8112`. Those are for the REPL (goalc) and the game (gk) respectively.
- Ensure that Windows Defender and Windows Firewall are not blocking those programs from hosting or listening on those ports.
- You can use Windows Resource Monitor to verify those ports are open when the programs are running.
- Ensure that you only opened those ports for your local network, not the wider internet.

## Known Issues

- The game needs to boot in debug mode in order to allow the compiler to connect to it. **Clicking "Play" on the mod page in the OpenGOAL Launcher will not work.**
- The Compiler console window is orphaned once you close the game - you will have to kill it manually when you stop playing.
- The console windows cannot be run as background processes due to how the REPL works, so the best we can do is minimize them.
- Orbsanity checks may show up out of order in the text client.
- Large item releases may take up to several minutes for the game to process them all. Item Messages will usually take longer to appear than Items themselves.
- In Lost Precursor City, if you die in the Color Platforms room, the game may crash after you respawn. The cause is unknown.
- Darkness Trap may cause some visual glitches on certain levels. This is temporary, and terrain and object collision are unaffected.
