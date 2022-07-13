import os
import json
from .Locations import SMGLocation
from .Regions import create_regions, smgcourses
from .Rules import set_rules
from .items import genric_item_table
from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld
from .Options import Galaxy_options



class SuperMarioGalaxy(World):
    """
    Super Mario Galaxy allows you to explore the cosomos with rosalinna in the comet obserbatory. 
    Mario must collect Power Stars and Grand Stars to power the obserbatory so it can go to the 
    center of the universe in order to save peach.
    """
    game: str = "Super Mario Galaxy"
    options = Galaxy_options
    topology_present = True
    web = GalaxyWeb()

    item_name_to_id = generic_item_table
    location_name_to_id = location_table

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world,self.player)
   
    def make_items(self): 
        staritem = self.create_item("Power Star")
            self.world.itempool += [staritem for i in range(0,120)]