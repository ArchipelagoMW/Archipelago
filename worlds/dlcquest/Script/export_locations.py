"""Locations export script
This script can be used to export all the AP locations into a json file in the output folder. This file is used by the
tests of the mod to ensure it can handle all possible locations.

To run the script, use `python -m worlds.stardew_valley.scripts.export_locations` from the repository root.
"""

import json
import os

from worlds.dlcquest import location_table

if not os.path.isdir("output"):
    os.mkdir("output")

if __name__ == "__main__":
    with open("output/dlc_quest_location_table.json", "w+") as f:
        locations = location_table
           
        json.dump({"locations": locations}, f)
