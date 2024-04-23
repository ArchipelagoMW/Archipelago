# StarCraft 2 Randomizer Setup Guide

This guide contains instructions on how to install and troubleshoot the StarCraft 2 Archipelago client, as well as where
to obtain a config file for StarCraft 2.

## Required Software

- [StarCraft 2](https://starcraft2.com/en-us/)
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)

## How do I install this randomizer?

1. Install StarCraft 2 and Archipelago using the links above. The StarCraft 2 Archipelago client is downloaded by the Archipelago installer.
   - Linux users should also follow the instructions found at the bottom of this page 
     (["Running in Linux"](#running-in-linux)).
2. Run ArchipelagoStarcraft2Client.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step only.
3. Type the command `/download_data`. This will automatically install the Maps and Data files from the third link above.

## Where do I get a config file (aka "YAML") for this game?

Yaml files are configuration files that tell Archipelago how you'd like your game to be randomized, even if you're only using default options.
When you're setting up a multiworld, every world needs its own yaml file.

There are three basic ways to get a yaml:
* You can go to the [Player Options](https://archipelago.gg/games/Starcraft%202/player-options) page, set your options in the GUI, and export the yaml.
* You can generate a template, either by downloading it from the [Player Options](https://archipelago.gg/games/Starcraft%202/player-options) page or by generating it from the Launcher (ArchipelagoLauncher.exe). The template includes descriptions of each option, you just have to edit it in your text editor of choice.
* You can ask someone else to share their yaml to use it for yourself or adjust it as you wish.

Remember the name you enter in the options page or in the yaml file, you'll need it to connect later!

Note that the basic Player Options page doesn't allow you to change all advanced options, such as excluding particular units or upgrades. Go through the [Weighted Options](https://archipelago.gg/weighted-options) page for that.

Check out [Creating a YAML](https://archipelago.gg/tutorial/Archipelago/setup/en#creating-a-yaml) for more game-agnostic information.

### Common yaml questions
#### How do I know I set my yaml up correctly?

The simplest way to check is to test it out. Save your yaml to the Players/ folder within your Archipelago installation and run ArchipelagoGenerate.exe. You should see a new .zip file within the output/ folder of your Archipelago installation if things worked correctly. It's advisable to run ArchipelagoGenerate through a terminal so that you can see the printout, which will include any errors and the precise output file name if it's successful. If you don't like terminals, you can also check the log file in the logs/ folder.

#### What does Progression Balancing do?

For Starcraft 2, not much. It's an Archipelago-wide option meant to shift required items earlier in the playthrough, but Starcraft 2 tends to be much more open in what items you can use. As such, this adjustment isn't very noticeable. It can also increase generation times, so we generally recommend turning it off.

#### How do I specify items in a list, like in excluded items?

You can look up the syntax for yaml collections in the [YAML specification](https://yaml.org/spec/1.2.2/#21-collections). For lists, every item goes on its own line, started with a hyphen:

```yaml
excluded_items:
  - Battlecruiser
  - Drop-Pods (Kerrigan Tier 7)
```

An empty list is just a matching pair of square brackets: `[]`. That's the default value in the template, which should let you know to use this syntax.

#### How do I specify items for the starting inventory?

The starting inventory is a YAML mapping rather than a list, which associates an item with the amount you start with. The syntax looks like the item name, followed by a colon, then a whitespace character, and then the value:

```yaml
start_inventory:
  Micro-Filtering: 1
  Additional Starting Vespene: 5
```

An empty mapping is just a matching pair of curly braces: `{}`. That's the default value in the template, which should let you know to use this syntax.

#### How do I know the exact names of items?

You can look up a complete list if item names in the [Icon Repository](https://matthewmarinets.github.io/ap_sc2_icons/).

## How do I join a MultiWorld game?

1. Run ArchipelagoStarcraft2Client.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step only.
2. Type `/connect [server ip]`.
   - If you're running through the website, the server IP should be displayed near the top of the room page.
3. Type your slot name from your YAML when prompted.
4. If the server has a password, enter that when prompted.
5. Once connected, switch to the 'StarCraft 2 Launcher' tab in the client. There, you can see all the missions in your world. Unreachable missions will have greyed-out text. Just click on an available mission to start it!

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
