from typing import List, Mapping, Any

from BaseClasses import MultiWorld, Item, Region
from worlds.AutoWorld import WebWorld, World
from .data.strings import SPZ
from .items import Shapez2Item, item_table, filler_items, delivery_unlocks
from .locations import shapesanity_locations, location_table
from .options import Shapez2Options
from .regions import get_regions


class Shapez2Web(WebWorld):
    rich_text_options_doc = True
    theme = "partyTime"


class Shapez2World(World):
    """
    shapez 2 is an automation game about cutting, rotating, stacking, and painting shapes, that you extract from
    randomly generated islands in an infinite space, without the need to manage your infinite resources or to pay for
    building your factories.
    """
    game = SPZ.game_name
    is_experimental = True
    options_dataclass = Shapez2Options
    options: Shapez2Options
    topology_present = True
    web = Shapez2Web()
    base_id = 20250105
    item_name_to_id = {name: id for id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_table.keys(), base_id)}

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def create_item(self, name: str) -> Item:
        return Shapez2Item(name, item_table[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return list(filler_items.keys())[self.random.randint(0, len(filler_items)-1)]

    def create_regions(self) -> None:
        self.multiworld.regions.extend(get_regions(self.location_name_to_id, self.player, self.multiworld))

    def create_items(self) -> None:
        self.multiworld.itempool.extend([self.create_item(key) for key in delivery_unlocks] +
                                        [self.create_item(self.get_filler_item_name()) for _ in range(1)])

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {"shapes": SPZ.shapes}
