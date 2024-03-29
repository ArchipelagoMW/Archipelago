import dataclasses
import os
import typing
import math
import settings
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import MMX3Item, ItemData, item_table, junk_table, item_groups
from .Locations import MMX3Location, setup_locations, all_locations
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName, EventName
from .Options import MMX3Options
from .Client import MMX3SNIClient
from .Rom import LocalRom, patch_rom, get_base_rom_path, MMX3DeltaPatch
from worlds.generic.Rules import add_rule, exclusion_rules

class MMX3Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the SMW US rom"""
        description = "Mega Man X3 (USA) ROM File"
        copy_to = "Mega Man X3 (USA).sfc"
        md5s = [MMX3DeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMX3Web(WebWorld):
    setup_en = Tutorial(
        "setup",
        "description here",
        "en",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )
    tutorials = [setup_en]


class MMX3World(World):
    game = "Mega Man X3"
    web = MMX3Web()

    settings: typing.ClassVar[MMX3Settings]
    
    options_dataclass = MMX3Options
    options: MMX3Options

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        location_table = setup_locations(self)
        create_regions(self.multiworld, self.player, self, location_table)

        itempool: typing.List[MMX3Item] = []
        
        connect_regions(self)
        
        total_required_locations = 54
        if self.options.pickupsanity:
            total_required_locations += 58
        
        # Setup item pool
        itempool += [self.create_item(ItemName.stage_toxic_seahorse)]
        itempool += [self.create_item(ItemName.stage_volt_catfish)]
        itempool += [self.create_item(ItemName.stage_tunnel_rhino)]
        itempool += [self.create_item(ItemName.stage_blizzard_buffalo)]
        itempool += [self.create_item(ItemName.stage_crush_crawfish)]
        itempool += [self.create_item(ItemName.stage_neon_tiger)]
        itempool += [self.create_item(ItemName.stage_blast_hornet)]
        itempool += [self.create_item(ItemName.stage_gravity_beetle)]

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

        if self.options.doppler_open.value == 3 or self.options.vile_open.value == 3:
            itempool += [self.create_item(ItemName.third_armor_helmet) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_body) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_arms) for _ in range(2)]
        else:
            itempool += [self.create_item(ItemName.third_armor_helmet, ItemClassification.useful) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_body, ItemClassification.useful) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_arms, ItemClassification.useful)]
            itempool += [self.create_item(ItemName.third_armor_arms)]
        itempool += [self.create_item(ItemName.third_armor_legs) for _ in range(2)]

        if self.options.doppler_open.value == 4 or self.options.vile_open.value == 4:
            itempool += [self.create_item(ItemName.heart_tank) for _ in range(8)]
        else:
            itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8)]
        if self.options.doppler_open.value == 5 or self.options.vile_open.value == 5:
            itempool += [self.create_item(ItemName.sub_tank) for _ in range(4)]
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

    
    def _get_slot_data(self):
        return
    
    def generate_early(self):
        return

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))

    def generate_output(self, output_directory: str):
        rompath = ""  # if variable is not declared finally clause may fail
        try:
            multiworld = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom, self.player)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = MMX3DeltaPatch(os.path.splitext(rompath)[0]+MMX3DeltaPatch.patch_file_ending, player=player,
                                  player_name=multiworld.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)


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