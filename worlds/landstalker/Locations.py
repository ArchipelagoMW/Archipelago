from typing import Dict, Optional

from BaseClasses import Location, ItemClassification, Item
from .Regions import LandstalkerRegion
from .data.item_source import ITEM_SOURCES_JSON
from .data.world_path import WORLD_PATHS_JSON

BASE_LOCATION_ID = 4000
BASE_GROUND_LOCATION_ID = BASE_LOCATION_ID + 256
BASE_SHOP_LOCATION_ID = BASE_GROUND_LOCATION_ID + 30
BASE_REWARD_LOCATION_ID = BASE_SHOP_LOCATION_ID + 50


class LandstalkerLocation(Location):
    game: str = "Landstalker - The Treasures of King Nole"
    type_string: str
    price: int = 0

    def __init__(self, player: int, name: str, location_id: Optional[int], region: LandstalkerRegion, type_string: str):
        super().__init__(player, name, location_id, region)
        self.type_string = type_string


def create_locations(player: int, regions_table: Dict[str, LandstalkerRegion], name_to_id_table: Dict[str, int]):
    # Create real locations from the data inside the corresponding JSON file
    for data in ITEM_SOURCES_JSON:
        region_id = data["nodeId"]
        region = regions_table[region_id]
        new_location = LandstalkerLocation(player, data["name"], name_to_id_table[data["name"]], region, data["type"])
        region.locations.append(new_location)

    # Create fake event locations that will be used to determine if some key regions has been visited
    regions_with_entrance_checks = []
    for data in WORLD_PATHS_JSON:
        if "requiredNodes" in data:
            regions_with_entrance_checks.extend([region_id for region_id in data["requiredNodes"]])
    regions_with_entrance_checks = sorted(set(regions_with_entrance_checks))
    for region_id in regions_with_entrance_checks:
        region = regions_table[region_id]
        location = LandstalkerLocation(player, 'event_visited_' + region_id, None, region, "event")
        location.place_locked_item(Item("event_visited_" + region_id, ItemClassification.progression, None, player))
        region.locations.append(location)

    # Create a specific end location that will contain a fake win-condition item
    end_location = LandstalkerLocation(player, "End", None, regions_table["end"], "reward")
    regions_table["end"].locations.append(end_location)


def build_location_name_to_id_table():
    location_name_to_id_table = {}

    for data in ITEM_SOURCES_JSON:
        if data["type"] == "chest":
            location_id = BASE_LOCATION_ID + int(data["chestId"])
        elif data["type"] == "ground":
            location_id = BASE_GROUND_LOCATION_ID + int(data["groundItemId"])
        elif data["type"] == "shop":
            location_id = BASE_SHOP_LOCATION_ID + int(data["shopItemId"])
        else:  # if data["type"] == "reward":
            location_id = BASE_REWARD_LOCATION_ID + int(data["rewardId"])
        location_name_to_id_table[data["name"]] = location_id

    # Win condition location ID
    location_name_to_id_table["Gola"] = BASE_REWARD_LOCATION_ID + 10

    return location_name_to_id_table
