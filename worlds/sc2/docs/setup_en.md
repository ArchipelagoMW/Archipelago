# StarCraft 2 Randomizer Setup Guide

This guide contains instructions on how to install and troubleshoot the StarCraft 2 Archipelago client, as well as 
where to obtain a config file for StarCraft 2.

## Required Software

- [StarCraft 2](https://starcraft2.com/en-us/)
   - While StarCraft 2 Archipelago supports all four campaigns, they are not mandatory to play the randomizer. 
   If you do not own certain campaigns, you only need to exclude them in the configuration file of your world.
- [The most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)

## How do I install this randomizer?

1. Install StarCraft 2 and Archipelago using the links above. The StarCraft 2 Archipelago client is downloaded by the 
Archipelago installer.
   - Linux users should also follow the instructions found at the bottom of this page 
     (["Running in Linux"](#running-in-linux)).
2. Run ArchipelagoStarcraft2Client.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step 
   only.
3. Type the command `/download_data`. 
This will automatically install the Maps and Data files needed to play StarCraft 2 Archipelago.

## Where do I get a config file (aka "YAML") for this game?

Yaml files are configuration files that tell Archipelago how you'd like your game to be randomized, even if you're only 
using default options.
When you're setting up a multiworld, every world needs its own yaml file.

There are three basic ways to get a yaml:
* You can go to the [Player Options](/games/Starcraft%202/player-options) page, set your options in the GUI, and export 
the yaml.
* You can generate a template, either by downloading it from the [Player Options](/games/Starcraft%202/player-options) 
page or by generating it from the Launcher (`ArchipelagoLauncher.exe`). 
The template includes descriptions of each option, you just have to edit it in your text editor of choice.
* You can ask someone else to share their yaml to use it for yourself or adjust it as you wish.

Remember the name you enter in the options page or in the yaml file, you'll need it to connect later!

Check out [Creating a YAML](/tutorial/Archipelago/setup/en#creating-a-yaml) for more game-agnostic information.

### Common yaml questions

#### How do I know I set my yaml up correctly?

The simplest way to check is to use the website [validator](/check). 

You can also test it by attempting to generate a multiworld with your yaml. Save your yaml to the `Players/` folder 
within your Archipelago installation and run `ArchipelagoGenerate.exe`. 
You should see a new `.zip` file within the `output/` folder of your Archipelago installation if things worked 
correctly. 
It's advisable to run `ArchipelagoGenerate.exe` through a terminal so that you can see the printout, which will include 
any errors and the precise output file name if it's successful. 
If you don't like terminals, you can also check the log file in the `logs/` folder.

#### What does Progression Balancing do?

For StarCraft 2, this option doesn't have much impact. 
It is an Archipelago option designed to balance world progression by swapping items in spheres. 
If the Progression Balancing of one world is greater than that of others, items in that world are more likely to be 
obtained early, and vice versa if its value is smaller. 
However, StarCraft 2 is more permissive regarding the items that can be used to progress, so this option has little 
influence on progression in a StarCraft 2 world. 
Since this option increases the time required to generate a MultiWorld, we recommend deactivating it (i.e., setting it 
to zero) for a StarCraft 2 world.

#### What does Tactics Level do?

Tactics level allows controlling the difficulty through what items you're likely to get early.
This is independent of game difficulty like causal, normal, hard, or brutal.

"Standard" and "Advanced" levels are guaranteed to be beatable with the items you are given.
The logic is a little more restrictive than a player's creativity, so an advanced player is likely to have
more items than they need in any situation. These levels are entirely safe to use in a multiworld.

The "Any Units" level only guarantees that a minimum number of faction-appropriate units or buildings are reachable
early on, with minimal restrictions on what those units are.
Generation will guarantee a number of faction-appropriate units are reachable before starting a mission,
based on the depth of that mission. For example, if the third mission is a zerg mission, it is guaranteed that 2
zerg units are somewhere in the preceding 2 missions. This logic level is not guaranteed to be beatable, and may
require lowering the difficulty level (`/difficulty` in the client) if many no-build missions are excluded.

The "No Logic" level provides no logical safeguards for beatability. It is only safe to use in a multiworld if the player curates
a start inventory or the organizer is okay with the possibility of the StarCraft 2 world being unbeatable.
Safeguards exist so that other games' items placed in the StarCraft 2 world are reachable under "Advanced" logic rules.

#### How do I specify items in a list, like in enabled campaigns?

You can look up the syntax for yaml collections in the 
[YAML specification](https://yaml.org/spec/1.2.2/#21-collections). 
For lists, every item goes on its own line, started with a hyphen.
Putting each element on its own line makes it easy to toggle elements by commenting
(ie adding a `#` character at the start of the line).

```yaml
  enabled_campaigns:
    - Wings of Liberty
    # - Heart of the Swarm
    - Legacy of the Void
    - Nova Covert Ops
    - Prophecy
    - 'Whispers of Oblivion (Legacy of the Void: Prologue)'
    # - 'Into the Void (Legacy of the Void: Epilogue)'
```

An inline syntax may also be used for short lists:

```yaml
  enabled_campaigns: ['Wings of Liberty', 'Nova Covert Ops']
```

An empty list is just a matching pair of square brackets: `[]`. 
That's often the default value in the template, which should let you know to use this syntax.

#### How do I specify items for key-value mappings, like starting inventory or filler item distribution?

Many options pertaining to the item pool are yaml mappings.
These are several lines, where each line looks like a name, followed by a colon, then a space, then a value.

```yaml
  start_inventory:
    Micro-Filtering: 1
    Additional Starting Vespene: 5

  locked_items:
    MULE (Command Center): 1
```

For options like `start_inventory`, `locked_items`, `excluded_items`, and `unexcluded_items`, the value 
is a number specifying how many copies of an item to start with/exclude/lock.
Note the name can also be an item group, and the value will then be added to the values for all the items
within the group. A value of `0` will exclude all copies of an item, but will add +0 if the value
is also specified by another name.

For options like `filler_items_distribution`, the value is a number specifying the relative weight of 
a filler item being that particular item.

For the `custom_mission_order` option, the value is a nested structure of other mapppings to specify the structure 
of the mission order. See the [Custom Mission Order documentation](/tutorial/Starcraft%202/custom_mission_orders_en)

An empty mapping is just a matching pair of curly braces: `{}`. 
That's the default value in the template, which should let you know to use this syntax.

#### How do I know the exact names of items and locations?

You can look up a complete list of the item names in the 
[Icon Repository](https://matthewmarinets.github.io/ap_sc2_icons/) page.
This page also contains supplementary information of each item.

Locations are of the format `<mission name>: <location name>`. Names are most easily looked up by hovering
your mouse over a mission in the launcher tab of a client. Note this requires already generating a game connect to.

This information can also be found in the [*datapackage*](/datapackage) page of the Archipelago website.
This page includes all data associated with all games.

## How do I join a MultiWorld game?

1. Run ArchipelagoStarcraft2Client.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step 
   only.
2. In the Archipelago tab, type `/connect [server IP]`.
   - If you're running through the website, the server IP should be displayed near the top of the room page.
   - The server IP may also be typed into the top bar, and then clicking "Connect"
3. Type your slot name from your YAML when prompted.
4. If the server has a password, enter that when prompted.
5. Once connected, switch to the 'StarCraft 2 Launcher' tab in the client. There, you can see all the missions in your 
world.

Unreachable missions will have greyed-out text. Completed missions (all locations collected) will have white text.
Accessible but incomplete missions will have blue text. Goal missions will have a gold border.
Mission buttons will have a color corresponding to the faction you play as in that mission.

Click on an available mission to start it.

## The game isn't launching when I try to start a mission.

Usually, this is caused by the mod files not being downloaded.
Make sure you have run `/download_data` in the Archipelago tab before playing.
You should only have to run `/download_data` again to pick up bugfixes and updates.

Make sure that you are running an up-to-date version of the client.
Check the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases) to
look up what the latest version is (RC releases are not necessary; that stands for "Release Candidate").

If these things are in order, check the log file for issues (stored at `[Archipelago Directory]/logs/Starcraft2Client.txt`).
If you can't figure out the log file, visit our [Discord's](https://discord.com/invite/8Z65BR2) tech-support channel 
for help. 
Please include a specific description of what's going wrong and attach your log file to your message.

## My keyboard shortcuts profile is not available when I play *StarCraft 2 Archipelago*.

For your keyboard shortcuts profile to work in Archipelago, you need to copy your shortcuts file from 
`Documents/StarCraft II/Accounts/######/Hotkeys` to `Documents/StarCraft II/Hotkeys`. 
If the folder doesn't exist, create it.

To enable StarCraft 2 Archipelago to use your profile, follow these steps:
1. Launch StarCraft 2 via the Battle.net application.
2. Change your hotkey profile to the standard mode and accept.
3. Select your custom profile and accept.

You will only need to do this once.

## Running in macOS

To run StarCraft 2 through Archipelago in macOS, you will need to run the client via source as seen here: 
[macOS Guide](/tutorial/Archipelago/mac/en). 
Note: to launch the client, you will need to run the command `python3 Starcraft2Client.py`.

## Running in Linux

To run StarCraft 2 through Archipelago on Linux, you will need to install the game using Wine, then run the Linux build
of the Archipelago client.

Make sure you have StarCraft 2 installed using Wine, and you know where Wine and Starcraft 2 are installed.
If you're having trouble installing or running StarCraft 2 on Linux, it is recommended to use the Lutris installer.

Copy the following into a .sh file, preferably within your Archipelago directory,
replacing the values of **WINE** and **SC2PATH** variables with the relevant locations,
as well as setting **PATH_TO_ARCHIPELAGO** to the directory containing the AppImage if it is not in the same
folder as the script.

```sh
# Let the client know we're running SC2 in Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# FIXME Replace with path to the version of Wine used to run SC2
export WINE="/usr/bin/wine"

# FIXME If using nondefault wineprefix for SC2 install (usual for Lutris installs), uncomment the next line and change the path
#export WINEPREFIX="/path/to/wineprefix"

# FIXME Uncomment the following lines if experiencing issues with DXVK (like DDRAW.ddl does not exist)
#export WINEDLLOVERRIDES=d3d10core,d3d11,d3d12,d3d12core,d3d9,d3dcompiler_33,d3dcompiler_34,d3dcompiler_35,d3dcompiler_36,d3dcompiler_37,d3dcompiler_38,d3dcompiler_39,d3dcompiler_40,d3dcompiler_41,d3dcompiler_42,d3dcompiler_43,d3dcompiler_46,d3dcompiler_47,d3dx10,d3dx10_33,d3dx10_34,d3dx10_35,d3dx10_36,d3dx10_37,d3dx10_38,d3dx10_39,d3dx10_40,d3dx10_41,d3dx10_42,d3dx10_43,d3dx11_42,d3dx11_43,d3dx9_24,d3dx9_25,d3dx9_26,d3dx9_27,d3dx9_28,d3dx9_29,d3dx9_30,d3dx9_31,d3dx9_32,d3dx9_33,d3dx9_34,d3dx9_35,d3dx9_36,d3dx9_37,d3dx9_38,d3dx9_39,d3dx9_40,d3dx9_41,d3dx9_42,d3dx9_43,dxgi,nvapi,nvapi64
#export DXVK_ENABLE_NVAPI=1

# FIXME Replace with path to StarCraft II install folder
export SC2PATH="/home/user/Games/starcraft-ii/drive_c/Program Files (x86)/StarCraft II/"

# FIXME Set to directory which contains Archipelago AppImage file
PATH_TO_ARCHIPELAGO=

# Gets the latest version of Archipelago AppImage in PATH_TO_ARCHIPELAGO.
# If PATH_TO_ARCHIPELAGO is not set, this defaults to the directory containing
# this script file.
ARCHIPELAGO="$(ls ${PATH_TO_ARCHIPELAGO:-$(dirname $0)}/Archipelago_*.AppImage | sort -r | head -1)"

# Start the Archipelago client
$ARCHIPELAGO "Starcraft 2 Client"
```

For Lutris installs, you can run `lutris -l` to get the numerical ID of your StarCraft II install, then run the command
below, replacing **${ID}** with the numerical ID.

    lutris lutris:rungameid/${ID} --output-script sc2.sh

This will get all of the relevant environment variables Lutris sets to run StarCraft 2 in a script, including the path
to the Wine binary that Lutris uses. 
You can then remove the line that runs the Battle.Net launcher and copy the code above into the existing script.

Finally, you can run the script to start your Archipelago client,
and it should be able to launch Starcraft 2 when you start a mission.
