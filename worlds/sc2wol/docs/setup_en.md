# StarCraft 2 Wings of Liberty Randomizer Setup Guide

This guide contains instructions on how to install and troubleshoot the StarCraft 2 Archipelago client, as well as where
to obtain a config file for StarCraft 2.

## Required Software

- [StarCraft 2](https://starcraft2.com/en-us/)
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)
- [StarCraft 2 AP Maps and Data](https://github.com/TheCondor07/Starcraft2ArchipelagoData)

## How do I install this randomizer?

1. Install StarCraft 2 and Archipelago using the first two links above. (The StarCraft 2 client for Archipelago is
   included by default.)
2. Click the third link above and follow the instructions there.
3. Linux users should also follow the instructions found at the bottom of this page 
   (["Running in Linux"](#running-in-linux)).

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
2. Type `/connect [server ip]`.
3. Type your slot name and the server's password when prompted.
4. Once connected, use `/unfinished` to find which missions you can play and their ids, and use `/play [mission id]` to
   launch a mission. By default, the first mission you can play is `Liberation Day[1]`, and you can play it
   using the command `/play 1`.

## The game isn't launching when I type /play.

First, check the log file for issues (stored at `[Archipelago Directory]/logs/SC2Client.txt`). If none of the below
fixes work for you, check out our [Discord's](https://discord.com/invite/8Z65BR2) tech-support channel for help.

### Check your installation

Make sure you've followed the installation instructions completely. Specifically, make sure that you've placed the Maps
and Mods folders directly inside the StarCraft II installation folder. They should be in the same location as the
SC2Data, Support, Support64, and Versions folders.

### Windows: Documents folder mixup

Sometimes, on Windows devices, the client cannot find StarCraft 2. Typically, this is because the Documents folder is
not in the default location. The following directions may work around this:

1. Navigate to '%userprofile%'.  (The easiest way to do this is to hit Windows key+R, type in `%userprofile%`, and click
   "OK".)
2. A File Explorer window will appear. If you don't see a folder here named 'Documents', create a new folder with that
   name.
3. Locate the original 'Documents' folder on your PC.  (Navigate to 'My PC' or 'This PC' on the left side of File
   Explorer. There should be a link to a folder there named 'Documents'.)
4. Inside the original 'Documents' folder, find a folder named 'StarCraft II' and copy it.
5. Go back to the 'Documents' folder you created or found in step 2. Paste the StarCraft II folder there.
6. Try to type /play again.

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
