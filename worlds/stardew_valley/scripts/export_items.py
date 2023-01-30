import json
import os.path

from worlds.stardew_valley import item_table

if not os.path.isdir('output'):
    os.mkdir('output')

if __name__ == "__main__":
    with open("output/stardew_valley_item_table.json", "w+") as f:
        items = {
            item.name: {
                "code": item.code,
                "classification": item.classification.name
            }
            for item in item_table.values()
            if item.code is not None
        }
        json.dump({"items": items}, f)
