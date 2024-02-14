# world/dark_souls_3/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DarkSouls3Item, DS3ItemCategory, item_dictionary, key_item_names, item_descriptions
from .Locations import DarkSouls3Location, DS3LocationCategory, location_tables, location_dictionary
from .Options import RandomizeWeaponLevelOption, PoolTypeOption, EarlySmallLothricBanner, dark_souls_options


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
    data_version = 8
    base_id = 100000
    enabled_location_categories: Set[DS3LocationCategory]
    required_client_version = (0, 4, 2)
    item_name_to_id = DarkSouls3Item.get_name_to_id()
    location_name_to_id = DarkSouls3Location.get_name_to_id()
    item_name_groups = {
        "Cinders": {
            "Cinders of a Lord - Abyss Watcher",
            "Cinders of a Lord - Aldrich",
            "Cinders of a Lord - Yhorm the Giant",
            "Cinders of a Lord - Lothric Prince"
        }
    }
    item_descriptions = item_descriptions


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()


    def generate_early(self):
        if self.multiworld.enable_weapon_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.WEAPON)
        if self.multiworld.enable_shield_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.SHIELD)
        if self.multiworld.enable_armor_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.ARMOR)
        if self.multiworld.enable_ring_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.RING)
        if self.multiworld.enable_spell_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.SPELL)
        if self.multiworld.enable_npc_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.NPC)
        if self.multiworld.enable_key_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.KEY)
            if self.multiworld.early_banner[self.player] == EarlySmallLothricBanner.option_early_global:
                self.multiworld.early_items[self.player]['Small Lothric Banner'] = 1
            elif self.multiworld.early_banner[self.player] == EarlySmallLothricBanner.option_early_local:
                self.multiworld.local_early_items[self.player]['Small Lothric Banner'] = 1
        if self.multiworld.enable_boss_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.BOSS)
        if self.multiworld.enable_misc_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.MISC)
        if self.multiworld.enable_health_upgrade_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.HEALTH)
        if self.multiworld.enable_progressive_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.PROGRESSIVE_ITEM)


    def create_regions(self):
        progressive_location_table = []
        if self.multiworld.enable_progressive_locations[self.player]:
            progressive_location_table = [] + \
                location_tables["Progressive Items 1"] + \
                location_tables["Progressive Items 2"] + \
                location_tables["Progressive Items 3"] + \
                location_tables["Progressive Items 4"]

            if self.multiworld.enable_dlc[self.player].value:
                progressive_location_table += location_tables["Progressive Items DLC"]

        if self.multiworld.enable_health_upgrade_locations[self.player]:
            progressive_location_table += location_tables["Progressive Items Health"]

        # Create Vanilla Regions
        regions: Dict[str, Region] = {}
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

        # Adds Path of the Dragon as an event item for Archdragon Peak access
        potd_location = DarkSouls3Location(self.player, "CKG: Path of the Dragon", DS3LocationCategory.EVENT, "Path of the Dragon", None, regions["Consumed King's Garden"])
        potd_location.place_locked_item(Item("Path of the Dragon", ItemClassification.progression, None, self.player))
        regions["Consumed King's Garden"].locations.append(potd_location)

        # Create DLC Regions
        if self.multiworld.enable_dlc[self.player]:
            regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
                "Painted World of Ariandel 1",
                "Painted World of Ariandel 2",
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
            create_connection("Cathedral of the Deep", "Painted World of Ariandel 1")
            create_connection("Painted World of Ariandel 1", "Painted World of Ariandel 2")
            create_connection("Painted World of Ariandel 2", "Dreg Heap")
            create_connection("Dreg Heap", "Ringed City")


    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            if location.category in self.enabled_location_categories:
                new_location = DarkSouls3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                if event_item.classification != ItemClassification.progression:
                    continue

                new_location = DarkSouls3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)

            if region_name == "Menu":
                add_item_rule(new_location, lambda item: not item.advancement)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        dlc_enabled = self.multiworld.enable_dlc[self.player] == Toggle.option_true

        itempool_by_category = {category: [] for category in self.enabled_location_categories}

        # Gather all default items on randomized locations
        num_required_extra_items = 0
        for location in self.multiworld.get_locations(self.player):
            if location.category in itempool_by_category:
                if item_dictionary[location.default_item_name].category == DS3ItemCategory.SKIP:
                    num_required_extra_items += 1
                else:
                    itempool_by_category[location.category].append(location.default_item_name)

        # Replace each item category with a random sample of items of those types
        if self.multiworld.pool_type[self.player] == PoolTypeOption.option_various:
            def create_random_replacement_list(item_categories: Set[DS3ItemCategory], num_items: int):
                candidates = [
                    item.name for item
                    in item_dictionary.values()
                    if (item.category in item_categories and (not item.is_dlc or dlc_enabled))
                ]
                return self.multiworld.random.sample(candidates, num_items)

            if DS3LocationCategory.WEAPON in self.enabled_location_categories:
                itempool_by_category[DS3LocationCategory.WEAPON] = create_random_replacement_list(
                    {
                        DS3ItemCategory.WEAPON_UPGRADE_5,
                        DS3ItemCategory.WEAPON_UPGRADE_10,
                        DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE
                    },
                    len(itempool_by_category[DS3LocationCategory.WEAPON])
                )
            if DS3LocationCategory.SHIELD in self.enabled_location_categories:
                itempool_by_category[DS3LocationCategory.SHIELD] = create_random_replacement_list(
                    {DS3ItemCategory.SHIELD, DS3ItemCategory.SHIELD_INFUSIBLE},
                    len(itempool_by_category[DS3LocationCategory.SHIELD])
                )
            if DS3LocationCategory.ARMOR in self.enabled_location_categories:
                itempool_by_category[DS3LocationCategory.ARMOR] = create_random_replacement_list(
                    {DS3ItemCategory.ARMOR},
                    len(itempool_by_category[DS3LocationCategory.ARMOR])
                )
            if DS3LocationCategory.RING in self.enabled_location_categories:
                itempool_by_category[DS3LocationCategory.RING] = create_random_replacement_list(
                    {DS3ItemCategory.RING},
                    len(itempool_by_category[DS3LocationCategory.RING])
                )
            if DS3LocationCategory.SPELL in self.enabled_location_categories:
                itempool_by_category[DS3LocationCategory.SPELL] = create_random_replacement_list(
                    {DS3ItemCategory.SPELL},
                    len(itempool_by_category[DS3LocationCategory.SPELL])
                )

        itempool: List[DarkSouls3Item] = []
        for category in self.enabled_location_categories:
            itempool += [self.create_item(name) for name in itempool_by_category[category]]

        # A list of items we can replace
        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]

        guaranteed_items = self.multiworld.guaranteed_items[self.player].value
        for item_name in guaranteed_items:
            # Break early just in case nothing is removable (if user is trying to guarantee more
            # items than the pool can hold, for example)
            if len(removable_items) == 0:
                break

            num_existing_copies = len([item for item in itempool if item.name == item_name])
            for _ in range(guaranteed_items[item_name]):
                if num_existing_copies > 0:
                    num_existing_copies -= 1
                    continue

                if num_required_extra_items > 0:
                    # We can just add them instead of using "Soul of an Intrepid Hero" later
                    num_required_extra_items -= 1
                else:
                    if len(removable_items) == 0:
                        break

                    # Try to construct a list of items with the same category that can be removed
                    # If none exist, just remove something at random
                    removable_shortlist = [
                        item for item
                        in removable_items
                        if item_dictionary[item.name].category == item_dictionary[item_name].category
                    ]
                    if len(removable_shortlist) == 0:
                        removable_shortlist = removable_items

                    removed_item = self.multiworld.random.choice(removable_shortlist)
                    removable_items.remove(removed_item) # To avoid trying to replace the same item twice
                    itempool.remove(removed_item)

                itempool.append(self.create_item(item_name))

        # Extra filler items for locations containing SKIP items
        itempool += [self.create_filler() for _ in range(num_required_extra_items)]

        # Add items to itempool
        self.multiworld.itempool += itempool


    def create_item(self, name: str) -> Item:
        useful_categories = {
            DS3ItemCategory.WEAPON_UPGRADE_5,
            DS3ItemCategory.WEAPON_UPGRADE_10,
            DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE,
            DS3ItemCategory.SPELL,
        }
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories or name in {"Estus Shard", "Undead Bone Shard"}:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DarkSouls3Item(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return "Soul of an Intrepid Hero"


    def set_rules(self) -> None:
        # Define the access rules to the entrances
        set_rule(self.multiworld.get_entrance("Go To Undead Settlement", self.player),
                 lambda state: state.has("Small Lothric Banner", self.player))
        set_rule(self.multiworld.get_entrance("Go To Lothric Castle", self.player),
                 lambda state: state.has("Basin of Vows", self.player))
        set_rule(self.multiworld.get_entrance("Go To Irithyll of the Boreal Valley", self.player),
                 lambda state: state.has("Small Doll", self.player))
        set_rule(self.multiworld.get_entrance("Go To Archdragon Peak", self.player),
                 lambda state: state.has("Path of the Dragon", self.player))
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
            set_rule(self.multiworld.get_entrance("Go To Ringed City", self.player),
                     lambda state: state.has("Small Envoy Banner", self.player))

            # If key items are randomized, must have contraption key to enter second half of Ashes DLC
            # If key items are not randomized, Contraption Key is guaranteed to be accessible before it is needed
            if self.multiworld.enable_key_locations[self.player] == Toggle.option_true:
                add_rule(self.multiworld.get_entrance("Go To Painted World of Ariandel 2", self.player),
                         lambda state: state.has("Contraption Key", self.player))

            if self.multiworld.late_dlc[self.player] == Toggle.option_true:
                add_rule(self.multiworld.get_entrance("Go To Painted World of Ariandel 1", self.player),
                         lambda state: state.has("Small Doll", self.player))

        # Define the access rules to some specific locations
        set_rule(self.multiworld.get_location("PC: Cinders of a Lord - Yhorm the Giant", self.player),
                 lambda state: state.has("Storm Ruler", self.player))

        if self.multiworld.enable_ring_locations[self.player] == Toggle.option_true:
            set_rule(self.multiworld.get_location("ID: Bellowing Dragoncrest Ring", self.player),
                     lambda state: state.has("Jailbreaker's Key", self.player))
            set_rule(self.multiworld.get_location("ID: Covetous Gold Serpent Ring", self.player),
                     lambda state: state.has("Old Cell Key", self.player))
            set_rule(self.multiworld.get_location("UG: Hornet Ring", self.player),
                     lambda state: state.has("Small Lothric Banner", self.player))

        if self.multiworld.enable_npc_locations[self.player] == Toggle.option_true:
            set_rule(self.multiworld.get_location("HWL: Greirat's Ashes", self.player),
                     lambda state: state.has("Cell Key", self.player))
            set_rule(self.multiworld.get_location("HWL: Blue Tearstone Ring", self.player),
                     lambda state: state.has("Cell Key", self.player))
            set_rule(self.multiworld.get_location("ID: Karla's Ashes", self.player),
                     lambda state: state.has("Jailer's Key Ring", self.player))
            set_rule(self.multiworld.get_location("ID: Karla's Pointed Hat", self.player),
                     lambda state: state.has("Jailer's Key Ring", self.player))
            set_rule(self.multiworld.get_location("ID: Karla's Coat", self.player),
                     lambda state: state.has("Jailer's Key Ring", self.player))
            set_rule(self.multiworld.get_location("ID: Karla's Gloves", self.player),
                     lambda state: state.has("Jailer's Key Ring", self.player))
            set_rule(self.multiworld.get_location("ID: Karla's Trousers", self.player),
                     lambda state: state.has("Jailer's Key Ring", self.player))

        if self.multiworld.enable_misc_locations[self.player] == Toggle.option_true:
            set_rule(self.multiworld.get_location("ID: Prisoner Chief's Ashes", self.player),
                     lambda state: state.has("Jailer's Key Ring", self.player))

        if self.multiworld.enable_boss_locations[self.player] == Toggle.option_true:
            set_rule(self.multiworld.get_location("PC: Soul of Yhorm the Giant", self.player),
                     lambda state: state.has("Storm Ruler", self.player))
            set_rule(self.multiworld.get_location("HWL: Soul of the Dancer", self.player),
                     lambda state: state.has("Basin of Vows", self.player))

            # Lump Soul of the Dancer in with LC for locations that should not be reachable
            # before having access to US. (Prevents requiring getting Basin to fight Dancer to get SLB to go to US)
            if self.multiworld.late_basin_of_vows[self.player] == Toggle.option_true:
                add_rule(self.multiworld.get_location("HWL: Soul of the Dancer", self.player),
                         lambda state: state.has("Small Lothric Banner", self.player))

        gotthard_corpse_rule = lambda state: \
            (state.can_reach("AL: Cinders of a Lord - Aldrich", "Location", self.player) and
             state.can_reach("PC: Cinders of a Lord - Yhorm the Giant", "Location", self.player))

        set_rule(self.multiworld.get_location("LC: Grand Archives Key", self.player), gotthard_corpse_rule)

        if self.multiworld.enable_weapon_locations[self.player] == Toggle.option_true:
            set_rule(self.multiworld.get_location("LC: Gotthard Twinswords", self.player), gotthard_corpse_rule)

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Cinders of a Lord - Abyss Watcher", self.player) and \
            state.has("Cinders of a Lord - Yhorm the Giant", self.player) and \
            state.has("Cinders of a Lord - Aldrich", self.player) and \
            state.has("Cinders of a Lord - Lothric Prince", self.player)


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        # Depending on the specified option, modify items hexadecimal value to add an upgrade level or infusion
        name_to_ds3_code = {item.name: item.ds3_code for item in item_dictionary.values()}

        # Randomize some weapon upgrades
        if self.multiworld.randomize_weapon_level[self.player] != RandomizeWeaponLevelOption.option_none:
            # if the user made an error and set a min higher than the max we default to the max
            max_5 = self.multiworld.max_levels_in_5[self.player]
            min_5 = min(self.multiworld.min_levels_in_5[self.player], max_5)
            max_10 = self.multiworld.max_levels_in_10[self.player]
            min_10 = min(self.multiworld.min_levels_in_10[self.player], max_10)
            weapon_level_percentage = self.multiworld.randomize_weapon_level_percentage[self.player]

            for item in item_dictionary.values():
                if self.multiworld.per_slot_randoms[self.player].randint(0, 99) < weapon_level_percentage:
                    if item.category == DS3ItemCategory.WEAPON_UPGRADE_5:
                        name_to_ds3_code[item.name] += self.multiworld.per_slot_randoms[self.player].randint(min_5, max_5)
                    elif item.category in {DS3ItemCategory.WEAPON_UPGRADE_10, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE}:
                        name_to_ds3_code[item.name] += self.multiworld.per_slot_randoms[self.player].randint(min_10, max_10)

        # Randomize some weapon infusions
        if self.multiworld.randomize_infusion[self.player] == Toggle.option_true:
            infusion_percentage = self.multiworld.randomize_infusion_percentage[self.player]
            for item in item_dictionary.values():
                if item.category in {DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE, DS3ItemCategory.SHIELD_INFUSIBLE}:
                    if self.multiworld.per_slot_randoms[self.player].randint(0, 99) < infusion_percentage:
                        name_to_ds3_code[item.name] += 100 * self.multiworld.per_slot_randoms[self.player].randint(0, 15)

        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            # Skip events
            if location.item.code is None:
                continue

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
                "enable_weapon_locations": self.multiworld.enable_weapon_locations[self.player].value,
                "enable_shield_locations": self.multiworld.enable_shield_locations[self.player].value,
                "enable_armor_locations": self.multiworld.enable_armor_locations[self.player].value,
                "enable_ring_locations": self.multiworld.enable_ring_locations[self.player].value,
                "enable_spell_locations": self.multiworld.enable_spell_locations[self.player].value,
                "enable_key_locations": self.multiworld.enable_key_locations[self.player].value,
                "enable_boss_locations": self.multiworld.enable_boss_locations[self.player].value,
                "enable_npc_locations": self.multiworld.enable_npc_locations[self.player].value,
                "enable_misc_locations": self.multiworld.enable_misc_locations[self.player].value,
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
