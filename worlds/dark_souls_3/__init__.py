# world/dark_souls_3/__init__.py
from collections.abc import Sequence
import logging
from collections import defaultdict
from typing import Dict, Set, List, Optional, TextIO, Union
import re

from BaseClasses import CollectionState, MultiWorld, Region, Item, Location, LocationProgressType, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import CollectionRule, set_rule, add_rule, add_item_rule

from .Bosses import DS3BossInfo, all_bosses, default_yhorm_location
from .Items import DarkSouls3Item, DS3ItemCategory, DS3ItemData, Infusion, UsefulIf, filler_item_names, item_dictionary
from .Locations import DarkSouls3Location, DS3LocationCategory, DS3LocationData, location_tables, location_dictionary, location_name_groups, region_order
from .Options import DarkSouls3Options, RandomizeWeaponLevelOption, PoolTypeOption, SoulLocationsOption, UpgradeLocationsOption, UpgradedWeaponLocationsOption


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
    options: DarkSouls3Options
    options_dataclass = DarkSouls3Options
    topology_present: bool = True
    web = DarkSouls3Web()
    data_version = 8
    base_id = 100000
    enabled_location_categories: Set[DS3LocationCategory]
    required_client_version = (0, 4, 2)
    item_name_to_id = {data.name: data.ap_code for data in item_dictionary.values()}
    location_name_to_id = DarkSouls3Location.get_name_to_id()
    location_name_groups = location_name_groups
    item_name_groups = {
        "Cinders": {
            "Cinders of a Lord - Abyss Watcher",
            "Cinders of a Lord - Aldrich",
            "Cinders of a Lord - Yhorm the Giant",
            "Cinders of a Lord - Lothric Prince"
        }
    }

    yhorm_location: Optional[DS3BossInfo]
    """If enemy randomization is enabled, this is the boss who Yhorm the Giant should replace.
    
    This is used to determine where the Storm Ruler can be placed.
    """


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()


    def generate_early(self):
        if self.multiworld.enable_weapon_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.WEAPON)
            # Always make this available early because so many items are useless without it.
            self.multiworld.early_items[self.player]['Pyromancy Flame'] = 1
        if self.multiworld.enable_shield_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.SHIELD)
        if self.multiworld.enable_armor_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.ARMOR)
        if self.multiworld.enable_ring_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.RING)
        if self.multiworld.enable_spell_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.SPELL)
        if self.multiworld.enable_key_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.KEY)
        if self.multiworld.enable_unique_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.UNIQUE)
            # Make this available early just because it's fun to be able to check boss souls early.
            self.multiworld.early_items[self.player]['Transposing Kiln'] = 1
        if self.multiworld.enable_misc_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.MISC)
        if self.multiworld.enable_health_locations[self.player] == Toggle.option_true:
            self.enabled_location_categories.add(DS3LocationCategory.HEALTH)
        if self.multiworld.upgrade_locations[self.player] != UpgradeLocationsOption.option_not_randomized:
            self.enabled_location_categories.add(DS3LocationCategory.UPGRADE)
        if self.multiworld.soul_locations[self.player] != SoulLocationsOption.option_not_randomized:
            self.enabled_location_categories.add(DS3LocationCategory.SOUL)

        # The offline randomizer's clever code for converting an item into a gesture only works for
        # items in the local world.
        self.multiworld.local_items[self.player].value.add("Path of the Dragon")

        # Randomize Yhorm manually so that we know where to place the Storm Ruler
        if self.multiworld.randomize_enemies[self.player] == Toggle.option_true:
            self.yhorm_location = self.multiworld.random.choice(
                [
                    boss for boss in all_bosses if not boss.dlc
                ] if not self.multiworld.enable_dlc[self.player] else all_bosses
            )

            # If Yhorm is early, make sure the Storm Ruler is easily available to avoid BK
            if (
                self.yhorm_location.name == "Iudex Gundyr" or
                self.yhorm_location.name == "Vordt of the Boreal Valley" or (
                    self.yhorm_location.name == "Dancer of the Boreal Valley" and
                    self.multiworld.late_basin_of_vows[self.player] == Toggle.option_false
                )
            ):
                self.multiworld.early_items[self.player]['Storm Ruler'] = 1
                self.multiworld.local_items[self.player].value.add('Storm Ruler')
        else:
            self.yhorm_location = default_yhorm_location

    def create_regions(self):
        # Create Vanilla Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", {})
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Cemetery of Ash",
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
            "Greirat's Shop",
            "Karla's Shop",
        ]})

        # Create DLC Regions
        if self.multiworld.enable_dlc[self.player]:
            regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
                "Painted World of Ariandel (Before Contraption)",
                "Painted World of Ariandel (After Contraption)",
                "Dreg Heap",
                "Ringed City",
            ]})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"Go To {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "New Game", regions["Menu"]))
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Cemetery of Ash"])

        create_connection("Cemetery of Ash", "Firelink Shrine")

        create_connection("Firelink Shrine", "High Wall of Lothric")
        create_connection("Firelink Shrine", "Firelink Shrine Bell Tower")
        create_connection("Firelink Shrine", "Kiln of the First Flame")

        create_connection("High Wall of Lothric", "Undead Settlement")
        create_connection("High Wall of Lothric", "Lothric Castle")
        create_connection("High Wall of Lothric", "Greirat's Shop")

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
        create_connection("Irithyll Dungeon", "Karla's Shop")

        create_connection("Lothric Castle", "Consumed King's Garden")
        create_connection("Lothric Castle", "Grand Archives")

        create_connection("Consumed King's Garden", "Untended Graves")

        # Connect DLC Regions
        if self.multiworld.enable_dlc[self.player]:
            create_connection("Cathedral of the Deep", "Painted World of Ariandel (Before Contraption)")
            create_connection("Painted World of Ariandel (Before Contraption)",
                              "Painted World of Ariandel (After Contraption)")
            create_connection("Painted World of Ariandel (After Contraption)", "Dreg Heap")
            create_connection("Dreg Heap", "Ringed City")


    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            if self.is_location_available(location):
                new_location = DarkSouls3Location.from_data(
                    self.player,
                    location,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item_name)
                if event_item.classification != ItemClassification.progression:
                    continue

                new_location = DarkSouls3Location.from_data(
                    self.player,
                    location,
                    parent = new_region
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

        # Just used to efficiently deduplicate items
        item_set_by_category = {category: set() for category in self.enabled_location_categories}

        # Gather all default items on randomized locations
        num_required_extra_items = 0
        for location in self.multiworld.get_unfilled_locations(self.player):
            if not self.is_location_available(location.name):
                raise Exception("DS3 generation bug: Added an unavailable location.")

            item = item_dictionary[location.default_item_name]
            if item.category == DS3ItemCategory.SKIP:
                num_required_extra_items += 1
            elif item.category == DS3ItemCategory.MISC and not item.force_unique:
                itempool_by_category[location.category].append(location.default_item_name)
            else:
                # For non-miscellaneous non-skip items, make sure there aren't duplicates in the
                # item set even if there are multiple in-game locations that provide them.
                item_set = item_set_by_category[location.category]
                if location.default_item_name in item_set:
                    num_required_extra_items += 1
                else:
                    item_set.add(location.default_item_name)
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
            itempool.extend(self.create_item(name) for name in itempool_by_category[category])

        # A list of items we can replace
        removable_items = [item for item in itempool if item.classification == ItemClassification.filler]

        guaranteed_items = {"Path of the Dragon": 1}
        guaranteed_items.update(self.multiworld.guaranteed_items[self.player].value)
        if len(removable_items) == 0 and num_required_extra_items == 0:
            raise Exception("Can't add Path of the Dragon to the item pool")

        for item_name in guaranteed_items:
            # Break early just in case nothing is removable (if user is trying to guarantee more
            # items than the pool can hold, for example)
            if len(removable_items) == 0 and num_required_extra_items == 0:
                break

            num_existing_copies = len([item for item in itempool if item.name == item_name])
            for _ in range(guaranteed_items[item_name]):
                if num_existing_copies > 0:
                    num_existing_copies -= 1
                    continue

                if num_required_extra_items > 0:
                    # We can just add them instead of using filler later
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

        injectable_items = [
            item for item
            in item_dictionary.values()
            if item.inject and (not item.is_dlc or dlc_enabled)
        ]
        number_to_inject = min(num_required_extra_items, len(injectable_items))
        for item in self.multiworld.random.choices(injectable_items, k=number_to_inject):
            num_required_extra_items -= 1
            itempool.append(self.create_item(item.name))

        # Extra filler items for locations containing SKIP items
        itempool.extend(self.create_filler() for _ in range(num_required_extra_items))

        # Add items to itempool
        self.multiworld.itempool += itempool


    def create_item(self, item: Union[str, DS3ItemData]) -> Item:
        data = item if isinstance(item, DS3ItemData) else item_dictionary[item]
        classification = None
        if self.multiworld and ((
            data.useful_if == UsefulIf.BASE and
            not self.multiworld.enable_dlc[self.player] and
            not self.multiworld.enable_ngp[self.player]
        ) or (
            data.useful_if == UsefulIf.NO_DLC and
            not self.multiworld.enable_dlc[self.player]
        ) or (
            data.useful_if == UsefulIf.NO_NGP and
            not self.multiworld.enable_ngp[self.player]
        )):
            classification = ItemClassification.useful

        if (
            self.multiworld.randomize_weapon_level[self.player] != RandomizeWeaponLevelOption.option_none
            and data.category.upgrade_level
        ):
            # if the user made an error and set a min higher than the max we default to the max
            max_5 = self.multiworld.max_levels_in_5[self.player]
            min_5 = min(self.multiworld.min_levels_in_5[self.player], max_5)
            max_10 = self.multiworld.max_levels_in_10[self.player]
            min_10 = min(self.multiworld.min_levels_in_10[self.player], max_10)
            weapon_level_percentage = self.multiworld.randomize_weapon_level_percentage[self.player]

            if self.multiworld.random.randint(0, 99) < weapon_level_percentage:
                if data.category.upgrade_level == 5:
                    data = data.upgrade(self.multiworld.random.randint(min_5, max_5))
                elif data.category.upgrade_level == 10:
                    data = data.upgrade(self.multiworld.random.randint(min_10, max_10))

        if self.multiworld.randomize_infusion[self.player] and data.category.is_infusible:
            infusion_percentage = self.multiworld.randomize_infusion_percentage[self.player]
            if self.multiworld.random.randint(0, 99) < infusion_percentage:
                data = data.infuse(self.multiworld.random.choice(list(Infusion)))

        return DarkSouls3Item(self.player, data, classification=classification)


    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_item_names)


    def set_rules(self) -> None:
        # Define the access rules to the entrances
        self._add_entrance_rule("Firelink Shrine Bell Tower", "Tower Key")
        self._add_entrance_rule("Undead Settlement", "Small Lothric Banner")
        self._add_entrance_rule("Lothric Castle", "Basin of Vows")
        self._add_entrance_rule("Irithyll of the Boreal Valley", "Small Doll")
        self._add_entrance_rule("Archdragon Peak", "Path of the Dragon")
        self._add_entrance_rule("Grand Archives", "Grand Archives Key")
        self._add_entrance_rule(
            "Kiln of the First Flame",
            lambda state: state.has("Cinders of a Lord - Abyss Watcher", self.player) and
                          state.has("Cinders of a Lord - Yhorm the Giant", self.player) and
                          state.has("Cinders of a Lord - Aldrich", self.player) and
                          state.has("Cinders of a Lord - Lothric Prince", self.player))

        ashes = {
            "Mortician's Ashes": ["Alluring Skull", "Ember (Mortician)", "Grave Key"],
            "Dreamchaser's Ashes": ["Life Ring"],
            "Paladin's Ashes": ["Lloyd's Shield Ring"],
            "Grave Warden's Ashes": ["Ember (Grave Warden)"],
            "Prisoner Chief's Ashes": [
                "Karla's Pointed Hat",
                "Karla's Coat",
                "Karla's Gloves",
                "Karla's Trousers",
            ],
            "Xanthous Ashes": ["Xanthous Overcoat", "Xanthous Gloves", "Xanthous Trousers"],
            "Dragon Chaser's Ashes": ["Ember (Dragon Chaser)"],
            "Easterner's Ashes": [
                "Washing Pole",
                "Eastern Helm",
                "Eastern Armor",
                "Eastern Gauntlets",
                "Eastern Leggings",
                "Wood Grain Ring",
            ],
            "Captain's Ashes": [
                "Millwood Knight Helm",
                "Millwood Knight Armor",
                "Millwood Knight Gauntlets",
                "Millwood Knight Leggings",
                "Refined Gem",
            ]
        }
        for ash, items in ashes.items():
            for item in items:
                self._add_location_rule("FS: " + item, ash)

        if self.multiworld.late_basin_of_vows[self.player] == Toggle.option_true:
            self._add_entrance_rule("Lothric Castle", "Small Lothric Banner")

        # DLC Access Rules Below
        if self.multiworld.enable_dlc[self.player]:
            self._add_entrance_rule("Ringed City", "Small Envoy Banner")
            self._add_entrance_rule("Painted World of Ariandel (After Contraption)", "Contraption Key")

            if self.multiworld.late_dlc[self.player]:
                self._add_entrance_rule("Painted World of Ariandel (After Contraption)", "Small Doll")

        # Define the access rules to some specific locations
        self._add_location_rule("HWL: Red Eye Orb", "Lift Chamber Key")
        self._add_location_rule("ID: Bellowing Dragoncrest Ring", "Jailbreaker's Key")
        self._add_location_rule("ID: Covetous Gold Serpent Ring", "Old Cell Key")
        self._add_location_rule("UG: Hornet Ring", "Small Lothric Banner")
        self._add_entrance_rule("Karla's Shop", "Jailer's Key Ring")

        # The offline randomizer edits events to guarantee that Greirat won't go to Lothric until
        # Grand Archives is available, so his shop will always be available one way or another.
        self._add_entrance_rule("Greirat's Shop", "Cell Key")

        for item in ["Leonhard's Garb", "Leonhard's Gauntlets", "Leonhard's Trousers"]:
            self._add_location_rule("AL: " + item, "Black Eye Orb")

        # You could just kill NPCs for these, but it's more fun to ensure the player can do
        # their quests.
        self._add_location_rule("FS: Lift Chamber Key", "Pale Tongue")
        self._add_location_rule("AP: Hawkwood's Swordgrass", "Twinkling Dragon Torso Stone")
        self._add_location_rule("ID: Prisoner Chief's Ashes", "Jailer's Key Ring")

        # Make sure that the player can keep Orbeck around by giving him at least one scroll
        # before killing Abyss Watchers.
        def has_any_scroll(state):
            return (state.has("Sage's Scroll", self.player) or
                state.has("Golden Scroll", self.player) or
                state.has("Logan's Scroll", self.player) or
                state.has("Crystal Scroll", self.player))
        self._add_location_rule("FK: Soul of the Blood of the Wolf", has_any_scroll)
        self._add_location_rule("FK: Cinders of a Lord - Abyss Watcher", has_any_scroll)
        self._add_entrance_rule("Catacombs of Carthus", has_any_scroll)
        # Not really necessary but ensures players can decide which way to go
        self._add_entrance_rule("Painted World of Ariandel (After Contraption)", has_any_scroll)

        self._add_location_rule("HWL: Soul of the Dancer", "Basin of Vows")

        # Lump Soul of the Dancer in with LC for locations that should not be reachable
        # before having access to US. (Prevents requiring getting Basin to fight Dancer to get SLB to go to US)
        if self.multiworld.late_basin_of_vows[self.player]:
            self._add_location_rule("HWL: Soul of the Dancer", "Small Lothric Banner")
            # This isn't really necessary, but it ensures that the game logic knows players will
            # want to do Lothric Castle after at least being _able_ to access Catacombs. This is
            # useful for smooth item placement.
            self._add_location_rule("HWL: Soul of the Dancer", has_any_scroll)

        gotthard_corpse_rule = lambda state: \
            (state.can_reach("AL: Cinders of a Lord - Aldrich", "Location", self.player) and
             state.can_reach("PC: Cinders of a Lord - Yhorm the Giant", "Location", self.player))
        self._add_location_rule("LC: Grand Archives Key", gotthard_corpse_rule)
        self._add_location_rule("LC: Gotthard Twinswords", gotthard_corpse_rule)

        # Forbid shops from carrying items with multiple counts (the offline randomizer has its own
        # logic for choosing how many shop items to sell), and from carring soul items.
        for location in location_dictionary.values():
            if location.shop and self.is_location_available(location):
                add_item_rule(self.multiworld.get_location(location.name, self.player),
                              lambda item: (
                                  item.player != self.player or
                                  (item.count == 1 and not item.souls)
                              ))
        
        # Make sure the Storm Ruler is available BEFORE Yhorm the Giant
        if self.yhorm_location.region:
            self._add_entrance_rule(self.yhorm_location.region, "Storm Ruler")
        for location in self.yhorm_location.locations:
            self._add_location_rule(location, "Storm Ruler")

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Cinders of a Lord - Abyss Watcher", self.player) and \
            state.has("Cinders of a Lord - Yhorm the Giant", self.player) and \
            state.has("Cinders of a Lord - Aldrich", self.player) and \
            state.has("Cinders of a Lord - Lothric Prince", self.player)


    def _add_location_rule(self, location: str, rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the given location if it that location is randomized.

        The rule can just be a single item/event name as well as an explicit rule lambda.
        """
        if not self.is_location_available(location): return
        if isinstance(rule, str):
            assert item_dictionary[rule].classification == ItemClassification.progression
            rule = lambda state, item=rule: state.has(item, self.player)
        add_rule(self.multiworld.get_location(location, self.player), rule)


    def _add_entrance_rule(self, region: str, rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the entrance to the given region."""
        if isinstance(rule, str):
            assert item_dictionary[rule].classification == ItemClassification.progression
            rule = lambda state, item=rule: state.has(item, self.player)
        add_rule(self.multiworld.get_entrance("Go To " + region, self.player), rule)


    def is_location_available(self, location: Union[str, DS3LocationData]) -> bool:
        """Returns whether the given location is being randomized."""
        if isinstance(location, DS3LocationData):
            data = location
        else:
            data = location_dictionary[location]

        return (
            data.category in self.enabled_location_categories and
            (not data.npc or self.multiworld.enable_npc_locations[self.player] == Toggle.option_true) and
            (not data.dlc or self.multiworld.enable_dlc[self.player] == Toggle.option_true) and
            (not data.ngp or self.multiworld.enable_ngp[self.player] == Toggle.option_true)
        )


    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.yhorm_location != default_yhorm_location:
            spoiler_handle.write(f"Yhorm takes the place of {self.yhorm_location.name}")


    def pre_fill(self) -> None:
        # If upgrade smoothing is enabled, make sure one raw gem is available early for SL1 players
        if self.multiworld.upgrade_locations[self.player] == UpgradeLocationsOption.option_smooth:
            candidate_locations = [
                self.multiworld.get_location(location.name, self.player)
                for region in ["Cemetery of Ash", "Firelink Shrine", "High Wall of Lothric"]
                for location in location_tables[region]
                if self.is_location_available(location)
                and not location.missable and not location.conditional
            ]
            location = self.multiworld.random.choice([
                location for location in candidate_locations
                if not location.item and location.progress_type != LocationProgressType.EXCLUDED
            ])
            raw_gem = next(
                item for item in self.multiworld.itempool
                if item.player == self.player and item.name == "Raw Gem"
            )
            location.place_locked_item(raw_gem)
            self.multiworld.itempool.remove(raw_gem)


    def post_fill(self):
        """If item smoothing is enabled, rearrange items so they scale up smoothly through the run.

        This determines the approximate order a given silo of items (say, soul items) show up in the
        main game, then rearranges their shuffled placements to match that order. It determines what
        should come "earlier" or "later" based on sphere order: earlier spheres get lower-level
        items, later spheres get higher-level ones. Within a sphere, items in DS3 are distributed in
        region order, and then the best items in a sphere go into the multiworld.
        """

        state: CollectionState = CollectionState(self.multiworld)
        unchecked_locations = set(self.multiworld.get_locations())
        locations_by_sphere: List[Set[Location]] = []

        while len(unchecked_locations) > 0:
            sphere_locations = {loc for loc in unchecked_locations if state.can_reach(loc)}
            locations_by_sphere.append(self._shuffle(sphere_locations))
            unchecked_locations.difference_update(sphere_locations)

            state.sweep_for_events(key_only=True, locations=unchecked_locations)
            for location in sphere_locations:
                if location.event: state.collect(location.item, True, location)

        # All items in the base game in approximately the order they appear
        all_item_order = [
            item_dictionary[location.default_item_name]
            for region in region_order
            # Shuffle locations within each region.
            for location in self._shuffle(location_tables[region])
            if self.is_location_available(location)
        ]

        def smooth_items(item_order: List[Union[DS3ItemData, DarkSouls3Item]]) -> None:
            """Rearrange all items in item_order to match that order.

            Note: this requires that item_order exactly matches the number of placed items from this
            world matching the given names.
            """

            names = {item.name for item in item_order}

            for i, all_locations in enumerate(locations_by_sphere):
                locations = [
                    loc for loc in all_locations
                    if loc.item.player == self.player
                    and not loc.locked
                    and loc.item.name in names
                ]

                # Check the game, not the player, because we know how to sort within regions for DS3
                offworld = [loc for loc in locations if loc.game != "Dark Souls III"]
                self.multiworld.random.shuffle(offworld)
                onworld = sorted((loc for loc in locations if loc.game == "Dark Souls III"),
                                 key=lambda loc: loc.region_value)

                # Give offworld regions the last (best) items within a given sphere
                for location in onworld + offworld:
                    new_item = self._pop_item(location, item_order)
                    if isinstance(new_item, DarkSouls3Item):
                        location.item = new_item
                        new_item.location = location
                    else:
                        location.item.name = new_item.name
                        location.item.base_name = new_item.base_name
                        location.item.ds3_code = new_item.ds3_code
                        location.item.count = new_item.count

        if self.multiworld.upgrade_locations[self.player] == UpgradeLocationsOption.option_smooth:
            base_names = {
                "Titanite Shard", "Large Titanite Shard", "Titanite Chunk", "Titanite Slab",
                "Titanite Scale", "Twinkling Titanite", "Farron Coal", "Sage's Coal", "Giant's Coal",
                "Profaned Coal"
            }
            smooth_items([item for item in all_item_order if item.base_name in base_names])

        if self.multiworld.soul_locations[self.player] == SoulLocationsOption.option_smooth:
            # Shuffle larger boss sould among themselves because they're all worth 10-20k souls in
            # no particular order and that's a lot more interesting than getting them in the same
            # order every single run.
            shuffled = {
                item.name for item in item_dictionary.values()
                if item.category == DS3ItemCategory.BOSS and item.souls and item.souls >= 10000
            }
            shuffled_order = self._shuffle(shuffled)
            item_order: List[DS3ItemData] = []
            for item in all_item_order:
                if not item.souls: continue
                if item.base_name in shuffled:
                    item_order.append(item_dictionary[shuffled_order.pop(0)])
                else:
                    item_order.append(item)

            order_names = [item.name for item in item_order]
            location_names = [loc.item.name for loc in self.multiworld.get_locations() if loc.item.name in order_names]

            smooth_items(item_order)

        if self.multiworld.upgraded_weapon_locations[self.player] == UpgradedWeaponLocationsOption.option_smooth:
            upgraded_weapons = [
                location.item
                for location in self.multiworld.get_locations()
                if location.item.player == self.player
                and location.item.level and location.item.level > 0
            ]
            upgraded_weapons.sort(key=lambda item: item.level)
            smooth_items(upgraded_weapons)


    def _shuffle(self, seq: Sequence) -> Sequence:
        """Returns a shuffled copy of a sequence."""
        copy = list(seq)
        self.multiworld.random.shuffle(copy)
        return copy


    def _pop_item(self, location: Location, items: List[DS3ItemData]) -> DS3ItemData:
        """Returns the next item in items that can be assigned to location."""
        # Non-excluded locations can take any item we throw at them. (More specifically, if they can
        # take one item in a group, they can take any other).
        if location.progress_type != LocationProgressType.EXCLUDED: return items.pop(0)

        # Excluded locations require filler items.
        for i, item in enumerate(items):
            if item.classification == ItemClassification.filler:
                return items.pop(i)

        # If we can't find a suitable item, give up and assign an unsuitable one.
        return items.pop(0)


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        our_items = {
            location.item
            for location in self.multiworld.get_filled_locations()
            # item.code None is used for events, which we want to skip
            if location.item.code is not None and location.item.player == self.player
        }

        ap_ids_to_ds3_ids: Dict[str, int] = {}
        item_counts: Dict[str, int] = {}
        for item in our_items:
            ap_ids_to_ds3_ids[str(item.code)] = item.ds3_code
            if item.count != 1: item_counts[str(item.code)] = item.count

        # A map from Archipelago's location IDs to the keys the offline
        # randomizer uses to identify locations.
        location_ids_to_keys: Dict[str, str] = {}
        for location in self.multiworld.get_filled_locations():
            # Skip events and only look at this world's locations
            if (location.address is not None and location.item.code is not None
                    and location.player == self.player and location.offline):
                location_ids_to_keys[location.address] = location.offline

        slot_data = {
            "options": {
                "random_starting_loadout": self.multiworld.random_starting_loadout[self.player].value,
                "require_one_handed_starting_weapons": self.multiworld.require_one_handed_starting_weapons[self.player].value,
                "auto_equip": self.multiworld.auto_equip[self.player].value,
                "lock_equip": self.multiworld.lock_equip[self.player].value,
                "no_weapon_requirements": self.multiworld.no_weapon_requirements[self.player].value,
                "death_link": self.multiworld.death_link[self.player].value,
                "no_spell_requirements": self.multiworld.no_spell_requirements[self.player].value,
                "no_equip_load": self.multiworld.no_equip_load[self.player].value,
                "enable_dlc": self.multiworld.enable_dlc[self.player].value,
                "enable_ngp": self.multiworld.enable_ngp[self.player].value,
                "randomize_enemies": self.multiworld.randomize_enemies[self.player].value,
                "randomize_mimics_with_enemies": self.multiworld.randomize_mimics_with_enemies[self.player].value,
                "randomize_small_crystal_lizards_with_enemies": self.multiworld.randomize_small_crystal_lizards_with_enemies[self.player].value,
                "reduce_harmless_enemies": self.multiworld.reduce_harmless_enemies[self.player].value,
                "simple_early_bosses": self.multiworld.simple_early_bosses[self.player].value,
                "scale_enemies": self.multiworld.scale_enemies[self.player].value,
                "all_chests_are_mimics": self.multiworld.all_chests_are_mimics[self.player].value,
                "impatient_mimics": self.multiworld.impatient_mimics[self.player].value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "yhorm": (
                f"{self.yhorm_location.name} {self.yhorm_location.id}"
                if self.yhorm_location != default_yhorm_location
                else None
            ),
            "apIdsToItemIds": ap_ids_to_ds3_ids,
            "itemCounts": item_counts,
            "locationIdsToKeys": location_ids_to_keys,
        }

        return slot_data
