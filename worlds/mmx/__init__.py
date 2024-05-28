import dataclasses
import os
import typing
import math
import settings
import hashlib
import threading
import pkgutil

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import MMXItem, ItemData, item_table, junk_table, item_groups
from .Locations import MMXLocation, setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName, EventName
from .Options import MMXOptions, mmx_option_groups
from .Client import MMXSNIClient
from .Levels import location_id_to_level_id
from .Weaknesses import handle_weaknesses, weapon_id
from .Rom import patch_rom, MMXProcedurePatch, HASH_US, HASH_LEGACY

class MMXSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Mega Man X US ROM"""
        description = "Mega Man X (USA) ROM File"
        copy_to = "Mega Man X (USA).sfc"
        md5s = [HASH_US, HASH_LEGACY]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMXWeb(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Mega Man X with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )

    tutorials = [setup_en]

    #option_groups = mmx_option_groups


class MMXWorld(World):
    """
    Mega Man X WIP
    """
    game = "Mega Man X"
    web = MMXWeb()

    settings: typing.ClassVar[MMXSettings]
    
    options_dataclass = MMXOptions
    options: MMXOptions
    
    required_client_version = (0, 4, 6)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups
    location_name_groups = location_groups
    hint_blacklist = {
        LocationName.armored_armadillo_clear,
        LocationName.chill_penguin_clear,
        LocationName.boomer_kuwanger_clear,
        LocationName.sting_chameleon_clear,
        LocationName.storm_eagle_clear,
        LocationName.flame_mammoth_clear,
        LocationName.spark_mandrill_clear,
        LocationName.launch_octopus_clear,
        LocationName.intro_completed,
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        location_table = setup_locations(self)
        create_regions(self.multiworld, self.player, self, location_table)

        itempool: typing.List[MMXItem] = []
        
        connect_regions(self)
        
        total_required_locations = 47
        if self.options.pickupsanity:
            total_required_locations += 26

        # Add levels into the pool
        start_inventory = self.options.start_inventory.value.copy()
        stage_list = [
            ItemName.stage_armored_armadillo,
            ItemName.stage_boomer_kuwanger,
            ItemName.stage_chill_penguin,
            ItemName.stage_flame_mammoth,
            ItemName.stage_launch_octopus,
            ItemName.stage_spark_mandrill,
            ItemName.stage_sting_chameleon,
            ItemName.stage_storm_eagle,
        ]
        stage_selected = self.random.randint(0, 7)
        if any(stage in self.options.start_inventory_from_pool for stage in stage_list) or \
           any(stage in start_inventory for stage in stage_list):
            total_required_locations += 1
            for i in range(len(stage_list)):
                if stage_list[i] not in start_inventory:
                    itempool += [self.create_item(stage_list[i])]
        else:
            for i in range(len(stage_list)):
                if i == stage_selected:
                    self.multiworld.get_location(LocationName.intro_completed, self.player).place_locked_item(self.create_item(stage_list[i]))
                else:
                    itempool += [self.create_item(stage_list[i])]

        if len(self.options.sigma_open.value) == 0:
            itempool += [self.create_item(ItemName.stage_sigma_fortress)]

        # Add weapons into the pool
        itempool += [self.create_item(ItemName.electric_spark)]
        itempool += [self.create_item(ItemName.homing_torpedo)]
        itempool += [self.create_item(ItemName.storm_tornado)]
        itempool += [self.create_item(ItemName.shotgun_ice)]
        itempool += [self.create_item(ItemName.rolling_shield)]
        itempool += [self.create_item(ItemName.chameleon_sting)]
        itempool += [self.create_item(ItemName.fire_wave)]
        itempool += [self.create_item(ItemName.boomerang_cutter)]

        if self.options.hadouken_in_pool:
            itempool += [self.create_item(ItemName.hadouken, ItemClassification.useful)]

        # Add upgrades into the pool
        sigma_open = self.options.sigma_open.value
        if "Armor Upgrades" in sigma_open and self.options.sigma_upgrade_count.value > 0:
            itempool += [self.create_item(ItemName.body)]
        else:
            itempool += [self.create_item(ItemName.body, ItemClassification.useful)]
        itempool += [self.create_item(ItemName.arms)]
        if self.options.jammed_buster.value:
            itempool += [self.create_item(ItemName.arms)]
        itempool += [self.create_item(ItemName.helmet)]
        itempool += [self.create_item(ItemName.legs)]

        # Add heart tanks into the pool
        if "Heart Tanks" in sigma_open and self.options.sigma_heart_tank_count.value > 0:
            i = self.options.sigma_heart_tank_count.value
            itempool += [self.create_item(ItemName.heart_tank) for _ in range(i)]
            if i != 8:
                itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8 - i)]
        else:
            itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8)]

        # Add sub tanks into the pool
        if "Sub Tanks" in sigma_open and self.options.sigma_sub_tank_count.value > 0:
            i = self.options.sigma_sub_tank_count.value
            itempool += [self.create_item(ItemName.sub_tank) for _ in range(i)]
            if i != 4:
                itempool += [self.create_item(ItemName.sub_tank, ItemClassification.useful) for _ in range(4 - i)]
        else:
            itempool += [self.create_item(ItemName.sub_tank, ItemClassification.useful) for _ in range(4)]

        # Add junk items into the pool
        junk_count = total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([ItemName.small_hp] * 30)
        junk_weights += ([ItemName.large_hp] * 40)
        junk_weights += ([ItemName.life] * 30)

        junk_pool = []
        for i in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Set Maverick Medals
        maverick_location_names = [
            LocationName.armored_armadillo_clear,
            LocationName.boomer_kuwanger_clear,
            LocationName.chill_penguin_clear,
            LocationName.flame_mammoth_clear,
            LocationName.launch_octopus_clear,
            LocationName.spark_mandrill_clear,
            LocationName.sting_chameleon_clear,
            LocationName.storm_eagle_clear
        ]
        for location_name in maverick_location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(ItemName.maverick_medal))

        # Set victory item
        self.multiworld.get_location(LocationName.sigma_fortress_4_sigma, self.player).place_locked_item(self.create_item(ItemName.victory))

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_classification=False) -> Item:
        data = item_table[name]

        if force_classification:
            classification = force_classification
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
        
        created_item = MMXItem(name, classification, data.code, self.player)

        return created_item


    def set_rules(self):
        from .Rules import set_rules
        set_rules(self)


    def fill_slot_data(self):
        slot_data = {}
        # Write options to slot_data
        slot_data["boss_weakness_rando"] = self.options.boss_weakness_rando.value
        slot_data["boss_weakness_strictness"] = self.options.boss_weakness_strictness.value
        slot_data["pickupsanity"] = self.options.pickupsanity.value
        slot_data["jammed_buster"] = self.options.jammed_buster.value
        slot_data["hadouken_in_pool"] = self.options.hadouken_in_pool.value
        slot_data["pickupsanity"] = self.options.pickupsanity.value
        slot_data["logic_boss_weakness"] = self.options.logic_boss_weakness.value
        slot_data["logic_leg_sigma"] = self.options.logic_leg_sigma.value
        slot_data["logic_charged_shotgun_ice"] = self.options.logic_charged_shotgun_ice.value
        slot_data["sigma_all_levels"] = self.options.sigma_all_levels.value
        value = 0
        sigma_open = self.options.sigma_open.value
        if "Medals" in sigma_open:
            value |= 0x01
        if "Weapons" in sigma_open:
            value |= 0x02
        if "Armor Upgrades" in sigma_open:
            value |= 0x04
        if "Heart Tanks" in sigma_open:
            value |= 0x08
        if "Sub Tanks" in sigma_open:
            value |= 0x10
        slot_data["sigma_open"] = value
        slot_data["sigma_medal_count"] = self.options.sigma_medal_count.value
        slot_data["sigma_weapon_count"] = self.options.sigma_weapon_count.value
        slot_data["sigma_upgrade_count"] = self.options.sigma_upgrade_count.value
        slot_data["sigma_heart_tank_count"] = self.options.sigma_heart_tank_count.value
        slot_data["sigma_sub_tank_count"] = self.options.sigma_sub_tank_count.value

        # Write boss weaknesses to slot_data
        slot_data["boss_weaknesses"] = {}
        for boss, entries in self.boss_weaknesses.items():
            slot_data["boss_weaknesses"][boss] = []
            for entry in entries:
                slot_data["boss_weaknesses"][boss].append(entry[1])
        
        return slot_data


    def generate_early(self):
        if self.options.early_legs:
            self.multiworld.early_items[self.player][ItemName.legs] = 1
            
        self.boss_weaknesses = {}
        self.boss_weakness_data = {}
        handle_weaknesses(self)
    
        early_stage = self.random.choice(list(item_groups["Access Codes"]))
        self.multiworld.local_early_items[self.player][early_stage] = 1


    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        if self.options.boss_weakness_rando != "vanilla":
            spoiler_handle.write(f"\nMega Man X boss weaknesses for {self.multiworld.player_name[self.player]}:\n")
            
            for boss, data in self.boss_weaknesses.items():
                weaknesses = ""
                for i in range(len(data)):
                    weaknesses += f"{weapon_id[data[i][1]]}, "
                weaknesses = weaknesses[:-2]
                spoiler_handle.writelines(f"{boss + ':':<30s}{weaknesses}\n")


    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if not self.options.boss_weakness_rando:
            return
        
        boss_to_id = {
            0x00: "Armored Armadillo",
            0x01: "Chill Penguin",
            0x02: "Spark Mandrill",
            0x03: "Launch Octopus",
            0x04: "Boomer Kuwanger",
            0x05: "Sting Chameleon",
            0x06: "Storm Eagle",
            0x07: "Flame Mammoth",
            0x08: "Bospider",
            0x09: "Vile",
            0x0A: "Boomer Kuwanger",
            0x0B: "Chill Penguin",
            0x0C: "Storm Eagle",
            0x0D: "Rangda Bangda",
            0x0E: "Armored Armadillo",
            0x0F: "Sting Chameleon",
            0x10: "Spark Mandrill",
            0x11: "Launch Octopus",
            0x12: "Flame Mammoth",
            0x17: "Thunder Slimer",
            0x1E: "D-Rex",
            0x13: "Velguarder",
            0x1F: "Sigma",
        }
        boss_weakness_hint_data = {}
        for loc_name, level_data in location_id_to_level_id.items():
            if level_data[1] == 0x000:
                boss_id = level_data[2]
                if boss_id not in boss_to_id.keys():
                    continue
                boss = boss_to_id[boss_id]
                data = self.boss_weaknesses[boss]
                weaknesses = ""
                for i in range(len(data)):
                    weaknesses += f"{weapon_id[data[i][1]]}, "
                weaknesses = weaknesses[:-2]
                if boss == "Sigma":
                    data = self.boss_weaknesses["Wolf Sigma"]
                    weaknesses += ". Wolf Sigma: "
                    for i in range(len(data)):
                        weaknesses += f"{weapon_id[data[i][1]]}, "
                    weaknesses = weaknesses[:-2]
                location = self.multiworld.get_location(loc_name, self.player)
                boss_weakness_hint_data[location.address] = weaknesses

        hint_data[self.player] = boss_weakness_hint_data


    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))


    def generate_output(self, output_directory: str):
        try:
            patch = MMXProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("mmx_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mmx_basepatch.bsdiff4"))
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected


    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
