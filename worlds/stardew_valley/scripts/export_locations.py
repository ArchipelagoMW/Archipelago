import json
import os

from worlds.stardew_valley import location_table

if not os.path.isdir('output'):
    os.mkdir('output')

if __name__ == "__main__":
    with open("output/stardew_valley_location_table.json", "w+") as f:
        locations = {
            location.name: {
                "code": location.code,
                "region": location.region,
            }
            for location in location_table.values()
            if location.code is not None
        }
        json.dump({"locations": locations}, f)
