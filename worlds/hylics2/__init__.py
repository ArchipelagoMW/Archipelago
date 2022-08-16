from lib2to3.pgen2.token import OP
import logging
from typing import List, Dict, Any, Tuple

from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, RegionType
from ..AutoWorld import World, WebWorld
from . import Items, Locations, Options
from .Items import item_table
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
    description
    """
    game: str = "Hylics 2"
    web = Hylics2Web()

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    options: Options.hylics2_options

    topology_present: bool = False
    remote_items: bool = True
    remote_start_inventory: bool = True

    data_version: 1

    prefill_items: List[Item]

    set_rules = set_location_rules

    def generate_basic(self):

        # Generate item pool
        pool = []
        for item in item_table.values():
            for i in range(item["count"]):
                hylics2_item = self.create_item(item["name"])
                pool.append(hylics2_item)
        
        self.world.itempool += pool

    #def fill_slot_data(self) -> Dict[str, Any]:

    def create_item(self, name: str) -> Item:
        item_id: int = self.item_name_to_id[name]

        return Hylics2Item(name,
                           item_table[item_id]["classification"],
                           item_id, player=self.player)

    def create_regions(self) -> None:
        r = Region("Menu", RegionType.Generic, "Menu", self.player, self.world)
        r.exits = [Entrance(self.player, "New Game", r)]
        self.world.regions.append(r)

        r = Region("Afterlife", RegionType.Generic, "Afterlife", self.player, self.world)
        r.exits = [Entrance(self.player, "To Waynehouse", r), Entrance(self.player, "To New Muldul", r), Entrance(self.player, "To Viewax", r), Entrance(self.player, "To TV Island", r), Entrance(self.player, "To Shield Facility", r), Entrance(self.player, "To Worm Pod", r), Entrance(self.player, "To Foglast", r), Entrance(self.player, "To Sage Labyrinth", r), Entrance(self.player, "To Hylemxylem", r)]
        self.world.regions.append(r)

        r = Region("Waynehouse", RegionType.Generic, "Waynehouse", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        r = Region("World", RegionType.Generic, "World", self.player, self.world)
        r.exits = [Entrance(self.player, "To Waynehouse", r), Entrance(self.player, "To New Muldul", r), Entrance(self.player, "To Drill Castle", r), Entrance(self.player, "To Viewax", r), Entrance(self.player, "To Airship", r), Entrance(self.player, "To Arcade Island", r), Entrance(self.player, "To TV Island", r), Entrance(self.player, "To Juice Ranch", r), Entrance(self.player, "To Shield Facility", r), Entrance(self.player, "To Worm Pod", r), Entrance(self.player, "To Foglast", r), Entrance(self.player, "To Sage Airship", r), Entrance(self.player, "To Hylemxylem", r)]
        self.world.regions.append(r)

        r = Region("New Muldul", RegionType.Generic, "New Muldul", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r), Entrance(self.player, "To New Muldul Vault", r)]
        self.world.regions.append(r)

        r = Region("New Muldul Vault", RegionType.Generic, "New Muldul Vault", self.player, self.world)
        r.exits = [Entrance(self.player, "To New Muldul", r)]
        self.world.regions.append(r)

        r = Region("Viewax", RegionType.Generic, "Viewax's Edifice", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        r = Region("Airship", RegionType.Generic, "Airship", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r)]
        self.world.regions.append(r)

        r = Region("Arcade Island", RegionType.Generic, "Arcade Island", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r)]
        self.world.regions.append(r)

        r = Region("TV Island", RegionType.Generic, "TV Island", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        r = Region("Juice Ranch", RegionType.Generic, "Juice Ranch", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r)]
        self.world.regions.append(r)

        r = Region("Shield Facility", RegionType.Generic, "Shield Facility", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r), Entrance(self.player, "To Worm Pod", r)]
        self.world.regions.append(r)

        r = Region("Worm Pod", RegionType.Generic, "Worm Pod", self.player, self.world)
        r.exits = [Entrance(self.player, "To Shield Facility", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        r = Region("Foglast", RegionType.Generic, "Foglast", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        r = Region("Drill Castle", RegionType.Generic, "Drill Castle", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Sage Labyrinth", r)]
        self.world.regions.append(r)

        r = Region("Sage Labyrinth", RegionType.Generic, "Sage Labyrinth", self.player, self.world)
        r.exits = [Entrance(self.player, "To Drill Castle", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        r = Region("Sage Airship", RegionType.Generic, "Sage Airship", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r)]
        self.world.regions.append(r)

        r = Region("Hylemxylem", RegionType.Generic, "Hylemxylem", self.player, self.world)
        r.exits = [Entrance(self.player, "To World", r), Entrance(self.player, "To Afterlife", r)]
        self.world.regions.append(r)

        self.world.get_entrance("New Game", self.player)\
            .connect(self.world.get_region("Waynehouse", self.player))
        self.world.get_entrance("To Waynehouse", self.player)\
            .connect(self.world.get_region("Waynehouse", self.player))
        self.world.get_entrance("To New Muldul", self.player)\
            .connect(self.world.get_region("New Muldul", self.player))
        self.world.get_entrance("To Viewax", self.player)\
            .connect(self.world.get_region("Viewax", self.player))
        self.world.get_entrance("To TV Island", self.player)\
            .connect(self.world.get_region("TV Island", self.player))
        self.world.get_entrance("To Shield Facility", self.player)\
            .connect(self.world.get_region("Shield Facility", self.player))
        self.world.get_entrance("To Worm Pod", self.player)\
            .connect(self.world.get_region("Worm Pod", self.player))
        self.world.get_entrance("To Foglast", self.player)\
            .connect(self.world.get_region("Foglast", self.player))
        self.world.get_entrance("To Sage Labyrinth", self.player)\
            .connect(self.world.get_region("Sage Labyrinth", self.player))
        self.world.get_entrance("To Hylemxylem", self.player)\
            .connect(self.world.get_region("Hylemxylem", self.player))
        self.world.get_entrance("To World", self.player)\
            .connect(self.world.get_region("World", self.player))
        self.world.get_entrance("To Afterlife", self.player)\
            .connect(self.world.get_region("Afterlife", self.player))
        self.world.get_entrance("To Drill Castle", self.player)\
            .connect(self.world.get_region("Drill Castle", self.player))
        self.world.get_entrance("To Airship", self.player)\
            .connect(self.world.get_region("Airship", self.player))
        self.world.get_entrance("To Arcade Island", self.player)\
            .connect(self.world.get_region("Arcade Island", self.player))
        self.world.get_entrance("To Juice Ranch", self.player)\
            .connect(self.world.get_region("Juice Ranch", self.player))
        self.world.get_entrance("To Sage Airship", self.player)\
            .connect(self.world.get_region("Sage Airship", self.player))
        self.world.get_entrance("To New Muldul Vault", self.player)\
            .connect(self.world.get_region("New Muldul Vault", self.player))

        for l, data in Locations.location_table.items():
            reg = data["region"]
            match reg:
                case "Afterlife":
                    self.world.get_region("Afterlife", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Afterlife", self.player)))
                case "Waynehouse":
                    self.world.get_region("Waynehouse", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Waynehouse", self.player)))
                case "New Muldul":
                    self.world.get_region("New Muldul", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("New Muldul", self.player)))
                case "New Muldul Vault":
                    self.world.get_region("New Muldul Vault", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("New Muldul Vault", self.player)))
                case "Viewax":
                    self.world.get_region("Viewax", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Viewax", self.player)))
                case "Airship":
                    self.world.get_region("Airship", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Airship", self.player)))
                case "Arcade Island":
                    self.world.get_region("Arcade Island", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Arcade Island", self.player)))
                case "TV Island":
                    self.world.get_region("TV Island", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("TV Island", self.player)))
                case "Juice Ranch":
                    self.world.get_region("Juice Ranch", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Juice Ranch", self.player)))
                case "Worm Pod":
                    self.world.get_region("Worm Pod", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Worm Pod", self.player)))
                case "Foglast":
                    self.world.get_region("Foglast", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Foglast", self.player)))
                case "Drill Castle":
                    self.world.get_region("Drill Castle", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Drill Castle", self.player)))
                case "Sage Labyrinth":
                    self.world.get_region("Sage Labyrinth", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Sage Labyrinth", self.player)))
                case "Sage Airship":
                    self.world.get_region("Sage Airship", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Sage Airship", self.player)))
                case "Hylemxylem":
                    self.world.get_region("Hylemxylem", self.player).locations\
                        .append(Hylics2Location(self.player, data["name"], None, self.world.get_region("Hylemxylem", self.player)))


class Hylics2Location(Location):
    game: str = "Hylics 2"

class Hylics2Item(Item):
    game: str = "Hylics 2"