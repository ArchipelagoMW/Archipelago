import typing
import os
import json
from .Items import item_table, cannon_item_table, SM64Item
from .Locations import location_table, SM64Location
from .Options import sm64_options
from .Rules import set_rules
from .Regions import create_regions, sm64courses
from BaseClasses import Region, RegionType, Entrance, Item, MultiWorld, Tutorial
from ..AutoWorld import World, WebWorld

client_version = 1


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
    forced_auto_forfeit = False

    area_connections: typing.Dict[int, int]

    options = sm64_options

    def generate_early(self):
        self.topology_present = self.world.AreaRandomizer[self.player].value

    def create_regions(self):
        create_regions(self.world,self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.world, self.player, self.area_connections)
        if self.topology_present:
            # Write area_connections to spoiler log
            for painting_id, course_id in self.area_connections.items():
                self.world.spoiler.set_entrance(
                    sm64courses[painting_id] + " Painting",
                    sm64courses[course_id],
                    'entrance', self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = SM64Item(name, name != "1Up Mushroom", item_id, self.player)
        if name == "Power Star": 
            item.skip_in_prog_balancing = True
        return item

    def generate_basic(self):
        staritem = self.create_item("Power Star")
        starcount = min(self.world.StarsToFinish[self.player].value + self.world.ExtraStars[self.player].value,120)
        if (not self.world.EnableCoinStars[self.player].value):
            starcount = max(starcount - 15,self.world.StarsToFinish[self.player].value)
        self.world.itempool += [staritem for i in range(0,starcount)]
        mushroomitem = self.create_item("1Up Mushroom") 
        self.world.itempool += [mushroomitem for i in range(starcount,120 - (15 if not self.world.EnableCoinStars[self.player].value else 0))]

        if (not self.world.ProgressiveKeys[self.player].value):
            key1 = self.create_item("Basement Key")
            key2 = self.create_item("Second Floor Key")
            self.world.itempool += [key1,key2]
        else:
            key = self.create_item("Progressive Key")
            self.world.itempool += [key,key]

        wingcap = self.create_item("Wing Cap")
        metalcap = self.create_item("Metal Cap")
        vanishcap = self.create_item("Vanish Cap")
        self.world.itempool += [wingcap,metalcap,vanishcap]

        if (self.world.BuddyChecks[self.player].value):
            self.world.itempool += [self.create_item(name) for name, id in cannon_item_table.items()]
        else:
            self.world.get_location("BoB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock BoB"))
            self.world.get_location("WF: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WF"))
            self.world.get_location("JRB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock JRB"))
            self.world.get_location("CCM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock CCM"))
            self.world.get_location("SSL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SSL"))
            self.world.get_location("SL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SL"))
            self.world.get_location("WDW: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WDW"))
            self.world.get_location("TTM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock TTM"))
            self.world.get_location("THI: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock THI"))
            self.world.get_location("RR: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock RR"))

    def get_filler_item_name(self) -> str:
        return "1Up Mushroom"

    def fill_slot_data(self):
        return {
            "AreaRando": self.area_connections,
            "StarsToFinish": self.world.StarsToFinish[self.player].value,
            "DeathLink": self.world.death_link[self.player].value,
        }

    def generate_output(self, output_directory: str):
        if self.world.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.world.get_locations()},
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
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_file_safe_player_name(self.player)}.apsm64ex"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def modify_multidata(self, multidata):
        if self.topology_present:
            er_hint_data = {}
            for painting_id, course_id in self.area_connections.items():
                region = self.world.get_region(sm64courses[course_id], self.player)
                for location in region.locations:
                    er_hint_data[location.address] = sm64courses[painting_id]
            multidata['er_hint_data'][self.player] = er_hint_data
