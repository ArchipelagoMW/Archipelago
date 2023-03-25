# Stardew Valley Randomizer Setup Guide

## Required Software

- DLC Quest on PC (Recommended: [Steam version](https://store.steampowered.com/app/230050/DLC_Quest/))
- BepinEx ([Used as a modloader for DLC Quest](https://github.com/agilbert1412/DLCQuestipelago/releases/tag/BepInEx))
- [DLCQuestipelago](https://github.com/agilbert1412/DLCQuestipelago/releases)

## Optional Software
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (Only for the TextClient)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your settings by visiting the [DLC Quest Player Settings Page](../player-settings)

## Joining a MultiWorld Game

### Installing the mod

- Create a folder on your computer intended to hold the modded version of DLC Quest. Suggested Name: DLCQuestipelago
- Locate your DLC Quest installation and copy the entirety of its content into your DLCQuestipelago folder
  ![image](https://i.imgur.com/m7OM7Fu.png)


- Extract the BepInEx Modloader by extracting all of the BepInEx files into your DLCQuestipelago folder.
  ![image](https://i.imgur.com/oyL941C.png)


- Run the executable file "BepInEx.NetLauncher.exe" Once, to generate relevant files and folders
- Download and extract the [DLCQuestipelago](https://github.com/ArchipelagoMW/Archipelago/releases) into the "BepInEx\plugins\" subfolder
  ![image](https://i.imgur.com/CUr3Ust.png)
- **IMPORTANT**: Make sure the folder structure visible in the screenshots is replicated **perfectly**

### Connect to the MultiServer

Locate the file "ArchipelagoConnectionInfo.json", that should be in "DLCQuestipelago\BepInEx\plugins\DLQuestipelago\" (visible in the last screenshot of the previous step)

Edit this file with your text editor of choice, and fill the relevant fields for your server ip, port, slotname and password (optional)

![image](https://i.imgur.com/fykpEgt.png)

Your game will connect automatically to Archipelago when launched using these credentials. It will also generate a save game linked to these credentials, so you do not need to worry about simultaneous saves overwriting each other. will never need to enter this information again for this character.

You can now launch the executable "BepInEx.NetLauncher.exe" to launch DLCQuest with the mod installed. If done correctly

### Interacting with the MultiWorld from in-game

You cannot send commands to the server or chat with the other players from DLC Quest, as the game lacks a proper way to input these.
You can keep track of the server activity in your BepInEx console, as Archipelago chat messages will be displayed in it.