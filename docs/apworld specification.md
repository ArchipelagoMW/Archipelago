# APWorld Specification

Archipelago depends on worlds to provide game-specific details like items, locations and output generation.
These are called "APWorlds".
They are located in the `worlds/` folder (source) or `<install dir>/lib/worlds/` (when installed).
See [world api.md](world%20api.md) for details.
APWorlds can either be a folder, or they can be packaged as an .apworld file.

## .apworld File Format

.apworld provides a way to package and ship an APWorld that is not part of the main distribution
by placing a `*.apworld` file into the worlds folder.

.apworld files are zip archives, all lower case, with the file ending `.apworld`.
The zip has to contain a folder with the same name as the zip, case-sensitive, that contains what would normally be in
the world's folder in `worlds/`. I.e. `worlds/ror2.apworld` containing `ror2/__init__.py`.

**Warning:** apworlds have to be all lower case,
otherwise they raise a bogus Exception when trying to import in frozen python 3.10+!

## Metadata

Metadata about the APWorld is defined in an `archipelago.json` file.

If the APWorld is a folder, the only required field is "game":
```json
{
  "game": "Game Name"
}
```

If the APWorld is packaged as an .apworld zip file, it also needs to have `version` and `compatible_version`,
which refer to the version of the APContainer packaging scheme defined in [Files.py](../worlds/Files.py):
```json
{
    "version": 6,
    "compatible_version": 5,
    "game": "Game Name"
}
```

with the following optional version fields using the format `"1.0.0"` to represent major.minor.build:
* `minimum_ap_version` and `maximum_ap_version` - which if present will each be compared against the current
  Archipelago version respectively to filter those files from being loaded
* `world_version` - an arbitrary version for that world in order to only load the newest valid world.
  An APWorld without a world_version is always treated as older than one with a version


## Extra Data

The zip can contain arbitrary files in addition what was specified above.


## Caveats

Imports from other files inside the APWorld have to use relative imports. e.g. `from .options import MyGameOptions`

Imports from AP base have to use absolute imports, e.g. `from Options import Toggle` or
`from worlds.AutoWorld import World`
