import typing
import os
import json
from .Items import item_table, cannon_item_table, SM64Item
from .Locations import location_table, SM64Location
from .Options import sm64_options
from .Rules import set_rules
from .Regions import create_regions, sm64courses, sm64entrances_s, sm64_internalloc_to_string, sm64_internalloc_to_regionid
from BaseClasses import Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld

class SM64Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up SM64EX for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing"]
    )]


class SM64World(World):
    """ 
    The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons,
    combined with traditional Mario gameplay, visual style, and characters.
    """

    game: str = "Super Mario 64"
    topology_present = False

    web = SM64Web()

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 6
    required_client_version = (0, 3, 0)

    area_connections: typing.Dict[int, int]

    option_definitions = sm64_options

    def generate_early(self):
        self.topology_present = self.multiworld.AreaRandomizer[self.player].value

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.multiworld, self.player, self.area_connections)
        if self.topology_present:
            # Write area_connections to spoiler log
            for entrance, destination in self.area_connections.items():
                self.multiworld.spoiler.set_entrance(
                    sm64_internalloc_to_string[entrance] + " Entrance",
                    sm64_internalloc_to_string[destination],
                    'entrance', self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "1Up Mushroom":
            classification = ItemClassification.filler
        elif name == "Power Star":
            classification = ItemClassification.progression_skip_balancing
        else:
            classification = ItemClassification.progression
        item = SM64Item(name, classification, item_id, self.player)

        return item

    def generate_basic(self):
        staritem = self.create_item("Power Star")
        starcount = self.multiworld.AmountOfStars[self.player].value
        if (not self.multiworld.EnableCoinStars[self.player].value):
            starcount = max(35, self.multiworld.AmountOfStars[self.player].value - 15)
        starcount = max(starcount, self.multiworld.FirstBowserStarDoorCost[self.player].value,
                        self.multiworld.BasementStarDoorCost[self.player].value, self.multiworld.SecondFloorStarDoorCost[self.player].value,
                        self.multiworld.MIPS1Cost[self.player].value, self.multiworld.MIPS2Cost[self.player].value,
                        self.multiworld.StarsToFinish[self.player].value)
        self.multiworld.itempool += [staritem for i in range(0, starcount)]
        mushroomitem = self.create_item("1Up Mushroom") 
        self.multiworld.itempool += [mushroomitem for i in range(starcount, 120 - (15 if not self.multiworld.EnableCoinStars[self.player].value else 0))]

        if (not self.multiworld.ProgressiveKeys[self.player].value):
            key1 = self.create_item("Basement Key")
            key2 = self.create_item("Second Floor Key")
            self.multiworld.itempool += [key1, key2]
        else:
            key = self.create_item("Progressive Key")
            self.multiworld.itempool += [key, key]

        wingcap = self.create_item("Wing Cap")
        metalcap = self.create_item("Metal Cap")
        vanishcap = self.create_item("Vanish Cap")
        self.multiworld.itempool += [wingcap, metalcap, vanishcap]

        if (self.multiworld.BuddyChecks[self.player].value):
            self.multiworld.itempool += [self.create_item(name) for name, id in cannon_item_table.items()]
        else:
            self.multiworld.get_location("BoB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock BoB"))
            self.multiworld.get_location("WF: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WF"))
            self.multiworld.get_location("JRB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock JRB"))
            self.multiworld.get_location("CCM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock CCM"))
            self.multiworld.get_location("SSL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SSL"))
            self.multiworld.get_location("SL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SL"))
            self.multiworld.get_location("WDW: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WDW"))
            self.multiworld.get_location("TTM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock TTM"))
            self.multiworld.get_location("THI: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock THI"))
            self.multiworld.get_location("RR: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock RR"))

    def get_filler_item_name(self) -> str:
        return "1Up Mushroom"

    def fill_slot_data(self):
        return {
            "AreaRando": self.area_connections,
            "FirstBowserDoorCost": self.multiworld.FirstBowserStarDoorCost[self.player].value,
            "BasementDoorCost": self.multiworld.BasementStarDoorCost[self.player].value,
            "SecondFloorDoorCost": self.multiworld.SecondFloorStarDoorCost[self.player].value,
            "MIPS1Cost": self.multiworld.MIPS1Cost[self.player].value,
            "MIPS2Cost": self.multiworld.MIPS2Cost[self.player].value,
            "StarsToFinish": self.multiworld.StarsToFinish[self.player].value,
            "DeathLink": self.multiworld.death_link[self.player].value,
        }

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"AP_{self.multiworld.seed_name}_P{self.player}_{self.multiworld.get_file_safe_player_name(self.player)}.apsm64ex"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def modify_multidata(self, multidata):
        if self.topology_present:
            er_hint_data = {}
            for entrance, destination in self.area_connections.items():
                regionid = sm64_internalloc_to_regionid[destination]
                region = self.multiworld.get_region(sm64courses[regionid], self.player)
                for location in region.locations:
                    er_hint_data[location.address] = sm64_internalloc_to_string[entrance]
            multidata['er_hint_data'][self.player] = er_hint_data
