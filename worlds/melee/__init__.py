import os
import typing
import threading
import pkgutil
import json
import base64
import logging


from typing import List, Set, Dict, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, filler_item_table, item_table
from .Locations import get_locations
from .Regions import init_areas
from .Options import SSBMOptions, ssbm_option_groups
from .Rules import set_location_rules
from .Rom import apply_patch, MeleePlayerContainer
from .static_location_data import location_ids
from .setup_game import setup_gamevars, place_static_items, calculate_trophy_based_locations
from .in_game_data import global_trophy_table
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths

def run_client(*args):
    print("Running SSBM Client")
    from .Client import launch
    launch_subprocess(launch, name="SSBMClient", args=args)

components.append(
    Component("Super Smash Bros. Melee Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apssbm"))
)


class SSBMWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Melee randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

    option_groups = ssbm_option_groups


class SSBMWorld(World):
    """Bottom text"""
    
    game = "Super Smash Bros. Melee"
    option_definitions = SSBMOptions
    data_version = 1
    required_client_version = (0, 6, 1)
    origin_region_name = "Game Base"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()

    web = SSBMWeb()
    # topology_present = True

#    @staticmethod
 #   def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
  #      return slot_data

   # ut_can_gen_without_yaml = True

    #tracker_world: ClassVar = {
     #   "map_page_folder": "ut_map_page",
      #  "map_page_maps": "maps.json",
       # "map_page_locations": "locations.json",
        #"map_page_setting_key": "{player}_{team}_nine_sols_area",
        #"map_page_index": map_page_index
    #}

    options_dataclass = SSBMOptions
    options: SSBMOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.world_version = "1.1"
        self.extra_item_count = 0
        self.goal_count = 1
        self.picked_trophies = set()
        self.all_trophies = global_trophy_table.copy()
        self.all_adventure_trophies = False
        self.all_classic_trophies = False
        self.all_allstar_trophies = False
        self.location_count = 287
        self.required_item_count = 55

    def create_regions(self) -> None:
        for item in self.multiworld.precollected_items[self.player]: #First add starting inventories to the Trophy Pool
            if item.name in global_trophy_table:
                self.picked_trophies.add(item.name)

        calculate_trophy_based_locations(self) #Check if the current Trophy Pool will affect the location pool
        excess_trophies = len(self.picked_trophies) - (self.location_count - self.required_item_count)

        if excess_trophies > 0:
            logging.warning(f"""Warning: {self.multiworld.get_player_name(self.player)}'s generated Trophy Count is higher than the number of locations and required items.
                    Your Trophy counts have automatically been lowered as necessary.""")

        #TODO; slice and shuffle this i guess? dont get it
        for i in range(excess_trophies):
            self.removed_list = sorted(self.picked_trophies)
            self.picked_trophies.remove(self.random.choice(self.removed_list))
            if self.options.extra_trophies:
                self.options.extra_trophies.value -= 1
            else:
                self.options.trophies_required.value -= 1


        calculate_trophy_based_locations(self) # If the Trophy Pool was adjusted, recalculate this to remove the locations

        for trophy in self.picked_trophies:
            if trophy not in self.multiworld.precollected_items[self.player]: #Don't create any extra trophies
                self.multiworld.itempool.append(self.create_item(trophy))
            self.extra_item_count += 1

        init_areas(self, get_locations(self))
        place_static_items(self)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())
        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Sense of Accomplishment', self.player, self.goal_count)

    def generate_early(self):
        setup_gamevars(self)
        
        self.authentication_id = self.random.getrandbits(32)

    def generate_output(self, output_directory: str) -> None:
        from Main import __version__
        try:
            basepatch = pkgutil.get_data(__name__, "melee_base.xml")
            base_str = basepatch.decode("utf-8")
            self.encoded_slot_name = bytearray(f'SSBM{__version__.replace(".", "")[0:3]}_{self.player:05d}_{self.authentication_id:09d}\0', "utf8")[:27]
            self.rom_name = self.encoded_slot_name.decode("ascii").rstrip("\x00")
            self.encoded_slot_name = ''.join(f'{b:02X}' for b in self.encoded_slot_name)

            output_patch = apply_patch(self, base_str, output_directory)
            output_file_path = os.path.join(output_directory, f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}.zip")
            #with open(output_file_path, "w") as file:
                #file.write(output_patch)
            patch_name = f"{self.multiworld.get_out_file_name_base(self.player)}"
            melee_container = MeleePlayerContainer(output_patch, output_file_path,
                self.multiworld.player_name[self.player], self.player, patch_name)
            melee_container.write()

        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()


    def fill_slot_data(self) -> Dict[str, typing.Any]:
        if self.options.lottery_pool_mode == 2:
            lottery_type = "Static"
        elif self.options.lottery_pool_mode == 1:
            lottery_type = "Progressive"
        else:
            lottery_type = "N/A"

        return {
            "authentication_id": self.authentication_id,
            "giga_bowser_required": self.options.goal_giga_bowser.value,
            "crazy_hand_required": self.options.goal_crazy_hand.value,
            "goal_evn_51": self.options.goal_event_51.value,
            "goal_all_events": self.options.goal_all_events.value,
            "targets_required": self.options.goal_all_targets.value,
            "total_trophies_required": self.options.trophies_required.value,
            "lottery_pool_mode": lottery_type
        }

    def modify_multidata(self, multidata: dict) -> None:
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            multidata["connect_names"][self.rom_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:  #
        return self.random.choice(filler_item_table)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add(self.starting_character)
        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.extra_item_count):  # Change to fix event count
            item = self.set_classifications(self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        return pool
