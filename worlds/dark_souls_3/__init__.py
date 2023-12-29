# world/dark_souls_3/__init__.py
from collections.abc import Sequence
from collections import defaultdict
import json
from typing import Callable, Dict, Set, List, Optional, TextIO, Union

from BaseClasses import CollectionState, MultiWorld, Region, Item, Location, LocationProgressType, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import CollectionRule, set_rule, add_rule, add_item_rule

from .Bosses import DS3BossInfo, all_bosses, default_yhorm_location
from .Items import DarkSouls3Item, DS3ItemCategory, DS3ItemData, Infusion, UsefulIf, filler_item_names, item_dictionary
from .Locations import DarkSouls3Location, DS3LocationCategory, DS3LocationData, location_tables, location_dictionary, location_name_groups, region_order
from .Options import DarkSouls3Options, EarlySmallLothricBanner, RandomizeWeaponLevelOption, SoulLocationsOption, UpgradeLocationsOption, UpgradedWeaponLocationsOption


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
    data_version = 9
    base_id = 100000
    enabled_location_categories: Set[DS3LocationCategory]
    required_client_version = (0, 4, 2)
    item_name_to_id = {data.name: data.ap_code for data in item_dictionary.values()}
    location_name_to_id = {
        location.name: location.ap_code
        for locations in location_tables.values()
        for location in locations
    }
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
        if self.options.enable_weapon_locations:
            self.enabled_location_categories.add(DS3LocationCategory.WEAPON)
            # Always make this available early because so many items are useless without it.
            self.multiworld.early_items[self.player]['Pyromancy Flame'] = 1
        if self.options.enable_shield_locations:
            self.enabled_location_categories.add(DS3LocationCategory.SHIELD)
        if self.options.enable_armor_locations:
            self.enabled_location_categories.add(DS3LocationCategory.ARMOR)
        if self.options.enable_ring_locations:
            self.enabled_location_categories.add(DS3LocationCategory.RING)
        if self.options.enable_spell_locations:
            self.enabled_location_categories.add(DS3LocationCategory.SPELL)
        if self.options.enable_unique_locations:
            self.enabled_location_categories.add(DS3LocationCategory.UNIQUE)
        if self.options.enable_key_locations:
            self.enabled_location_categories.add(DS3LocationCategory.KEY)
            if self.options.early_banner == "early_global":
                self.multiworld.early_items[self.player]['Small Lothric Banner'] = 1
            elif self.options.early_banner == "early_local":
                self.multiworld.local_early_items[self.player]['Small Lothric Banner'] = 1
        if self.options.enable_misc_locations:
            self.enabled_location_categories.add(DS3LocationCategory.MISC)
        if self.options.enable_health_locations:
            self.enabled_location_categories.add(DS3LocationCategory.HEALTH)
        if self.options.upgrade_locations != "not_randomized":
            self.enabled_location_categories.add(DS3LocationCategory.UPGRADE)
        if self.options.soul_locations != "not_randomized":
            self.enabled_location_categories.add(DS3LocationCategory.SOUL)

        # Randomize Yhorm manually so that we know where to place the Storm Ruler.
        if self.options.randomize_enemies:
            self.yhorm_location = self.multiworld.random.choice(
                [boss for boss in all_bosses if self._allow_boss_for_yhorm(boss)])

            # If Yhorm is early, make sure the Storm Ruler is easily available to avoid BK
            if (
                self.yhorm_location.name == "Iudex Gundyr" or
                self.yhorm_location.name == "Vordt of the Boreal Valley" or (
                    self.yhorm_location.name == "Dancer of the Boreal Valley" and
                    not self.multiworld.late_basin_of_vows
                )
            ):
                self.multiworld.early_items[self.player]['Storm Ruler'] = 1
                self.multiworld.local_items[self.player].value.add('Storm Ruler')
        else:
            self.yhorm_location = default_yhorm_location


    def _allow_boss_for_yhorm(self, boss: DS3BossInfo) -> bool:
        """Returns whether boss is a valid location for Yhorm in this seed."""

        if not self.options.enable_dlc and boss.dlc: return False

        if not self.options.enable_weapon_locations:
            # If weapons aren't randomized, make sure the player can get to the normal Storm Ruler
            # location before they need to get through Yhorm.
            if boss.before_storm_ruler: return False

            # If keys also aren't randomized, make sure Yhorm isn't blocking access to the Small
            # Doll or it won't be possible to get into Profaned Capital before beating him.
            if (
                not self.options.enable_key_locations
                and boss.name in {"Crystal Sage", "Deacons of the Deep"}
            ):
                return False

        if boss.name != "Iudex Gundyr": return True

        # Cemetery of Ash has very few locations and all of them are excluded by default, so only
        # allow Yhorm as Iudex Gundyr if there's at least one available location.
        excluded = self.multiworld.exclude_locations[self.player].value
        return any(
            self.is_location_available(location)
            and location.name not in excluded
            and location.name != "CA: Coiled Sword"
            for location in location_tables["Cemetery of Ash"]
        )


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
        if self.options.enable_dlc:
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
        if self.options.enable_dlc:
            create_connection("Cathedral of the Deep", "Painted World of Ariandel (Before Contraption)")
            create_connection("Painted World of Ariandel (Before Contraption)",
                              "Painted World of Ariandel (After Contraption)")
            create_connection("Painted World of Ariandel (After Contraption)", "Dreg Heap")
            create_connection("Dreg Heap", "Ringed City")


    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        # Use this to un-exclude event locations so the fill doesn't complain about items behind
        # them being unreachable.
        excluded = self.multiworld.exclude_locations[self.player].value

        for location in location_table:
            if self.is_location_available(location):
                new_location = DarkSouls3Location(
                    self.player,
                    location,
                    new_region
                )

                # Mark Red Eye Orb as missable if key locations aren't being randomized, because the
                # Lift Chamber Key is missable by default.
                if (
                    not self.options.enable_key_locations
                    and location.name == "HWL: Red Eye Orb (wall tower, miniboss)"
                ):
                    new_location.progress_type = LocationProgressType.EXCLUDED
            else:
                # Don't allow Siegward's Storm Ruler to mark Yhorm as defeatable.
                if location.name == "PC: Storm Ruler (Siegward)": continue

                # Replace non-randomized progression items with events
                event_item = (
                    self.create_item(location.default_item_name) if location.default_item_name
                    else DarkSouls3Item.event(location.name, self.player)
                )
                if event_item.classification != ItemClassification.progression: continue

                new_location = DarkSouls3Location(
                    self.player,
                    location,
                    parent = new_region,
                    event = True,
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                if location.name in excluded: excluded.remove(location.name)

            if region_name == "Menu":
                add_item_rule(new_location, lambda item: not item.advancement)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        # Just used to efficiently deduplicate items
        item_set = set()

        # Gather all default items on randomized locations
        itempool: List[DarkSouls3Item] = []
        num_required_extra_items = 0
        for location in self.multiworld.get_unfilled_locations(self.player):
            if not self.is_location_available(location.name):
                raise Exception("DS3 generation bug: Added an unavailable location.")

            item = item_dictionary[location.data.default_item_name]
            if item.category == DS3ItemCategory.SKIP:
                num_required_extra_items += 1
            elif not item.unique:
                itempool.append(self.create_item(location.data.default_item_name))
            else:
                # For unique items, make sure there aren't duplicates in the item set even if there
                # are multiple in-game locations that provide them.
                if location.data.default_item_name in item_set:
                    num_required_extra_items += 1
                else:
                    item_set.add(location.data.default_item_name)
                    itempool.append(self.create_item(location.data.default_item_name))

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
            if item.inject and (not item.is_dlc or self.options.enable_dlc)
        ]
        number_to_inject = min(num_required_extra_items, len(injectable_items))
        for item in self.multiworld.random.sample(injectable_items, k=number_to_inject):
            num_required_extra_items -= 1
            itempool.append(self.create_item(item.name))

        # Extra filler items for locations containing SKIP items
        itempool.extend(self.create_filler() for _ in range(num_required_extra_items))

        # Add items to itempool
        self.multiworld.itempool += itempool


    def create_item(self, item: Union[str, DS3ItemData]) -> Item:
        data = item if isinstance(item, DS3ItemData) else item_dictionary[item]
        classification = None
        if self.multiworld and (
            (
                data.useful_if == UsefulIf.BASE and
                not self.options.enable_dlc and
                not self.options.enable_ngp
            )
            or (data.useful_if == UsefulIf.NO_DLC and not self.options.enable_dlc)
            or (data.useful_if == UsefulIf.NO_NGP and not self.options.enable_ngp)
        ):
            classification = ItemClassification.useful

        if (
            self.options.randomize_weapon_level != "none"
            and data.category.upgrade_level
            # Because we require the Pyromancy Flame to be available early, don't upgrade it so it
            # doesn't get shuffled around by weapon smoothing.
            and not data.name == "Pyromancy FLame"
        ):
            # if the user made an error and set a min higher than the max we default to the max
            max_5 = self.multiworld.max_levels_in_5[self.player]
            min_5 = min(self.multiworld.min_levels_in_5[self.player], max_5)
            max_10 = self.multiworld.max_levels_in_10[self.player]
            min_10 = min(self.multiworld.min_levels_in_10[self.player], max_10)
            weapon_level_percentage = self.options.randomize_weapon_level_percentage

            if self.multiworld.random.randint(0, 99) < weapon_level_percentage:
                if data.category.upgrade_level == 5:
                    data = data.upgrade(self.multiworld.random.randint(min_5, max_5))
                elif data.category.upgrade_level == 10:
                    data = data.upgrade(self.multiworld.random.randint(min_10, max_10))

        if self.options.randomize_infusion and data.category.is_infusible:
            infusion_percentage = self.options.randomize_infusion_percentage
            if self.multiworld.random.randint(0, 99) < infusion_percentage:
                data = data.infuse(self.multiworld.random.choice(list(Infusion)))

        return DarkSouls3Item(self.player, data, classification=classification)


    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_item_names)


    def set_rules(self) -> None:
        # Define the access rules to the entrances
        self._add_entrance_rule("Firelink Shrine Bell Tower", "Tower Key")
        self._add_entrance_rule("Undead Settlement", "Small Lothric Banner")
        self._add_entrance_rule("Road of Sacrifices", "US -> RS")
        self._add_entrance_rule("Cathedral of the Deep", "RS -> CD")
        self._add_entrance_rule("Farron Keep", "RS -> FK")
        self._add_entrance_rule("Catacombs of Carthus", "FK -> CC")
        self._add_entrance_rule("Irithyll Dungeon", "IBV -> ID")
        self._add_entrance_rule("Lothric Castle", "Basin of Vows")
        self._add_entrance_rule("Untended Graves", "CKG -> UG")
        self._add_entrance_rule("Irithyll of the Boreal Valley", "Small Doll")
        self._add_entrance_rule("Anor Londo", "IBV -> AL")
        self._add_entrance_rule("Archdragon Peak", "Path of the Dragon")
        self._add_entrance_rule("Grand Archives", "Grand Archives Key")
        self._add_entrance_rule(
            "Kiln of the First Flame",
            lambda state: state.has("Cinders of a Lord - Abyss Watcher", self.player) and
                          state.has("Cinders of a Lord - Yhorm the Giant", self.player) and
                          state.has("Cinders of a Lord - Aldrich", self.player) and
                          state.has("Cinders of a Lord - Lothric Prince", self.player))

        if self.options.late_basin_of_vows:
            self._add_entrance_rule("Lothric Castle", "Small Lothric Banner")

        # DLC Access Rules Below
        if self.options.enable_dlc:
            self._add_entrance_rule("Painted World of Ariandel (Before Contraption)", "CD -> PW1")
            self._add_entrance_rule("Painted World of Ariandel (After Contraption)", "Contraption Key")
            self._add_entrance_rule("Dreg Heap", "PW2 -> DH")
            self._add_entrance_rule("Ringed City", "Small Envoy Banner")

            if self.options.late_dlc:
                self._add_entrance_rule("Painted World of Ariandel (After Contraption)", "Small Doll")

        # Define the access rules to some specific locations
        if self.options.enable_key_locations:
            self._add_location_rule("HWL: Red Eye Orb (wall tower, miniboss)",
                                    "Lift Chamber Key")
        self._add_location_rule("ID: Bellowing Dragoncrest Ring (drop from B1 towards pit)",
                                "Jailbreaker's Key")
        self._add_location_rule("ID: Covetous Gold Serpent Ring (Siegward's cell)", "Old Cell Key")
        self._add_location_rule("UG: Hornet Ring (environs, right of main path)",
                                "Small Lothric Banner")
        self._add_entrance_rule("Karla's Shop", "Jailer's Key Ring")

        # Ashes
        ashes = {
            "Mortician's Ashes": ["Alluring Skull", "Ember", "Grave Key"],
            "Dreamchaser's Ashes": ["Life Ring", "Hidden Blessing"],
            "Paladin's Ashes": ["Lloyd's Shield Ring"],
            "Grave Warden's Ashes": ["Ember"],
            "Prisoner Chief's Ashes": [
                "Karla's Pointed Hat", "Karla's Coat", "Karla's Gloves", "Karla's Trousers"
            ],
            "Xanthous Ashes": ["Xanthous Overcoat", "Xanthous Gloves", "Xanthous Trousers"],
            "Dragon Chaser's Ashes": ["Ember"],
            "Easterner's Ashes": [
                "Washing Pole", "Eastern Helm", "Eastern Armor", "Eastern Gauntlets",
                "Eastern Leggings", "Wood Grain Ring",
            ],
            "Captain's Ashes": [
                "Millwood Knight Helm", "Millwood Knight Armor", "Millwood Knight Gauntlets",
                "Millwood Knight Leggings", "Refined Gem",
            ]
        }
        for (ash, items) in ashes.items():
            self._add_location_rule([f"FS: {item} ({ash})" for item in items], ash)

        # Soul transposition
        transpositions = [
            (
                "Soul of Boreal Valley Vordt", "Vordt",
                ["Vordt's Great Hammer", "Pontiff's Left Eye"]
            ),
            ("Soul of Rosaria", "Rosaria", ["Bountiful Sunlight"]),
            ("Soul of Aldrich", "Aldrich", ["Darkmoon Longbow", "Lifehunt Scythe"]),
            (
                "Soul of the Rotted Greatwood", "Greatwood",
                ["Hollowslayer Greatsword", "Arstor's Spear"]
            ),
            ("Soul of a Crystal Sage", "Sage", ["Crystal Sage's Rapier", "Crystal Hail"]),
            ("Soul of the Deacons of the Deep", "Deacons", ["Cleric's Candlestick", "Deep Soul"]),
            ("Soul of a Stray Demon", "Stray Demon", ["Havel's Ring", "Boulder Heave"]),
            (
                "Soul of the Blood of the Wolf", "Abyss Watchers",
                ["Farron Greatsword", "Wolf Knight's Greatsword"]
            ),
            ("Soul of High Lord Wolnir", "Wolnir", ["Wolnir's Holy Sword", "Black Serpent"]),
            ("Soul of a Demon", "Fire Demon", ["Demon's Greataxe", "Demon's Fist"]),
            (
                "Soul of the Old Demon King", "Old Demon King",
                ["Old King's Great Hammer", "Chaos Bed Vestiges"]
            ),
            (
                "Soul of Pontiff Sulyvahn", "Pontiff",
                ["Greatsword of Judgment", "Profaned Greatsword"]
            ),
            ("Soul of Yhorm the Giant", "Yhorm", ["Yhorm's Great Machete", "Yhorm's Greatshield"]),
            ("Soul of the Dancer", "Dancer", ["Dancer's Enchanted Swords", "Soothing Sunlight"]),
            (
                "Soul of Dragonslayer Armour", "Dragonslayer",
                ["Dragonslayer Greataxe", "Dragonslayer Greatshield"]
            ),
            (
                "Soul of Consumed Oceiros", "Oceiros",
                ["Moonlight Greatsword", "White Dragon Breath"]
            ),
            (
                "Soul of the Twin Princes", "Princes",
                ["Lorian's Greatsword", "Lothric's Holy Sword"]
            ),
            ("Soul of Champion Gundyr", "Champion", ["Gundyr's Halberd", "Prisoner's Chain"]),
            (
                "Soul of the Nameless King", "Nameless",
                ["Storm Curved Sword", "Dragonslayer Swordspear", "Lightning Storm"]
            ),
            ("Soul of the Lords", "Cinder", ["Firelink Greatsword", "Sunlight Spear"]),
            ("Soul of Sister Friede", "Friede", ["Friede's Great Scythe", "Rose of Ariandel"]),
            ("Soul of the Demon Prince", "Demon Prince", ["Demon's Scar", "Seething Chaos"]),
            ("Soul of Darkeater Midir", "Midir", ["Frayed Blade", "Old Moonlight"]),
            ("Soul of Slave Knight Gael", "Gael", ["Gael's Greatsword", "Repeating Crossbow"]),
        ]
        for (soul, soul_name, items) in transpositions:
            self._add_location_rule([
                f"FS: {item} (Ludleth for {soul_name})" for item in items
            ], soul)

        # List missable locations even though they never contain progression items so that the game
        # knows what sphere they're in. This is especially useful for item smoothing. We could add
        # rules for boss transposition items as well, but then we couldn't freely reorder boss soul
        # locations for smoothing.

        self._add_location_rule("FS: Lift Chamber Key (Leonhard)", "Pale Tongue")
        self._add_location_rule([
            "FK: Twinkling Dragon Head Stone (Hawkwood drop)",
            "FS: Hawkwood's Swordgrass (Andre after gesture in AP summit)"
        ], "Twinkling Dragon Torso Stone")

        # Shop unlocks
        shop_unlocks = {
            "Cornyx": [
                (
                    "Great Swamp Pyromancy Tome", "Great Swamp Tome",
                    ["Poison Mist", "Fire Orb", "Profuse Sweat", "Bursting Fireball"]
                ),
                (
                    "Carthus Pyromancy Tome", "Carthus Tome",
                    ["Acid Surge", "Carthus Flame Arc", "Carthus Beacon"]
                ),
                ("Izalith Pyromancy Tome", "Izalith Tome", ["Great Chaos Fire Orb", "Chaos Storm"]),
            ],
            "Irina": [
                (
                    "Braille Divine Tome of Carim", "Tome of Carim",
                    ["Med Heal", "Tears of Denial", "Force"]
                ),
                (
                    "Braille Divine Tome of Lothric", "Tome of Lothric",
                    ["Bountiful Light", "Magic Barrier", "Blessed Weapon"]
                ),
            ],
            "Orbeck": [
                ("Sage's Scroll", "Sage's Scroll", ["Great Farron Dart", "Farron Hail"]),
                (
                    "Golden Scroll", "Golden Scroll",
                    [
                        "Cast Light", "Repair", "Hidden Weapon", "Hidden Body",
                        "Twisted Wall of Light"
                    ],
                ),
                ("Logan's Scroll", "Logan's Scroll", ["Homing Soulmass", "Soul Spear"]),
                (
                    "Crystal Scroll", "Crystal Scroll",
                    ["Homing Crystal Soulmass", "Crystal Soul Spear", "Crystal Magic Weapon"]
                ),
            ],
            "Karla": [
                ("Quelana Pyromancy Tome", "Quelana Tome", ["Firestorm", "Rapport", "Fire Whip"]),
                (
                    "Grave Warden Pyromancy Tome", "Grave Warden Tome",
                    ["Black Flame", "Black Fire Orb"]
                ),
                ("Deep Braille Divine Tome", "Deep Braille Tome", ["Gnaw", "Deep Protection"]),
                (
                    "Londor Braille Divine Tome", "Londor Tome",
                    ["Vow of Silence", "Dark Blade", "Dead Again"]
                ),
            ],
        }
        for (shop, unlocks) in shop_unlocks.items():
            for (key, key_name, items) in unlocks:
                self._add_location_rule(
                    [f"FS: {item} ({shop} for {key_name})" for item in items], key)

        self._add_location_rule([
            "FS: Divine Blessing (Greirat from US)",
            "FS: Ember (Greirat from US)",
        ], lambda state: state.can_reach("Go To Undead Settlement", "Entrance", self.player))
        self._add_location_rule([
            "FS: Divine Blessing (Greirat from IBV)",
            "FS: Hidden Blessing (Greirat from IBV)",
            "FS: Titanite Scale (Greirat from IBV)",
            "FS: Twinkling Titanite (Greirat from IBV)",
            "FS: Ember (shop for Greirat's Ashes)"
        ], lambda state: state.can_reach(
            "Go To Irithyll of the Boreal Valley",
            "Entrance",
            self.player
        ))
        self._add_location_rule(
            "FS: Ember (shop for Greirat's Ashes)",
            lambda state: state.can_reach("Go To Grand Archives", "Entrance", self.player)
        )

        # Crow items
        crow = {
            "Loretta's Bone": "Ring of Sacrifice",
            # "Avelyn": "Titanite Scale", # Missing from offline randomizer
            "Coiled Sword Fragment": "Titanite Slab",
            "Seed of a Giant Tree": "Iron Leggings",
            "Siegbräu": "Armor of the Sun",
            "Vertebra Shackle": "Lucatiel's Mask",
            "Xanthous Crown": "Lightning Gem",
            "Mendicant's Staff": "Sunlight Shield",
            "Blacksmith Hammer": "Titanite Scale",
            "Large Leather Shield": "Twinkling Titanite",
            "Moaning Shield": "Blessed Gem",
            "Eleonora": "Hollow Gem",
        }
        for (given, received) in crow.items():
            self._add_location_rule(f"FSBT: {received} (crow for {given})", given)

        # The offline randomizer edits events to guarantee that Greirat won't go to Lothric until
        # Grand Archives is available, so his shop will always be available one way or another.
        self._add_entrance_rule("Greirat's Shop", "Cell Key")

        self._add_location_rule([
            f"FS: {item} (shop after killing Leonhard)"
            for item in ["Leonhard's Garb", "Leonhard's Gauntlets", "Leonhard's Trousers"]
        ], "Black Eye Orb")

        # You could just kill NPCs for these, but it's more fun to ensure the player can do
        # their quests.
        self._add_location_rule("HWL: Basin of Vows (Emma)", "Small Doll")
        self._add_location_rule(
            "ID: Prisoner Chief's Ashes (B2 near, locked cell by stairs)",
            "Jailer's Key Ring"
        )
        self._add_location_rule([
            "US: Old Sage's Blindfold (kill Cornyx)", "US: Cornyx's Garb (kill Cornyx)",
            "US: Cornyx's Wrap (kill Cornyx)", "US: Cornyx's Skirt (kill Cornyx)"
        ], lambda state: (
            state.has("Great Swamp Pyromancy Tome", self.player)
            and state.has("Carthus Pyromancy Tome", self.player)
            and state.has("Izalith Pyromancy Tome", self.player)
        ))

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
        if self.options.enable_dlc:
            self._add_entrance_rule("Painted World of Ariandel (After Contraption)", has_any_scroll)

        self._add_location_rule("HWL: Soul of the Dancer", "Basin of Vows")

        # Lump Soul of the Dancer in with LC for locations that should not be reachable
        # before having access to US. (Prevents requiring getting Basin to fight Dancer to get SLB to go to US)
        if self.options.late_basin_of_vows:
            self._add_location_rule("HWL: Soul of the Dancer", "Small Lothric Banner")
            # This isn't really necessary, but it ensures that the game logic knows players will
            # want to do Lothric Castle after at least being _able_ to access Catacombs. This is
            # useful for smooth item placement.
            self._add_location_rule("HWL: Soul of the Dancer", has_any_scroll)

        self._add_location_rule([
            "LC: Grand Archives Key (by Grand Archives door, after PC and AL bosses)",
            "LC: Gotthard Twinswords (by Grand Archives door, after PC and AL bosses)"
        ], lambda state: (
            state.can_reach("AL: Cinders of a Lord - Aldrich", "Location", self.player) and
            state.can_reach("PC: Cinders of a Lord - Yhorm the Giant", "Location", self.player)
        ))

        self._add_location_rule([
            "FS: Morne's Great Hammer (Eygon)",
            "FS: Moaning Shield (Eygon)"
        ], lambda state: (
            state.can_reach("LC: Soul of Dragonslayer Armour", "Location", self.player) and
            state.can_reach("FK: Soul of the Blood of the Wolf", "Location", self.player)
        ))

        self._add_location_rule([
            "CKG: Drakeblood Helm (tomb, after killing AP mausoleum NPC)",
            "CKG: Drakeblood Armor (tomb, after killing AP mausoleum NPC)",
            "CKG: Drakeblood Gauntlets (tomb, after killing AP mausoleum NPC)",
            "CKG: Drakeblood Leggings (tomb, after killing AP mausoleum NPC)",
        ], lambda state: state.can_reach(
            "AP: Drakeblood Greatsword (mausoleum, NPC drop)",
            "Location",
            self.player
        ))

        self._add_location_rule([
            "FK: Havel's Helm (upper keep, after killing AP belfry roof NPC)",
            "FK: Havel's Armor (upper keep, after killing AP belfry roof NPC)",
            "FK: Havel's Gauntlets (upper keep, after killing AP belfry roof NPC)",
            "FK: Havel's Leggings (upper keep, after killing AP belfry roof NPC)",
        ], lambda state: state.can_reach(
            "AP: Dragon Tooth (belfry roof, NPC drop)",
            "Location",
            self.player
        ))

        self._add_location_rule([
            "RC: Dragonhead Shield (streets monument, across bridge)",
            "RC: Large Soul of a Crestfallen Knight (streets monument, across bridge)",
            "RC: Divine Blessing (streets monument, mob drop)",
            "RC: Lapp's Helm (Lapp)",
            "RC: Lapp's Armor (Lapp)",
            "RC: Lapp's Gauntlets (Lapp)",
            "RC: Lapp's Leggings (Lapp)",
        ], "Chameleon")

        # Forbid shops from carrying items with multiple counts (the offline randomizer has its own
        # logic for choosing how many shop items to sell), and from carring soul items.
        for location in location_dictionary.values():
            if self.is_location_available(location):
                if location.shop:
                    add_item_rule(self.multiworld.get_location(location.name, self.player),
                                    lambda item: (
                                        item.player != self.player or
                                        (item.data.count == 1 and not item.data.souls)
                                    ))

        # This particular location is bugged, and will drop two copies of whatever item is placed
        # there.
        if self.is_location_available("US: Young White Branch (by white tree #2)"):
            loc = self.multiworld.get_location(
                "US: Young White Branch (by white tree #2)",
                self.player
            )
            add_item_rule(loc, lambda item: item.player == self.player and not item.data.unique)
        
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


    def _add_location_rule(self, location: Union[str, List[str]], rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the given location if it that location is randomized.

        The rule can just be a single item/event name as well as an explicit rule lambda.
        """
        locations = location if type(location) is list else [location]
        for location in locations:
            if not self.is_location_available(location): return
            if isinstance(rule, str):
                assert item_dictionary[rule].classification == ItemClassification.progression
                rule = lambda state, item=rule: state.has(item, self.player)
            add_rule(self.multiworld.get_location(location, self.player), rule)


    def _add_entrance_rule(self, region: str, rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the entrance to the given region."""
        assert region in location_tables
        if not any(region == reg.name for reg in self.multiworld.regions): return
        if isinstance(rule, str):
            if " -> " not in rule:
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
            (not data.npc or self.options.enable_npc_locations) and
            (not data.dlc or self.options.enable_dlc) and
            (not data.ngp or self.options.enable_ngp)
        )


    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.yhorm_location != default_yhorm_location:
            spoiler_handle.write(
                f"Yhorm takes the place of {self.yhorm_location.name} in " +
                f"{self.multiworld.get_player_name(self.player)}'s world\n")


    def pre_fill(self) -> None:
        # Fill this manually so that, if very few slots are available in Cemetery of Ash, this
        # doesn't get locked out by bad rolls on the next two fills.
        if self.yhorm_location.name == 'Iudex Gundyr':
            self._fill_local_item("Storm Ruler", {"Cemetery of Ash"},
                                  lambda location: location.name != "CA: Coiled Sword (boss drop)",
                                  mandatory = True)

        # Don't place this in the multiworld because it's necessary almost immediately, and don't
        # mark it as a blocker for HWL because having a miniscule Sphere 1 screws with progression
        # balancing.
        self._fill_local_item("Coiled Sword", ["Cemetery of Ash", "Firelink Shrine"])

        # If upgrade smoothing is enabled, make sure one raw gem is available early for SL1 players
        if self.options.upgrade_locations == "smooth":
            self._fill_local_item("Raw Gem", [
                "Cemetery of Ash",
                "Firelink Shrine",
                "High Wall of Lothric"
            ])


    def _fill_local_item(
        self, name: str,
        regions: List[str],
        additional_condition: Optional[Callable[[DarkSouls3Location], bool]] = None,
        mandatory = False,
    ) -> None:
        """Chooses a valid location for the item with the given name and places it there.
        
        This always chooses a local location among the given regions. If additional_condition is
        passed, only locations meeting that condition will be considered.

        If mandatory is True, this will throw an error if the item could not be filled in.
        """
        item = next(
            (
                item for item in self.multiworld.itempool
                if item.player == self.player and item.name == name
            ),
            None
        )
        if not item: return

        candidate_locations = [
            location for location in (
                self.multiworld.get_location(location.name, self.player)
                for region in regions
                for location in location_tables[region]
                if self.is_location_available(location)
                and not location.missable
                and not location.conditional
                and (not additional_condition or additional_condition(location))
            )
            if not location.item and location.progress_type != LocationProgressType.EXCLUDED
            and location.item_rule(item)
        ]

        if not candidate_locations:
            if not mandatory: return
            raise Exception(f"No valid locations to place {name}")

        location = self.multiworld.random.choice(candidate_locations)
        location.place_locked_item(item)
        self.multiworld.itempool.remove(item)

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
            locations_by_sphere.append(self._shuffle(sorted(sphere_locations)))

            old_length = len(unchecked_locations)
            unchecked_locations.difference_update(sphere_locations)
            if len(unchecked_locations) == old_length: break # Unreachable locations

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

        # All DarkSouls3Items for this world that have been assigned anywhere, grouped by name
        full_items_by_name = defaultdict(list)
        for location in self.multiworld.get_filled_locations():
            if location.item.player == self.player:
                full_items_by_name[location.item.name].append(location.item)

        def smooth_items(item_order: List[Union[DS3ItemData, DarkSouls3Item]]) -> None:
            """Rearrange all items in item_order to match that order.

            Note: this requires that item_order exactly matches the number of placed items from this
            world matching the given names.
            """

            # Convert items to full DarkSouls3Items.
            item_order = [
                item for item in (
                    (
                        # full_items_by_name won't contain DLC items if the DLC is disabled.
                        (full_items_by_name[item.name] or [None]).pop(0)
                        if isinstance(item, DS3ItemData) else item
                    )
                    for item in item_order
                )
                # Never re-order event items, because they weren't randomized in the first place.
                if item and item.code is not None
            ]

            names = {item.name for item in item_order}

            for i, all_locations in enumerate(locations_by_sphere):
                locations = [
                    loc for loc in all_locations
                    if loc.item.player == self.player
                    and not loc.locked
                    and loc.item.name in names
                ]

                # Check the game, not the player, because we know how to sort within regions for DS3
                offworld = self._shuffle(loc for loc in locations if loc.game != "Dark Souls III")
                onworld = sorted((loc for loc in locations if loc.game == "Dark Souls III"),
                                 key=lambda loc: loc.data.region_value)

                # Give offworld regions the last (best) items within a given sphere
                for location in onworld + offworld:
                    new_item = self._pop_item(location, item_order)
                    location.item = new_item
                    new_item.location = location

        if self.options.upgrade_locations == "smooth":
            base_names = {
                "Titanite Shard", "Large Titanite Shard", "Titanite Chunk", "Titanite Slab",
                "Titanite Scale", "Twinkling Titanite", "Farron Coal", "Sage's Coal", "Giant's Coal",
                "Profaned Coal"
            }
            smooth_items([item for item in all_item_order if item.base_name in base_names])

        if self.options.soul_locations == "smooth":
            # Shuffle larger boss souls among themselves because they're all worth 10-20k souls in
            # no particular order and that's a lot more interesting than getting them in the same
            # order every single run.
            shuffled_order = self._shuffle([
                item.name for item in item_dictionary.values()
                if item.category == DS3ItemCategory.BOSS and item.souls and item.souls >= 10000
            ])
            shuffled = set(shuffled_order)
            item_order: List[DS3ItemData] = []
            for item in all_item_order:
                if not item.souls: continue
                if item.base_name in shuffled:
                    item_order.append(item_dictionary[shuffled_order.pop(0)])
                else:
                    item_order.append(item)
            smooth_items(item_order)

        if self.options.upgraded_weapon_locations == "smooth":
            upgraded_weapons = [
                location.item
                for location in self.multiworld.get_filled_locations()
                if location.item.player == self.player
                and location.item.level and location.item.level > 0
                and location.item.classification != ItemClassification.progression
            ]
            upgraded_weapons.sort(key=lambda item: item.level)
            smooth_items(upgraded_weapons)


    def _shuffle(self, seq: Sequence) -> List:
        """Returns a shuffled copy of a sequence."""
        copy = list(seq)
        self.multiworld.random.shuffle(copy)
        return copy


    def _pop_item(
        self,
        location: Location,
        items: List[Union[DS3ItemData, DarkSouls3Item]]
    ) -> Union[DS3ItemData, DarkSouls3Item]:
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
            if item.data.ds3_code: ap_ids_to_ds3_ids[str(item.code)] = item.data.ds3_code
            if item.data.count != 1: item_counts[str(item.code)] = item.data.count

        # A map from Archipelago's location IDs to the keys the offline
        # randomizer uses to identify locations.
        location_ids_to_keys: Dict[str, str] = {}
        for location in self.multiworld.get_filled_locations(self.player):
            # Skip events and only look at this world's locations
            if (location.address is not None and location.item.code is not None
                    and location.data.offline):
                location_ids_to_keys[location.address] = location.data.offline

        slot_data = {
            "options": {
                "random_starting_loadout": self.options.random_starting_loadout.value,
                "require_one_handed_starting_weapons": self.options.require_one_handed_starting_weapons.value,
                "auto_equip": self.options.auto_equip.value,
                "lock_equip": self.options.lock_equip.value,
                "no_weapon_requirements": self.options.no_weapon_requirements.value,
                "death_link": self.options.death_link.value,
                "no_spell_requirements": self.options.no_spell_requirements.value,
                "no_equip_load": self.options.no_equip_load.value,
                "enable_dlc": self.options.enable_dlc.value,
                "enable_ngp": self.options.enable_ngp.value,
                "smooth_soul_locations": self.options.soul_locations == "smooth",
                "smooth_upgrade_locations": self.options.upgrade_locations == "smooth",
                "randomize_enemies": self.options.randomize_enemies.value,
                "randomize_mimics_with_enemies": self.options.randomize_mimics_with_enemies.value,
                "randomize_small_crystal_lizards_with_enemies": self.options.randomize_small_crystal_lizards_with_enemies.value,
                "reduce_harmless_enemies": self.options.reduce_harmless_enemies.value,
                "simple_early_bosses": self.options.simple_early_bosses.value,
                "scale_enemies": self.options.scale_enemies.value,
                "all_chests_are_mimics": self.options.all_chests_are_mimics.value,
                "impatient_mimics": self.options.impatient_mimics.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            # Reserializing here is silly, but it's easier for the offline randomizer.
            "random_enemy_preset": json.dumps(self.options.random_enemy_preset.value),
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
