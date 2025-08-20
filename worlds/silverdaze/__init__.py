from .Rules import set_rules, set_completion_rules
from .Regions import sd_regions
from .Items import SDItem, ItemData, item_table
from .Locations import location_table, SDLocationData, SDLocation
from .Options import SilverDazeOptions
from BaseClasses import Region, Entrance, Tutorial, Item
from worlds.AutoWorld import WebWorld, World
# from Items import item_table
# from Locations import SDLocationData
# from Locations import location_table


class SDWorld(World):
    """
    This will describe Silver Daze eventually
    """
    
    game = "Silver Daze"
    required_client_version = (0,5,4)
    options_dataclass = SilverDazeOptions
    #options: SilverDazeOptions
    #settings: typing.classVar[SilverDazeSettings] #Nat: somehow settings and options are different?
    topology_present = True  # show path to required location checks in spoiler    
    
    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    
    # IDs in this dict are numeric and totally arbitrary, as long as they're unique
    # from each other. For normal items, we can use their database IDs from the game itself.
    item_name_to_id = {
        name: data.code for name, data in item_table.items()
    }
    # For locations, we'll use ``enumerate`` to make us IDs in increasing order, from 0.
    location_name_to_id = {
        name: id for id, name in enumerate(location_table, 0)
    }
      
    def get_filler_item_name(self):
        return "Heal Token"
      
    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = SDItem(name, item_data.classification, item_data.code, self.player)
        return item

    # CORRECT ORDER OF EXECUTION:
    # stage_assert_generate(cls, multiworld: MultiWorld)
    # generate_early(self)                                                     unused?
    # create_regions(self)                                                          OK
    # create_items(self)                                                            OK       
    # set_rules(self)                                                               OK
    # connect_entrances(self)                                     unused in undertale?
    # generate_basic(self) 
    # pre_fill(self), fill_hook(self) and post_fill(self) 
    # generate_output(self, output_directory: str) 
    # fill_slot_data(self) and modify_multidata(self, multidata: Dict[str, Any]) 
    
    def create_regions(self):
        player = self.player
        for (region_name, exit_names) in sd_regions:
            region = Region(region_name, player, self)
            
            # add internal locations as SDLocations
            region.locations += [SDLocation(player, name, self.location_name_to_id[name], region)
                                 for name, data in location_table if data.region == region_name]
            # same, maybe slower:
            # for (name, data) in location_table:
            #     if data.region == region_name:
            #         region.locations += SDLocation(player, name, self.location_name_to_id[name], region)
            
            # add exits as Entrances
            for exit_name in exit_names:
                region.exits.append(Entrance(player, exit_name, region))
            
            self.multiworld.regions.append(region)
    
    def create_items(self):
        itempool = []
        
        for name, max_quantity in item_table:
            itempool += [name] * max_quantity
        
        #Starting Party Member given at game start
        starter_member = "Pinn"
        if (Options.StartingPartyMember == "option_geo"):
            starter_member = "Geo"
        if (Options.StartingPartyMember == "option_kani"):
            starter_member = "Kani"
        if (Options.StartingPartyMember == "option_random"):
            import random
            #TODO:
            #Sawyer: Make sure this has all party members in the final game.
            member = random.randint(1,3)
            if (member == 1): starter_member = "Pinn"
            elif (member == 2): starter_member = "Geo"
            elif (member == 3): starter_member = "Kani"
        itempool.remove(starter_member)
        self.multiworld.push_precollected(self.create_item(starter_member))
        
        #other steps here maybe
        
        #Create Items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        # Fill remaining items with randomly generated junk
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())
        
        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self)
        set_completion_rules(self)

