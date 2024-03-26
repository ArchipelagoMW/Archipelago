from .Items import item_table, ShiversItem
from .Rules import set_rules
from BaseClasses import Item, Tutorial, Region, Location
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from . import Constants, Rules
from .Options import ShiversOptions


class ShiversWeb(WebWorld):
    tutorials = [Tutorial(
        "Shivers Setup Guide",
        "A guide to setting up Shivers for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["GodlFire", "Mathx2"]
    )]

class ShiversWorld(World):
    """
    Shivers is a horror themed point and click adventure. Explore the mysteries of Windlenot's Museum of the Strange and Unusual.
    """

    game: str = "Shivers"
    topology_present = False
    web = ShiversWeb()
    options_dataclass = ShiversOptions
    options: ShiversOptions

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = Constants.location_name_to_id
    
    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return ShiversItem(name, data.classification, data.code, self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region = self.multiworld.get_region(region_name, self.player)
        loc = ShiversLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        region.locations.append(loc)

    def create_regions(self) -> None:
        # Create regions
        for region_name, exits in Constants.region_info["regions"]:
            r = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(r)
            for exit_name in exits:
                r.create_exit(exit_name)


        # Bind mandatory connections
        for entr_name, region_name in Constants.region_info["mandatory_connections"]:
            e = self.multiworld.get_entrance(entr_name, self.player)
            r = self.multiworld.get_region(region_name, self.player)
            e.connect(r)
        
        # Locations
        # Build exclusion list
        self.removed_locations = set()
        if not self.options.include_information_plaques:
            self.removed_locations.update(Constants.exclusion_info["plaques"])
        if not self.options.elevators_stay_solved:
            self.removed_locations.update(Constants.exclusion_info["elevators"])
        if not self.options.early_lightning:
            self.removed_locations.update(Constants.exclusion_info["lightning"])

        # Add locations
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.multiworld.get_region(region_name, self.player)
            for loc_name in locations:
                if loc_name not in self.removed_locations:
                    loc = ShiversLocation(self.player, loc_name, self.location_name_to_id.get(loc_name, None), region)
                    region.locations.append(loc)

    def create_items(self) -> None:
        #Add items to item pool
        itempool = []
        for name, data in item_table.items():
            if data.type in {"pot", "key", "ability", "filler2"}:
                itempool.append(self.create_item(name))

        #Add Filler
        itempool += [self.create_item("Easier Lyre") for i in range(9)]

        #Extra filler is random between Heals and Easier Lyre. Heals weighted 95%.
        filler_needed = len(self.multiworld.get_unfilled_locations(self.player)) - 24 - len(itempool)
        itempool += [self.random.choices([self.create_item("Heal"), self.create_item("Easier Lyre")], weights=[95, 5])[0] for i in range(filler_needed)]


        #Place library escape items. Choose a location to place the escape item
        library_region = self.multiworld.get_region("Library", self.player)
        librarylocation = self.random.choice([loc for loc in library_region.locations if not loc.name.startswith("Accessible:")])

        #Roll for which escape items will be placed in the Library
        library_random = self.random.randint(1, 3)
        if library_random == 1: 
            librarylocation.place_locked_item(self.create_item("Crawling"))

            itempool = [item for item in itempool if item.name != "Crawling"]

        elif library_random == 2: 
            librarylocation.place_locked_item(self.create_item("Key for Library Room"))

            itempool = [item for item in itempool if item.name != "Key for Library Room"]
        elif library_random == 3: 
            librarylocation.place_locked_item(self.create_item("Key for Three Floor Elevator"))
            
            librarylocationkeytwo = self.random.choice([loc for loc in library_region.locations if not loc.name.startswith("Accessible:") and loc != librarylocation])
            librarylocationkeytwo.place_locked_item(self.create_item("Key for Egypt Room"))

            itempool = [item for item in itempool if item.name not in ["Key for Three Floor Elevator", "Key for Egypt Room"]]

        #If front door option is on, determine which set of keys will be used for lobby access and add front door key to item pool
        lobby_access_keys = 1
        if self.options.front_door_usable:
            lobby_access_keys = self.random.randint(1, 2)
            itempool += [self.create_item("Key for Front Door")]
        else:
            itempool += [self.create_item("Heal")]

        self.multiworld.itempool += itempool

        #Lobby acess:
        if self.options.lobby_access == 1:
            if lobby_access_keys == 1:
                self.multiworld.early_items[self.player]["Key for Underground Lake Room"] = 1
                self.multiworld.early_items[self.player]["Key for Office Elevator"] = 1
                self.multiworld.early_items[self.player]["Key for Office"] = 1
            elif lobby_access_keys == 2:
                self.multiworld.early_items[self.player]["Key for Front Door"] = 1
        if self.options.lobby_access == 2:
            if lobby_access_keys == 1:
                self.multiworld.local_early_items[self.player]["Key for Underground Lake Room"] = 1
                self.multiworld.local_early_items[self.player]["Key for Office Elevator"] = 1
                self.multiworld.local_early_items[self.player]["Key for Office"] = 1
            elif lobby_access_keys == 2:
                self.multiworld.local_early_items[self.player]["Key for Front Door"] = 1

    def pre_fill(self) -> None:
        # Prefills event storage locations with duplicate pots
        storagelocs = []
        storageitems = []
        self.storage_placements = []

        for locations in Constants.location_info["locations_by_region"].values():
            for loc_name in locations:
                if loc_name.startswith("Accessible: "):
                    storagelocs.append(self.multiworld.get_location(loc_name, self.player))

        storageitems += [self.create_item(name) for name, data in item_table.items() if data.type == 'potduplicate']
        storageitems += [self.create_item("Empty") for i in range(3)]

        state = self.multiworld.get_all_state(True)

        self.random.shuffle(storagelocs)
        self.random.shuffle(storageitems)
        
        fill_restrictive(self.multiworld, state, storagelocs.copy(), storageitems, True, True)

        self.storage_placements = {location.name: location.item.name for location in storagelocs}

    set_rules = set_rules

    def fill_slot_data(self) -> dict:

        return {
            "storageplacements": self.storage_placements,
            "excludedlocations": {str(excluded_location).replace('ExcludeLocations(', '').replace(')', '') for excluded_location in self.multiworld.exclude_locations.values()},
            "elevatorsstaysolved": {self.options.elevators_stay_solved.value},
            "earlybeth": {self.options.early_beth.value},
            "earlylightning": {self.options.early_lightning.value},
        }


class ShiversLocation(Location):
    game = "Shivers"
