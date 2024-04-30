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

No metadata is specified yet.


## Extra Data

The zip can contain arbitrary files in addition what was specified above.


## Caveats

Imports from other files inside the apworld have to use relative imports. e.g. `from .options import MyGameOptions`

Imports from AP base have to use absolute imports, e.g. `from Options import Toggle` or
`from worlds.AutoWorld import World`
