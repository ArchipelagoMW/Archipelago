import typing
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

    data_version = 5
    forced_auto_forfeit = False

    area_connections: typing.Dict[int, int]

    options = sm64_options

    def generate_early(self):
        self.topology_present = self.world.AreaRandomizer[self.player].value

    def create_regions(self):
        create_regions(self.world,self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.world, self.player, self.area_connections)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = SM64Item(name, name != "1Up Mushroom", item_id, self.player)
        return item

    def generate_basic(self):
        staritem = self.create_item("Power Star")
        starcount = min(self.world.StarsToFinish[self.player].value + self.world.ExtraStars[self.player].value,120)
        if (not self.world.EnableCoinStars[self.player].value):
            starcount = max(starcount - 15,self.world.StarsToFinish[self.player].value)
        self.world.itempool += [staritem for i in range(0,starcount)]
        mushroomitem = self.create_item("1Up Mushroom") 
        self.world.itempool += [mushroomitem for i in range(starcount,120 - (15 if not self.world.EnableCoinStars[self.player].value else 0))]

        if (not self.world.ProgressiveKeys[self.player].value):
            key1 = self.create_item("Basement Key")
            key2 = self.create_item("Second Floor Key")
            self.world.itempool += [key1,key2]
        else:
            key = self.create_item("Progressive Key")
            self.world.itempool += [key,key]

        wingcap = self.create_item("Wing Cap")
        metalcap = self.create_item("Metal Cap")
        vanishcap = self.create_item("Vanish Cap")
        self.world.itempool += [wingcap,metalcap,vanishcap]

    def fill_slot_data(self):
        return {
            "AreaRando": self.area_connections,
            "StarsToFinish": self.world.StarsToFinish[self.player].value,
            "DeathLink": self.world.DeathLink[self.player].value,
        }
