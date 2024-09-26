import argparse
import json

from ...options import FarmType, EntranceRandomization
from ...test import setup_solo_multiworld, allsanity_mods_6_x_x

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='Define seed number to generate.', type=int, required=True)

    args = parser.parse_args()
    seed = args.seed

    options = allsanity_mods_6_x_x()
    options[FarmType.internal_name] = FarmType.option_standard
    options[EntranceRandomization.internal_name] = EntranceRandomization.option_buildings
    multi_world = setup_solo_multiworld(options, seed=seed)

    world = multi_world.worlds[1]
    output = {
        "bundles": {
            bundle_room.name: {
                bundle.name: str(bundle.items)
                for bundle in bundle_room.bundles
            }
            for bundle_room in world.modified_bundles
        },
        "items": [item.name for item in multi_world.get_items()],
        "location_rules": {location.name: repr(location.access_rule) for location in multi_world.get_locations(1)},
        "slot_data": world.fill_slot_data()
    }

    print(json.dumps(output))
else:
    raise RuntimeError("Do not import this file, execute it in different python session so the PYTHONHASHSEED is different..")
