# Outer Wilds Shared Static Logic

These .jsonc files are the source of truth for the statically known items, locations, regions, connections between regions, and logic / access rules for each location and connection.

If you haven't heard of .jsonc before, it's just JSON with Comments.
Those files have a lot of valuable comments explaining subtleties of the logic.

"Shared" means these files are used by both this .apworld and by the game mod. See below.

Data files are always "static," but we keep using that world to emphasize that some parts of the logic are dynamic, and thus cannot be represented in the data files.
The main examples are random spawn and warp platform randomization.
These features fundamentally require writing "the same code" in both Python and C#.

### .apworld / Python Usage

Part of maintaining this .apworld is running the `pickle_static_data.py` script to convert those .jsonc files into serialized Python data structures.
Archipelago cares a lot about world load times, and loading non-standard .jsonc is slow, loading clean .json is fast-ish, but loading pickled/serialized Python data is as fast as it gets in Python.

When I tested this using test/benchmark/load_worlds.py, I found OW took ~10-50ms to load with .jsonc, ~6-10ms with clean .json, and ~6-7ms with pickle.

To run the script, go to the root Archipelago/ folder and run:
```shell
python worlds/outer_wilds/shared_static_logic/pickle_static_logic.py
```

The unit test `test_pickle_file_hashes` checks that the generated `static_logic.pickle` file is up-to-date.

### In-Game Tracker / C# Usage

The C# code for the "Archipelago Randomizer" mod for Outer Wilds is at https://github.com/Ixrec/OuterWildsArchipelagoRandomizer.
That repo includes this one as a submodule, so the mod's build process can directly use these .jsonc files (and record in git history exactly which versions were last used).
The mod itself then uses that information for its in-game tracker, which includes full logic tracking for every location.