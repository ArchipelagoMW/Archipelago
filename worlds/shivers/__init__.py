from .Items import item_table, ShiversItem, get_full_item_list
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
        ["Godl-Fire"]
    )]

class ShiversWorld(World):
    """ 
     Shivers is a horror themed point and click adventure. Explore the mysteries of Windlenot's Museum of the Strange and Unusual.
    """

    game: str = "Shivers"
    topology_present = False
    web = ShiversWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = Constants.location_name_to_id
    data_version = 0

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return ShiversItem(name, data.classification, data.code, self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region = self.multiworld.get_region(region_name, self.player)
        loc = ShiversLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        region.locations.append(loc)

    #def create_event_item(self, name: str) -> None:
    #    item = self.create_item(name)
    #    item.classification = ItemClassification.progression
    #    return item

    option_definitions = Shivers_options

    

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

        # Add locations
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.multiworld.get_region(region_name, self.player)
            for loc_name in locations:
                loc = ShiversLocation(self.player, loc_name,
                                      self.location_name_to_id.get(loc_name, None), region)
                region.locations.append(loc)

    def create_items(self) -> Item:
        # Add pots
        pots = [self.create_item(name) for name, data in item_table.items() if data.type == 'pot']

        # Add keys
        keys = [self.create_item(name) for name, data in item_table.items() if data.type == 'key']

        #Add Filler
        filler = []
        filler += [self.create_item("Easier Lyre") for i in range(9)]
        filler += [self.create_item(name) for name, data in item_table.items() if data.type == 'filler2']

        self.multiworld.itempool += pots
        self.multiworld.itempool += keys
        self.multiworld.itempool += filler

        #Place crawling locally in the library to prevent softlock
        librarylocation = self.multiworld.random.choice(self.multiworld.get_region("Library", self.player).locations)
        while librarylocation.name.startswith("Accessible: "):
            librarylocation = self.multiworld.random.choice(self.multiworld.get_region("Library", self.player).locations)
        librarylocation.place_locked_item(self.create_item("Crawling"))

        #Lobby acess:
        if get_option_value(self.multiworld, self.player, "lobby_access") == 1:
            self.multiworld.early_items[self.player]["Key for Underground Lake Room"] = 1
            self.multiworld.early_items[self.player]["Key for Office Elevator"] = 1
            self.multiworld.early_items[self.player]["Key for Lobby"] = 1
        if get_option_value(self.multiworld, self.player, "lobby_access") == 2:
            self.multiworld.local_early_items[self.player]["Key for Underground Lake Room"] = 1
            self.multiworld.local_early_items[self.player]["Key for Office Elevator"] = 1
            self.multiworld.local_early_items[self.player]["Key for Lobby"] = 1

        


    #Prefills event storage locations with duplicate pots
    def pre_fill(self) -> None:
        global storage_placements
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
        
        fill_restrictive(self.multiworld, state, storagelocs.copy(), storageitems, True)

        self.storage_placements = {location.name: location.item.name for location in storagelocs}


    set_rules = set_rules
        

    def generate_output(self, output_directory: str) -> None:
        #print("Accessible: Storage: Desk Drawer -", self.multiworld.get_location("Accessible: Storage: Desk Drawer", self.player).item)
        #print("Accessible: Storage: Workshop Drawers -", self.multiworld.get_location("Accessible: Storage: Workshop Drawers", self.player).item)
        #print("Accessible: Storage: Library Cabinet -", self.multiworld.get_location("Accessible: Storage: Library Cabinet", self.player).item)
        #print("Accessible: Storage: Library Statue -", self.multiworld.get_location("Accessible: Storage: Library Statue", self.player).item)
        #print("Accessible: Storage: Slide -", self.multiworld.get_location("Accessible: Storage: Slide", self.player).item)
        #print("Accessible: Storage: Eagles Head -", self.multiworld.get_location("Accessible: Storage: Eagles Head", self.player).item)
        #print("Accessible: Storage: Clock Tower -", self.multiworld.get_location("Accessible: Storage: Clock Tower", self.player).item)
        #print("Accessible: Storage: Ocean -", self.multiworld.get_location("Accessible: Storage: Ocean", self.player).item)
        #print("Accessible: Storage: Egypt -", self.multiworld.get_location("Accessible: Storage: Egypt", self.player).item)
        #print("Accessible: Storage: Chinese Solitaire -", self.multiworld.get_location("Accessible: Storage: Chinese Solitaire", self.player).item)
        #print("Accessible: Storage: Tiki Hut -", self.multiworld.get_location("Accessible: Storage: Tiki Hut", self.player).item)
        #print("Accessible: Storage: Lyre -", self.multiworld.get_location("Accessible: Storage: Lyre", self.player).item)
        #print("Accessible: Storage: Alchemy -", self.multiworld.get_location("Accessible: Storage: Alchemy", self.player).item)
        #print("Accessible: Storage: UFO -", self.multiworld.get_location("Accessible: Storage: UFO", self.player).item)
        #print("Accessible: Storage: Skeleton -", self.multiworld.get_location("Accessible: Storage: Skeleton", self.player).item)
        #print("Accessible: Storage: Anansi -", self.multiworld.get_location("Accessible: Storage: Anansi", self.player).item)
        #print("Accessible: Storage: Hanging -", self.multiworld.get_location("Accessible: Storage: Hanging", self.player).item)
        #print("Accessible: Storage: Eagles Nest -", self.multiworld.get_location("Accessible: Storage: Eagles Nest", self.player).item)
        #print("Accessible: Storage: Tar River -", self.multiworld.get_location("Accessible: Storage: Tar River", self.player).item)
        #print("Accessible: Storage: Theater -", self.multiworld.get_location("Accessible: Storage: Theater", self.player).item)
        #print("Accessible: Storage: Greenhouse -", self.multiworld.get_location("Accessible: Storage: Greenhouse", self.player).item)
        #print("Accessible: Storage: Janitor Closet -", self.multiworld.get_location("Accessible: Storage: Janitor Closet", self.player).item)
        #print("Accessible: Storage: Skull Bridge -", self.multiworld.get_location("Accessible: Storage: Skull Bridge", self.player).item)

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
