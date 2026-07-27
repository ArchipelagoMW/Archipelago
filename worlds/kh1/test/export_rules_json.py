import json
import sys

from . import KH1TestBase
from ..Rules import export_rules_to_dict

MAXIMAL_OPTIONS = {
    "super_bosses": True,
    "cups": "hades_cup",
    "hundred_acre_wood": True,
    "atlantica": True,
    "destiny_islands": True,
    "jungle_slider": True,
    "final_rest_door_key": "lucky_emblems",
}


def main(output_path: str) -> None:
    class _MaximalWorld(KH1TestBase):
        options = MAXIMAL_OPTIONS

    world_test = _MaximalWorld()
    world_test.setUp()

    data = export_rules_to_dict(world_test.world)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Wrote {len(data['locations'])} locations and {len(data['entrances'])} entrances to {output_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "kh1_rules.json")
