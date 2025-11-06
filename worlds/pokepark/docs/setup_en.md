# Pokepark Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Dolphin
- Any unmodified Pokepark ISO
- [pokeparkrando Patcher](https://github.com/Mekurushi/pokeparkrando/releases/latest)
- [Poptracker](https://github.com/Mekurushi/pokepark_ap_poptracker/releases/latest) (optional)

## Installation

1. Install the latest version of Archipelago.
2. Download `pokepark.apworld` and put it in your `Archipelago/custom_worlds/` folder.


## Generating a Game

1. Create your player options YAML file. A sample YAML is included.
2. Gather the YAMLs of all players into the `Archipelago/Players` folder.
3. Run the Archipelago Launcher and select Generate.
4. A zip file will be created in the `Archipelago/output` folder. Upload this
   to [the Archipelago website](https://archipelago.gg/uploads) to host your game.

## Obtain your patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your patch file should have a .appkprk extension.

## Playing a Game

1. Patch your unmodified Pokepark ISO using the Pokeparkrando Patcher and the provided patch file.
2. Launch the patched Pokepark ISO (which will be named after the patch file) with Dolphin.
3. Start a new save slot. You should spawn in the Treehouse (Meeting Place).
4. Launch the Pokepark Archipelago Client and connect to the hosted server.
