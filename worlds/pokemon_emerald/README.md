# Pokemon Emerald

Version 1.2.0

This README contains general info useful for understanding the world. Pretty much all the long lists of locations,
regions, and items are stored in `data/` and (mostly) loaded in by `data.py`. Access rules are in `rules.py`. Check
[data/README.md](data/README.md) for more detailed information on the JSON files holding most of the data.

## Warps

Quick note to start, you should not be defining or modifying encoded warps from this repository. They're encoded in the
source code repository for the mod, and then assigned to regions in `data/regions/`. All warps in the game already exist
within `extracted_data.json`, and all relevant warps are already placed in `data/regions/` (unless they were deleted
accidentally).

Many warps are actually two or three events acting as one logical warp. Doorways, for example, are often 2 tiles wide
indoors but only 1 tile wide outdoors. Both indoor warps point to the outdoor warp, and the outdoor warp points to only
one of the indoor warps. We want to describe warps logically in a way that retains information about individual warp
events. That way a 2-tile-wide doorway doesnt look like a one-way warp next to an unrelated two-way warp, but if we want
to randomize the destinations of those warps, we can still get back each individual id of the multi-tile warp.

This is how warps are encoded:

`{source_map}:{source_warp_ids}/{dest_map}:{dest_warp_ids}[!]`

- `source_map`: The map the warp events are located in
- `source_warp_ids`: The ids of all adjacent warp events in source_map which lead to the same destination (these must be
in ascending order)
- `dest_map`: The map of the warp event to which this one is connected
- `dest_warp_ids`: The ids of the warp events in dest_map
- `[!]`: If the warp expects to lead to a destination which doesnot lead back to it, add a ! to the end

Example: `MAP_LAVARIDGE_TOWN_HOUSE:0,1/MAP_LAVARIDGE_TOWN:4`

Example 2: `MAP_AQUA_HIDEOUT_B1F:14/MAP_AQUA_HIDEOUT_B1F:12!`

Note: A warp must have its destination set to another warp event. However, that does not guarantee that the destination
warp event will warp back to the source.

Note 2: Some warps _only_ act as destinations and cannot actually be interacted with by the player as sources. These are
usually places you fall from a hole above. At the time of writing, these are actually not accounted for, but there are
no instances where it changes logical access.

Note 3: Some warp destinations go to the map `MAP_DYNAMIC` and have a special warp id. These edge cases are:

- The Moving Truck
- Terra Cave
- Marine Cave
- The Department Store Elevator
- Secret Bases
- The Trade Center
- The Union Room
- The Record Corner
- 2P/4P Battle Colosseum

Note 4: The trick house on Route 110 changes the warp destinations of its entrance and ending room as you progress
through the puzzles, but the source code only sets the trick house up for the first puzzle, and I assume the destination
gets overwritten at run time when certain flags are set.
