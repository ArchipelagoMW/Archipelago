# world/dark_souls_3/__init__.py
import json
import os

from .Options import dark_souls_options  # the options we defined earlier
from .Items import DarkSouls3Item  # data used below to add items to the World
from .Locations import DarkSouls3Location  # same as above
from .data.locations_data import dictionary_table
from ..AutoWorld import World
from BaseClasses import MultiWorld, Location, Region, Item, RegionType


class DarkSouls3World(World):
    """Insert description of the world/game here."""

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]
        return DarkSouls3Item(name, False, data, self.player)

    def create_regions(self):
        menu_region = Region("Menu", RegionType.Generic, "Menu", self.player)
        """
        cemetery_of_ash_region = Region("Cemetery Of Ash", RegionType.Generic, "Cemetery Of Ash", self.player)
        firelink_shrine_region = Region("Firelink Shrine", RegionType.Generic, "Firelink Shrine", self.player)
        high_wall_of_lothric_region = Region("High Wall of Lothric", RegionType.Generic, "High Wall of Lothric", self.player)
        undead_settlement_region = Region("Undead Settlement", RegionType.Generic, "Undead Settlement", self.player)
        road_of_sacrifices_region = Region("Road of Sacrifices", RegionType.Generic, "Road of Sacrifices", self.player)
        cathedral_of_the_deep_region = Region("Cathedral of the Deep", RegionType.Generic, "Cathedral of the Deep", self.player)
        farron_keep_region = Region("Farron Keep", RegionType.Generic, "Farron Keep", self.player)
        catacombs_of_carthus_region = Region("Catacombs of Carthus", RegionType.Generic, "Catacombs of Carthus", self.player)
        smouldering_lake_region = Region("Smouldering Lake", RegionType.Generic, "Smouldering Lake", self.player)
        irithyll_of_the_boreal_valley_region = Region("Irithyll of the Boreal Valley", RegionType.Generic, "Irithyll of the Boreal Valley", self.player)
        irithyll_dungeon_region = Region("Irithyll Dungeon", RegionType.Generic, "Irithyll Dungeon", self.player)
        profaned_capital_region = Region("Profaned Capital", RegionType.Generic, "Profaned Capital", self.player)
        anor_londo_region = Region("Anor Londo", RegionType.Generic, "Anor Londo", self.player)
        lothric_castle_region = Region("Lothric Castle", RegionType.Generic, "Lothric Castle", self.player)
        consumed_king_garden_region = Region("Consumed King's Garden", RegionType.Generic, "Consumed King's Garden", self.player)
        grand_archives_region = Region("Grand Archives", RegionType.Generic, "Grand Archives", self.player)
        untended_graves_region = Region("Untended Graves", RegionType.Generic, "Untended Graves", self.player)
        archdragon_peak_region = Region("Archdragon Peak", RegionType.Generic, "Archdragon Peak", self.player)
        """

        for name, address in self.location_name_to_id.items():
            location = Location(self.player, name, address, menu_region)
            menu_region.locations.append(location)
        self.world.regions += [menu_region]

    def create_items(self):
        for name, address in self.item_name_to_id.items():
            self.world.itempool += [self.create_item(name)]

    def generate_early(self):
        pass

    def set_rules(self):
        pass

    def generate_basic(self):
        pass

    def generate_output(self, output_directory: str):

        location_list = list()
        for location in self.world.get_filled_locations(self.player):
            if location.item.player == self.player:
                location_list.append(location.item.code)
            else:
                location_list.append(0)

        data = {
            "options": {
                "auto_equip": (True if self.world.auto_equip[self.player] else False),
                "lock_equip": (True if self.world.lock_equip[self.player] else False),
                "no_weapon_requirements": (True if self.world.no_weapon_requirements[self.player] else False),
            },
            "seed": self.world.seed_name,  # to verify the server's multiworld
            "slot": self.world.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locations": location_list,
            "itemsAddress": list(dictionary_table.values())
        }

        # generate the file
        filename = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}.json"
        with open(os.path.join(output_directory, filename), 'w') as outfile:
            json.dump(data, outfile)

    game: str = "Dark Souls III"  # name of the game/world
    options = dark_souls_options  # options the player can set
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False  # True if all items come from the server
    remote_start_inventory: bool = False  # True if start inventory comes from the server

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 0

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = 100000
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for id, name in enumerate(DarkSouls3Item.get_item_name_to_id(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(DarkSouls3Location.get_item_name_to_id(), base_id)}
