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
        return self.random.choice(junk_items)
    
    
    def create_disjointed_maps_for_er(self, chapter_number: int) -> Region:
        chapter_name = f"Chapter {chapter_number}"
        chapter_region = Region(chapter_name, self.player, self.multiworld)
        self.multiworld.regions.append(chapter_region)
        chapter_start_entrance = chapter_region.create_exit(f"{chapter_name} To First Map")
        chapter_start_entrance.randomization_group = chapter_number
        chapter_start_entrance.randomization_type = EntranceType.ONE_WAY

        # Get all map locations for that chapter
        map_location_names = [name for name in all_locations_table.keys() if name.startswith(chapter_name)]
        map_prefix = [name.removesuffix(" Completion") for name in map_location_names]

        """
        Each map is actually 2 regions
        Region(MapAStart) -> Entrance(BeatMapA) -> Region(MapAEnd) -> Entrance(ProgressToNextMap)
        The BeatMapA entrance has the rule "Has [itemsYouNeedToBeatTheRoom]"
        You can randomize maps by connecting the Progress Entrance to randomized Map Starts. But you do not randomize the BeatMap entrances, and they're the ones with the rules
        """
        for name, map_name in zip(map_prefix, map_location_names):
            # Increment the location counter for filler items
            self.location_count += 1

            region_start = Region(f"{name} Start", self.player, self.multiworld)
            self.multiworld.regions.append(region_start)
            region_end = Region(f"{name} End", self.player, self.multiworld)
            self.multiworld.regions.append(region_end)
            region_end.add_locations({map_name: self.location_name_to_id[map_name]})

            region_start.connect(region_end, f"Beat {name}", lambda state: state.has_all(all_locations_table[map_name].required_items, self.player))

            start_entrance = region_start.create_er_target(f"{name} Start Entrance")
            start_entrance.randomization_group = chapter_number
            start_entrance.randomization_type = EntranceType.ONE_WAY
            progress_to_next_map_entrance = region_end.create_exit(f"{name} To Next Map")
            progress_to_next_map_entrance.randomization_group = chapter_number
            progress_to_next_map_entrance.randomization_type = EntranceType.ONE_WAY

        # Add dead end region to each chapter
        chapter_end_region = Region(f"{chapter_name} End", self.player, self.multiworld)
        self.multiworld.regions.append(chapter_end_region)
        chapter_end_entrance = chapter_region.create_er_target(f"{chapter_name} End")
        chapter_end_entrance.randomization_group = chapter_number
        chapter_end_entrance.randomization_type = EntranceType.ONE_WAY

        return chapter_region


    # Overridden methods called by Main.py in execution order

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add chapters to those regions
        for i in range(1,9):
            chapter_region = self.create_disjointed_maps_for_er(i)
            menu_region.connect(chapter_region, f"Chapter {i} Entrance")

        # For chapter 9
        chapter_9_region = Region("Chapter 9", self.player, self.multiworld)
        self.multiworld.regions.append(chapter_9_region)
        chapter_9_locations = [name for name in all_locations_table.keys() if name.startswith("Chapter 9")]
        chapter_9_region.add_locations({name: all_locations_table[name] for name in chapter_9_locations})
        self.location_count += len(chapter_9_locations)
        all_chapter_9_requirements = set()
        for loc in chapter_9_locations:
            all_chapter_9_requirements.update(all_locations_table[loc].required_items)
        menu_region.connect(chapter_9_region, f"Chapter 9 Entrance", rule=lambda state: state.has_all(all_chapter_9_requirements, self.player))

        # Add a final location to the end of chapter 9 for end game event
        chapter_9_region.add_event("Beat Final Level", "Victory", None, Portal2Location, None, True)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_items(self):
        for item, info in item_table.items():
            if info.classification != ItemClassification.filler:
                self.multiworld.itempool.append(self.create_item(item))

        filler_name = self.get_filler_item_name()
        while self.item_count < self.location_count:
            self.multiworld.itempool.append(self.create_item(filler_name))
        
    def connect_entrances(self):
        try:
            groups_dict = {i:[i] for i in range(1, 9)}
            er_placement_state = randomize_entrances(self, True, groups_dict)
            print("Pairings " + str(er_placement_state.pairings))
            print("Placements " + str(er_placement_state.placements))
        finally:
            state = self.multiworld.get_all_state(False)
            state.update_reachable_regions(self.player)
            Utils.visualize_regions(self.multiworld.get_region("Menu", self.player), f"output/map_Player{self.player}.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
            
    def fill_slot_data(self):
        # Return the chapter map orders e.g. {chapter1: ['sp_a1_intro2', 'sp_a1_intro5', ...], chapter2: [...], ...}
        # This is for generating and updating the Extras menu (level select screen) in portal 2 at the start and when checks are made
        return {}
