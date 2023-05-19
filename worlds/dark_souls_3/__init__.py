# world/dark_souls_3/__init__.py
from typing import Dict

from .Items import DarkSouls3Item, DS3ItemCategory, item_dictionary, key_item_names
from .Locations import DarkSouls3Location, DS3LocationCategory, location_tables, location_dictionary
from .Options import dark_souls_options
from ..AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle
from ..generic.Rules import set_rule, add_rule, add_item_rule


class DarkSouls3Web(WebWorld):
    bug_report_page = "https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/issues"
    setup_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Dark Souls III randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Marech"]
    )

    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Marech"]
    )

    tutorials = [setup_en, setup_fr]


class DarkSouls3World(World):
    """
    Dark souls III is an Action role-playing game and is part of the Souls series developed by FromSoftware.
    Played in a third-person perspective, players have access to various weapons, armour, magic, and consumables that
    they can use to fight their enemies.
    """

    game: str = "Dark Souls III"
    option_definitions = dark_souls_options
    topology_present: bool = True
    web = DarkSouls3Web()
    data_version = 6
    base_id = 100000
    required_client_version = (0, 3, 7)
    item_name_to_id = DarkSouls3Item.get_name_to_id()
    location_name_to_id = DarkSouls3Location.get_name_to_id()


    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []


    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in {DS3ItemCategory.WEAPON_UPGRADE_5, DS3ItemCategory.WEAPON_UPGRADE_10}:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DarkSouls3Item(name, item_classification, data, self.player)


    def create_regions(self):
        progressive_location_table = None
        if self.multiworld.enable_progressive_locations[self.player].value:
            progressive_location_table = [] + \
                location_tables["Progressive Items 1"] + \
                location_tables["Progressive Items 2"] + \
                location_tables["Progressive Items 3"]

            if self.multiworld.enable_dlc[self.player].value:
                progressive_location_table += location_tables["Progressive Items DLC"]

        # Create Vanilla Regions
        regions = {}
        regions["Menu"] = self.create_region("Menu", progressive_location_table)
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Firelink Shrine",
            "Firelink Shrine Bell Tower",
            "High Wall of Lothric",
            "Undead Settlement",
            "Road of Sacrifices",
            "Cathedral of the Deep",
            "Farron Keep",
            "Catacombs of Carthus",
            "Smouldering Lake",
            "Irithyll of the Boreal Valley",
            "Irithyll Dungeon",
            "Profaned Capital",
            "Anor Londo",
            "Lothric Castle",
            "Consumed King's Garden",
            "Grand Archives",
            "Untended Graves",
            "Archdragon Peak",
            "Kiln of the First Flame",
        ]})

        # Create DLC Regions
        if self.multiworld.enable_dlc[self.player]:
            regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
                "Painted World of Ariandel",
                "Dreg Heap",
                "Ringed City",
            ]})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"Go To {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "New Game", regions["Menu"]))
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Firelink Shrine"])

        create_connection("Firelink Shrine", "High Wall of Lothric")
        create_connection("Firelink Shrine", "Firelink Shrine Bell Tower")
        create_connection("Firelink Shrine", "Kiln of the First Flame")

        create_connection("High Wall of Lothric", "Undead Settlement")
        create_connection("High Wall of Lothric", "Lothric Castle")

        create_connection("Undead Settlement", "Road of Sacrifices")

        create_connection("Road of Sacrifices", "Cathedral of the Deep")
        create_connection("Road of Sacrifices", "Farron Keep")

        create_connection("Farron Keep", "Catacombs of Carthus")

        create_connection("Catacombs of Carthus", "Irithyll of the Boreal Valley")
        create_connection("Catacombs of Carthus", "Smouldering Lake")

        create_connection("Irithyll of the Boreal Valley", "Irithyll Dungeon")
        create_connection("Irithyll of the Boreal Valley", "Anor Londo")

        create_connection("Irithyll Dungeon", "Archdragon Peak")
        create_connection("Irithyll Dungeon", "Profaned Capital")

        create_connection("Lothric Castle", "Consumed King's Garden")
        create_connection("Lothric Castle", "Grand Archives")

        create_connection("Consumed King's Garden", "Untended Graves")

        # Connect DLC Regions
        if self.multiworld.enable_dlc[self.player]:
            create_connection("Cathedral of the Deep", "Painted World of Ariandel")
            create_connection("Painted World of Ariandel", "Dreg Heap")
            create_connection("Dreg Heap", "Ringed City")


    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        skip_weapon_locations = self.multiworld.enable_weapon_locations[self.player] == Toggle.option_false

        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            if skip_weapon_locations and location.category == DS3LocationCategory.WEAPON:
                new_location = DarkSouls3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item = self.create_item(location.default_item)
                event_item.code = None
                new_location.place_locked_item(event_item)
            else:
                new_location = DarkSouls3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )

            if region_name == "Menu":
                add_item_rule(new_location, lambda item: not item.advancement)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        dlc_enabled = self.multiworld.enable_dlc[self.player] == Toggle.option_true

        enabled_categories = []
        if self.multiworld.enable_weapon_locations[self.player] == Toggle.option_true:
            enabled_categories.append(DS3LocationCategory.WEAPON)
        enabled_categories.append(DS3LocationCategory.SHIELD)
        enabled_categories.append(DS3LocationCategory.ARMOR)
        enabled_categories.append(DS3LocationCategory.RING)
        enabled_categories.append(DS3LocationCategory.SPELL)
        enabled_categories.append(DS3LocationCategory.NPC)
        enabled_categories.append(DS3LocationCategory.KEY)
        enabled_categories.append(DS3LocationCategory.MISC)
        enabled_categories.append(DS3LocationCategory.HEALTH)
        enabled_categories.append(DS3LocationCategory.PROGRESSIVE_ITEM)

        itempool_by_category = {category: [] for category in enabled_categories}

        # Gather all default items on randomized locations
        num_required_extra_items = 0
        for location in self.multiworld.get_locations(self.player):
            if location.category in itempool_by_category:
                if item_dictionary[location.default_item_name].category == DS3ItemCategory.SKIP:
                    num_required_extra_items += 1
                else:
                    itempool_by_category[location.category].append(location.default_item_name)

        # Replace weapons with a random sample of all_weapons
        if DS3LocationCategory.WEAPON in enabled_categories:
            all_weapons = [
                item.name for item
                in item_dictionary.values()
                if (item.category in {DS3ItemCategory.WEAPON_UPGRADE_5, DS3ItemCategory.WEAPON_UPGRADE_10} and
                    (not item.is_dlc or dlc_enabled))
            ]

            itempool_by_category[DS3LocationCategory.WEAPON] = self.multiworld.random.sample(
                all_weapons,
                len(itempool_by_category[DS3LocationCategory.WEAPON])
            )

        # Add items to itempool
        for category in enabled_categories:
            self.multiworld.itempool += [self.create_item(name) for name in itempool_by_category[category]]

        # Extra filler items for locations without default items specified
        self.multiworld.itempool += [self.create_item("Soul of an Intrepid Hero") for i in range(num_required_extra_items)]


    def generate_early(self):
        pass


    def set_rules(self) -> None:
        # Define the access rules to the entrances
        set_rule(self.multiworld.get_entrance("Go To Firelink Shrine Bell Tower", self.player),
                 lambda state: state.has("Tower Key", self.player))
        set_rule(self.multiworld.get_entrance("Go To Undead Settlement", self.player),
                 lambda state: state.has("Small Lothric Banner", self.player))
        set_rule(self.multiworld.get_entrance("Go To Lothric Castle", self.player),
                 lambda state: state.has("Basin of Vows", self.player))
        set_rule(self.multiworld.get_entrance("Go To Irithyll of the Boreal Valley", self.player),
                 lambda state: state.has("Small Doll", self.player))
        set_rule(self.multiworld.get_entrance("Go To Archdragon Peak", self.player),
                 lambda state: state.can_reach("CKG: Soul of Consumed Oceiros", "Location", self.player))
        set_rule(self.multiworld.get_entrance("Go To Profaned Capital", self.player),
                 lambda state: state.has("Storm Ruler", self.player))
        set_rule(self.multiworld.get_entrance("Go To Grand Archives", self.player),
                 lambda state: state.has("Grand Archives Key", self.player))
        set_rule(self.multiworld.get_entrance("Go To Kiln of the First Flame", self.player),
                 lambda state: state.has("Cinders of a Lord - Abyss Watcher", self.player) and
                               state.has("Cinders of a Lord - Yhorm the Giant", self.player) and
                               state.has("Cinders of a Lord - Aldrich", self.player) and
                               state.has("Cinders of a Lord - Lothric Prince", self.player))

        if self.multiworld.late_basin_of_vows[self.player] == Toggle.option_true:
            add_rule(self.multiworld.get_entrance("Go To Lothric Castle", self.player),
                     lambda state: state.has("Small Lothric Banner", self.player))

        # DLC Access Rules Below
        if self.multiworld.enable_dlc[self.player]:
            set_rule(self.multiworld.get_entrance("Go To Painted World of Ariandel", self.player),
                     lambda state: state.has("Contraption Key", self.player))
            set_rule(self.multiworld.get_entrance("Go To Ringed City", self.player),
                     lambda state: state.has("Small Envoy Banner", self.player))

            if self.multiworld.late_dlc[self.player] == Toggle.option_true:
                add_rule(self.multiworld.get_entrance("Go To Painted World of Ariandel", self.player),
                        lambda state: state.has("Small Doll", self.player))

        # Define the access rules to some specific locations
        set_rule(self.multiworld.get_location("HWL: Soul of the Dancer", self.player),
                 lambda state: state.has("Basin of Vows", self.player))
        set_rule(self.multiworld.get_location("HWL: Greirat's Ashes", self.player),
                 lambda state: state.has("Cell Key", self.player))
        set_rule(self.multiworld.get_location("HWL: Blue Tearstone Ring", self.player),
                 lambda state: state.has("Cell Key", self.player))
        set_rule(self.multiworld.get_location("ID: Bellowing Dragoncrest Ring", self.player),
                 lambda state: state.has("Jailbreaker's Key", self.player))
        set_rule(self.multiworld.get_location("ID: Prisoner Chief's Ashes", self.player),
                 lambda state: state.has("Jailer's Key Ring", self.player))
        set_rule(self.multiworld.get_location("ID: Covetous Gold Serpent Ring", self.player),
                 lambda state: state.has("Old Cell Key", self.player))
        set_rule(self.multiworld.get_location("ID: Karla's Ashes", self.player),
                 lambda state: state.has("Jailer's Key Ring", self.player))

        black_hand_gotthard_corpse_rule = lambda state: \
            (state.can_reach("AL: Cinders of a Lord - Aldrich", "Location", self.player) and
             state.can_reach("PC: Cinders of a Lord - Yhorm the Giant", "Location", self.player))
        set_rule(self.multiworld.get_location("LC: Grand Archives Key", self.player), black_hand_gotthard_corpse_rule)
        set_rule(self.multiworld.get_location("LC: Gotthard Twinswords", self.player), black_hand_gotthard_corpse_rule)

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Cinders of a Lord - Abyss Watcher", self.player) and \
            state.has("Cinders of a Lord - Yhorm the Giant", self.player) and \
            state.has("Cinders of a Lord - Aldrich", self.player) and \
            state.has("Cinders of a Lord - Lothric Prince", self.player)


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        # Depending on the specified option, modify items hexadecimal value to add an upgrade level
        name_to_ds3_code = {item.name: item.ds3_code for item in item_dictionary.values()}
        if self.multiworld.randomize_weapons_level[self.player] > 0:
            # if the user made an error and set a min higher than the max we default to the max
            max_5 = self.multiworld.max_levels_in_5[self.player]
            min_5 = min(self.multiworld.min_levels_in_5[self.player], max_5)
            max_10 = self.multiworld.max_levels_in_10[self.player]
            min_10 = min(self.multiworld.min_levels_in_10[self.player], max_10)
            weapons_percentage = self.multiworld.randomize_weapons_percentage[self.player]

            # Randomize some weapons upgrades
            if self.multiworld.randomize_weapons_level[self.player] in [1, 3]:  # Options are either all or +5
                for name in [item.name for item in item_dictionary.values() if item.category == DS3ItemCategory.WEAPON_UPGRADE_5]:
                    if self.multiworld.per_slot_randoms[self.player].randint(1, 100) < weapons_percentage:
                        name_to_ds3_code[name] += self.multiworld.per_slot_randoms[self.player].randint(min_5, max_5)

            if self.multiworld.randomize_weapons_level[self.player] in [1, 2]:  # Options are either all or +10
                for name in [item.name for item in item_dictionary.values() if item.category == DS3ItemCategory.WEAPON_UPGRADE_10]:
                    if self.multiworld.per_slot_randoms[self.player].randint(1, 100) < weapons_percentage:
                        name_to_ds3_code[name] += self.multiworld.per_slot_randoms[self.player].randint(min_10, max_10)

        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            if location.item.player == self.player:
                items_id.append(location.item.code)
                items_address.append(name_to_ds3_code[location.item.name])

            if location.player == self.player:
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].ds3_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_ds3_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "auto_equip": self.multiworld.auto_equip[self.player].value,
                "lock_equip": self.multiworld.lock_equip[self.player].value,
                "no_weapon_requirements": self.multiworld.no_weapon_requirements[self.player].value,
                "death_link": self.multiworld.death_link[self.player].value,
                "no_spell_requirements": self.multiworld.no_spell_requirements[self.player].value,
                "no_equip_load": self.multiworld.no_equip_load[self.player].value,
                "enable_dlc": self.multiworld.enable_dlc[self.player].value
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
        }

        return slot_data
