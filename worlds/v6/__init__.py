import string
from .Items import item_table, V6Item
from .Locations import location_table, V6Location
from .Options import v6_options
from .Rules import set_rules, area_connections
from .Regions import create_regions
from BaseClasses import Region, RegionType, Entrance, Item, MultiWorld
from ..AutoWorld import World

client_version = 1

class V6World(World):
    """ 
     VVVVVV is a platform game all about exploring one simple mechanical idea - what if you reversed gravity instead of jumping?
    """ #Lifted from Store Page

    game: str = "VVVVVV"
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 1
    forced_auto_forfeit = False

    area_connections = {}

    options = v6_options

    def create_regions(self):
        create_regions(self.world,self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.world,self.player,self.area_connections)

    def create_item(self, name: str) -> Item:
        return V6Item(name, True, item_table[name], self.player)

    def generate_basic(self):
        self.world.itempool += [self.create_item(name) for name in self.item_names]

    def fill_slot_data(self):
        return {
            "AreaRando": self.area_connections,
            "DoorCost": self.world.DoorCost[self.player].value,
            "DeathLink": self.world.DeathLink[self.player].value,
            "DeathLink_Amnesty": self.world.DeathLinkAmnesty[self.player].value
        }
