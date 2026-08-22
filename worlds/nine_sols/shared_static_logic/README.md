# Nine Sols Shared Static Logic

items.py, locations.py and connections.py are the source of truth for the statically known items, locations, regions, connections between regions, and logic / access rules for each location and connection.

"Shared" means these files are used by both this .apworld and by the game mod. See below.

Data files are always "static," but we keep using that world to emphasize that some parts of the logic are dynamic, and thus cannot be represented in the data files.
These features fundamentally require writing "the same code" in both Python and C#.

### In-Game Tracker / C# Usage

The C# code for the "Archipelago Randomizer" mod for Nine Sols is at https://github.com/Ixrec/NineSolsArchipelagoRandomizer.
That repo includes this one as a submodule, so the mod's build process can directly use these .jsonc files (and record in git history exactly which versions were last used).
The mod itself (will hopefully someday) use that information for its in-game tracker, which includes full logic tracking for every location.

That repo assumes we have already converted the .py files into .jsonc files (this should be changed someday).
Part of maintaining this AP integration is running the `serialize_static_data.py` script to generate those .jsonc files.

To run the script, go to the root Archipelago/ folder and run:
```shell
python worlds/nine_sols/shared_static_logic/serialize_static_data.py
```

The unit test `test_logic_files` checks that the generated files are up-to-date.
