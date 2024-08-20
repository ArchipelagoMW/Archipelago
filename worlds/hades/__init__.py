from re import I
import string
import typing
import settings
from dataclasses import dataclass, fields

from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from .Items import event_item_pairs_weapon_mode, item_table, item_table_pacts, HadesItem, event_item_pairs, \
      create_pact_pool_amount, create_filler_pool_options, item_table_keepsake, item_table_weapons, \
        item_table_store, item_table_hidden_aspects, create_trap_pool, item_name_groups
from .Locations import setup_location_table_with_settings, give_all_locations_table, HadesLocation, location_table_fates_events, location_name_groups
from .Options import hades_option_presets, HadesOptions
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .Client import launch
    launch_subprocess(launch, "HadesClient")


components.append(Component("Hades Client", "HadesClient",
                  func=launch_client, component_type=Type.CLIENT))


class HadesSettings(settings.Group):
    class StyxScribePath(settings.UserFilePath):
        """Path to the StyxScribe install"""

    styx_scribe_path: StyxScribePath = StyxScribePath(
        "C:/Program Files/Steam/steamapps/common/Hades/StyxScribe.py")


class HadesWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Hades for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "Hades.md",
        "Hades/en",
        ["Naix"]
    )]
    options_presets = hades_option_presets


class HadesWorld(World):
    """
    Hades is a rogue-like dungeon crawler in which you defy the god of the dead as you hack and slash 
    your way out of the Underworld of Greek myth.
    """

    options: HadesOptions
    options_dataclass = HadesOptions
    game = "Hades"
    topology_present = False
    settings: typing.ClassVar[HadesSettings]
    web = HadesWeb()
    required_client_version = (0, 5, 0)

    polycosmos_version = "0.12"

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = give_all_locations_table()

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def create_items(self):
        local_location_table = setup_location_table_with_settings(self.options).copy()
        
        pool = []

        # Fill pact items
        item_pool_pacts = create_pact_pool_amount(self.options)

        # Fill pact items
        if (self.options.heat_system == "reverseheat"):
            for name, data in item_table_pacts.items():
                for amount in range(item_pool_pacts.get(name, 1)):
                    item = HadesItem(name, self.player)
                    pool.append(item)

        # Fill keepsake items
        if self.options.keepsakesanity:
            for name, data in item_table_keepsake.items():
                item = HadesItem(name, self.player)
                pool.append(item)

        # Fill weapons items
        if self.options.weaponsanity:
            for name, data in item_table_weapons.items():
                if (self.should_ignore_weapon(name)):
                    continue
                item = HadesItem(name, self.player)
                pool.append(item)

        # Fill store items
        if self.options.storesanity:
            for name, data in item_table_store.items():
                item = HadesItem(name, self.player)
                pool.append(item)

        if self.options.hidden_aspectsanity:
            for name, date in item_table_hidden_aspects.items():
                item = HadesItem(name, self.player)
                pool.append(item)

        # Pair up our event locations with our event items
        if self.options.location_system == "roomweaponbased":
            for event, item in event_item_pairs_weapon_mode.items():
                event_item = HadesItem(item, self.player)
                self.multiworld.get_location(
                    event, self.player).place_locked_item(event_item)
        else:
            for event, item in event_item_pairs.items():
                event_item = HadesItem(item, self.player)
                self.multiworld.get_location(
                    event, self.player).place_locked_item(event_item)
                

        # create the pack of filler options
        filler_options = create_filler_pool_options(self.options)

        # Fill filler items uniformly. Maybe later we can tweak this.
        index = 0
        total_fillers_needed = len(local_location_table)-len(pool)-len(location_table_fates_events)
        
        if (self.options.location_system.value == "roomweaponbased"):
            #Substract the 4 bosses for each of the 6 weapons = 24
            total_fillers_needed = total_fillers_needed - 24
        else:
            #Substract the 4 bosses
            total_fillers_needed = total_fillers_needed - 4

        helper_percentage = self.options.filler_helper_percentage
        helper_fillers_needed = int(total_fillers_needed*helper_percentage/100)

        trap_percentage = min(self.options.filler_trap_percentage, 100-helper_percentage)
        trap_fillers_needed = int(total_fillers_needed*trap_percentage/100)
        trap_pool = create_trap_pool()

        fillers_needed = total_fillers_needed-trap_fillers_needed-helper_fillers_needed
        for amount in range(0, fillers_needed):
            item_name = filler_options[index]
            item = HadesItem(item_name, self.player)
            pool.append(item)
            index = (index+1) % len(filler_options)

        #Fill helpers
        health_helpers_needed = int(helper_fillers_needed*self.options.max_health_helper_percentage/100)
        money_helpers_needed = int(helper_fillers_needed*self.options.initial_money_helper_percentage/100)
        boon_helpers_needed = helper_fillers_needed-health_helpers_needed-money_helpers_needed

        for amount in range(0, health_helpers_needed):
            item = HadesItem("MaxHealthHelper", self.player)
            pool.append(item)

        for amount in range(0, min(money_helpers_needed, helper_fillers_needed-health_helpers_needed)):
            item = HadesItem("InitialMoneyHelper", self.player)
            pool.append(item)

        helpers_available = max(boon_helpers_needed,0)
        for amount in range(0, max(boon_helpers_needed,0)):
            item = HadesItem("BoonBoostHelper", self.player)
            pool.append(item)

        index = 0

        #Fill traps
        for amount in range(0,trap_fillers_needed):
            item_name = trap_pool[index]
            item = HadesItem(item_name, self.player)
            pool.append(item)
            index = (index+1) % len(trap_pool)
            
        self.multiworld.itempool += pool

    def should_ignore_weapon(self, name):
        if (self.options.initial_weapon == "Sword" and name == "SwordWeaponUnlockItem"):
            return True
        if (self.options.initial_weapon == "Bow" and name == "BowWeaponUnlockItem"):
            return True
        if (self.options.initial_weapon == "Spear" and name == "SpearWeaponUnlockItem"):
            return True
        if (self.options.initial_weapon == "Shield" and name == "ShieldWeaponUnlockItem"):
            return True
        if (self.options.initial_weapon == "Fist" and name == "FistWeaponUnlockItem"):
            return True
        if (self.options.initial_weapon == "Gun" and name == "GunWeaponUnlockItem"):
            return True
        return False

    def set_rules(self):
        local_location_table = setup_location_table_with_settings(self.options).copy()
        set_rules(self.multiworld, self.player, self.calculate_number_of_pact_items(
        ), local_location_table, self.options)

    def calculate_number_of_pact_items(self):
        # Go thorugh every option and count what is the chosen level
        total = int(self.options.hard_labor_pact_amount)
        total += int(self.options.lasting_consequences_pact_amount)
        total += int(self.options.convenience_fee_pact_amount)
        total += int(self.options.jury_summons_pact_amount)
        total += int(self.options.extreme_measures_pact_amount)
        total += int(self.options.calisthenics_program_pact_amount)
        total += int(self.options.benefits_package_pact_amount)
        total += int(self.options.middle_management_pact_amount)
        total += int(self.options.underworld_customs_pact_amount)
        total += int(self.options.forced_overtime_pact_amount)
        total += int(self.options.heightened_security_pact_amount)
        total += int(self.options.routine_inspection_pact_amount)
        total += int(self.options.damage_control_pact_amount)
        total += int(self.options.approval_process_pact_amount)
        total += int(self.options.tight_deadline_pact_amount)
        total += int(self.options.personal_liability_pact_amount)
        return total

    def create_item(self, name: str) -> Item:
        return HadesItem(name, self.player)

    def create_regions(self):
        local_location_table = setup_location_table_with_settings(self.options).copy()
        create_regions(self, local_location_table)

    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict("initial_weapon", "location_system", "score_rewards_amount", "keepsakesanity",
                                         "weaponsanity", "hidden_aspectsanity", "storesanity", "fatesanity",
                                         "hades_defeats_needed", "weapons_clears_needed", "keepsakes_needed", 
                                         "fates_needed", "heat_system", "hard_labor_pact_amount",
                                         "lasting_consequences_pact_amount", "convenience_fee_pact_amount",
                                         "jury_summons_pact_amount", "extreme_measures_pact_amount",
                                         "calisthenics_program_pact_amount", "benefits_package_pact_amount",
                                         "middle_management_pact_amount", "underworld_customs_pact_amount",
                                         "forced_overtime_pact_amount", "heightened_security_pact_amount",
                                         "routine_inspection_pact_amount", "damage_control_pact_amount",
                                         "approval_process_pact_amount", "tight_deadline_pact_amount",
                                         "personal_liability_pact_amount", "darkness_pack_value", "keys_pack_value",
                                         "gemstones_pack_value", "diamonds_pack_value", "titan_blood_pack_value",
                                         "nectar_pack_value", "ambrosia_pack_value", "filler_helper_percentage",
                                         "max_health_helper_percentage", "initial_money_helper_percentage",
                                         "filler_trap_percentage", "reverse_order_em", "ignore_greece_deaths",
                                         "store_give_hints", "automatic_rooms_finish_on_hades_defeat", "death_link")
        slot_data['seed'] = "".join(self.random.choice(string.ascii_letters) for i in range(16))
        slot_data["version_check"] = self.polycosmos_version
        return slot_data

    def get_filler_item_name(self) -> str:
        return "Darkness"


def create_region(world: MultiWorld, player: int, location_database, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = location_database.get(location, 0)
            location = HadesLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
