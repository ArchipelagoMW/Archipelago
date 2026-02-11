# world/spyro2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import OptionError

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule, forbid_item

from .Items import Spyro2Item, Spyro2ItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import Spyro2Location, Spyro2LocationCategory, location_tables, location_dictionary
from .Options import Spyro2Option, GoalOptions, GemsanityOptions, MoneybagsOptions, SparxUpgradeOptions, \
    AbilityOptions, RandomizeGemColorOptions, LevelLockOptions, spyro_options_groups


class Spyro2Web(WebWorld):
    bug_report_page = ""
    theme = "stone"
    option_groups = spyro_options_groups
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Spyro 2 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin", "Uroogla"]
    )
    game_info_languages = ["en"]
    tutorials = [setup_en]


class Spyro2World(World):
    """
    Spyro 2: Ripto's Rage! is a 1999 platforming adventure game where the purple dragon Spyro travels to the realm of Avalar to stop the evil sorcerer Ripto. Players collect talismans and orbs by completing minigames and challenges to open new areas and progress the story, all while learning new abilities like swimming and climbing. The game features vibrant worlds, humorous characters, and a focus on exploration and problem-solving.
    """

    game: str = "Spyro 2"
    options_dataclass = Spyro2Option
    options: Spyro2Option
    topology_present: bool = False  # Turn on when entrance randomizer is available.
    web = Spyro2Web()
    data_version = 0
    base_id = 1230000
    enabled_location_categories: Set[Spyro2LocationCategory]
    required_client_version = (0, 5, 0)
    # TODO: Remember to update this!
    ap_world_version = "1.0.1"
    item_name_to_id = Spyro2Item.get_name_to_id()
    location_name_to_id = Spyro2Location.get_name_to_id()
    item_name_groups = {}
    item_descriptions = item_descriptions
    key_locked_levels = []
    glitches_item_name: str = "Glitched Item"  # UT Glitched Logic Support, Not implemented yet.
    options_copy = []  # Copy of options used to support UT.

    all_levels = [
        "Summer Forest","Glimmer","Idol Springs","Colossus","Hurricos","Aquaria Towers","Sunny Beach","Ocean Speedway","Crush's Dungeon",
        "Autumn Plains","Skelos Badlands","Crystal Glacier","Breeze Harbor","Zephyr","Metro Speedway","Scorch","Shady Oasis","Magma Cone","Fracture Hills","Icy Speedway","Gulp's Overlook",
        "Winter Tundra","Mystic Marsh","Cloud Temples","Canyon Speedway","Robotica Farms","Metropolis","Dragon Shores","Ripto's Arena",
    ]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()
        self.enabled_hint_locations = []
        self.chosen_gem_locations = []
        # TODO: Implement.
        self.level_orb_requirements = {
            "Idol Springs": 0,
            "Colossus": 0,
            "Hurricos": 0,
            "Sunny Beach": 0,
            "Aquaria Towers": 0,
            "Crystal Glacier": 0,
            "Skelos Badlands": 0,
            "Breeze Harbor": 0,
            "Zephyr": 0,
            "Scorch": 0,
            "Fracture Hills": 0,
            "Magma Cone": 0,
            "Shady Oasis": 0,
            "Icy Speedway": 0,
            "Mystic Marsh": 0,
            "Canyon Speedway": 0,
            "Robotica Farms": 0,
        }

    def generate_early(self):
        is_ut = getattr(self.multiworld, "generation_is_fake", False)

        self.enabled_location_categories.add(Spyro2LocationCategory.TALISMAN)
        self.enabled_location_categories.add(Spyro2LocationCategory.ORB)
        self.enabled_location_categories.add(Spyro2LocationCategory.EVENT)
        if self.options.enable_25_pct_gem_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.GEM_25)
        if self.options.enable_50_pct_gem_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.GEM_50)
        if self.options.enable_75_pct_gem_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.GEM_75)
        if self.options.enable_gem_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.GEM_100)
        if self.options.enable_skillpoint_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.SKILLPOINT)
        if self.options.goal.value in [GoalOptions.ALL_SKILLPOINTS, GoalOptions.EPILOGUE]:
            self.enabled_location_categories.add(Spyro2LocationCategory.SKILLPOINT_GOAL)
        if self.options.enable_total_gem_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.TOTAL_GEM)
        if self.options.goal.value == GoalOptions.TEN_TOKENS:
            self.enabled_location_categories.add(Spyro2LocationCategory.SHORES_TOKEN)
        # Use the Moneybags unlocks for logic if they are in place.  The checks themselves will not be randomized.
        if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY:
            self.enabled_location_categories.add(Spyro2LocationCategory.MONEYBAGS)
        if self.options.enable_life_bottle_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.LIFE_BOTTLE)
        if self.options.enable_gemsanity.value != GemsanityOptions.OFF:
            self.enabled_location_categories.add(Spyro2LocationCategory.GEM)
        if self.options.enable_gemsanity.value == GemsanityOptions.PARTIAL:
            all_gem_locations = []
            for location in location_dictionary:
                if location_dictionary[location].category == Spyro2LocationCategory.GEM:
                    all_gem_locations.append(location)
            # Universal Tracker does not know which gems were picked.  Have it assume all gems were picked when it
            # creates its seed.  The location list on the AP server will then remove all non-selected gems.
            if is_ut:
                self.chosen_gem_locations = []
            else:
                self.chosen_gem_locations = self.multiworld.random.sample(all_gem_locations, k=200)
        if self.options.enable_gemsanity.value == GemsanityOptions.FULL:
            for itemname, item in item_dictionary.items():
                if item.category == Spyro2ItemCategory.GEM:
                    self.options.local_items.value.add(item)
        if self.options.enable_spirit_particle_checks.value:
            self.enabled_location_categories.add(Spyro2LocationCategory.SPIRIT_PARTICLE)

        if hasattr(self.multiworld, "re_gen_passthrough"):
            self.key_locked_levels = self.multiworld.re_gen_passthrough["Spyro 2"]["key_locked_levels"]
        else:
            possible_locked_levels = [
                "Colossus", "Idol Springs", "Hurricos", "Aquaria Towers", "Sunny Beach", "Ocean Speedway",
                "Skelos Badlands", "Crystal Glacier", "Breeze Harbor", "Zephyr", "Metro Speedway", "Scorch", "Shady Oasis",
                "Magma Cone", "Fracture Hills", "Icy Speedway", "Mystic Marsh", "Cloud Temples", "Canyon Speedway",
                "Robotica Farms", "Metropolis", "Dragon Shores"
            ]
            self.key_locked_levels = self.multiworld.random.sample(possible_locked_levels, k=22 - self.options.level_unlocks.value)

        # Generation struggles to place swim, which restricts too much of the seed.
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY:
            self.multiworld.early_items[self.player]["Moneybags Unlock - Swim"] = 1

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in (self.all_levels + ["Inventory"])})
        
        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            
        create_connection("Menu", "Glimmer")
        create_connection("Menu", "Inventory")
                
        create_connection("Glimmer", "Summer Forest")
        create_connection("Summer Forest", "Idol Springs")
        create_connection("Summer Forest", "Colossus")
        create_connection("Summer Forest", "Hurricos")
        create_connection("Summer Forest", "Aquaria Towers")
        create_connection("Summer Forest", "Sunny Beach")
        create_connection("Summer Forest", "Ocean Speedway")
             
        create_connection("Summer Forest", "Crush's Dungeon")
        create_connection("Summer Forest", "Autumn Plains")

        create_connection("Autumn Plains", "Skelos Badlands")
        create_connection("Autumn Plains", "Crystal Glacier")
        create_connection("Autumn Plains", "Breeze Harbor")
        create_connection("Autumn Plains", "Zephyr")
        create_connection("Autumn Plains", "Metro Speedway")
        create_connection("Autumn Plains", "Scorch")
        create_connection("Autumn Plains", "Shady Oasis")
        create_connection("Autumn Plains", "Magma Cone")
        create_connection("Autumn Plains", "Fracture Hills")
        create_connection("Autumn Plains", "Icy Speedway")

        create_connection("Autumn Plains", "Gulp's Overlook")
        create_connection("Autumn Plains", "Winter Tundra")

        create_connection("Winter Tundra", "Mystic Marsh")
        create_connection("Winter Tundra", "Cloud Temples")
        create_connection("Winter Tundra", "Canyon Speedway")
        create_connection("Winter Tundra", "Robotica Farms")
        create_connection("Winter Tundra", "Metropolis")

        create_connection("Winter Tundra", "Ripto's Arena")
        create_connection("Winter Tundra", "Dragon Shores")
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if location.category in self.enabled_location_categories and \
                    location.category not in [Spyro2LocationCategory.EVENT, Spyro2LocationCategory.TOTAL_GEM, Spyro2LocationCategory.GEM]:
                new_location = Spyro2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and \
                    location.category == Spyro2LocationCategory.GEM and \
                    (len(self.chosen_gem_locations) == 0 or location.name in self.chosen_gem_locations):
                new_location = Spyro2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and \
                    location.category == Spyro2LocationCategory.TOTAL_GEM:
                gems_needed = int(location.name.split("Total Gems: ")[1])
                if gems_needed <= self.options.max_total_gem_checks.value:
                    new_location = Spyro2Location(
                        self.player,
                        location.name,
                        location.category,
                        location.default_item,
                        self.location_name_to_id[location.name],
                        new_region
                    )
                    new_region.locations.append(new_location)
            elif location.category == Spyro2LocationCategory.EVENT:
                event_item = self.create_item(location.default_item)
                new_location = Spyro2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                new_region.locations.append(new_location)
        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        itempool: List[Spyro2Item] = []
        itempoolSize = 0

        for location in self.multiworld.get_locations(self.player):
            if location.category in [Spyro2LocationCategory.EVENT, Spyro2LocationCategory.MONEYBAGS, Spyro2LocationCategory.SKILLPOINT_GOAL, Spyro2LocationCategory.SHORES_TOKEN]:
                item = self.create_item(location.default_item_name)
                self.multiworld.get_location(location.name, self.player).place_locked_item(item)
            elif location.category in self.enabled_location_categories:
                itempoolSize += 1

        foo = BuildItemPool(self, itempoolSize, self.options, self.key_locked_levels)
        for item in foo:
            itempool.append(self.create_item(item.name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]
        useful_categories = {}

        if name in key_item_names or \
                name == "Glitched Item" or \
                item_dictionary[name].category in [Spyro2ItemCategory.LEVEL_UNLOCK, Spyro2ItemCategory.TALISMAN, Spyro2ItemCategory.ORB, Spyro2ItemCategory.EVENT, Spyro2ItemCategory.MONEYBAGS, Spyro2ItemCategory.SKILLPOINT_GOAL, Spyro2ItemCategory.TOKEN, Spyro2ItemCategory.GEM, Spyro2ItemCategory.GEMSANITY_PARTIAL] or \
                self.options.enable_progressive_sparx_logic.value and name == 'Progressive Sparx Health Upgrade':
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories or \
                not self.options.enable_progressive_sparx_logic.value and name == 'Progressive Sparx Health Upgrade' or \
                name in ["Double Jump Ability", "Permanent Fireball Ability"]:
            item_classification = ItemClassification.useful
        elif item_dictionary[name].category == Spyro2ItemCategory.TRAP:
            item_classification = ItemClassification.trap
        else:
            item_classification = ItemClassification.filler

        return Spyro2Item(name, item_classification, data, self.player)

    def get_filler_item_name(self) -> str:
        return "Extra Life"
    
    def set_rules(self) -> None:
        def is_boss_defeated(self, boss, state):
            if self.options.enable_open_world and self.options.open_world_ability_and_warp_unlocks and boss in ["Crush", "Gulp"]:
                return True
            return state.has(boss + " Defeated", self.player)

        def can_swim(self, state):
            return state.has("Moneybags Unlock - Swim", self.player) or is_boss_defeated(self, "Ripto", state)

        def can_climb(self, state):
            return state.has("Moneybags Unlock - Climb", self.player) or is_boss_defeated(self, "Ripto", state)

        def can_headbash(self, state):
            return state.has("Moneybags Unlock - Headbash", self.player) or is_boss_defeated(self, "Ripto", state)

        def can_reach_summer_second_half(self, state):
            return can_swim(self, state)

        def can_reach_metro(self, state):
            return state.has("Orb", self.player, 6)

        def can_reach_autumn_second_half(self, state):
            return can_climb(self, state)

        def can_pass_autumn_door(self, state):
            return can_reach_autumn_second_half(self, state) and state.has("Orb", self.player, 8)

        def can_reach_winter_second_half(self, state):
            return can_headbash(self, state)

        def get_gemsanity_gems(self, level, state):
            count = 0
            count += state.count(f"{level} Red Gem", self.player)
            count += state.count(f"{level} Green Gem", self.player) * 2
            count += state.count(f"{level} Blue Gem", self.player) * 5
            count += state.count(f"{level} Gold Gem", self.player) * 10
            count += state.count(f"{level} Pink Gem", self.player) * 25
            count += state.count(f"{level} 50 Gems", self.player) * 50
            return count

        def get_gems_accessible_in_level(self, level, state):
            if self.options.enable_gemsanity.value != GemsanityOptions.OFF and "Speedway" not in level:
                return get_gemsanity_gems(self, level, state)

            # Older versions of Python do not support switch statements, so use if/elif.
            if level == 'Glimmer':
                gems = 353
                if can_climb(self, state):
                    # Upper level in cave; technically accessible with double jump
                    gems += 47
                return gems
            elif level == 'Summer Forest':
                gems = 155
                if can_swim(self, state):
                    # TODO: Count underwater gems for DJ logic.
                    gems += 221
                    if state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state):
                        gems += 14
                    if can_climb(self, state):
                        gems += 10
                return gems
            elif level == 'Idol Springs':
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Idol Springs Unlock", self.player):
                    return 0
                # Probably 315, but gem RNG from the strong chest could impact this - remove those gems from logic.
                gems = 298
                if can_swim(self, state):
                    gems += 102
                return gems
            elif level == 'Colossus':
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Colossus Unlock", self.player):
                    return 0
                return 400
            elif level == 'Hurricos':
                if not can_reach_summer_second_half(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Hurricos Unlock", self.player):
                    return 0
                return 400
            elif level == 'Aquaria Towers':
                if not can_reach_summer_second_half(self, state) or \
                        not (state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state)) or \
                        (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 1, state)):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Aquaria Towers Unlock", self.player):
                    return 0
                # TODO: Allow for getting in without swim as a trick.
                gems = 127
                if state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state):
                    gems += 273
                return gems
            elif level == "Sunny Beach":
                if not can_reach_summer_second_half(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Sunny Beach Unlock", self.player):
                    return 0
                # TODO: Allow for getting in without swim.
                gems = 380
                if can_climb(self, state):
                    gems += 20
                return gems
            elif level == "Ocean Speedway":
                if not can_reach_summer_second_half(self, state) or not state.has("Orb", self.player, 3):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Ocean Speedway Unlock", self.player):
                    return 0
                return 400
            elif level == "Autumn Plains":
                if not (self.options.enable_open_world and self.options.open_world_ability_and_warp_unlocks) and not is_boss_defeated(self, "Crush", state):
                    return 0
                gems = 118
                if can_reach_metro(self, state):
                    gems += 22
                if can_reach_autumn_second_half(self, state):
                    gems += 51
                if can_pass_autumn_door(self, state):
                    gems += 202
                    if state.has("Moneybags Unlock - Shady Oasis Portal", self.player) or is_boss_defeated(self, "Ripto", state):
                        gems += 7
                return gems
            elif level == "Skelos Badlands":
                if not is_boss_defeated(self, "Crush", state) or \
                        (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Skelos Badlands Unlock", self.player):
                    return 0
                return 400
            elif level == "Crystal Glacier":
                if not is_boss_defeated(self, "Crush", state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Crystal Glacier Unlock", self.player):
                    return 0
                gems = 245
                if state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state):
                    gems += 155
                return gems
            elif level == "Breeze Harbor":
                if not is_boss_defeated(self, "Crush", state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Breeze Harbor Unlock", self.player):
                    return 0
                return 400
            elif level == "Zephyr":
                if not is_boss_defeated(self, "Crush", state) or \
                        not (state.has("Moneybags Unlock - Zephyr Portal", self.player) or is_boss_defeated(self, "Ripto", state)):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Zephyr Unlock", self.player):
                    return 0
                gems = 284
                if can_climb(self, state):
                    gems += 116
                return gems
            elif level == "Metro Speedway":
                if not is_boss_defeated(self, "Crush", state) or not can_reach_metro(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Metro Speedway Unlock", self.player):
                    return 0
                return 400
            elif level == "Scorch":
                if not is_boss_defeated(self, "Crush", state) or not can_reach_autumn_second_half(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Scorch Unlock", self.player):
                    return 0
                return 400
            elif level == "Shady Oasis":
                if not is_boss_defeated(self, "Crush", state) or \
                        not can_pass_autumn_door(self, state) or \
                        not (state.has("Moneybags Unlock - Shady Oasis Portal", self.player) or is_boss_defeated(self, "Ripto", state)):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Shady Oasis Unlock", self.player):
                    return 0
                gems = 380
                if can_headbash(self, state):
                    gems += 20
                return gems
            elif level == "Magma Cone":
                if not is_boss_defeated(self, "Crush", state) or \
                        not can_pass_autumn_door(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Magma Cone Unlock", self.player):
                    return 0
                gems = 295
                if state.has("Moneybags Unlock - Magma Cone Elevator", self.player) or is_boss_defeated(self, "Ripto", state):
                    gems += 105
                return gems
            elif level == "Fracture Hills":
                if not is_boss_defeated(self, "Crush", state) or not can_reach_autumn_second_half(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Fracture Hills Unlock", self.player):
                    return 0
                return 400
            elif level == "Icy Speedway":
                if not is_boss_defeated(self, "Crush", state) or \
                        not can_pass_autumn_door(self, state) or \
                        not (state.has("Moneybags Unlock - Icy Speedway Portal", self.player) or is_boss_defeated(self, "Ripto", state)):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Icy Speedway Unlock", self.player):
                    return 0
                return 400
            elif level == "Winter Tundra":
                if not (self.options.enable_open_world and self.options.open_world_ability_and_warp_unlocks) and not is_boss_defeated(self, "Gulp", state):
                    return 0
                gems = 139
                if can_reach_winter_second_half(self, state):
                    gems += 254
                    if state.has("Orb", self.player, self.options.ripto_door_orbs.value):
                        gems += 7
                return gems
            elif level == "Mystic Marsh":
                if not is_boss_defeated(self, "Gulp", state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Mystic Marsh Unlock", self.player):
                    return 0
                return 400
            elif level == "Cloud Temples":
                if not is_boss_defeated(self, "Gulp", state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Cloud Temples Unlock", self.player) or \
                        not state.has("Orb", self.player, 15):
                    return 0
                gems = 375
                if can_headbash(self, state):
                    gems += 25
                return gems
            elif level == "Canyon Speedway":
                if not is_boss_defeated(self, "Gulp", state) or \
                        not (state.has("Moneybags Unlock - Canyon Speedway Portal", self.player) or is_boss_defeated(self, "Ripto", state)):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Canyon Speedway Unlock", self.player):
                    return 0
                return 400
            elif level == "Robotica Farms":
                if not is_boss_defeated(self, "Gulp", state) or \
                        not can_reach_winter_second_half(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Robotica Farms Unlock", self.player):
                    return 0
                return 400
            elif level == "Metropolis":
                if not is_boss_defeated(self, "Gulp", state) or \
                        not can_reach_winter_second_half(self, state):
                    return 0
                if self.options.level_lock_options.value == LevelLockOptions.KEYS and not state.has("Metropolis Unlock", self.player) or \
                        not state.has("Orb", self.player, 25):
                    return 0
                return 400
            return 0

        def has_total_accessible_gems(self, state, max_gems):
            accessible_gems = 0

            for level in self.all_levels:
                accessible_gems += get_gems_accessible_in_level(self, level, state)

            if not is_boss_defeated(self, "Ripto", state):
                # Remove gems for possible Moneybags payments.  To avoid a player locking themselves out of progression,
                # we have to assume every possible payment is made, including where the player can skip into the level
                # out of logic and then pay Moneybags.
                # Moneybags for Glimmer is free, as well as when gemsanity is on and moneybagssanity is not.
                # TODO: Add Dragon Shores theater logic.
                if self.options.moneybags_settings == MoneybagsOptions.VANILLA and self.options.enable_gemsanity.value == GemsanityOptions.OFF:
                    # Total gem checks probably don't make sense under these settings.
                    accessible_gems -= 4000
            return accessible_gems >= max_gems

        def has_sparx_health(self, health, state):
            if self.options.enable_progressive_sparx_health.value in [SparxUpgradeOptions.OFF, SparxUpgradeOptions.TRUE_SPARXLESS]:
                return True
            max_health = 0
            if self.options.enable_progressive_sparx_health.value == SparxUpgradeOptions.BLUE:
                max_health = 2
            elif self.options.enable_progressive_sparx_health.value == SparxUpgradeOptions.GREEN:
                max_health = 1
            max_health += state.count("Progressive Sparx Health Upgrade", self.player)
            return max_health >= health

        def set_indirect_rule(self, regionName, rule):
            region = self.multiworld.get_region(regionName, self.player)
            entrance = self.multiworld.get_entrance(regionName, self.player)
            set_rule(entrance, rule)
            self.multiworld.register_indirect_condition(region, entrance)
         
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                    set_rule(location, lambda state: True)

        if self.options.goal.value == GoalOptions.RIPTO:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Ripto", state) and state.has("Orb", self.player, self.options.ripto_door_orbs.value)
        elif self.options.goal.value == GoalOptions.SIXTY_FOUR_ORB:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Ripto", state) and state.has("Orb", self.player, 64)
        elif self.options.goal.value == GoalOptions.HUNDRED_PERCENT and not self.options.enable_open_world.value:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Ripto", state) and state.has("Summer Forest Talisman", self.player, 6) and state.has("Autumn Plains Talisman", self.player, 8) and state.has("Orb", self.player, 64) and has_total_accessible_gems(self, state, 10000)
        elif self.options.goal.value == GoalOptions.HUNDRED_PERCENT and self.options.enable_open_world.value:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Ripto", state) and state.has("Orb", self.player, 64) and has_total_accessible_gems(self, state, 10000)
        elif self.options.goal.value == GoalOptions.TEN_TOKENS:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Dragon Shores Token", self.player, 10) and state.has("Orb", self.player, 55) and has_total_accessible_gems(self, state, 8000)
        elif self.options.goal.value == GoalOptions.ALL_SKILLPOINTS:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Skill Point", self.player, 16)
        elif self.options.goal.value == GoalOptions.EPILOGUE:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Ripto", state) and state.has("Skill Point", self.player, 16)

        # Summer Forest Rules
        set_rule(
            self.multiworld.get_location("Summer Forest: On a secret ledge", self.player),
            lambda state: can_swim(self, state)
        )
        set_rule(
            self.multiworld.get_location("Summer Forest: Atop a ladder", self.player),
            lambda state: can_reach_summer_second_half(self, state) and can_climb(self, state)
        )
        set_rule(
            self.multiworld.get_location("Summer Forest: Behind the door", self.player),
            lambda state: can_reach_summer_second_half(self, state)
        )
        if Spyro2LocationCategory.MONEYBAGS in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Summer Forest: Moneybags Unlock: Door to Aquaria Towers", self.player),
                lambda state: can_reach_summer_second_half(self, state)
            )
        if Spyro2LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Summer Forest: Life Bottle Near Sunny Beach", self.player),
                lambda state: can_reach_summer_second_half(self, state)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            swim_gems = [1, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 49, 50, 51, 52, 53, 54, 68, 69, 74, 77, 78, 79, 80, 87, 88, 89, 90, 91, 92, 93, 116, 117, 118, 119, 120, 121, 138, 144, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158]
            climb_gems = [83, 84, 85, 86, 94, 102, 103, 104, 105, 106]
            aquaria_gems = [2, 3, 4, 5, 13, 21, 101, 107]
            empty_bits = [27, 39, 41, 42, 43, 44, 45, 46, 47, 61, 62, 72, 73, 81, 82, 95, 96, 97, 98, 99, 100, 108, 126, 127, 128]
            for gem in swim_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Summer Forest: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Summer Forest: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_swim(self, state)
                    )
            for gem in climb_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Summer Forest: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Summer Forest: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_reach_summer_second_half(self, state) and can_climb(self, state)
                    )
            for gem in aquaria_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Summer Forest: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Summer Forest: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_reach_summer_second_half(self, state) and (state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state))
                    )

        # Glimmer Rules
        set_rule(
            self.multiworld.get_location("Glimmer: Gem Lamp Flight in cave", self.player),
            lambda state: can_climb(self, state)
        )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            climb_gems = [110, 111, 112, 113, 114, 115, 117, 118, 119, 151]
            empty_bits = [1, 2, 3, 4, 5, 6, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 152]
            for gem in climb_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Glimmer: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Glimmer: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_climb(self, state)
                    )

        # Idol Springs Rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(self, "Idol Springs", lambda state: state.has("Idol Springs Unlock", self.player))
        set_rule(
            self.multiworld.get_location("Idol Springs: Foreman Bud's puzzles", self.player),
            lambda state: can_swim(self, state)
        )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            swim_gems = [16, 17, 18, 19, 20, 21, 61, 64, 65, 66, 67, 76, 85, 86, 93, 94, 95, 96, 99, 100, 101, 102, 103, 104, 105, 106]
            empty_bits = [63, 88, 90, 122, 127, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145]
            for gem in swim_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Idol Springs: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Idol Springs: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_swim(self, state)
                    )

        # Colossus Rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(self, "Colossus", lambda state: state.has("Colossus Unlock", self.player))

        # Hurricos Rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(self, "Hurricos", lambda state: can_reach_summer_second_half(self, state) and state.has("Hurricos Unlock", self.player))
        else:
            set_indirect_rule(self, "Hurricos", lambda state: can_reach_summer_second_half(self, state))

        # Aquaria Towers Rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Aquaria Towers",
                    lambda state: state.has("Aquaria Towers Unlock", self.player) and can_reach_summer_second_half(self, state) and (state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state)) and has_sparx_health(self, 1, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Aquaria Towers",
                    lambda state: state.has("Aquaria Towers Unlock", self.player) and can_reach_summer_second_half(self, state) and (state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state))
                )
        else:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Aquaria Towers",
                    lambda state: can_reach_summer_second_half(self, state) and (state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state)) and has_sparx_health(self, 1, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Aquaria Towers",
                    lambda state: can_reach_summer_second_half(self, state) and (state.has("Moneybags Unlock - Door to Aquaria Towers", self.player) or is_boss_defeated(self, "Ripto", state))
                )
        set_rule(
            self.multiworld.get_location("Aquaria Towers: Talisman", self.player),
            lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        set_rule(
            self.multiworld.get_location("Aquaria Towers: Seahorse Rescue", self.player),
            lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        set_rule(
            self.multiworld.get_location("Aquaria Towers: Manta ride I", self.player),
            lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        set_rule(
            self.multiworld.get_location("Aquaria Towers: Manta ride II", self.player),
            lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        if Spyro2LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Aquaria Towers: All Seaweed (Skill Point)", self.player),
                lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        if Spyro2LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Aquaria Towers: All Seaweed (Goal)", self.player),
                lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        if Spyro2LocationCategory.SPIRIT_PARTICLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Aquaria Towers: All Spirit Particles", self.player),
                lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            sub_gems = [3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 93, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134]
            empty_bits = [85, 86, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 109, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 167]
            for gem in sub_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Aquaria Towers: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Aquaria Towers: Gem {gem - skipped_bits}", self.player),
                        lambda state: state.has("Moneybags Unlock - Aquaria Towers Submarine", self.player) or is_boss_defeated(self, "Ripto", state)
                    )

        # Sunny Beach rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(self, "Sunny Beach", lambda state: state.has("Sunny Beach Unlock", self.player) and can_reach_summer_second_half(self, state))
        else:
            set_indirect_rule(self, "Sunny Beach", lambda state: can_reach_summer_second_half(self, state))
        set_rule(
            self.multiworld.get_location("Sunny Beach: Turtle soup I", self.player),
            lambda state: can_climb(self, state)
        )
        set_rule(
            self.multiworld.get_location("Sunny Beach: Turtle soup II", self.player),
            lambda state: can_climb(self, state)
        )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            climb_gems = [56, 57, 58, 83, 84, 85, 86, 87, 108]
            empty_bits = [1, 2, 3, 4, 5, 6, 53, 91, 105, 106, 107, 109]
            for gem in climb_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Sunny Beach: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Sunny Beach: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_climb(self, state)
                    )

        # Ocean Speedway rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Ocean Speedway",
                lambda state: state.has("Ocean Speedway Unlock", self.player) and can_reach_summer_second_half(self, state) and state.has("Orb", self.player, 3)
            )
        else:
            set_indirect_rule(
                self,
                "Ocean Speedway",
                lambda state: can_reach_summer_second_half(self, state) and state.has("Orb", self.player, 3)
            )

        # Crush's Dungeon rules
        # TODO: It is likely that the client implementation will make swim not required because Elora will warp
        #  the player. But this complicates the logic significantly.
        if self.options.enable_open_world:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Crush's Dungeon",
                    lambda state: can_reach_summer_second_half(self, state) and has_sparx_health(self, 1, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Crush's Dungeon",
                    lambda state: can_reach_summer_second_half(self, state)
                )
        else:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Crush's Dungeon",
                    lambda state: can_reach_summer_second_half(self, state) and state.has("Summer Forest Talisman", self.player, 6) and has_sparx_health(self, 1, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Crush's Dungeon",
                    lambda state: can_reach_summer_second_half(self, state) and state.has("Summer Forest Talisman", self.player, 6)
                )

        # Autumn Plains Rules
        if not (self.options.enable_open_world and self.options.open_world_ability_and_warp_unlocks):
            set_indirect_rule(self, "Autumn Plains", lambda state: is_boss_defeated(self, "Crush", state))
        set_rule(
            self.multiworld.get_location("Autumn Plains: The end of the wall", self.player),
            lambda state: can_reach_metro(self, state) or can_pass_autumn_door(self, state)
        )
        set_rule(
            self.multiworld.get_location("Autumn Plains: Long glide!", self.player),
            lambda state: can_pass_autumn_door(self, state)
        )
        if Spyro2LocationCategory.MONEYBAGS in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Autumn Plains: Moneybags Unlock: Shady Oasis Portal", self.player),
                lambda state: can_pass_autumn_door(self, state)
            )
        if Spyro2LocationCategory.MONEYBAGS in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Autumn Plains: Moneybags Unlock: Icy Speedway Portal", self.player),
                lambda state: can_pass_autumn_door(self, state)
            )
        if Spyro2LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Autumn Plains: Life Bottle", self.player),
                lambda state: can_reach_autumn_second_half(self, state)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            whirlwind_gems = [31, 32, 89, 90]
            climb_gems = [17, 18, 19, 20, 21, 35, 36, 37, 46, 47, 93, 94]
            door_gems = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 99, 100, 101, 122]
            shady_gems = [75, 76, 77]
            empty_bits = [1, 2, 3, 4, 5, 6, 102, 103, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133]
            for gem in whirlwind_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Autumn Plains: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Autumn Plains: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_reach_metro(self, state)
                    )
            for gem in climb_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Autumn Plains: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Autumn Plains: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_reach_autumn_second_half(self, state)
                    )
            for gem in door_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Autumn Plains: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Autumn Plains: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_pass_autumn_door(self, state)
                    )
            for gem in shady_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Autumn Plains: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Autumn Plains: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_pass_autumn_door(self, state) and (state.has("Moneybags Unlock - Shady Oasis Portal", self.player) or is_boss_defeated(self, "Ripto", state))
                    )

        # Skelos Badlands rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Skelos Badlands",
                    lambda state: state.has("Skelos Badlands Unlock", self.player) and has_sparx_health(self, 2, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Skelos Badlands",
                    lambda state: state.has("Skelos Badlands Unlock", self.player)
                )
        else:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Skelos Badlands",
                    lambda state: has_sparx_health(self, 2, state)
                )

        # Crystal Glacier rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Crystal Glacier",
                lambda state: state.has("Crystal Glacier Unlock", self.player)
            )
        set_rule(
            self.multiworld.get_location("Crystal Glacier: Talisman", self.player),
            lambda state: state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        set_rule(
            self.multiworld.get_location("Crystal Glacier: Draclet cave", self.player),
            lambda state: state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        set_rule(
            self.multiworld.get_location("Crystal Glacier: George the snow leopard", self.player),
            lambda state: state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        if Spyro2LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Crystal Glacier: Life Bottle", self.player),
                lambda state: state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        if Spyro2LocationCategory.SPIRIT_PARTICLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Crystal Glacier: All Spirit Particles", self.player),
                lambda state: state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            bridge_gems = [23, 24, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]
            empty_bits = [1, 2, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
            for gem in bridge_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Crystal Glacier: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Crystal Glacier: Gem {gem - skipped_bits}", self.player),
                        lambda state: state.has("Moneybags Unlock - Crystal Glacier Bridge", self.player) or is_boss_defeated(self, "Ripto", state)
                    )

        # Breeze Harbor rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Breeze Harbor",
                lambda state: state.has("Breeze Harbor Unlock", self.player)
            )

        # Zephyr rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Zephyr",
                lambda state: state.has("Zephyr Unlock", self.player) and (state.has("Moneybags Unlock - Zephyr Portal", self.player) or is_boss_defeated(self, "Ripto", state))
            )
        else:
            set_indirect_rule(
                self,
                "Zephyr",
                lambda state: state.has("Moneybags Unlock - Zephyr Portal", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        set_rule(
            self.multiworld.get_location("Zephyr: Cowlek corral II", self.player),
            lambda state: can_climb(self, state)
        )
        if Spyro2LocationCategory.SPIRIT_PARTICLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Zephyr: All Spirit Particles", self.player),
                lambda state: can_climb(self, state)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            climb_gems = [90, 91, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180]
            empty_bits = [1, 2, 8, 9, 10, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 105, 107, 117, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 149, 150, 151, 153, 167, 168]
            for gem in climb_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Zephyr: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Zephyr: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_climb(self, state)
                    )

        # Metro Speedway rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Metro Speedway",
                lambda state: state.has("Metro Speedway Unlock", self.player) and can_reach_metro(self, state)
            )
        else:
            set_indirect_rule(
                self,
                "Metro Speedway",
                lambda state: can_reach_metro(self, state)
            )

        # Scorch rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Scorch",
                lambda state: state.has("Scorch Unlock", self.player) and can_reach_autumn_second_half(self, state)
            )
        else:
            set_indirect_rule(
                self,
                "Scorch",
                lambda state: can_reach_autumn_second_half(self, state)
            )

        # Shady Oasis rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Shady Oasis",
                lambda state: state.has("Shady Oasis Unlock", self.player) and can_pass_autumn_door(self, state) and (state.has("Moneybags Unlock - Shady Oasis Portal", self.player) or is_boss_defeated(self, "Ripto", state))
            )
        else:
            set_indirect_rule(
                self,
                "Shady Oasis",
                lambda state: can_pass_autumn_door(self, state) and (state.has("Moneybags Unlock - Shady Oasis Portal", self.player) or is_boss_defeated(self, "Ripto", state))
            )
        set_rule(
            self.multiworld.get_location("Shady Oasis: Free Hippos", self.player),
            lambda state: can_headbash(self, state)
        )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            headbash_gems = [144, 145, 146, 147]
            empty_bits = [1, 2, 3, 4, 5, 6, 7, 28, 29, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 138, 140, 141, 142, 143, 148, 155, 168, 169]
            for gem in headbash_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Shady Oasis: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Shady Oasis: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_headbash(self, state)
                    )

        # Magma Cone rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Magma Cone",
                lambda state: state.has("Magma Cone Unlock", self.player) and can_pass_autumn_door(self, state)
            )
        else:
            set_indirect_rule(
                self,
                "Magma Cone",
                lambda state: can_pass_autumn_door(self, state)
            )
        set_rule(
            self.multiworld.get_location("Magma Cone: Talisman", self.player),
            lambda state: state.has("Moneybags Unlock - Magma Cone Elevator", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        set_rule(
            self.multiworld.get_location("Magma Cone: Party crashers", self.player),
            lambda state: state.has("Moneybags Unlock - Magma Cone Elevator", self.player) or is_boss_defeated(self, "Ripto", state)
        )
        if Spyro2LocationCategory.SPIRIT_PARTICLE in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Magma Cone: All Spirit Particles", self.player),
                lambda state: state.has("Moneybags Unlock - Magma Cone Elevator", self.player) or is_boss_defeated(self, "Ripto", state)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            elevator_gems = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 92, 93, 94, 95, 96, 97, 98, 99, 100, 114, 115, 116, 117, 118, 119, 120, 124, 125, 126]
            empty_bits = [1, 2, 48, 78, 121, 122, 123]
            for gem in elevator_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Magma Cone: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Magma Cone: Gem {gem - skipped_bits}", self.player),
                        lambda state: state.has("Moneybags Unlock - Magma Cone Elevator", self.player) or is_boss_defeated(self, "Ripto", state)
                    )

        # Fracture Hills rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Fracture Hills",
                lambda state: state.has("Fracture Hills Unlock", self.player) and can_reach_autumn_second_half(self, state)
            )
        else:
            set_indirect_rule(
                self,
                "Fracture Hills",
                lambda state: can_reach_autumn_second_half(self, state)
            )
        set_rule(
            self.multiworld.get_location("Fracture Hills: Earthshaper bash", self.player),
            lambda state: can_headbash(self, state)
        )
        if Spyro2LocationCategory.SPIRIT_PARTICLE in self.enabled_location_categories and not self.options.fracture_easy_earthshapers:
            set_rule(
                self.multiworld.get_location("Fracture Hills: All Spirit Particles", self.player),
                lambda state: can_headbash(self, state)
            )

        # Icy Speedway rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Icy Speedway",
                lambda state: state.has("Icy Speedway Unlock", self.player) and can_pass_autumn_door(self, state) and (state.has("Moneybags Unlock - Icy Speedway Portal", self.player) or is_boss_defeated(self, "Ripto", state))
            )
        else:
            set_indirect_rule(
                self,
                "Icy Speedway",
                lambda state: can_pass_autumn_door(self, state) and (state.has("Moneybags Unlock - Icy Speedway Portal", self.player) or is_boss_defeated(self, "Ripto", state))
            )

        # Gulp's Overlook rules
        # TODO: The orb and climb requirements are likely not true because of Elora warping the player (or Gulp Skip).
        #  But this complicates logic substantially so ignore it for now.
        if self.options.enable_open_world:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Gulp's Overlook",
                    lambda state: can_pass_autumn_door(self, state) and has_sparx_health(self, 2, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Gulp's Overlook",
                    lambda state: can_pass_autumn_door(self, state)
                )
        else:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(
                    self,
                    "Gulp's Overlook",
                    lambda state: can_pass_autumn_door(self, state) and state.has("Summer Forest Talisman", self.player, 6) and state.has("Autumn Plains Talisman", self.player, 8) and has_sparx_health(self, 2, state)
                )
            else:
                set_indirect_rule(
                    self,
                    "Gulp's Overlook",
                    lambda state: can_pass_autumn_door(self, state) and state.has("Summer Forest Talisman", self.player, 6) and state.has("Autumn Plains Talisman", self.player, 8)
                )

        # Winter Tundra Rules
        if not (self.options.enable_open_world and self.options.open_world_ability_and_warp_unlocks):
            set_indirect_rule(self, "Winter Tundra", lambda state: is_boss_defeated(self, "Gulp", state))
        set_rule(
            self.multiworld.get_location("Winter Tundra: On the tall wall", self.player),
            lambda state: can_reach_winter_second_half(self, state)
        )
        set_rule(
            self.multiworld.get_location("Winter Tundra: Top of the waterfall", self.player),
            lambda state: can_reach_winter_second_half(self, state)
        )
        set_rule(
            self.multiworld.get_location("Winter Tundra: Smash the rock", self.player),
            lambda state: can_headbash(self, state)
        )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            headbash_gems = [8, 9, 10, 11, 12, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 68, 69, 70, 71, 72, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106]
            door_gems = [73, 74, 75, 76, 77]
            empty_bits = [1, 2, 3, 4, 5, 6, 7, 13, 14, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143]
            for gem in headbash_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Winter Tundra: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Winter Tundra: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_headbash(self, state)
                    )
            for gem in door_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Winter Tundra: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Winter Tundra: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_reach_winter_second_half(self, state) and state.has("Orb", self.player, self.options.ripto_door_orbs.value)
                    )

        # Mystic Marsh rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Mystic Marsh",
                lambda state: state.has("Mystic Marsh Unlock", self.player)
            )

        # Cloud Temples rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Cloud Temples",
                lambda state: state.has("Cloud Temples Unlock", self.player) and state.has("Orb", self.player, 15)
            )
        else:
            set_indirect_rule(
                self,
                "Cloud Temples",
                lambda state: state.has("Orb", self.player, 15)
            )
        if Spyro2LocationCategory.GEM in self.enabled_location_categories:
            # Bits of the gems, not accounting for empty bits
            headbash_gems = [104, 105, 106, 107, 108]
            empty_bits = [1, 34, 54, 55, 101, 102, 103]
            for gem in headbash_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if len(self.chosen_gem_locations) == 0 or f"Cloud Temples: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Cloud Temples: Gem {gem - skipped_bits}", self.player),
                        lambda state: can_headbash(self, state)
                    )

        # Canyon Speedway rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Canyon Speedway",
                lambda state: state.has("Canyon Speedway Unlock", self.player) and (state.has("Moneybags Unlock - Canyon Speedway Portal", self.player) or is_boss_defeated(self, "Ripto", state))
            )
        else:
            set_indirect_rule(
                self,
                "Canyon Speedway",
                lambda state: state.has("Moneybags Unlock - Canyon Speedway Portal", self.player) or is_boss_defeated(self, "Ripto", state)
            )

        # Robotica Farms rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Robotica Farms",
                lambda state: state.has("Robotica Farms Unlock", self.player) and can_reach_winter_second_half(self, state)
            )
        else:
            set_indirect_rule(
                self,
                "Robotica Farms",
                lambda state: can_reach_winter_second_half(self, state)
            )

        # Metropolis rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(
                self,
                "Metropolis",
                lambda state: state.has("Metropolis Unlock", self.player) and can_reach_winter_second_half(self, state) and state.has("Orb", self.player, 25)
            )
        else:
            set_indirect_rule(
                self,
                "Metropolis",
                lambda state: can_reach_winter_second_half(self, state) and state.has("Orb", self.player, 25)
            )

        # Ripto's Arena rules
        if self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(
                self,
                "Ripto's Arena",
                lambda state: can_reach_winter_second_half(self, state) and state.has("Orb", self.player, self.options.ripto_door_orbs.value) and has_sparx_health(self, 3, state)
            )
        else:
            set_indirect_rule(
                self,
                "Ripto's Arena",
                lambda state: can_reach_winter_second_half(self, state) and state.has("Orb", self.player, self.options.ripto_door_orbs.value)
            )

        # Dragon Shores rules
        if self.options.level_lock_options.value == LevelLockOptions.KEYS:
            set_indirect_rule(self, "Dragon Shores", lambda state: state.has("Dragon Shores Unlock", self.player) and is_boss_defeated(self, "Ripto", state))
        else:
            set_indirect_rule(self, "Dragon Shores", lambda state: is_boss_defeated(self, "Ripto", state))
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Tunnel o' Love", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Shooting Gallery I", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Shooting Gallery II", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Shooting Gallery III", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Rollercoaster I", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Rollercoaster II", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Rollercoaster III", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Dunk Tank I", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Dunk Tank II", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )
        if Spyro2LocationCategory.SHORES_TOKEN in self.enabled_location_categories:
            set_rule(
                self.multiworld.get_location("Dragon Shores: Dunk Tank III", self.player),
                lambda state: has_total_accessible_gems(self, state, 8000) and state.has("Orb", self.player, 55)
            )

        # Level Gem Count rules
        for level in self.all_levels:
            if level in ["Crush's Dungeon", "Gulp's Overlook", "Dragon Shores", "Ripto's Arena"]:
                continue
            if Spyro2LocationCategory.GEM_25 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: 25% Gems", self.player),
                    lambda state, level=level: get_gems_accessible_in_level(self, level, state) >= 100
                )
            if Spyro2LocationCategory.GEM_50 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: 50% Gems", self.player),
                    lambda state, level=level: get_gems_accessible_in_level(self, level, state) >= 200
                )
            if Spyro2LocationCategory.GEM_75 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: 75% Gems", self.player),
                    lambda state, level=level: get_gems_accessible_in_level(self, level, state) >= 300
                )
            if Spyro2LocationCategory.GEM_100 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: All Gems", self.player),
                    lambda state, level=level: get_gems_accessible_in_level(self, level, state) >= 400
                )

        # Inventory rules
        if Spyro2LocationCategory.TOTAL_GEM in self.enabled_location_categories:
            for i in range(20):
                gems = 500 * (i + 1)
                if gems <= self.options.max_total_gem_checks.value:
                    set_rule(
                        self.multiworld.get_location(f"Total Gems: {gems}", self.player),
                        lambda state, gems=gems: has_total_accessible_gems(self, state, gems)
                    )
                else:
                    break

    # Universal Tracker Support
    def interpret_slot_data(self, slot_data):
        return slot_data

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_s2_code = {item.name: item.s2_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        
        for location in self.multiworld.get_filled_locations():


            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_s2_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].s2_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_s2_code[location.item.name])
                else:
                    locations_target.append(0)

        gemsanity_locations = []
        for loc in self.chosen_gem_locations:
            loc_id = self.location_name_to_id[loc]
            gemsanity_locations.append(loc_id)

        colors = [
            [0x00000040, 0x002000ff],  # Red
            [0x00104808, 0x0020ff00],  # Green
            [0x00480020, 0x00ff0080],  # Blue/Purple
            [0x00005066, 0x0000c0ff],  # Gold
            [0x00240034, 0x008000c0],  # Magenta
        ]
        if self.options.gem_color.value == RandomizeGemColorOptions.SHUFFLE:
            self.random.shuffle(colors)
        elif self.options.gem_color.value == RandomizeGemColorOptions.RANDOM:
            colors = colors + [
                [0x00003848, 0x002060ff],  # Orange
                [0x00482400, 0x00ff9000],  # Cyan
                [0x00160826, 0x00642288],  # Violet
                [0x00801490, 0x004314ff],  # Hot Pink
                [0x00202626, 0x00c0c0c0],  # Silver
                [0x000a2026, 0x0000d7ff],  # Gold
                [0x0000a050, 0x0000fc7c],  # Neon Green
                [0x00808000, 0x00808000],  # Teal
            ]
            self.random.shuffle(colors)
        elif self.options.gem_color.value == RandomizeGemColorOptions.TRUE_RANDOM:
            colors = [
                [self.random.randint(0, 16777216), self.random.randint(0, 16777216)],
                [self.random.randint(0, 16777216), self.random.randint(0, 16777216)],
                [self.random.randint(0, 16777216), self.random.randint(0, 16777216)],
                [self.random.randint(0, 16777216), self.random.randint(0, 16777216)],
                [self.random.randint(0, 16777216), self.random.randint(0, 16777216)],
            ]

        slot_data = {
            "options": {
                "goal": self.options.goal.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "ripto_door_orbs": self.options.ripto_door_orbs.value,
                "enable_open_world": self.options.enable_open_world.value,
                "level_lock_options": self.options.level_lock_options.value,
                "level_unlocks": self.options.level_unlocks.value,
                "open_world_ability_and_warp_unlocks": self.options.open_world_ability_and_warp_unlocks.value,
                "enable_25_pct_gem_checks": self.options.enable_25_pct_gem_checks.value,
                "enable_50_pct_gem_checks": self.options.enable_50_pct_gem_checks.value,
                "enable_75_pct_gem_checks": self.options.enable_75_pct_gem_checks.value,
                "enable_gem_checks": self.options.enable_gem_checks.value,
                "enable_total_gem_checks": self.options.enable_total_gem_checks.value,
                "max_total_gem_checks": self.options.max_total_gem_checks.value,
                "enable_skillpoint_checks": self.options.enable_skillpoint_checks.value,
                "enable_life_bottle_checks": self.options.enable_life_bottle_checks.value,
                "enable_spirit_particle_checks": self.options.enable_spirit_particle_checks.value,
                "enable_gemsanity": self.options.enable_gemsanity.value,
                "moneybags_settings": self.options.moneybags_settings.value,
                "death_link": self.options.death_link.value,
                "enable_filler_extra_lives": self.options.enable_filler_extra_lives.value,
                "enable_destructive_spyro_filler": self.options.enable_destructive_spyro_filler.value,
                "enable_filler_color_change": self.options.enable_filler_color_change.value,
                "enable_filler_big_head_mode": self.options.enable_filler_big_head_mode.value,
                "enable_filler_heal_sparx": self.options.enable_filler_heal_sparx.value,
                "trap_filler_percent": self.options.trap_filler_percent.value,
                "enable_trap_damage_sparx": self.options.enable_trap_damage_sparx.value,
                "enable_trap_sparxless": self.options.enable_trap_sparxless.value,
                "enable_trap_invisibility": self.options.enable_trap_invisibility.value,
                "enable_progressive_sparx_health": self.options.enable_progressive_sparx_health.value,
                "enable_progressive_sparx_logic": self.options.enable_progressive_sparx_logic.value,
                "double_jump_ability": self.options.double_jump_ability.value,
                "permanent_fireball_ability": self.options.permanent_fireball_ability.value,
                "colossus_starting_goals": self.options.colossus_starting_goals.value,
                "idol_easy_fish": self.options.idol_easy_fish.value,
                "hurricos_easy_lightning_orbs": self.options.hurricos_easy_lightning_orbs.value,
                "breeze_required_gears": self.options.breeze_required_gears.value,
                "scorch_bombo_settings": self.options.scorch_bombo_settings.value,
                "fracture_require_headbash": self.options.fracture_require_headbash.value,
                "fracture_easy_earthshapers": self.options.fracture_easy_earthshapers.value,
                "magma_spyro_starting_popcorn": self.options.magma_spyro_starting_popcorn.value,
                "magma_hunter_starting_popcorn": self.options.magma_hunter_starting_popcorn.value,
                "shady_require_headbash": self.options.shady_require_headbash.value,
                "easy_gulp": self.options.easy_gulp.value,
                "portal_gem_collection_color": self.options.portal_gem_collection_color.value,
                "gem_color": self.options.gem_color.value,
                "red_gem_shadow_color": colors[0][0],
                "red_gem_color": colors[0][1],
                "green_gem_shadow_color": colors[1][0],
                "green_gem_color": colors[1][1],
                "blue_gem_shadow_color": colors[2][0],
                "blue_gem_color": colors[2][1],
                "gold_gem_shadow_color": colors[3][0],
                "gold_gem_color": colors[3][1],
                "pink_gem_shadow_color": colors[4][0],
                "pink_gem_color": colors[4][1],
            },
            "gemsanity_ids": gemsanity_locations,
            # "moneybags_prices": moneybags_prices,
            "level_orb_requirements": self.level_orb_requirements,
            "key_locked_levels": self.key_locked_levels,
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address,
            "apworldVersion": self.ap_world_version,
        }

        return slot_data
