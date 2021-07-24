import logging
from typing import Set

logger = logging.getLogger("Super Metroid")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import lookup_id_to_name as items_lookup_id_to_name
from .Items import lookup_name_to_id as items_lookup_name_to_id
from .Regions import create_regions
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, CollectionState
from ..AutoWorld import World

from rom.rompatcher import RomPatcher
from graph.vanilla.graph_locations import locationsDict
from rando.ItemLocContainer import ItemLocation
from rando.Items import ItemManager
from utils.parameters import *
from Utils import output_path
from shutil import copy2

class SMWorld(World):
    game: str = "Super Metroid"
    topology_present = True
    item_names: Set[str] = frozenset(items_lookup_name_to_id)
    location_names: Set[str] = frozenset(locations_lookup_name_to_id)
    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id

    qty = {'energy': 'vanilla',
           'minors': 100,
           'ammo': { 'Missile': 9,
                     'Super': 9,
                     'PowerBomb': 9 },
           'strictMinors' : False }

    itemManager: ItemManager

    locations = {}
    
    def generate_basic(self):
        # Link regions
        #self.world.get_entrance('Landing Site', self.player).connect(self.world.get_region('Zebes', self.player))

        self.itemManager = ItemManager('Chozo', self.qty, self.world.state, 100, easy)
        self.itemManager.createItemPool()
        itemPool = self.itemManager.getItemPool()
        
        # Generate item pool
        pool = []
        locked_items = {}
        weaponCount = [0, 0, 0]
        for item in itemPool:
            isAdvancement = True
            if item.Type == 'Missile':
                if weaponCount[0] < 3:
                    weaponCount[0] += 1
                else:
                    isAdvancement = False
            elif item.Type == 'Super':
                if weaponCount[1] < 2:
                    weaponCount[1] += 1
                else:
                    isAdvancement = False
            elif item.Type == 'PowerBomb':
                if weaponCount[2] < 3:
                    weaponCount[2] += 1
                else:
                    isAdvancement = False

            itemClass = self.itemManager.Items[item.Type].Class
            smitem = SMItem(item.Name, isAdvancement, item.Type, self.item_name_to_id[item.Name], player = self.player)
            if itemClass == 'Boss':
                locked_items[item.Name] = smitem
            else:
                pool.append(smitem)

        self.world.itempool += pool

        for (location, item) in locked_items.items():
            self.world.get_location(location, self.player).place_locked_item(item)

    def set_rules(self):
        set_rules(self.world, self.player)


    def create_regions(self):
        create_locations(self, self.player)
        create_regions(self, self.world, self.player)


    def generate_output(self):
        copy2("TEST.sfc", output_path("TEST.sfc"))
        romPatcher = RomPatcher(output_path("TEST.sfc"), None)

        romPatcher.applyIPSPatches()
        romPatcher.commitIPS()

        itemLocs = [ItemLocation(self.itemManager.Items[itemLoc.item.type], locationsDict[itemLoc.name], True) for itemLoc in self.world.get_locations()]
        romPatcher.writeItemsLocs(itemLocs)
        #romPatcher.writeSplitLocs(args.majorsSplit, itemLocs, progItemLocs)
        #romPatcher.writeItemsNumber()
        romPatcher.end()

        pass


    def fill_slot_data(self): 
        slot_data = {}
        return slot_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        state.addItem(item.type)
        if item.advancement:
            state.prog_items[item.name, item.player] += 1
            return True  # indicate that a logical state change has occured
        return False

def create_locations(self, player: int):
    for name, id in locations_lookup_name_to_id.items():
        self.locations[name] = SMLocation(player, name, id)

def create_region(self, world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.LightWorld, name, player)
    ret.world = world
    if locations:
        for loc in locations:
            # loc_id = locations_lookup_name_to_id.get(loc, 0)
            location = self.locations[loc] # SMLocation(player, location, loc_id, ret)
            location.parent_regions.append(ret)
            location.parent_region = ret
            ret.locations.append(location)
    if exits:
        for exit in exits:
            #entrance = Entrance(player, exit, ret) #TEST
            ret.exits.append(Entrance(player, exit, ret))
            #entrance.connect(ret) #TEST
    return ret


class SMLocation(Location):
    game: str = "Super Metroid"

    def __init__(self, player: int, name: str, address=None, parent=None):
        self.parent_regions = []
        super(SMLocation, self).__init__(player, name, address, parent)

    def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
        return self.always_allow(state, item) or (any(region.can_fill(item) for region in self.parent_regions) and self.item_rule(item) and (not check_access or self.can_reach(state)))

    def can_reach(self, state: CollectionState) -> bool:
        # self.access_rule computes faster on average, so placing it first for faster abort
        if self.access_rule(state) and any(region.can_reach(state) for region in self.parent_regions):
            return True
        return False


class SMItem(Item):
    game = "Super Metroid"

    def __init__(self, name, advancement, type, code, player: int = None):
        super(SMItem, self).__init__(name, advancement, code, player)
        self.type = type