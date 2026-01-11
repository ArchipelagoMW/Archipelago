# Setup Guide for Metroid Fusion Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prerequisite installer first, which can also be found at the above link.
- The built-in Bizhawk client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
- A US copy of Mario & Luigi: Superstar Saga

## Optional Software

- [Poptracker](https://github.com/black-sliver/PopTracker/releases)
  - [Metroid Fusion Autotracker](https://github.com/RunInAWeek/Metroid-Fusion-AP-Tracker/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your options by visiting the 
[Metroid Fusion Options Page](/games/Metroid Fusion/player-options)

## Joining a MultiWorld Game

### Obtain your GBA patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apmetfus` extension.

Double-click on your `.apmetfus` file to start your client and start the ROM patch process. Once the process is finished, the client and the emulator will be started automatically (if you associated the extension
to the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click on the "Tools"
menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)
