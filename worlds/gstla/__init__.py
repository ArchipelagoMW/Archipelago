from worlds.AutoWorld import WebWorld, World
import os

from typing import List, Dict

from .Options import GSTLAOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType, create_events, create_items, pre_fillitems, create_item, \
    AP_PLACEHOLDER_ITEM, items_by_id
from .Locations import GSTLALocation, all_locations, location_name_to_id, location_type_to_data
from .Rules import set_access_rules, set_item_rules, set_entrance_rules
from .Regions import create_regions
from .Connections import create_connections
from .gen.LocationData import LocationType
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
        ItemType.Djinn.name: {item.name for item in all_items if item.type == ItemType.Djinn},
        ItemType.Character.name: {item.name for item in all_items if item.type == ItemType.Character}
    }

    def generate_early(self) -> None:
        self.multiworld.non_local_items[self.player].value -= self.item_name_groups[ItemType.Djinn.name]

        if self.multiworld.character_shuffle[self.player] > 0:
            self.multiworld.non_local_items[self.player].value -= self.item_name_groups[ItemType.Character.name]

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

    def get_prefill_items(self) -> Dict[str, List["Item"]]:
        return pre_fillitems

    def pre_fill(self) -> None:
        from Fill import fill_restrictive, FillError
        all_state = self.multiworld.get_all_state(use_cache=False)
        locs = []

        for loc in location_type_to_data[LocationType.Djinn]:
            locs.append(self.multiworld.get_location(loc_names_by_id[loc.ap_id], self.player))

        prefill_items_collection = self.get_prefill_items()
        prefill_items = prefill_items_collection[ItemType.Djinn.name]
        assert len(locs) == len(prefill_items), "Djinn Locations: %d, Djinn: %d" % (len(locs), len(prefill_items))
        self.multiworld.random.shuffle(locs)
        self.multiworld.random.shuffle(prefill_items)

        for ap_item in prefill_items:
            all_state.remove(ap_item)
        # print(len(locs))
        # print(locs)
        # for loc_name in LocationName:
        #     try:
        #         self.multiworld.get_location(loc_name, self.player)
        #     except:
        #         print("Failed to find location in multiworld: " + loc_name)
        fill_restrictive(self.multiworld, all_state, locs, prefill_items, True, True)


        prefill_items = prefill_items_collection[ItemType.Character.name]
        for ap_item in prefill_items:
            all_state.remove(ap_item)

        if self.multiworld.character_shuffle[self.player] == 2:
            for character in prefill_items:
                if character.name == ItemName.Jenna:
                    vanilla_location = self.multiworld.get_location(LocationName.Idejima_Jenna, self.player)
                if character.name == ItemName.Sheba:
                    vanilla_location = self.multiworld.get_location(LocationName.Idejima_Sheba, self.player)
                if character.name == ItemName.Piers:
                    vanilla_location = self.multiworld.get_location(LocationName.Kibombo_Piers, self.player)
                if character.name == ItemName.Isaac:
                    vanilla_location = self.multiworld.get_location(LocationName.Contigo_Isaac, self.player)
                if character.name == ItemName.Garet:
                    vanilla_location = self.multiworld.get_location(LocationName.Contigo_Garet, self.player)
                if character.name == ItemName.Ivan:
                    vanilla_location = self.multiworld.get_location(LocationName.Contigo_Ivan, self.player)
                if character.name == ItemName.Mia:
                    vanilla_location = self.multiworld.get_location(LocationName.Contigo_Mia, self.player)

                vanilla_location.place_locked_item(character)

        else:   
            locs = []

            for loc in location_type_to_data[LocationType.Character]:
                loc_name = loc_names_by_id[loc.ap_id]
                ap_location = self.multiworld.get_location(loc_name, self.player)
                if loc_name == LocationName.Idejima_Jenna:
                    character = self.random.choice(prefill_items)
                    ap_location.place_locked_item(character)
                    prefill_items.remove(character)
                else:
                    locs.append(ap_location)

            if self.multiworld.character_shuffle[self.player] == 1:
                for ap_item in prefill_items:
                    all_state.remove(ap_item)

                assert len(locs) == len(prefill_items), "Character Locations: %d, Djinn: %d" % (len(locs), len(prefill_items))
                fill_restrictive(self.multiworld, all_state, locs, prefill_items, True, True)
            else:
                for item in prefill_items:
                    self.multiworld.itempool.append(item)




    def generate_output(self, output_directory: str):
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

    def create_item(self, name: str) -> "Item":
        return create_item(name, self.player)

