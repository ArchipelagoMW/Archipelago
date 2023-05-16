This README is meant as documentation for the files found within the `data/` directory, and especially for describing the shape of the region config.

## `regions/`

These define regions, connections, and where locations are. If you know what you're doing, it should be pretty clear how this works by taking a quick look through the files. The rest of this section is pretty verbose to cover everything. Not to say you shouldn't read it, but the tl;dr is:
- Every map, even trivial ones, gets a region definition, and they cannot be coalesced (to keep warp rando an option)
- Stick to the naming convention for regions and events (look at Route 103 and Petalburg City for guidance)
- Locations and warps can only be claimed by one region
- Events are declared here, their individual access logic is in `Rules.py`

A `Map`, which you will see referenced in `parent_map` attribute in the region JSON, is an id from the source code. `Map`s are sets of tiles, encounters, warps, events, and so on. Route 103, Littleroot Town, the Oldale Town Mart, the second floor of Devon Corp, and each level of Victory Road are all examples of `Map`s. You transition between `Map`s by stepping on a warp (warp pads, doorways, etc...) or walking over a border between `Map`s in the overworld. Some warps don't go to a different `Map`.

Regions must describe physical areas which are subsets of a `Map`. Every `Map` must have one or more defined regions. A region cannot contain tiles from more than one `Map`. We'll need to draw those lines now even when there is no logical boundary (like between two the first and second floors of your rival's house), so that warp rando in the future will be easier.

Every `Map` has at least one region defined for it (with a couple exceptions for multiplayer rooms), and many have been split into multiple regions. In the example below, `MAP_ROUTE103` was split into `REGION_ROUTE_103/WEST`, `REGION_ROUTE_103/WATER`, and `REGION_ROUTE_103/EAST`. Keeping the name consistent with the `Map` name and adding a label suffix for the subarea makes it clearer where we are in the world and where within a map we're describing.

Every region (except `Menu`) is configured here. All files in this directory are appended to each other at runtime, and are only split and ordered for development convenience. Regions defined in `data/regions/unused` are entirely unused because they're not yet reachable in the randomizer. They're there for future reference in case we want to pull those maps in later. Any locations or warps in here should be blacklisted. Data for a single region looks like this:

```json
"REGION_ROUTE103/EAST": {
  "parent_map": "MAP_ROUTE103",
  "locations": [
    "ITEM_ROUTE_103_GUARD_SPEC",
    "ITEM_ROUTE_103_PP_UP"
  ],
  "events": [],
  "exits": [
    "REGION_ROUTE103/WATER",
    "REGION_ROUTE110/MAIN"
  ],
  "warps": [
    "MAP_ROUTE103:0/MAP_ALTERING_CAVE:0"
  ]
}
```

- `[key]`: The name of the object, in this case `REGION_ROUTE103/EAST`, should be the value of `parent_map` where the `MAP` prefix is replaced with `REGION`. Then there should be a following `/` and a label describing this specific region within the `Map`. This is not enforced or required by the code, but it makes things much more clear to developers.
- `parent_map`: The name of the `Map` this region exists under. It can relate this region to information like encounter tables.
- `locations`: Locations, or checks, contained within this region. This can be anything from an item on the ground to a badge to a gift from an NPC. Locations themselves are defined in `data/extracted_data.json`, and the names used here should come directly from it.
- `events`: Events that can be completed in this region. Defeating a gym leader or Aqua/Magma team leader, for example, can trigger story progression and unblock roads and buildings. Events are defined here and nowhere else, and access rules are set in `rules.py`.
- `exits`: Names of regions that can be directly accessed from this one. Most often regions within the same `Map`, neighboring maps in the overworld, or transitions from using HM08 Dive. Most connections between maps/regions come from warps. Any region in this list should be defined somewhere in `data/regions`.
- `warps`: Warp events contained within this region. Warps are defined in `data/extracted_data.json`, and must exist there to be referenced here. More on warps in `../README.md`.

Think of this data as defining which regions are "claiming" a given location, event, or warp. No more than one region may claim ownership of a location. Even if some "thing" may happen in two different regions and set the same flag, they should be defined as two different events and anything conditional on said "thing" happening can check whether either of the two events is accessible. (e.g. Interacting with the Poke Ball in your rival's room and going back downstairs will both trigger a conversation with them which enables you to rescue Professor Birch. It's the same "thing" on two different `Map`s.)

Conceptually, you shouldn't have to "add" any new regions. You should only have to "split" existing regions. When you split a region, make sure to correctly reassign `locations`, `events`, `exits`, and `warps` according to which new region they now exist in. Make sure to define new `exits` to link the new regions to each other if applicable. And especially remember to rename incoming `exits` defined in other regions which are still pointing to the pre-split region. `sanity_check.py` should catch you if there are other regions that point to a region that no longer exists, but if one of your newly-split regions still has the same name as the original, it won't be detected and you may find that things aren't connected correctly.

## `extracted_data.json`

DO NOT TOUCH

This contains data automatically pulled from the base rom and its source code when it is built. There should be no reason to manually modify it. Data from this file is piped through `data.py` to create a data object that's more useful and complete.

## `ignorable_locations.json` and `ignorable_warps.json`

A list of locations or warps that are pulled from `extracted_data.json` but aren't currently factored into logic. Usually these involve dynamic destinations (like Terra/Marine Cave or the Trick House), or they may be part of `Map`s/regions that aren't accessible in the randomizer (like event islands). More on warps in `../README.md`.

Note: These lists suppress warnings, but don't actually filter anything. They're indications that the sanity check should not care whether they were included in any regions or not. If a location is claimed by a region and also listed in `ignorable_locations.json`, generation will carry on as if it were not listed in `ignorable_locations.json`.

## `items.json`

A map from items as defined in the `constants` in `extracted_data.json` to useful info like a human-friendly label, the type of progression it enables, and tags to associate. There are many unused items and extra helper constants in `extracted_data.json`, so this file contains an exhaustive list of items which can actually be found in the modded game.

## `pokemon.json`

Similar to `items.json`, maps the constant name for a pokemon species to a human-friendly label and its national dex id. The source code values for species do not match up with their national dex id. Gen 3 mons look to be in hoenn dex order, and there is a gap between the end of gen 2 and the start of gen 3 for unused Unown variants.
