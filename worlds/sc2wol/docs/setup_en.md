# StarCraft 2 Wings of Liberty Randomizer Setup Guide

This guide contains instructions on how to install and troubleshoot the StarCraft 2 Archipelago client, as well as where
to obtain a config file for StarCraft 2.

## Required Software

- [StarCraft 2](https://starcraft2.com/en-us/)
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)
- [StarCraft 2 AP Maps and Data](https://github.com/Ziktofel/Archipelago-SC2-data/releases)

## How do I install this randomizer?

1. Install StarCraft 2 and Archipelago using the first two links above. (The StarCraft 2 client for Archipelago is
   included by default.)
   - Linux users should also follow the instructions found at the bottom of this page 
     (["Running in Linux"](#running-in-linux)).
2. Run ArchipelagoStarcraft2Client.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step only.
3. Type the command `/download_data`. This will automatically install the Maps and Data files from the third link above.

## Where do I get a config file (aka "YAML") for this game?

The [Player Settings](https://archipelago.gg/games/Starcraft%202%20Wings%20of%20Liberty/player-settings) page on this
website allows you to choose your personal settings for the randomizer and download them into a config file. Remember
the name you type in the `Player Name` box; that's the "slot name" the client will ask you for when you attempt to
connect!

### And why do I need a config file?

Config files tell Archipelago how you'd like your game to be randomized, even if you're only using default settings.
When you're setting up a multiworld, every world needs its own config file.
Check out [Creating a YAML](https://archipelago.gg/tutorial/Archipelago/setup/en#creating-a-yaml) for more information.

## How do I join a MultiWorld game?

1. Run ArchipelagoStarcraft2Client.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step only.
2. Type `/connect [server ip]`.
3. Type your slot name and the server's password when prompted.
4. Once connected, switch to the 'StarCraft 2 Launcher' tab in the client. There, you can see every mission. By default,
   only 'Liberation Day' will be available at the beginning. Just click on a mission to start it!

## The game isn't launching when I try to start a mission.

First, check the log file for issues (stored at `[Archipelago Directory]/logs/SC2Client.txt`). If you can't figure out
the log file, visit our [Discord's](https://discord.com/invite/8Z65BR2) tech-support channel for help. Please include a
specific description of what's going wrong and attach your log file to your message.

## Running in macOS

To run StarCraft 2 through Archipelago in macOS, you will need to run the client via source as seen here: [macOS Guide](https://archipelago.gg/tutorial/Archipelago/mac/en). Note: when running the client, you will need to run the command `python3 Starcraft2Client.py`.

## Running in Linux

To run StarCraft 2 through Archipelago in Linux, you will need to install the game using Wine, then run the Linux build
of the Archipelago client.

Make sure you have StarCraft 2 installed using Wine, and that you have followed the
[installation procedures](#how-do-i-install-this-randomizer?) to add the Archipelago maps to the correct location. You will not
need to copy the .dll files. If you're having trouble installing or running StarCraft 2 on Linux, I recommend using the
Lutris installer.

Copy the following into a .sh file, replacing the values of **WINE** and **SC2PATH** variables with the relevant
locations, as well as setting **PATH_TO_ARCHIPELAGO** to the directory containing the AppImage if it is not in the same
folder as the script.

```sh
# Let the client know we're running SC2 in Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# FIXME Replace with path to the version of Wine used to run SC2
export WINE="/usr/bin/wine"

# FIXME Replace with path to StarCraft II install folder
export SC2PATH="/home/user/Games/starcraft-ii/drive_c/Program Files (x86)/StarCraft II/"

# FIXME Set to directory which contains Archipelago AppImage file
PATH_TO_ARCHIPELAGO=

# Gets the latest version of Archipelago AppImage in PATH_TO_ARCHIPELAGO.
# If PATH_TO_ARCHIPELAGO is not set, this defaults to the directory containing
# this script file.
ARCHIPELAGO="$(ls ${PATH_TO_ARCHIPELAGO:-$(dirname $0)}/Archipelago_*.AppImage | sort -r | head -1)"

# Start the Archipelago client
$ARCHIPELAGO Starcraft2Client
```

For Lutris installs, you can run `lutris -l` to get the numerical ID of your StarCraft II install, then run the command
below, replacing **${ID}** with the numerical ID.

    lutris lutris:rungameid/${ID} --output-script sc2.sh

This will get all of the relevant environment variables Lutris sets to run StarCraft 2 in a script, including the path
to the Wine binary that Lutris uses. You can then remove the line that runs the Battle.Net launcher and copy the code
above into the existing script.
