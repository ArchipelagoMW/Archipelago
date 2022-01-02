import string
from .Items import item_table, V6Item
from .Locations import location_table, V6Location
from .Options import v6_options
from ..generic.Rules import set_rule
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

    options = v6_options

    def create_regions(self):
        reg = Region("Menu", RegionType.Generic, "Dimension VVVVVV", self.player, self.world)
        for location_name in location_table:
            location = V6Location(self.player, location_name, location_table[location_name], reg)
            reg.locations.append(location)
        self.world.regions.append(reg)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = V6Item(name, True, item_id, self.player)
        return item

    def generate_basic(self):      
        self.world.itempool += [self.create_item(name) for name in self.item_names]

    def fill_slot_data(self):
        return {
            "DeathLink": self.world.DeathLink[self.player].value,
            "DeathLink_Amnesty": self.world.DeathLinkAmnesty[self.player].value
        }
