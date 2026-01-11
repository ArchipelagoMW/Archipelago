# Ratchet and Clank 3 Up your Arsenal Guide

This guide is meant to help you get up and running with Ratchet & Clank 3 in your Archipelago run.

## Requirements

The following are required in order to play Ratchet & Clank 3 in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.5.0 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Ratchet & Clank 3 apworld](https://github.com/Taoshix/Archipelago-RaC3/releases).
- [PCSX2 Emulator](https://pcsx2.net/downloads/). Must be v1.7 or higher for the required PINE support.
- A Ratchet & Clank 3 US ISO (`SCUS-97353`)

## AP World Installation

1. Unzip the downloaded Ratchet & Clank 3 apworld zip file
2. Double-click the `rac3.apworld` to install it to your local Archipelago instance

## PCSX2 Settings
- Enable PINE in PCSX2
  - In PCSX2, Under Tools, **Check** Show Advanced Settings
  - In PCSX2, System -> Settings -> Advanced tab -> PINE Settings,
    **Check** Enable and ensure Slot is set to 28011

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your options by visiting
the [Ratchet and Clank 3 Options Page](/games/Ratchet%20and%20Clank%203%20Up%20your%20Arsenal/player-options).

### Connect to the MultiServer

1. Launch PCSX2, boot your copy of RaC3
    - Start a new file, watch/skip the intro cutscene and pause the game when you load in on Veldin

2. Launch Ratchet and Clank 3 client in the Archipelago Launcher
    - Under address input your archipelago connection address (ie: archipelago.gg:51780)


    - PCSX2 must be open before the RaC3 client is opened or it will give an error
    - Items will begin being sent to the player before they are in their save file if the client is connected first

