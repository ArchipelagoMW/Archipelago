import argparse
import json

from ...test import setup_solo_multiworld, allsanity_options_with_mods

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='Define seed number to generate.', type=int, required=True)

    args = parser.parse_args()
    seed = args.seed

    multi_world = setup_solo_multiworld(
        allsanity_options_with_mods(),
        seed=seed
    )

    output = {
        "bundles": {
            bundle_room.name: {
                bundle.name: str(bundle.items)
                for bundle in bundle_room.bundles
            }
            for bundle_room in multi_world.worlds[1].modified_bundles
        },
        "items": [item.name for item in multi_world.get_items()],
        "location_rules": {location.name: repr(location.access_rule) for location in multi_world.get_locations(1)}
    }

    print(json.dumps(output))
else:
    raise RuntimeError("Do not import this file, execute it in different python session so the PYTHONHASHSEED is different..")
