# Mega Man X3 setup guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- [SNI](https://github.com/alttpo/sni/releases). This is automatically included with your Archipelago installation above.
- Software capable of loading and playing SNES ROM files:
   - [snes9x-nwa](https://github.com/Skarsnik/snes9x-emunwa/releases)
   - [snes9x-rr](https://github.com/gocha/snes9x-rr/releases)
   - [BSNES-plus](https://github.com/black-sliver/bsnes-plus). **Note:** Do not reset within the emulator. It will cause 
   RAM corruption.
- Your Mega Man X3 US ROM file from the original cartridge or extracted from the Legacy Collection. Archipelago can't 
provide these.
   - SNES US MD5: `cfe8c11f0dce19e4fa5f3fd75775e47c`
   - Legacy Collection US MD5: `ff683b75e75e9b59f0c713c7512a016b`

## Optional Software
- [Map & Level tracker for Mega Man X3 Archipelago](https://github.com/BrianCumminger/megamanx3-ap-poptracker/releases), 
para usar con [PopTracker](https://github.com/black-sliver/PopTracker/releases)
- [Emulator Lua Scripts](https://github.com/Coltaho/emulator_lua_scripts), 
for [snes9x-rr](https://github.com/gocha/snes9x-rr/releases) and [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory)

### Alternative ways of playing
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) has reports of working fine but it isn't an officially endorsed way to play the game by the developer. Proceed at your own risk.
- RetroArch doesn't have any report of working fine. Proceed at your own risk.
- sd2snes/FX Pak don't work with this game due to limitations on the cartridge's internal hardware.

## Installation process

1. Download and install [Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **The installer 
   file is located in the assets section at the bottom of the version information.**
2. If you are using an emulator, you should assign your Lua capable emulator as your default program for launching ROM
   files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .sfc files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for your emulator's `.exe` file and click **Open**. This file should be located inside the folder you
       extracted in step one.

## Setup your YAML

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the [Mega Man X3 Player Options Page](/games/Mega%20Man%20X3%20/player-options)

## Joining a MultiWorld Game

### Get your Mega Man X3 patch

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apmmx3` extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should automatically launch the
client, and will also create your ROM in the same place as your patch file.

### Connect to the multiworld

When the client launched automatically, SNI should have also automatically launched in the background. If this is its
first time launching, you may be prompted to allow it to communicate through the Windows Firewall.

To connect the client with the server, write `<address>:<port>` in the text box located at the top and hit Enter (if the
server has a password, then write `/connect <address>:<port> [password]` in the bottom text box)

Each emulator requires following a specific procedure to be able to play. Follow whichever fits your preferences.

#### snes9x-nwa

1. Click on the Network Menu and check **Enable Emu Network Control**
2. Load your ROM file if it hasn't already been loaded.
3. The emulator should automatically connect while SNI is running.

#### snes9x-rr

1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Select the connector lua file included with your client
    - Look in the Archipelago folder for `/SNI/lua/`.
6. If you see an error while loading the script that states `socket.dll missing` or similar, navigate to the folder of 
the lua you are using in your file explorer and copy the `socket.dll` to the base folder of your snes9x install.

#### BSNES-Plus

1. Load your ROM file if it hasn't already been loaded.
2. The emulator should automatically connect while SNI is running.

## Final notes

When the client shows both SNES Device and Server as connected, you're ready to begin playing. Congratulations on
successfully joining a multiworld game! You can execute various commands in your client. For more information regarding
these commands you can use `/help` for local client commands and `!help` for server commands.
