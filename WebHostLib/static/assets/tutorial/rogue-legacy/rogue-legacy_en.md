# Rogue Legacy Randomizer Setup Guide

## Required Software

- Rogue Legacy Randomizer from
  the [Rogue Legacy Randomizer Releases Page](https://github.com/ThePhar/RogueLegacyRandomizer/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

you can customize your settings by visiting the [Rogue Legacy Settings Page](/games/Rogue%20Legacy/player-settings).

### Connect to the MultiServer

Once in game, press the start button and the AP connection screen should appear. You will fill out the hostname, port,
slot name, and password (if applicable). You should only need to fill out hostname, port, and password if the server
provides an alternative one to the default values.

### Play the game

Once you have entered the required values, you go to Connect and then select Confirm on the "Ready to Start" screen. Now
you're off to start your legacy!

## Manual Installation

In order to run Rogue Legacy Randomizer you will need to have Rogue Legacy installed on your local machine. Extract the
Randomizer release into a desired folder **outside** of your Rogue Legacy install. Copy the following files from your
Rogue Legacy install into the main directory of your Rogue Legacy Randomizer install:

- DS2DEngine.dll
- InputSystem.dll
- Nuclex.Input.dll
- SpriteSystem.dll
- Tweener.dll

And copy the directory from your Rogue Legacy install as well into the main directory of your Rogue Legacy Randomizer
install:

- Content/

Then copy the contents of the CustomContent directory in your Rogue Legacy Randomizer into the newly copied Content
directory and overwrite all files.

**BE SURE YOU ARE REPLACING THE COPIED FILES IN YOUR ROGUE LEGACY RANDOMIZER DIRECTORY AND NOT REPLACING YOUR ROGUE
LEGACY FILES!**
