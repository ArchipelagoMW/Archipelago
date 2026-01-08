import logging
from typing import Any, ClassVar, Dict, Optional

from BaseClasses import Item, MultiWorld, Tutorial
from worlds.AutoWorld import CollectionState, WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess, SuffixIdentifier, Type
from . import UniversalTracker
from .Items import create_item, create_itempool, get_filler_item_selection, item_table
from .Locations import get_level_locations, get_location_names, get_regions, get_total_locations, location_groups
from .Rac3Options import GAME_TITLE_FULL, RaC3Options
from .Regions import create_regions
from .Rules import set_rules

rac3_logger = logging.getLogger("Ratchet & Clank 3")
rac3_logger.setLevel(logging.DEBUG)


def run_client(_url: Optional[str] = None):
    from .Rac3Client import launch_client
    launch_subprocess(launch_client, name="Rac3Client")


components.append(
    Component("Ratchet & Clank 3 Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".aprac3"))
)


class RaC3Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ratchet and Clank 3: Up Your Arsenal for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Bread"]
    )]


class RaC3World(World):
    """
    Ratchet and Clank 3 is a third person action shooter.
    Blast your enemies with over the top weaponry and save the galaxy from total disaster.
    """

    game = GAME_TITLE_FULL
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    location_name_groups = location_groups
    preplaced_items: list[str] = []
    filler_items: list[str] = []
    # Config for Universal Tracker

    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]
    ut_can_gen_without_yaml = True
    disable_ut = False
    tracker_world: ClassVar = UniversalTracker.tracker_world

    for region in get_regions():
        location_name_groups[region] = set(get_level_locations(region))

    options_dataclass = RaC3Options
    options = RaC3Options
    web = RaC3Web()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def generate_early(self):
        rac3_logger.warning(
            "INCOMPLETE WORLD! Slot '%s' is using an unfinished alpha world that is not stable yet!",
            self.player_name)
        rac3_logger.warning("INCOMPLETE WORLD! Slot '%s' may require send_location/send_item for completion!",
                            self.player_name)
        self.preplaced_items = []

        # implement .yaml-less Universal Tracker support
        UniversalTracker.setup_options_from_slot_data(self)

        starting_weapons = Items.starting_weapons(self, self.options.starting_weapons.value)
        starting_planets = ["Infobot: Florana", "Infobot: Starship Phoenix"]

        create_regions(self)

        if len(starting_weapons) > 0:
            self.get_location("Veldin: First Ranger").place_locked_item(self.create_item(starting_weapons[0]))
            if len(starting_weapons) > 1:
                self.get_location("Veldin: Second Ranger").place_locked_item(self.create_item(starting_weapons[1]))
        self.get_location("Veldin: Save Veldin").place_locked_item(self.create_item(starting_planets[0]))
        self.get_location("Florana: Defeat Qwark").place_locked_item(self.create_item(starting_planets[1]))
        self.preplaced_items.extend(starting_weapons)
        self.preplaced_items.extend(starting_planets)

    def create_items(self):
        itempool = create_itempool(self)
        self.multiworld.itempool.extend(itempool)
        filler = [self.create_filler() for _ in
                  range(get_total_locations(self) - len(self.preplaced_items) - len(itempool) - 1)]
        self.multiworld.itempool.extend(filler)

    def get_filler_item_name(self) -> str:
        if not len(self.filler_items):
            self.filler_items = get_filler_item_selection(self)
        return self.random.choice(self.filler_items)

    def set_rules(self):
        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "options": {
                "start_inventory_from_pool": self.options.start_inventory_from_pool.value,
                "starting_weapons": self.options.starting_weapons.value,
                "bolt_and_xp_multiplier": self.options.bolt_and_xp_multiplier.value,
                "enable_progressive_weapons": self.options.enable_progressive_weapons.value,
                "extra_armor_upgrade": self.options.extra_armor_upgrade.value,
                "skill_points": self.options.skill_points.value,
                "trophies": self.options.trophies.value,
                "titanium_bolts": self.options.titanium_bolts.value,
                "nanotech_milestones": self.options.nanotech_milestones.value,
            },
            "TotalLocations": get_total_locations(self)
        }

        return slot_data

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)

    # For Universal Tracker integration
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    # def post_fill(self) -> None:
    #    from Utils import visualize_regions
    #    visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
    #                      regions_to_highlight=self.multiworld.get_all_state(False).reachable_regions[
    #                          self.player])
