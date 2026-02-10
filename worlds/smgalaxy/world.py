from typing import ClassVar
from BaseClasses import Item
from Utils import visualize_regions
from worlds.AutoWorld import World

from . import items, regions, Rules, web_world, Options
from .Constants.Names import region_names as regname
from .locations import LOCATION_NAME_TO_ID, get_location_names_per_category
from .items import SMGItem, ITEM_NAME_TO_ID, get_item_names_per_category


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

    item_name_to_id: ClassVar[dict[str, int]] = ITEM_NAME_TO_ID
    location_name_to_id: ClassVar[dict[str, int]] = LOCATION_NAME_TO_ID

    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    required_client_version = (0, 6, 6)

    hint_blacklist = {"B: Bowser's Galaxy Reactor", "Peach"}

    def __init__(self, *args, **kwargs):
        super(SMGWorld, self).__init__(*args, **kwargs)
        self.origin_region_name: str = regname.SHIP

    def create_regions(self):
        regions.create_regions(self)

    def set_rules(self):
        Rules.set_rules(self, self.player)
    
    def create_item(self, name: str) -> SMGItem:
        item = items.SMGItem(name, self.player, items.item_table[name])
        
        return item

    def get_filler_item_name(self) -> str:
        return "Nothing"
    
    def create_items(self):
        # creates the green stars in each player's itempool
        local_pool: list[SMGItem] = []
        local_pool += [self.create_item("Green Star") for i in range(0,3)]
        local_pool += [self.create_item("Grand Star") for i in range(0,7)]
        self.multiworld.get_location("B: The Fate of the Universe", self.player).place_locked_item(self.create_item("Peach"))
        
        # check to see what setting enable purple coin stars is on to see how many stars to create 
        if self.options.enable_purple_coin_stars == self.options.enable_purple_coin_stars.option_main_game_only:
           local_pool += [self.create_item("Power Star") for i in range(0,95)]
        
        elif self.options.enable_purple_coin_stars == self.options.enable_purple_coin_stars.option_all:
             local_pool += [self.create_item("Power Star") for i in range(0,110)]

        else:
             local_pool += [self.create_item("Power Star") for i in range(0,94)]

        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        n_items = len(local_pool)
        n_filler_items = n_locations - n_items

        # Create filler
        for _ in range(n_filler_items):
            local_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += local_pool

    def pre_fill(self) -> None:
        visualize_regions(self.get_region(self.origin_region_name), "SMG_region_graph",show_entrance_names=True)