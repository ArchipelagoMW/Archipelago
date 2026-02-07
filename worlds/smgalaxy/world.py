from typing import ClassVar
from BaseClasses import Item
from worlds.AutoWorld import World

from . import items, locations, regions, Rules, web_world, Options

class SMGWorld(World):
    """
    Super Mario Galaxy allows you to explore the cosmos with Rosalina in the Comet Observatory.
    Mario must collect Power Stars and Grand Stars to power the observatory so it can go to the
    center of the universe in order to save Princess Peach from Bowser's clutches.
    """

    game = "Super Mario Galaxy"
    topology_present = False
    
    web = web_world.SMGWebWorld()
    
    #option definitions
    options_dataclass = Options.SMGOptions
    options: Options.SMGOptions

    item_name_to_id = ClassVar[items.ITEM_NAME_TO_ID]
    location_name_to_id = ClassVar[locations.LOCATION_NAME_TO_ID]

    required_client_version = (0, 6, 6)

    hint_blacklist = {"B: Bowser's Galaxy Reactor", "Peach"}

    def __init__(self, *args, **kwargs):
        super(SMGWorld, self).__init__(*args, **kwargs)
        self.origin_region_name: str = "Ship"

    def create_regions(self):
        regions.create_regions(self, self.player)

    def set_rules(self):
        Rules.set_rules(self, self.player)
    
    def create_item(self, name: str) -> Item:
        item = items.SMGItem(name, self.player, items.item_table[name])
        
        return item
    
    def create_items(self):
        # creates the green stars in each players itempool
        self.multiworld.itempool += [self.create_item("Green Star") for i in range(0,3)]
        self.multiworld.itempool += [self.create_item("Progressive Grand Star") for i in range(0,5)]       
        self.multiworld.get_location("B: The Fate of the Universe", self.player).place_locked_item(self.create_item("Peach"))
        
        # check to see what setting enable purple coin stars is on to see how many stars to create 
        if self.options.enable_purple_coin_stars == self.options.enable_purple_coin_stars.option_main_game_only:
           self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,99)]
        
        elif self.options.enable_purple_coin_stars == self.options.enable_purple_coin_stars.option_all:
             self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,127)]

        else:
             self.multiworld.itempool += [self.create_item("Power Star") for i in range(0,92)]
         
        # creates the grand stars in each players itempool

        if self.options.enable_purple_coin_stars == self.options.enable_purple_coin_stars.option_none:
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
        elif self.options.enable_purple_coin_stars == self.options.enable_purple_coin_stars.option_all:
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
    