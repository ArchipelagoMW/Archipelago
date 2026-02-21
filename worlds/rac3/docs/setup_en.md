# Ratchet and Clank 3 Up your Arsenal Guide

This guide is meant to help you get up and running with Ratchet and Clank 3 in your Archipelago run.

## Requirements

The following are required in order to play Ratchet and Clank 3 in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.5.0 or higher (the latest version is recommended).\
  **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Ratchet and Clank 3 apworld](https://github.com/Taoshix/Archipelago-RaC3/releases).
- [PCSX2 Emulator](https://pcsx2.net/downloads/). Must be v1.7 or higher for the required PINE support.
- A Ratchet and Clank 3 US ISO (`SCUS-97353`)

## AP World Installation

1. Unzip the downloaded Ratchet and Clank 3 apworld zip file
2. Double-click the `rac3.apworld` to install it to your local Archipelago instance

## PCSX2 Settings

- Enable PINE in PCSX2
    - In PCSX2, Under Tools, **Check** Show Advanced Settings
    - In PCSX2, System → Settings → Advanced tab → PINE Settings,
      **Check** Enable and ensure Slot is set to 28011

Make sure you restart PCSX2 afterwards.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your options by visiting
the [Ratchet and Clank 3 Options Page](/games/Ratchet%20and%20Clank%203/player-options).

### Connect to the MultiServer

1. Launch PCSX2, boot your copy of RaC3

2. Launch Ratchet and Clank 3 client in the Archipelago Launcher
    - In the address field, enter your Archipelago connection address (e.g., archipelago.gg:51780 or localhost:38281). Then, type your player name (as specified in your YAML file, e.g., Player1) into the client.
    - Start a new save file by choosing "New Game" from the main menu, then select your preferred save slot. Watch/skip the intro cutscene once the game starts. If the client is connected first, items will begin being sent to the player even if you are still on the main menu but you will not receive them until you are actually in-game.
    - To apply cosmetics, reload the save file by pausing and going into options and then load file with the same slot.


## Troubleshooting
For common issues, check the [FAQ](https://github.com/Taoshix/Archipelago-RaC3/blob/staging/worlds/rac3/docs/frequently_asked_questions_Rac3_en.md).

If you need further help, join the [Archipelago Discord](https://discord.gg/archipelago) and visit the `[PS2] Ratchet and Clank 3: Up Your Arsenal` thread in the `future-game-design` forum channel (located at the bottom).

