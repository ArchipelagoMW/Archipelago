import string
from .Items import item_table, SM64Item
from .Locations import location_table, SM64Location
from .Options import sm64_options
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Region, RegionType, Entrance, Item, MultiWorld
from ..AutoWorld import World

client_version = 1

class SM64World(World):
    """ 
    The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons,
    combined with traditional Mario gameplay, visual style, and characters.
    """

    game: str = "Super Mario 64"
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 1
    forced_auto_forfeit = False

    options = sm64_options

    def create_regions(self):
        create_regions(self.world,self.player)


    def set_rules(self):
        set_rules(self.world,self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = SM64Item(name, True, item_id, self.player)
        return item

    def generate_basic(self):
        staritem = self.create_item("Star")
        if (self.world.EnableCoinStars[self.player].value):
            self.world.itempool += [staritem for i in range(0,120)]
        else:
            self.world.itempool += [staritem for i in range(0,105)]

        key1 = self.create_item("Cellar Key")
        key2 = self.create_item("Second Floor Key")
        self.world.itempool += [key1,key2]

        wingcap = self.create_item("Wing Cap")
        metalcap = self.create_item("Metal Cap")
        vanishcap = self.create_item("Vanish Cap")
        self.world.itempool += [wingcap,metalcap,vanishcap]

    def fill_slot_data(self):
        return {
            "StarsToFinish": self.world.StarsToFinish[self.player].value
        }
