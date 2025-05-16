# Setup Guide for Gauntlet Legends in Archipelago

## Required Software

- Retroarch: [Standalone](https://www.retroarch.com/?page=platforms), [Steam](https://store.steampowered.com/app/1118310/RetroArch/)
- The built-in Gauntlet Legends Client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
- A US copy of Gauntlet Legends for the N64

## Configuring Retroarch

### Enabling Network Commands

You must go to Settings -> User Interface and turn the Show Advanced Settings to On. 
Then in Settings -> Network, you must also turn On Network Commands. 
Leave the port as the default.

### Selecting a Core

When selecting a core, make sure to select Mupen64-plus-next core.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your options by visiting the 
[Gauntlet Legends Options Page](/games/Gauntlet%20Legends/player-options)

## Joining a MultiWorld Game

### Obtain your N64 patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting.
The host generating does not need a copy of Gauntlet Legends to be able to generate with a Gauntlet Legends yaml.

Once that is done, the host will provide you with either a link to download your data file, 
or with a zip file containing everyone's data files. Your data file should have a `.apgl` extension.


Double-click on your `.apgl` file to start the ROM patch process. Once the process is finished, the client will be started automatically.

### Connect to the Multiserver

This game uses its own custom client, named Gauntlet Legends Client.
Retroarch is only emulator this client will accept.

Once both the client and the emulator are started, you must connect them. Once your ROM is open in Retroarch,
as long as the client is open they will be connected to each other.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`).

The client will prompt you for your slot name, once you enter and submit it, you will be connected to the lobby.
