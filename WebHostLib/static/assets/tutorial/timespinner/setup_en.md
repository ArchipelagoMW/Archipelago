# Timespinner Randomizer Setup Guide

## Required Software

- [Timespinner (steam)](https://store.steampowered.com/app/368620/Timespinner/), [Timespinner (humble)](https://www.humblebundle.com/store/timespinner) or [Timespinner (GOG)](https://www.gog.com/game/timespinner)
- [Timespinner Randomizer](https://github.com/JarnoWesthof/TsRandomizer)

## General Concept

The timespinner Randomizer loads Timespinner.exe from the same folder, and alters its state in memory to allow for randomization of the items

## Installation Procedures

Download latest release on [Timespinner Randomizer Releases](https://github.com/JarnoWesthof/TsRandomizer/releases) you can find the .zip files on the releases page, download the zip for your current platform. Then extract the zip to the folder where your Timespinner game is installed. Then just run TsRandomizer.exe (on windows) or TsRandomizerItemTracker.bin.x86_64 (on linux) or TsRandomizerItemTracker.bin.osx (on mac) instead of Timespinner.exe to start the game in randomized mode, for more info see the [ReadMe](https://github.com/JarnoWesthof/TsRandomizer)
    
## Joining a MultiWorld Game

1. Run TsRandomizer.exe
2. Select "New Game"
3. Switch "<< Select Seed >>" to "<< Archiplago >>" by pressing left on the controller or keyboard 
4. Select "<< Archiplago >>" to open a new menu where you can enter your Archipelago login credentails
	* NOTE: the input fields support Ctrl + V pasting of values
5. Select "Connect"
6. If all went well you will be taken back the difficulty selection menu and the game will start as soon as you select a difficulty

## YAML Settings
An example YAML would look like this:
```yaml
description: Default Timespinner Template
name: Lunais{number} # Your name in-game. Spaces will be replaced with underscores and there is a 16 character limit
game:
  Timespinner: 1
requires:
  version: 0.2.3
Timespinner:
  StartWithJewelryBox: 'true'
  DownloadableItems: 'true'
  FacebookMode: 'false'
  StartWithMeyef: 'false'
  QuickSeed: 'false'
  SpecificKeycards: 'true'
  Inverted: random
  DeathLink: 'false'
  Cantoran: 'false'
  DamageRando: 'false'
  GyreArchives: 'false'
  LoreChecks: 'false'
```
* All Options are either enabled or not, if values are specified for both true & false the generator will select one based on weight
* The Timespinner Randomizer option "StinkyMaw" is currently always enabled for Archipelago generated seeds
* The Timespinner Randomizer options "ProgressiveVerticalMovement" & "ProgressiveKeycards" are currently not supported on Archipelago generated seeds