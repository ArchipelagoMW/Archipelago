# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import MedievilItem, MedievilItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import MedievilLocation, MedievilLocationCategory, location_tables, location_dictionary
from .Options import MedievilOption

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
        self.enabled_location_categories.add(MedievilLocationCategory.LEVEL_END),
        self.enabled_location_categories.add(MedievilLocationCategory.CHALICE),
        self.enabled_location_categories.add(MedievilLocationCategory.FUN),
        self.enabled_location_categories.add(MedievilLocationCategory.PROGRESSION),

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "MainWorld"
        ]})
        
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            print(f"Connecting {from_region} to {to_region} Using entrance: " + connection.name)
            
        create_connection("Menu", "MainWorld")
        
        
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
        print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        print("adding region: " + region_name)
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
                "guaranteed_items": self.options.guaranteed_items.value,
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