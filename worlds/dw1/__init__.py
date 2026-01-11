# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DigimonWorldItem, DigimonWorldItemCategory, item_dictionary, key_item_names, key_item_categories, item_descriptions, _all_items, BuildItemPool
from .Locations import DigimonWorldLocation, DigimonWorldLocationCategory, location_tables, location_dictionary
from .Options import DigimonWorldOption
from .RecruitDigimon import recruit_digimon_list

class DigimonWorldWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Digimon World randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )


    tutorials = [setup_en]


class DigimonWorldWorld(World):
    """
    Digimon World is a game about raising digital monsters and recruiting allies to save the digital world.
    """

    game: str = "Digimon World"
    is_experimental = True
    options_dataclass = DigimonWorldOption
    options: DigimonWorldOption
    topology_present: bool = True
    web = DigimonWorldWeb()
    data_version = 0
    base_id = 690000
    enabled_location_categories: Set[DigimonWorldLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = DigimonWorldItem.get_name_to_id()
    location_name_to_id = DigimonWorldLocation.get_name_to_id()
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
        self.enabled_location_categories.add(DigimonWorldLocationCategory.MISC)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.EVENT)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.RECRUIT)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.CARD)
        


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}      
        regions["Menu"] = self.create_region("Menu", [])  
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Start Game","Consumable", "Cards",
            "Prosperity",
            "Digimon"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            #print(f"Connecting {from_region} to {to_region} Using entrance: " + connection.name)
        create_connection("Menu", "Start Game") 
        create_connection("Start Game", "Cards") 
        create_connection("Start Game", "Digimon") 
        create_connection("Start Game", "Prosperity") 


        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if location.category in self.enabled_location_categories:
                new_location = DigimonWorldLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region) 
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                new_location = DigimonWorldLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region)
                #event_item.code = None
                new_location.place_locked_item(event_item)
                print("Placing event: " + event_item.name + " in location: " + location.name)

            new_region.locations.append(new_location)
        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        itempool: List[DigimonWorldItem] = []
        itempoolSize = 0
        for location in self.multiworld.get_locations(self.player):
            if location.category in self.enabled_location_categories:
                itempoolSize += 1

        print(f"Itempool size: {itempoolSize}")

        for item in _all_items:
            if item.category == DigimonWorldItemCategory.SOUL:
                if item.name == "Agumon Soul":
                    continue
                itempool.append(self.create_item(item.name))
                itempoolSize -= 1
            
        
        print(f"Itempool size after adding souls: {itempoolSize}")
        filler_pool = BuildItemPool(self.multiworld, itempoolSize, self.options)
        for item in filler_pool:
            itempool.append(self.create_item(item.name))
            itempoolSize -= 1
        print(f"Itempool size after adding fillers: {itempoolSize}")

        if self.options.early_statcap.value:
            # print("Adding early stat cap item")
            location = self.multiworld.get_location("1 Prosperity", self.player)
            location.place_locked_item(self.create_item("Progressive Stat Cap"))
        location = self.multiworld.get_location("Start Game", self.player)
        location.place_locked_item(self.create_item("Agumon Soul"))
        # Add regular items to itempool
        print("Final itempool order:")
        for i, item in enumerate(itempool[:20]):
            print(f"  {i}: {item.name}")
        self.multiworld.itempool += itempool
        
    def create_item(self, name: str) -> Item:
        useful_categories = {
           # DigimonWorldItemCategory.CONSUMABLE,
           # DigimonWorldItemCategory.DV,
           # DigimonWorldItemCategory.MISC,
        }
        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category in key_item_categories:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DigimonWorldItem(name, item_classification, data, self.player)

    
    def get_filler_item_name(self) -> str:
        return "1000 Bits"
    
    def set_rules(self) -> None:  
        def get_recruited_digimon(self, state, current_digimon = None) -> List[str]:
            recruited_digimon = []
            for digimon in recruit_digimon_list: 
                if current_digimon:
                    if digimon.name == current_digimon or current_digimon in digimon.digimon_requirements:
                        continue
                if state.can_reach_location(f"{digimon.name}", self.player):
                    recruited_digimon.append(digimon.name)                
            return recruited_digimon
        def calculate_prosperity(self, state, current_digimon = None) -> int:
            current_prosperity = 1 #agumon always available
            recruit_confirmed = ["Agumon"]
            for iteration in range(10):
                added_this_round = False
                for digimon in recruit_digimon_list:  
                    requirements_met = True
                    if digimon.name in recruit_confirmed:
                        requirements_met = False
                        continue
                    if digimon.name == current_digimon: 
                        requirements_met = False
                        continue
                    if digimon.requires_soul:
                        if not state.has(digimon.name + " Soul", self.player):
                            requirements_met = False
                            continue
                    if digimon.prosperity_requirement > current_prosperity:
                        requirements_met = False
                        continue
                    for name in digimon.digimon_requirements:
                        if name not in recruit_confirmed:
                            requirements_met = False
                            break
                    if requirements_met:
                        recruit_confirmed.append(digimon.name)
                        current_prosperity += digimon.prosperity_value
                        added_this_round = True
                if not added_this_round:
                    break
            return current_prosperity
        def has_digimon_requirements(self, state, digimon) -> bool:
            existing_recruits = get_recruited_digimon(self, state)
            print("Checking requirements for" + digimon.name)
            print("Recruited digimon:")
            for requirement in digimon.digimon_requirements:
                if requirement not in existing_recruits:
                    return False
                print(requirement)
                current_prosperity = calculate_prosperity(self, state, digimon)
                print("Have " + str(current_prosperity) + " out of " + str(digimon.prosperity_requirement) + " prosperity") 
                if not current_prosperity >= digimon.prosperity_requirement:
                    return False
                if not digimon.requires_soul:
                    return True            
                has_soul = state.has(digimon.name + " Soul", self.player)
                print("Has required soul: " + str(has_soul))
                return has_soul
        def has_minimum_statcap(self, state, count) -> bool:
            return state.has("Progressive Stat Cap", self.player, count)
        if self.options.goal.value == 0:
            self.multiworld.completion_condition[self.player] = lambda state: calculate_prosperity(self, state) >= self.options.required_prosperity.value
        else:        
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Digitamamon", self.player)
        def set_indirect_rule(self, regionName, rule):
            region = self.multiworld.get_region("Digimon", self.player)
            entrance = self.multiworld.get_entrance("Digimon", self.player)
            location = self.multiworld.get_location(regionName, self.player)
            set_rule(location, rule)
            self.multiworld.register_indirect_condition(region, entrance)
        #for region in self.multiworld.get_regions(self.player):
        #    for location in region.locations:
        #            set_rule(location, lambda state: True)

        set_rule(self.multiworld.get_location("Start Game", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance(f"Start Game", self.player),lambda state: True)
        set_rule(self.multiworld.get_entrance(f"Digimon", self.player), lambda state: state.has("Agumon Soul", self.player))
        # print("Setting rules for:")
        # for digimon in recruit_digimon_list:
            # print(digimon.name)
            # if digimon.name != "Agumon":
                # set_indirect_rule(self, digimon.name, lambda state, s=self, d=digimon: has_digimon_requirements(s, state, d))
            # else:
                # print("Skipping agumon")
        set_indirect_rule(self, f"Betamon", lambda state: state.has("Betamon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Kunemon", lambda state: state.has("Kunemon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Palmon", lambda state: state.has("Palmon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Bakemon", lambda state: state.has("Bakemon Soul", self.player) and calculate_prosperity(self, state, "Bakemon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Centarumon", lambda state: state.has("Centarumon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Coelamon", lambda state: state.has("Coelamon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Gabumon", lambda state: state.has("Gabumon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Greymon", lambda state: state.has("Greymon Soul", self.player) and calculate_prosperity(self, state) >= 15 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Monochromon", lambda state: state.has("Monochromon Soul", self.player) and calculate_prosperity(self, state, "Monochromon") >= 6 and state.can_reach_location("Agumon", self.player))  
        set_indirect_rule(self, f"Meramon", lambda state: has_minimum_statcap(self, state, 1) and (state.has("Meramon Soul", self.player) and state.can_reach_location("Agumon", self.player) and (state.can_reach_location("Coelamon", self.player) or state.can_reach_location("Betamon", self.player))))
        set_indirect_rule(self, f"Elecmon", lambda state: state.has("Elecmon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Patamon", lambda state: state.has("Patamon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Biyomon", lambda state: state.has("Biyomon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Sukamon", lambda state: state.has("Sukamon Soul", self.player) and state.can_reach_location("Agumon", self.player) and state.can_reach_location("Meramon", self.player))
        set_indirect_rule(self, f"Tyrannomon", lambda state: state.has("Tyrannomon Soul", self.player) and state.can_reach_location("Centarumon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Birdramon", lambda state: state.has("Birdramon Soul", self.player) and calculate_prosperity(self, state, "Birdramon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Unimon", lambda state: state.has("Unimon Soul", self.player) and state.can_reach_location("Centarumon", self.player) and state.can_reach_location("Meramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Penguinmon", lambda state: state.has("Penguinmon Soul", self.player) and calculate_prosperity(self, state, "Penguinmon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Mojyamon", lambda state: state.has("Mojyamon Soul", self.player) and calculate_prosperity(self, state, "Mojyamon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Angemon", lambda state: state.has("Angemon Soul", self.player) and calculate_prosperity(self, state, "Angemon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Vegiemon", lambda state: state.has("Vegiemon Soul", self.player) and state.can_reach_location("Palmon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Shellmon", lambda state: state.has("Shellmon Soul", self.player) and calculate_prosperity(self, state, "Shellmon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Piximon", lambda state: has_minimum_statcap(self, state, 3) and (state.has("Piximon Soul", self.player) and state.can_reach_location("Agumon", self.player)))
        set_indirect_rule(self, f"Whamon", lambda state: state.has("Whamon Soul", self.player) and calculate_prosperity(self, state, "Whamon") >= 6 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Numemon", lambda state: state.has("Numemon Soul", self.player) and state.can_reach_location("Whamon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Giromon", lambda state: state.has("Giromon Soul", self.player) and state.can_reach_location("Whamon", self.player) and state.can_reach_location("Numemon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Andromon", lambda state: state.has("Andromon Soul", self.player) and state.can_reach_location("Whamon", self.player) and state.can_reach_location("Numemon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Frigimon", lambda state: state.has("Frigimon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Seadramon", lambda state: state.has("Seadramon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Garurumon", lambda state: state.has("Garurumon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Monzaemon", lambda state: state.has("Monzaemon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Kokatorimon", lambda state: state.has("Kokatorimon Soul", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Ogremon", lambda state: state.has("Ogremon Soul", self.player) and calculate_prosperity(self, state, "Ogremon") >= 6 and state.can_reach_location("Whamon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Kuwagamon", lambda state: state.has("Kuwagamon Soul", self.player) and state.can_reach_location("Seadramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Kabuterimon", lambda state: state.has("Kabuterimon Soul", self.player) and state.can_reach_location("Seadramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Drimogemon", lambda state: state.has("Drimogemon Soul", self.player) and state.can_reach_location("Meramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Vademon", lambda state: state.has("Vademon Soul", self.player) and calculate_prosperity(self, state, "Vademon") >= 45 and state.can_reach_location("Meramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"MetalMamemon", lambda state: state.has("MetalMamemon Soul", self.player) and state.can_reach_location("Whamon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"SkullGreymon", lambda state: state.has("SkullGreymon Soul", self.player) and calculate_prosperity(self, state, "SkullGreymon") >= 50 and state.can_reach_location("Greymon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Mamemon", lambda state: state.has("Mamemon Soul", self.player) and state.can_reach_location("Meramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Ninjamon", lambda state: state.has("Ninjamon Soul", self.player) and calculate_prosperity(self, state, "Ninjamon") >= 50 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Devimon", lambda state: state.has("Devimon Soul", self.player) and calculate_prosperity(self, state, "Devimon") >= 50 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Leomon", lambda state: state.has("Leomon Soul", self.player) and calculate_prosperity(self, state, "Leomon") >= 50 and state.can_reach_location("Meramon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Nanimon", lambda state: state.has("Nanimon Soul", self.player) and state.can_reach_location("Numemon", self.player) and state.can_reach_location("Leomon", self.player) and state.can_reach_location("Tyrannomon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"MetalGreymon", lambda state: state.has("MetalGreymon Soul", self.player) and calculate_prosperity(self, state, "MetalGreymon") >= 50 and state.can_reach_location("Greymon", self.player) and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Etemon", lambda state: state.has("Etemon Soul", self.player) and calculate_prosperity(self, state, "Etemon") >= 50 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Megadramon", lambda state: state.has("Megadramon Soul", self.player) and calculate_prosperity(self, state, "Megadramon") >= 50 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Airdramon", lambda state: state.has("Airdramon Soul", self.player) and calculate_prosperity(self, state, "Airdramon") >= 50 and state.can_reach_location("Agumon", self.player))
        set_indirect_rule(self, f"Digitamamon", lambda state: state.has("Digitamamon Soul", self.player) and calculate_prosperity(self, state, "Digitamamon") >= 50 and state.can_reach_location("Agumon", self.player))
        
        for card in [card for card in self.multiworld.get_locations(self.player) if card.category == DigimonWorldLocationCategory.CARD]:            
            if(card.name == "Machinedramon Card"):
                set_rule(card, lambda state, s=self: state.has("Digitamamon Soul", s.player) and calculate_prosperity(s, state) >= 50 and state.can_reach_location("Agumon", s.player))
                continue
            set_rule(card, lambda state, s=self: state.can_reach_location("Meramon", s.player))

        set_rule(self.multiworld.get_location(f"1 Prosperity", self.player), lambda state, s=self: state.can_reach_location("Agumon", s.player))
        for prosperity_location in self.multiworld.get_locations(self.player):   
            if prosperity_location.name.endswith("Prosperity"):                
                prosperity_value = int(prosperity_location.name.split(" ")[0])                     
                set_rule(prosperity_location, lambda state, pval=prosperity_value, s=self: calculate_prosperity(s, state) >= pval and state.can_reach_location("Agumon", s.player))

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_dw_code = {item.name: item.dw_code for item in item_dictionary.values()}
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
                items_address.append(name_to_dw_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].dw_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_dw_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "goal": self.options.goal.value,
                "required_prosperity": self.options.required_prosperity.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "exp_multiplier": self.options.exp_multiplier.value,
                "progressive_stats": self.options.progressive_stats.value,
                "random_starter": self.options.random_starter.value,
                "early_statcap": self.options.early_statcap.value,
                "random_techniques": self.options.random_techniques.value,
                "easy_monochromon": self.options.easy_monochromon.value,
                "fast_drimogemon": self.options.fast_drimogemon.value
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
