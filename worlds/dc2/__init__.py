# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DarkCloud2Item, DC2ItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import DarkCloud2Location, DC2LocationCategory, location_tables, location_dictionary, location_skip_categories
from .Options import DC2Option

class DarkCloud2Web(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Dark Cloud 2 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )


    tutorials = [setup_en]


class DarkCloud2World(World):
    """
    Dark Cloud 2 is a game.
    """

    game: str = "Dark Cloud 2"
    is_experimental = True
    options_dataclass = DC2Option
    options: DC2Option
    topology_present: bool = True
    web = DarkCloud2Web()
    data_version = 0
    base_id = 694200000
    enabled_location_categories: Set[DC2LocationCategory]
    required_client_version = (0, 5, 1)
    item_name_to_id = DarkCloud2Item.get_name_to_id()
    location_name_to_id = DarkCloud2Location.get_name_to_id()
    item_name_groups = {
    }
    item_descriptions = item_descriptions
    explicit_indirect_conditions = False

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()


    def generate_early(self):
        self.enabled_location_categories.add(DC2LocationCategory.FLOOR)
        self.enabled_location_categories.add(DC2LocationCategory.RECRUIT)
        self.enabled_location_categories.add(DC2LocationCategory.GEORAMA)
        self.enabled_location_categories.add(DC2LocationCategory.MIRACLE_CHEST)
        self.enabled_location_categories.add(DC2LocationCategory.BOSS)
        self.enabled_location_categories.add(DC2LocationCategory.MISC)
        self.enabled_location_categories.add(DC2LocationCategory.GEOSTONE)
       # self.enabled_location_categories.add(DC2LocationCategory.EVENT)
        self.enabled_location_categories.add(DC2LocationCategory.KEY_ITEM)


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Palm Brinks",
            "Underground Water Channel",
            "Sindain",
            "Rainbow Butterfly Wood",
            "Jurak Mall",
            "Balance Valley",
            "Starlight Canyon",
            "Starlight Temple",
            "Veniccio",
            "Ocean's Roar Cave",
            "Lunatic Wisdom Laboratories",
            "Heim Rada",
            "Mount Gundor",
            "Gundorada Workshop",
            "Moon Flower Palace"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
        
        create_connection("Menu", "Palm Brinks")

        create_connection("Palm Brinks", "Underground Water Channel")
        
        create_connection("Palm Brinks", "Sindain")
        create_connection("Palm Brinks", "Balance Valley")
        create_connection("Palm Brinks", "Veniccio")
        create_connection("Palm Brinks", "Heim Rada")
        create_connection("Palm Brinks", "Moon Flower Palace")
        
        create_connection("Sindain", "Rainbow Butterfly Wood")
        create_connection("Sindain", "Jurak Mall")
        
        create_connection("Balance Valley", "Starlight Canyon")
        create_connection("Balance Valley", "Starlight Temple")
        
        create_connection("Veniccio", "Ocean's Roar Cave")
        create_connection("Veniccio", "Lunatic Wisdom Laboratories")        
        
        create_connection("Heim Rada", "Mount Gundor")
        create_connection("Heim Rada", "Gundorada Workshop")
        
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        #print("location table size: " + str(len(location_table)))
        for location in location_table:
            #print("Creating location: " + location.name)
            if location.category in self.enabled_location_categories and location.category not in location_skip_categories:
                #print("Adding location: " + location.name + " with default item " + location.default_item)
                new_location = DarkCloud2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                #if event_item.classification != ItemClassification.progression:
                #    continue
                #print("Adding Location: " + location.name + " as an event with default item " + location.default_item)
                new_location = DarkCloud2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                #print("Placing event: " + event_item.name + " in location: " + location.name)

            new_region.locations.append(new_location)
        #print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        #print("adding region: " + region_name)
        return new_region


    def create_items(self):
        skip_items: List[DarkCloud2Item] = []
        itempool: List[DarkCloud2Item] = []
        itempoolSize = 0
        
        #print("Creating items")
        for location in self.multiworld.get_locations(self.player):            
            item_data = item_dictionary[location.default_item_name]
            if item_data.category in location_skip_categories:               
                print("Adding skip item: " + location.default_item_name)
                skip_items.append(self.create_item(location.default_item_name))
            elif location.category in self.enabled_location_categories:
                print("Adding item: " + location.default_item_name)
                itempoolSize += 1
                itempool.append(self.create_item(location.default_item_name))
        
        print("Requesting itempool size: " + str(itempoolSize))
        foo = BuildItemPool(self.multiworld, itempoolSize, self.options)
        print("Created item pool size: " + str(len(foo)))

        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]
        #print("marked " + str(len(removable_items)) + " items as removable")
        
        for item in removable_items:
            #print("removable item: " + item.name)
            itempool.remove(item)
            itempool.append(self.create_item(foo.pop().name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

        # Handle SKIP items separately
        #for skip_item in skip_items:
        #    location = next(loc for loc in self.multiworld.get_locations(self.player) if loc.default_item_name == skip_item.name)
        #    location.place_locked_item(skip_item)
            #self.multiworld.itempool.append(skip_item)
            #print("Placing skip item: " + skip_item.name + " in location: " + location.name)
        
        #print("Final Item pool: ")
        #for item in self.multiworld.itempool:
            #print(item.name)




    def create_item(self, name: str) -> Item:
        useful_categories = {
           # DC2ItemCategory.GEORAMA_RESOURCE, DC2ItemCategory.GEM, DC2ItemCategory.COIN
        }
        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category in [DC2ItemCategory.KEY_ITEM]:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DarkCloud2Item(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return "Bread"

    def set_rules(self) -> None:
        # Define the access rules to the entrances
        set_rule(self.multiworld.get_entrance("Palm Brinks -> Underground Water Channel", self.player), lambda state: True) 
        set_rule(self.multiworld.get_entrance("Palm Brinks -> Sindain", self.player), lambda state: state.can_reach_location("UWC: Chapter 1 Complete", self.player))     
        set_rule(self.multiworld.get_entrance("Sindain -> Rainbow Butterfly Wood", self.player), lambda state: state.has("Grape Juice", self.player)) 
        set_rule(self.multiworld.get_entrance("Palm Brinks -> Balance Valley", self.player), lambda state: state.can_reach_location("RBW: Chapter 2 Complete", self.player))   
        set_rule(self.multiworld.get_entrance("Palm Brinks -> Veniccio", self.player), lambda state: state.can_reach_location("SC: Chapter 3 Complete", self.player))   
        set_rule(self.multiworld.get_entrance("Palm Brinks -> Heim Rada", self.player), lambda state: state.can_reach_location("ORC: Chapter 4 Complete", self.player))     
        set_rule(self.multiworld.get_entrance("Palm Brinks -> Moon Flower Palace", self.player), lambda state: state.can_reach_location("MG: Chapter 5 Complete", self.player))            
                  
        set_rule(self.multiworld.get_entrance("Sindain -> Jurak Mall", self.player), lambda state: state.has("Grape Juice", self.player) and state.can_reach_location("S: Grape Juice", self.player)) 
        
        # Chapter 1 floors        
        set_rule(self.multiworld.get_location("UWC: Floor 1 - To the Outside World", self.player), lambda state: True)
        set_rule(self.multiworld.get_location("UWC: Floor 2 - Battle with Rats", self.player), lambda state: state.can_reach_location("UWC: Floor 1 - To the Outside World", self.player))
        set_rule(self.multiworld.get_location("UWC: Floor 3 - Ghosts in the Channel", self.player), lambda state: state.can_reach_location("UWC: Floor 2 - Battle with Rats", self.player))
        set_rule(self.multiworld.get_location("UWC: Pump Room", self.player), lambda state: state.can_reach_location("UWC: Floor 3 - Ghosts in the Channel", self.player))
        set_rule(self.multiworld.get_location("UWC: Linda", self.player), lambda state: state.can_reach_location("UWC: Floor 3 - Ghosts in the Channel", self.player))
        set_rule(self.multiworld.get_location("UWC: Floor 4 - Steve's Battle", self.player), lambda state: state.can_reach_location("UWC: Pump Room", self.player))
        set_rule(self.multiworld.get_location("UWC: Floor 5 - Ghost in the Channel", self.player), lambda state: state.can_reach_location("UWC: Floor 4 - Steve's Battle", self.player))
        set_rule(self.multiworld.get_location("UWC: Halloween", self.player), lambda state: state.can_reach_location("UWC: Floor 5 - Ghost in the Channel", self.player))
        set_rule(self.multiworld.get_location("UWC: Chapter 1 Complete", self.player), lambda state: state.can_reach_location("UWC: Halloween", self.player))
       
       # Chapter 2 floors       
        set_rule(self.multiworld.get_location("RBW: Floor 1 - Frightening Forest", self.player), lambda state: state.can_reach_location("UWC: Chapter 1 Complete", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 2 - Strange Tree", self.player), lambda state: state.can_reach_location("RBW: Floor 1 - Frightening Forest", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 3 - Rolling Shells", self.player), lambda state: state.can_reach_location("RBW: Floor 2 - Strange Tree", self.player))
        set_rule(self.multiworld.get_location("RBW: Fish Monster Swamp", self.player), lambda state: state.can_reach_location("RBW: Floor 3 - Rolling Shells", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 4 - This is a Geostone?", self.player), lambda state: state.can_reach_location("RBW: Fish Monster Swamp", self.player) and state.has("Fishing Rod", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 5 - Noise in the Forest", self.player), lambda state: state.can_reach_location("RBW: Floor 4 - This is a Geostone?", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 6 - I'm a Pixie", self.player), lambda state: state.can_reach_location("RBW: Floor 5 - Noise in the Forest", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 7 - Legendary Killer Snake", self.player), lambda state: state.can_reach_location("RBW: Floor 6 - I'm a Pixie", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 8 - Grotesque Spider Lady", self.player), lambda state: state.can_reach_location("RBW: Floor 7 - Legendary Killer Snake", self.player))
        set_rule(self.multiworld.get_location("RBW: Rainbow Butterfly", self.player), lambda state: state.can_reach_location("RBW: Floor 8 - Grotesque Spider Lady", self.player) and state.has("Lafrescia Seed", self.player) and state.has("Sundrop", self.player))
        set_rule(self.multiworld.get_location("RBW: Chapter 2 Complete", self.player), lambda state: state.can_reach_location("RBW: Rainbow Butterfly", self.player))
           
        # RBW Star path floors
        set_rule(self.multiworld.get_location("RBW: Floor 9 - Looking for the Earth Gem", self.player), lambda state: state.can_reach_location("RBW: Chapter 2 Complete", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 10 - Something Rare Here!", self.player), lambda state: state.can_reach_location("RBW: Floor 9 - Looking for the Earth Gem", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("RBW: Floor 11 - Scary Tree", self.player), lambda state: state.can_reach_location("RBW: Floor 10 - Something Rare Here!", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("RBW: Trentos", self.player), lambda state: state.can_reach_location("RBW: Floor 11 - Scary Tree", self.player) and state.has("Star Key", self.player))
    
        # Chapter 3 floors
        set_rule(self.multiworld.get_location("SC: Floor 1 - Headlong Dash", self.player), lambda state: state.can_reach_location("RBW: Chapter 2 Complete", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 2 - Fire and Ice Don't Mix", self.player), lambda state: state.can_reach_location("SC: Floor 1 - Headlong Dash", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 3 - Earth-Shaking Demon", self.player), lambda state: state.can_reach_location("SC: Floor 2 - Fire and Ice Don't Mix", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 4 - Powerful Yo-Yo Robot", self.player), lambda state: state.can_reach_location("SC: Floor 3 - Earth-Shaking Demon", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 5 - Elephant Army in the Valley", self.player), lambda state: state.can_reach_location("SC: Floor 4 - Powerful Yo-Yo Robot", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 6 - Dangerous Treasure Chest", self.player), lambda state: state.can_reach_location("SC: Floor 5 - Elephant Army in the Valley", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 7 - Little Dragon Counterattack", self.player), lambda state: state.can_reach_location("SC: Floor 6 - Dangerous Treasure Chest", self.player))
        set_rule(self.multiworld.get_location("SC: Barga's Valley", self.player), lambda state: state.can_reach_location("SC: Floor 7 - Little Dragon Counterattack", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 8 - Warrior in Starlight Canyon", self.player), lambda state: state.can_reach_location("SC: Barga's Valley", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 9 - Smiling Fairy Village", self.player), lambda state: state.can_reach_location("SC: Floor 8 - Warrior in Starlight Canyon", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 10 - Cursed Mask", self.player), lambda state: state.can_reach_location("SC: Floor 9 - Smiling Fairy Village", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 11 - We're the Roly-Poly Brothers", self.player), lambda state: state.can_reach_location("SC: Floor 10 - Cursed Mask", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 12 - Dragon Slayer", self.player), lambda state: state.can_reach_location("SC: Floor 11 - We're the Roly-Poly Brothers", self.player))
        set_rule(self.multiworld.get_location("SC: Memo Eater", self.player), lambda state: state.can_reach_location("SC: Floor 12 - Dragon Slayer", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 13 - Rama Priests Like Cheese", self.player), lambda state: state.can_reach_location("SC: Memo Eater", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 14 - Nature's Threat", self.player), lambda state: state.can_reach_location("SC: Floor 13 - Rama Priests Like Cheese", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 15 - Moon Baron", self.player), lambda state: state.can_reach_location("SC: Floor 14 - Nature's Threat", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 16 - Lighthouse Appears", self.player), lambda state: state.can_reach_location("SC: Floor 15 - Moon Baron", self.player))
        set_rule(self.multiworld.get_location("SC: Evil Flame and Gaspard", self.player), lambda state: state.can_reach_location("SC: Floor 16 - Lighthouse Appears", self.player))
        set_rule(self.multiworld.get_location("SC: Chapter 3 Complete", self.player), lambda state: state.can_reach_location("SC: Evil Flame and Gaspard", self.player))
        
        # SC Star path floors
        set_rule(self.multiworld.get_location("SC: Floor 17 - Looking for the Wind Gem", self.player), lambda state: state.can_reach_location("SC: Chapter 3 Complete", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 18 - Evil Spirit in the Valley", self.player), lambda state: state.can_reach_location("SC: Floor 17 - Looking for the Wind Gem", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("SC: Floor 19 - Brave Warriors in the Valley", self.player), lambda state: state.can_reach_location("SC: Floor 18 - Evil Spirit in the Valley", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("SC: Lapis Garter", self.player), lambda state: state.can_reach_location("SC: Floor 19 - Brave Warriors in the Valley", self.player) and state.has("Star Key", self.player))

        # Chapter 4 floors
        set_rule(self.multiworld.get_location("ORC: Floor 1 - Pirates!", self.player), lambda state: state.can_reach_location("SC: Chapter 3 Complete", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 2 - Tons of Fish", self.player), lambda state: state.can_reach_location("ORC: Floor 1 - Pirates!", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 3 - Tank and Boss", self.player), lambda state: state.can_reach_location("ORC: Floor 2 - Tons of Fish", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 4 - Water Monster", self.player), lambda state: state.can_reach_location("ORC: Floor 3 - Tank and Boss", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 5 - Scary Auntie Medusa", self.player), lambda state: state.can_reach_location("ORC: Floor 4 - Water Monster", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 6 - Sand Molers", self.player), lambda state: state.can_reach_location("ORC: Floor 5 - Scary Auntie Medusa", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 7 - Bat Den", self.player), lambda state: state.can_reach_location("ORC: Floor 6 - Sand Molers", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 8 - Pirates' Hideout", self.player), lambda state: state.can_reach_location("ORC: Floor 7 - Bat Den", self.player))
        set_rule(self.multiworld.get_location("ORC: Cave of Ancient Murals", self.player), lambda state: state.can_reach_location("ORC: Floor 8 - Pirates' Hideout", self.player) and state.has("Electric Worm", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 9 - Wandering Zappy", self.player), lambda state: state.can_reach_location("ORC: Cave of Ancient Murals", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 10 - Banquet of the Dead", self.player), lambda state: state.can_reach_location("ORC: Floor 9 - Wandering Zappy", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 11 - Improvements", self.player), lambda state: state.can_reach_location("ORC: Floor 10 - Banquet of the Dead", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 12 - Return of the Serpent", self.player), lambda state: state.can_reach_location("ORC: Floor 11 - Improvements", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 13 - Cursed Sea", self.player), lambda state: state.can_reach_location("ORC: Floor 12 - Return of the Serpent", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 14 - Sea of Atrocity", self.player), lambda state: state.can_reach_location("ORC: Floor 13 - Cursed Sea", self.player))
        set_rule(self.multiworld.get_location("ORC: Dr. Jaming", self.player), lambda state: state.can_reach_location("ORC: Floor 14 - Sea of Atrocity", self.player) and state.has("Secret Dragon Remedy", self.player) and state.has("Shell Talkie", self.player))
        set_rule(self.multiworld.get_location("ORC: Chapter 4 Complete", self.player), lambda state: state.can_reach_location("ORC: Dr. Jaming", self.player))        

        # ORC Star path floors
        set_rule(self.multiworld.get_location("ORC: Floor 15 - Looking for the Water Gem", self.player), lambda state: state.can_reach_location("ORC: Chapter 4 Complete", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 16 - Pirates' Revenge", self.player), lambda state: state.can_reach_location("ORC: Floor 15 - Looking for the Water Gem", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("ORC: Floor 17 - Death Ocean", self.player), lambda state: state.can_reach_location("ORC: Floor 16 - Pirates' Revenge", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("ORC: Sea Dragon", self.player), lambda state: state.can_reach_location("ORC: Floor 17 - Death Ocean", self.player) and state.has("Star Key", self.player))
        
        # Chapter 5 floors
        set_rule(self.multiworld.get_location("MG: Floor 1 - Battle with Griffon's Army", self.player), lambda state: state.can_reach_location("ORC: Chapter 4 Complete", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 2 - Mt. Gundor Wind", self.player), lambda state: state.can_reach_location("MG: Floor 1 - Battle with Griffon's Army", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 3 - Little Dragons on the Mountain", self.player), lambda state: state.can_reach_location("MG: Floor 2 - Mt. Gundor Wind", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 4 - Steam Goyone", self.player), lambda state: state.can_reach_location("MG: Floor 3 - Little Dragons on the Mountain", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 5 - Mountain Baddie Appears", self.player), lambda state: state.can_reach_location("MG: Floor 4 - Steam Goyone", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 6 - Magmanoff", self.player), lambda state: state.can_reach_location("MG: Floor 5 - Mountain Baddie Appears", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 7 - Danger Zone", self.player), lambda state: state.can_reach_location("MG: Floor 6 - Magmanoff", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 8 - Secret of Fire Mountain", self.player), lambda state: state.can_reach_location("MG: Floor 7 - Danger Zone", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 9 - Deathtrap", self.player), lambda state: state.can_reach_location("MG: Floor 8 - Secret of Fire Mountain", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 10 - Desperation on the Mountain", self.player), lambda state: state.can_reach_location("MG: Floor 9 - Deathtrap", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 11 - Pains in the Neck", self.player), lambda state: state.can_reach_location("MG: Floor 10 - Desperation on the Mountain", self.player))
        set_rule(self.multiworld.get_location("MG: Mount Gundor Peak", self.player), lambda state: state.can_reach_location("MG: Floor 11 - Pains in the Neck", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 12 - Walking the Path of Flames", self.player), lambda state: state.can_reach_location("MG: Mount Gundor Peak", self.player) and state.has("Time Bomb", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 13 - Burning Undead", self.player), lambda state: state.can_reach_location("MG: Floor 12 - Walking the Path of Flames", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 14 - Fire Dragon", self.player), lambda state: state.can_reach_location("MG: Floor 13 - Burning Undead", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 15 - Treasure Chest Danger Zone", self.player), lambda state: state.can_reach_location("MG: Floor 14 - Fire Dragon", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 16 - Road to the River of Flames", self.player), lambda state: state.can_reach_location("MG: Floor 15 - Treasure Chest Danger Zone", self.player))
        set_rule(self.multiworld.get_location("MG: Gaspard", self.player), lambda state: state.can_reach_location("MG: Floor 16 - Road to the River of Flames", self.player) and state.has("Fire Horn", self.player))
        set_rule(self.multiworld.get_location("MG: Chapter 5 Complete", self.player), lambda state: state.can_reach_location("MG: Gaspard", self.player))        
        # MG Star path floors
        set_rule(self.multiworld.get_location("MG: Floor 17 - Looking for the Fire Gem", self.player), lambda state: state.can_reach_location("MG: Chapter 5 Complete", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 18 - Explosive Hot Spring", self.player), lambda state: state.can_reach_location("MG: Floor 17 - Looking for the Fire Gem", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("MG: Floor 19 - Crazy Mountain", self.player), lambda state: state.can_reach_location("MG: Floor 18 - Explosive Hot Spring", self.player) and state.has("Star Key", self.player))
        set_rule(self.multiworld.get_location("MG: Inferno", self.player), lambda state: state.can_reach_location("MG: Floor 19 - Crazy Mountain", self.player) and state.has("Star Key", self.player))
        
        # Moon Flower Palace floors
        set_rule(self.multiworld.get_location("MFP: Floor 1 - Ancient Wind", self.player), lambda state: state.can_reach_location("MG: Chapter 5 Complete", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 2 - Card Warriors Gather", self.player), lambda state: state.can_reach_location("MFP: Floor 1 - Ancient Wind", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 3 - Dangerous Treasure", self.player), lambda state: state.can_reach_location("MFP: Floor 2 - Card Warriors Gather", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 4 - Zombie Zone", self.player), lambda state: state.can_reach_location("MFP: Floor 3 - Dangerous Treasure", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 5 - Feeling Out of Place", self.player), lambda state: state.can_reach_location("MFP: Floor 4 - Zombie Zone", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 6 - Living Statue", self.player), lambda state: state.can_reach_location("MFP: Floor 5 - Feeling Out of Place", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 7 - Danger Zone", self.player), lambda state: state.can_reach_location("MFP: Floor 6 - Living Statue", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 8 - Scary Women", self.player), lambda state: state.can_reach_location("MFP: Floor 7 - Danger Zone", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 9 - Hell Elephant", self.player), lambda state: state.can_reach_location("MFP: Floor 8 - Scary Women", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 10 - Crush the Undead", self.player), lambda state: state.can_reach_location("MFP: Floor 9 - Hell Elephant", self.player))
        set_rule(self.multiworld.get_location("MFP: Garden", self.player), lambda state: state.can_reach_location("MFP: Floor 10 - Crush the Undead", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 11 - Missing Gem Dealer", self.player), lambda state: state.can_reach_location("MFP: Garden", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 12 - Max's Longest Day", self.player), lambda state: state.can_reach_location("MFP: Floor 11 - Missing Gem Dealer", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 13 - Hell's Corridor", self.player), lambda state: state.can_reach_location("MFP: Floor 12 - Max's Longest Day", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 14 - Monica All Alone", self.player), lambda state: state.can_reach_location("MFP: Floor 13 - Hell's Corridor", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 15 - Raging Spirits", self.player), lambda state: state.can_reach_location("MFP: Floor 14 - Monica All Alone", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 16 - Lonely Machine", self.player), lambda state: state.can_reach_location("MFP: Floor 15 - Raging Spirits", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 17 - Nobility", self.player), lambda state: state.can_reach_location("MFP: Floor 16 - Lonely Machine", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 18 - Palace Watchdog", self.player), lambda state: state.can_reach_location("MFP: Floor 17 - Nobility", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 19 - Road to Memories", self.player), lambda state: state.can_reach_location("MFP: Floor 18 - Palace Watchdog", self.player))
        set_rule(self.multiworld.get_location("MFP: Alexandra's Room", self.player), lambda state: state.can_reach_location("MFP: Floor 19 - Road to Memories", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 20 - Final Trump Card", self.player), lambda state: state.can_reach_location("MFP: Alexandra's Room", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 21 - Elemental Party", self.player), lambda state: state.can_reach_location("MFP: Floor 20 - Final Trump Card", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 22 - Wandering Knight's Soul", self.player), lambda state: state.can_reach_location("MFP: Floor 21 - Elemental Party", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 23 - Beware Carelessness", self.player), lambda state: state.can_reach_location("MFP: Floor 22 - Wandering Knight's Soul", self.player))
        set_rule(self.multiworld.get_location("MFP: Floor 24 - Final Battle", self.player), lambda state: state.can_reach_location("MFP: Floor 23 - Beware Carelessness", self.player))
        
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("MG: Chapter 5 Complete", self.player)


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}
        name_to_dc2_code = {item.name: item.dc2_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_dc2_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].dc2_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_dc2_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                #"fishsanity": self.options.fishsanity.value,
                #"sphedasanity": self.options.sphedasanity.value,
                #"medalsanity": self.options.medalsanity.value,
                #"georamasanity": self.options.georamasanity.value,
                #"photosanity": self.options.photosanity.value,
                #"inventionsanity": self.options.inventionsanity.value,
                #"resource_pack_count": self.options.resource_pack_count.value,
                #"weapon_upgrade_pack_count": self.options.weapon_upgrade_pack_count.value,
                #"element_pack_count": self.options.element_pack_count.value,
                #"chapter_goal_count": self.options.chapter_goal_count.value,
                "abs_multiplier": self.options.abs_multiplier.value,
                "gilda_multiplier": self.options.gilda_multiplier.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "enable_enemy_randomiser": self.options.enable_enemy_randomiser.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
        }

        return slot_data
