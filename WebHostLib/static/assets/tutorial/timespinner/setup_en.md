# Timespinner Randomizer Setup Guide

## Required Software

- One of:
    - Timespinner (steam) from: [Timespinner Steam Store Page](https://store.steampowered.com/app/368620/Timespinner/)
    - Timespinner (drm free) from: [Timespinner Humble Store Page](https://www.humblebundle.com/store/timespinner)
- Timespinner Randomizer from: [Timespinner Randomizer GitHub](https://github.com/JarnoWesthof/TsRandomizer)

## General Concept

The Timespinner Randomizer loads Timespinner.exe from the same folder, and alters its state in memory to allow for
randomization of the items.

## Installation Procedures

Download latest version of Timespinner randomizer you can find the .zip files on the releases page, download the zip for
your current platform. Then extract the zip to the folder where your Timespinner game is installed. Then just run
TsRandomizer.exe instead of Timespinner.exe to start the game in randomized mode, for more info see the Timespinner
randomizer readme.

Timespinner Randomizer downloads
page: [Timespinner Randomizer Releases](https://github.com/JarnoWesthof/TsRandomizer/releases)

Timespinner Randomizer readme page: [Timespinner Randomizer GitHub](https://github.com/JarnoWesthof/TsRandomizer)

## Joining a MultiWorld Game

1. Run TsRandomizer.exe
2. Select "New Game"
3. Switch "<< Select Seed >>" to "<< Archiplago >>" by pressing left on the controller or keyboard
4. Select "<< Archiplago >>" to open a new menu where you can enter your Archipelago login credentails
    * NOTE: the input fields support Ctrl + V pasting of values
5. Select "Connect"
6. If all went well you will be taken back the difficulty selection menu and the game will start as soon as you select a
   difficulty

## YAML Settings

An example YAML would look like this:

```yaml
description: Default Timespinner Template
name: Lunais{number} # Your name in-game. Spaces will be replaced with underscores and there is a 16 character limit
game:
  Timespinner: 1
requires:
  version: 0.1.8
Timespinner:
  StartWithJewelryBox: # Start with Jewelry Box unlocked
    false: 50
    true: 0
  DownloadableItems: # With the tablet you will be able to download items at terminals
    false: 50
    true: 50
  FacebookMode: # Requires Oculus Rift(ng) to spot the weakspots in walls and floors
    false: 50
    true: 0
  StartWithMeyef: # Start with Meyef, ideal for when you want to play multiplayer
    false: 50
    true: 50
  QuickSeed: # Start with Talaria Attachment, Nyoom!
    false: 50
    true: 0
  SpecificKeycards: # Keycards can only open corresponding doors
    false: 0
    true: 50
  Inverted: # Start in the past
    false: 50
    true: 50
```

* All Options are either enabled or not, if values are specified for both true & false the generator will select one
  based on weight
* The Timespinner Randomizer option "StinkyMaw" is currently always enabled for Archipelago generated seeds
* The Timespinner Randomizer options "ProgressiveVerticalMovement" & "ProgressiveKeycards" are currently not supported
  on Archipelago generated seeds