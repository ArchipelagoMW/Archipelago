# Terraria for Archipelago Setup Guide

## Required Software

Download and install [Terraria](https://store.steampowered.com/app/105600/Terraria/)
and [TModLoader](https://store.steampowered.com/app/1281930/tModLoader/) on Steam

## Installing the Archipelago Mod

Subscribe to [the mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2922217554) on Steam.

This mod might not work with mods that significantly alter progression, and is very unlikely to work
with mods that significantly modify vanilla features. Feel free to use your preferred utility mods
to speed up gameplay.

Mods known to be incompatible:

* Boss Checklist
* Magic Storage

## Configuring your YAML File

### What is a YAML and why do I need one?

You can see the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here
on the Archipelago website to learn about why Archipelago uses YAML files and what they're for.

### Where do I get a YAML?

You can use the [game settings page for Terraria](/games/Terraria/player-settings) here
on the Archipelago website to generate a YAML using a graphical interface.

## Joining an Archipelago Game in Terraria

1. Launch TModLoader
2. In Workshop > Manage Mods, edit Archipelago Randomizer's settings
    * "Name" should be the player name you set when creating your YAML file
    * "Port" should be the port number associated with the Archipelago server. It will be a 4 or 5
    digit number.
    * If you're not hosting your game on the Archipelago website, change "Address" to the server's
    URL or IP address
3. Create a new character and world as normal (or use an existing one if you prefer).
4. Open the world in single player or multiplayer
5. When you're ready, open chat, and send "/apstart" to start the game
   
## Commands

While playing Archipelago, you can interact with the server using the commands listed in the
[commands guide](/tutorial/Archipelago/commands/en). As this game does not have an in-game text
client at the moment, you can optionally connect to the multiworld using the text client,
which can be found
in the [main Archipelago installation](https://github.com/ArchipelagoMW/Archipelago/releases) as
Archipelago Text Client to enter these commands.
