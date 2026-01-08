"""
This is the entry point of the codegen module, a script that runs the code generation, producing:
- `Locations.py' from `Locations.template.py'
- `Items.py' from `Items.template.py'
This process requires a few data files.
Put the following files in the `data' directory:
- `assets' from your CrossCode installation
- `data/in' from the CCMultiworldRandomizer mod
This script also produces a copy of the json files in `data/in`, all combined together, with additional metadata for
the mod, called `data.json`.

Copy `data/out/data.json` into `CCMultiworldRandomizer/data`
To run it for yourself, navigate to the root directory and run `python -m worlds.crosscode.codegen`
"""

import argparse

from .context import make_context_from_package
from .gen import FileGenerator
from .lists import ListInfo

parser = argparse.ArgumentParser(
    prog="CrossCode Code Generation",
    description="Generate python interfaces for CrossCode APWorld"
)

parser.add_argument(
    "-p", "--no-python-interfaces",
    dest="python",
    action="store_false",
    help="Don't generate Items.py, Location.py, etc. Instead, pull this data from the existing files"
)

parser.add_argument(
    "-m", "--no-mod-data",
    dest="mod",
    action="store_false",
    help="Don't generate out/data.json for the mod"
)

parser.add_argument(
    "-a", "--no-archipelago-data",
    dest="archipelago",
    action="store_false"
)

namespace = parser.parse_args()

if namespace.python:
    fg = FileGenerator("worlds/crosscode")
    fg.generate_python_files()
else:
    from ..items import items_dict, single_items_dict
    from ..locations import locations_dict, events_dict

    ctx = make_context_from_package("worlds.crosscode")

    lists = ListInfo(ctx)
    lists.single_items_dict = single_items_dict
    lists.items_dict = items_dict
    lists.locations_data = locations_dict
    lists.events_data = events_dict

    fg = FileGenerator("worlds/crosscode", lists)

if namespace.mod:
    fg.generate_mod_files()
