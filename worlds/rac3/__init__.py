from logging import DEBUG, getLogger
from typing import Any, ClassVar, Optional

from BaseClasses import CollectionState, Item, MultiWorld, Tutorial
from constants.data.Rac3ItemData import item_groups, RAC3_ITEM_DATA_TABLE
from constants.Rac3Items import RAC3ITEM
from constants.Rac3Options import RAC3OPTION
from Items import create_item, create_itempool, get_filler_item_selection, starting_weapons
from Locations import get_level_locations, get_location_names, get_regions, get_total_locations, location_groups
from Rac3Options import RaC3Options
from Regions import create_regions
from Rules import set_rules
from UniversalTracker import setup_options_from_slot_data, tracker_world
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess, SuffixIdentifier, Type


def run_client(_url: Optional[str] = None):
    from client.Rac3Client import launch_client
    launch_subprocess(launch_client, name=f"{RAC3OPTION.GAME_TITLE}Client")


components.append(Component(f"{RAC3OPTION.GAME_TITLE_FULL} Client", func=run_client, component_type=Type.CLIENT,
                            file_identifier=SuffixIdentifier(".aprac3")))


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


rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


class RaC3World(World):
    """
    Ratchet and Clank 3 is a third person action shooter.
    Blast your enemies with over the top weaponry and save the galaxy from total disaster.
    """

    game = RAC3OPTION.GAME_TITLE_FULL
    item_name_to_id = {name: data.AP_CODE for name, data in RAC3_ITEM_DATA_TABLE.items()}
    location_name_to_id = get_location_names()
    location_name_groups = location_groups
    item_name_groups = item_groups
    preplaced_items: list[str] = []
    filler_items: list[str] = []
    # Config for Universal Tracker

    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]
    ut_can_gen_without_yaml = True
    disable_ut = False
    tracker_world: ClassVar = tracker_world

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
        self.preplaced_items = [RAC3ITEM.VELDIN, RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK]
        # implement .yaml-less Universal Tracker support
        setup_options_from_slot_data(self)
        create_regions(self)

        for item in self.preplaced_items:
            self.push_precollected(self.create_item(item))
        starting_weapon_list = starting_weapons(self, self.options.starting_weapons.value)
        starting_planets = [RAC3ITEM.FLORANA, RAC3ITEM.STARSHIP_PHOENIX]

        if len(starting_weapon_list) > 0:
            self.get_location("Veldin: First Ranger").place_locked_item(self.create_item(starting_weapon_list[0]))
            if len(starting_weapon_list) > 1:
                self.get_location("Veldin: Second Ranger").place_locked_item(self.create_item(starting_weapon_list[1]))
        self.get_location("Veldin: Save Veldin").place_locked_item(self.create_item(starting_planets[0]))
        self.get_location("Florana: Defeat Qwark").place_locked_item(self.create_item(starting_planets[1]))
        self.preplaced_items.extend(starting_weapon_list)
        self.preplaced_items.extend(starting_planets)

    def create_items(self):
        itempool = create_itempool(self)
        self.multiworld.itempool.extend(itempool)
        filler = [self.create_filler() for _ in
                  range(get_total_locations(self) - len(self.preplaced_items) - len(itempool) + 2)]
        self.multiworld.itempool.extend(filler)

    def get_filler_item_name(self) -> str:
        if not len(self.filler_items):
            self.filler_items = get_filler_item_selection(self)
        return self.random.choice(self.filler_items)

    def set_rules(self):
        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> dict[str, object]:
        slot_data: dict[str, object] = {
            RAC3OPTION.START_INVENTORY_FROM_POOL: self.options.start_inventory_from_pool.value,
            RAC3OPTION.STARTING_WEAPONS: self.options.starting_weapons.value,
            RAC3OPTION.BOLT_AND_XP_MULTIPLIER: self.options.bolt_and_xp_multiplier.value,
            RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS: self.options.enable_progressive_weapons.value,
            RAC3OPTION.EXTRA_ARMOR_UPGRADE: self.options.extra_armor_upgrade.value,
            RAC3OPTION.SKILL_POINTS: self.options.skill_points.value,
            RAC3OPTION.TROPHIES: self.options.trophies.value,
            RAC3OPTION.TITANIUM_BOLTS: self.options.titanium_bolts.value,
            RAC3OPTION.NANOTECH_MILESTONES: self.options.nanotech_milestones.value,
            RAC3OPTION.EXCLUDE: self.options.exclude_locations.value,
            RAC3OPTION.SHIP_NOSE: self.options.ship_nose.value,
            RAC3OPTION.SHIP_WINGS: self.options.ship_wings.value,
            RAC3OPTION.SHIP_SKIN: self.options.ship_skin.value,
            RAC3OPTION.SKIN: self.options.skin.value,
            RAC3OPTION.ENABLE_TRAPS: self.options.traps_enabled.value,
            RAC3OPTION.TRAP_WEIGHT: self.options.trap_weight.value,
            RAC3OPTION.TOTAL_LOCATIONS: get_total_locations(self)
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
