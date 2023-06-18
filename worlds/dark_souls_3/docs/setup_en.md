# Dark Souls III Randomizer Setup Guide

## Required Software

- [Dark Souls III](https://store.steampowered.com/app/374320/DARK_SOULS_III/)
- [Dark Souls III AP Client](https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/releases)

## Optional Software

- [Dark Souls III Maptracker Pack](https://github.com/Br00ty/DS3_AP_Maptracker/releases/latest), for use with [Poptracker](https://github.com/black-sliver/PopTracker/releases)

## General Concept

<span style="color:tomato">
**This mod can ban you permanently from the FromSoftware servers if used online.** 
</span>
The Dark Souls III AP Client is a dinput8.dll triggered when launching Dark Souls III. This .dll file will launch a command 
prompt where you can read information about your run and write any command to interact with the Archipelago server.

This client has only been tested with the Official Steam version of the game at version 1.15. It does not matter which DLCs are installed. However, you will have to downpatch your Dark Souls III installation from current patch, which is 1.15.2.

## Downpatching Dark Souls III

Download the 1.15 crash-fix executable from the [speedsouls wiki](https://wiki.speedsouls.com/darksouls3:Crash_Fix) and use it to replace DarkSoulsIII.exe in your installation. This modified executable also fixes a memory leak that may otherwise cause the game to crash.

An alternate method is to download version 1.15 from the Steam console. Follow instructions from the [speedsouls wiki](https://wiki.speedsouls.com/darksouls3:Downpatching). Your download command, including the correct depot and manifest ids, is "download_depot 374320 374321 4471176929659548333"

## Installing the Archipelago mod

Get the dinput8.dll from the [Dark Souls III AP Client](https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/releases) and 
add it at the root folder of your game (e.g. "SteamLibrary\steamapps\common\DARK SOULS III\Game")

## Joining a MultiWorld Game

1. Run Steam in offline mode, both to avoid being banned and to prevent Steam from updating the game files
1. Launch Dark Souls III
2. Type in "/connect {SERVER_IP}:{SERVER_PORT} {SLOT_NAME}" in the "Windows Command Prompt" that opened
3. Once connected, create a new game, choose a class and wait for the others before starting
4. You can quit and launch at anytime during a game

## Where do I get a config file?

The [Player Settings](/games/Dark%20Souls%20III/player-settings) page on the website allows you to
configure your personal settings and export them into a config file.
