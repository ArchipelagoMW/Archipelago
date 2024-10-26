from worlds.AutoWorld import WebWorld, World
import os

from typing import List, TextIO, BinaryIO

from .Options import GSTLAOptions, RandoOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType, create_events, create_items, pre_fillitems, create_item, \
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
from worlds.LauncherComponents import Component, components, Type, launch_subprocess, SuffixIdentifier


# TODO: point at BHC
# def launch_client():
#     from .Client import launch
#     launch_subprocess(launch, name="GSTLAClient")


# components.append(Component("Golden Sun The Lost Age Client", "GSTLAClient", func=launch_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apgstla")))

class GSTLAWeb(WebWorld):
    theme = "jungle"

class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    option_definitions = GSTLAOptions
    data_version = 1
    items_ids_populated = set()
    location_flags_populated = set()

    item_name_to_id = item_id_by_name#{item.itemName: itemfor item in all_items if item.type != ItemType.Event}
    location_name_to_id = ids_by_loc_name#{location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn.name: {item.name for item in all_items if item.type == ItemType.Djinn}
    }

    def generate_early(self) -> None:
        self.multiworld.non_local_items[self.player].value -= self.item_name_groups[ItemType.Djinn.name]

        if self.multiworld.starter_ship[self.player] == 0:
            self.multiworld.start_inventory[self.player].value[ ItemName.Ship ] = 1

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)
        create_connections(self.multiworld, self.player)

    def create_items(self) -> None:
        create_events(self.multiworld, self.player)
        create_items(self.multiworld, self.player)

    def set_rules(self) -> None:
        set_entrance_rules(self.multiworld, self.player)
        set_item_rules(self.multiworld, self.player)
        set_access_rules(self.multiworld, self.player)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def generate_basic(self):
        pass

    def get_prefill_items(self) -> List["Item"]:
        return pre_fillitems

    def pre_fill(self) -> None:
        from Fill import fill_restrictive, FillError
        all_state = self.multiworld.get_all_state(use_cache=False)
        locs = []

        for loc in location_type_to_data[LocationType.Djinn]:
            locs.append(self.multiworld.get_location(loc_names_by_id[loc.ap_id], self.player))

        djinnList = self.get_prefill_items()
        assert len(locs) == len(djinnList), "Djinn Locations: %d, Djinn: %d" % (len(locs), len(djinnList))
        self.multiworld.random.shuffle(locs)
        self.multiworld.random.shuffle(djinnList)

        for ap_item in djinnList:
            all_state.remove(ap_item)
        # print(len(locs))
        # print(locs)
        # for loc_name in LocationName:
        #     try:
        #         self.multiworld.get_location(loc_name, self.player)
        #     except:
        #         print("Failed to find location in multiworld: " + loc_name)
        fill_restrictive(self.multiworld, all_state, locs, djinnList, True, True)

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

                if location_data is None or location_data.loc_type == LocationType.Event:
                    continue
                ap_item = location.item
                # print(ap_item)
                if ap_item is None:
                    # TODO: need to fill with something else
                    continue

                item_data = item_table.get(ap_item.name, AP_PLACEHOLDER_ITEM)
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

    def _generate_rando_file(self, output_directory: str):
        with open(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}_debug.txt"),'w') as debug_file:
            with open(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gstlarando"),'wb') as rando_file:
                rando_file.write(0x1.to_bytes(length=1,byteorder='little'))
                debug_file.write("Version: 1\n")

                rando_file.write(self.multiworld.seed.to_bytes(length=16,byteorder='little'))
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

                        item_data = item_table.get(ap_item.name, AP_PLACEHOLDER_ITEM)
                        if item_data.type == ItemType.Djinn:
                            djinn_locs.append(location)
                        else:
                            # rom.write_item(location_data, item_data)
                            # TODO: cleanup
                            item_id = 0xA00 if item_data.id == 412 else item_data.id
                            rando_file.write(location_data.rando_flag.to_bytes(length=2, byteorder='little'))
                            rando_file.write(item_id.to_bytes(length=2, byteorder='little'))
                            debug_file.write(f"{index} \n\tLocation: {location.name.value} \n\tLocation Flag: {hex(location_data.rando_flag)} \n\tItem: {location.item.name} \n\tItem ID: {item_id}\n\n")
                        index += 1
                        # debug_file.write()
                        #TODO: Questions
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
                    rando_file.write(item_data.get_rando_flag().to_bytes(length=2,byteorder='little'))
                    loc_name = loc_names_by_id[location_data.ap_id]
                    debug_file.write(f"Djinn(Location): {loc_name}\nDjinn(Location) Flag: {hex(location_data.rando_flag)}\nDjinn(Item): {item_data.name}\nDjinn(Item) Flag: {hex(item_data.get_rando_flag())}\n\n")


    def _write_options_for_rando(self, rando_file: BinaryIO, debug_file: TextIO):
        write_me = 0
        hidden = self.options.hidden_items
        if hidden == 2:
            write_me |= RandoOptions.ItemShufTreas.bit_flag
            debug_file.write(RandoOptions.ItemShufTreas.name + '\n')
        else:
            write_me |= RandoOptions.ItemShufAll.bit_flag
            debug_file.write(RandoOptions.ItemShufAll.name + '\n')

        super = self.options.super_bosses

        if super == 0:
            write_me |= RandoOptions.OmitSuper.bit_flag | RandoOptions.OmitAnemos.bit_flag
            debug_file.write(RandoOptions.OmitSuper.name + '\n')
            debug_file.write(RandoOptions.OmitAnemos.name + '\n')
        elif super == 1:
            write_me |= RandoOptions.OmitAnemos.bit_flag
            debug_file.write(RandoOptions.OmitAnemos.name + '\n')

        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Equip not a thing
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Djinn/Summon
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Char Stat/Enemy Psy Shuffle
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Psy/Qol
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        #Ship/Skips
        ship = self.options.starter_ship
        if ship == 0:
            write_me |= RandoOptions.ShipFromStart.bit_flag
            debug_file.write(RandoOptions.ShipFromStart.name + '\n')
        elif ship == 1:
            write_me |= RandoOptions.ShipUnlock.bit_flag
            debug_file.write(RandoOptions.ShipUnlock.name + '\n')

        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # More QoL
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Scale Exp/Coins
        write_me = 0b00010001
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # More QoL
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Speedstuffs
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

        # Misc
        rando_file.write(write_me.to_bytes(length=1))
        write_me = 0

    def create_item(self, name: str) -> "Item":
        return create_item(name, self.player)

