from typing import NamedTuple, Union
import typing
import logging
import random

from ..AutoWorld import World
from .items import WitnessItem, item_table, junk_weights, event_item_table
from .Locations import location_table, event_location_table
from .Rules import set_rules
from .Regions import create_regions
from .full_logic import EVENT_ITEM_PAIRS
from BaseClasses import Region, RegionType, Location, MultiWorld, Item, Entrance


class WitnessWorld(World):
    game = "The Witness"
    topology_present = False
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table
    hidden = False
    
    def _get_slot_data(self):
        return {
            'seed': random.randint(0, 1000000)
        }
    
    def generate_basic(self):
        # Link regions
     
        # Generate item pool
        pool = []
        for item in item_table:
            witness_item = self.create_item(item)
            if not item == "Victory" and not item in event_item_table:
                pool.append(witness_item)
       

        # Victory item


        junk_pool = junk_weights.copy()
        junk_pool = self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()), k=len(self.location_names)-len(pool)-1)
        
        pool += [self.create_item(junk) for junk in junk_pool]
               
        self.world.get_location("Inside Mountain Final Room Elevator Start", self.player).place_locked_item(self.create_item("Victory"))
        
        for event_location in event_location_table:
            self.world.get_location(event_location, self.player).place_locked_item(self.create_item(EVENT_ITEM_PAIRS[event_location]))
    
        self.world.itempool += pool

    def create_regions(self):
        create_regions(self.world, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in set(): #Put Witness Options in!
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = int(option.value)
            
        return slot_data
        
    

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        return WitnessItem(name, item.progression, item.code, player=self.player)

class WitnessLocation(Location):
    game: str = "The Witness"
    checkHex: int = -1
    
    def __init__(self, player: int, name: str, address: typing.Optional[int], parent, chHex: int = -1):
        super().__init__(player, name, address, parent)
        self.checkHex = chHex

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    from .full_logic import CHECKS_BY_NAME
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table[location]
            
            checkHex = -1
            if location in CHECKS_BY_NAME:
                checkHex = int(CHECKS_BY_NAME[location]["checkHex"], 0)
            location = WitnessLocation(player, location, loc_id, ret, checkHex)

            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
#class PlandoConnection(NamedTuple):
 #   entrance: str
  #  exit: str
   # direction: str  # entrance, exit or both
