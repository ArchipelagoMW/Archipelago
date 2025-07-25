# The Grinch - Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Please use version 0.6.2 or later for integrated
BizHawk support.
- Legally obtained NTSC Bin ROM file, probably named something like `Grinch, The (USA) (En,Fr,Es).bin`.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) Version 2.9.1 is supported, but I can't promise if any version is stable or not.
- The latest `thegrinch.apworld` file. You can find this on the [Releases page](https://github.com/MarioSpore/Grinch-AP/releases/latest). Put this in your `Archipelago/custom_worlds` folder.

## Configuring BizHawk



## Configuring your Config (.yaml) file

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player options page on the website allows you to configure your personal
options and export a config file from them: [The Grinch Player Options Page](../player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do
so on the YAML Validator page: [YAML Validation page](/check)

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whomever is
hosting. Once that is done, the host will provide you with either a link to download your patch
file, or with a zip file containing everyone's patch files. Your patch file should have a `.apgrinch`
extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should
automatically launch the client, and will also create your ROM in the same place as your patch file.

### Connect to the Multiserver

Once both the client and the emulator are started, they must be connected. **This should happen automatically.**
However, if the lua script window doesn't appear, then within the emulator click
on the "Tools" menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua
script. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the text field on top and
press enter (if the server uses a password, type in the bottom text field
`/connect <address>:<port> [password]`)

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Upload the config files to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
3. Wait a moment while the seed is generated.
4. When the seed is generated, you will be redirected to a "Seed Info" page.
5. Click "Create New Room". This will take you to the server page. Provide the link to this page to
  your players, so they may download their patch files from there.
6. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the
  progress of all players in the game. Any observers may also be given the link to this page.
7. Once all players have joined, you may begin playing.