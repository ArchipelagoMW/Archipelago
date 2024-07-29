"""Locations export script
This script can be used to export all the AP locations into a json file in the output folder. This file is used by the
tests of the mod to ensure it can handle all possible locations.

To run the script, use `python -m worlds.stardew_valley.scripts.export_locations` from the repository root.
"""

import json
import os

from worlds.stardew_valley import location_table

if not os.path.isdir("output"):
    os.mkdir("output")

if __name__ == "__main__":
    with open("output/stardew_valley_location_table.json", "w+") as f:
        locations = {
            "Cheat Console":
                {"code": -1, "region": "Archipelago"},
            "Server":
                {"code": -2, "region": "Archipelago"}
        }
        locations.update({
            location.name: {
                "code": location.code,
                "region": location.region,
            }
            for location in location_table.values()
            if location.code is not None
        })
        json.dump({"locations": locations}, f)
