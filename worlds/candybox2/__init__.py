import typing
import uuid

from BaseClasses import CollectionState
from entrance_rando import ERPlacementState
from worlds.AutoWorld import World, WebWorld
from .locations import location_descriptions, locations
from .items import items, CandyBox2Item
from .options import CandyBox2Options
from .regions import create_regions, connect_entrances


class CandyBox2World(World):
    """Text-based web game with fun ASCII art"""

    game = "Candy Box 2"
    base_id = 1
    location_name_to_id = locations
    item_name_to_id = {name: data.code for name, data in items.items() if data.code is not None}
    options_dataclass = CandyBox2Options
    topology_present = True

    entrance_randomisation: ERPlacementState = None

    def create_regions(self) -> None:
        return create_regions(self.multiworld, self.options, self.player)

    def create_item(self, name: str) -> CandyBox2Item:
        data = items[name]
        item = CandyBox2Item(name, data.classification, data.code, self.player)

        return item

    def create_items(self):
        for name, data in items.items():
            if data.required_amount > 0:
                for i in range(data.required_amount):
                    self.multiworld.itempool += [self.create_item(name)]

    def connect_entrances(self) -> None:
        connect_entrances(self)

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            "uuid": str(uuid.uuid4()),
            "entranceInformation": self.entrance_randomisation.pairings,
        }

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)

    def completion_rule(self, state: CollectionState):
        return state.has("Progressive World Map", self.player, 7) and \
            state.has("The P Stone", self.player) and \
            state.has("The L Stone", self.player) and \
            state.has("The A Stone", self.player) and \
            state.has("The Y Stone", self.player) and \
            state.has("Locked Candy Box", self.player)

class CandyBox2WebWorld(WebWorld):
    location_descriptions = location_descriptions
