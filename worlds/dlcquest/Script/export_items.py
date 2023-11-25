"""Items export script
This script can be used to export all the AP items into a json file in the output folder. This file is used by the tests
of the mod to ensure it can handle all possible items.

To run the script, use `python -m worlds.dlcquest.Script.export_items` from the repository root.
"""

import json
import os.path

from worlds.dlcquest import item_table

if not os.path.isdir("output"):
    os.mkdir("output")

if __name__ == "__main__":
    with open("output/dlc_quest_item_table.json", "w+") as f:
        items = {
            item.name: {
                "code": item.code,
                "classification": item.classification.name
            }
            for item in item_table.values()
            if item.code is not None
        }
        json.dump({"items": items}, f)
