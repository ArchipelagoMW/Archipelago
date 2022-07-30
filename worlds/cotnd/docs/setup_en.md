# Crypt of the NecroDancer Setup Guide

## Required Software

- Crypt of the NecroDancer (CotND) on PC, updated to at least version 3.0.0.
- The Archipelago integration mod for CotND. The `.necromod` file can be downloaded [here](https://github.com/espeon65536/APNecrodancer/releases).
- The ArchipelagoCotNDClient.exe that installs with Archipelago.

## Computer Requirements

Although CotND supports both 32-bit and 64-bit systems, Archipelago only officially supports 64-bit systems. This means that
you won't be able to play the randomizer on a 32-bit computer.

## Installation Procedure and Configuration

This guide was written before the Lua modding workshop was available for CotND. If you're reading this guide after the workshop
is available, just download the Archipelago mod from the workshop and skip to step 4. 
1. Navigate to the NecroDancer local data folder on your computer.
   - On Windows, press Win + R and type `%LOCALAPPDATA%\NecroDancer`.
   - On Mac, go to `~/Library/Application Support/NecroDancer`.
   - On Linux, go to `~/.local/share/NecroDancer`.
2. Place the `.necromod` file in the `mods` directory. If it doesn't already exist, create it.
3. Navigate to your Steam directory and go to `Steam/userdata/247080/remote`. Delete `SynchronyConfig.lua` from this directory.
   This forces the game to update the file, which will load the mod as part of the game.
4. Right-click CotND in your Steam library and choose "Manage > Browse local files".
5. Open the Necrodancer64 folder and open `config.json` in a text editor of your choice. Unfortunately, this file is poorly
   formatted, since it's automatically generated.
6. Search for `scriptWhitelist` in the file. You should find something that looks like this:
```json
"scriptWhitelist":["necro.*","system.game.Audio","system.game.Bitmap",...
```
   Add "system.file.Storage" to the start of this list, so it looks like this:
```json
"scriptWhitelist":["system.file.Storage","necro.*","system.game.Audio","system.game.Bitmap",...
```
   This allows the Archipelago mod to read and write files to the local data folder, which is necessary for communication between
   the game and client. This functionality isn't enabled by default; this addition permits it to be used.

## Joining a Multiworld Game

1. Start the game with the mod active. Upon loading into the lobby, the game should display "Connect to server" in the chat.
   (All chat messages can be dismissed with Escape.)
2. Run ArchipelagoCotNDClient.exe.
3. Enter the server address in the top bar and click Connect.
4. When prompted, enter your slot name as configured in your YAML, and the password if necessary.
5. Once the client connects to the server and begins communicating with the game, a message will display in the CotND chat
   listing the characters you have access to.
6. You can now begin an All Zones run with any of the currently available characters.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. Player settings page: [Crypt of the NecroDancer Player Settings Page](/games/Crypt%20of%20the%20NecroDancer/player-settings)

**Important**: The option `available_characters` will likely be missing from your YAML after downloading. This option is quite important
as it allows you to control the characters available for gameplay. You can add it like this:
```yaml
available_characters: [Cadence, Melody, Aria, Nocturna]
```

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)
