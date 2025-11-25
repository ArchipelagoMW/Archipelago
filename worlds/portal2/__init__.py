from BaseClasses import Region
from .Options import Portal2Options
from .Items import Portal2Item, item_table
from .Locations import Portal2Location, map_complete_table, cutscene_completion_table
from worlds.AutoWorld import World

class Portal2World(World):
    """Portal 2 is a first person puzzle adventure where you shoot solve test chambers using portal mechanics and other map specific items"""
    game = "Portal 2"  # name of the game/world
    options_dataclass = Portal2Options  # options the player can set
    options: Portal2Options  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 98275000
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(item_table.keys(), base_id)}
    
    # add other locations from options when set up
    location_name_to_id = {name: id for
                           id, name in enumerate(map_complete_table.keys(), base_id)}
    
    def create_item(self, name: str):
        return Portal2Item(name, item_table[name].classification, self.item_name_to_id[name], self.player)
    
    def create_location(self, name, id, parent, event=False):
        return_location = Portal2Location(self.player, name, id, parent)
        return return_location
    
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # add all locations to menu region for now, will change later when we add other locations e.g. item locations, achievements etc.
        menu_region.add_locations(self.location_name_to_id, Portal2Location)

    def create_items(self):
        for item in map(self.create_item, item_table.keys()):
            self.multiworld.itempool.append(item)

        junk = len(self.location_name_to_id) - len(self.item_name_to_id)
        self.multiworld.itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]
    
    def get_filler_item_name(self):
        return "Moon Dust"
    
    def generate_early(self):
        if self.options.cutscenesanity:
            self.location_name_to_id.update({name: id for
                                            id, name in enumerate(cutscene_completion_table.keys(), self.base_id + len(self.location_name_to_id))})
