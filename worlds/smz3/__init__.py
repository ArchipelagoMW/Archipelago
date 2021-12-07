import logging
import copy
import os
import threading
import sys
import pathlib
import Patch
from typing import Set

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, CollectionState
from ..AutoWorld import World
from .Rom import get_base_rom_bytes
from .ips import IPS_Patch

#sys.path.append(r"E:\Github\Archipelago\worlds\smz3")
#import clr
#import System
#import System.Runtime
#SWF = clr.AddReference("Randomizer.Shared")
#print (SWF.Location)
#from Randomizer.Shared.Models import World as TestWorld

class SMZ3World(World):
    game: str = "SMZ3"
    topology_present = True
    data_version = 1
    # options = sm_options
    item_names: Set[str] = {"TestItem"}
    location_names: Set[str] = {"TestLoc"}
    item_name_to_id = {"TestItem": 84000}
    location_name_to_id = {"TestLoc": 85000}

    remote_items: bool = False
    remote_start_inventory: bool = False

    locations = {}


    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)
        #print(TestWorld.Player)
        
    def generate_early(self):
        pass
    
    def generate_basic(self):
        pass

    def set_rules(self):
        pass

    def create_regions(self):
        pass

    def generate_output(self, output_directory: str):
        base_combined_rom = get_base_rom_bytes()
        basepatch = IPS_Patch.load("worlds/smz3/zsm.ips")
        base_combined_rom = basepatch.apply(base_combined_rom)
        with open("Test.sfc", "wb") as binary_file:
            binary_file.write(base_combined_rom)
        Patch.create_patch_file("Test.sfc", player=self.player, player_name=self.world.player_name[self.player], game=Patch.GAME_SMZ3)
        pass

    def modify_multidata(self, multidata: dict):
        pass

    def fill_slot_data(self): 
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        return SMZ3Item()

def create_locations(self, player: int):
    pass

def create_region(self, world: MultiWorld, player: int, name: str, locations=None, exits=None):
    pass


class SMZ3Location(Location):
    game: str = "SMZ3"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(SMZ3Location, self).__init__(player, name, address, parent)

    def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
        return self.always_allow(state, item) or (self.item_rule(item) and (not check_access or self.can_reach(state)))


class SMZ3Item(Item):
    game = "SMZ3"

    def __init__(self, name, advancement, type, code, player: int = None):
        super(SMZ3Item, self).__init__(name, advancement, code, player)
