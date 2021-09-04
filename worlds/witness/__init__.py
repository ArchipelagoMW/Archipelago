from typing import NamedTuple, Union
import logging
import random

from ..AutoWorld import World
from .Items import item_table, event_item_pairs, junk_weights
from .Locations import location_table
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Region, Location, MultiWorld, Item, Entrance

class WitnessWorld(World):
    game = "The Witness"
    topology_present = False
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table
    hidden = True
    
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
            if not item == "Victory":
                pool.append(witness_item)
        

        # Victory item


        junk_pool = junk_weights.copy()
        junk_pool = self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()), k=len(self.location_names)-len(pool)-1)
        pool += [self.create_item(junk) for junk in junk_pool]
               
        self.world.get_location("Final Elevator Control", self.player).place_locked_item(self.create_item("Victory"))
    
        self.world.itempool += pool

    def create_regions(self):
        create_regions(self.world, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        return WitnessItem(name, True, item, player=self.player)
    
    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        #Redo this part (with StS reference) later
        return slot_data

class WitnessLocation(Location):
    game: str = "The Witness"


class WitnessItem(Item):
    game = "The Witness"

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table[location]
            location = WitnessLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
#class PlandoConnection(NamedTuple):
 #   entrance: str
  #  exit: str
   # direction: str  # entrance, exit or both
