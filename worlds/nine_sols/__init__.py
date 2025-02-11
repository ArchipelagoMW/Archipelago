from typing import Any, Dict

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import NineSolsItem, all_non_event_items_table, item_name_groups, create_item, create_items
from .locations_and_regions import all_non_event_locations_table, location_name_groups, create_regions
from .options import NineSolsGameOptions


class NineSolsWebWorld(WebWorld):
    theme = "ocean"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Nine Sols.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Ixrec"]
        )
    ]


class NineSolsWorld(World):
    game = "Nine Sols"
    web = NineSolsWebWorld()

    # TODO: alternate spawns, etc

    # this is how we tell the Universal Tracker we want to use re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    def generate_early(self) -> None:
        # implement Universal Tracker support
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Nine Sols" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Nine Sols"]
                    # TODO: alternate spawns, etc
            return

        # generate game-specific randomizations separate from AP items/locations
        # TODO: random jade costs, etc

    # members and methods implemented by locations_and_regions.py, locations.jsonc and connections.jsonc

    location_name_to_id = all_non_event_locations_table
    location_name_groups = location_name_groups

    def create_regions(self) -> None:
        create_regions(self)

    # members and methods implemented by items.py and items.jsonc

    item_name_to_id = all_non_event_items_table
    item_name_groups = item_name_groups

    def create_item(self, name: str) -> NineSolsItem:
        return create_item(self.player, name)

    def create_items(self) -> None:
        create_items(self)

    def get_filler_item_name(self) -> str:
        # Used in corner cases (e.g. plando, item_links, start_inventory_from_pool)
        # where even a well-behaved world may end up "missing" items.
        # Technically this "should" be a random choice among all filler/trap items
        # the world is configured to have, but it's not worth that much effort.
        return "Jin x50"

    # members and methods related to options.py

    options_dataclass = NineSolsGameOptions
    options: NineSolsGameOptions

    # miscellaneous smaller methods

    def set_rules(self) -> None:
        # here we only set the completion condition; all the location/region rules were set in create_regions()
        # currently there is only one goal
        goal_item = 'Victory - Eggnog'
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item, self.player)

    def fill_slot_data(self):
        slot_data = self.options.as_dict(
            "death_link", # a client/mod feature
        )
        # Archipelago does not yet have apworld versions (data_version is deprecated),
        # so we have to roll our own with slot_data for the time being
        slot_data["apworld_version"] = "0.1.0"
        return slot_data

