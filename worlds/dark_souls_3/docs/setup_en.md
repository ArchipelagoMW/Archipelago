# Dark Souls III Randomizer Setup Guide

## Required Software

- [Dark Souls III](https://store.steampowered.com/app/374320/DARK_SOULS_III/)
- [Dark Souls III AP Client](https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/releases)

## Optional Software

- [Dark Souls III Maptracker Pack](https://github.com/Br00ty/DS3_AP_Maptracker/releases/latest), for use with [Poptracker](https://github.com/black-sliver/PopTracker/releases)

## General Concept

The Dark Souls III AP Client is a dinput8.dll triggered when launching Dark Souls III. This .dll file will launch a command 
prompt where you can read information about your run and write any command to interact with the Archipelago server.

## Installation Procedures

<span style="color:tomato">
**This mod can ban you permanently from the FromSoftware servers if used online.** 
</span>  
This client has only been tested with the Official Steam version of the game (v1.15/1.35) not matter which DLCs are installed.

Get the dinput8.dll from the [Dark Souls III AP Client](https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/releases) and 
add it at the root folder of your game (e.g. "SteamLibrary\steamapps\common\DARK SOULS III\Game")

## Joining a MultiWorld Game

1. Run DarkSoulsIII.exe or run the game through Steam
2. Type in "/connect {SERVER_IP}:{SERVER_PORT} {SLOT_NAME}" in the "Windows Command Prompt" that opened
3. Once connected, create a new game, choose a class and wait for the others before starting
4. You can quit and launch at anytime during a game

## Where do I get a config file?

The [Player Settings](/games/Dark%20Souls%20III/player-settings) page on the website allows you to
configure your personal settings and export them into a config file
