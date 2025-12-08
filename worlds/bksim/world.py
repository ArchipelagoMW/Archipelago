from typing import Any

from BaseClasses import Region, MultiWorld
from worlds.AutoWorld import World
from . import locations, items, regions, rules, options, web_world
from .common import *


class BKSimWorld(World):
    """
    BK Simulator is a simple game where you walk to BK and back.
    """

    game = game_name
    topology_present = False
    web = web_world.BKSimWebWorld()
    options_dataclass = options.BKSim_Options
    options: options.BKSim_Options
    location_name_to_id = locations.location_name_to_id
    item_name_to_id = items.item_name_to_id

    origin_region_name = RID.HOME

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        regions.create_regions(self)

    def create_items(self) -> None:
        items.create_items(self)

    def create_item(self, name: str) -> items.BKSim_Item:
        return items.create_item(name, self.player)

    def set_rules(self) -> None:
        rules.set_rules(self)

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            'LocsPerWeather': self.options.locs_per_weather.value,
            'StartDistance': self.options.start_distance.value,
            'SpeedPerUpgrade': self.options.speed_per_upgrade.value,
        }

    def get_region(self, region_name: str) -> Region:
        return self.multiworld.get_region(region_name, self.player)
