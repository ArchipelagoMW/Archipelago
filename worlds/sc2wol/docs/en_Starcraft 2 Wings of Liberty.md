# Starcraft 2 Wings of Liberty

## What does randomization do to this game?

The following unlocks are randomized as items:
1. Your ability to build any non-worker unit (including Marines!).
2. Your ability to upgrade infantry weapons, infantry armor, vehicle weapons, etc.
3. All armory upgrades
4. All laboratory upgrades
5. All mercenaries
6. Small boosts to your starting mineral and vespene gas totals on each mission

You find items by making progress in bonus objectives (like by rescuing allies in 'Zero Hour') and by completing
missions. When you receive items, they will immediately become available, even during a mission, and you will be
notified via a text box in the top-right corner of the game screen. (The text client for StarCraft 2 also records all
items in all worlds.)

Missions are launched only through the text client. The Hyperion is never visited. Additionally, credits are not used.

## What is the goal of this game when randomized?

The goal is to beat the final mission: 'All In'. The config file determines which variant you must complete.

## What non-randomized changes are there from vanilla Starcraft 2?

1. Some missions have more vespene geysers available to allow a wider variety of units.
2. Starports no longer require Factories in order to be built.
3. In 'A Sinister Turn' and 'Echoes of the Future', you can research Protoss air weapon/armor upgrades.

## Which of my items can be in another player's world?

By default, any of StarCraft 2's items (specified above) can be in another player's world. See the
[Advanced YAML Guide](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en)
for more information on how to change this.

## Unique Local Commands

The following commands are only available when using the Starcraft 2 Client to play with Archipelago.

- `/difficulty [difficulty]` Overrides the difficulty set for the world.
  - Options: casual, normal, hard, brutal
- `/game_speed [game_speed]` Overrides the game speed for the world
  - Options: default, slower, slow, normal, fast, faster
- `/color [color]` Changes your color (Currently has no effect)
  - Options: white, red, blue, teal, purple, yellow, orange, green, lightpink, violet, lightgrey, darkgreen, brown,
    lightgreen, darkgrey, pink, rainbow, random, default
- `/disable_mission_check` Disables the check to see if a mission is available to play. Meant for co-op runs where one
  player can play the next mission in a chain the other player is doing.
- `/play [mission_id]` Starts a Starcraft 2 mission based off of the mission_id provided
- `/available` Get what missions are currently available to play
- `/unfinished` Get what missions are currently available to play and have not had all locations checked
- `/set_path [path]` Menually set the SC2 install directory (if the automatic detection fails)
- `/download_data` Download the most recent release of the necassry files for playing SC2 with Archipelago. Will
  overwrite existing files
