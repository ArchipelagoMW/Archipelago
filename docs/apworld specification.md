# apworld Specification

Archipelago depends on worlds to provide game-specific details like items, locations and output generation.
Those are located in the `worlds/` folder (source) or `<install dir>/lib/worlds/` (when installed).
See [world api.md](world%20api.md) for details.

apworld provides a way to package and ship a world that is not part of the main distribution by placing a `*.apworld`
file into the worlds folder.

**Warning:** apworlds have to be all lower case, otherwise they raise a bogus Exception when trying to import in frozen python 3.10+!


## File Format

apworld files are zip archives, all lower case, with the file ending `.apworld`.
The zip has to contain a folder with the same name as the zip, case-sensitive, that contains what would normally be in
the world's folder in `worlds/`. I.e. `worlds/ror2.apworld` containing `ror2/__init__.py`.


## Metadata

Metadata about the apworld is defined in an `archipelago.json` file inside the zip archive.
The current format version has at minimum:
```json
{
    "version": 6,
    "compatible_version": 5,
    "game": "Game Name"
}
```

The `version` and `compatible_version` fields get automatically added to the `archipelago.json`
of an .apworld if it is packaged using the ["Build apworlds" launcher component](#build-apworlds-launcher-component),
which is strongly recommended instead of trying to write these yourself.  
The `game` field should be present in any handwritten apworld manifest files.

There are also the following optional version fields (using the format `"1.0.0"` to represent major.minor.build):
* `minimum_ap_version` and `maximum_ap_version` - which if present will each be compared against the current
  Archipelago version respectively to filter those files from being loaded
* `world_version` - an arbitrary version for that world in order to only load the newest valid world.
  An apworld without a world_version is always treated as older than one with a version

### "Build apworlds" Launcher Component

In the Archipelago Launcher, there is a "Build apworlds" component that will package all world folders to `.apworld`,
and add `archipelago.json` manifest files to them.  
This `archipelago.json` will contain the appropriate `version`, `compatible_version`, and `game` fields automatically
(`game` is taken from your world class).

If a world folder has an `archipelago.json` in its root, any fields it contains will be carried over.  
So, a world folder with an `archipelago.json` that looks like this:

```json
{
    "game": "Game Name",
    "minimum_ap_version": "0.6.4",
    "world_version": "2.1.4"
}
```

will be packaged into an `.apworld` with a manifest file inside of it that looks like this:

```json
{
    "minimum_ap_version": "0.6.4", 
    "world_version": "2.1.4",
    "version": 6,
    "compatible_version": 5,
    "game": "Game Name"
}
```

This is the recommended workflow for packaging your world to an `.apworld`.

## Extra Data

The zip can contain arbitrary files in addition what was specified above.


## Caveats

Imports from other files inside the apworld have to use relative imports. e.g. `from .options import MyGameOptions`

Imports from AP base have to use absolute imports, e.g. `from Options import Toggle` or
`from worlds.AutoWorld import World`
