## `regions/`

These define regions, connections, and where locations are. If you know what you're doing, it should be pretty clear how
this works by taking a quick look through the files. The rest of this section is pretty verbose to cover everything. Not
to say you shouldn't read it, but the tl;dr is:

- Every map, even trivial ones, gets a region definition, and they cannot be coalesced (because of warp rando)
- Stick to the naming convention for regions and events (look at Route 103 and Petalburg City for guidance)
- Locations and warps can only be claimed by one region
- Events are declared here

A `Map`, which you will see referenced in `parent_map` attribute in the region JSON, is an id from the source code.
`Map`s are sets of tiles, encounters, warps, events, and so on. Route 103, Littleroot Town, the Oldale Town Mart, the
second floor of Devon Corp, and each level of Victory Road are all examples of `Map`s. You transition between `Map`s by
stepping on a warp (warp pads, doorways, etc...) or walking over a border between `Map`s in the overworld. Some warps
don't go to a different `Map`.

Regions usually describe physical areas which are subsets of a `Map`. Every `Map` must have one or more defined regions.
A region should not contain area from more than one `Map`. We'll need to draw those lines now even when there is no
logical boundary (like between two the first and second floors of your rival's house), for warp rando.

Most `Map`s have been split into multiple regions. In the example below, `MAP_ROUTE103` was split into
`REGION_ROUTE_103/WEST`, `REGION_ROUTE_103/WATER`, and `REGION_ROUTE_103/EAST` (this document may be out of date; the
example is demonstrative). Keeping the name consistent with the `Map` name and adding a label suffix for the subarea
makes it clearer where we are in the world and where within a `Map` we're describing.

Every region (except `Menu`) is configured here. All files in this directory are combined with each other at runtime,
and are only split and ordered for organization. Regions defined in `data/regions/unused` are entirely unused because
they're not yet reachable in the randomizer. They're there for future reference in case we want to pull those maps in
later. Any locations or warps in here should be ignored. Data for a single region looks like this:

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

- `[key]`: The name of the object, in this case `REGION_ROUTE103/EAST`, should be the value of `parent_map` where the
`MAP` prefix is replaced with `REGION`. Then there should be a following `/` and a label describing this specific region
within the `Map`. This is not enforced or required by the code, but it makes things much more clear.
- `parent_map`: The name of the `Map` this region exists under. It can relate this region to information like encounter
tables.
- `locations`: Locations contained within this region. This can be anything from an item on the ground to a badge to a
gift from an NPC. Locations themselves are defined in `data/extracted_data.json`, and the names used here should come
directly from it.
- `events`: Events that can be completed in this region. Defeating a gym leader or Aqua/Magma team leader, for example,
can trigger story progression and unblock roads and buildings. Events are defined here and nowhere else, and access
rules are set in `rules.py`.
- `exits`: Names of regions that can be directly accessed from this one. Most often regions within the same `Map`,
neighboring maps in the overworld, or transitions from using HM08 Dive. Most connections between maps/regions come from
warps. Any region in this list should be defined somewhere in `data/regions`.
- `warps`: Warp events contained within this region. Warps are defined in `data/extracted_data.json`, and must exist
there to be referenced here. More on warps in [../README.md](../README.md).

Think of this data as defining which regions are "claiming" a given location, event, or warp. No more than one region
may claim ownership of a location. Even if some "thing" may happen in two different regions and set the same flag, they
should be defined as two different events and anything conditional on said "thing" happening can check whether either of
the two events is accessible. (e.g. Interacting with the Poke Ball in your rival's room and going back downstairs will
both trigger a conversation with them which enables you to rescue Professor Birch. It's the same "thing" on two
different `Map`s.)

Conceptually, you shouldn't have to "add" any new regions. You should only have to "split" existing regions. When you
split a region, make sure to correctly reassign `locations`, `events`, `exits`, and `warps` according to which new
region they now exist in. Make sure to define new `exits` to link the new regions to each other if applicable. And
especially remember to rename incoming `exits` defined in other regions which are still pointing to the pre-split
region. `sanity_check.py` should catch you if there are other regions that point to a region that no longer exists, but
if one of your newly-split regions still has the same name as the original, it won't be detected and you may find that
things aren't connected correctly.

## `extracted_data.json`

DO NOT TOUCH

Contains data automatically pulled from the base rom and its source code when it is built. There should be no reason to
manually modify it. Data from this file is piped through `data.py` to create a data object that's more useful and
complete.

## `items.json`

A map from items as defined in the `constants` in `extracted_data.json` to useful info like a human-friendly label, the
type of progression it enables, and tags to associate. There are many unused items and extra helper constants in
`extracted_data.json`, so this file contains an exhaustive list of items which can actually be found in the modded game.

## `locations.json`

Similar to `items.json`, this associates locations with human-friendly labels and tags that are used for filtering. Any
locations claimed by any region need an entry here.
