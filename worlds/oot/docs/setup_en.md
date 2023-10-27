# Setup Guide for Ocarina of Time Archipelago

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- BizHawk: [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
  (select `Ocarina of Time Client` during installation).
- An Ocarina of Time v1.0 ROM.

## Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

- (≤ 2.8) Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". Then restart EmuHawk. This is required for the Lua script to function correctly.
  **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs** 
  **of newer versions of EmuHawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load** 
  **"NLua+KopiLua" until this step is done.**
- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to
  continue playing in the background, even if another window is selected.
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want
  to disable most of these, which you can do quickly using `Esc`.
- If playing with a controller, when you bind controls, disable "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right"
  as these interfere with aiming if bound. Set directional input using the Analog tab instead.
- Under N64 enable "Use Expansion Slot". This is required for savestates to work.
  (The N64 menu only appears after loading a ROM.)

It is strongly recommended to associate N64 rom extensions (\*.n64, \*.z64) to the EmuHawk we've just installed.
To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with...", unfold
the list that appears and select the bottom option "Look for another application", then browse to the BizHawk folder
and select EmuHawk.exe.

An alternative BizHawk setup guide as well as various pieces of troubleshooting advice can be found
[here](https://wiki.ootrandomizer.com/index.php?title=Bizhawk).

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. Player settings page: [Ocarina of Time Player Settings Page](/games/Ocarina%20of%20Time/player-settings)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

### Obtain your OOT patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apz5` extension.

Double-click on your `.apz5` file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically (if you associated the extension
to the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Navigate to your Archipelago install folder,
then to `data/lua`, and drag+drop the `connector_oot.lua` script onto the main EmuHawk window. (You could instead open
the Lua Console manually, click `Script` 〉 `Open Script`, and navigate to `connector_oot.lua` with the file picker.)

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

Now you are ready to start your adventure in Hyrule.
