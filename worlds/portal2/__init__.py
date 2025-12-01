import random
from BaseClasses import ItemClassification, MultiWorld, Region
from .Options import Portal2Options
from .Items import Portal2Item, Portal2ItemData, item_table, junk_items
from .Locations import Portal2Location, map_complete_table, all_locations_table
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

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
        item_name_to_id[key] = value.id_offset + BASE_ID

    for key, value in all_locations_table.items():
        location_name_to_id[key] = value.id
    
    def create_item(self, name: str):
        self.item_count += 1
        return Portal2Item(name, item_table[name].classification, self.item_name_to_id[name], self.player)
    
    def create_location(self, name, id, parent, event=False):
        return_location = Portal2Location(self.player, name, id, parent)
        return return_location
    
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add chapters to those regions
        for i in range(1, 10):
            # Get chapters
            chapter_list = {name: info.id for name, info in map_complete_table.items()
                            if name.split()[1].startswith(str(i))}
            # Count locations
            self.location_count += len(chapter_list)
            # Create Region
            region = Region(f"Chapter{i}", self.player, self.multiworld)
            region.add_locations(chapter_list, Portal2Location)
            menu_region.connect(region, f"Chapter {i} Entrance")

        victory_loc = Portal2Location(self.player, "Beat Final Level", None, "Chapter 9")
        victory_loc.place_locked_item(Portal2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def set_rules(self):
        # Cannot access chapter 9 until goal items collected
        set_rule(self.multiworld.get_entrance("Chapter 9 Entrance", self.player),
             lambda state: state.has("Adventure Core", self.player) and
                           state.has("Space Core", self.player) and
                           state.has("Fact Core", self.player))

    def create_items(self):
        for item in item_table.keys():
            self.multiworld.itempool.append(self.create_item(item))

        filler_name = self.get_filler_item_name()
        while self.item_count < self.location_count:
            self.multiworld.itempool.append(self.create_item(filler_name))
    
    def get_filler_item_name(self):
        return random.choice(junk_items)
