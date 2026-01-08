# Minit Randomizer Setup Guide

## Required Software

- Minit installed
	- Tested with [Steam](https://store.steampowered.com/app/609490/Minit/), and Epic games.
	- The itch.io release is not supported currently.
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your options by visiting the [Minit Player Options Page](../player-options)

## Joining a MultiWorld Game

### For Connecting
* Run ArchipelagoLauncher.exe
* Open the "Minit Client" through the Launcher
* Use the top bar to enter the host and port of the Archipelago server running already
  (ex. "localhost:38281" if you are hosting it locally and your port is 38281).
* When prompted for you Slot Name, enter whatever your username in the .yaml file is,
  if left default it will likely be "Player1".
* You now have the proxy client connected to the AP server

### For Patching
In the client there is a `/Patch` command you can use which will automatically create a patched data file
if needed and launch the game when the patching is complete.

The entire process should be automated but in case you need the information for debugging or alternate setups:
* The location of your install will be saved in the `host.yaml` configuration file in your Archipelago Install
* The patched data file will be saved in your minit install folder as `ap_v1.0_data.win`. If you need to manually
  launch then the launch args `-game ap_v1.0_data.win` will work both in a terminal and in steam launch args
  (swap the `v1.0` version for whatever patch version it is).
* If the client does not have access to that folder unexpected things may happen, so having a copy of your Minit folder
  for AP and pointing it there may be safer.
