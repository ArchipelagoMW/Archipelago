# Setup Guide for Prodigal Archipelago

## Required Software

- [Prodigal](https://store.steampowered.com/app/1393820/Prodigal/) (Steam version only)
- [BepInEx 5](https://github.com/BepInEx/BepInEx/releases/) -- make sure you get version 5 and not the pre-release of 6
- [Prodigal Archipelago Mod](https://github.com/randomsalience/ProdigalArchipelago/releases/)

## Installation

1. Unzip BepInEx into the folder containing the Prodigal executable.
2. Run Prodigal once to complete the BepInEx setup. Once it reaches the menu, you can close the game.
3. Unzip the Prodigal Archipelago mod and place the `Archipelago` folder into the `BepInEx/plugins` folder.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the [settings page](/games/Prodigal/player-settings).

## Joining a multiworld game

Start a new game of Prodigal and select the Archipelago option. This brings up the connection screen. Enter the address of the server, the port number, your slot name, and optionally a password, then select Start. You should now be connected to Archipelago.

## Tracking

The mod includes a map tracker. The map screen shows dots in all locations which contain items. A dot is colored green if all the items may be obtained, yellow if some may be obtained, orange if some may be obtained out of logic by spending keys, and red if no items may be obtained. Hovering over a dot with the mouse shows a list of all checks at that location and tells you which ones may be obtained.