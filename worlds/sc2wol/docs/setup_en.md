# Starcraft 2 Wings of Liberty Randomizer Setup Guide

## Required Software

- [Starcraft 2](https://starcraft2.com/en-us/)
- [Starcraft 2 AP Client](https://github.com/ArchipelagoMW/Archipelago)
- [Starcraft 2 AP Maps and Data](https://github.com/TheCondor07/Starcraft2ArchipelagoData)

## General Concept

Starcraft 2 AP Client launches a custom version of Starcraft 2 running modified Wings of Liberty campaign maps
 to allow for randomization of the items

## Installation Procedures

Follow the installation directions at the 
[Starcraft 2 AP Maps and Data](https://github.com/TheCondor07/Starcraft2ArchipelagoData) page you can find the .zip 
files on the releases page. After it is installed just run ArchipelagoStarcraftClient.exe to start the client to connect
to a Multiworld Game.

## Joining a MultiWorld Game

1. Run ArchipelagoStarcraftClient.exe
2. Type in /connect [sever ip]
3. Insert slot name and password as prompted
4. Once connected, use /unfinished to find what missions you can play and '/play [mission id]' to launch a mission. For 
new games under default settings the first mission available will always be Liberation Day[1] playable using the command
'/play 1'

## Where do I get a config file?

The [Player Settings](/games/Starcraft%202%20Wings%20of%20Liberty/player-settings) page on the website allows you to
configure your personal settings and export them into a config file

## Game isn't launching when I type /play

First check the log file for issues (stored at [Archipelago Directory]/logs/SC2Client.txt. There is sometimes an issue 
where the client can not find Starcraft 2.  Usually Documents/Starcraft 2/ExecuteInfo.txt is checked to find where 
Starcraft 2 is installed. On some computers particularly if you have OneDrive running this may  fail.  The following 
directions may help you in this case if you are on Windows. 

1. Navigate to '%userprofile%'.  Easiest way to do this is to hit Windows key+R type in %userprofile% and hit run or 
type in %userprofile% in the navigation bar of your file explorer. 
2. If it does not exist create a folder in her named 'Documents'.
3. Locate your 'My Documents' folder on your pc.  If you navigate to 'My PC' on the sidebar of file explorer should be a
link to this folder there labeled 'Documents'.
4. Find a folder labeled 'Starcraft 2' and copy it.
5. Paste this Starcraft 2 folder into the folder created or found in step 2.

These steps have been shown to work for some people for some people having issues with launching the game.  If you are 
still having issues check out our [Discord](https://discord.com/invite/8Z65BR2) for help.