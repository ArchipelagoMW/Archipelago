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
from .Options import MMXOptions
from .Client import MMXSNIClient
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
        start_inventory = self.multiworld.start_inventory[self.player].value.copy()
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

        if self.options.sigma_open == "multiworld":
            itempool += [self.create_item(ItemName.stage_sigma_fortress)]

        # Add weapons into the pool
        if self.options.sigma_open == "weapons" or (self.options.sigma_open == "all" and self.options.sigma_weapon_count.value > 0):
            itempool += [self.create_item(ItemName.electric_spark)]
            itempool += [self.create_item(ItemName.homing_torpedo)]
            itempool += [self.create_item(ItemName.storm_tornado)]
            itempool += [self.create_item(ItemName.shotgun_ice)]
            itempool += [self.create_item(ItemName.rolling_shield)]
        else:
            if self.options.logic_boss_weakness.value:
                itempool += [self.create_item(ItemName.electric_spark)]
                itempool += [self.create_item(ItemName.homing_torpedo)]
                itempool += [self.create_item(ItemName.storm_tornado)]
            else:
                itempool += [self.create_item(ItemName.electric_spark, ItemClassification.useful)]
                itempool += [self.create_item(ItemName.homing_torpedo, ItemClassification.useful)]
                itempool += [self.create_item(ItemName.storm_tornado, ItemClassification.useful)]

            if self.options.logic_boss_weakness.value or self.options.logic_charged_shotgun_ice.value:
                itempool += [self.create_item(ItemName.shotgun_ice)]
            else:
                itempool += [self.create_item(ItemName.shotgun_ice, ItemClassification.useful)]

            if self.options.logic_boss_weakness.value or self.options.pickupsanity.value: 
                itempool += [self.create_item(ItemName.rolling_shield)]
            else: 
                itempool += [self.create_item(ItemName.rolling_shield, ItemClassification.useful)]

        itempool += [self.create_item(ItemName.chameleon_sting)]
        itempool += [self.create_item(ItemName.fire_wave)]
        itempool += [self.create_item(ItemName.boomerang_cutter)]

        # Add upgrades into the pool
        if self.options.sigma_open == "armor_upgrades" or (self.options.sigma_open == "all" and self.options.sigma_upgrade_count.value > 0):
            itempool += [self.create_item(ItemName.body)]
        else:
            itempool += [self.create_item(ItemName.body, ItemClassification.useful)]
        itempool += [self.create_item(ItemName.arms)]
        if self.options.jammed_buster.value:
            itempool += [self.create_item(ItemName.arms)]
        itempool += [self.create_item(ItemName.helmet)]
        itempool += [self.create_item(ItemName.legs)]

        # Add heart tanks into the pool
        if self.options.sigma_open == "heart_tanks" or (self.options.sigma_open == "all" and self.options.sigma_heart_tank_count.value > 0):
            i = self.options.sigma_heart_tank_count.value
            itempool += [self.create_item(ItemName.heart_tank) for _ in range(i)]
            if i != 8:
                i = 8 - i
                itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8 - i)]
        else:
            itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8)]

        # Add sub tanks into the pool
        if self.options.sigma_open == "sub_tanks" or (self.options.sigma_open == "all" and self.options.sigma_sub_tank_count.value > 0):
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
        for option_name in (attr.name for attr in dataclasses.fields(MMXOptions)
                            if attr not in dataclasses.fields(PerGameCommonOptions)):
            option = getattr(self.options, option_name)
            slot_data[option_name] = option.value
        return slot_data
    
    def generate_early(self):
        if self.options.early_legs:
            self.multiworld.early_items[self.player][ItemName.legs] = 1

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

    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool, usefulitempool, filleritempool, fill_locations):
        return