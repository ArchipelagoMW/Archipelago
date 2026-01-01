# Timespinner Randomizer Setup Guide

## Required Software

- [Timespinner (Steam)](https://store.steampowered.com/app/368620/Timespinner/)
  , [Timespinner (Humble)](https://www.humblebundle.com/store/timespinner)
  or [Timespinner (GOG)](https://www.gog.com/game/timespinner) (other versions are not supported)
- [Timespinner Randomizer](https://github.com/Jarno458/TsRandomizer)

## General Concept

The Timespinner Randomizer loads Timespinner.exe from the same folder, and alters its state in memory to allow for
randomization of the items

## Installation Procedures

Download latest release on [Timespinner Randomizer Releases](https://github.com/Jarno458/TsRandomizer/releases) you
can find the .zip files on the releases page. Download the zip for your current platform. Then extract the zip to the
folder where your Timespinner game is installed. Then just run TsRandomizer.exe (on Windows) or
TsRandomizer.bin.x86_64 (on Linux) or TsRandomizer.bin.osx (on Mac) instead of Timespinner.exe to start the game in
randomized mode. For more info see the [ReadMe](https://github.com/Jarno458/TsRandomizer)

## Joining a MultiWorld Game

1. Run TsRandomizer.exe
2. Select "New Game"
3. Switch "<< Select Seed >>" to "<< Archipelago >>" by pressing left on your controller or keyboard
4. Select "<< Archipelago >>" to open a new menu where you can enter your Archipelago login credentials
    * NOTE: the input fields support Ctrl + V pasting of values
5. Select "Connect"
6. If all went well you will be taken back to the difficulty selection menu and the game will start as soon as you
   select a difficulty

## Where do I get a config file?

The [Player Options](/games/Timespinner/player-options) page on the website allows you to
configure your personal options and export them into a config file

* The Timespinner Randomizer option "StinkyMaw" is currently always enabled for Archipelago generated seeds
* The Timespinner Randomizer options "ProgressiveVerticalMovement" & "ProgressiveKeycards" are currently not supported
  on Archipelago generated seeds
