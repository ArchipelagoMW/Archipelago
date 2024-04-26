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
from .Items import MMX3Item, ItemData, item_table, junk_table, item_groups
from .Locations import MMX3Location, setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName, EventName
from .Options import MMX3Options
from .Client import MMX3SNIClient
from .Rom import patch_rom, MMX3ProcedurePatch, HASH_US, HASH_LEGACY

class MMX3Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Mega Man X3 US ROM"""
        description = "Mega Man X3 (USA) ROM File"
        copy_to = "Mega Man X3 (USA).sfc"
        md5s = [HASH_US, HASH_LEGACY]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMX3Web(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Mega Man X3 with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )

    tutorials = [setup_en]


class MMX3World(World):
    """
    Mega Man X3 WIP
    """
    game = "Mega Man X3"
    web = MMX3Web()

    settings: typing.ClassVar[MMX3Settings]
    
    options_dataclass = MMX3Options
    options: MMX3Options

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

        itempool: typing.List[MMX3Item] = []
        
        connect_regions(self)
        
        total_required_locations = 45
        if self.options.doppler_lab_3_boss_rematch_count != 0:
            total_required_locations += 8
        if self.options.pickupsanity:
            total_required_locations += 58
        
        # Setup item pool

        # Add levels into the pool
        start_inventory = self.multiworld.start_inventory[self.player].value.copy()
        stage_list = [
            ItemName.stage_toxic_seahorse,
            ItemName.stage_volt_catfish,
            ItemName.stage_tunnel_rhino,
            ItemName.stage_blizzard_buffalo,
            ItemName.stage_crush_crawfish,
            ItemName.stage_neon_tiger,
            ItemName.stage_blast_hornet,
            ItemName.stage_gravity_beetle,
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
                    self.multiworld.get_location(LocationName.intro_stage_clear, self.player).place_locked_item(self.create_item(stage_list[i]))
                else:
                    itempool += [self.create_item(stage_list[i])]

        if self.options.doppler_open == "multiworld":
            itempool += [self.create_item(ItemName.stage_doppler_lab)]
        if self.options.vile_open == "multiworld":
            itempool += [self.create_item(ItemName.stage_vile)]

        itempool += [self.create_item(ItemName.parasitic_bomb)]
        itempool += [self.create_item(ItemName.frost_shield)]
        itempool += [self.create_item(ItemName.acid_burst)]
        itempool += [self.create_item(ItemName.tornado_fang)]
        itempool += [self.create_item(ItemName.triad_thunder)]
        itempool += [self.create_item(ItemName.spinning_blade)]
        itempool += [self.create_item(ItemName.ray_splasher)]
        itempool += [self.create_item(ItemName.gravity_well)]

        itempool += [self.create_item(ItemName.ride_chimera)]
        itempool += [self.create_item(ItemName.ride_kangaroo)]
        itempool += [self.create_item(ItemName.ride_hawk)]
        itempool += [self.create_item(ItemName.ride_frog)]
        
        if self.options.logic_z_saber.value == 5:
            itempool += [self.create_item(ItemName.z_saber, ItemClassification.useful)]
        else:
            itempool += [self.create_item(ItemName.z_saber)]

        if self.options.doppler_open in ("armor_upgrades", "all") or self.options.vile_open in ("armor_upgrades", "all"):
            itempool += [self.create_item(ItemName.third_armor_helmet) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_body) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_arms) for _ in range(2 + self.options.jammed_buster.value)]
        else:
            itempool += [self.create_item(ItemName.third_armor_helmet, ItemClassification.useful) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_body, ItemClassification.useful) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_arms, ItemClassification.useful)]
            itempool += [self.create_item(ItemName.third_armor_arms) for _ in range(1 + self.options.jammed_buster.value)]
        itempool += [self.create_item(ItemName.third_armor_legs) for _ in range(2)]

        # Add heart tanks into the pool
        doppler_logic = self.options.doppler_open in ("heart_tanks", "all") and self.options.doppler_heart_tank_count.value > 0
        highest_count = self.options.doppler_heart_tank_count.value if doppler_logic else 0
        vile_logic = self.options.vile_open in ("heart_tanks", "all") and self.options.vile_heart_tank_count.value > 0
        if vile_logic:
            if self.options.vile_heart_tank_count.value > highest_count:
                highest_count = self.options.vile_heart_tank_count.value
        if highest_count > 0:
            i = highest_count
            itempool += [self.create_item(ItemName.heart_tank) for _ in range(i)]
            if i != 8:
                i = 8 - i
                itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8 - i)]
        else:
            itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8)]

        # Add heart tanks into the pool
        doppler_logic = self.options.doppler_open in ("sub_tanks", "all") and self.options.doppler_sub_tank_count.value > 0
        highest_count = self.options.doppler_sub_tank_count.value if doppler_logic else 0
        vile_logic = self.options.vile_open in ("sub_tanks", "all") and self.options.vile_sub_tank_count.value > 0
        if vile_logic:
            if self.options.vile_sub_tank_count.value > highest_count:
                highest_count = self.options.vile_sub_tank_count.value
        if highest_count > 0:
            i = highest_count
            itempool += [self.create_item(ItemName.sub_tank) for _ in range(i)]
            if i != 4:
                i = 4 - i
                itempool += [self.create_item(ItemName.sub_tank, ItemClassification.useful) for _ in range(4 - i)]
        else:
            itempool += [self.create_item(ItemName.sub_tank, ItemClassification.useful) for _ in range(4)]

        # Setup junk items
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
        maverick_location_names =[
            LocationName.blizzard_buffalo_clear,
            LocationName.toxic_seahorse_clear,
            LocationName.tunnel_rhino_clear,
            LocationName.volt_catfish_clear,
            LocationName.crush_crawfish_clear,
            LocationName.neon_tiger_clear,
            LocationName.gravity_beetle_clear,
            LocationName.blast_hornet_clear
        ]
        for location_name in maverick_location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(ItemName.maverick_medal))

        # Set victory item
        self.multiworld.get_location(LocationName.victory, self.player).place_locked_item(self.create_item(ItemName.victory))

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
        
        created_item = MMX3Item(name, classification, data.code, self.player)

        return created_item

    def set_rules(self):
        from .Rules import set_rules
        set_rules(self)
    
    def fill_slot_data(self):
        slot_data = {}
        for option_name in (attr.name for attr in dataclasses.fields(MMX3Options)
                            if attr not in dataclasses.fields(PerGameCommonOptions)):
            option = getattr(self.options, option_name)
            slot_data[option_name] = option.value
        return slot_data
    
    def generate_early(self):
        early_stage = self.random.choice(list(item_groups["Access Codes"]))
        self.multiworld.local_early_items[self.player][early_stage] = 1

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))

    def generate_output(self, output_directory: str):
        try:
            patch = MMX3ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("mmx3_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mmx3_basepatch.bsdiff4"))
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