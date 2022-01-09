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

Download latest release on [Timespinner Randomizer Releases](https://github.com/JarnoWesthof/TsRandomizer/releases) you
can find the .zip files on the releases page, download the zip for your current platform. Then extract the zip to the
folder where your Timespinner game is installed. Then just run TsRandomizer.exe (on windows) or
TsRandomizerItemTracker.bin.x86_64 (on linux) or TsRandomizerItemTracker.bin.osx (on mac) instead of Timespinner.exe to
start the game in randomized mode, for more info see
the [ReadMe for TsRandomizer](https://github.com/JarnoWesthof/TsRandomizer)

## Joining a MultiWorld Game

1. Run TsRandomizer.exe
2. Select "New Game"
3. Switch "<< Select Seed >>" to "<< Archiplago >>" by pressing left on the controller or keyboard
4. Select "<< Archiplago >>" to open a new menu where you can enter your Archipelago login credentails
    * NOTE: the input fields support Ctrl + V pasting of values
5. Select "Connect"
6. If all went well you will be taken back the difficulty selection menu and the game will start as soon as you select a
   difficulty

## Where do I get a config file?

The [Timespinner Player Settings Page](https://archipelago.gg/games/Timespinner/player-settings) on the website allows
you to configure your personal settings and export a config file from them.

* The Timespinner Randomizer option "StinkyMaw" is currently always enabled for Archipelago generated seeds
* The Timespinner Randomizer options "ProgressiveVerticalMovement" & "ProgressiveKeycards" are currently not supported
  on Archipelago generated seeds