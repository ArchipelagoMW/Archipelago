from typing import List, Dict, Any

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import LoonylandItem, item_frequencies, loony_item_table
from .Locations import LoonylandLocation, LoonylandLocationData, loonyland_location_table #, locked_locations
from .Options import LoonylandOptions
from .Regions import loonyland_region_table
from .Entrances import loonyland_entrance_table, LoonylandEntrance
from .Rules import set_rules


class LoonylandWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Loonyland.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["AutomaticFrenzy"]
    )

    tutorials = [setup_en]

class LoonylandWorld(World):
    """The greatest game of all time."""

    game = "Loonyland"
    web = LoonylandWebWorld()
    options: LoonylandOptions
    options_dataclass = LoonylandOptions
    location_name_to_id = {name: data.id for name, data in loonyland_location_table.items()}
    item_name_to_id = {name: data.id for name, data in loony_item_table.items()}

    def create_item(self, name: str) -> LoonylandItem:
        return LoonylandItem(name, loony_item_table[name].classification, loony_item_table[name].id, self.player)

    def create_items(self) -> None:
        item_pool: List[LoonylandItem] = []
        for name, item in loony_item_table.items():
            if item.id: #and item.can_create(self):
                for i in range(item_frequencies.get(name, 1)):
                    item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in loonyland_region_table:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        #connect regions

        # Create locations.
        for region_name in loonyland_region_table:
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.id for location_name, location_data in loonyland_location_table.items()
                if location_data.region == region_name # and location_data.can_create(self)
            }, LoonylandLocation)
            region.add_exits()


        # Place locked locations.
        #for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
        #    if not location_data.can_create(self):
        #        continue

       #    locked_item = self.create_item(location_data_table[location_name].locked_item)
        #    self.get_location(location_name).place_locked_item(locked_item)

        # Set priority location for the Big Red Button!
        #self.options.priority_locations.value.add("The Big Red Button")

    def get_filler_item_name(self) -> str:
        return "A Cool Filler Item (No Satisfaction Guaranteed)"

    def set_rules(self):
        set_rules(self.multiworld, self, self.player)

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("The Evilizer - Save Halloween Hill", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {

            "sampledata": "plerp"
        }