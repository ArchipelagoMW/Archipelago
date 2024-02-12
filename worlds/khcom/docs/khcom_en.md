# Kingdom Hearts Chain of Memories Randomizer Setup Guide

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software
- BizHawk: [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
- A Kingdom Hearts Chain of Memories (US) ROM file. The Archipelago community cannot provide this.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your settings by visiting the [Kingdom Hearts Chain of Memories Settings Page](/games/Kingdom%20Hearts%20Chain%20of%20Memories/player-settings).

## Joining a MultiWorld Game

### Connect to the MultiServer

1. Open your Kingdom Hearts Chain of Memories (US) ROM in Emuhawk by navigating to `File > Open ROM` and selecting your Kingdom Hearts Chain of Memories (US) ROM file.
2. Open the LUA console in Emuhawk by navigating to `Tools > Lua Console`
3. In the Lua Console window, go to `Script > Open Script…`.
4. Navigate to your Archipelago installation and open `data/lua/connector_khcom.lua`.
5. Open your KHCOM Launcher from your Archipelago installation root folder or by using the Launcher
6. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.
7. When prompted, enter the slot name defined in your YAML.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)