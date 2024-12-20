loonyland_base_id: int = 2876900

from BaseClasses import Region, Tutorial, ItemClassification, Location
from worlds.AutoWorld import WebWorld, World
from .Items import LoonylandItem
from .Locations import LoonylandLocation, LL_Location
from .Options import LoonylandOptions
from .Entrances import LoonylandEntrance
from .Data.game_data import *



class LoonylandWebWorld(WebWorld):
    theme = "dirt"

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
    location_name_to_id = {name: data.id + loonyland_base_id for name, data in loonyland_location_table.items()}
    item_name_to_id = {name: data.id for name, data in loony_item_table.items()}

    def create_item(self, name: str) -> LoonylandItem:
        return LoonylandItem(name, loony_item_table[name].classification, loony_item_table[name].id, self.player)

    def create_items(self) -> None:
        item_pool: List[LoonylandItem] = []
        for name, item in loony_item_table.items():
            if item.id and item.can_create(self.multiworld, self.player):
                for i in range(item.frequency):
                    item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_event(self, event: str) -> LoonylandItem:
        return LoonylandItem(event, ItemClassification.progression, None, self.player)

    def create_regions(self) -> None:
        for region_name in loonyland_region_table:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for loc_name, loc_data in loonyland_location_table.items():
            if not loc_data.can_create(self.multiworld, self.player):
                continue
            region = self.multiworld.get_region(loc_data.region, self.player)
            new_loc = LoonylandLocation(self.player, loc_name, loc_data.id, region)
            region.locations.append(new_loc)

    def get_filler_item_name(self) -> str:
        return "A Cool Filler Item (No Satisfaction Guaranteed)"

    def set_rules(self):
        # Completion condition.
        # self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        final_loc = self.get_location("Q: Save Halloween Hill")
        final_loc.address = None
        final_loc.place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        #location rules
        set_rules(self.multiworld, self, self.player)
        #entrance rules
        set_entrance_rules(self.multiworld, self, self.player)

    def fill_slot_data(self):
        return {
            "DeathLink": self.options.death_link.value
        }