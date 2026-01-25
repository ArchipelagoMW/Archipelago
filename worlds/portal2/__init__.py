from math import ceil
import sys

from BaseClasses import ItemClassification, MultiWorld, Region, Tutorial
from Options import PerGameCommonOptions
import settings
from worlds.generic.Rules import add_item_rule
from .Options import CutsceneLevels, Portal2Options, portal2_option_groups, portal2_option_presets
from .Items import Portal2Item, game_item_table, item_table, junk_items, trap_items
from .Locations import Portal2Location, map_complete_table, cutscene_completion_table, all_locations_table
from worlds.AutoWorld import WebWorld, World
from entrance_rando import *
from .ItemNames import portal_gun_2

from . import Components as components

randomize_maps = True

class Portal2Settings(settings.Group):
    class Portal2ExtrasFilePath(settings.UserFilePath):
        """The file path of the extras.txt file (used to generate the menu in game)"""
        description = "Portal 2 extras.txt file inside the mod"

    is_windows = sys.platform == "win32"
    is_linux = sys.platform == "linux"
    extras_path = "C:\\Program Files (x86)\\Steam\\steamapps\\sourcemods\\Portal2Archipelago\\scripts\\extras.txt" if is_windows else \
                    "$HOME/.local/share/Steam/steamapps/sourcemods/Portal2Archipelago/scripts/extras.txt" if is_linux else "" # May may be user specific so cannot auto select
    menu_file: Portal2ExtrasFilePath = Portal2ExtrasFilePath(extras_path)

    class Portal2NetConPort(int):
        """The port set in the portal 2 launch options e.g. 3000"""

    default_portal2_port: Portal2NetConPort = Portal2NetConPort(3000)

class Portal2WebWorld(WebWorld):
    game = "Portal 2"
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Setup Guide",
        description="A guide to playing Portal 2 in Archipelago.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Dyroha"]
    )

    tutorials = [setup_en]

    option_groups = portal2_option_groups
    option_presets = portal2_option_presets

