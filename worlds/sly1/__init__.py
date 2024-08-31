
from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from .Items import item_table, create_itempool
from .Locations import get_location_names
from .Options import Sly1Options
from .Regions import create_regions

class Sly1World(World):
    """
    Sly Cooper and the Thievius Raccoonus is a action stealth game.
    Avenge your father and take back the pages from the fiendish five.
    """

    game = "Sly Cooper and the Thievius Raccoonus"
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    # options_dataclass = Sly1Options
    # options = Sly1Options

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        
    def create_regions(self):
        create_regions(self)

        # If needed, can create a boss locations and input a proof of victory item
        # Add them to the correct location here

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)
        