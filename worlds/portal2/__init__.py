from BaseClasses import ItemClassification, MultiWorld, Region
import Utils
from .Options import Portal2Options
from .Items import Portal2Item, Portal2ItemData, item_table, junk_items
from .Locations import Portal2Location, map_complete_table, all_locations_table
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from entrance_rando import *

randomize_maps = False

class Portal2World(World):
    """Portal 2 is a first person puzzle adventure where you shoot solve test chambers using portal mechanics and other map specific items"""
    game = "Portal 2"  # name of the game/world
    options_dataclass = Portal2Options  # options the player can set
    options: Portal2Options  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler

    BASE_ID = 98275000

    item_name_to_id = {}
    location_name_to_id = {}

    location_count = 0
    item_count= 0
    
    for key, value in item_table.items():
        item_name_to_id[key] = value.id

    for key, value in all_locations_table.items():
        location_name_to_id[key] = value.id
    
    # Helper Functions

    def create_item(self, name: str):
        self.item_count += 1
        return Portal2Item(name, item_table[name].classification, self.item_name_to_id[name], self.player)
    
    def create_location(self, name, id, parent, event=False):
        return_location = Portal2Location(self.player, name, id, parent)
        return return_location
    
    def get_filler_item_name(self):
        return self.multiworld.random.choice(junk_items)
    
    def create_chapter_region(self, chapter_number: int, randomized: bool = False) -> Region:
        # Get chapters
        chapter_map_dict = {name: info.id for name, info in map_complete_table.items()
                        if name.split()[1].startswith(str(chapter_number))}
        # Count locations
        self.location_count += len(chapter_map_dict)
        # Create Region
        region = Region(f"Chapter{chapter_number}", self.player, self.multiworld)

        # Create a region for each level and place the location in that region (This handles the in order map completion logic for each chapter)
        chapter_map_list = list(chapter_map_dict.keys())

        if randomized:
            # For randomization
            # region_exit = region.create_exit(f"Chapter {chapter_number} First Level")
            # region_exit.randomization_group = chapter_number * 10
            # region_exit.randomization_type = EntranceType.ONE_WAY

            self.multiworld.random.shuffle(chapter_map_list)
            dead_end_set = False
            for c in chapter_map_list:
                base_name = c.removesuffix("Completion")
                map_region = Region(base_name + "Region", self.player, self.multiworld)
                map_region.add_locations({c: chapter_map_dict[c]}, Portal2Location)
                map_entrance = map_region.create_er_target(base_name + "Entrance")
                # Add access rule
                map_entrance.access_rule = lambda state: state.has_all(map_complete_table[c].required_items, self.player)
                # Keep chapter maps in the same randomization pools
                map_entrance.randomization_group = chapter_number
                # Chapters cannot be accessed in reverse
                map_entrance.randomization_type = EntranceType.ONE_WAY
                
                # Same for exit
                if dead_end_set:
                    map_exit = map_region.create_exit(base_name + "Exit")
                    map_exit.randomization_group = chapter_number
                    map_exit.randomization_type = EntranceType.ONE_WAY
                else:
                    dead_end_set = True

        # For non randomized locations
        else:
            regions: list[Region] = []
            for c in chapter_map_list:
                base_name = c.removesuffix("Completion")
                map_region = Region(base_name + "Region", self.player, self.multiworld)
                map_region.add_locations({c: chapter_map_dict[c]})
                regions.append(map_region)

            for i in range(len(regions) - 1):
                regions[i].connect(regions[i+1], rule=lambda state: state.has_all(map_complete_table[chapter_map_list[i+1]].required_items, self.player))

            region.connect(regions[0])

        return region

    # Overridden methods called by Main.py in execution order

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add chapters to those regions
        for i in range(1, 8):
            region = self.create_chapter_region(i, randomize_maps)
            menu_region.connect(region, f"Chapter {i} Entrance")

        # For chapter 9
        chapter_9_region = self.create_chapter_region(9)
        menu_region.connect(chapter_9_region, f"Chapter 9 Entrance")

        victory_loc = Portal2Location(self.player, "Beat Final Level", None, chapter_9_region)
        victory_loc.place_locked_item(Portal2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_items(self):
        for item in item_table.keys():
            self.multiworld.itempool.append(self.create_item(item))

        filler_name = self.get_filler_item_name()
        while self.item_count < self.location_count:
            self.multiworld.itempool.append(self.create_item(filler_name))

    def set_rules(self):
        # Cannot access chapter 9 until goal items collected
        set_rule(self.multiworld.get_entrance("Chapter 9 Entrance", self.player),
             lambda state: state.has("Adventure Core", self.player) and
                           state.has("Space Core", self.player) and
                           state.has("Fact Core", self.player))
        
    def connect_entrances(self):
        try:
            if randomize_maps:
                groups_dict = {i*10:[i] for i in range(1, 9)}
                groups_dict.update({i:[i] for i in range(1, 9)})
                er_placement_state = randomize_entrances(self, False, groups_dict)
                print("Pairings " + str(er_placement_state.pairings))
                print("Placements " + str(er_placement_state.placements))
        finally:
            Utils.visualize_regions(self.multiworld.get_region("Menu", self.player), "output/map.puml", show_entrance_names=True)
        
    def fill_slot_data(self):
        # Return the chapter map orders e.g. {chapter1: ['sp_a1_intro2', 'sp_a1_intro5', ...], chapter2: [...], ...}
        # This is for generating and updating the Extras menu (level select screen) in portal 2 at the start and when checks are made
        return {}
