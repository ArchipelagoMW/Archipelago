import random

from .Items import item_table, ShiversItem
from .Rules import set_rules
from BaseClasses import Item, Tutorial, Region, Entrance, Location
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from . import Constants
from .Options import Shivers_options, get_option_value

client_version = 0


class ShiversWeb(WebWorld):
    tutorials = [Tutorial(
        "Shivers Setup Guide",
        "A guide to setting up Shivers for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["GodlFire, Mathx2, Mouse"]
    )]

class ShiversWorld(World):
    """ 
     Shivers is a horror themed point and click adventure. Explore the mysteries of Windlenot's Museum of the Strange and Unusual.
    """

    game: str = "Shivers"
    topology_present = False
    web = ShiversWeb()
    option_definitions = Shivers_options

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = Constants.location_name_to_id
    data_version = 0
    
    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return ShiversItem(name, data.classification, data.code, self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region = self.multiworld.get_region(region_name, self.player)
        loc = ShiversLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        region.locations.append(loc)

    def create_regions(self):
        # Create regions
        for region_name, exits in Constants.region_info["regions"]:
            r = Region(region_name, self.player, self.multiworld)
            for exit_name in exits:
                r.exits.append(Entrance(self.player, exit_name, r))
            self.multiworld.regions.append(r)

        # Bind mandatory connections
        for entr_name, region_name in Constants.region_info["mandatory_connections"]:
            e = self.multiworld.get_entrance(entr_name, self.player)
            r = self.multiworld.get_region(region_name, self.player)
            e.connect(r)
        
        # Locations
        # Build exclusion list
        self.removed_locations = set()
        if not self.multiworld.include_information_plaques[self.player]:
            self.removed_locations.update(Constants.exclusion_info["plaques"])

        # Add locations
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.multiworld.get_region(region_name, self.player)
            for loc_name in locations:
                if loc_name not in self.removed_locations:
                    loc = ShiversLocation(self.player, loc_name,
                                          self.location_name_to_id.get(loc_name, None), region)
                    region.locations.append(loc)
                

    def create_items(self) -> Item:
        # Add pots
        pots = [self.create_item(name) for name, data in item_table.items() if data.type == 'pot']

        # Add keys
        keys = [self.create_item(name) for name, data in item_table.items() if data.type == 'key']

        #Add abilities
        abilities = [self.create_item(name) for name, data in item_table.items() if data.type == 'ability']

        #Add Filler
        filler = []
        filler += [self.create_item("Easier Lyre") for i in range(49 - len(self.removed_locations))]
        filler += [self.create_item(name) for name, data in item_table.items() if data.type == 'filler2']

        #Place library escape items. Choose a location to place the escape item
        library_region = self.multiworld.get_region("Library", self.player)
        librarylocation = self.multiworld.random.choice([loc for loc in library_region.locations if not loc.name.startswith("Accessible:")])
        
        #Roll for which escape items will be placed in the Library
        library_random = self.random.randint(1, 3)
        if library_random == 1: 
            librarylocation.place_locked_item(self.create_item("Crawling"))

            abilities = [ability for ability in abilities if ability.name != "Crawling"]
        elif library_random == 2: 
            librarylocation.place_locked_item(self.create_item("Key for Library Room"))
            
            keys = [key for key in keys if key.name != "Key for Library Room"]
        elif library_random == 3: 
            librarylocation.place_locked_item(self.create_item("Key for Three Floor Elevator"))
            
            librarylocationkeytwo = self.multiworld.random.choice([loc for loc in library_region.locations if not loc.name.startswith("Accessible:") and loc != librarylocation])
            librarylocationkeytwo.place_locked_item(self.create_item("Key for Egypt Room"))
            
            keys = [key for key in keys if key.name not in ["Key for Three Floor Elevator", "Key for Egypt Room"]]
                


        #If front door option is on, determine which set of keys will be used for lobby access and add front door key to item pool
        lobby_access_keys = 1
        if self.multiworld.front_door_usable[self.player]:
            lobby_access_keys = library_random = self.random.randint(1, 2)
            keys += [self.create_item("Key for Front Door")]
        else:
            filler += [self.create_item("Easier Lyre")]

        self.multiworld.itempool += pots
        self.multiworld.itempool += keys
        self.multiworld.itempool += abilities
        self.multiworld.itempool += filler

        #Lobby acess:
        print(lobby_access_keys)
        if get_option_value(self.multiworld, self.player, "lobby_access") == 1:
            if lobby_access_keys == 1:
                self.multiworld.early_items[self.player]["Key for Underground Lake Room"] = 1
                self.multiworld.early_items[self.player]["Key for Office Elevator"] = 1
                self.multiworld.early_items[self.player]["Key for Office"] = 1
            elif lobby_access_keys == 2:
                self.multiworld.early_items[self.player]["Key for Front Door"] = 1
        if get_option_value(self.multiworld, self.player, "lobby_access") == 2:
            if lobby_access_keys == 1:
                self.multiworld.local_early_items[self.player]["Key for Underground Lake Room"] = 1
                self.multiworld.local_early_items[self.player]["Key for Office Elevator"] = 1
                self.multiworld.local_early_items[self.player]["Key for Office"] = 1
            elif lobby_access_keys == 2:
                self.multiworld.local_early_items[self.player]["Key for Front Door"] = 1

    #Prefills event storage locations with duplicate pots
    def pre_fill(self) -> None:
        storagelocs = []
        storageitems = []
        self.storage_placements = []
        
         
        for locations in Constants.location_info["locations_by_region"].values():
            for loc_name in locations:
                if loc_name.startswith("Accessible: "):
                    storagelocs.append(self.multiworld.get_location(loc_name, self.player))

        storageitems += [self.create_item(name) for name, data in item_table.items() if data.type == 'potduplicate']
        storageitems += [self.create_item("Empty") for i in range(3)]

        state = self.multiworld.get_all_state(False)

        self.multiworld.random.shuffle(storagelocs)
        self.multiworld.random.shuffle(storageitems)
        
        fill_restrictive(self.multiworld, state, storagelocs.copy(), storageitems, True, True)

        self.storage_placements = {location.name: location.item.name for location in storagelocs}


    set_rules = set_rules
        

    def generate_output(self, output_directory: str) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: Rules.lightning_capturable(state, self.player)
        return super().generate_output(output_directory)

    def _get_slot_data(self):
        return {
            'storageplacements': self.storage_placements,
            'excludedlocations': {str(excluded_location).replace('ExcludeLocations(', '').replace(')', '') for excluded_location in self.multiworld.exclude_locations.values()}
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        return slot_data

class ShiversLocation(Location):
    game = "Shivers"
