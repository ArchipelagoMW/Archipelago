import dataclasses
import os
import typing
import settings
import threading
import pkgutil

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import MMX2Item, ItemData, item_table, junk_table, item_groups
from .Locations import MMX2Location, setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName, EventName
from .Options import MMX2Options, mmx2_option_groups
from .Client import MMX2SNIClient
from .Levels import location_id_to_level_id
from .Weaknesses import handle_weaknesses, weapon_id
from .Rom import patch_rom, MMX2ProcedurePatch, HASH_US, HASH_LEGACY

class MMX2Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Mega Man X2 US ROM"""
        description = "Mega Man X2 (USA) ROM File"
        copy_to = "Mega Man X2 (USA).sfc"
        md5s = [HASH_US, HASH_LEGACY]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMX2Web(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Mega Man X2 with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )
    
    setup_es = Tutorial(
        "Guía de configuración de Multiworld",
        "Guía para jugar Mega Man X2 en Archipelago",
        "Spanish",
        "setup_es.md",
        "setup/es",
        ["lx5"]
    )

    tutorials = [setup_en, setup_es]


    option_groups = mmx2_option_groups


class MMX2World(World):
    """
    Mega Man X2, released in 1994 for the SNES, is the second game in Capcom's "Mega Man X" series. 
    Players control Mega Man X, a Maverick Hunter, as he battles a new group of Mavericks and the X-Hunters, 
    who have taken parts of his ally Zero. The game features classic run-and-gun gameplay with challenging levels, 
    boss battles that grant new weapons, and the use of the Cx4 chip for enhanced graphics.
    """
    game = "Mega Man X2"
    web = MMX2Web()

    settings: typing.ClassVar[MMX2Settings]
    
    options_dataclass = MMX2Options
    options: MMX2Options

    required_client_version = (0, 5, 0)

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

        itempool: typing.List[MMX2Item] = []
        
        connect_regions(self)
        
        total_required_locations = 38
        if self.options.base_boss_rematch_count.value != 0:
            total_required_locations += 8
        if self.options.pickupsanity.value:
            total_required_locations += 78

        # Setup item pool

        # Add levels into the pool
        start_inventory = self.options.start_inventory.value.copy()
        stage_list = [
            ItemName.stage_wheel_gator,
            ItemName.stage_bubble_crab,
            ItemName.stage_flame_stag,
            ItemName.stage_morph_moth,
            ItemName.stage_magna_centipede,
            ItemName.stage_crystal_snail,
            ItemName.stage_overdrive_ostrich,
            ItemName.stage_wire_sponge,
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

        if len(self.options.base_open.value) == 0:
            itempool += [self.create_item(ItemName.stage_x_hunter)]

        # Add weapons into the pool
        itempool += [self.create_item(ItemName.spin_wheel)]
        itempool += [self.create_item(ItemName.bubble_splash)]
        itempool += [self.create_item(ItemName.speed_burner)]
        itempool += [self.create_item(ItemName.silk_shot)]
        itempool += [self.create_item(ItemName.magnet_mine)]
        itempool += [self.create_item(ItemName.crystal_hunter)]
        itempool += [self.create_item(ItemName.sonic_slicer)]
        itempool += [self.create_item(ItemName.strike_chain)]
        
        if self.options.shoryuken_in_pool:
            itempool += [self.create_item(ItemName.shoryuken, ItemClassification.useful)]

        # Add armor upgrades into the pool
        base_open = self.options.base_open.value
        if "Armor Upgrades" in base_open and self.options.base_upgrade_count.value > 0:
            itempool += [self.create_item(ItemName.body)]
            itempool += [self.create_item(ItemName.helmet)]
        else:
            itempool += [self.create_item(ItemName.body, ItemClassification.useful)]
            if self.options.logic_helmet_checkpoints.value:
                itempool += [self.create_item(ItemName.helmet)]
            else:
                itempool += [self.create_item(ItemName.helmet, ItemClassification.useful)]
        itempool += [self.create_item(ItemName.arms)]
        if self.options.jammed_buster.value:
            itempool += [self.create_item(ItemName.arms)]
        itempool += [self.create_item(ItemName.legs)]

        # Add heart tanks into the pool
        if "Heart Tanks" in base_open and self.options.base_heart_tank_count.value > 0:
            i = self.options.base_heart_tank_count.value
            itempool += [self.create_item(ItemName.heart_tank) for _ in range(i)]
            if i != 8:
                i = 8 - i
                itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8 - i)]
        else:
            itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8)]

        # Add sub tanks into the pool
        if "Sub Tanks" in base_open and self.options.base_sub_tank_count.value > 0:
            i = self.options.base_sub_tank_count.value
            itempool += [self.create_item(ItemName.sub_tank) for _ in range(i)]
            if i != 4:
                itempool += [self.create_item(ItemName.sub_tank, ItemClassification.useful) for _ in range(4 - i)]
        else:
            itempool += [self.create_item(ItemName.sub_tank, ItemClassification.useful) for _ in range(4)]

        # Setup junk items
        junk_count = total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([ItemName.small_hp] * 20)
        junk_weights += ([ItemName.large_hp] * 35)
        junk_weights += ([ItemName.life] * 25)

        junk_pool = []
        for i in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Set Maverick Medals
        maverick_location_names =[
            LocationName.wheel_gator_clear,
            LocationName.bubble_crab_clear,
            LocationName.flame_stag_clear,
            LocationName.morph_moth_clear,
            LocationName.magna_centipede_clear,
            LocationName.crystal_snail_clear,
            LocationName.overdrive_ostrich_clear,
            LocationName.wire_sponge_clear
        ]
        for location_name in maverick_location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(ItemName.maverick_medal))

        # Set sigma access item
        self.multiworld.get_location(LocationName.x_hunter_stage_4_clear, self.player).place_locked_item(self.create_item(ItemName.stage_sigma))

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
        
        created_item = MMX2Item(name, classification, data.code, self.player)

        return created_item


    def set_rules(self):
        from .Rules import set_rules
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Mega Man X2" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Mega Man X2"]
                    self.boss_weaknesses = slot_data["weakness_rules"]
        set_rules(self)


    def fill_slot_data(self):
        slot_data = {}

        # Write options to slot_data
        slot_data["boss_weakness_rando"] = self.options.boss_weakness_rando.value
        slot_data["boss_weakness_strictness"] = self.options.boss_weakness_strictness.value
        slot_data["pickupsanity"] = self.options.pickupsanity.value
        slot_data["jammed_buster"] = self.options.jammed_buster.value
        slot_data["shoryuken_in_pool"] = self.options.shoryuken_in_pool.value
        slot_data["energy_link"] = self.options.energy_link.value
        
        value = 0
        base_open = self.options.base_open.value
        if "Medals" in base_open:
            value |= 0x01
        if "Weapons" in base_open:
            value |= 0x02
        if "Armor Upgrades" in base_open:
            value |= 0x04
        if "Heart Tanks" in base_open:
            value |= 0x08
        if "Sub Tanks" in base_open:
            value |= 0x10
        slot_data["base_open"] = value
        slot_data["base_medal_count"] = self.options.base_medal_count.value
        slot_data["base_weapon_count"] = self.options.base_weapon_count.value
        slot_data["base_upgrade_count"] = self.options.base_upgrade_count.value
        slot_data["base_heart_tank_count"] = self.options.base_heart_tank_count.value
        slot_data["base_sub_tank_count"] = self.options.base_sub_tank_count.value
        slot_data["base_all_levels"] = self.options.base_all_levels.value
        
        # Write boss weaknesses to slot_data (and for UT)
        slot_data["boss_weaknesses"] = {}
        slot_data["weakness_rules"] = {}
        for boss, entries in self.boss_weaknesses.items():
            slot_data["weakness_rules"][boss] = entries.copy()
            slot_data["boss_weaknesses"][boss] = []
            for entry in entries:
                slot_data["boss_weaknesses"][boss].append(entry[1])
                
        return slot_data


    def generate_early(self):
        # Generate weaknesses
        self.boss_weakness_data = {}
        self.boss_weaknesses = {}
        handle_weaknesses(self)


    def interpret_slot_data(self, slot_data):
        local_weaknesses = dict()
        for boss, entries in slot_data["weakness_rules"].items():
            local_weaknesses[boss] = entries.copy()
        return {"weakness_rules": local_weaknesses}
    

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        spoiler_handle.write(f"\nMega Man X2 boss weaknesses for {self.multiworld.player_name[self.player]}:\n")
        
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
            0x00: "Wheel Gator",
            0x01: "Bubble Crab",
            0x02: "Flame Stag",
            0x03: "Morph Moth",
            0x04: "Magna Centipede",
            0x05: "Crystal Snail",
            0x06: "Overdrive Ostrich",
            0x07: "Wire Sponge",
            0x08: "Agile",
            0x09: "Serges",
            0x0A: "Violen",
            0x0B: "Neo Violen",
            0x0C: "Serges Tank",
            0x0D: "Agile Flyer",
            0x0E: "Wheel Gator",
            0x0F: "Bubble Crab",
            0x10: "Flame Stag",
            0x11: "Morph Moth",
            0x12: "Magna Centipede",
            0x13: "Crystal Snail",
            0x14: "Overdrive Ostrich",
            0x15: "Wire Sponge",
            0x16: "Zero",
            0x17: "Sigma",
            0x19: "Pararoid S-38",
            0x1D: "Pararoid S-38",
            0x1A: "Chop Register",
            0x1B: "Raider Killer",
            0x1C: "Magna Quartz",
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
                if boss == "Serges Tank":
                    data = self.boss_weaknesses["Serges"]
                    weaknesses += ". Serges: "
                    for i in range(len(data)):
                        weaknesses += f"{weapon_id[data[i][1]]}, "
                    weaknesses = weaknesses[:-2]
                elif boss == "Sigma":
                    data = self.boss_weaknesses["Sigma Virus"]
                    weaknesses += ". Sigma Virus: "
                    for i in range(len(data)):
                        weaknesses += f"{weapon_id[data[i][1]]}, "
                    weaknesses = weaknesses[:-2]
                try:
                    location = self.multiworld.get_location(loc_name, self.player)
                except KeyError:
                    pass
                boss_weakness_hint_data[location.address] = weaknesses

        hint_data[self.player] = boss_weakness_hint_data


    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))


    def generate_output(self, output_directory: str):
        try:
            patch = MMX2ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("mmx2_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mmx2_basepatch.bsdiff4"))
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
