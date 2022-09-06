# Overcooked! 2 Randomizer Setup Guide

## Quick Links
- [Main Page](../../../../games/Overcooked!%202/info/en)
- [Settings Page](../../../../games/Overcooked!%202/player-settings)
- [OC2-Modding GitHub](https://github.com/toasterparty/oc2-modding)

## Required Software

- Windows 10+ (Windows 7 requires extra installation steps, dm toasterparty if you exist)
- [Overcooked! 2](https://store.steampowered.com/bundle/13608/Overcooked_2___Gourmet_Edition/) for PC (only steam version has been tested so far, but others should work)
- [OC2-Modding Client](https://github.com/toasterparty/oc2-modding/releases)

## Overview

*OC2-Modding* is a general purpose modding framework which doubles as an Archipelago Network Client. It works by using Harmony to inject custom code into the game at runtime, so none of the game files are modified in any way.

When connecting to an archipelago session using the in-game login screen, a JSON manifest file containing all relevant game modifications is automatically downloaded and applied.

From this point, the game will communicate with the Archipelago service directly to manage sending/receiving items. Notifications of important events will appear in-game at the top of the screen.

Alternatively, solo seeds can be download and manually placed in the installation directory, thus not requiring sign-in to the Archipelago service.

## Installation Guide

### Install OC2Modding

1. Download and extract the contents of the latest [OC2-Modding Release](https://github.com/toasterparty/oc2-modding/releases) anywhere on your PC

2. Double-Click `oc2-modding-install.bat` follow the instructions

Once *OC2-Modding* is installed, you have successfuly installed everything you need to play/participate in Archipelago MultiWorld games.

### Uninstall OC2Modding

To uninstall *OC2-Modding*, simply navigate to your game's installation folder and run `oc2-modding-uninstall.bat`.

## Generate a MultiWorld Game

1. Visit the [Player Settings](../player-settings) page and configure the game-specific settings to taste.

2. Export your yaml file and use it to generate a new randomized game. (for how to generate an Archipelago game, refer to the [Archipelago Setup Guide](http://localhost/tutorial/Archipelago/setup/en).*).

## Joining a MultiWorld Game

1. Launch the game

2. When attempting to leave the the title screen and enter the main menu, the game will freeze and prompt you to sign in:

![Sign-In Screen](https://i.imgur.com/goMy7o2.png)

3. Sign-in with server address, username and password of the corresponding room you would like to joing.

Otherwise, if you just want to play the vanilla game without any modifications (of if you've manually installed a solo seed), you may press "Continue without Archipelago" button.

4. Upon successful connection to the Archipelago service, you will be granted access to the main menu. The game will act as though you are playing for the first time. *DO NOT FEAR*, your orginal save data has not been overwritten, the Overcooked Randomizer just uses a different tempoary directory for it's game save data.

## Auto-Complete

Since the goal of randomizer isn't to achieve new personal high score, players may find themselves waiting for a level timer to expire once they've met their objectives. A new feature called *Auto-Complete* has been added to automatically complete levels once a target star count has been achieved.

To enable *Auto-Complete*, press the `"Show"` button near the top of your screen to expand the modding controls. Then, press the "`Auto-Complete <x>`" button until it shows the desired setting.
