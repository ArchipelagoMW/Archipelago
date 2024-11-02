from __future__ import annotations

from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
import os

from typing import List, TextIO, BinaryIO, Dict, ClassVar, Type, cast

from .Options import GSTLAOptions, RandoOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType, create_events, create_items, create_item, \
    AP_PLACEHOLDER_ITEM, items_by_id
from .Locations import GSTLALocation, all_locations, location_name_to_id, location_type_to_data
from .Rules import set_access_rules, set_item_rules, set_entrance_rules
from .Regions import create_regions
from .Connections import create_connections
from .gen.LocationData import LocationType, location_name_to_data
from .gen.ItemNames import ItemName, item_id_by_name
from .gen.LocationNames import LocationName, ids_by_loc_name, loc_names_by_id
from .Names.RegionName import RegionName
from .Rom import get_base_rom_path, get_base_rom_bytes, LocalRom, GSTLADeltaPatch
from .BizClient import GSTLAClient

import logging

class GSTLAWeb(WebWorld):
    theme = "jungle"

class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = GSTLAOptions
    options: GSTLAOptions
    data_version = 1
    items_ids_populated = set()
    location_flags_populated = set()

    item_name_to_id = item_id_by_name#{item.itemName: itemfor item in all_items if item.type != ItemType.Event}
    location_name_to_id = ids_by_loc_name#{location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn.name: {item.name for item in all_items if item.type == ItemType.Djinn},
        ItemType.Character.name: {item.name for item in all_items if item.type == ItemType.Character}
    }

    def generate_early(self) -> None:
        self.options.non_local_items.value -= self.item_name_groups[ItemType.Djinn.name]

        if self.options.character_shuffle < 2:
            self.options.non_local_items.value -= self.item_name_groups[ItemType.Character.name]

        if self.options.starter_ship == 2:
            self.options.start_inventory.value[ ItemName.Ship ] = 1

        #force unsupported options to off
        self.options.gs1_items = 0

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

    def generate_basic(self):
        pass

    def pre_fill(self) -> None:
        pass

    def generate_output(self, output_directory: str):
        self._generate_rando_file(output_directory)
        rom = LocalRom(get_base_rom_path())
        world = self.multiworld
        player = self.player

        rom.write_story_flags()
        rom.apply_qol_patches()

        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                location_data = location_name_to_id.get(location.name, None)

                if location_data is None or location_data.loc_type == LocationType.Event or location_data.loc_type == LocationType.Character:
                    continue
                ap_item = location.item
                # print(ap_item)
                if ap_item is None:
                    # TODO: need to fill with something else
                    continue

                if ap_item.player != self.player:
                    item_data = AP_PLACEHOLDER_ITEM
                else:
                    item_data = item_table[ap_item.name]

                if item_data.type == ItemType.Djinn:
                    rom.write_djinn(location_data, item_data)
                else:
                    rom.write_item(location_data, item_data)

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gba")

        try:
            rom.write_to_file(rompath)
            patch = GSTLADeltaPatch(os.path.splitext(rompath)[0]+GSTLADeltaPatch.patch_file_ending, player=player,
                        player_name=world.player_name[player], patched_path=rompath)

            patch.write()
        except:
            raise()
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)

    def _generate_rando_data(self, rando_file: BinaryIO, debug_file: TextIO):
        rando_file.write(0x1.to_bytes(length=1, byteorder='little'))
        debug_file.write("Version: 1\n")

        rando_file.write(self.multiworld.seed.to_bytes(length=16, byteorder='little'))
        debug_file.write(f"Seed: {self.multiworld.seed}\n")

        self._write_options_for_rando(rando_file, debug_file)

        # rando_file.write((0).to_bytes(length=16, byteorder='little'))
        # debug_file.write("no settings (TBD)\n")

        rando_file.write(f"{self.player_name}\n".encode('ascii'))
        debug_file.write(f"Slot Name {self.player_name.encode('ascii')}\n")

        # locations = [x for x in all_locations if x.loc_type not in {LocationType.Event, LocationType.Djinn}]

        djinn_locs: List[GSTLALocation] = []
        index = 0
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                location_data = location_name_to_id.get(location.name, None)

                if location_data is None or location_data.loc_type == LocationType.Event:
                    continue
                ap_item = location.item
                # print(ap_item)
                if ap_item is None:
                    # TODO: need to fill with something else
                    continue

                if ap_item.player != self.player:
                    item_data = AP_PLACEHOLDER_ITEM
                else:
                    item_data = item_table[ap_item.name]

                if item_data.type == ItemType.Djinn:
                    djinn_locs.append(location)
                else:
                    # rom.write_item(location_data, item_data)
                    # TODO: cleanup
                    item_id = 0xA00 if item_data.id == 412 else item_data.id
                    rando_file.write(location_data.rando_flag.to_bytes(length=2, byteorder='little'))
                    rando_file.write(item_id.to_bytes(length=2, byteorder='little'))
                    debug_file.write(
                        f"{index} \n\tLocation: {location.name.value} \n\tLocation Flag: {hex(location_data.rando_flag)} \n\tItem: {location.item.name} \n\tItem ID: {item_id}\n\n")
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
            rando_file.write(location_data.rando_flag.to_bytes(length=2, byteorder='little'))
            rando_file.write(item_data.get_rando_flag().to_bytes(length=2, byteorder='little'))
            loc_name = loc_names_by_id[location_data.ap_id]
            debug_file.write(
                f"Djinn(Location): {loc_name}\nDjinn(Location) Flag: {hex(location_data.rando_flag)}\nDjinn(Item): {item_data.name}\nDjinn(Item) Flag: {hex(item_data.get_rando_flag())}\n\n")

    def _generate_rando_file(self, output_directory: str):
        with open(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}_debug.txt"),'w') as debug_file:
            with open(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gstlarando"),'wb') as rando_file:
                self._generate_rando_data(rando_file, debug_file)

    def _write_options_for_rando(self, rando_file: BinaryIO, debug_file: TextIO):
        write_me = 0
        write_me += self.options.item_shuffle << 6 #item-shuffle
        debug_file.write('Item Shuffle: ' + self.options.item_shuffle.name_lookup[self.options.item_shuffle] + '\n')
        write_me += self.options.omit_locations << 4 #omit
        debug_file.write('Omit Locations: ' + self.options.omit_locations.name_lookup[self.options.omit_locations] + '\n')
        write_me += self.options.gs1_items << 3 #gs-1items
        debug_file.write('GS1 Items: ' + self.options.gs1_items.name_lookup[self.options.gs1_items] + '\n')
        write_me += self.options.visible_items << 2 #show-items
        debug_file.write('Visible Items: ' + self.options.visible_items.name_lookup[self.options.visible_items] + '\n')
        write_me += self.options.no_learning_util << 1 #no-learning
        debug_file.write('No Learning Util: ' + self.options.no_learning_util.name_lookup[self.options.no_learning_util] + '\n')
        write_me += self.options.shuffle_class_stats #class-stats
        debug_file.write('Class Stats Shuffle: ' + self.options.shuffle_class_stats.name_lookup[self.options.shuffle_class_stats] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += 0 << 7 #equip-shuffle
        write_me += 0 << 6 #equip-cose
        write_me += 0 << 5 #equip-stats
        write_me += 0 << 4 #equip-sort, unsupported
        write_me += 0 << 3 #equip-unleash
        write_me += 0 << 2 #equip-effect
        write_me += 0 << 1 #equip-curse
        write_me += 0 #psynergy-power
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        if self.options.djinn_shuffle > 0: #djinn-shuffle
            write_me += self.options.djinn_shuffle << 7
        write_me += 0 << 6 #djinn-stats
        write_me += 0 << 5 #djinn-power
        write_me += 0 << 4 #djinn-aoe
        write_me += 0 << 3 #djinn-scale
        write_me += 0 << 2 #summon-cost
        write_me += 0 << 1 #summon-power
        write_me += 0 #summon-sort, unsupported
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))


        write_me = 0
        write_me += 0 << 6 #char-stats
        write_me += 0 << 4 #char-element
        write_me += 0 << 3 #psynergy-cost
        write_me += 0 << 2 #psynergy-aoe
        write_me += 0 << 1 #enemypsy-power
        write_me += 0 #enemypsy-aoe
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += 0 << 5 #class-psynergy
        write_me += 0 << 3 #class-levels
        write_me += 0 << 2 #qol-cutscenes
        write_me += 0 << 1 #qol-tickets
        write_me += 0 #qol-fastship
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += self.options.starter_ship << 6 #ship
        write_me += 0 << 5 #skips-basic
        write_me += 0 << 4 #skips-oob-easy
        write_me += 0 << 3 #skips-maze
        write_me += 0 << 2 #boss-logic
        write_me += 0 << 1 #free-avoid
        write_me += 0 #free-retreat
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))


        write_me = 0
        write_me += 0 << 7 #adv-equip
        write_me += 0 << 6 #dummy-items
        write_me += 0 << 5 #skips-oob-hard
        write_me += 0 << 4 #equip-attack
        write_me += 0 << 3 #qol-hints
        write_me += 0 << 2 #start-heal
        write_me += 0 << 1 #start-revive
        write_me += 0 #start-reveal
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))


        write_me = 0
        write_me += 0 << 4 #scale-exp
        write_me += 0 #scale-coins
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += 0 << 7 #equip-defense
        write_me += 0 #start-levels
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += 0 << 6 #enemy-eres
        write_me += 0 << 4 #sanc-revive
        write_me += 0 << 3 #curse-disable
        write_me += 0 << 2 #avoid-patch
        write_me += 0 << 1 #retreat-patch, does nothing in base rando
        write_me += 0 #teleport-patch
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += 0 << 7 #hard-mode
        write_me += 0 << 6 #halve-enc
        write_me += 0 << 5 #major-shuffle
        write_me += 0 << 4 #easier-bosses
        write_me += 0 << 3 #random-puzzles
        write_me += 0 << 2 #fixed-puzzles
        write_me += 0 << 1 #manual-rg
        write_me += 0 #ship-wings
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        write_me += 0 << 7 #music-shuffle
        write_me += 0 << 6 #teleport-everywhere
        write_me += 0 << 5 #force-boss-drops
        write_me += 0 << 4 #force-superboss-minors
        write_me += 0 << 2 #anemos-access
        if self.options.character_shuffle > 0: #shuffle-characters
            write_me += 1 << 1
        write_me += 0 #unused
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0
        # Placeholder in case we need more flags
        rando_file.write(write_me.to_bytes(length=4, byteorder='big'))

    def create_item(self, name: str) -> "Item":
        return create_item(name, self.player)

    def get_location(self, location_name: str) -> GSTLALocation:
        return cast(GSTLALocation, super().get_location(location_name))