from typing import List, Dict

from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, RegionType
from ..AutoWorld import World, WebWorld
from . import Items, Locations, Options
from .Rules import set_location_rules

class Hylics2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to settings up the Hylics 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]

class Hylics2World(World):
    """
    Hylics 2 is a surreal and unusual RPG, with an equally bizarre yet unique visual style. Play as Wayne, travel the world, and gather your allies to defeat the nefarious Gibby in his Hylemxylem!
    """
    game: str = "Hylics 2"
    web = Hylics2Web()

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    options: Options.options

    topology_present: bool = False
    remote_items: bool = True
    remote_start_inventory: bool = True

    data_version: 1

    def set_rules(self):
        set_location_rules(self.world, self.player)

    def generate_basic(self):

        # Generate item pool
        pool = []
        
        for i, data in Items.item_table.items():
            if data["count"] > 0:
                for j in range(data["count"]):
                    pool.append(Hylics2Item(data["name"], data["classification"], i, self.player))
        
        self.world.itempool += pool

        # Place victory item
        loc = Location(self.player, "Defeat Gibby", None, self.world.get_region("Hylemxylem", self.player))
        loc.place_locked_item(Item("Victory", ItemClassification.skip_balancing, None, self.player))
        self.world.get_region("Hylemxylem", self.player).locations.append(loc)

    #def fill_slot_data(self) -> Dict[str, Any]:

    def create_regions(self) -> None:

        region_table: Dict[int, Region] = {
            0: Region("Menu", RegionType.Generic, "Menu", self.player, self.world),
            1: Region("Afterlife", RegionType.Generic, "Afterlife", self.player, self.world),
            2: Region("Waynehouse", RegionType.Generic, "Waynehouse", self.player, self.world),
            3: Region("World", RegionType.Generic, "World", self.player, self.world),
            4: Region("New Muldul", RegionType.Generic, "New Muldul", self.player, self.world),
            5: Region("New Muldul Vault", RegionType.Generic, "New Muldul Vault", self.player, self.world),
            6: Region("Viewax", RegionType.Generic, "Viewax's Edifice", self.player, self.world),
            7: Region("Airship", RegionType.Generic, "Airship", self.player, self.world),
            8: Region("Arcade Island", RegionType.Generic, "Arcade Island", self.player, self.world),
            9: Region("TV Island", RegionType.Generic, "TV Island", self.player, self.world),
            10: Region("Juice Ranch", RegionType.Generic, "Juice Ranch", self.player, self.world),
            11: Region("Shield Facility", RegionType.Generic, "Shield Facility", self.player, self.world),
            12: Region("Worm Pod", RegionType.Generic, "Worm Pod", self.player, self.world),
            13: Region("Foglast", RegionType.Generic, "Foglast", self.player, self.world),
            14: Region("Drill Castle", RegionType.Generic, "Drill Castle", self.player, self.world),
            15: Region("Sage Labyrinth", RegionType.Generic, "Sage Labyrinth", self.player, self.world),
            16: Region("Sage Airship", RegionType.Generic, "Sage Airship", self.player, self.world),
            17: Region("Hylemxylem", RegionType.Generic, "Hylemxylem", self.player, self.world)
        }

        region_exit_table: Dict[int, List[str]] = {
            0: ["New Game"],

            1: ["To Waynehouse",
                "To New Muldul",
                "To Viewax",
                "To TV Island",
                "To Shield Facility",
                "To Worm Pod",
                "To Foglast",
                "To Sage Labyrinth",
                "To Hylemxylem"],

            2: ["To World",
                "To Afterlife",],

            3: ["To Waynehouse",
                "To New Muldul",
                "To Drill Castle",
                "To Viewax",
                "To Arcade Island",
                "To TV Island",
                "To Juice Ranch",
                "To Shield Facility",
                "To Worm Pod",
                "To Foglast",
                "To Sage Airship",
                "To Hylemxylem"],

            4: ["To World",
                "To Afterlife",
                "To New Muldul Vault"],
            
            5: ["To New Muldul"],
            
            6: ["To World",
                "To Afterlife"],
            
            7: ["To World"],
            
            8: ["To World"],
            
            9: ["To World",
                "To Afterlife"],
            
            10: ["To World"],
            
            11: ["To World",
                 "To Afterlife",
                 "To Worm Pod"],
            
            12: ["To Shield Facility",
                 "To Afterlife"],
            
            13: ["To World",
                 "To Afterlife"],
            
            14: ["To World",
                 "To Sage Labyrinth"],
            
            15: ["To Drill Castle",
                 "To Afterlife"],
            
            16: ["To World"],
            
            17: ["To World",
                "To Afterlife"]
        }

        for i, reg in region_table.items():
            self.world.regions.append(reg)
            for j, exits in region_exit_table.items():
                if j == i:
                    for k in exits:
                        ent = Entrance(self.player, k, reg)
                        reg.exits.append(ent)
                        ent.connect(reg)

        for l, data in Locations.location_table.items():
            region_table[data["region"]].locations\
                .append(Hylics2Location(self.player, data["name"], l, region_table[data["region"]]))

    

class Hylics2Location(Location):
    game: str = "Hylics 2"

class Hylics2Item(Item):
    game: str = "Hylics 2"