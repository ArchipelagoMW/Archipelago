# Okami HD APWorld Contribution Guide

## Introduction

This is the APWorld data for Okami HD; It's meant to be used with
the [Okami APClient Mod](https://github.com/Axertin/okami-apclient).

The goal of these files is to describe all Items, Locations and Regions that are used to randomize the game.
For more info on what this means, check
the [Archipelago Autoworld Docs](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md).

English is not my native language; I hope this guide is clear; Feel free to message me if it's not.

## What needs to be done?

Main releases will only include logic up to the end of moon cave, while we're ironing out how we can remove softlocks
and properly randomize what we want.
In the meantime, logic for the reminder of the game is being wirtten. But getting arc1 to work properly will always take
priority.
There might be some checks that I might have missed, feel free to message me if you find one.
You can help by contributing to logic here or over to the [client mod](https://github.com/Axertin/okami-apclient).

The checks we need to have in the logic are currently limited to only these:

- Brush Techniques
- Chest Items, and Item given by main quests
- Merchants

## How does logic work ?

*Note: These structures will probably change with time, I'll try to keep the guide up to date*

Logic is currently stored in the RegionData Folder. Each file in the folder represents a different in-game map,
as [listed by the game](https://github.com/whataboutclyde/okami-utils/blob/master/data/area_id.yaml).

Each of these files is split in three parts:

### Exits

For each Region described in the file, you need to contribute all exits that connect to another Region.
The ExitData struc works as follows:

| Field           | Content      | Notes                                                                                                      | Default Value |
|-----------------|--------------|------------------------------------------------------------------------------------------------------------|---------------|
| destination     | string       | Required. The Region this exits leads to. Please make sure you use a element of the RegionNames enum.      | N/A           |
| has_events      | string array | List of events that need to be cleared before being able to use this exit.                                 | []            |
| needs_long_swim | boolean      | Is it needed to swim a long distance to use this exit ? (eg. waterlily, orca, or water tablet)             | False         |
| one_way         | boolean      |                                                                                                            | False         |
| loading_screen  | boolean      | (very baldly named property) Stuff for later when we want to do ER; Should that transition be randomized ? | True          |

Note that a Region can be a part of a map or a sequence, it's basically a way to share access rules between some
locations or events;

Exits:

- should only require events to be traversable, **techically**, you could put item names in *has_events* and it should
  work. But I'd rather have an event that represents blowing up a boulder that allows an exit, than an exit requiring
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

| Field                     | Content                          | Notes                                                                                                                                                                                                                    | Default Value                |
|---------------------------|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| Name                      | string                           | Required.Used as dict key. Must be unique                                                                                                                                                                                | N/A                          |
| id                        | int or None                      | Only required if the event can be precollected or a seperate Item.                                                                                                                                                       | None                         |
| type                      | LocationType                     | What kind of location is that event ? (Chest, underwater chest, treasure bud )                                                                                                                                           | LocationType.Event           |
| required_brush_techniques | BrushTechniques array            | All techniques required to collect that event. (Except power slash and Cherry Bomb;See below)                                                                                                                            | []                           |
| power_slash_level         | int                              | Power slash level required to get this event.                                                                                                                                                                            | 0                            |
| cherry_bomb_level         | int                              | Cherry Bomb level required to get this event.                                                                                                                                                                            | 0                            |
| event_item_name           | str or None                      | Name given if we need that event to be "given" to the player like an item                                                                                                                                                | None                         |                                                                                              
| required_items_events     | str array                        | List of items or events needed to collect this event.                                                                                                                                                                    | []                           |
| mandatory_enemies         | OkamiEnemies array               | List of enemies you have to defeat to collect this event. This is used for enemies that requires a specific brush technique to defeat (bud ogre...) and to check for the weapon tier the player currently has.           | []                           |
| needs_long_swim           | boolean                          | Is it needed to swim a long distance to collect this event ? (eg. waterlily, orca, or water tablet)                                                                                                                      | False                        |
| precollected              | boolean or function              | Should this event be collected from the start of the game ? Can Take a lambda with OkamiOptions as parameter to adapt to user yaml settings. A precollected event will not be added as a location, nor in the item pool. | False                        |
| is_event_item             | boolean or function              | Should this event be split in a location and an item in the item pool. Can Take a lambda with OkamiOptions as parameter to adapt to user yaml settings.                                                                  | False                        |
| progress_type             | LocationProgressType or function | If this event is split into an item and a location, the LocationProgressType for the location. Can also take a lambda.                                                                                                   | LocationProgressType.DEFAULT |
| special_rule              | Rule or None                     | Additional access rule that will be added with other rules on the event                                                                                                                                                  | None                         |

### Locations

Locations are very similar to events, except they give an item from item pool.

| Field                     | Content               | Notes                                                                                                                                                                                                           | Default Value                |
|---------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| Name                      | string                | Required.Used as dict key. Must be unique                                                                                                                                                                       | N/A                          |
| id                        | int                   | Required, use functions in CheckIds and [container.json](https://github.com/user-attachments/files/26185358/containers.json) to get the right Id.                                                               | N/A                          |
| type                      | LocationType          | The type of location (buried chest, frozen chest,etc...). Will automatically require the right techinques/items to open the chest depending of this                                                             | LocationType.NORMAL_CHEST    |
| required_brush_techniques | BrushTechniques array | All techniques required to collect that check. (Except power slash and Cherry Bomb;See below)                                                                                                                   | []                           |
| power_slash_level         | int                   | Power slash level required to get this check.                                                                                                                                                                   | 0                            |
| cherry_bomb_level         | int                   | Cherry Bomb level required to get this check.                                                                                                                                                                   | 0                            |
| required_items_events     | str array             | List of items or events needed to collect this check.                                                                                                                                                           | []                           |
| mandatory_enemies         | OkamiEnemies array    | List of enemies you have to defeat to collect this check. This is used for ennemies that requires a specific brush technique to defeat (bud ogre...) and to check for the weapon tier the player currently has. | []                           |
| needs_long_swim           | boolean               | Is it needed to swim a long distance to collect this check ? (eg. waterlily, orca, or water tablet)                                                                                                             | False                        | 
| praise_sanity             | int                   | Used to mark locations related to praise randomization. NOT YET USED                                                                                                                                            | 0                            |
| progress_type             | LocationProgressType  | The location type for archipelago                                                                                                                                                                               | LocationProgressType.DEFAULT |
| special_rule              | Rule or None          | Additional access rule that will be added with other rules on the event                                                                                                                                         | None                         |

Merchants should be declared on their own part of the file, called shop_locations, they still use LocData.

Feel free to review the logic currently merged, or suggest changes to the structure of this.

If you need help or have questions, you can contact me in
the [Dedicated Archipelago therad](https://discord.com/channels/731205301247803413/1196620860405067848).


