from worlds.AutoWorld import WebWorld, World
import os

from typing import List

from .Options import GSTLAOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType
from .Locations import GSTLALocation, all_locations, location_name_to_id, LocationType, location_type_to_data
from .Rules import set_access_rules, set_item_rules
from .Regions import create_regions
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
    djinnlist = []

    item_name_to_id = {item.itemName: item.ap_id for item in all_items if item.type != ItemType.Event}
    location_name_to_id = {location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn: {item.itemName for item in all_items if item.type == ItemType.Djinn}
    }


    def generate_early(self) -> None:
        self.multiworld.non_local_items[self.player].value -= self.item_name_groups[ItemType.Djinn]
        self.multiworld.start_inventory[self.player].value[ "Ship" ] = 1



    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)


    def create_items(self) -> None:
        for location in all_locations:
            if location.event:
                ap_item = self.create_event(location.vanilla_item)
                ap_location = self.multiworld.get_location(location.name, self.player)
                ap_location.place_locked_item(ap_item)
                continue

            ap_item = self.create_item(location.vanilla_item)
            if location.loc_type == LocationType.Djinn:
                self.djinnlist.append(ap_item)
            else:
                self.multiworld.itempool.append(ap_item)

        self.multiworld.push_precollected(self.create_event(ItemName.Ship))



    def set_rules(self) -> None:
        set_item_rules(self.multiworld, self.player)
        set_access_rules(self.multiworld, self.player)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def generate_basic(self):
        pass

    def get_pre_fill_items(self) -> List["Item"]:
        return self.djinnlist

    def pre_fill(self) -> None:
        from Fill import fill_restrictive, FillError
        all_state = self.multiworld.get_all_state(use_cache=False)
        locs = []

        for loc in location_type_to_data[LocationType.Djinn]:
            locs.append(self.multiworld.get_location(loc.name, self.player))

        self.multiworld.random.shuffle(locs)
        self.multiworld.random.shuffle(self.djinnlist)

        for ap_item in self.djinnlist:
            all_state.remove(ap_item)

        fill_restrictive(self.multiworld, all_state, locs, self.djinnlist, True, True)

    def generate_output(self, output_directory: str):
        rom = LocalRom(get_base_rom_path())
        world = self.multiworld
        player = self.player

        rom.write_story_flags()
        rom.apply_qol_patches()

        locations = location_name_to_id
        for location in locations:
            ap_location = world.get_location(location, player)
            location_data = location_name_to_id[location]
            ap_item = ap_location.item

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
        item = item_table[name]
        return GSTLAItem(item.itemName, item.progression, item.ap_id, self.player)

    def create_event(self, event: str):
        return GSTLAItem(event, ItemClassification.progression, None, self.player)