# APWorld Specification

Archipelago depends on worlds to provide game-specific details like items, locations and output generation.
These are called "APWorlds".
They are located in the `worlds/` folder (source) or `<install dir>/lib/worlds/` (when installed).
See [world api.md](world%20api.md) for details.
APWorlds can either be a folder, or they can be packaged as an .apworld file.

## .apworld File Format

The `.apworld` file format provides a way to package and ship an APWorld that is not part of the main distribution
by placing a `*.apworld` file into the worlds folder.

`.apworld` files are zip archives, all lower case, with the file ending `.apworld`.
The zip has to contain a folder with the same name as the zip, case-sensitive, that contains what would normally be in
the world's folder in `worlds/`. I.e. `worlds/ror2.apworld` containing `ror2/__init__.py`.

**Warning:** `.apworld` files have to be all lower case,
otherwise they raise a bogus Exception when trying to import in frozen python 3.10+!

## Metadata

Metadata about the APWorld is defined in an `archipelago.json` file.

If the APWorld is a folder, the only required field is "game":
```json
{
  "game": "Game Name"
}
```

There are also the following optional fields:
* `minimum_ap_version` and `maximum_ap_version` - which if present will each be compared against the current
  Archipelago version respectively to filter those files from being loaded.
* `world_version` - an arbitrary version for that world in order to only load the newest valid world.
  An APWorld without a world_version is always treated as older than one with a version
  (**Must** use exactly the format `"major.minor.build"`, e.g. `1.0.0`)
* `authors` - a list of authors, to eventually be displayed in various user-facing places such as WebHost and
  package managers. Should always be a list of strings.

If the APWorld is packaged as an `.apworld` zip file, it also needs to have `version` and `compatible_version`,
which refer to the version of the APContainer packaging scheme defined in [Files.py](../worlds/Files.py).  
These get automatically added to the `archipelago.json` of an .apworld if it is packaged using the 
["Build APWorlds" launcher component](#build-apworlds-launcher-component),
which is the correct way to package your `.apworld` as a world developer. Do not write these fields yourself.

### "Build APWorlds" Launcher Component

In the Archipelago Launcher, there is a "Build APWorlds" component that will package all world folders to `.apworld`,
and add `archipelago.json` manifest files to them.  
These .apworld files will be output to `build/apworlds` (relative to the Archipelago root directory).  
The `archipelago.json` file in each .apworld will automatically include the appropriate
`version` and `compatible_version`.  
The component can also be called from the command line to allow for specifying a certain list of worlds to build.
For example, running `Launcher.py "Build APWorlds" -- "Game Name"` will build only the game called `Game Name`.

If a world folder has an `archipelago.json` in its root, any fields it contains will be carried over.  
So, a world folder with an `archipelago.json` that looks like this:

```json
{
    "game": "Game Name",
    "minimum_ap_version": "0.6.4",
    "world_version": "2.1.4",
    "authors": ["NewSoupVi"]
}
```

will be packaged into an `.apworld` with a manifest file inside of it that looks like this:

```json
{
    "minimum_ap_version": "0.6.4", 
    "world_version": "2.1.4",
    "authors": ["NewSoupVi"],
    "version": 7,
    "compatible_version": 7,
    "game": "Game Name"
}
```

This is the recommended workflow for packaging your world to an `.apworld`.

### .apignore Exclusions

By default, any additional files inside of the world folder will be packaged into the resulting `.apworld` archive and
can then be read by the world. However, if there are any other files that aren't needed in the resulting `.apworld`, you
can automatically prevent the build component from including them by specifying them in a file called `.apignore` inside
the root of the world folder.

The `.apignore` file selects files in the same way as the `.gitignore` format with patterns separated by line describing
which files to ignore. For example, an `.apignore` like this:

```gitignore
*.iso
scripts/
!scripts/needed.py
```

would ignore any `.iso` files and anything in the scripts folder except for `scripts/needed.py`.

Some exclusions are made by default for all worlds such as `__pycache__` folders. These are listed in the
`GLOBAL.apignore` file inside of the `data` directory.

## Caveats

Imports from other files inside the APWorld have to use relative imports. e.g. `from .options import MyGameOptions`

Imports from AP base have to use absolute imports, e.g. `from Options import Toggle` or
`from worlds.AutoWorld import World`
