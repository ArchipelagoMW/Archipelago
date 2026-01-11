# Shadow The Hedgehgog Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Dolphin Emulator, recommended 2409 version of higher.
- An NTSC Rom for Shadow the Hedgehog for Gamecube. The Archipelago community cannot provide this.


### Configuring Game

- Launch Dolphin
- Disable use of Emulated Memory Size override, as archipelago will not work with memory processing.
- 

## Optional Software
- Universal Tracker: This game aims to support universal tracker allowing you to know what checks are available in game.

## Generating a Game
1. Create your options file (YAML). Refer to the generated file for information regarding the options. 
	If you want the latest template, open the Archipelago Launcher and click 'Generate Templates'
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
   This will generate an output file.
3. Open `ArchipelagoLauncher.exe`
4. Host your game. You can host local games using 'Host' option on the launcher, or upload to Archipelago's site.
5. Open Dolphin emulator.
6. Ensure you do not have a Shadow the Hedgehog save present.
	You can move save files or edit in the Memory Card manager where you can also export saves before removal.
	Loading a save will automatically start clearing level clear checks as they load from the save, but archipelago prevents some of this behaviour.
7. Open the Shadow the Hedgehog rom.
8. Select 'Shadow The Hedgehog Client' in Archipelago Launcher.
9. Enter your credentials and connect to the server.
10. Play!

You must remain with client running whenever playing the game to receive checks and other items.
You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect.

## Advanced YAML Configuration

The percent_overrides list option in the yaml file is very powerful in terms of overwriting behaviours.
You can define a list of stages and the requirement to override the percentage for, for this check.
This feature is new and welcome for feedback.
These values will override the default setting for each of the available options.
You can override settings in the following format:
{type}.{stage}

The available types are:
Enemysanity:
- EA: Alien enemysanity
- EG: Gun enemysanity
- EE: Egg robo enemysanity

Objective
- OD: Locations percentage for dark mission
- OH: Locations percentage for hero mission

Completion
- CD: Amount of items from pool required to complete dark mission.
- CH: Amount of items from pool required to complete hero mission.

Available
- AD: Available dark items in the pool
- AH: Available hero items in the pool

e.g. CH.Westopolis: 10 -- set the Hero Clear requirement to 10%.

