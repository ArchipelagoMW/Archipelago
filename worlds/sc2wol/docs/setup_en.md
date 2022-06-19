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
files on the releases page. After it is installed, just run ArchipelagoStarcraft2Client.exe to start the client and connect
to a Multiworld Game.

## Joining a MultiWorld Game

1. Run ArchipelagoStarcraft2Client.exe
2. Type in `/connect [server ip]`
3. Insert slot name and password as prompted
4. Once connected, use `/unfinished` to find what missions you can play and `/play [mission id]` to launch a mission. For
new games under default settings the first mission available will always be Liberation Day[1] playable using the command
`/play 1`.

## Where do I get a config file?

The [Player Settings](/games/Starcraft%202%20Wings%20of%20Liberty/player-settings) page on the website allows you to
configure your personal settings and export them into a config file.

## Game isn't launching when I type /play

First check the log file for issues (stored at [Archipelago Directory]/logs/SC2Client.txt. There is sometimes an issue
where the client can not find Starcraft 2.  Usually 'Documents/StarCraft II/ExecuteInfo.txt' is checked to find where
Starcraft 2 is installed. On some computers particularly if you have OneDrive running this may  fail.  The following
directions may help you in this case if you are on Windows.

1. Navigate to '%userprofile%'.  Easiest way to do this is to hit Windows key+R type in `%userprofile%` and hit run or
type in `%userprofile%` in the navigation bar of your file explorer.
2. If it does not exist create a folder in her named 'Documents'.
3. Locate your 'My Documents' folder on your PC.  If you navigate to 'My PC' on the sidebar of file explorer should be a
link to this folder there labeled 'Documents'.
4. Find a folder labeled 'StarCraft II' and copy it.
5. Paste this 'StarCraft II' folder into the folder created or found in step 2.

These steps have been shown to work for some people for some people having issues with launching the game.  If you are
still having issues check out our [Discord](https://discord.com/invite/8Z65BR2) for help.

## Running in Linux

To run StarCraft 2 through Archipelago in Linux, you will need to install the game using Wine then run the Linux build of the Archipelago client.

Make sure you have StarCraft 2 installed using Wine and you have followed the [Installation Procedures](#installation-procedures) to add the Archipelago maps to the correct location. You will not need to copy the .dll files. If you're having trouble installing or running StarCraft 2 on Linux, I recommend using the Lutris installer.

Copy the following into a .sh file, replacing the values of **WINE** and **SC2PATH** variables to the relevant locations, as well as updating the path to the Archipelago client, if it is not in the same folder as the script.

```sh
# Let the client know we're running SC2 in Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# FIXME Replace with path to the version of Wine used to run SC2
export WINE="/usr/bin/wine"

# FIXME Replace with path to StarCraft II install folder
export SC2PATH="/home/user/Games/starcraft-ii/drive_c/Program Files (x86)/StarCraft II/"

# Start the Archipelago client
./Archipelago_0.3.2_linux-x86_64.AppImage Starcraft2Client
```

For Lutris installs, you can run `lutris -l` to get the numerical ID of your StarCraft II install, then run the command below, replacing **${ID}** with the numerical ID.

    lutris lutris:rungameid/${ID} --output-script sc2.sh

This will get all of the relevant environment variables Lutris sets to run StarCraft 2 in a script, including the path to the Wine binary that Lutris uses. You can then remove the line that runs the Battle.Net launcher and copy the code above into the existing script.