class Portal2World(World):
    """Portal 2 is a first person puzzle adventure where you shoot solve test chambers using portal mechanics and other map specific items"""
    game = "Portal 2"  # name of the game/world
    options_dataclass = Portal2Options  # options the player can set
    options: Portal2Options  # typing hints for option results
    settings: Portal2Settings
    web = Portal2WebWorld()

    BASE_ID = 98275000

    goal_location = "Chapter 9: Finale 4 Completion"

    item_name_to_id = {}
    location_name_to_id = {}

    location_count = 0
    item_count= 0

    maps_in_use: set[str] = set()
    chapter_maps_dict = {}
    
    for key, value in item_table.items():
        item_name_to_id[key] = value.id

    for key, value in all_locations_table.items():
        location_name_to_id[key] = value.id

    # Helper Functions

    def create_item(self, name: str):
        self.item_count += 1
        return Portal2Item(name, item_table[name].classification, self.item_name_to_id[name], self.player)
    
    def create_location(self, name, id, parent):
        self.location_count += 1
        return Portal2Location(self.player, name, id, parent)
    
    def get_filler_item_name(self):
        return self.random.choice(junk_items)
    
    def create_randomized_maps(self) -> dict[str, list[str]]:
        def pick_maps(number: int) -> None:
            self.random.shuffle(map_pool)
            for _ in range(number):
                map_choice = map_pool.pop(0)
                used_maps.append(map_choice)
                chapter_maps[map_choice.split(":")[0]].append(map_choice)
        
        chapter_maps: dict[str, list[str]] = {f"Chapter {i}": [] for i in range(1,9)}

        map_pool: list[str] = []
        used_maps: list[str] = []

        possible_maps = [name for name in sorted(self.maps_in_use) if not name.startswith("Chapter 9")]
        
        proportion_map_pick: float = self.options.early_playability_percentage / 100

        # Maps with no requirements
        map_pool += [name for name in possible_maps if len(all_locations_table[name].required_items) == 0]
        pick_maps(ceil(len(map_pool) * proportion_map_pick))
        
        # Maps with just portal gun upgrade
        map_pool += [name for name in possible_maps if all_locations_table[name].required_items == [portal_gun_2]]
        pick_maps(ceil(len(map_pool) * proportion_map_pick))

        # All other maps
        map_pool += [name for name in possible_maps if name not in used_maps and name not in map_pool]
        pick_maps(len(map_pool))

        return chapter_maps

    def create_connected_maps(self, chapter_number: int, map_location_names: list[str] = None):
        chapter_name = f"Chapter {chapter_number}"
        chapter_region = Region(chapter_name, self.player, self.multiworld)
        self.multiworld.regions.append(chapter_region)

        # Get all map locations for that chapter
        if not map_location_names:
            map_location_names = [name for name in all_locations_table.keys() if name.startswith(chapter_name)]
        map_prefix = [name.removesuffix(" Completion") for name in map_location_names]

        last_region: Region = None
        for name, map_name in zip(map_prefix, map_location_names):
            region_start = Region(f"{name} Start", self.player, self.multiworld)
            self.multiworld.regions.append(region_start)
            region_end = Region(f"{name} End", self.player, self.multiworld)
            self.multiworld.regions.append(region_end)
            region_end.add_locations({map_name: self.location_name_to_id[map_name]}, Portal2Location)
            self.location_count += 1
            item_reqs = all_locations_table[map_name].required_items
            region_start.connect(region_end, f"Beat {name}", lambda state, _item_reqs=item_reqs: state.has_all(_item_reqs, self.player))

            if last_region:
                last_region.connect(region_start)
            else:
                chapter_region.connect(region_start)

            last_region = region_end

        return chapter_region, last_region

    # Overridden methods called by Main.py in execution order

    def generate_early(self):
        self.multiworld.early_items[self.player][portal_gun_2] = 1
        
        # Universal Tracker Support
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, any] = re_gen_passthrough[self.game]

            if "chapter_dict" in slot_data:
                self.chapter_maps_dict = slot_data.get("chapter_dict", [])
                print(self.chapter_maps_dict)
                self.chapter_maps_dict = {f"Chapter {key}":value for key, value in self.chapter_maps_dict.items()}
                return
        
        self.maps_in_use = set(map_complete_table.keys())
        # Cutscene levels option
        if self.options.cutscenelevels:
            self.maps_in_use.update(cutscene_completion_table.keys())

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        if not self.chapter_maps_dict:
            self.chapter_maps_dict = self.create_randomized_maps()
        # Add chapters to those regions
        for i in range(1,9):
            if randomize_maps:
                # chapter_region = self.create_disjointed_maps_for_er(i)
                chapter_region, last_region = self.create_connected_maps(i, self.chapter_maps_dict[f"Chapter {i}"])
            else:
                chapter_region, last_region = self.create_connected_maps(i)

            menu_region.connect(chapter_region, f"Chapter {i} Entrance")
        

        # For chapter 9
        self.chapter_maps_dict["Chapter 9"] = [name for name in all_locations_table.keys() if name.startswith("Chapter 9")]
        chapter_9_region, last_region = self.create_connected_maps(9)
        all_chapter_9_requirements = set()
        for name, value in all_locations_table.items():
            if name.startswith("Chapter 9"):
                all_chapter_9_requirements.update(value.required_items)
        menu_region.connect(chapter_9_region, f"Chapter 9 Entrance", rule=lambda state: state.has_all(all_chapter_9_requirements, self.player))

        # Add Goal Region and Event
        end_game_region = Region("End Game", self.player, self.multiworld)
        last_region.connect(end_game_region, f"End Game Entrance")
        self.multiworld.regions.append(end_game_region)
        end_game_region.add_event("Beat Final Level", "Victory", None, Portal2Location, None, True)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_items(self):
        for item, _ in game_item_table.items():
            self.multiworld.itempool.append(self.create_item(item))

        fill_count = self.location_count - self.item_count
        trap_percentage = self.options.trap_fill_percentage
        trap_fill_number = round(trap_percentage/100 * fill_count)
        trap_weights = [self.options.motion_blur_trap_weight, 
                        self.options.fizzle_portal_trap_weight, 
                        self.options.butter_fingers_trap_weight,
                        self.options.cube_confetti_trap_weight,
                        self.options.slippery_floor_trap_weight] # in the same order as the traps appear in trap_items list

        if sum(trap_weights) > 0 and trap_fill_number > 0:
            traps = self.random.choices(trap_items, weights=trap_weights, k=trap_fill_number)
            for t in traps:
                self.multiworld.itempool.append(self.create_item(t))
        else:
            trap_fill_number = 0

        # Fill remaining with filler item
        filler_name = self.get_filler_item_name()
        for _ in range(fill_count - trap_fill_number):
            self.multiworld.itempool.append(self.create_item(filler_name))

    def set_rules(self):
        # Stop any progression items from being in the final location
        add_item_rule(self.multiworld.get_location(self.goal_location, self.player), 
                      lambda item: item.name not in game_item_table or item.player != self.player)
    
    def fill_slot_data(self):
        # Return the chapter map orders e.g. {chapter1: ['sp_a1_intro2', 'sp_a1_intro5', ...], chapter2: [...], ...}
        # This is for generating and updating the Extras menu (level select screen) in portal 2 at the start and when checks are made
        excluded_option_names = [CutsceneLevels]
        generic_option_names = [option_name for option_name in PerGameCommonOptions.type_hints]
        excluded_option_names += generic_option_names
        included_option_names: list[str] = [option_name for option_name in self.options_dataclass.type_hints if option_name not in excluded_option_names]
        slot_data = self.options.as_dict(*included_option_names, toggles_as_bools=True)
        slot_data.update({
            "goal_map_code": all_locations_table[self.goal_location].map_name,
            "location_name_to_id": self.location_name_to_id,
            "chapter_dict": {int(name[-1]): values for name, values in self.chapter_maps_dict.items()}
        })
        return slot_data
    
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, any]) -> dict[str, any]:
        return slot_data
