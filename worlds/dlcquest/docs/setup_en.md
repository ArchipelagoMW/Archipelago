# DLCQuest Randomizer Setup Guide

## Required Software

- DLC Quest on PC (Recommended: [Steam version](https://store.steampowered.com/app/230050/DLC_Quest/))
- [DLCQuestipelago](https://github.com/agilbert1412/DLCQuestipelago/releases)
- BepinEx (Used as a modloader for DLCQuest. The Mod release above includes BepInEx if you pick the full installer version)

## Optional Software
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (Only for the TextClient)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your options by visiting the [DLC Quest Player Options Page](/games/DLCQuest/player-options)

## Joining a MultiWorld Game

### Installing the mod

- Download the [DLCQuestipelago mod release](https://github.com/agilbert1412/DLCQuestipelago/releases). If this is your first time installing the mod, or if you are not comfortable with manually editing files, you should pick the Installer. It will handle most of the work for you


- Extract the .zip archive to a location of your choice


- Run "DLCQuestipelagoInstaller.exe"

![image](https://i.imgur.com/2sPhMgs.png)
- The installer should describe what it is doing each step of the way, and will ask for your input when necessary.
  - It will allow you to choose where to install your modded game, and offer a default location
  - It will **try** to find your DLCQuest game on your computer, and should it fail, it will ask you to input the path to it
  - It will offer the choice of creating a desktop shortcut for the modded launcher

### Connect to the MultiServer

- Locate the file "ArchipelagoConnectionInfo.json", at the root of your modded installation. You can edit this file with any text editor, and you need to enter the server ip address, port and your slotname into the relevant fields.


- Run BepInEx.NET.Framework.Launcher.exe. If you opted for a desktop shortcut, you will find it with an icon and a more recognizable name.
![image](https://i.imgur.com/ZUiFrhf.png)


- Your game should launch alongside a modloader console, which will contain important debugging information if you run into problems.
- The game should automatically connect, and attempt reconnecting if your internet or the server fails, during your playthrough.

### Interacting with the MultiWorld from in-game

You cannot send commands to the server or chat with the other players from DLC Quest, as the game lacks a proper way to input text.
You can keep track of the server activity in your BepInEx console, as Archipelago chat messages will be displayed in it.
You will need to use an [Archipelago Text Client](https://github.com/ArchipelagoMW/Archipelago/releases) if you want to send commands.