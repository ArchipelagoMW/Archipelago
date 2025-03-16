import typing

from BaseClasses import ItemClassification
from worlds.AutoWorld import World, WebWorld
from .locations import location_descriptions, locations
from .items import items, CandyBox2Item
from .options import CandyBox2Options


class CandyBox2World(World):
    """Text-based web game with fun ASCII art"""

    game = "Candy Box 2"
    base_id = 1
    location_name_to_id = {name: id for id, name in enumerate(locations, base_id)}
    item_name_to_id = {name: id for id, name in enumerate(items, base_id)}
    options_dataclass = CandyBox2Options
    options: CandyBox2Options
    settings: typing.ClassVar[CandyBox2Options]
    topology_present = True

    def create_item(self, name: str) -> CandyBox2Item:
        return CandyBox2Item(name, ItemClassification.useful, 1, self.player)

class CandyBox2WebWorld(WebWorld):
    location_descriptions = location_descriptions
