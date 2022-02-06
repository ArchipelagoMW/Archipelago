import typing

from .Items import item_table, V6Item
from .Locations import location_table, V6Location
from .Options import v6_options
from .Rules import set_rules
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

    area_connections: typing.Dict[int, int]
    area_cost_map: typing.Dict[int,int]

    music_map: typing.Dict[int,int]

    options = v6_options

    def create_regions(self):
        create_regions(self.world,self.player)

    def set_rules(self):
        self.area_connections = {}
        self.area_cost_map = {}
        set_rules(self.world, self.player, self.area_connections, self.area_cost_map)

    def create_item(self, name: str) -> Item:
        return V6Item(name, True, item_table[name], self.player)

    def generate_basic(self):
        trinkets = [self.create_item("Trinket " + str(i+1).zfill(2)) for i in range(0,20)]
        self.world.itempool += trinkets

        musiclist_o = [1,2,3,4,9,12]
        musiclist_s = musiclist_o.copy()
        if self.world.MusicRandomizer[self.player].value:
            self.world.random.shuffle(musiclist_s)
        self.music_map = dict(zip(musiclist_o, musiclist_s))

    def fill_slot_data(self):
        return {
            "MusicRando": self.music_map,
            "AreaRando": self.area_connections,
            "DoorCost": self.world.DoorCost[self.player].value,
            "AreaCostRando": self.area_cost_map,
            "DeathLink": self.world.DeathLink[self.player].value,
            "DeathLink_Amnesty": self.world.DeathLinkAmnesty[self.player].value
        }
