from typing import Dict, Optional

from BaseClasses import Location
from .Regions import LandstalkerRegion
from .data.item_source import ITEM_SOURCES_JSON

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
