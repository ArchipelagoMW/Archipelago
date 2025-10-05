import orjson
import pkgutil
from typing import Any, ClassVar

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import NineSolsItem, all_non_event_items_table, item_name_groups, create_item, create_items
from .locations_and_regions import all_non_event_locations_table, location_name_groups, create_regions
from .options import NineSolsGameOptions
from .ut_map_page.map_page_index import map_page_index
from .jade_costs import generate_random_jade_costs


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

    jade_costs = 'vanilla'
    # TODO: alternate spawns, etc

    # this is how we tell the Universal Tracker we want to use re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data

    # and this is how we tell Universal Tracker we don't need the yaml
    ut_can_gen_without_yaml = True

    tracker_world: ClassVar = {
        "map_page_folder": "ut_map_page",
        "map_page_maps": "maps.json",
        "map_page_locations": "locations.json",
        "map_page_setting_key": "{player}_{team}_nine_sols_area",
        "map_page_index": map_page_index
    }

    def generate_early(self) -> None:
        # implement .yaml-less Universal Tracker support
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Nine Sols" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Nine Sols"]
                    self.options.seals_for_eigong.value = slot_data['seals_for_eigong']
                    self.options.seals_for_prison.value = slot_data['seals_for_prison']
                    self.options.seals_for_ethereal.value = slot_data['seals_for_ethereal']
                    self.options.skip_soulscape_platforming.value = slot_data['skip_soulscape_platforming']
                    # TODO: alternate spawns, etc
            return

        # generate game-specific randomizations separate from AP items/locations
        self.jade_costs = generate_random_jade_costs(self.random, self.options) \
            if self.options.randomize_jade_costs else "vanilla"

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
            'skip_soulscape_platforming',  # implemented by client/mod code, and affects logic/trackers
            'seals_for_eigong',
            'seals_for_prison',
            'seals_for_ethereal',
        )
        # more client/mod features, these are only in the apworld because we want them fixed per-slot/at gen time
        slot_data["jade_costs"] = self.jade_costs
        # APWorld versions are not (yet?) exposed by AP servers, so the client/mod needs us to put it in slot_data
        slot_data["apworld_version"] = self.world_version
        return slot_data

