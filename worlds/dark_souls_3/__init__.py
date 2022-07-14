# world/dark_souls_3/__init__.py
import json
import os

from .Options import dark_souls_options  # the options we defined earlier
from .data.items_data import weapons_upgrade_5_table, weapons_upgrade_10_table, item_dictionary_table, key_items_list
from .data.locations_data import location_dictionary_table, cemetery_of_ash_table, fire_link_shrine_table, \
    high_wall_of_lothric, \
    undead_settlement_table, road_of_sacrifice_table, consumed_king_garden_table, cathedral_of_the_deep_table, \
    farron_keep_table, catacombs_of_carthus_table, smouldering_lake_table, irithyll_of_the_boreal_valley_table, \
    irithyll_dungeon_table, profaned_capital_table, anor_londo_table, lothric_castle_table, grand_archives_table, \
    untended_graves_table, archdragon_peak_table, firelink_shrine_bell_tower_table
from ..AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from ..generic.Rules import set_rule


class DarkSouls3Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Dark Souls 3 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Marech"]
    )]


class DarkSouls3World(World):
    """
    Dark souls 3 is an Action role-playing game and is part of the Souls series developed by FromSoftware.
    Played in a third-person perspective, players have access to various weapons, armour, magic, and consumables that
    they can use to fight their enemies.
    """

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []

    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]

        if name in key_items_list:
            item_classification = ItemClassification.progression
        elif name in weapons_upgrade_5_table or name in weapons_upgrade_10_table:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return Item(
            name, item_classification, data, self.player)

    def create_regions(self):
        menu_region = Region("Menu", RegionType.Generic, "Menu", self.player)
        self.world.regions.append(menu_region)

        # Create all Vanilla regions of Dark Souls 3
        cemetery_of_ash_region = self.create_region("Cemetery Of Ash", cemetery_of_ash_table)
        firelink_shrine_region = self.create_region("Firelink Shrine", fire_link_shrine_table)
        firelink_shrine_bell_tower_region = self.create_region("Firelink Shrine Bell Tower",
                                                               firelink_shrine_bell_tower_table)
        high_wall_of_lothric_region = self.create_region("High Wall of Lothric", high_wall_of_lothric)
        undead_settlement_region = self.create_region("Undead Settlement", undead_settlement_table)
        road_of_sacrifices_region = self.create_region("Road of Sacrifices", road_of_sacrifice_table)
        consumed_king_garden_region = self.create_region("Consumed King's Garden", consumed_king_garden_table)
        cathedral_of_the_deep_region = self.create_region("Cathedral of the Deep", cathedral_of_the_deep_table)
        farron_keep_region = self.create_region("Farron Keep", farron_keep_table)
        catacombs_of_carthus_region = self.create_region("Catacombs of Carthus", catacombs_of_carthus_table)
        smouldering_lake_region = self.create_region("Smouldering Lake", smouldering_lake_table)
        irithyll_of_the_boreal_valley_region = self.create_region("Irithyll of the Boreal Valley",
                                                                  irithyll_of_the_boreal_valley_table)
        irithyll_dungeon_region = self.create_region("Irithyll Dungeon", irithyll_dungeon_table)
        profaned_capital_region = self.create_region("Profaned Capital", profaned_capital_table)
        anor_londo_region = self.create_region("Anor Londo", anor_londo_table)
        lothric_castle_region = self.create_region("Lothric Castle", lothric_castle_table)
        grand_archives_region = self.create_region("Grand Archives", grand_archives_table)
        untended_graves_region = self.create_region("Untended Graves", untended_graves_table)
        archdragon_peak_region = self.create_region("Archdragon Peak", archdragon_peak_table)
        kiln_of_the_first_flame_region = self.create_region("Kiln Of The First Flame", None)

        # Create the entrance to connect those regions
        menu_region.exits.append(Entrance(self.player, "New Game", menu_region))
        self.world.get_entrance("New Game", self.player).connect(cemetery_of_ash_region)
        cemetery_of_ash_region.exits.append(Entrance(self.player, "Goto Firelink Shrine", cemetery_of_ash_region))
        self.world.get_entrance("Goto Firelink Shrine", self.player).connect(firelink_shrine_region)
        firelink_shrine_region.exits.append(Entrance(self.player, "Goto High Wall of Lothric",
                                                     firelink_shrine_region))
        firelink_shrine_region.exits.append(Entrance(self.player, "Goto Kiln Of The First Flame",
                                                     firelink_shrine_region))
        firelink_shrine_region.exits.append(Entrance(self.player, "Goto Bell Tower",
                                                     firelink_shrine_region))
        self.world.get_entrance("Goto High Wall of Lothric", self.player).connect(high_wall_of_lothric_region)
        self.world.get_entrance("Goto Kiln Of The First Flame", self.player).connect(kiln_of_the_first_flame_region)
        self.world.get_entrance("Goto Bell Tower", self.player).connect(firelink_shrine_bell_tower_region)
        high_wall_of_lothric_region.exits.append(Entrance(self.player, "Goto Undead Settlement",
                                                          high_wall_of_lothric_region))
        high_wall_of_lothric_region.exits.append(Entrance(self.player, "Goto Lothric Castle",
                                                          high_wall_of_lothric_region))
        self.world.get_entrance("Goto Undead Settlement", self.player).connect(undead_settlement_region)
        self.world.get_entrance("Goto Lothric Castle", self.player).connect(lothric_castle_region)
        undead_settlement_region.exits.append(Entrance(self.player, "Goto Road Of Sacrifices",
                                                       undead_settlement_region))
        self.world.get_entrance("Goto Road Of Sacrifices", self.player).connect(road_of_sacrifices_region)
        road_of_sacrifices_region.exits.append(Entrance(self.player, "Goto Cathedral", road_of_sacrifices_region))
        road_of_sacrifices_region.exits.append(Entrance(self.player, "Goto Farron keep", road_of_sacrifices_region))
        self.world.get_entrance("Goto Cathedral", self.player).connect(cathedral_of_the_deep_region)
        self.world.get_entrance("Goto Farron keep", self.player).connect(farron_keep_region)
        farron_keep_region.exits.append(Entrance(self.player, "Goto Carthus catacombs", farron_keep_region))
        self.world.get_entrance("Goto Carthus catacombs", self.player).connect(catacombs_of_carthus_region)
        catacombs_of_carthus_region.exits.append(Entrance(self.player, "Goto Irithyll of the boreal",
                                                          catacombs_of_carthus_region))
        catacombs_of_carthus_region.exits.append(Entrance(self.player, "Goto Smouldering Lake",
                                                          catacombs_of_carthus_region))
        self.world.get_entrance("Goto Irithyll of the boreal", self.player).\
            connect(irithyll_of_the_boreal_valley_region)
        self.world.get_entrance("Goto Smouldering Lake", self.player).connect(smouldering_lake_region)
        irithyll_of_the_boreal_valley_region.exits.append(Entrance(self.player, "Goto Irithyll dungeon",
                                                                   irithyll_of_the_boreal_valley_region))
        irithyll_of_the_boreal_valley_region.exits.append(Entrance(self.player, "Goto Anor Londo",
                                                                   irithyll_of_the_boreal_valley_region))
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
        consumed_king_garden_region.exits.append(Entrance(self.player, "Goto Untended Graves",
                                                          consumed_king_garden_region))
        self.world.get_entrance("Goto Untended Graves", self.player).connect(untended_graves_region)

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, RegionType.Generic, region_name, self.player)
        if location_table:
            for name, address in location_table.items():
                location = Location(self.player, name, address, new_region)
                new_region.locations.append(location)
        self.world.regions.append(new_region)
        return new_region

    def create_items(self):
        for name, address in self.item_name_to_id.items():
            # Specific items will be included in the item pool under certain conditions. See generate_basic
            if name != "Basin of Vows":
                self.world.itempool += [self.create_item(name)]

    def generate_early(self):
        pass

    def set_rules(self) -> None:

        # Define the access rules to the entrances
        set_rule(
            self.world.get_entrance("Goto Bell Tower", self.player),
            lambda state: state.has("Mortician's Ashes", self.player))
        set_rule(
            self.world.get_entrance("Goto Undead Settlement", self.player),
            lambda state: state.has("Small Lothric Banner", self.player))
        set_rule(
            self.world.get_entrance("Goto Lothric Castle", self.player),
            lambda state: state.has("Basin of Vows", self.player))
        set_rule(
            self.world.get_location("HWL: Soul of the Dancer", self.player),
            lambda state: state.has("Basin of Vows", self.player))
        set_rule(
            self.world.get_entrance("Goto Irithyll of the boreal", self.player),
            lambda state: state.has("Small Doll", self.player))
        set_rule(
            self.world.get_entrance("Goto Archdragon peak", self.player),
            lambda state: state.has("Path of the Dragon Gesture", self.player))
        set_rule(
            self.world.get_entrance("Goto Profaned capital", self.player),
            lambda state: state.has("Storm Ruler", self.player))
        set_rule(
            self.world.get_entrance("Goto Grand Archives", self.player),
            lambda state: state.has("Grand Archives Key", self.player))
        set_rule(
            self.world.get_entrance("Goto Kiln Of The First Flame", self.player), lambda state:
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
        # Depending on the specified option, add the Basin of Vows to a specific location or to the item pool
        item = self.create_item("Basin of Vows")
        if self.world.late_basin_of_vows[self.player]:
            self.world.get_location("IBV: Soul of Pontiff Sulyvahn", self.player).place_locked_item(item)
        else:
            self.world.itempool += [item]

    def generate_output(self, output_directory: str):
        # Depending on the specified option, modify items hexadecimal value to add an upgrade level
        item_dictionary = item_dictionary_table.copy()
        if self.world.randomize_weapons_level[self.player]:
            # Randomize some weapons upgrades
            for name in weapons_upgrade_5_table.keys():
                if self.world.random.randint(0, 100) < 33:
                    value = self.world.random.randint(1, 5)
                    item_dictionary[name] += value

            for name in weapons_upgrade_10_table.keys():
                if self.world.random.randint(0, 100) < 33:
                    value = self.world.random.randint(1, 10)
                    item_dictionary[name] += value

        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.world.get_filled_locations():
            if location.item.player == self.player:
                items_id.append(location.item.code)
                items_address.append(item_dictionary[location.item.name])

            if location.player == self.player:
                locations_address.append(location_dictionary_table[location.name])
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(item_dictionary[location.item.name])
                else:
                    locations_target.append(0)

        data = {
            "options": {
                "auto_equip": self.world.auto_equip[self.player].value,
                "lock_equip": self.world.lock_equip[self.player].value,
                "no_weapon_requirements": self.world.no_weapon_requirements[self.player].value,
            },
            "seed": self.world.seed_name,  # to verify the server's multiworld
            "slot": self.world.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
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
    data_version = 1

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 100000

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for id, name in enumerate(item_dictionary_table, base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_dictionary_table, base_id)}
