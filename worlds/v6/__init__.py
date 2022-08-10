import typing
import os, json
from .Items import item_table, V6Item
from .Locations import location_table, V6Location
from .Options import v6_options
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld

client_version = 1


class V6Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up VVVVVV for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing"]
    )]


class V6World(World):
    """ 
     VVVVVV is a platform game all about exploring one simple mechanical idea - what if you reversed gravity instead of jumping?
    """ #Lifted from Store Page

    game: str = "VVVVVV"
    topology_present = False
    web = V6Web()

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 1

    area_connections: typing.Dict[int, int]
    area_cost_map: typing.Dict[int,int]

    music_map: typing.Dict[int,int]

    options = v6_options

    def create_regions(self):
        create_regions(self.world,self.player)

    def set_rules(self):
        self.area_connections = {}
        self.area_cost_map = {}
        set_rules(self.world, self.player, self.area_connections, self.area_cost_map)

    def create_item(self, name: str) -> Item:
        return V6Item(name, ItemClassification.progression, item_table[name], self.player)

    def generate_basic(self):
        trinkets = [self.create_item("Trinket " + str(i+1).zfill(2)) for i in range(0,20)]
        self.world.itempool += trinkets

        musiclist_o = [1,2,3,4,9,12]
        musiclist_s = musiclist_o.copy()
        if self.world.MusicRandomizer[self.player].value:
            self.world.random.shuffle(musiclist_s)
        self.music_map = dict(zip(musiclist_o, musiclist_s))

    def fill_slot_data(self):
        return {
            "MusicRando": self.music_map,
            "AreaRando": self.area_connections,
            "DoorCost": self.world.DoorCost[self.player].value,
            "AreaCostRando": self.area_cost_map,
            "DeathLink": self.world.death_link[self.player].value,
            "DeathLink_Amnesty": self.world.DeathLinkAmnesty[self.player].value
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
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_file_safe_player_name(self.player)}.apv6"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)
