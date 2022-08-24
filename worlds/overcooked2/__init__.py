from .Items import is_progression  # this is just a dummy
from ..AutoWorld import World, WebWorld
from .Options import overcooked_options
from .Items import item_table, is_progression, Overcooked2Item
from .Locations import location_id_to_name, location_name_to_id
from BaseClasses import ItemClassification

from .Overcooked2Levels import Overcooked2Level
from .Locations import Overcooked2Location, location_name_to_id

import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType


class Overcooked2Web(WebWorld):
    pass


class Overcooked2Web(World):
    """
    Overcooked! 2 is a franticly paced cooking arcade game where
    players race against the clock to complete orders for points. Bring
    peace to the Onion Kingdom once again by recovering lost items and abilities,
    earning stars to unlock levels, and defeating the unbread horde. Levels are
    randomized to increase gameplay variety. Best enjoyed with a friend or three.
    """
    game = "Overcooked! 2"
    web = Overcooked2Web()
    option_definitions = overcooked_options
    topology_present: bool = False
    remote_items: bool = True
    remote_start_inventory: bool = True
    data_version = 0
    base_id = 0

    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id

    # use this for pre-generation
    def generate_early(self) -> None:
        pass

    def create_event(self, event: str):
        return Overcooked2Item(event, True, None, self.player)

    def create_item(self, item: str):
        if is_progression(item):
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return Overcooked2Item(item, classification, self.item_name_to_id[item], self.player)

    # called to place player's items into the MultiWorld's itempool
    def create_items(self):
        # Add Items
        self.world.itempool += [self.create_item(item_name)
                                for item_name in item_table]

        # Add Events (Star Acquisition)
        for _ in Overcooked2Level():
            self.create_event("Star")
            self.create_event("Star")
            self.create_event("Star")

    # called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done during generate_early or basic as well.
    def create_regions(self):
        # Menu -> Overworld
        self.create_region("Menu")
        self.create_region("Overworld")
        self.connect_regions("Menu", "Overworld")

        for level in Overcooked2Level():
            level_name = level.level_name()

            # Create Region (e.g. "1-1")
            self.create_region(level_name)

            # Populate Region (e.g. "1-1 Reward (1 Star)")
            self.create_location(level_name, level.reward_name_one_star())
            self.create_location(level_name, level.reward_name_two_star())
            self.create_location(level_name, level.reward_name_three_star())

            # Level <--> Overworld
            self.connect_regions(level_name, "Overworld")
            self.connect_regions("Overworld", level_name)

    # called to set access and item rules on locations and entrances.
    def set_rules(self):
        for level in Overcooked2Level():
            level_name = level.level_name()



    # After this step all regions and items have to be in the MultiWorld's regions and itempool.
    def generate_basic(self) -> None:
        pass

    def generate_output(self, output_directory: str) -> None:
        pass

    def create_region(self, region_name: str):
        region = Region(
            region_name,
            RegionType.Generic,
            region_name,
            self.player,
            self.world,
        )
        self.world.regions.append(region)

    def connect_regions(self, source: str, target: str, rule=None):
        sourceRegion = self.world.get_region(source, self.player)
        targetRegion = self.world.get_region(target, self.player)

        connection = Entrance(self.player, '', sourceRegion)
        if rule:
            connection.access_rule = rule

        sourceRegion.exits.append(connection)
        connection.connect(targetRegion)
    
    def create_location(self, region_name: str, location_name: str) -> Location:
        region = self.world.get_region(region_name, self.player)
        return Overcooked2Location(
            self.player,
            location_name,
            self.location_name_to_id[location_name],
            region,
        )
