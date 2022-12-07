import json
import os
import typing

from BaseClasses import ItemClassification, Tutorial
from .Items import item_table, V6Item
from .Locations import location_table, V6Location
from .Options import v6_options
from .Regions import create_regions, v6_areas
from .Rules import set_rules
from ..AutoWorld import World, WebWorld


class V6Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up VVVVVV for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing"]
    )]


class V6World(World):
    """
     VVVVVV is a platform game all about exploring one simple mechanical idea - what if you reversed gravity instead of jumping?
    """

    game = "VVVVVV"
    topology_present = True
    item_name_to_id = item_table
    location_name_to_id = location_table
    option_definitions = v6_options
    data_version = 1
    web = V6Web()
    area_connections: typing.Dict[int, int]
    area_cost_map: typing.Dict[int, int]
    music_map: typing.Dict[int, int]

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str, progression: bool = False) -> V6Item:
        return V6Item(
            name,
            ItemClassification.progression if progression else ItemClassification.filler,
            item_table[name],
            self.player)

    def generate_early(self):
        self.area_connections = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
        self.area_cost_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

        # Area Randomization
        if self.multiworld.AreaRandomizer[self.player]:
            shuffled_areas = list(range(len(v6_areas)))
            self.multiworld.random.shuffle(shuffled_areas)
            self.area_connections.update({(index + 1): (value + 1) for index, value in enumerate(shuffled_areas)})

            if self.multiworld.AreaCostRandomizer[self.player]:
                self.multiworld.random.shuffle(shuffled_areas)
                self.area_cost_map.update({(index + 1): (value + 1) for index, value in enumerate(shuffled_areas)})

        # Music Randomization
        music_list_o = [1, 2, 3, 4, 9, 12]
        music_list_s = music_list_o.copy()
        if self.multiworld.MusicRandomizer[self.player]:
            self.multiworld.random.shuffle(music_list_s)

        self.music_map = dict(zip(music_list_o, music_list_s))

    def create_items(self):
        for i in range(20):
            trinket = self.create_item(f"Trinket {str(i + 1).zfill(2)}",
                                       i + 1 <= (self.multiworld.DoorCost[self.player] * 4))
            self.multiworld.itempool.append(trinket)


    def fill_slot_data(self):
        return {
            "MusicRando": self.music_map,
            "AreaRando": self.area_connections,
            "DoorCost": self.multiworld.DoorCost[self.player].value,
            "AreaCostRando": self.area_cost_map,
            "DeathLink": self.multiworld.death_link[self.player].value,
            "DeathLink_Amnesty": self.multiworld.DeathLinkAmnesty[self.player].value
        }

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return

        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[location.name]: item_table[location.item.name]
                                 for location in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apv6"
        with open(os.path.join(output_directory, filename), 'w') as file:
            json.dump(data, file)
