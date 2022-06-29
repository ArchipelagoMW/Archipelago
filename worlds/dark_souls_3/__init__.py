# world/dark_souls_3/__init__.py
import json
import os

from random import randint
from .Options import dark_souls_options  # the options we defined earlier
from .Items import DarkSouls3Item  # data used below to add items to the World
from .Locations import DarkSouls3Location  # same as above
from .data.items_data import weapons_upgrade_5_table, weapons_upgrade_10_table, item_dictionary_table, key_items_list
from .data.locations_data import dictionary_table, cemetery_of_ash_table, fire_link_shrine_table, \
    high_wall_of_lothric, \
    undead_settlement_table, road_of_sacrifice_table, consumed_king_garden_table, cathedral_of_the_deep_table, \
    farron_keep_table, catacombs_of_carthus_table, smouldering_lake_table, irithyll_of_the_boreal_valley_table, \
    irithyll_dungeon_table, profaned_capital_table, anor_londo_table, lothric_castle_table, grand_archives_table, \
    untended_graves_table, archdragon_peak_table, firelink_shrine_bell_tower_table, main_path_location_list
from ..AutoWorld import World
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance
from ..generic.Rules import set_rule


class DarkSouls3World(World):
    """Insert description of the world/game here."""

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []

    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]
        return DarkSouls3Item(name, name in key_items_list, data, self.player)

    def create_regions(self):
        menu_region = Region("Menu", RegionType.Generic, "Menu", self.player)
        self.world.regions.append(menu_region)

        self.main_path_locations = main_path_location_list
        cemetery_of_ash_region = self.create_region("Cemetery Of Ash", cemetery_of_ash_table)
        firelink_shrine_region = self.create_region("Firelink Shrine", fire_link_shrine_table)
        firelink_shrine_bell_tower_region = self.create_region("Firelink Shrine Bell Tower", firelink_shrine_bell_tower_table)
        high_wall_of_lothric_region = self.create_region("High Wall of Lothric", high_wall_of_lothric)
        undead_settlement_region = self.create_region("Undead Settlement", undead_settlement_table)
        road_of_sacrifices_region = self.create_region("Road of Sacrifices", road_of_sacrifice_table)
        consumed_king_garden_region = self.create_region("Consumed King's Garden", consumed_king_garden_table)
        cathedral_of_the_deep_region = self.create_region("Cathedral of the Deep", cathedral_of_the_deep_table)
        farron_keep_region = self.create_region("Farron Keep", farron_keep_table)
        catacombs_of_carthus_region = self.create_region("Catacombs of Carthus", catacombs_of_carthus_table)
        smouldering_lake_region = self.create_region("Smouldering Lake", smouldering_lake_table)
        irithyll_of_the_boreal_valley_region = self.create_region("Irithyll of the Boreal Valley", irithyll_of_the_boreal_valley_table)
        irithyll_dungeon_region = self.create_region("Irithyll Dungeon", irithyll_dungeon_table)
        profaned_capital_region = self.create_region("Profaned Capital", profaned_capital_table)
        anor_londo_region = self.create_region("Anor Londo", anor_londo_table)
        lothric_castle_region = self.create_region("Lothric Castle", lothric_castle_table)
        grand_archives_region = self.create_region("Grand Archives", grand_archives_table)
        untended_graves_region = self.create_region("Untended Graves", untended_graves_table)
        archdragon_peak_region = self.create_region("Archdragon Peak", archdragon_peak_table)
        kiln_of_the_first_flame_region = self.create_region("Kiln Of The First Flame", None)

        # Entrances
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

    def create_region(self, name, location_table) -> Region:
        new_region = Region(name, RegionType.Generic, name, self.player)
        if location_table is not None:
            for name, address in self.location_name_to_id.items():
                if location_table.get(name): # and name in self.main_path_locations:
                    location = Location(self.player, name, address, new_region)
                    new_region.locations.append(location)
        self.world.regions.append(new_region)
        return new_region

    def create_items(self):
        for name, address in self.item_name_to_id.items():
            if name != "Basin of Vows" and name != "Path of the Dragon Gesture":
                self.world.itempool += [self.create_item(name)]

    def generate_early(self):
        if self.world.priority_locations_preset[self.player]:
            self.world.priority_locations[self.player].value.update(main_path_location_list)

    def set_rules(self) -> None:
        set_rule(self.world.get_entrance("Goto Bell Tower", self.player),
                   lambda state: state.has("Mortician's Ashes", self.player))
        set_rule(self.world.get_entrance("Goto Undead Settlement", self.player),
                   lambda state: state.has("Small Lothric Banner", self.player))
        set_rule(self.world.get_entrance("Goto Lothric Castle", self.player),
                  lambda state: state.has("Basin of Vows", self.player))
        set_rule(self.world.get_location("HWL: Soul of the Dancer", self.player),
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

        self.world.completion_condition[self.player] = lambda state: \
            state.has("Cinders of a Lord - Abyss Watcher", self.player) and \
            state.has("Cinders of a Lord - Yhorm the Giant", self.player) and \
            state.has("Cinders of a Lord - Aldrich", self.player) and \
            state.has("Cinders of a Lord - Lothric Prince", self.player)

    def generate_basic(self):
        item = self.create_item("Basin of Vows")
        if self.world.late_basin_of_vows[self.player]:
            self.world.get_location("IBV: Soul of Pontiff Sulyvahn", self.player).place_locked_item(item)
        else:
            self.world.itempool += item

        itempool_len = self.item_name_to_id.__len__()
        total_required_locations = self.location_name_to_id.__len__()

        # Fill item pool with the remaining
        for i in range(itempool_len, total_required_locations):
            self.world.itempool += [self.create_item("Soul of an Intrepid Hero")]

    def generate_output(self, output_directory: str):

        print(self.world.get_items().__len__())

        item_dictionary = item_dictionary_table.copy()
        if self.world.randomize_weapons_level[self.player]:
            # Randomize some weapons upgrades
            for name in weapons_upgrade_5_table.keys():
                if randint(0, 100) < 33:
                    value = randint(1, 5)
                    item_dictionary[name] += value

            for name in weapons_upgrade_10_table.keys():
                if randint(0, 100) < 33:
                    value = randint(1, 10)
                    item_dictionary[name] += value

        itemsId = []
        itemsAddress = []
        locationsId = []
        locationsAddress = []
        locationsTarget = []
        for location in self.world.get_filled_locations():
            if location.item.player == self.player:
                itemsId.append(location.item.code)
                itemsAddress.append(item_dictionary[location.item.name])

            if location.player == self.player:
                locationsAddress.append(dictionary_table[location.name])
                locationsId.append(location.address)
                if location.item.player == self.player:
                    locationsTarget.append(item_dictionary[location.item.name])
                else:
                    locationsTarget.append(0)

        data = {
            "options": {
                "auto_equip": (True if self.world.auto_equip[self.player] else False),
                "lock_equip": (True if self.world.lock_equip[self.player] else False),
                "no_weapon_requirements": (True if self.world.no_weapon_requirements[self.player] else False),
            },
            "seed": self.world.seed_name,  # to verify the server's multiworld
            "slot": self.world.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locationsId,
            "locationsAddress": locationsAddress,
            "locationsTarget": locationsTarget,
            "itemsId": itemsId,
            "itemsAddress": itemsAddress
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
    location_name_to_id = {name: id for id, name in enumerate(DarkSouls3Location.get_location_name_to_id(), base_id)}





