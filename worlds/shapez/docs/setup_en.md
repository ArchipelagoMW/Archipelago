# Setup Guide for shapez: Archipelago

## Quick Links

- Game Info Page
    * [English](/games/shapez/info/en)
    * [Deutsch](/games/shapez/info/de)
- [Player Options Page](/games/shapez/player-options)

## Required Software

- An installable, up-to-date PC version of shapez ([Steam](https://store.steampowered.com/app/1318690/shapez/)).
- The shapezipelago mod from the [mod.io page](https://mod.io/g/shapez/m/shapezipelago).

## Optional Software

- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    * (Only for the TextClient)
    * (You can alternatively use the built-in console by launching the game with the `-dev` parameter and typing 
      `AP.sendAPMessage("<message>"")`)
- Universal Tracker (check UT's channel in the discord server for more information and instructions)

## Installation

As the game has a built-in mod loader, all you need to do is copy the `shapezipelago@X.X.X.js` mod file into the mods
folder. If you don't know where that is, open the game, click on `MODS`, and then `OPEN MODS FOLDER`.

It is recommended to go into the settings of the game and disable `HINTS & TUTORIALS` in the `USER INTERFACE` tab, as 
this setting will disable the upgrade shop until you complete a few levels.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the 
[shapez Player Options Page](/games/shapez/player-options)

## Joining a MultiWorld Game

1. Open the game.
2. In the main menu, type the slot name, address, port, and password (optional) into the input box.
3. Click "Connect".
   - To disconnect, just press this button again.
   - The status of your connection is shown right next to the button.
4. Create a new game.

After creating the save file and returning to the main menu, opening the save file again will automatically reconnect. 

### The MultiWorld changed its port/address, how do I reconnect correctly with my existing save file? 

Repeat steps 1-3 and open the existing save file. This will also overwrite the saved connection details, so you will 
only have to do this once. 
