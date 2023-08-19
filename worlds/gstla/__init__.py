from worlds.AutoWorld import WebWorld, World
import os

from typing import List

from .Options import GSTLAOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType, create_events, create_items, pre_fillitems, create_item
from .Locations import GSTLALocation, all_locations, location_name_to_id, LocationType, location_type_to_data
from .Rules import set_access_rules, set_item_rules, set_entrance_rules
from .Regions import create_regions
from .Connections import create_connections
from .Names.ItemName import ItemName
from .Names.LocationName import LocationName
from .Names.RegionName import RegionName
from .Rom import get_base_rom_path, get_base_rom_bytes, LocalRom, GSTLADeltaPatch


class GSTLAWeb(WebWorld):
    theme = "jungle"


class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    option_definitions = GSTLAOptions
    data_version = 1

    item_name_to_id = {item.itemName: item.ap_id for item in all_items if item.type != ItemType.Event}
    location_name_to_id = {location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn: {item.itemName for item in all_items if item.type == ItemType.Djinn}
    }

    def generate_early(self) -> None:
        self.multiworld.non_local_items[self.player].value -= self.item_name_groups[ItemType.Djinn]

        if self.multiworld.starter_ship[self.player] == 0:
            self.multiworld.start_inventory[self.player].value[ "Ship" ] = 1

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
            locs.append(self.multiworld.get_location(loc.name, self.player))

        djinnList = self.get_prefill_items()
        self.multiworld.random.shuffle(locs)
        self.multiworld.random.shuffle(djinnList)

        for ap_item in djinnList:
            all_state.remove(ap_item)

        fill_restrictive(self.multiworld, all_state, locs, djinnList, True, True)

    def generate_output(self, output_directory: str):
        rom = LocalRom(get_base_rom_path())
        world = self.multiworld
        player = self.player

        rom.write_story_flags()
        rom.apply_qol_patches()

        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                if location.event:
                    continue

                location_data = location_name_to_id[location.name]
                ap_item = location.item

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

    def create_item(self, name: str) -> "Item":
        return create_item(name, self.player)