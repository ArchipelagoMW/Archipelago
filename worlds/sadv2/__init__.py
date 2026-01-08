import settings
import typing
import logging

from BaseClasses import ItemClassification, MultiWorld
from .Options import SADV2Options
from .Items import SADV2Item, character_table, zone_table, emerald_table, event_table, item_table, filler_table
from .Locations import SADV2Location, leaf_forest_locations, hot_crater_locations, music_plant_locations, \
                        ice_paradise_locations, sky_canyon_locations, techno_base_locations, egg_utopia_locations, \
                        xx_locations, event_locations, all_locations
from .Regions import SADV2Region, create_regions, create_region, connect, create_locations
from worlds.AutoWorld import World
from .Client import SonicAdvance2Client
from . import Names

class SADV2World(World):
    game = "Sonic Advance 2"
    options_dataclass = SADV2Options
    options: SADV2Options
    topology_present = True
    xx_req = 0
    starting_character = 0
    starting_zone = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: id for name, id in all_locations.items() if id is not None}

    item_name_groups = {
        "chaos emeralds": { "Red Chaos Emerald", "Blue Chaos Emerald", "Yellow Chaos Emerald",
                     "Green Chaos Emerald", "White Chaos Emerald", "Cyan Chaos Emerald", "Purple Chaos Emerald" },
        "zones": { "Leaf Forest", "Hot Crater", "Music Plant", "Ice Paradise", "Sky Canyon", "Techno Base", "Egg Utopia" }
    }

    def generate_early(self) -> None:
        self.xx_req = int(self.options.xx_coords_pool * (self.options.xx_coords / 100)) + 1

        self.starting_character = self.options.starting_character.value
        self.starting_zone = self.options.starting_zone.value

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Vanilla Rescued", self.player)

    def create_item(self, name: str) -> SADV2Item:
        item = item_table[name]
        classification = ItemClassification.filler

        if item.progression == 1:
            classification = ItemClassification.progression
        elif item.progression == 2:
            classification = ItemClassification.progression_skip_balancing

        return SADV2Item(name, classification, item.code, self.player)

    def create_items(self) -> None:
        itempool = []
        starting_zone = self.item_id_to_name[200 + self.starting_zone]
        self.multiworld.push_precollected(self.create_item(starting_zone))
        itempool.extend([self.create_item(name) for name in zone_table.keys() if name != starting_zone and
                                                                                name != Names.xx_unlock])
        itempool.extend(self.create_item(name) for name in emerald_table.keys())

        xx_count = 0
        while xx_count < self.options.xx_coords_pool:
            itempool.append(self.create_item(Names.xx_unlock))
            xx_count += 1

        starting_character = self.item_id_to_name[100 + self.starting_character]
        self.multiworld.push_precollected(self.create_item(starting_character))
        itempool.extend([self.create_item(name) for name in character_table.keys() if name != starting_character])

        num_locations = len(all_locations)
        filler_needed = num_locations - len(itempool)
        filler_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        itempool.extend(self.create_item(name) 
                        for name in self.random.choices(list(filler_table.keys()), weights = filler_weights,
                                                            k = filler_needed))
        
        self.multiworld.itempool += itempool

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player, self.xx_req)

    def stage_fill_hook(multiworld: MultiWorld, progitempool, usefulitempool, filleritempool, fill_locations):
        if multiworld.get_game_players("Sonic Advance 2"):
            progitempool.sort(
                key=lambda item: 1 if("XX" in item.name and item.game == "Sonic Advance 2") else 0
            )

    def fill_slot_data(self):
        return {
            "starting_zone": self.starting_zone,
            "starting_character": self.starting_character,
            "xx_coords": self.xx_req,
            "xx_total": self.options.xx_coords_pool.value
        }