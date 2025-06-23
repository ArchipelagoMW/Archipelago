# StarCraft 2

## Game page in other languages:

* [Français](/games/Starcraft%202/info/fr)

## What does randomization do to this game?

### Items and locations

The following unlocks are randomized as items:
1. Your ability to build any non-worker unit.
2. Unit specific upgrades including some combinations not available in the vanilla campaigns, such as both strain 
choices simultaneously for Zerg and every Spear of Adun upgrade simultaneously for Protoss!
3. Your ability to get the generic unit upgrades, such as attack and armour upgrades.
4. Other miscellaneous upgrades such as laboratory upgrades and mercenaries for Terran, Kerrigan levels and upgrades 
for Zerg, and Spear of Adun upgrades for Protoss.
5. Small boosts to your starting mineral, vespene gas, and supply totals on each mission.

You find items by making progress in these categories:
* Completing missions
* Completing bonus objectives (like by gathering lab research material in Wings of Liberty)
* Reaching milestones in the mission, such as completing part of a main objective
* Completing challenges based on achievements in the base game, such as clearing all Zerg on Devil's Playground

In Archipelago's nomenclature, these are the locations where items can be found.
Each location, including mission completion, has a set of rules that specify the items required to access it.
These rules were designed assuming that StarCraft 2 is played on the Brutal difficulty.
Since each location has its own rule, it's possible that an item required for progression is in a mission where you 
can't reach all of its locations or complete it. 
However, mission completion is always required to gain access to new missions.

Aside from mission completion, the other location categories can be disabled in the player options.
For instance, you can disable getting items for reaching required milestones.

When you receive items, they will immediately become available, even during a mission, and you will be
notified via a text box in the top-right corner of the game screen. 
Item unlocks are also logged in the Archipelago client.

### Mission order

The missions and the order in which they need to be completed, referred to as the mission order, can also be randomized.
The four StarCraft 2 campaigns can be used to populate the mission order. 
Note that the evolution missions from Heart of the Swarm are not included in the randomizer.
The default mission order follows the structure of the selected campaigns but several other options are available, 
e.g., blitz, grid, etc.

Missions are launched through the StarCraft 2 Archipelago client, through the StarCraft 2 Launcher tab. 
The between mission segments on the Hyperion, the Leviathan, and the Spear of Adun are not included. 
Additionally, metaprogression currencies such as credits and Solarite are not used.
Available missions are in blue; missions where all locations were collected are in white.
If you move your mouse over a mission, the uncollected locations will be displayed, categorized by type.
Unavailable missions are in grey; their requirements will also be shown there.

## What is the goal of this game when randomized?

The goal is to beat the final mission in the mission order. 
The yaml configuration file controls the mission order, which combination of the four StarCraft 2 campaigns can be 
used, and how missions are shuffled. 
Since the first two options determine the number of missions in a StarCraft 2 world, they can be used to customize the 
expected time to complete the world. 

## What non-randomized changes are there from vanilla StarCraft 2?

1. Some missions have more vespene geysers available to allow a wider variety of units.
2. Many new units and upgrades have been added as items, coming from co-op, melee, later campaigns, later expansions, 
brood war, and original ideas.
3. Higher-tech production structures, including Factories, Starports, Robotics Facilities, and Stargates, no longer 
have tech requirements.
4. Zerg missions have been adjusted to give the player a starting Lair where they would only have Hatcheries.
5. Upgrades with a downside have had the downside removed, such as automated refineries costing more or tech reactors 
taking longer to build.
6. Unit collision within the vents in Enemy Within has been adjusted to allow larger units to travel through them 
without getting stuck in odd places.
7. Several vanilla bugs have been fixed.

## Which of my items can be in another player's world?

By default, any of StarCraft 2's items (specified above) can be in another player's world. 
See the [Advanced YAML Guide](/tutorial/Archipelago/advanced_settings/en) for more information on how to change this.

## Unique Local Commands

The following commands are only available when using the StarCraft 2 Client to play with Archipelago. 
You can list them any time in the client with `/help`.

* `/download_data` Download the most recent release of the necessary files for playing SC2 with Archipelago. 
Will overwrite existing files
* `/difficulty [difficulty]` Overrides the difficulty set for the world.
    * Options: casual, normal, hard, brutal
* `/game_speed [game_speed]` Overrides the game speed for the world
    * Options: default, slower, slow, normal, fast, faster
* `/color [faction] [color]` Changes your color for one of your playable factions.
    * Run without arguments to list all factions and colors that are available.
* `/option [option_name] [option_value]` Sets an option normally controlled by your yaml after generation.
    * Run without arguments to list all options.
    * Options pertain to automatic cutscene skipping, Kerrigan presence, Spear of Adun presence, starting resource 
    amounts, controlling AI allies, etc.
* `/disable_mission_check` Disables the check to see if a mission is available to play. 
Meant for co-op runs where one player can play the next mission in a chain the other player is doing.
* `/play [mission_id]` Starts a StarCraft 2 mission based off of the mission_id provided
* `/available` Get what missions are currently available to play
* `/unfinished` Get what missions are currently available to play and have not had all locations checked
* `/set_path [path]` Manually set the SC2 install directory (if the automatic detection fails)

Note that the behavior of the command `/received` was modified in the StarCraft 2 client.
In the Common client of Archipelago, the command returns the list of items received in the reverse order they were 
received.
In the StarCraft 2 client, the returned list will be divided by races (i.e., Any, Protoss, Terran, and Zerg).
Additionally, upgrades are grouped beneath their corresponding units or buildings.
A filter parameter can be provided, e.g., `/received Thor`, to limit the number of items shown.
Every item whose name, race, or group name contains the provided parameter will be shown.

## Particularities in a multiworld

### Collect on goal completion

One of the default options of multiworlds is that once a world has achieved its goal, it collects its items from all 
other worlds. 
If you do not want this to happen, you should ask the person generating the multiworld to set the `Collect Permission` 
option to something else, e.g., manual. 
If the generation is not done via the website, the person that does the generation should modify the `collect_mode` 
option in their `host.yaml` file prior to generation. 
If the multiworld has already been generated, the host can use the command `/option collect_mode [value]` to change 
this option.

## Known issues

- StarCraft 2 Archipelago does not support loading a saved game. 
For this reason, it is recommended to play on a difficulty level lower than what you are normally comfortable with.
- StarCraft 2 Archipelago does not support the restart of a mission from the StarCraft 2 menu. 
To restart a mission, use the StarCraft 2 Client.
- A crash report is often generated when a mission is closed. 
This does not affect the game and can be ignored.
- Currently, the StarCraft 2 client uses the Victory locations to determine which missions have been completed. 
As a result, the Archipelago collect feature can sometime grant access to missions that are connected to a mission that 
you did not complete.

