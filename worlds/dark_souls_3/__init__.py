# world/dark_souls_3/__init__.py
import json
import os

from random import randint
from .Options import dark_souls_options  # the options we defined earlier
from .Items import DarkSouls3Item  # data used below to add items to the World
from .Locations import DarkSouls3Location  # same as above
from .data.items_data import weapons_table, item_dictionary_table
from .data.locations_data import key_items_list, dictionary_table, cemetery_of_ash_table, fire_link_shrine_table, \
    high_wall_of_lothric, \
    undead_settlement_table, road_of_sacrifice_table, consumed_king_garden_table, cathedral_of_the_deep_table, \
    farron_keep_table, catacombs_of_carthus_table, smouldering_lake_table, irithyll_of_the_boreal_valley_table, \
    irithyll_dungeon_table, profaned_capital_table, anor_londo_table, lothric_castle_table, grand_archives_table, \
    untended_graves_table, archdragon_peak_table, firelink_shrine_bell_tower_table
from ..AutoWorld import World
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance
from ..generic.Rules import set_rule


class DarkSouls3World(World):
    """Insert description of the world/game here."""

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []

    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]
        return DarkSouls3Item(name, name in key_items_list, data, self.player)

    def create_regions(self):
        menu_region = Region("Menu", RegionType.Generic, "Menu", self.player)
        self.world.regions.append(menu_region)

        cemetery_of_ash_region = Region("Cemetery Of Ash", RegionType.Generic, "Cemetery Of Ash", self.player)
        for name, address in self.location_name_to_id.items():
            if cemetery_of_ash_table.get(name):
                location = Location(self.player, name, address, cemetery_of_ash_region)
                cemetery_of_ash_region.locations.append(location)
        self.world.regions.append(cemetery_of_ash_region)

        firelink_shrine_region = Region("Firelink Shrine", RegionType.Generic, "Firelink Shrine", self.player)
        for name, address in self.location_name_to_id.items():
            if fire_link_shrine_table.get(name):
                location = Location(self.player, name, address, firelink_shrine_region)
                firelink_shrine_region.locations.append(location)
        self.world.regions.append(firelink_shrine_region)

        firelink_shrine_bell_tower_region = Region("Firelink Shrine Bell Tower", RegionType.Generic, "Firelink Shrine Bell Tower", self.player)
        for name, address in self.location_name_to_id.items():
            if firelink_shrine_bell_tower_table.get(name):
                location = Location(self.player, name, address, firelink_shrine_bell_tower_region)
                firelink_shrine_bell_tower_region.locations.append(location)
        self.world.regions.append(firelink_shrine_bell_tower_region)

        high_wall_of_lothric_region = Region("High Wall of Lothric", RegionType.Generic, "High Wall of Lothric", self.player)
        for name, address in self.location_name_to_id.items():
            if high_wall_of_lothric.get(name):
                location = Location(self.player, name, address, high_wall_of_lothric_region)
                high_wall_of_lothric_region.locations.append(location)
        self.world.regions.append(high_wall_of_lothric_region)

        undead_settlement_region = Region("Undead Settlement", RegionType.Generic, "Undead Settlement", self.player)
        for name, address in self.location_name_to_id.items():
            if undead_settlement_table.get(name):
                location = Location(self.player, name, address, undead_settlement_region)
                undead_settlement_region.locations.append(location)
        self.world.regions.append(undead_settlement_region)

        road_of_sacrifices_region = Region("Road of Sacrifices", RegionType.Generic, "Road of Sacrifices", self.player)
        for name, address in self.location_name_to_id.items():
            if road_of_sacrifice_table.get(name):
                location = Location(self.player, name, address, road_of_sacrifices_region)
                road_of_sacrifices_region.locations.append(location)
        self.world.regions.append(road_of_sacrifices_region)

        consumed_king_garden_region = Region("Consumed King's Garden", RegionType.Generic, "Consumed King's Garden",
                                             self.player)
        for name, address in self.location_name_to_id.items():
            if consumed_king_garden_table.get(name):
                location = Location(self.player, name, address, consumed_king_garden_region)
                consumed_king_garden_region.locations.append(location)
        self.world.regions.append(consumed_king_garden_region)

        cathedral_of_the_deep_region = Region("Cathedral of the Deep", RegionType.Generic, "Cathedral of the Deep",
                                              self.player)
        for name, address in self.location_name_to_id.items():
            if cathedral_of_the_deep_table.get(name):
                location = Location(self.player, name, address, cathedral_of_the_deep_region)
                cathedral_of_the_deep_region.locations.append(location)
        self.world.regions.append(cathedral_of_the_deep_region)

        farron_keep_region = Region("Farron Keep", RegionType.Generic, "Farron Keep", self.player)
        for name, address in self.location_name_to_id.items():
            if farron_keep_table.get(name):
                location = Location(self.player, name, address, farron_keep_region)
                farron_keep_region.locations.append(location)
        self.world.regions.append(farron_keep_region)

        catacombs_of_carthus_region = Region("Catacombs of Carthus", RegionType.Generic, "Catacombs of Carthus", self.player)
        for name, address in self.location_name_to_id.items():
            if catacombs_of_carthus_table.get(name):
                location = Location(self.player, name, address, catacombs_of_carthus_region)
                catacombs_of_carthus_region.locations.append(location)
        self.world.regions.append(catacombs_of_carthus_region)

        smouldering_lake_region = Region("Smouldering Lake", RegionType.Generic, "Smouldering Lake", self.player)
        for name, address in self.location_name_to_id.items():
            if smouldering_lake_table.get(name):
                location = Location(self.player, name, address, smouldering_lake_region)
                smouldering_lake_region.locations.append(location)
        self.world.regions.append(smouldering_lake_region)

        irithyll_of_the_boreal_valley_region = Region("Irithyll of the Boreal Valley", RegionType.Generic,
                                                      "Irithyll of the Boreal Valley", self.player)
        for name, address in self.location_name_to_id.items():
            if irithyll_of_the_boreal_valley_table.get(name):
                location = Location(self.player, name, address, irithyll_of_the_boreal_valley_region)
                irithyll_of_the_boreal_valley_region.locations.append(location)
        self.world.regions.append(irithyll_of_the_boreal_valley_region)

        irithyll_dungeon_region = Region("Irithyll Dungeon", RegionType.Generic, "Irithyll Dungeon", self.player)
        for name, address in self.location_name_to_id.items():
            if irithyll_dungeon_table.get(name):
                location = Location(self.player, name, address, irithyll_dungeon_region)
                irithyll_dungeon_region.locations.append(location)
        self.world.regions.append(irithyll_dungeon_region)

        profaned_capital_region = Region("Profaned Capital", RegionType.Generic, "Profaned Capital", self.player)
        for name, address in self.location_name_to_id.items():
            if profaned_capital_table.get(name):
                location = Location(self.player, name, address, profaned_capital_region)
                profaned_capital_region.locations.append(location)
        self.world.regions.append(profaned_capital_region)

        anor_londo_region = Region("Anor Londo", RegionType.Generic, "Anor Londo", self.player)
        for name, address in self.location_name_to_id.items():
            if anor_londo_table.get(name):
                location = Location(self.player, name, address, anor_londo_region)
                anor_londo_region.locations.append(location)
        self.world.regions.append(anor_londo_region)

        lothric_castle_region = Region("Lothric Castle", RegionType.Generic, "Lothric Castle", self.player)
        for name, address in self.location_name_to_id.items():
            if lothric_castle_table.get(name):
                location = Location(self.player, name, address, lothric_castle_region)
                lothric_castle_region.locations.append(location)
        self.world.regions.append(lothric_castle_region)

        grand_archives_region = Region("Grand Archives", RegionType.Generic, "Grand Archives", self.player)
        for name, address in self.location_name_to_id.items():
            if grand_archives_table.get(name):
                location = Location(self.player, name, address, grand_archives_region)
                grand_archives_region.locations.append(location)
        self.world.regions.append(grand_archives_region)

        untended_graves_region = Region("Untended Graves", RegionType.Generic, "Untended Graves", self.player)
        for name, address in self.location_name_to_id.items():
            if untended_graves_table.get(name):
                location = Location(self.player, name, address, untended_graves_region)
                untended_graves_region.locations.append(location)
        self.world.regions.append(untended_graves_region)

        archdragon_peak_region = Region("Archdragon Peak", RegionType.Generic, "Archdragon Peak", self.player)
        for name, address in self.location_name_to_id.items():
            if archdragon_peak_table.get(name):
                location = Location(self.player, name, address, archdragon_peak_region)
                archdragon_peak_region.locations.append(location)
        self.world.regions.append(archdragon_peak_region)

        kiln_of_the_first_flame_region = Region("Kiln Of The First Flame", RegionType.Generic,
                                                "Kiln Of The First Flame", self.player)
        self.world.regions.append(kiln_of_the_first_flame_region)

        menu_region.exits.append(Entrance(self.player, "New Game", menu_region))
        self.world.get_entrance("New Game", self.player).connect(cemetery_of_ash_region)

        cemetery_of_ash_region.exits.append(Entrance(self.player, "Goto Firelink Shrine", cemetery_of_ash_region))
        self.world.get_entrance("Goto Firelink Shrine", self.player).connect(firelink_shrine_region)
        firelink_shrine_region.exits.append(Entrance(self.player, "Goto High Wall of Lothric", firelink_shrine_region))
        firelink_shrine_region.exits.append(Entrance(self.player, "Goto Kiln Of The First Flame", firelink_shrine_region))
        firelink_shrine_region.exits.append(Entrance(self.player, "Goto Bell Tower", firelink_shrine_region))
        self.world.get_entrance("Goto High Wall of Lothric", self.player).connect(high_wall_of_lothric_region)
        self.world.get_entrance("Goto Kiln Of The First Flame", self.player).connect(kiln_of_the_first_flame_region)
        self.world.get_entrance("Goto Bell Tower", self.player).connect(firelink_shrine_bell_tower_region)

        high_wall_of_lothric_region.exits.append(Entrance(self.player, "Goto Undead Settlement", high_wall_of_lothric_region))
        high_wall_of_lothric_region.exits.append(Entrance(self.player, "Goto Lothric Castle", high_wall_of_lothric_region))
        self.world.get_entrance("Goto Undead Settlement", self.player).connect(undead_settlement_region)
        self.world.get_entrance("Goto Lothric Castle", self.player).connect(lothric_castle_region)
        undead_settlement_region.exits.append(Entrance(self.player, "Goto Road Of Sacrifices", undead_settlement_region))
        self.world.get_entrance("Goto Road Of Sacrifices", self.player).connect(road_of_sacrifices_region)
        road_of_sacrifices_region.exits.append(Entrance(self.player, "Goto Cathedral", road_of_sacrifices_region))
        road_of_sacrifices_region.exits.append(Entrance(self.player, "Goto Farron keep", road_of_sacrifices_region))
        self.world.get_entrance("Goto Cathedral", self.player).connect(cathedral_of_the_deep_region)
        self.world.get_entrance("Goto Farron keep", self.player).connect(farron_keep_region)
        farron_keep_region.exits.append(Entrance(self.player, "Goto Carthus catacombs", farron_keep_region))
        self.world.get_entrance("Goto Carthus catacombs", self.player).connect(catacombs_of_carthus_region)
        catacombs_of_carthus_region.exits.append(Entrance(self.player, "Goto Irithyll of the boreal", catacombs_of_carthus_region))
        catacombs_of_carthus_region.exits.append(Entrance(self.player, "Goto Smouldering Lake", catacombs_of_carthus_region))
        self.world.get_entrance("Goto Irithyll of the boreal", self.player).connect(irithyll_of_the_boreal_valley_region)
        self.world.get_entrance("Goto Smouldering Lake", self.player).connect(smouldering_lake_region)
        irithyll_of_the_boreal_valley_region.exits.append(Entrance(self.player, "Goto Irithyll dungeon", irithyll_of_the_boreal_valley_region))
        irithyll_of_the_boreal_valley_region.exits.append(Entrance(self.player, "Goto Anor Londo", irithyll_of_the_boreal_valley_region))
        self.world.get_entrance("Goto Irithyll dungeon", self.player).connect(irithyll_dungeon_region)
        self.world.get_entrance("Goto Anor Londo", self.player).connect(anor_londo_region)
        irithyll_dungeon_region.exits.append(Entrance(self.player, "Goto Archdragon peak", irithyll_dungeon_region))
        irithyll_dungeon_region.exits.append(Entrance(self.player, "Goto Profaned capital", irithyll_dungeon_region))
        self.world.get_entrance("Goto Archdragon peak", self.player).connect(archdragon_peak_region)
        self.world.get_entrance("Goto Profaned capital", self.player).connect(profaned_capital_region)

        lothric_castle_region.exits.append(Entrance(self.player, "Goto Consumed King Garden", lothric_castle_region))
        lothric_castle_region.exits.append(Entrance(self.player, "Goto Grand Archives", lothric_castle_region))
        self.world.get_entrance("Goto Consumed King Garden", self.player).connect(consumed_king_garden_region)
        self.world.get_entrance("Goto Grand Archives", self.player).connect(grand_archives_region)

        consumed_king_garden_region.exits.append(Entrance(self.player, "Goto Untended Graves", consumed_king_garden_region))
        self.world.get_entrance("Goto Untended Graves", self.player).connect(untended_graves_region)

    def create_items(self):
        for name, address in self.item_name_to_id.items():
            self.world.itempool += [self.create_item(name)]

    def generate_early(self):
        pass

    def set_rules(self) -> None:
        set_rule(self.world.get_entrance("Goto Bell Tower", self.player),
                   lambda state: state.has("Mortician's Ashes", self.player))
        set_rule(self.world.get_entrance("Goto Undead Settlement", self.player),
                   lambda state: state.has("Small Lothric Banner", self.player))
        set_rule(self.world.get_entrance("Goto Lothric Castle", self.player),
                  lambda state: state.has("Basin of Vows", self.player))
        set_rule(self.world.get_entrance("Goto Irithyll of the boreal", self.player),
                 lambda state: state.has("Small Doll", self.player))
        set_rule(self.world.get_entrance("Goto Archdragon peak", self.player),
                 lambda state: state.has("Path of the Dragon Gesture", self.player))
        set_rule(self.world.get_entrance("Goto Profaned capital", self.player),
                 lambda state: state.has("Storm Ruler", self.player))
        set_rule(self.world.get_entrance("Goto Grand Archives", self.player),
                 lambda state: state.has("Grand Archives Key", self.player))
        set_rule(self.world.get_entrance("Goto Kiln Of The First Flame", self.player), lambda state:
            state.has("Cinders of a Lord - Abyss Watcher", self.player) and
            state.has("Cinders of a Lord - Yhorm the Giant", self.player) and
            state.has("Cinders of a Lord - Aldrich", self.player) and
            state.has("Cinders of a Lord - Lothric Prince", self.player))

    def generate_basic(self):
        self.world.completion_condition[self.player] = lambda state: \
            state.has("Cinders of a Lord - Abyss Watcher", self.player) and\
            state.has("Cinders of a Lord - Yhorm the Giant", self.player) and\
            state.has("Cinders of a Lord - Aldrich", self.player) and\
            state.has("Cinders of a Lord - Lothric Prince", self.player)

    def generate_output(self, output_directory: str):

        for region in self.world.get_regions(self.player):
            print(region)

        locations_dict = {}
        for location in self.world.get_filled_locations(self.player):
            if location.item.player == self.player:
                print(location)
            else:
                locations_dict[dictionary_table[location.name]] = 0

        data = {
            "options": {
                "auto_equip": (True if self.world.auto_equip[self.player] else False),
                "lock_equip": (True if self.world.lock_equip[self.player] else False),
                "no_weapon_requirements": (True if self.world.no_weapon_requirements[self.player] else False),
            },
            "seed": self.world.seed_name,  # to verify the server's multiworld
            "slot": self.world.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locations": json.dumps(locations_dict)
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
    item_name_to_id = {name: id for id, name in enumerate(DarkSouls3Location.get_item_name_to_id(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(DarkSouls3Location.get_item_name_to_id(), base_id)}



