# Overcooked! 2 Randomizer Setup Guide

## Quick Links
- [Main Page](../../../../games/Overcooked!%202/info/en)
- [Options Page](../../../../games/Overcooked!%202/player-options)
- [OC2-Modding GitHub](https://github.com/toasterparty/oc2-modding)

## Required Software

- Windows 10+
- [Overcooked! 2](https://store.steampowered.com/bundle/13608/Overcooked_2___Gourmet_Edition/) for PC
    - **Steam: Recommended**
    - Steam (Beta Branch): Supported
    - Epic Games: Supported
    - GOG: Not officially supported - Adventurous users may choose to experiment at their own risk
    - Windows Store (aka GamePass): Not Supported
    - Xbox/PS/Switch: Not Supported
- [OC2-Modding Client](https://github.com/toasterparty/oc2-modding/releases) (instructions below)

## Overview

*OC2-Modding* is a general purpose modding framework which doubles as an Archipelago MultiWorld Client. It works by using Harmony to inject custom code into the game at runtime, so none of the original game files need to be modified in any way.

When connecting to an Archipelago session using the in-game login screen, a mod file containing all relevant game modifications is automatically downloaded and applied.

From this point, the game will communicate with the Archipelago service directly to manage sending/receiving items. Notifications of important events will appear through an in-game console at the top of the screen.

## Overcooked! 2 Modding Guide

### Install

1. Download and extract the contents of the latest [OC2-Modding Release](https://github.com/toasterparty/oc2-modding/releases) anywhere on your PC

2. Double-Click **oc2-modding-install.bat** follow the instructions.

Once *OC2-Modding* is installed, you have successfully installed everything you need to play/participate in Archipelago MultiWorld games.

### Disable

To temporarily turn off *OC2-Modding* and return to the original game, open **...\Overcooked! 2\BepInEx\config\OC2Modding.cfg** in a text editor like notepad and edit the following:

`DisableAllMods = true`

To re-enable, simply change the word **true** back to a **false**.

### Uninstall

To completely remove *OC2-Modding*, navigate to your game's installation folder and run **oc2-modding-uninstall.bat**.

## Generate a MultiWorld Game

1. Visit the [Player Options](../../../../games/Overcooked!%202/player-options) page and configure the game-specific options to taste

2. Export your yaml file and use it to generate a new randomized game

*For instructions on how to generate an Archipelago game, refer to the [Archipelago Setup Guide](../../../../tutorial/Archipelago/setup/en)*

## Joining a MultiWorld Game

1. Launch the game

2. When attempting to enter the main menu from the title screen, the game will freeze and prompt you to sign in:

![Sign-In Screen](https://i.imgur.com/goMy7o2.png)

3. Sign-in with server address, username and password of the corresponding room you would like to join.
- Otherwise, if you just want to play the vanilla game without any modifications, you may press "Continue without Archipelago" button.

4. Upon successful connection to the Archipelago service, you will be granted access to the main menu. The game will act as though you are playing for the first time. ***DO NOT FEAR*** — your original save data has not been overwritten; the Overcooked Randomizer just uses a temporary directory for it's save game data.

## Playing Co-Op

- To play local multiplayer (or Parsec/"Steam Play Together"), simply add the additional player to your game session as you would in the base game

- To play online multiplayer, the guest *must* also have the same version of OC2-Modding installed. In order for the game to work, the guest must sign in using the same information the host used to connect to the Archipelago session. Once both host and client are both connected, they may join one another in-game and proceed as normal. It does not matter who hosts the game, and the game's hosts may be changed at any point. You may notice some things are different when playing this way:

    - Guests will still receive Archipelago messages about sent/received items the same as the host
    
    - When the host loads the campaign, any connected guests are forced to select "Don't Save" when prompted to pick which save slot to use. This is because randomizer uses the Archipelago service as a pseudo "cloud save", so progress will always be synchronized between all participants of that randomized *Overcooked! 2* instance.

## Auto-Complete

Since the goal of randomizer isn't necessarily to achieve new personal high scores, players may find themselves waiting for a level timer to expire once they've met their objective. A new feature called *Auto-Complete* has been added to automatically complete levels once a target star count has been achieved.

To enable *Auto-Complete*, press the **Show** button near the top of your screen to expand the modding controls. Then, repeatedly press the **Auto-Complete** button until it shows the desired option.

## Overworld Sequence Breaking

In the world's options, there is an option called "Overworld Tricks" which allows the generator to make games which require doing tricks with the food truck to complete. This includes:

- Dashing across gaps

- "Wiggling" up ledges

- Going out of bounds [See Video](https://youtu.be/VdOGhi6XPu4)
