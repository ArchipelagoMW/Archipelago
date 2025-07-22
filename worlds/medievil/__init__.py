# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification, CollectionState
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import MedievilItem, MedievilItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import MedievilLocation, MedievilLocationCategory, location_tables, location_dictionary
from .Options import MedievilOption, GoalOptions

class MedievilWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Medievil randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RiezaHughes"]
    )

    tutorials = [setup_en]


class MedievilWorld(World):
    """
    Medievil is a game about an idiot who died and was accidentally resurrected as a one eyed bandit to fight knockoff voldemort.
    """

    game: str = "Medievil"
    explicit_indirect_conditions = False
    options_dataclass = MedievilOption
    options: MedievilOption
    topology_present: bool = True
    web = MedievilWeb()
    data_version = 0
    base_id = 1230000
    enabled_location_categories: Set[MedievilLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = MedievilItem.get_name_to_id()
    location_name_to_id = MedievilLocation.get_name_to_id()
    item_name_groups = {
    }
    item_descriptions = item_descriptions
    


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()


    def generate_early(self):
        self.enabled_location_categories.add(MedievilLocationCategory.PROGRESSION),
        self.enabled_location_categories.add(MedievilLocationCategory.WEAPON),
        self.enabled_location_categories.add(MedievilLocationCategory.CHALICE),
        self.enabled_location_categories.add(MedievilLocationCategory.FUN),
        self.enabled_location_categories.add(MedievilLocationCategory.LEVEL_END),    

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        
        regions["Menu"] = self.create_region("Menu", [])
        
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Map",
            "Hall of Heroes",
            "Dan's Crypt",
            "The Graveyard",
            "Return to the Graveyard",
            "Cemetery Hill",
            "The Hilltop Mausoleum",
            "Scarecrow Fields",
            "Ant Hill",
            "The Crystal Caves",
            "The Lake",
            "Pumpkin Gorge",
            "Pumpkin Serpent",
            "The Sleeping Village",
            "Pools of the Ancient Dead",
            "Asylum Grounds",
            "Inside the Asylum",
            "Enchanted Earth",
            "The Gallows Gauntlet",
            "The Haunted Ruins",
            "The Ghost Ship",
            "The Entrance Hall",
            "The Time Device",
            "Zaroks Lair"
        ]})
        
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            
        create_connection("Menu", "Map")
        
        # Can go from the map to every location
        create_connection("Map", "Dan's Crypt")
        create_connection("Map", "The Graveyard")
        create_connection("Map", "Return to the Graveyard")
        create_connection("Map", "Cemetery Hill")
        create_connection("Map", "The Hilltop Mausoleum")
        create_connection("Map", "Scarecrow Fields")
        create_connection("Map", "The Crystal Caves")
        create_connection("Map", "The Lake")
        create_connection("Map", "Pumpkin Gorge")
        create_connection("Map", "Pumpkin Serpent")
        create_connection("Map", "The Sleeping Village")
        create_connection("Map", "Pools of the Ancient Dead")
        create_connection("Map", "Asylum Grounds")
        create_connection("Map", "Inside the Asylum")
        create_connection("Map", "Enchanted Earth")
        create_connection("Map", "The Gallows Gauntlet")
        create_connection("Map", "The Haunted Ruins")
        create_connection("Map", "The Ghost Ship")
        create_connection("Map", "The Entrance Hall")
        create_connection("Map", "The Time Device")
        create_connection("Map", "Zaroks Lair")
        
        # can go from every location back to the map
        create_connection("Dan's Crypt", "Map")
        create_connection("The Graveyard", "Map")
        create_connection("Return to the Graveyard", "Map")
        create_connection("Cemetery Hill", "Map")
        create_connection("The Hilltop Mausoleum", "Map")
        create_connection("Scarecrow Fields", "Map")        
        create_connection("Enchanted Earth", "Map")
        create_connection("The Crystal Caves", "Map")
        create_connection("The Lake", "Map")
        create_connection("Pumpkin Gorge", "Map")
        create_connection("Pumpkin Serpent", "Map")
        create_connection("The Sleeping Village", "Map")
        create_connection("Pools of the Ancient Dead", "Map")
        create_connection("Asylum Grounds", "Map")
        create_connection("Inside the Asylum", "Map")
        create_connection("The Gallows Gauntlet", "Map")
        create_connection("The Haunted Ruins", "Map")
        create_connection("The Ghost Ship", "Map")
        create_connection("The Entrance Hall", "Map")
        create_connection("The Time Device", "Map")        
        
        # create_connection("Dan's Crypt", "The Graveyard")
        # create_connection("The Graveyard", "Cemetery Hill")
        # create_connection("Cemetery Hill", "The Hilltop Mausoleum")
        # create_connection("The Hilltop Mausoleum", "Return to the Graveyard")
        
        # create_connection("Return to the Graveyard", "Scarecrow Fields")
        
        # # dragon gem 1 + Shadow Artefact path
        # create_connection("Scarecrow Fields", "The Sleeping Village")
        # create_connection("The Sleeping Village", "Asylum Grounds")
        # create_connection("Asylum Grounds", "Inside the Asylum")
        
        # # dragon gem 2 path
        # create_connection("Scarecrow Fields", "Pumpkin Gorge")
        # create_connection("Pumpkin Gorge", "Pumpkin Serpent")
        
        # create_connection("Return to the Graveyard", "Enchanted Earth")
        # # needs shadow artefact
        # create_connection("Enchanted Earth", "Pools of the Ancient Dead")
        
        # # Requires Witches Talisman
        create_connection("Enchanted Earth", "Ant Hill")
        
        # create_connection("Pools of the Ancient Dead", "The Lake")
        # create_connection("The Lake", "The Crystal Caves")
        
        # # Needs dragon armour
        # create_connection("The Crystal Caves", "The Gallows Gauntlet")
        # create_connection("The Gallows Gauntlet", "The Haunted Ruins")
        # create_connection("The Haunted Ruins", "The Ghost Ship")
        # create_connection("The Ghost Ship", "The Entrance Hall")
        # create_connection("The Entrance Hall", "The Time Device")
        # create_connection("The Time Device", "Zaroks Lair")
        
        # # hall of heroes
        create_connection("The Graveyard", "Hall of Heroes")
        create_connection("Return to the Graveyard", "Hall of Heroes")
        create_connection("Cemetery Hill", "Hall of Heroes")        
        create_connection("The Hilltop Mausoleum", "Hall of Heroes")        
        create_connection("Scarecrow Fields", "Hall of Heroes")        
        create_connection("Ant Hill", "Hall of Heroes")        
        create_connection("The Crystal Caves", "Hall of Heroes")
        create_connection("The Lake", "Hall of Heroes")
        create_connection("Pumpkin Gorge", "Hall of Heroes")
        create_connection("Pumpkin Serpent", "Hall of Heroes")
        create_connection("The Sleeping Village", "Hall of Heroes")
        create_connection("Pools of the Ancient Dead", "Hall of Heroes")
        create_connection("Asylum Grounds", "Hall of Heroes")
        create_connection("Inside the Asylum", "Hall of Heroes")
        create_connection("Enchanted Earth", "Hall of Heroes")
        create_connection("The Gallows Gauntlet", "Hall of Heroes")
        create_connection("The Haunted Ruins", "Hall of Heroes")
        create_connection("The Ghost Ship", "Hall of Heroes")
        create_connection("The Entrance Hall", "Hall of Heroes")
        create_connection("The Time Device", "Hall of Heroes")
        
        create_connection("Hall of Heroes", "Map") 
                                                                                                                   
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if location.category in self.enabled_location_categories:
                new_location = MedievilLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                event_item = self.create_item(location.default_item)
                new_location = MedievilLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)

            new_region.locations.append(new_location)
            
        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        
        randomized_location_count = 0 
        for location in self.multiworld.get_locations(self.player):
            if not location.locked and location.address is not None:
                randomized_location_count += 1
        
        print(f"Requesting itempool size for randomized locations: {randomized_location_count}")
        
        # Call BuildItemPool to get a list of item NAMES (strings)
        item_names_to_add = BuildItemPool(randomized_location_count, self.options)
        
        generated_items: List[Item] = []
        for item_name in item_names_to_add:
            new_item = self.create_item(item_name)
            generated_items.append(new_item)
            
        print(f"Created item pool size: {len(generated_items)}")

        # Add the generated MedievilItem objects to the multiworld's item pool
        self.multiworld.itempool.extend(generated_items)
        
        print("Final Item pool: ")
        for item in self.multiworld.itempool:
            print(item.name)

    def create_item(self, name: str) -> Item:
        item_data = item_dictionary.get(name)
        
        if not item_data:
            # Fallback for unknown items. This indicates a data inconsistency.
            print(f"Warning: Attempted to create unknown item: {name}. Falling back to filler.")
            return MedievilItem(name, ItemClassification.filler, None, self.player)

        # Determine the Archipelago ItemClassification based on MedievilItemData.
        item_classification: ItemClassification

        if item_data.progression or item_data.category == MedievilItemCategory.PROGRESSION or item_data.category == MedievilItemCategory.LEVEL_END:
            item_classification = ItemClassification.progression
        elif item_data.category == MedievilItemCategory.FUN or item_data.category == MedievilItemCategory.WEAPON or item_data.category == MedievilItemCategory.CHALICE:
            item_classification = ItemClassification.useful
        else: # Default for FILLER or other categories not explicitly useful/progression
            item_classification = ItemClassification.filler

        return MedievilItem(name, item_classification, MedievilItem.get_name_to_id()[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Gold (50)" # this clearly needs looked into
    
    def set_rules(self) -> None:
        
        def is_level_cleared(self, location: str, state: CollectionState):        
            return state.can_reach_location("Cleared: " + location, self.player)
        
        def is_boss_defeated(self, boss: str, state: CollectionState): # can used later
            return state.has("Boss: " + boss, self.player, 1)
        
        def has_keyitem_required(self, item: str, state: CollectionState):
            return state.has("Key Item: " + item, self.player, 1)

        def has_weapon_required(self, weapon: str, state: CollectionState):
            return state.has("Equipment: " + weapon, self.player)
        
        def has_number_of_chalices(count, state: CollectionState):
            
            chaliceList = [
                "Chalice: The Graveyard"
                "Chalice: Cemetery Hill"
                "Chalice: The Hilltop Mausoleum"
                "Chalice: Return to the Graveyard"
                "Chalice: Scarecrow Fields"
                "Chalice: Ant Hill"
                "Chalice: Enchanted Earth"
                "Chalice: Sleeping Village"
                "Chalice: Pools of the Ancient Dead"
                "Chalice: The Lake"
                "Chalice: The Crystal Caves"
                "Chalice: The Gallows Gauntlet"
                "Chalice: Asylum Grounds"
                "Chalice: Inside the Asylum"
                "Chalice: Pumpkin Gorge"
                "Chalice: Pumpkin Serpent"
                "Chalice: The Haunted Ruins"
                "Chalice: Ghost Ship"
                "Chalice: The Entrance Hall"
                "Chalice: The Time Device"
            ]
            
            matches = []
            for chalice in state.has:
                if chalice in chaliceList:
                    matches.append(chalice)
            return matches == count
            
            
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                    set_rule(location, lambda state: True)
                    
        if self.options.goal.value == GoalOptions.DEFEAT_ZAROK:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Cleared: Zaroks Lair", self.player)
        
        
        # Map rules
        
        set_rule(self.get_entrance("Map -> The Graveyard"), lambda state: is_level_cleared(self, "Dan's Crypt" , state)) 
        set_rule(self.get_entrance("Map -> Cemetery Hill"), lambda state: is_level_cleared(self, "The Graveyard" , state)) 
        set_rule(self.get_entrance("Map -> The Hilltop Mausoleum"), lambda state: is_level_cleared(self, "Cemetery Hill" , state)) 
        set_rule(self.get_entrance("Map -> Return to the Graveyard"), lambda state: is_level_cleared(self, "The Hilltop Mausoleum" , state)) 
        set_rule(self.get_entrance("Map -> Enchanted Earth"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state))
        set_rule(self.get_entrance("Map -> Scarecrow Fields"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state)) 
        set_rule(self.get_entrance("Map -> The Sleeping Village"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state)) 
        set_rule(self.get_entrance("Map -> Pumpkin Gorge"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state)) 
        set_rule(self.get_entrance("Map -> Asylum Grounds"), lambda state: is_level_cleared(self, "Sleeping Village" , state)) 
        set_rule(self.get_entrance("Map -> Inside the Asylum"), lambda state: is_level_cleared(self, "Asylum Grounds" , state)) 
        set_rule(self.get_entrance("Map -> Pumpkin Serpent"), lambda state: is_level_cleared(self, "Pumpkin Gorge" , state)) 
        set_rule(self.get_entrance("Map -> Pools of the Ancient Dead"), lambda state: is_level_cleared(self, "Enchanted Earth" , state)) 
        set_rule(self.get_entrance("Map -> The Lake"), lambda state: is_level_cleared(self, "Pools of the Ancient Dead" , state)) 
        set_rule(self.get_entrance("Map -> The Crystal Caves"), lambda state: is_level_cleared(self, "The Lake" , state)) 
        set_rule(self.get_entrance("Map -> The Gallows Gauntlet"), lambda state: is_level_cleared(self, "The Crystal Caves" , state)) 
        set_rule(self.get_entrance("Map -> The Haunted Ruins"), lambda state: is_level_cleared(self, "The Gallows Gauntlet" , state)) 
        set_rule(self.get_entrance("Map -> The Ghost Ship"), lambda state: is_level_cleared(self, "The Haunted Ruins" , state)) 
        set_rule(self.get_entrance("Map -> The Entrance Hall"), lambda state: is_level_cleared(self, "Ghost Ship" , state)) 
        set_rule(self.get_entrance("Map -> The Time Device"), lambda state: is_level_cleared(self, "The Entrance Hall" , state)) 
        set_rule(self.get_entrance("Map -> Zaroks Lair"), lambda state: is_level_cleared(self, "The Time Device" , state))
        
        
        # hall of heroes rules
        
        # set_rule(self.get_entrance("The Graveyard -> Hall of Heroes"), lambda state: has_number_of_chalices(1, state)) 
        # set_rule(self.get_entrance("Return to the Graveyard -> Hall of Heroes"), lambda state: has_number_of_chalices(2, state)) 
        # set_rule(self.get_entrance("Cemetery Hill -> Hall of Heroes"), lambda state: has_number_of_chalices(3, state)) 
        # set_rule(self.get_entrance("The Hilltop Mausoleum -> Hall of Heroes",    self.player), lambda state: has_number_of_chalices(4, state)) 
        # set_rule(self.get_entrance("Scarecrow Fields -> Hall of Heroes",  self.player), lambda state: has_number_of_chalices(5, state)) 
        # set_rule(self.get_entrance("Ant Hill -> Hall of Heroes"), lambda state: has_number_of_chalices(6, state)) 
        # set_rule(self.get_entrance("The Crystal Caves -> Hall of Heroes"), lambda state: has_number_of_chalices(7, state)) 
        # set_rule(self.get_entrance("The Lake -> Hall of Heroes"), lambda state: has_number_of_chalices(8, state)) 
        # set_rule(self.get_entrance("Pumpkin Gorge -> Hall of Heroes"), lambda state: has_number_of_chalices(9, state)) 
        # set_rule(self.get_entrance("Pumpkin Serpent -> Hall of Heroes"), lambda state: has_number_of_chalices(10, state)) 
        # set_rule(self.get_entrance("The Sleeping Village -> Hall of Heroes"), lambda state: has_number_of_chalices(11, state)) 
        # set_rule(self.get_entrance("Pools of the Ancient Dead -> Hall of Heroes"), lambda state: has_number_of_chalices(12, state)) 
        # set_rule(self.get_entrance("Asylum Grounds -> Hall of Heroes"), lambda state: has_number_of_chalices(13, state)) 
        # set_rule(self.get_entrance("Inside the Asylum -> Hall of Heroes"), lambda state: has_number_of_chalices(14, state)) 
        # set_rule(self.get_entrance("Enchanted Earth -> Hall of Heroes"), lambda state: has_number_of_chalices(15, state)) 
        # set_rule(self.get_entrance("The Gallows Gauntlet -> Hall of Heroes"), lambda state: has_number_of_chalices(16, state)) 
        # set_rule(self.get_entrance("The Haunted Ruins -> Hall of Heroes"), lambda state: has_number_of_chalices(17, state)) 
        # set_rule(self.get_entrance("The Ghost Ship -> Hall of Heroes"), lambda state: has_number_of_chalices(18, state)) 
        # set_rule(self.get_entrance("The Entrance Hall -> Hall of Heroes"), lambda state: has_number_of_chalices(19, state)) 
        # set_rule(self.get_entrance("The Time Device -> Hall of Heroes"), lambda state: has_number_of_chalices(20, state)) 
        
        
        # Level Rules
        
        # set_rule(self.get_entrance("Dan's Crypt -> The Graveyard"), lambda state: is_level_cleared(self, "Dan's Crypt" , state))    

        # set_rule(self.get_entrance("The Graveyard -> Cemetery Hill"), lambda state: is_level_cleared(self, "The Graveyard" , state))

        # set_rule(self.get_entrance("Cemetery Hill -> The Hilltop Mausoleum"), lambda state: is_level_cleared(self, "Cemetery Hill" , state))

        # set_rule(self.get_entrance("The Hilltop Mausoleum -> Return to the Graveyard"), lambda state: is_level_cleared(self, "The Hilltop Mausoleum" , state))
        
        # set_rule(self.get_entrance("Return to the Graveyard -> Enchanted Earth"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state) and has_keyitem_required(self, "Skull Key" , state ) and has_keyitem_required(self, "Witches Talisman" , state ))
        
        # set_rule(self.get_entrance("Return to the Graveyard -> Scarecrow Fields"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state) and has_keyitem_required(self, "Skull Key" , state ))
        
        # set_rule(self.get_entrance("Scarecrow Fields -> The Sleeping Village"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state) and has_keyitem_required(self, "Landlords Bust" , state))

        # set_rule(self.get_entrance("The Sleeping Village -> Asylum Grounds"), lambda state: is_level_cleared(self, "The Sleeping Village" , state) and has_keyitem_required(self, "Crucifix Cast" , state)  and has_keyitem_required(self, "Landlords Bust" , state) and has_keyitem_required(self, "Crucifix" , state))
        
        # set_rule(self.get_entrance("Asylum Grounds -> Inside the Asylum"), lambda state: is_level_cleared(self, "Asylum Grounds" , state))
        
        # set_rule(self.get_entrance("Scarecrow Fields -> Pumpkin Gorge"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state))

        # set_rule(self.get_entrance("Pumpkin Gorge -> Pumpkin Serpent"), lambda state: is_level_cleared(self, "Pumpkin Gorge" , state) and has_keyitem_required(self, "Witches Talisman" , state))
        
        
        # # ant caves
        # # if self.options.exclude_ant_caves.value != 50:
        set_rule(self.get_entrance("Enchanted Earth -> Ant Hill"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state) and has_keyitem_required(self, "Witches Talisman" , state))

        # set_rule(self.get_entrance("Enchanted Earth -> Pools of the Ancient Dead"), lambda state: is_level_cleared(self, "Enchanted Earth" , state) and has_keyitem_required(self, "Shadow Talisman" , state))
        
        # set_rule(self.get_entrance("Pools of the Ancient Dead -> The Lake"), lambda state: is_level_cleared(self, "Pools of the Ancient Dead" , state))
        
        # set_rule(self.get_entrance("The Lake -> The Crystal Caves"), lambda state: is_level_cleared(self, "The Lake" , state))    
        
        # set_rule(self.get_entrance("The Crystal Caves -> The Gallows Gauntlet"), lambda state: is_level_cleared(self, "The Crystal Caves" , state) and has_keyitem_required(self, "Dragon Gem - Pumpkin Serpent" , state) and has_keyitem_required(self, "Dragon Gem - Inside the Asylum" , state))
                   
        # set_rule(self.get_entrance("The Gallows Gauntlet -> The Haunted Ruins"), lambda state: is_level_cleared(self, "The Gallows Gauntlet" , state))
        # set_rule(self.get_entrance("The Haunted Ruins -> The Ghost Ship"), lambda state: is_level_cleared(self, "The Haunted Ruins" , state))
        # set_rule(self.get_entrance("The Ghost Ship -> The Entrance Hall"), lambda state: is_level_cleared(self, "The Ghost Ship" , state))
        # set_rule(self.get_entrance("The Entrance Hall -> The Time Device"), lambda state: is_level_cleared(self, "The Entrance Hall" , state))
        # set_rule(self.get_entrance("The Time Device -> Zaroks Lair"), lambda state: is_level_cleared(self, "The Time Device" , state))
        
        

        from Utils import visualize_regions
        state = self.multiworld.get_all_state(False)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region("Menu"), "medievil_layout.puml", show_entrance_names=True,
                        regions_to_highlight=state.reachable_regions[self.player])        
        
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_medievil_code = {item.name: item.m_code for item in item_dictionary.values()}
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
                items_address.append(name_to_medievil_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].m_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_medievil_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "guaranteed_items": self.options.guaranteed_items,
                "goal": self.options.goal.value,
                "exclude_ant_caves": self.options.exclude_ant_caves.value,
                "exclude_dynamic_items": self.options.exclude_dynamic_items.value
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