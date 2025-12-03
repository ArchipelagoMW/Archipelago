from BaseClasses import ItemClassification, MultiWorld, Region
import Utils
from .Options import Portal2Options
from .Items import Portal2Item, Portal2ItemData, item_table, junk_items
from .Locations import Portal2Location, map_complete_table, cutscene_completion_table, all_locations_table
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from entrance_rando import *
from .ItemNames import portal_gun_2

randomize_maps = True

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
    
    def create_chapter_region(self, chapter_name: str, map_list: list[str] = None) -> Region:
        """Creates Chapter region for a chapter by number where the maps are not in a random order. 
        If map_list is present it will use that as the order of the maps rather than the default order
        """

        # Get chapters
        if map_list:
            chapter_map_dict = {}
            for map_name in map_list:
                chapter_map_dict[map_name] = self.location_name_to_id[map_name]
            chapter_map_list = map_list
        else:
            chapter_map_dict = {name: id for name, id in self.location_name_to_id.items()
                            if name.split(":")[0] == chapter_name}
            chapter_map_list = list(chapter_map_dict.keys())
        # Count locations
        self.location_count += len(chapter_map_dict)
        # Create Region
        region = Region(chapter_name, self.player, self.multiworld)

        # Create a region for each level and place the location in that region (This handles the in order map completion logic for each chapter)
        regions: list[Region] = []
        for c in chapter_map_dict.keys():
            base_name = c.removesuffix("Completion")
            map_region = Region(base_name + "Region", self.player, self.multiworld)
            map_region.add_locations({c: chapter_map_dict[c]})
            regions.append(map_region)

        print(chapter_name + " Regions : " + str(regions))
        for i in range(len(regions) - 1):
            regions[i].connect(regions[i+1], rule=lambda state: state.has_all(map_complete_table[chapter_map_list[i]].required_items, self.player))

        region.connect(regions[0])

        return region
    
    def randomize_map_order(self) -> dict[str, list[str]]:

        # All chapters apart from the last
        chapter_maps = {f"Chapter {i}":[] for i in range(1, 9)}

        map_pool: list[str] = []
        used_maps: list[str] = []

        def pick_maps(number: int) -> None:
            self.multiworld.random.shuffle(map_pool)
            for _ in range(number):
                map_choice = map_pool.pop(0)
                used_maps.append(map_choice)
                chapter_maps[map_choice.split(":")[0]].append(map_choice)

        maps = {name:info for name, info in map_complete_table.items() if "Chapter 9" not in name}
        if self.options.cutscenesanity:
            maps.update(cutscene_completion_table)
        
        all_maps_required_items = {name:info.required_items for name, info in maps.items()}

        # Pick 3 that don't require any items
        map_pool += [name for name, ri in all_maps_required_items.items() if not ri]
        pick_maps(3)

        # Add maps that only require portal_gun_1 to map_pool and pick another 3
        map_pool += [name for name, ri in all_maps_required_items.items() if ri == [portal_gun_2]]
        pick_maps(3)

        # Add maps that only require <= 4 items and pick 10
        map_pool += [name for name, ri in all_maps_required_items.items() if ri and ri != [portal_gun_2] and len(ri) <= 4]
        pick_maps(10)

        # Add remaining maps and add the remainder of the maps to the game
        map_pool += [name for name, _ in all_maps_required_items.items() if name not in map_pool and name not in used_maps]
        pick_maps(len(map_pool))

        return chapter_maps

    # Overridden methods called by Main.py in execution order

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add chapters to those regions
        if randomize_maps:
            chapter_map_orders = self.randomize_map_order()
            for chapter_name, map_list in chapter_map_orders.items():
                region = self.create_chapter_region(chapter_name, map_list)
                menu_region.connect(region, f"{chapter_name} Entrance")
        else:
            for i in range(1, 8):
                chapter_name = f"Chapter {i}"
                region = self.create_chapter_region(chapter_name)
                menu_region.connect(region, f"{chapter_name} Entrance")

        # For chapter 9
        chapter_9_region = self.create_chapter_region("Chapter 9")
        menu_region.connect(chapter_9_region, f"Chapter 9 Entrance")

        victory_loc = Portal2Location(self.player, "Beat Final Level", None, menu_region)
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
        state = self.multiworld.get_all_state(False)
        state.update_reachable_regions(self.player)
        Utils.visualize_regions(self.multiworld.get_region("Menu", self.player), f"output/map_Player{self.player}.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
        
    def fill_slot_data(self):
        # Return the chapter map orders e.g. {chapter1: ['sp_a1_intro2', 'sp_a1_intro5', ...], chapter2: [...], ...}
        # This is for generating and updating the Extras menu (level select screen) in portal 2 at the start and when checks are made
        return {}
