from .Items import is_progression  # this is just a dummy
from ..AutoWorld import World, WebWorld
from .Options import overcooked_options
from .Items import item_table, is_progression, Overcooked2Item
from .Locations import location_id_to_name, location_name_to_id
from .Regions import create_regions
from BaseClasses import ItemClassification

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

    def create_item(self, item: str):
        if is_progression(item):
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
            
        return Overcooked2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str):
        return Overcooked2Item(event, True, None, self.player)

    # called to place player's items into the MultiWorld's itempool
    def create_items(self):
        pass

    # called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done during generate_early or basic as well.
    def create_regions(self):
        create_regions(self.world,self.player)

    # called to set access and item rules on locations and entrances.
    def set_rules(self):
        pass

    # After this step all regions and items have to be in the MultiWorld's regions and itempool.
    def generate_basic(self) -> None:
        itempool = []
        pool_counts = item_frequencies.copy()

        for item_name in item_table:
            for _ in range(pool_counts.get(item_name, 1)):
                itempool.append(self.create_item(item_name))

    
    def generate_output(self, output_directory: str) -> None:
        pass
