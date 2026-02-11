"""This module contains the World class for Ratchet and Clank 3"""
from logging import DEBUG, getLogger
from typing import Any, ClassVar, TYPE_CHECKING

from BaseClasses import CollectionState, Item, MultiWorld
from Options import OptionError
from worlds.AutoWorld import World
from worlds.rac3.constants.data.item import item_groups, RAC3_ITEM_DATA_TABLE
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.items import (create_item, create_itempool, get_filler_selection, process_start_inventory,
                               starting_planets, starting_weapons)
from worlds.rac3.locations import (get_level_locations, get_location_names, get_regions, get_total_locations,
                                   location_groups)
from worlds.rac3.rac3options import RaC3Options
from worlds.rac3.regions import create_regions
from worlds.rac3.rules import set_rules
from worlds.rac3.universal_tracker import setup_options_from_slot_data, tracker_world
from worlds.rac3.web_world import RaC3Web


rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)

class RaC3World(World):
    """
    Ratchet & Clank 3 is a third person action shooter.
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
    ut_can_gen_without_yaml: bool = True
    disable_ut: bool = False
    tracker_world: ClassVar = tracker_world

    for region in get_regions():
        location_name_groups[region] = set(get_level_locations(region))

    options_dataclass = RaC3Options
    web = RaC3Web()
    if TYPE_CHECKING:
        options = RaC3Options

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def generate_early(self):
        # count number of . in the version number to determine if dev build
        version_dots = RAC3OPTION.VERSION_NUMBER.count(".")
        if version_dots >= 3:
            rac3_logger.warning("\nYou are using a development build of the RaC3 Archipelago Randomizer!\n"
                                "There may be bugs present that have not been tested fully.\n"
                                "These builds are meant for testing and bug reporting purposes "
                                "and should not be used for normal play!\n")
        # implement .yaml-less Universal Tracker support
        setup_options_from_slot_data(self)
        create_regions(self)

        starting_weapon_list, starting_planet_list = self.generate_starting_items()
        self.handle_option_errors(starting_planet_list, starting_weapon_list)
        self.place_starting_items(starting_planet_list, starting_weapon_list)

    def place_starting_items(self, starting_planet_list: list[str], starting_weapon_list: list[str]):
        """Take the list of starting planets and starting weapons and place them on locations or as precollected"""
        if len(starting_weapon_list) > 0:
            self.get_location(RAC3LOCATION.VELDIN_FIRST_RANGER).place_locked_item(
                self.create_item(starting_weapon_list[0]))
            if len(starting_weapon_list) > 1:
                self.get_location(RAC3LOCATION.VELDIN_SECOND_RANGER).place_locked_item(
                    self.create_item(starting_weapon_list[1]))
        if self.options.intro_skip.value:
            if len(starting_planet_list) == 1:  # either [Phoenix] or [Other]
                if starting_planet_list[0] == RAC3ITEM.STARSHIP_PHOENIX:
                    self.preplaced_items.append(starting_planet_list[0])
                    self.push_precollected(self.create_item(starting_planet_list[0]))
                else:
                    self.get_location(RAC3LOCATION.VELDIN_SAVE_VELDIN).place_locked_item(
                        self.create_item(starting_planet_list[0]))
            elif len(starting_planet_list) > 1:  # always [Phoenix, Other]
                self.preplaced_items.append(starting_planet_list[0])
                self.push_precollected(self.create_item(starting_planet_list[0]))
                self.get_location(RAC3LOCATION.VELDIN_SAVE_VELDIN).place_locked_item(
                    self.create_item(starting_planet_list[1]))
        else:
            if len(starting_planet_list) == 1 and starting_planet_list[0] == RAC3ITEM.STARSHIP_PHOENIX:  # [Phoenix]
                self.get_location(RAC3LOCATION.FLORANA_DEFEAT_QWARK).place_locked_item(
                    self.create_item(starting_planet_list[0]))
            elif len(starting_planet_list) > 0:  # First entry not Phoenix
                self.get_location(RAC3LOCATION.VELDIN_SAVE_VELDIN).place_locked_item(
                    self.create_item(starting_planet_list[0]))
                if len(starting_planet_list) > 1:  # size == 2
                    self.get_location(RAC3LOCATION.FLORANA_DEFEAT_QWARK).place_locked_item(
                        self.create_item(starting_planet_list[1]))
        self.preplaced_items.extend(starting_weapon_list)
        self.preplaced_items.extend(starting_planet_list)

    def handle_option_errors(self, starting_planet_list: list[str], starting_weapon_list: list[str]):
        """Check for option combinations that will never result in successful seed generation and warn the player"""
        if (not self.options.intro_skip.value
                and self.options.clank_options.value
                and not self.options.titanium_bolts.value
                and not self.options.weapon_vendors.value
                and len(starting_weapon_list) > 1
                and starting_planet_list
                and self.multiworld.players == 1):
            raise OptionError("Options selected do not allow Ratchet to collect a Clank Pack and advance past Florana")

    def generate_starting_items(self):
        """Process player options to generate a list of early placed items, ensuring successful seed generation"""
        self.preplaced_items = [RAC3ITEM.VELDIN, RAC3ITEM.THIRD_PERSON, RAC3ITEM.FIRST_PERSON, RAC3ITEM.LOCK_STRAFE]
        if self.options.clank_options.value == self.options.clank_options.option_start_with:
            self.preplaced_items += [RAC3ITEM.CLANK, RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK]
        for item in self.preplaced_items:
            self.push_precollected(self.create_item(item))
        self.preplaced_items.extend(process_start_inventory(self))
        return starting_weapons(self), starting_planets(self)

    def create_items(self):
        itempool = create_itempool(self)
        self.multiworld.itempool.extend(itempool)
        location_count = len(self.multiworld.get_unfilled_locations(self.player))
        item_count = len(itempool)
        excluded_count = self.get_excluded_count()
        if excluded_count > location_count - item_count:
            raise OptionError("Too many locations have been excluded, not enough locations remain to place all items.")
        if location_count - item_count >= 0:
            filler = [self.create_filler() for _ in range(location_count - item_count)]
            self.multiworld.itempool.extend(filler)
        else:
            self.handle_not_enough_locations(item_count - location_count)

    def get_excluded_count(self) -> int:
        """Get the number of unique excluded locations for this player"""
        excluded_options = self.options.exclude_locations.value
        excluded_locations = set()
        for option in excluded_options:
            if option in location_groups:
                excluded_locations.update(location_groups[option])
            else:
                excluded_locations.add(option)
        return len(excluded_locations)

    def handle_not_enough_locations(self, count):
        """Check the available location and items counts, raise OptionErrors to warn the player of too few locations"""
        excluded_count = self.get_excluded_count()
        option_list: list[str] = []
        if self.options.skill_points.value == 0:
            option_list.append(RAC3OPTION.SKILL_POINTS)
        if self.options.trophies.value == 0:
            option_list.append(RAC3OPTION.TROPHIES)
        if self.options.titanium_bolts.value == 0:
            option_list.append(RAC3OPTION.TITANIUM_BOLTS)
        if self.options.nanotech_milestones.value < 3:
            option_list.append(RAC3OPTION.NANOTECH_MILESTONES)
        if self.options.rangers.value == 0:
            option_list.append(RAC3OPTION.RANGERS)
        if self.options.arena.value == 0:
            option_list.append(RAC3OPTION.ARENA)
        if self.options.vidcomics.value == 0:
            option_list.append(RAC3OPTION.VIDCOMICS)
        if self.options.vr_challenges.value == 0:
            option_list.append(RAC3OPTION.VR_CHALLENGES)
        if self.options.sewer_crystals.value < 3:
            option_list.append(RAC3OPTION.SEWER_CRYSTALS)
        if self.options.sewer_limitation.value < 20:
            option_list.append(RAC3OPTION.SEWER_LIMITATION)
        if self.options.nanotech_limitation.value < 60:
            option_list.append(RAC3OPTION.NANOTECH_LIMITATION)
        if excluded_count > 30:
            option_list.append(RAC3OPTION.EXCLUDE)
        if not option_list:
            option_list: str = "dunno"  # ¯\_(''/)_/¯
        message = f"Not enough location options enabled! {count} items have nowhere to be placed."
        if count >= 50:
            message += (f"\nThis large of a difference requires Progressive Weapons to be disabled, Additional Sewer "
                        f"Crystal Trade locations, or Additional Nanotech level locations.")
        if count <= 10 and sum(self.options.start_inventory_from_pool.value.values()) <= 10:
            message += f"Consider adding some items to your starting_items_from_pool or "
        else:
            message += f"Consider "
        message += f"adjusting some of the following options: {option_list}"
        raise OptionError(message)

    def get_filler_item_name(self) -> str:
        if not len(self.filler_items):
            self.filler_items = get_filler_selection(self)
        return self.random.choice(self.filler_items)

    def set_rules(self):
        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data: dict[str, Any] = {
            RAC3OPTION.VERSION: RAC3OPTION.VERSION_NUMBER,
            RAC3OPTION.START_INVENTORY_FROM_POOL: self.options.start_inventory_from_pool.value,
            RAC3OPTION.STARTING_WEAPONS: self.options.starting_weapons.value,
            RAC3OPTION.BOLT_AND_XP_MULTIPLIER: self.options.bolt_and_xp_multiplier.value,
            RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS: self.options.enable_progressive_weapons.value,
            RAC3OPTION.ARMOR_UPGRADE: self.options.armor_upgrade.value,
            RAC3OPTION.SKILL_POINTS: self.options.skill_points.value,
            RAC3OPTION.TROPHIES: self.options.trophies.value,
            RAC3OPTION.TITANIUM_BOLTS: self.options.titanium_bolts.value,
            RAC3OPTION.NANOTECH_MILESTONES: self.options.nanotech_milestones.value,
            RAC3OPTION.EXCLUDE: self.options.exclude_locations.value,
            RAC3OPTION.DEATHLINK: self.options.deathlink.value,
            RAC3OPTION.SHIP_NOSE: self.options.ship_nose.value,
            RAC3OPTION.SHIP_WINGS: self.options.ship_wings.value,
            RAC3OPTION.SHIP_SKIN: self.options.ship_skin.value,
            RAC3OPTION.SKIN: self.options.skin.value,
            RAC3OPTION.ENABLE_TRAPS: self.options.traps_enabled.value,
            RAC3OPTION.TRAP_WEIGHT: self.options.trap_weight.value,
            RAC3OPTION.RANGERS: self.options.rangers.value,
            RAC3OPTION.ARENA: self.options.arena.value,
            RAC3OPTION.VIDCOMICS: self.options.vidcomics.value,
            RAC3OPTION.VR_CHALLENGES: self.options.vr_challenges.value,
            RAC3OPTION.SEWER_CRYSTALS: self.options.sewer_crystals.value,
            RAC3OPTION.SEWER_LIMITATION: self.options.sewer_limitation.value,
            RAC3OPTION.NANOTECH_LIMITATION: self.options.nanotech_limitation.value,
            RAC3OPTION.WEAPON_VENDORS: self.options.weapon_vendors.value,
            RAC3OPTION.FILLER_WEIGHT: self.options.filler_weight.value,
            RAC3OPTION.ONE_HP_CHALLENGE: self.options.one_hp_challenge.value,
            RAC3OPTION.INTRO_SKIP: self.options.intro_skip.value,
            RAC3OPTION.HOLOSTAR_SKIP: self.options.holostar_skip.value,
            RAC3OPTION.CLANK_OPTIONS: self.options.clank_options.value,
            RAC3OPTION.TOTAL_LOCATIONS: get_total_locations(self),
        }

        return slot_data

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)

    # For Universal Tracker integration
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Trigger a regen in UT"""
        return slot_data

    # def post_fill(self) -> None:
    #    from Utils import visualize_regions
    #    visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
    #                      regions_to_highlight=self.multiworld.get_all_state(False).reachable_regions[
    #                          self.player])
