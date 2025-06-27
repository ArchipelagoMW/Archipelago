# Okami HD APWorld Contribution Guide

## Introduction

This is the APWorld data for Okami HD; It's meant to be used with the [Okami APClient Mod](https://github.com/Axertin/okami-apclient).

The goal of these files is to describe all Items, Locations and Regions that are used to randomize the game.
For more info on what this means, check the [Archipelago Autoworld Docs](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md).

## What needs to be done?

Currently, there only exists a stub of logic that goes from the start of the game to the Entrance of Tsuta ruins. There's probably some checks that I might have missed, feel free to message me if you find one.
You can help by contributing to logic. The checks we need to have in the logic are currently limited to only these:
- Brush Techniques (except Mist Warp bc we're not randomizing shops yet,still we'll probably add it in the item pool for convenience)
- Chest Items, and Item given by quests

## How does logic work ? 

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

Exits are always considered as going both ways: If you want to connect Kamiki to Shinshu, you only need an Exit from Kamiki to Shinshu or an Exit from Shinshu to Kamiki, but not both.


