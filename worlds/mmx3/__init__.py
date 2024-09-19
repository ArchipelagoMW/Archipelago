import dataclasses
import os
import typing
import math
import settings
import hashlib
import threading
import pkgutil

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import MMX3Item, ItemData, item_table, junk_table, item_groups
from .Locations import MMX3Location, setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName, EventName
from .Options import MMX3Options, mmx3_option_groups
from .Client import MMX3SNIClient
from .Levels import location_id_to_level_id
from .Weaknesses import handle_weaknesses, weapon_id
from .Rom import patch_rom, MMX3ProcedurePatch, HASH_US, HASH_LEGACY

from typing import Dict, Any, TYPE_CHECKING, Optional, Sequence, Tuple, ClassVar, List

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
    
    setup_es = Tutorial(
        "Guía de configuración de Multiworld",
        "Guía para jugar Mega Man X3 en Archipelago",
        "Spanish",
        "setup_es.md",
        "setup/es",
        ["lx5"]
    )

    tutorials = [setup_en, setup_es]

    option_groups = mmx3_option_groups


class MMX3World(World):
    """
    Mega Man X3, released in 1995 for the SNES, is the third game in Capcom's "Mega Man X" series. 
    Players once again control Mega Man X, who must thwart a rebellion led by the Maverick Reploid scientist 
    Dr. Doppler. The game introduces the ability to play as Zero for limited segments, adding variety to the gameplay.
    """
    game = "Mega Man X3"
    web = MMX3Web()

    settings: typing.ClassVar[MMX3Settings]
    
    options_dataclass = MMX3Options
    options: MMX3Options

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

        itempool: typing.List[MMX3Item] = []
        
        connect_regions(self)
        
        total_required_locations = 45
        if self.doppler_lab_3_boss_rematch_count != 0:
            total_required_locations += 8
        if self.pickupsanity:
            total_required_locations += 58
        
        # Setup item pool

        # Add levels into the pool
        start_inventory = self.options.start_inventory.value.copy()
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

        if len(self.doppler_open) == 0:
            itempool += [self.create_item(ItemName.stage_doppler_lab)]
        if len(self.vile_open) == 0:
            itempool += [self.create_item(ItemName.stage_vile)]

        # Add weapons into the pool
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
        
        if self.options.zsaber_in_pool:
            itempool += [self.create_item(ItemName.z_saber, ItemClassification.useful)]

        # Add armor upgrades into the pool
        doppler_open = self.doppler_open
        vile_open = self.vile_open
        if ("Armor Upgrades" in doppler_open and self.doppler_upgrade_count > 0) or \
           ("Armor Upgrades" in vile_open and self.vile_upgrade_count > 0):
            itempool += [self.create_item(ItemName.third_armor_helmet) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_body) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_arms) for _ in range(2 + self.jammed_buster)]
        else:
            if self.logic_helmet_checkpoints:
                itempool += [self.create_item(ItemName.third_armor_helmet) for _ in range(2)]
            else:
                itempool += [self.create_item(ItemName.third_armor_helmet, ItemClassification.useful) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_body, ItemClassification.useful) for _ in range(2)]
            itempool += [self.create_item(ItemName.third_armor_arms, ItemClassification.useful)]
            itempool += [self.create_item(ItemName.third_armor_arms) for _ in range(1 + self.jammed_buster)]
        itempool += [self.create_item(ItemName.third_armor_legs) for _ in range(2)]

        # Add heart tanks into the pool
        doppler_logic = "Heart Tanks" in doppler_open and self.doppler_heart_tank_count > 0
        highest_count = self.doppler_heart_tank_count if doppler_logic else 0
        vile_logic = "Heart Tanks" in vile_open and self.vile_heart_tank_count > 0
        if vile_logic:
            if self.vile_heart_tank_count > highest_count:
                highest_count = self.vile_heart_tank_count
        if highest_count > 0:
            i = highest_count
            itempool += [self.create_item(ItemName.heart_tank) for _ in range(i)]
            if i != 8:
                itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8 - i)]
        else:
            itempool += [self.create_item(ItemName.heart_tank, ItemClassification.useful) for _ in range(8)]

        # Add sub tanks into the pool
        doppler_logic = "Sub Tanks" in doppler_open and self.doppler_sub_tank_count > 0
        highest_count = self.doppler_sub_tank_count if doppler_logic else 0
        vile_logic = "Sub Tanks" in vile_open and self.vile_sub_tank_count > 0
        if vile_logic:
            if self.vile_sub_tank_count > highest_count:
                highest_count = self.vile_sub_tank_count
        if highest_count > 0:
            i = highest_count
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
        
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Mega Man X3" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Mega Man X3"]
                    self.boss_weaknesses = slot_data["weakness_rules"]
                    print (self.boss_weaknesses)
                    self.boss_weakness_strictness = slot_data["boss_weakness_strictness"]
                    self.pickupsanity = slot_data["pickupsanity"]
                    self.jammed_buster = slot_data["jammed_buster"]
                    self.logic_boss_weakness = slot_data["logic_boss_weakness"]
                    self.logic_vile_required = slot_data["logic_vile_required"]
                    self.logic_helmet_checkpoints = slot_data["logic_helmet_checkpoints"]
                    self.doppler_open = slot_data["doppler_open"]
                    self.doppler_medal_count = slot_data["doppler_medal_count"]
                    self.doppler_weapon_count = slot_data["doppler_weapon_count"]
                    self.doppler_upgrade_count = slot_data["doppler_upgrade_count"]
                    self.doppler_heart_tank_count = slot_data["doppler_heart_tank_count"]
                    self.doppler_sub_tank_count = slot_data["doppler_sub_tank_count"]
                    self.doppler_all_labs = slot_data["doppler_all_labs"]
                    self.doppler_lab_2_boss = slot_data["doppler_lab_2_boss"]
                    self.doppler_lab_3_boss_rematch_count = slot_data["doppler_lab_3_boss_rematch_count"]
                    self.vile_open = slot_data["vile_open"]
                    self.vile_medal_count = slot_data["vile_medal_count"]
                    self.vile_weapon_count = slot_data["vile_weapon_count"]
                    self.vile_upgrade_count = slot_data["vile_upgrade_count"]
                    self.vile_heart_tank_count = slot_data["vile_heart_tank_count"]
                    self.vile_sub_tank_count = slot_data["vile_sub_tank_count"]
                    self.bit_medal_count = slot_data["bit_medal_count"]
                    self.byte_medal_count = slot_data["byte_medal_count"]

        set_rules(self)


    def interpret_slot_data(self, slot_data):
        local_weaknesses = {boss: entries for boss, entries in slot_data["weakness_rules"].items()}
            
        interpreted_slot_data = {
            "weakness_rules": local_weaknesses,
            "boss_weakness_strictness": slot_data["boss_weakness_strictness"],
            "pickupsanity": slot_data["pickupsanity"],
            "jammed_buster": slot_data["jammed_buster"],
            "logic_boss_weakness": slot_data["logic_boss_weakness"],
            "logic_vile_required": slot_data["logic_vile_required"],
            "logic_helmet_checkpoints": slot_data["logic_helmet_checkpoints"],
            "doppler_open": slot_data["doppler_open_text"],
            "doppler_medal_count": slot_data["doppler_medal_count"],
            "doppler_weapon_count": slot_data["doppler_weapon_count"],
            "doppler_upgrade_count": slot_data["doppler_upgrade_count"],
            "doppler_heart_tank_count": slot_data["doppler_heart_tank_count"],
            "doppler_sub_tank_count": slot_data["doppler_sub_tank_count"],
            "doppler_all_labs": slot_data["doppler_all_labs"],
            "doppler_lab_2_boss": slot_data["doppler_lab_2_boss"],
            "doppler_lab_3_boss_rematch_count": slot_data["doppler_lab_3_boss_rematch_count"],
            "vile_open": slot_data["vile_open_text"],
            "vile_medal_count": slot_data["vile_medal_count"],
            "vile_weapon_count": slot_data["vile_weapon_count"],
            "vile_upgrade_count": slot_data["vile_upgrade_count"],
            "vile_heart_tank_count": slot_data["vile_heart_tank_count"],
            "vile_sub_tank_count": slot_data["vile_sub_tank_count"],
            "bit_medal_count": slot_data["bit_medal_count"],
            "byte_medal_count": slot_data["byte_medal_count"],
        }

        return interpreted_slot_data
    

    def fill_slot_data(self):
        slot_data = {}

        # Write options to slot_data
        slot_data["energy_link"] = self.options.energy_link.value
        slot_data["boss_weakness_rando"] = self.options.boss_weakness_rando.value
        slot_data["boss_weakness_strictness"] = self.boss_weakness_strictness
        slot_data["pickupsanity"] = self.pickupsanity
        slot_data["jammed_buster"] = self.jammed_buster
        slot_data["zsaber_in_pool"] = self.options.zsaber_in_pool.value
        slot_data["logic_boss_weakness"] = self.logic_boss_weakness
        slot_data["logic_helmet_checkpoints"] = self.logic_helmet_checkpoints
        slot_data["logic_vile_required"] = self.logic_vile_required
        
        value = 0
        if "Medals" in  self.doppler_open:
            value |= 0x01
        if "Weapons" in  self.doppler_open:
            value |= 0x02
        if "Armor Upgrades" in  self.doppler_open:
            value |= 0x04
        if "Heart Tanks" in  self.doppler_open:
            value |= 0x08
        if "Sub Tanks" in  self.doppler_open:
            value |= 0x10
        slot_data["doppler_open"] = value
        slot_data["doppler_open_text"] = self.doppler_open.copy()
        slot_data["doppler_medal_count"] = self.doppler_medal_count
        slot_data["doppler_weapon_count"] = self.doppler_weapon_count
        slot_data["doppler_upgrade_count"] = self.doppler_upgrade_count
        slot_data["doppler_heart_tank_count"] = self.doppler_heart_tank_count
        slot_data["doppler_sub_tank_count"] = self.doppler_sub_tank_count

        slot_data["doppler_lab_2_boss"] = self.doppler_lab_2_boss
        slot_data["doppler_lab_3_boss_rematch_count"] = self.doppler_lab_3_boss_rematch_count
        slot_data["doppler_all_labs"] = self.doppler_all_labs
        
        value = 0
        if "Medals" in  self.vile_open:
            value |= 0x01
        if "Weapons" in  self.vile_open:
            value |= 0x02
        if "Armor Upgrades" in  self.vile_open:
            value |= 0x04
        if "Heart Tanks" in  self.vile_open:
            value |= 0x08
        if "Sub Tanks" in  self.vile_open:
            value |= 0x10
        slot_data["vile_open"] = value
        slot_data["vile_open_text"] = self.vile_open.copy()
        slot_data["vile_medal_count"] = self.vile_medal_count
        slot_data["vile_weapon_count"] = self.vile_weapon_count
        slot_data["vile_upgrade_count"] = self.vile_upgrade_count
        slot_data["vile_heart_tank_count"] = self.vile_heart_tank_count
        slot_data["vile_sub_tank_count"] = self.vile_sub_tank_count
        slot_data["logic_vile_required"] = self.logic_vile_required

        slot_data["bit_medal_count"] = self.bit_medal_count
        slot_data["byte_medal_count"] = self.byte_medal_count

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
        # Parse logic-relevant settings and save them elsewhere (needed for UT support)
        self.boss_weakness_strictness = self.options.boss_weakness_strictness.value
        self.pickupsanity = self.options.pickupsanity.value
        self.jammed_buster = self.options.jammed_buster.value
        self.logic_boss_weakness = self.options.logic_boss_weakness.value
        self.logic_vile_required = self.options.logic_vile_required.value
        self.logic_helmet_checkpoints = self.options.logic_helmet_checkpoints.value
        self.doppler_open = self.options.doppler_open.value.copy()
        self.doppler_medal_count = self.options.doppler_medal_count.value
        self.doppler_weapon_count = self.options.doppler_weapon_count.value
        self.doppler_upgrade_count = self.options.doppler_upgrade_count.value
        self.doppler_heart_tank_count = self.options.doppler_heart_tank_count.value
        self.doppler_sub_tank_count = self.options.doppler_sub_tank_count.value
        self.doppler_all_labs = self.options.doppler_all_labs.value
        self.vile_open = self.options.vile_open.value.copy()
        self.vile_medal_count = self.options.vile_medal_count.value
        self.vile_weapon_count = self.options.vile_weapon_count.value
        self.vile_upgrade_count = self.options.vile_upgrade_count.value
        self.vile_heart_tank_count = self.options.vile_heart_tank_count.value
        self.vile_sub_tank_count = self.options.vile_sub_tank_count.value
        self.bit_medal_count = self.options.bit_medal_count.value
        self.byte_medal_count = self.options.byte_medal_count.value
        self.doppler_lab_2_boss = self.options.doppler_lab_2_boss.value
        self.doppler_lab_3_boss_rematch_count = self.options.doppler_lab_3_boss_rematch_count.value

        # Enforce Vile stage options to have lower count than the Lab
        if self.doppler_medal_count >= self.vile_medal_count:
            self.vile_medal_count = max(self.doppler_medal_count - 1, 0)
        if self.doppler_weapon_count >= self.vile_weapon_count:
            self.vile_weapon_count = max(self.doppler_weapon_count - 1, 0)
        if self.doppler_upgrade_count >= self.vile_upgrade_count:
            self.vile_upgrade_count = max(self.doppler_upgrade_count - 1, 0)
        if self.doppler_heart_tank_count >= self.vile_heart_tank_count:
            self.vile_heart_tank_count = max(self.doppler_heart_tank_count - 1, 0)
        if self.doppler_sub_tank_count >= self.vile_sub_tank_count:
            self.vile_sub_tank_count = max(self.doppler_sub_tank_count - 1, 0)

        # Adjust bit and byte medal counts
        if self.bit_medal_count == 0 and self.byte_medal_count == 0:
            self.byte_medal_count = 1
        elif self.bit_medal_count >= self.byte_medal_count:
            if self.bit_medal_count == 7:
                self.bit_medal_count = 6
            self.byte_medal_count = self.bit_medal_count + 1

        # Generate weaknesses
        self.boss_weakness_data = {}
        self.boss_weaknesses = {}
        handle_weaknesses(self)


    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        spoiler_handle.write(f"\nMega Man X3 boss weaknesses for {self.multiworld.player_name[self.player]}:\n")
        
        for boss, data in self.boss_weaknesses.items():
            weaknesses = ""
            for i in range(len(data)):
                weaknesses += f"{weapon_id[data[i][1]]}, "
            weaknesses = weaknesses[:-2]
            spoiler_handle.writelines(f"{boss + ':':<30s}{weaknesses}\n")


    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        boss_to_id = {
            0x202: "Blast Hornet",
            0x203: "Shurikein",
            0x204: "Blizzard Buffalo",
            0x205: "Gravity Beetle",
            0x206: "Toxic Seahorse",
            0x207: "Hotareeca",
            0x208: "Volt Catfish",
            0x209: "Crush Crawfish",
            0x20A: "Tunnel Rhino",
            0x20B: "Hell Crusher",
            0x20C: "Neon Tiger",
            0x20D: "Worm Seeker-R",
            0x009: "Vile",
            0x20E: "Godkarmachine",
            0x210: "Dr. Doppler's Lab 2 Boss",
            0x21A: "Blast Hornet",
            0x213: "Blizzard Buffalo",
            0x219: "Gravity Beetle",
            0x214: "Toxic Seahorse",
            0x216: "Volt Catfish",
            0x217: "Crush Crawfish",
            0x215: "Tunnel Rhino",
            0x218: "Neon Tiger",
            0x212: "Doppler",
            0x00B: "Bit",
            0x00A: "Byte",
            0x00E: "Sigma",
        }
        # Remove disabled locations if rematch count is 0
        if self.options.doppler_lab_3_boss_rematch_count.value == 0:
            del boss_to_id[0x21A]
            del boss_to_id[0x213]
            del boss_to_id[0x219]
            del boss_to_id[0x214]
            del boss_to_id[0x216]
            del boss_to_id[0x217]
            del boss_to_id[0x215]
            del boss_to_id[0x218]

        boss_weakness_hint_data = {}
        for loc_name, level_data in location_id_to_level_id.items():
            boss_id = level_data[1]
            if boss_id not in boss_to_id.keys():
                continue

            boss = boss_to_id[boss_id]
            data = self.boss_weaknesses[boss]
            weaknesses = ""
            for i in range(len(data)):
                weaknesses += f"{weapon_id[data[i][1]]}, "
            weaknesses = weaknesses[:-2]

            if boss == "Sigma":
                data = self.boss_weaknesses["Kaiser Sigma"]
                weaknesses += ". Kaiser Sigma: "
                for i in range(len(data)):
                    weaknesses += f"{weapon_id[data[i][1]]}, "
                weaknesses = weaknesses[:-2]
            elif boss == "Godkarmachine":
                data = self.boss_weaknesses["Press Disposer"]
                weaknesses += ". Press Disposer: "
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
            patch = MMX3ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("mmx3_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mmx3_basepatch.bsdiff4"))
            patch.write_file("mmx3_manifest_for_bsnes.xml", pkgutil.get_data(__name__, "data/mmx3_manifest_for_bsnes.xml"))
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
