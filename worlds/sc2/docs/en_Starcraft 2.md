# Starcraft 2 Wings of Liberty

## What does randomization do to this game?

The following unlocks are randomized as items:
1. Your ability to build any non-worker unit.
2. Unit specific upgrades including some combinations not available in the vanilla campaigns, such as both strain choices simultaneously for Zerg and every Spear of Adun upgrade simultaneously for Protoss!
3. Your ability to get the generic unit upgrades, such as attack and armour upgrades.
4. Other miscellaneous upgrades such as laboratory upgrades and mercenaries for Terran, Kerrigan levels and upgrades for Zerg, and Spear of Adun upgrades for Protoss.
5. Small boosts to your starting mineral, vespene gas, and supply totals on each mission.

You find items by making progress in these categories:
* Completing missions
* Completing bonus objectives (like by gathering lab research material in Wings of Liberty)
* Reaching milestones in the mission, such as completing part of a main objective
* Completing challenges based on achievements in the base game, such as clearing all Zerg on Devil's Playground

Except for mission completion, these categories can be disabled in the game's settings. For instance, you can disable getting items for reaching required milestones.

When you receive items, they will immediately become available, even during a mission, and you will be
notified via a text box in the top-right corner of the game screen. Item unlocks are also logged in the Archipelago client.

Missions are launched through the Starcraft 2 Archipelago client, through the Starcraft 2 Launcher tab. The between mission segments on the Hyperion, the Leviathan, and the Spear of Adun are not included. Additionally, metaprogression currencies such as credits and Solarite are not used.

## What is the goal of this game when randomized?

The goal is to beat the final mission in the mission order. The yaml configuration file controls the mission order and how missions are shuffled.

## What non-randomized changes are there from vanilla Starcraft 2?

1. Some missions have more vespene geysers available to allow a wider variety of units.
2. Many new units and upgrades have been added as items, coming from co-op, melee, later campaigns, later expansions, brood war, and original ideas.
3. Higher-tech production structures, including Factories, Starports, Robotics Facilities, and Stargates, no longer have tech requirements.
4. Zerg missions have been adjusted to give the player a starting Lair where they would only have Hatcheries.
5. Upgrades with a downside have had the downside removed, such as automated refineries costing more or tech reactors taking longer to build.
6. Unit collision within the vents in Enemy Within has been adjusted to allow larger units to travel through them without getting stuck in odd places.
7. Several vanilla bugs have been fixed.

## Which of my items can be in another player's world?

By default, any of StarCraft 2's items (specified above) can be in another player's world. See the
[Advanced YAML Guide](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en)
for more information on how to change this.

## Unique Local Commands

The following commands are only available when using the Starcraft 2 Client to play with Archipelago. You can list them any time in the client with `/help`.

* `/download_data` Download the most recent release of the necessary files for playing SC2 with Archipelago. Will overwrite existing files
* `/difficulty [difficulty]` Overrides the difficulty set for the world.
    * Options: casual, normal, hard, brutal
* `/game_speed [game_speed]` Overrides the game speed for the world
    * Options: default, slower, slow, normal, fast, faster
* `/color [faction] [color]` Changes your color for one of your playable factions.
    * Faction options: raynor, kerrigan, primal, protoss, nova
    * Color options: white, red, blue, teal, purple, yellow, orange, green, lightpink, violet, lightgrey, darkgreen, brown, lightgreen, darkgrey, pink, rainbow, random, default
* `/option [option_name] [option_value]` Sets an option normally controlled by your yaml after generation.
    * Run without arguments to list all options.
    * Options pertain to automatic cutscene skipping, Kerrigan presence, Spear of Adun presence, starting resource amounts, controlling AI allies, etc.
* `/disable_mission_check` Disables the check to see if a mission is available to play. Meant for co-op runs where one player can play the next mission in a chain the other player is doing.
* `/play [mission_id]` Starts a Starcraft 2 mission based off of the mission_id provided
* `/available` Get what missions are currently available to play
* `/unfinished` Get what missions are currently available to play and have not had all locations checked
* `/set_path [path]` Manually set the SC2 install directory (if the automatic detection fails)
