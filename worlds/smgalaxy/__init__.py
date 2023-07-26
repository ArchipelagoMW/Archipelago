import string
from typing import Optional
from .items import item_table, SMGItem
from .locations import location_table, SMGLocation
from .Options import EnablePurpleCoinStars, galaxy_options
from .Rules import set_rules
from .regions import create_regions
from BaseClasses import Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld


class SMGWeb(WebWorld):
    theme = "ice"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Super Mario Galaxy for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["squidy"]
    )]


class SuperMarioGalaxy(World):
    """
    Super Mario Galaxy allows you to explore the cosomos with rosalinna in the comet obserbatory. 
    Mario must collect Power Stars and Grand Stars to power the obserbatory so it can go to the 
    center of the universe in order to save peach.
    """

    game: str = "Super Mario Galaxy"
    topology_present = False
    
    web = SMGWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 0
    required_client_version = (0, 4, 0)
    
    option_definitions = galaxy_options
    hint_blacklist = {"B: Bowser's Galaxy Reactor", "Peach"}

    def create_regions(self):
        create_regions(self.multiworld, self.player, self)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self)
    
    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "Power Star":
            classification = ItemClassification.progression_skip_balancing
        elif name == "Nothing":
            classification = ItemClassification.filler
        else:
            classification = ItemClassification.progression
        item = SMGItem(name, classification, item_id, self.player)
        
        return item
    
    def create_items(self):
        # creates the green stars in each players itempool
        self.multiworld.itempool += [self.create_item("Green Star") for i in range(0,3)]
        self.multiworld.itempool += [self.create_item("Progressive Grand Star") for i in range(0,5)]       
        self.multiworld.get_location("B: Bowser's Galaxy Reactor", self.player).place_locked_item(self.create_item("Peach"))
        
        # check to see what setting enable purple coin stars is on to see how many stars to create 
        if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_main_game_only:
           self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,99)]
        
        elif self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
             self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,127)]

        else:
             self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,92)]
         
        # creates the grand stars in each players itempool

        if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_none:
           self.multiworld.get_location("TT: Luigi's Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("DN: Battlestation's Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("MM: Red-Hot Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("DD: Plunder the Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("SS: Purple Coins by the Seaside", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("GE: Purple Coin Omelet", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("BR: Purple Coins on the Battlerock", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("GG: Purple Coins on the Puzzle Cube", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("SJ: Purple Coin Spacewalk", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("BB: Beachcombing for Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("G: Purple Coins in the Bone Pen", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("GL: Purple Coins in the Woods", self.player).place_locked_item(self.create_item("Nothing")) 
           self.multiworld.get_location("DDune: Purple Coin in the Desert", self.player).place_locked_item(self.create_item("Nothing"))
           self.multiworld.get_location("HH: The Honeyhive's Purple Coins", self.player).place_locked_item(self.create_item("Nothing")) 
           self.multiworld.get_location("GG: Gateway's Purple coins", self.player).place_locked_item(self.create_item("Nothing"))
        elif self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
             return
        else:
             self.multiworld.get_location("TT: Luigi's Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("DN: Battlestation's Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("MM: Red-Hot Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("DD: Plunder the Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("SS: Purple Coins by the Seaside", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("GE: Purple Coin Omelet", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("BR: Purple Coins on the Battlerock", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("GG: Purple Coins on the Puzzle Cube", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("SJ: Purple Coin Spacewalk", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("BB: Beachcombing for Purple Coins", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("G: Purple Coins in the Bone Pen", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("GL: Purple Coins in the Woods", self.player).place_locked_item(self.create_item("Nothing")) 
             self.multiworld.get_location("DDune: Purple Coin in the Desert", self.player).place_locked_item(self.create_item("Nothing"))
             self.multiworld.get_location("HH: The Honeyhive's Purple Coins", self.player).place_locked_item(self.create_item("Nothing")) 
    