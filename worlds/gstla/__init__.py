from __future__ import annotations

import base64
import hashlib
from bisect import bisect
from collections import defaultdict
from io import BytesIO, StringIO
from math import floor

import settings
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
import os

from typing import List, TextIO, BinaryIO, ClassVar, Type, cast, Optional, Sequence, Tuple, Any, Mapping, TYPE_CHECKING, \
    Dict
from .Option_groups import gstla_option_groups
from .Option_presets import gstla_options_presets
from .Options import GSTLAOptions
from BaseClasses import Item, ItemClassification, Tutorial
from .Items import GSTLAItem, item_table, all_items, ItemType, create_events, create_items, create_item, \
    AP_PLACEHOLDER_ITEM, items_by_id, get_filler_item, AP_PROG_PLACEHOLDER_ITEM, create_filler_pool_weights, \
    create_trap_pool_weights, AP_USEFUL_PLACEHOLDER_ITEM, create_item_direct
from .Locations import GSTLALocation, all_locations, location_name_to_id, location_type_to_data
from .Rules import set_access_rules, set_item_rules, set_entrance_rules
from .Regions import create_regions
from .Connections import create_connections
from .gen.ItemData import mimics, characters
from .gen.LocationData import LocationType, location_name_to_data
from .gen.ItemNames import ItemName, item_id_by_name, name_by_item_id
from .gen.LocationNames import LocationName, ids_by_loc_name, loc_names_by_id
from .Names.RegionName import RegionName
from .LocationGroups import goldensuntla_location_groups
from .Rom import GSTLAPatchExtension, GSTLADeltaPatch, CHECKSUM_GSTLA
from .BizClient import GSTLAClient


import logging

from ..Files import APTokenTypes

logger = logging.getLogger()

class GSTLAWeb(WebWorld):
    theme = "jungle"
    option_groups = gstla_option_groups
    options_presets = gstla_options_presets

    tut_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Golden Sun The Lost Age randomizer on your computer",
        "English",
        "setup_en.md",
        "setup/en",
        ["Dragion", "PlatanoBailando"]
    )

    tutorials = [tut_en]

class GSTLASettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the GS TLA UE Rom"""
        description = "Golden Sun The Lost Age Rom File"
        copy_to: Optional[str] = "Golden Sun - The Lost Age (UE) [!].gba"

        def browse(self: settings.T,
                   filetypes: Optional[Sequence[Tuple[str, Sequence[str]]]] = None,
                   **kwargs: Any) -> Optional[settings.T]:
            if not filetypes:
                file_types = [("GBA", [".gba"])]
                return super().browse(file_types, **kwargs)
            else:
                return super().browse(filetypes, **kwargs)

        @classmethod
        def validate(cls, path: str) -> None:
            """Try to open and validate file against hashes"""
            with open(path, "rb", buffering=0) as f:
                try:
                    # cls._validate_stream_hashes(f)
                    base_rom_bytes = f.read()
                    basemd5 = hashlib.md5()
                    basemd5.update(base_rom_bytes)
                    if basemd5.hexdigest() == CHECKSUM_GSTLA:
                        # we need special behavior here
                        cls.copy_to = None
                    else:
                        raise ValueError('Supplied Base Rom does not match UE GBA Golden Sun TLA Version.'
                                        'Please provide the correct ROM version')
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")
    rom_file: RomFile = RomFile(RomFile.copy_to)


class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = GSTLAOptions
    options: GSTLAOptions
    data_version = 1
    items_ids_populated = set()
    location_flags_populated = set()
    settings: ClassVar[GSTLASettings]

    item_name_to_id = item_id_by_name#{item.itemName: itemfor item in all_items if item.type != ItemType.Event}
    location_name_to_id = ids_by_loc_name#{location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn.name: {item.name for item in all_items if item.type == ItemType.Djinn},
        ItemType.Character.name: {item.name for item in all_items if item.type == ItemType.Character},
        ItemType.Mimic.name: {item.name for item in all_items if item.type == ItemType.Mimic},
        "Lash": {ItemName.Lash_Pebble.value},
        "Pound": {ItemName.Pound_Cube.value},
        "Force": {ItemName.Orb_of_Force.value},
        "Douse": {ItemName.Douse_Drop.value},
        "Frost": {ItemName.Frost_Jewel.value},
        "Lift": {ItemName.Lifting_Gem.value},
        "Carry": {ItemName.Carry_Stone.value},
        "Catch": {ItemName.Catch_Beads.value},
        "Tremor": {ItemName.Tremor_Bit.value},
        "Scoop": {ItemName.Scoop_Gem.value},
        "Cyclone": {ItemName.Cyclone_Chip.value},
        "Burst": {ItemName.Burst_Brooch.value},
        "Grind": {ItemName.Grindstone.value},
        "Teleport": {ItemName.Teleport_Lapis.value},
        "Hover": {ItemName.Hover_Jade.value},
        "Shamans Rod": {ItemName.Shamans_Rod.value},
        "Sea Gods Tear": {ItemName.Sea_Gods_Tear.value},
        "Lil Turtle": {ItemName.Lil_Turtle.value}
    }
    location_name_groups = goldensuntla_location_groups

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self._character_levels: List[Tuple[int, int]] = []

    def generate_early(self) -> None:
        if self.options.shuffle_characters < 2:
            self.options.non_local_items.value -= self.item_name_groups[ItemType.Character.name]

        if self.options.lemurian_ship == 2:
            self.multiworld.push_precollected(create_item(ItemName.Ship, self.player))
        if self.options.start_with_wings_of_anemos == 1:
            self.multiworld.push_precollected(create_item(ItemName.Wings_of_Anemos, self.player))

        #When we add more traps and none are enabled we should force trap_chance to off
        if self.options.mimic_trap_weight == 0:
            self.options.trap_chance.value = 0

        if self.options.max_scaled_level < self.options.starting_levels:
            self.options.max_scaled_level = self.options.starting_levels

        #ensure that if all are set to 0 we force them all to 1, otherwise we can not create filler and clearly they wanted all to be the same weight.
        combined_weight = self.options.forge_material_filler_weight + self.options.rusty_material_filler_weight + self.options.stat_boost_filler_weight
        combined_weight += self.options.uncommon_consumable_filler_weight + self.options.forged_equipment_filler_weight + self.options.lucky_equipment_filler_weight
        combined_weight += self.options.shop_equipment_filler_weight + self.options.coins_filler_weight + self.options.common_consumable_filler_weight

        if combined_weight == 0:
            self.options.forge_material_filler_weight.value = 1
            self.options.rusty_material_filler_weight.value = 1
            self.options.stat_boost_filler_weight.value = 1
            self.options.uncommon_consumable_filler_weight.value = 1
            self.options.forged_equipment_filler_weight.value = 1
            self.options.lucky_equipment_filler_weight.value = 1
            self.options.shop_equipment_filler_weight.value = 1
            self.options.coins_filler_weight.value = 1
            self.options.common_consumable_filler_weight.value = 1

        create_filler_pool_weights(self)
        create_trap_pool_weights(self)


    def create_regions(self) -> None:
        create_regions(self)
        create_connections(self.multiworld, self.player)

    def create_items(self) -> None:
        create_events(self)
        create_items(self, self.player)

    def set_rules(self) -> None:
        set_entrance_rules(self)
        set_item_rules(self)
        set_access_rules(self)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def get_pre_fill_items(self) -> List["Item"]:
        pre_fill = []
        for key,val in GSTLAWorld.item_name_groups.items():
            if key in [ItemType.Djinn.name, ItemType.Character.name, ItemType.Mimic.name]:
                for item in val:
                    pre_fill.append(create_item(item, self.player))
        return pre_fill

    def generate_basic(self):
        pass

    def pre_fill(self) -> None:
        pass

    def get_filler_item_name(self) -> str:
        filler_item = get_filler_item(self)
        return filler_item.name

    def fill_slot_data(self) -> Mapping[str, Any]:
        ret = dict()
        ret['start_inventory'] = {
            item_id_by_name[k]: v
            for k, v in self.options.start_inventory.items()
        }

        for k,v in self.options.start_inventory_from_pool.items():
            if item_id_by_name[k] in ret['start_inventory']:
                ret['start_inventory'][item_id_by_name[k]] += v
            else:
                ret['start_inventory'][item_id_by_name[k]] = v

        return ret

    def generate_output(self, output_directory: str):
        if self.options.scale_mimics or self.options.scale_characters:
            self._handle_spheres()
        ap_settings = BytesIO()
        ap_settings_debug = StringIO()
        self._generate_rando_data(ap_settings, ap_settings_debug)

        patch = GSTLADeltaPatch(player=self.player,
                                player_name=self.player_name,
                                path=os.path.join(output_directory, self.multiworld.get_out_file_name_base(self.player)+GSTLADeltaPatch.patch_file_ending))
        patch.add_settings(ap_settings.getvalue(), ap_settings_debug.getvalue().encode("utf-8"))
        if self.options.auto_run:
            patch.write_token(APTokenTypes.XOR_8, 0x26361, 0x01)
            patch.write_token(APTokenTypes.XOR_8, 0x270A5, 0x01)
            patch.write_token(APTokenTypes.XOR_8, 0x279DD, 0x01)
            patch.write_token(APTokenTypes.XOR_8, 0x1007900, 0x01)
        patch.write_file("token_data.bin", patch.get_token_binary())
        patch.write()

    def _handle_spheres(self):
        mimic_map: defaultdict[int, List[GSTLALocation]]  = defaultdict(lambda: [])
        character_map: defaultdict[int, List[GSTLAItem]] = defaultdict(lambda: [])
        toons = {c.id for c in characters}
        spheres = self.multiworld.get_spheres()
        max_sphere = -1
        for i, sphere in enumerate(spheres):
            for loc in sphere:
                if loc.item.player != self.player:
                    continue
                if loc.item.name == ItemName.Victory:
                    max_sphere = i
                    continue
                if loc.item.code is None:
                    continue
                if cast(GSTLAItem, loc.item).item_data.is_mimic:
                    mimic_map[i].append(cast(GSTLALocation, loc))
                if loc.item.code in toons:
                    character_map[i].append(cast(GSTLAItem, loc.item))

        if max_sphere == -1:
            logger.warning("Could not find max sphere for GSTLA; cannot scale mimics or characters")
            return
        # logger.info("Max sphere is %d", max_sphere)

        if self.options.scale_mimics:
            self._scale_mimics(max_sphere, mimic_map)

        if self.options.scale_characters:
            self._scale_characters(max_sphere, character_map)


    def _scale_mimics(self, max_sphere: int, mimic_map: defaultdict[int, List[GSTLALocation]]):
        mimic_lists = []
        for i in range(1, len(mimics) - 1):
            mimic_lists.append(mimics[i - 1:i + 2])

        breakpoints = [(max_sphere + 1) / 7 * i for i in range(1, 8)]

        for sphere, mimic_locs in mimic_map.items():
            breakpoint_index = bisect(breakpoints, sphere)
            if breakpoint_index >= len(mimic_lists):
                breakpoint_index = len(mimic_lists) - 1
            mimic_list = mimic_lists[breakpoint_index]
            for mimic_loc in mimic_locs:
                if mimic_loc.locked:
                    # Guess someone really wanted this mimic here
                    continue
                current_item = mimic_loc.item
                current_item.location = None
                new_mimic = create_item_direct(self.random.choice(mimic_list), self.player)
                # logger.info("Replacing mimic %s with mimic %s in sphere %d", current_item.name, new_mimic.name, sphere)
                mimic_loc.item = new_mimic

    def _scale_characters(self, max_sphere: int, char_map: defaultdict[int, List[GSTLAItem]]):
        max_level = self.options.max_scaled_level.value
        starting_level = self.options.starting_levels.value
        for sphere, chars in char_map.items():
            for char in chars:
                level = min(max(floor((max_level - starting_level) * sphere / max_sphere + starting_level), starting_level), max_level)
                self._character_levels.append((char.code - 0xD00, level))


    def _generate_rando_data(self, rando_file: BinaryIO, debug_file: TextIO):
        rando_file.write(0x1.to_bytes(length=1, byteorder='little'))
        debug_file.write("Version: 1\n")

        rando_file.write(self.multiworld.seed.to_bytes(length=16, byteorder='little'))
        debug_file.write(f"Seed: {self.multiworld.seed}\n")

        self._write_options_for_rando(rando_file, debug_file)

        # rando_file.write((0).to_bytes(length=16, byteorder='little'))
        # debug_file.write("no settings (TBD)\n")
        encoded_name = base64.b64encode(self.player_name.encode('utf-8')) + '\n'.encode('ascii')
        rando_file.write(encoded_name)
        debug_file.write(f"Slot Name {encoded_name.decode('ascii')}")

        # locations = [x for x in all_locations if x.loc_type not in {LocationType.Event, LocationType.Djinn}]

        djinn_locs: List[GSTLALocation] = []
        index = 0
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                location_data = location_name_to_id.get(location.name, None)

                if location_data is None or location_data.loc_type == LocationType.Event:
                    continue
                ap_item = location.item
                if ap_item is None:
                    # TODO: need to fill with something else
                    continue

                if ap_item.player != self.player:
                    if ap_item.classification & (ItemClassification.progression | ItemClassification.trap) > 0:
                        item_data = AP_PROG_PLACEHOLDER_ITEM
                    elif ap_item.classification & ItemClassification.useful > 0:
                        item_data = AP_USEFUL_PLACEHOLDER_ITEM
                    else:
                        item_data = AP_PLACEHOLDER_ITEM
                else:
                    item_data = item_table[ap_item.name]

                if item_data.type == ItemType.Djinn:
                    djinn_locs.append(location)
                else:
                    item_id = item_data.id
                    rando_file.write(location_data.rando_flag.to_bytes(length=2, byteorder='little'))
                    rando_file.write(item_id.to_bytes(length=2, byteorder='little'))
                    debug_file.write(
                        f"{index} \n\tLocation: {location.name} \n\tLocation Flag: {hex(location_data.rando_flag)} \n\tItem: {location.item.name} \n\tItem ID: {item_id}\n\n")
                index += 1
                # debug_file.write()
                # TODO: Questions
                # Rando flags for summon tablets
                # Rando flags for psyenergy items
                # Rando flags for characters
                # Rando flags for djinn

        rando_file.write(0xFFFFFFFF.to_bytes(length=4, byteorder='little'))
        debug_file.write("0xFFFFFFFF\n")

        for loc in djinn_locs:
            item_data = item_table[loc.item.name]
            location_data = location_name_to_id[loc.name]
            rando_file.write(location_data.rando_flag.to_bytes(length=1, byteorder='little'))
            rando_file.write(item_data.get_rando_flag().to_bytes(length=1, byteorder='little'))
            loc_name = loc_names_by_id[location_data.ap_id]
            debug_file.write(
                f"Djinn(Location): {loc_name}\nDjinn(Location) Flag: {hex(location_data.rando_flag)}\nDjinn(Item): {item_data.name}\nDjinn(Item) Flag: {hex(item_data.get_rando_flag())}\n\n")

        rando_file.write(0xFFFF.to_bytes(length=2, byteorder='little'))
        debug_file.write("0xFFFF\n")

        if not self._character_levels:
            rando_file.write(0x0.to_bytes(length=7*2, byteorder='little'))
            debug_file.write("Did not scale character levels")
        else:
            for char, level in self._character_levels:
                rando_file.write(char.to_bytes(length=1, byteorder='little'))
                rando_file.write(level.to_bytes(length=1, byteorder='little'))
                debug_file.write(f"{name_by_item_id[char + 0xD00]} has starting level {level}\n")

    def _write_options_for_rando(self, rando_file: BinaryIO, debug_file: TextIO):
        write_me = 0
        write_me += self.options.item_shuffle << 6 #item-shuffle
        debug_file.write('Item Shuffle: ' + self.options.item_shuffle.name_lookup[self.options.item_shuffle] + '\n')
        write_me += self.options.omit_locations << 4 #omit
        debug_file.write('Omit Locations: ' + self.options.omit_locations.name_lookup[self.options.omit_locations] + '\n')
        write_me += self.options.add_elvenshirt_clericsring << 3 #gs-1items
        debug_file.write('GS1 Items: ' + self.options.add_elvenshirt_clericsring.name_lookup[self.options.add_elvenshirt_clericsring] + '\n')
        write_me += self.options.show_items_outside_chest << 2 #show-items
        debug_file.write('Visible Items: ' + self.options.show_items_outside_chest.name_lookup[self.options.show_items_outside_chest] + '\n')
        write_me += self.options.no_util_psynergy_from_classes << 1 #no-learning
        debug_file.write('No Learning Util: ' + self.options.no_util_psynergy_from_classes.name_lookup[self.options.no_util_psynergy_from_classes] + '\n')
        write_me += self.options.randomize_class_stat_boosts #class-stats
        debug_file.write('Class Stats Shuffle: ' + self.options.randomize_class_stat_boosts.name_lookup[self.options.randomize_class_stat_boosts] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.randomize_equip_compatibility << 7 #equip-shuffle
        debug_file.write('Equip Shuffle: ' + self.options.randomize_equip_compatibility.name_lookup[self.options.randomize_equip_compatibility] + '\n')
        write_me += self.options.adjust_equip_prices << 6 #equip-cost
        debug_file.write('Equip Prices: ' + self.options.adjust_equip_prices.name_lookup[self.options.adjust_equip_prices] + '\n')
        write_me += self.options.adjust_equip_stats << 5 #equip-stats
        debug_file.write('Equip Stats: ' + self.options.adjust_equip_stats.name_lookup[self.options.adjust_equip_stats] + '\n')
        #write_me += 0 << 4 #equip-sort, not supported, make weaker equipment appear earlier
        write_me += self.options.shuffle_weapon_effect << 3 #equip-unleash
        debug_file.write('Weapon Effects: ' + self.options.shuffle_weapon_effect.name_lookup[self.options.shuffle_weapon_effect] + '\n')
        write_me += self.options.shuffle_armour_effect << 2 #equip-effect
        debug_file.write('Armour Effects: ' + self.options.shuffle_armour_effect.name_lookup[self.options.shuffle_armour_effect] + '\n')
        write_me += self.options.randomize_curses << 1 #equip-curse
        debug_file.write('Shuffle Curses: ' + self.options.randomize_curses.name_lookup[self.options.randomize_curses] + '\n')
        write_me += self.options.adjust_psynergy_power #psynergy-power
        debug_file.write('Shuffle Psynergy Power: ' + self.options.adjust_psynergy_power.name_lookup[self.options.adjust_psynergy_power] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        if self.options.shuffle_djinn > 0: #djinn-shuffle
            write_me += 1 << 7
            debug_file.write('Shuffle Djinn: true\n')
        write_me += self.options.shuffle_djinn_stat_boosts << 6 #djinn-stats
        debug_file.write('Shuffle Djinn Stats: ' + self.options.shuffle_djinn_stat_boosts.name_lookup[self.options.shuffle_djinn_stat_boosts] + '\n')
        write_me += self.options.adjust_djinn_attack_power << 5 #djinn-power
        debug_file.write('Shuffle Djinn Power: ' + self.options.adjust_djinn_attack_power.name_lookup[self.options.adjust_djinn_attack_power] + '\n')
        write_me += self.options.randomize_djinn_attack_aoe << 4 #djinn-aoe
        debug_file.write('Shuffle Djinn Aoe: ' + self.options.randomize_djinn_attack_aoe.name_lookup[self.options.randomize_djinn_attack_aoe] + '\n')
        write_me += self.options.scale_djinni_battle_difficulty << 3 #djinn-scale
        debug_file.write('Scale Djinn: ' + self.options.scale_djinni_battle_difficulty.name_lookup[self.options.scale_djinni_battle_difficulty] + '\n')
        write_me += self.options.randomize_summon_costs << 2 #summon-cost
        debug_file.write('Shuffle Summon Costs: ' + self.options.randomize_summon_costs.name_lookup[self.options.randomize_summon_costs] + '\n')
        write_me += self.options.adjust_summon_power << 1 #summon-power
        debug_file.write('Shuffle Summon Power: ' + self.options.adjust_summon_power.name_lookup[self.options.adjust_summon_power] + '\n')
        #write_me += 0 #summon-sort, not supported, make cheaper summons appear earlier
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.character_stats << 6 #char-stats
        debug_file.write('Char Stats: ' + self.options.character_stats.name_lookup[self.options.character_stats] + '\n')
        write_me += self.options.character_elements << 4 #char-element
        debug_file.write('Char Element: ' + self.options.character_elements.name_lookup[self.options.character_elements] + '\n')
        write_me += self.options.adjust_psynergy_cost << 3 #psynergy-cost
        debug_file.write('Psnergy Cost: ' + self.options.adjust_psynergy_cost.name_lookup[self.options.adjust_psynergy_cost] + '\n')
        write_me += self.options.randomize_psynergy_aoe << 2 #psynergy-aoe
        debug_file.write('Psnergy AoE: ' + self.options.randomize_psynergy_aoe.name_lookup[self.options.randomize_psynergy_aoe] + '\n')
        write_me += self.options.adjust_enemy_psynergy_power << 1 #enemypsy-power
        debug_file.write('Enemy Psynergy Power: ' + self.options.adjust_enemy_psynergy_power.name_lookup[self.options.adjust_enemy_psynergy_power] + '\n')
        write_me += self.options.randomize_enemy_psynergy_aoe #enemypsy-aoe
        debug_file.write('Enemy Psynergy AoE: ' + self.options.randomize_enemy_psynergy_aoe.name_lookup[self.options.randomize_enemy_psynergy_aoe] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.class_psynergy << 5 #class-psynergy
        debug_file.write('Class Psynergy: ' + self.options.class_psynergy.name_lookup[self.options.class_psynergy] + '\n')
        write_me += self.options.psynergy_levels << 3 #class-levels
        debug_file.write('Class Levels: ' + self.options.psynergy_levels.name_lookup[self.options.psynergy_levels] + '\n')
        write_me += 1 << 2 #qol-cutscenes
        debug_file.write('QoL Cutscenes: true\n')
        write_me += 1 << 1 #qol-tickets
        debug_file.write('QoL Tickets: true\n')
        write_me += 1 #qol-fastship
        debug_file.write('QoL Fastship: true\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.lemurian_ship << 6 #ship
        debug_file.write('Starter Ship: ' + self.options.lemurian_ship.name_lookup[self.options.lemurian_ship] + '\n')
        #write_me += 0 << 5 #skips-basic, require logic changes
        debug_file.write('Skips Basic: false\n')
        #write_me += 0 << 4 #skips-oob-easy, require logic changes
        debug_file.write('Skips Oob Easy: false\n')
        #write_me += 0 << 3 #skips-maze, require logic changes
        debug_file.write('Skips Maze: false\n')
        if self.options.djinn_logic == 0:
            write_me += 1 << 2 #boss-logic, when we have no djinn logic we disable boss logic in base rando
            debug_file.write('Disable Boss Logic: true\n')
        write_me += self.options.free_avoid << 1 #free-avoid
        debug_file.write('Free Avoid: ' + self.options.free_avoid.name_lookup[self.options.free_avoid] + '\n')
        write_me += self.options.free_retreat #free-retreat
        debug_file.write('Free Retreat: ' + self.options.free_retreat.name_lookup[self.options.free_retreat] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))


        write_me = 0
        #write_me += 0 << 7 #adv-equip, not supported, requires AP to know shop artefact locations and forging locations
        debug_file.write('Adv Equip: false\n')        
        write_me += self.options.add_non_obtainable_items << 6 #dummy-items
        debug_file.write('Non Obtainabble Items: ' + self.options.add_non_obtainable_items.name_lookup[self.options.add_non_obtainable_items] + '\n')
        #write_me += 0 << 5 #skips-oob-hard, require logic changes
        debug_file.write('Skips Oob Hard: false\n')
        write_me += self.options.shuffle_weapon_attack << 4 #equip-attack
        debug_file.write('Equip Attack: ' + self.options.shuffle_weapon_attack.name_lookup[self.options.shuffle_weapon_attack] + '\n')
        #write_me += 0 << 3 #qol-hints, not supported yet
        debug_file.write('QoL Hints: false\n')
        write_me += self.options.start_with_healing_psynergy << 2 #start-heal
        debug_file.write('Start Heal: ' + self.options.start_with_healing_psynergy.name_lookup[self.options.start_with_healing_psynergy] + '\n')
        write_me += self.options.start_with_revive << 1 #start-revive
        debug_file.write('Start Revive: ' + self.options.start_with_revive.name_lookup[self.options.start_with_revive] + '\n')

        if ItemName.Reveal.name in self.options.start_inventory or ItemName.Reveal.name in self.options.start_inventory_from_pool:
            write_me += 1 #start-reveal
            debug_file.write('Start Reveal: true\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))


        write_me = 0
        write_me += self.options.scale_exp << 4 #scale-exp
        debug_file.write('Scale Exp: ' + str(self.options.scale_exp) + '\n')
        write_me += self.options.scale_coins #scale-coins
        debug_file.write('Scale Coins: ' + str(self.options.scale_coins) + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.shuffle_armour_defense << 7 #equip-defense
        debug_file.write('Equip Defense: ' + self.options.shuffle_armour_defense.name_lookup[self.options.shuffle_armour_defense] + '\n')
        write_me += self.options.starting_levels #start-levels
        debug_file.write('Start Levels: ' + str(self.options.starting_levels) + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.enemy_elemental_resistance << 6 #enemy-eres
        debug_file.write('Enemy ERes: ' + self.options.enemy_elemental_resistance.name_lookup[self.options.enemy_elemental_resistance] + '\n')
        write_me += self.options.sanctum_revive_cost << 4 #sanc-revive
        debug_file.write('Sanc Revive ' + self.options.sanctum_revive_cost.name_lookup[self.options.sanctum_revive_cost] + '\n')
        write_me += self.options.remove_all_curses << 3 #curse-disable
        debug_file.write('Curse Disabled: ' + self.options.remove_all_curses.name_lookup[self.options.remove_all_curses] + '\n')
        write_me += self.options.avoid_always_works << 2 #avoid-patch
        debug_file.write('Avoid Patch: ' + self.options.avoid_always_works.name_lookup[self.options.avoid_always_works] + '\n')
        #write_me += 0 << 1 #retreat-patch, does nothing in base rando
        #debug_file.write('Retreat Patch: false\n')
        #write_me += 0 #teleport-patch, does nothing in base rando
        #debug_file.write('Teleport Patch: false\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.enable_hard_mode << 7 #hard-mode
        debug_file.write('Hard Mode: ' + self.options.enable_hard_mode.name_lookup[self.options.enable_hard_mode] + '\n')
        write_me += self.options.reduced_encounter_rate << 6 #halve-enc
        debug_file.write('Halve Encounter Rate: ' + self.options.reduced_encounter_rate.name_lookup[self.options.reduced_encounter_rate] + '\n')
        write_me += self.options.major_minor_split << 5 #major-shuffle
        debug_file.write('Major Minor Split: ' + self.options.major_minor_split.name_lookup[self.options.major_minor_split] + '\n')
        write_me += self.options.easier_bosses << 4 #easier-bosses
        debug_file.write('Easier Bosses: ' + self.options.easier_bosses.name_lookup[self.options.easier_bosses] + '\n')
        if self.options.name_puzzles == 2:
            write_me += 1 << 3 #random-puzzles
            debug_file.write('Name puzzles: ' + self.options.name_puzzles.name_lookup[self.options.name_puzzles] + '\n')
        elif self.options.name_puzzles == 1:
            write_me += 1 << 2 #fixed-puzzles
            debug_file.write('Name puzzles: ' + self.options.name_puzzles.name_lookup[self.options.name_puzzles] + '\n')
        write_me += self.options.manual_retreat_glitch << 1 #manual-rg
        debug_file.write('Manual Retreat glitch: ' + self.options.manual_retreat_glitch.name_lookup[self.options.manual_retreat_glitch] + '\n')
        write_me += self.options.start_with_wings_of_anemos #ship-wings
        debug_file.write('Ship wings: ' + self.options.start_with_wings_of_anemos.name_lookup[self.options.start_with_wings_of_anemos] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.shuffle_music << 7 #music-shuffle
        debug_file.write('Music Shuffle: ' + self.options.shuffle_music.name_lookup[self.options.shuffle_music] + '\n')
        write_me += self.options.teleport_to_dungeons_and_towns << 6 #teleport-everywhere
        debug_file.write('Teleport Everywhere: ' + self.options.teleport_to_dungeons_and_towns.name_lookup[self.options.teleport_to_dungeons_and_towns] + '\n')
        #write_me += self.options.force_boss_required_checks_to_nonjunk << 5 #force-boss-drops, this can be done in just AP as is already
        debug_file.write('Force boss drops: false\n')
        #write_me += self.options.prevent_superboss_locked_check_to_progression << 4 #force-superboss-minors, this can be done in just AP as is already
        debug_file.write('Force superboss minor: false\n')
        write_me += self.options.anemos_inner_sanctum_access << 2 #anemos-access, require logic changes
        debug_file.write('Anemos Inner Sanctum Access: ' + self.options.anemos_inner_sanctum_access.name_lookup[self.options.anemos_inner_sanctum_access] + '\n')
        write_me += 1 << 1 #char shuffle always on to ensure game understands character items in case of players creating duplicates / plando in weird places
        debug_file.write('Character Shuffle: true\n')
        write_me += 0 #unused
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        # Placeholder in case we need more flags
        rando_file.write(write_me.to_bytes(length=4, byteorder='big'))

    def create_item(self, name: str) -> "Item":
        return create_item(name, self.player)

    def get_location(self, location_name: str) -> GSTLALocation:
        return cast(GSTLALocation, super().get_location(location_name))