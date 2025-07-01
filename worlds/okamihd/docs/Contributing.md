# Okami HD APWorld Contribution Guide

## Introduction

This is the APWorld data for Okami HD; It's meant to be used with
the [Okami APClient Mod](https://github.com/Axertin/okami-apclient).

The goal of these files is to describe all Items, Locations and Regions that are used to randomize the game.
For more info on what this means, check
the [Archipelago Autoworld Docs](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md).

English is not my native language; I hope this guide is clear; Feel free to message me if it's not.

## What needs to be done?

Currently, there only exists a stub of logic that goes from the start of the game to the Entrance of Tsuta ruins.
There's probably some checks that I might have missed, feel free to message me if you find one.
You can help by contributing to logic. The checks we need to have in the logic are currently limited to only these:

- Brush Techniques (except Mist Warp bc we're not randomizing shops yet,still we'll probably add it in the item pool for
  convenience)
- Chest Items, and Item given by quests

## How does logic work ?
*Note: These structures will probably change with time, I'll try to keep the guide up to date*

Logic is currently stored in the RegionData Folder. Each file in the folder represents a different in-game map,
as [listed by the game](https://github.com/whataboutclyde/okami-utils/blob/master/data/area_id.yaml).

Each of these files is split in three parts:

### Exits

For each Region described in the file, you need to contribute all exits that connect to another Region

The ExitData struc works as follows:

| Field       | Content      | Notes                                                                                                 |
|-------------|--------------|-------------------------------------------------------------------------------------------------------|
| name        | string       | Required. Needs to be unique.                                                                         |
| destination | string       | Required. The Region this exits leads to. Please make sure you use a element of the RegionNames enum. |
| has_events  | string array | List of events that need to be cleared before being able to use this exit.                            |
| needs_swim  | boolean      | Is it needed to swim a long distance to use this exit ? (eg. waterlily, orca, or water tablet)        |

Exits:

- are always considered as going both ways: If you want to connect Kamiki to Shinshu, you only need an Exit from Kamiki
  to Shinshu or an Exit from Shinshu to Kamiki, but not both.
- should only require events to be traversable, **techically**, you could put item names in *has_events* and it should
  work. But I d'rather have an event that represents blowing up a boulder that allows an exit, than an exit requiring
  cherry bomb. That way, if we ever want to introduce a setting where the boulder is removed, we'd juste have to set the
  event as precolleted.

When connecting a cursed region, the cursed part should be connected only to places that can be accessed when the region
is in cursed state.

### Events

Events represent something the player has to do to progress, but that doesn't give an item or check, like a mandatory
fight, clearing up an obstacle, restoring a guardian sapling, etc.

In logic an event gets represented as a check that always gives an item with the same name as itself.
Some options can allow for the event to be separated into a location and an item (if we ever want/need to do that at
some point), or for it to be collected before the start of the game.
The struct works has follows:

| Field                     | Content                | Notes                                                                                                                                                                                                                                    |
|---------------------------|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name                      | string                 | Required.Used as dict key. Must be unique                                                                                                                                                                                                |
| id                        | int or None            | Only required if the event can be precollected or a seperate Item.                                                                                                                                                                       |
| required_brush_techniques | BrushTechniques array  | All techniques required to collect that event. (Except power slash and Cherry Bomb;See below)                                                                                                                                            |
| power_slash_level         | int                    | Power slash level required to get this event.                                                                                                                                                                                            |
| cherry_bomb_level         | int                    | Cherry Bomb level required to get this event.                                                                                                                                                                                            |
| buried                    | int                    | Do you need to dig to get this item? 0= no, 1=yes, 2 = yes, with Iron claws                                                                                                                                                              |
| override_event_item_name  | str or None            | Defines a seperate Name for the event. Can be useful in some edge cases where we have multiple events that do the same thing (Like restoring the river of the heavens form one side or another, which is not really an issue until ER. ) |                                                                                              
| required_items_events     | str array              | List of items or events needed to collect this event.                                                                                                                                                                                    |
| mandatory_ennemies        | OkamiEnnemies array    | List of enemies you have to defeat to collect this event. This is used for ennemies that requires a specific brush technique to defeat (bud ogre...) and to check for the weapon tier the player currently has.                          |
| needs_swim                | boolean                | Is it needed to swim a long distance to collect this event ? (eg. waterlily, orca, or water tablet)                                                                                                                                      |
| is_event_item             | boolean or function    | Should this event be split in a location and an item in the item pool. Can Take a lambda with OkamiOptions as parameter to adapt to user yaml settings.                                                                                  |
| precollected              | boolean or function    | Should this event be collected from the start of the game ? Can Take a lambda with OkamiOptions as parameter to adapt to user yaml settings. A precollected event will not be added as a location, nor in the item pool.                 |

### Locations

Locations are very similar to events, except they give an item from item pool.

| Field                     | Content                | Notes                                                                                                                                                                                                                    |
|---------------------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name                      | string                 | Required.Used as dict key. Must be unique                                                                                                                                                                                |
| id                        | int or None            | Required? Must be unique.                                                                                                                                                                                                |
| required_brush_techniques | BrushTechniques array  | All techniques required to collect that check. (Except power slash and Cherry Bomb;See below)                                                                                                                            |
| power_slash_level         | int                    | Power slash level required to get this check.                                                                                                                                                                            |
| cherry_bomb_level         | int                    | Cherry Bomb level required to get this check.                                                                                                                                                                            |
| buried                    | int                    | Do you need to dig to get this check? 0= no, 1=yes, 2 = yes, with Iron claws                                                                                                                                             |
| required_items_events     | str array              | List of items or events needed to collect this check.                                                                                                                                                                    |
| mandatory_ennemies        | OkamiEnnemies array    | List of enemies you have to defeat to collect this check. This is used for ennemies that requires a specific brush technique to defeat (bud ogre...) and to check for the weapon tier the player currently has.          |
| needs_swim                | boolean                | Is it needed to swim a long distance to collect this check ? (eg. waterlily, orca, or water tablet)                                                                                                                      |

## Coordination

If you want to work on contributing, please fork the main branch of this repository, and open a PR with what you're planning to work on.
This should allow others to see what you're wokring on and not have multiple people working on the same things.

Feel free to review the logic currently merged, or suggest changes to the structure of this.

If you need help or have questions, you can contact me in the [Dedicated Archipelago therad](https://discord.com/channels/731205301247803413/1196620860405067848).


