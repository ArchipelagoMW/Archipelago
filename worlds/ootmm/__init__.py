from typing import List

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import OoTMMItem, item_data_table, item_table
from .locations import OoTMMLocation, OoTMMLocationData, location_data_table, location_table, locked_locations
from .options import ootmm_options
from .Regions import region_data_table
from .Rules import get_button_rule
import json


class OoTMMWebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing OoTMM.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Fletch & Iryoku"]
    )

    setup_de = Tutorial(
        tutorial_name="Anleitung zum Anfangen",
        description="Eine Anleitung um OoTMM zu spielen.",
        language="Deutsch",
        file_name="guide_de.md",
        link="guide/de",
        authors=["Held_der_Zeit"]
    )
    
    tutorials = [setup_en, setup_de]


class OoTMMWorld(World):
    """The greatest game of all time."""

    game = "Ocarina of Time & Majora's Mask"
    data_version = 3
    web = OoTMMWebWorld()
    option_definitions = ootmm_options
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> OoTMMItem:
        return OoTMMItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[OoTMMItem] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self.multiworld, self.player):
                for i in range (item.count): 
                    item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.multiworld, self.player)
            }, OoTMMLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.multiworld, self.player):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

        # Set priority location for the Big Red Button!
        # self.multiworld.priority_locations[self.player].value.add("The Big Red Button")
    
    def generate_output(self, output_directory):
        zetable = []
        for  location in self.multiworld.get_locations(self.player):
            assert(isinstance(location, OoTMMLocation))
            key = location.name
            data = location_data_table[key]
            zetable.append({"Location": data.name, "Game": data.game, "Id": data.id, "Item": location.item.name,})
            pass
        with open (output_directory + "/output.json","w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(zetable))
        
        # path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.json")

    # def get_filler_item_name(self) -> str:
    #     return "A Cool Filler Item (No Satisfaction Guaranteed)"

    # def set_rules(self) -> None:
    #     button_rule = get_button_rule(self.multiworld, self.player)
    #     self.multiworld.get_location("The Big Red Button", self.player).access_rule = button_rule
    #     self.multiworld.get_location("In the Player's Mind", self.player).access_rule = button_rule

    #     # Do not allow button activations on buttons.
    #     self.multiworld.get_location("The Big Red Button", self.player).item_rule =\
    #         lambda item: item.name != "Button Activation"

    #     # Completion condition.
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("The Urge to Push", self.player)

    # def fill_slot_data(self):
    #     return {
    #         "color": getattr(self.multiworld, "color")[self.player].current_key
    #     }
