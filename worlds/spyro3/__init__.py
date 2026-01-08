# world/spyro3/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule, forbid_item

from .Items import Spyro3Item, Spyro3ItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import Spyro3Location, Spyro3LocationCategory, location_tables, location_dictionary, hint_locations
from .Options import Spyro3Option, GoalOptions, LifeBottleOptions, MoneybagsOptions, SparxUpgradeOptions, GemsanityOptions, spyro_options_groups
from .Hints import generateHints

class Spyro3Web(WebWorld):
    bug_report_page = ""
    theme = "stone"
    option_groups = spyro_options_groups
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Spyro 3 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin", "Uroogla"]
    )
    game_info_languages = ["en"]
    tutorials = [setup_en]


class Spyro3World(World):
    """
    Spyro 3 is a game about a purple dragon who likes eggs.
    """

    game: str = "Spyro 3"
    options_dataclass = Spyro3Option
    options: Spyro3Option
    topology_present: bool = False  # Turn on when entrance randomizer is available.
    web = Spyro3Web()
    data_version = 0
    base_id = 1230000
    enabled_location_categories: Set[Spyro3LocationCategory]
    enabled_hint_locations = []
    required_client_version = (0, 5, 0)
    item_name_to_id = Spyro3Item.get_name_to_id()
    location_name_to_id = Spyro3Location.get_name_to_id()
    item_name_groups = {}
    item_descriptions = item_descriptions

    all_levels = [
        "Sunrise Spring","Sunny Villa","Cloud Spires","Molten Crater","Seashell Shore","Mushroom Speedway","Sheila's Alp", "Buzz", "Crawdad Farm",
        "Midday Gardens","Icy Peak","Enchanted Towers","Spooky Swamp","Bamboo Terrace","Country Speedway","Sgt. Byrd's Base","Spike","Spider Town",
        "Evening Lake","Frozen Altars","Lost Fleet","Fireworks Factory","Charmed Ridge","Honey Speedway","Bentley's Outpost","Scorch","Starfish Reef",
        "Midnight Mountain","Crystal Islands","Desert Ruins","Haunted Tomb","Dino Mines","Harbor Speedway","Agent 9's Lab","Sorceress","Bugbot Factory","Super Bonus Round"
    ]


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()

    def generate_early(self):
        self.enabled_location_categories.add(Spyro3LocationCategory.EGG)
        self.enabled_location_categories.add(Spyro3LocationCategory.EVENT)
        if self.options.zoe_gives_hints.value != 0:
            self.enabled_location_categories.add(Spyro3LocationCategory.HINT)
            # Randomly select which Zoes give hints.
            self.enabled_hint_locations = self.multiworld.random.sample(hint_locations, self.options.zoe_gives_hints.value)
        if self.options.goal.value in [GoalOptions.ALL_SKILLPOINTS, GoalOptions.EPILOGUE]:
            self.enabled_location_categories.add(Spyro3LocationCategory.SKILLPOINT_GOAL)
        if self.options.enable_25_pct_gem_checks.value:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM_25)
        if self.options.enable_50_pct_gem_checks.value:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM_50)
        if self.options.enable_75_pct_gem_checks.value:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM_75)
        if self.options.enable_gem_checks.value:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM)
        if self.options.enable_total_gem_checks.value:
            self.enabled_location_categories.add(Spyro3LocationCategory.TOTAL_GEM)
        #if self.options.enable_gemsanity_checks.value == GemsanityOptions.PINK_GEMS:
        #    self.enabled_location_categories.add(Spyro3LocationCategory.PINK_GEMS)
        if self.options.enable_skillpoint_checks.value:
            self.enabled_location_categories.add(Spyro3LocationCategory.SKILLPOINT)
        if self.options.enable_life_bottle_checks.value != LifeBottleOptions.OFF:
            self.enabled_location_categories.add(Spyro3LocationCategory.LIFE_BOTTLE)
        if self.options.enable_life_bottle_checks.value == LifeBottleOptions.HARD:
            self.enabled_location_categories.add(Spyro3LocationCategory.LIFE_BOTTLE_HARD)

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
            #print(f"Connecting {from_region} to {to_region} Using entrance: " + connection.name)
            
        create_connection("Menu", "Sunrise Spring")
        create_connection("Menu", "Inventory")
                
        create_connection("Sunrise Spring", "Sunny Villa")
        create_connection("Sunrise Spring", "Cloud Spires")
        create_connection("Sunrise Spring", "Molten Crater")
        create_connection("Sunrise Spring", "Seashell Shore")
        create_connection("Sunrise Spring", "Mushroom Speedway")
        create_connection("Sunrise Spring", "Sheila's Alp")
             
        create_connection("Sunrise Spring", "Buzz")
        create_connection("Sunrise Spring", "Crawdad Farm")
        create_connection("Sunrise Spring", "Midday Gardens")
        
        create_connection("Midday Gardens", "Icy Peak")
        create_connection("Midday Gardens", "Enchanted Towers")
        create_connection("Midday Gardens", "Spooky Swamp")
        create_connection("Midday Gardens", "Bamboo Terrace")
        create_connection("Midday Gardens", "Country Speedway")
        create_connection("Midday Gardens", "Sgt. Byrd's Base")

        create_connection("Midday Gardens", "Spike")
        create_connection("Midday Gardens", "Spider Town")
        create_connection("Midday Gardens", "Evening Lake")
        
        create_connection("Evening Lake", "Frozen Altars")
        create_connection("Evening Lake", "Lost Fleet")
        create_connection("Evening Lake", "Fireworks Factory")
        create_connection("Evening Lake", "Charmed Ridge")
        create_connection("Evening Lake", "Honey Speedway")
        create_connection("Evening Lake", "Bentley's Outpost")

        create_connection("Evening Lake", "Scorch")
        create_connection("Evening Lake", "Starfish Reef")        
        create_connection("Evening Lake", "Midnight Mountain")   
        
        create_connection("Midnight Mountain", "Crystal Islands")
        create_connection("Midnight Mountain", "Desert Ruins")
        create_connection("Midnight Mountain", "Haunted Tomb")
        create_connection("Midnight Mountain", "Dino Mines")
        create_connection("Midnight Mountain", "Harbor Speedway")
        create_connection("Midnight Mountain", "Agent 9's Lab")

        create_connection("Midnight Mountain", "Sorceress")
        create_connection("Midnight Mountain", "Bugbot Factory")
        create_connection("Midnight Mountain", "Super Bonus Round")
        
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        #print("location table size: " + str(len(location_table)))
        for location in location_table:
            #print("Creating location: " + location.name)
            if location.category in self.enabled_location_categories and location.category not in [Spyro3LocationCategory.EVENT, Spyro3LocationCategory.HINT, Spyro3LocationCategory.TOTAL_GEM]:
                #print("Adding location: " + location.name + " with default item " + location.default_item)
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and location.category == Spyro3LocationCategory.TOTAL_GEM:
                gems_needed = int(location.name.split("Total Gems: ")[1])
                if gems_needed <= self.options.max_total_gem_checks.value:
                    new_location = Spyro3Location(
                        self.player,
                        location.name,
                        location.category,
                        location.default_item,
                        self.location_name_to_id[location.name],
                        new_region
                    )
                    new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and location.category == Spyro3LocationCategory.HINT and location.name in self.enabled_hint_locations:
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category == Spyro3LocationCategory.EVENT:
                # Remove non-randomized progression items as checks because of the use of a "filler" fake item.
                # Replace events with event items for spoiler log readability.
                event_item = self.create_item(location.default_item)
                #if event_item.classification != ItemClassification.progression:
                #    continue
                #print("Adding Location: " + location.name + " as an event with default item " + location.default_item)
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                #print("Placing event: " + event_item.name + " in location: " + location.name)
                new_region.locations.append(new_location)

        #print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        #print("adding region: " + region_name)
        return new_region


    def create_items(self):
        itempool: List[Spyro3Item] = []
        itempoolSize = 0
        placedEggs = 0
        remainingHints = []
        for i in range(self.options.zoe_gives_hints.value):
            remainingHints.append(f"Hint {i + 1}")
        #print("Creating items")
        for location in self.multiworld.get_locations(self.player):
                #print("found item in category: " + str(location.category))
                item_data = item_dictionary[location.default_item_name]
                # There is a bug with the current client implementation where another player auto-collecting an item on the
                # goal condition results in the client thinking the player has completed the goal.
                # To avoid this, ensure the goal item is always vanilla.  Manually placed items exist outside the item pool.
                # TODO: Remove this restriction after implementing a better client solution.
                if item_data.category == Spyro3ItemCategory.HINT:
                    if len(remainingHints) == 0:
                        raise Exception('Ran out of hints to place.')
                    hint = self.multiworld.random.choice(remainingHints)
                    remainingHints.remove(hint)
                    item = self.create_item(hint)
                    self.multiworld.get_location(location.name, self.player).place_locked_item(item)
                elif item_data.category in [Spyro3ItemCategory.SKIP] or \
                        location.category in [Spyro3LocationCategory.EVENT] or \
                        (self.options.goal.value in [GoalOptions.ALL_SKILLPOINTS, GoalOptions.EPILOGUE] and location.category == Spyro3LocationCategory.SKILLPOINT_GOAL) or \
                        (self.options.goal.value in [GoalOptions.SORCERESS_ONE, GoalOptions.EPILOGUE] and location.name == "Sorceress's Lair: Defeat the Sorceress? (George)") or \
                        (self.options.goal.value == GoalOptions.EGG_FOR_SALE and location.name == "Midnight Mountain Home: Egg for sale. (Al)") or \
                        (self.options.goal.value == GoalOptions.SORCERESS_TWO and location.name == "Super Bonus Round: Woo, a secret egg. (Yin Yang)"):
                    #print(f"Adding vanilla item/event {location.default_item_name} to {location.name}")
                    item = self.create_item(location.default_item_name)
                    self.multiworld.get_location(location.name, self.player).place_locked_item(item)
                    if location.default_item_name == 'Egg':
                        placedEggs = placedEggs + 1
                elif location.category in self.enabled_location_categories:
                    #print("Adding item: " + location.default_item_name)
                    itempoolSize += 1
                    #itempool.append(self.create_item(location.default_item_name))
        
        #print("Requesting itempool size: " + str(itempoolSize))
        foo = BuildItemPool(self.multiworld, itempoolSize, placedEggs, self.options)
        #print("Created item pool size: " + str(len(foo)))
        #for item in foo:
            #print(f"{item.name}")

        for item in foo:
            #print("Adding regular item: " + item.name)
            itempool.append(self.create_item(item.name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool
        
        #print("Final Item pool: ")
        #for item in self.multiworld.itempool:
        #    print(item.name)


    def create_item(self, name: str) -> Item:
        useful_categories = [Spyro3ItemCategory.SPARX_POWERUP]
        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category == Spyro3ItemCategory.EGG \
                or item_dictionary[name].category == Spyro3ItemCategory.EVENT \
                or item_dictionary[name].category == Spyro3ItemCategory.MONEYBAGS \
                or item_dictionary[name].category == Spyro3ItemCategory.SKILLPOINT_GOAL \
                or item_dictionary[name].category == Spyro3ItemCategory.WORLD_KEY \
                or self.options.enable_progressive_sparx_logic.value and name == 'Progressive Sparx Health Upgrade':
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories \
                or not self.options.enable_progressive_sparx_logic.value and name == 'Progressive Sparx Health Upgrade':
            item_classification = ItemClassification.useful
        elif item_dictionary[name].category == Spyro3ItemCategory.TRAP:
            item_classification = ItemClassification.trap
        else:
            item_classification = ItemClassification.filler

        return Spyro3Item(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return "Egg"
    
    def set_rules(self) -> None:          
        def is_level_completed(self, level, state):
            return state.has(level + " Complete", self.player)
        
        def is_boss_defeated(self, boss, state):
            return state.has(boss + " Defeated", self.player)

        def is_companion_unlocked(self, companion, state):
            return state.has(f"Moneybags Unlock - {companion}", self.player)

        def has_world_keys(self, key_count, state):
            return state.count("World Key", self.player) >= key_count

        def get_gems_accessible_in_level(self, level, state):
            # TODO: It may be worth splitting this into some sort of standardized Logic framework,
            # especially once Gemsanity is added.  At present, some logic is duplicated between here
            # and location rules, but a framework to avoid this may be overkill.  Determine if it is
            # desirable to build a framework.

            # Older versions of Python do not support switch statements, so use if/elif.
            if level == 'Sunrise Spring':
                return 400
            elif level == 'Sunny Villa':
                # Sheila's area has 89 gems, skateboarding has 92.  All skateboarding gems are available regardless of Hunter's state.
                gems = 311
                if self.options.logic_sunny_sheila_early.value or is_level_completed(self, "Sheila's Alp", state):
                    gems += 89
                return gems
            elif level == 'Cloud Spires':
                # 171 gems are available logically before the Bellows unlock, with an extra 5 being possible in easy mode, since an enemy's gem falls to the start of the level.
                # All gems are available doing the level backwards.
                gems = 171
                if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_cloud_backwards.value or state.has("Moneybags Unlock - Cloud Spires Bellows", self.player):
                    gems += 229
                return gems
            elif level == 'Molten Crater':
                if not self.options.logic_molten_early.value and not state.has("Egg", self.player, 10):
                    return 0
                # 109 gems in the Byrd subarea, 106 in thieves.
                gems = 185
                if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_molten_thieves_no_moneybags.value or state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player):
                    gems += 106
                if is_level_completed(self, "Sgt. Byrd's Base", state) or self.options.logic_molten_byrd_early.value:
                    gems += 109
                return gems
            elif level == 'Seashell Shore':
                if not self.options.logic_seashell_early.value and not state.has("Egg", self.player, 14):
                    return 0
                # 105 gems in the Sheila sub area.
                gems = 295
                if is_level_completed(self, "Sheila's Alp", state):
                    gems += 105
                return gems
            elif level == 'Mushroom Speedway':
                if not self.options.logic_mushroom_early.value and not state.has("Egg", self.player, 20):
                    return 0
                return 400
            elif level == "Sheila's Alp":
                if not self.options.logic_sheila_early.value and self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not state.has("Moneybags Unlock - Sheila", self.player):
                    return 0
                return 400
            elif level == "Crawdad Farm":
                if not is_boss_defeated(self, "Buzz", state):
                    return 0
                return 200
            elif level == 'Midday Gardens':
                if not is_boss_defeated(self, "Buzz", state) or (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                return 400
            elif level == 'Icy Peak':
                if not is_boss_defeated(self, "Buzz", state) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 1, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                return 500
            elif level == 'Enchanted Towers':
                if not is_boss_defeated(self, "Buzz", state) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 1, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                # Most Sgt. Byrd gems can be obtained by Spyro with varying levels of difficulty, but at least 75% of the level's gems are in logic with simple movement.
                # TODO: Determine a better estimate for this.
                gems = 375
                if is_level_completed(self, "Sgt. Byrd's Base", state):
                    gems += 125
                return gems
            elif level == 'Spooky Swamp':
                if not is_boss_defeated(self, "Buzz", state) or (not self.options.logic_spooky_early.value and not state.has('Egg', self.player, 25)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 1, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                # Sheila area has 174 gems but it is not possible to get here without Sheila.
                # Enough gems are locked by Moneybags in vanilla logic to block 50% completion.
                # TODO: Determine a better estimate for this.
                gems = 125
                if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_spooky_no_moneybags.value or state.has("Moneybags Unlock - Spooky Swamp Door", self.player):
                    gems += 375
                return gems
            elif level == 'Bamboo Terrace':
                if not is_boss_defeated(self, "Buzz", state) or (not self.options.logic_bamboo_early.value and not state.has('Egg', self.player, 30)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 1, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                # Bentley's subarea has 189 gems.
                gems = 311
                if is_level_completed(self, "Bentley's Outpost", state) or self.options.logic_bamboo_bentley_early.value:
                    gems += 189
                return gems
            elif level == 'Country Speedway':
                if not is_boss_defeated(self, 'Buzz', state) or (not self.options.logic_country_early.value and not state.has('Egg', self.player, 36)) or (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                return 400
            elif level == "Sgt. Byrd's Base":
                if not is_boss_defeated(self, 'Buzz', state) or \
                        not self.options.logic_byrd_early.value and self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not state.has("Moneybags Unlock - Sgt. Byrd", self.player) or \
                        (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 1, state)) or \
                        (self.options.enable_world_keys.value and not has_world_keys(self, 1, state)):
                    return 0
                return 500
            elif level == 'Spider Town':
                if not is_boss_defeated(self, 'Spike', state):
                    return 0
                return 200
            elif level == 'Evening Lake':
                if not is_boss_defeated(self, 'Spike', state) or (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                return 400
            elif level == 'Frozen Altars':
                if not is_boss_defeated(self, 'Spike', state) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 65) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Bentley', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                return 600
            elif level == 'Lost Fleet':
                if not is_boss_defeated(self, 'Spike', state) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 65) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Bentley', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                # 100 gems in skateboarding area.  Of these, 13 are accessible easily without the skateboard.
                # Roughly 19 require the skateboard, and the rest can be obtained with a medium difficulty jump onto the track, but these are not in logic.
                gems = 513
                if is_boss_defeated(self, 'Scorch', state):
                    gems += 87
                return gems
            elif level == 'Fireworks Factory':
                if not is_boss_defeated(self, "Spike", state) or (not self.options.logic_fireworks_early.value and not state.has('Egg', self.player, 50)) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 65) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Bentley', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)))) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                # 175 gems in the Agent 9 subarea.
                gems = 425
                if is_level_completed(self, "Agent 9's Lab", state) or self.options.logic_fireworks_agent_9_early.value:
                    gems += 175
                return gems
            elif level == 'Charmed Ridge':
                if not is_boss_defeated(self, "Spike", state) or (not self.options.logic_charmed_early.value and not state.has('Egg', self.player, 58)) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 65) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Bentley', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)))) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                # Moneybags blocks 472 gems.
                gems = 128
                if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_charmed_no_moneybags.value or state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player):
                    gems += 472
                return gems
            elif level == 'Honey Speedway':
                if not is_boss_defeated(self, 'Spike', state) or (not self.options.logic_honey_early.value and not state.has('Egg', self.player, 65)) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 65) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Bentley', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                return 400
            elif level == "Bentley's Outpost":
                if not is_boss_defeated(self, 'Spike', state) or \
                        not self.options.logic_bentley_early.value and self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not state.has("Moneybags Unlock - Bentley", self.player) or \
                        (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 65) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 2, state)))) or \
                        (self.options.enable_world_keys.value and not has_world_keys(self, 2, state)):
                    return 0
                return 600
            elif level == 'Starfish Reef':
                if not is_boss_defeated(self, 'Scorch', state):
                    return 0
                return 200
            elif level == 'Midnight Mountain':
                if not is_boss_defeated(self, 'Scorch', state):
                    return 0
                return 400
            elif level == 'Crystal Islands':
                if not is_boss_defeated(self, 'Scorch', state) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 90) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Agent 9', state) and not is_boss_defeated(self, 'Sorceress', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 3, state)):
                    return 0
                # Moneybags locks 475 gems.
                gems = 225
                if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_crystal_no_moneybags.value or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player) or is_boss_defeated(self, 'Sorceress', state):
                    gems += 475
                return gems
            elif level == 'Desert Ruins':
                if not is_boss_defeated(self, 'Scorch', state) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 90) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Agent 9', state) and not is_boss_defeated(self, 'Sorceress', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 3, state)):
                    return 0
                # 252 gems are locked behind Moneybags.
                gems = 448
                if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_desert_no_moneybags.value or state.has("Moneybags Unlock - Desert Ruins Door", self.player) or is_boss_defeated(self, 'Sorceress', state):
                    gems += 252
                return gems
            elif level == 'Haunted Tomb':
                if not is_boss_defeated(self, 'Scorch', state) or not state.has('Egg', self.player, 70) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 90) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Agent 9', state) and not is_boss_defeated(self, 'Sorceress', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 3, state)):
                    return 0
                return 700
            elif level == 'Dino Mines':
                if not is_boss_defeated(self, 'Scorch', state) or not state.has('Egg', self.player, 80) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 90) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Agent 9', state) and not is_boss_defeated(self, 'Sorceress', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)))) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)) or (self.options.enable_world_keys.value and not has_world_keys(self, 3, state)):
                    return 0
                # 108 gems in Agent 9's subarea. This can be entered from out of bounds.
                # TODO: Add trick logic for this.
                gems = 592
                if is_level_completed(self, "Agent 9's Lab", state):
                    gems += 108
                return gems
            elif level == 'Harbor Speedway':
                if not is_boss_defeated(self, 'Scorch', state) or not state.has('Egg', self.player, 90) or (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 90) or (self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not is_companion_unlocked(self, 'Agent 9', state) and not is_boss_defeated(self, 'Sorceress', state)) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)))) or (self.options.enable_world_keys.value and not has_world_keys(self, 3, state)):
                    return 0
                return 400
            elif level == "Agent 9's Lab":
                if not is_boss_defeated(self, 'Scorch', state) or \
                        self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not state.has("Moneybags Unlock - Agent 9", self.player) and not is_boss_defeated(self, 'Sorceress', state) or \
                        (self.options.enable_hwd_randomizer.value and (not state.has('Egg', self.player, 90) or (self.options.enable_progressive_sparx_logic.value and not has_sparx_health(self, 3, state)))) or \
                        (self.options.enable_world_keys.value and not has_world_keys(self, 3, state)):
                    return 0
                return 700
            elif level == 'Bugbot Factory':
                if not is_boss_defeated(self, 'Sorceress', state):
                    return 0
                return 200
            elif level == 'Super Bonus Round':
                if not is_boss_defeated(self, 'Sorceress', state) or not state.has("Egg", self.player, 149) or not has_all_gems(self, state):
                    return 0
                return 5000
            return 0

        def has_total_accessible_gems(self, state, max_gems, include_sbr=True):
            accessible_gems = 0

            for level in self.all_levels:
                if include_sbr or level != 'Super Bonus Round':
                    accessible_gems += get_gems_accessible_in_level(self, level, state)

            if self.options.moneybags_settings != MoneybagsOptions.MONEYBAGSSANITY and not is_boss_defeated(self, "Sorceress", state):
                # Remove gems for possible Moneybags payments.  To avoid a player locking themselves out of progression,
                # we have to assume every possible payment is made, including any where the player can skip into the level
                # out of logic and then pay Moneybags.
                if self.options.enable_hwd_randomizer.value:
                    # Prices are randomized and can require all accessible gems.
                    return False
                if self.options.moneybags_settings != MoneybagsOptions.COMPANIONSANITY:
                    # Sheila
                    accessible_gems -= 300
                    # Sgt. Byrd
                    if is_boss_defeated(self, "Buzz", state):
                        accessible_gems -= 700
                    # Bentley
                    if is_boss_defeated(self, "Spike", state):
                        accessible_gems -= 1000
                    # Agent 9
                    if is_boss_defeated(self, "Scorch", state):
                        accessible_gems -= 1300
                # Cloud Spires and Molten Crater
                accessible_gems -= 500
                if is_boss_defeated(self, "Buzz", state):
                    # Spooky Swamp and Icy Peak
                    accessible_gems -= 1000
                if is_boss_defeated(self, "Spike", state):
                    # Frozen Altars and Charmed Ridge
                    accessible_gems -= 1400
                if is_boss_defeated(self, "Scorch", state):
                    # Crystal Islands and Desert Ruins
                    accessible_gems -= 1800
            return accessible_gems >= max_gems

        def has_all_gems(self, state):
            # Don't include SBR in gem calculations to avoid recursion issues.
            return has_total_accessible_gems(self, state, 15000, include_sbr=False)

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
         
        #print("Setting rules")   
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                    set_rule(location, lambda state: True)
        if self.options.goal.value == GoalOptions.SORCERESS_TWO:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Super Bonus Round Complete", self.player)
        elif self.options.goal.value == GoalOptions.EGG_FOR_SALE:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Moneybags Chase Complete", self.player)
        elif self.options.goal.value == GoalOptions.ALL_SKILLPOINTS:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Skill Point", self.player, 20)
        elif self.options.goal.value == GoalOptions.EPILOGUE:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Sorceress", state) and state.has("Skill Point", self.player, 20)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Sorceress", state) and state.has("Egg", self.player, 100)

        # After completing 3 levels in Evening Lake, the player is unable to complete any Hunter challenges until defeating Scorch.
        # To prevent the player from locking themselves out of progression, these must be logically locked behind Scorch.
        # Note: The egg "Sunrise Spring Home: Learn Gliding (Coltrane)" is not affected by this - Hunter remains in Sunrise Spring home.
        # Most, if not all gems, in skateboarding areas can be collected without the skateboard, but leave out of base logic.

        # Sunrise Spring Rules

        # Sunny Villa Rules
        # Sheila's sub area may be entered early with a spin jump to the peak of the roof of the hut, or from behind.
        if not self.options.logic_sunny_sheila_early.value:
            set_rule(self.multiworld.get_location("Sunny Villa: Hop to Rapunzel. (Lucy)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        # Skateboarding challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Sunny Villa: Lizard skating I. (Emily)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        set_rule(self.multiworld.get_location("Sunny Villa: Lizard skating II. (Daisy)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Sunny Villa: Skateboard course record I (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Sunny Villa: Skateboard course record I (Goal)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Sunny Villa: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Sunny Villa", state) >= 400)

        # Cloud Spires Rules
        # Cloud Spires can be completed backwards, skipping Moneybags payment.
        # This requires one of two jumps to the end of the level, plus a jump from the egg "Cloud Spires: Glide to the island. (Clare)".
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY and not self.options.logic_cloud_backwards.value:
            set_rule(self.multiworld.get_location("Cloud Spires: Turn on the cloud generator. (Henry)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Plant the sun seeds. (LuLu)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Bell tower spirits. (Jake)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Bell tower thief. (Bryan)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Glide to the island. (Clare)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires Complete", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Cloud Spires: Life Bottle Past Whirlwind", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
        if Spyro3LocationCategory.GEM_50 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Cloud Spires: 50% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Cloud Spires", state) >= 200)
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Cloud Spires: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Cloud Spires", state) >= 300)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Cloud Spires: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Cloud Spires", state) >= 400)

        # Molten Crater Rules
        # This requires either a swim in air or getting onto the wall by Molten Crater.
        if not self.options.logic_molten_early.value:
            set_indirect_rule(self, "Molten Crater", lambda state: state.has("Egg", self.player, 10))
        # This is possible jumping on the posts of the nearby bridge, then onto the sub-area hut's roof.
        if not self.options.logic_molten_byrd_early.value:
            set_rule(self.multiworld.get_location("Molten Crater: Replace idol heads. (Ryan)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
            set_rule(self.multiworld.get_location("Molten Crater: Sgt. Byrd blows up a wall. (Luna)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Assemble tiki heads (Skill Point)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Assemble tiki heads (Goal)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY and not self.options.logic_molten_thieves_no_moneybags.value:
            set_rule(self.multiworld.get_location("Molten Crater: Catch the thief. (Moira)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player))
            set_rule(self.multiworld.get_location("Molten Crater: Supercharge after the thief. (Kermitt)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Supercharge the wall (Skill Point)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Supercharge the wall (Goal)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Life Bottle in Breakable Wall in Thief Area", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player))
        if Spyro3LocationCategory.GEM_50 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Molten Crater: 50% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Molten Crater", state) >= 200)
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Molten Crater: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Molten Crater", state) >= 300)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Molten Crater: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Molten Crater", state) >= 400)

        # Seashell Shores Rules
        # This requires a swim in air.
        if not self.options.logic_seashell_early.value:
            set_indirect_rule(self, "Seashell Shore", lambda state: state.has("Egg", self.player, 14))
        # This might be possible with a proxy or similar, but keep the vanilla logic for now.
        set_rule(self.multiworld.get_location("Seashell Shore: Destroy the sand castle. (Mollie)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        set_rule(self.multiworld.get_location("Seashell Shore: Hop to the secret cave. (Jared)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Seashell Shore: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Seashell Shore", state) >= 300)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Seashell Shore: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Seashell Shore", state) >= 400)

        # Mushroom Speedway Rules
        # This requires a swim in air or getting onto the wall by Mushroom and Molten.
        if not self.options.logic_mushroom_early.value:
            set_indirect_rule(self, "Mushroom Speedway", lambda state: state.has("Egg", self.player, 20))
        # Hunter speedway challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Mushroom Speedway: Hunter's dogfight. (Tater)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))

        # Sheila's Alp Rules
        # This requires a swim in air.
        if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not self.options.logic_sheila_early.value:
            set_indirect_rule(self, "Sheila's Alp", lambda state: is_companion_unlocked(self, "Sheila", state))

        # Buzz's Dungeon Rules
        set_indirect_rule(self, "Buzz", lambda state: is_level_completed(self,"Sunny Villa", state) and \
                is_level_completed(self,"Cloud Spires", state) and \
                is_level_completed(self,"Molten Crater", state) and \
                is_level_completed(self,"Seashell Shore", state) and \
                is_level_completed(self,"Sheila's Alp", state))

        # Crawdad Farm Rules
        set_indirect_rule(self, "Crawdad Farm", lambda state: is_boss_defeated(self,"Buzz", state))

        # Midday Gardens Rules
        if self.options.enable_world_keys:
            set_indirect_rule(self, "Midday Gardens", lambda state: is_boss_defeated(self, "Buzz", state) and has_world_keys(self, 1, state))
        else:
            set_indirect_rule(self, "Midday Gardens", lambda state: is_boss_defeated(self,"Buzz", state))

        # Icy Peak Rules
        if self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Icy Peak", lambda state: has_sparx_health(self, 1, state))
        # This can be entered without paying Moneybags, but shooting the crystal you need to jump on with the cannon renders the skip impossible.
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY:
            # No gems in Nancy area.
            set_rule(self.multiworld.get_location("Icy Peak: Protect Nancy the skater. (Cerny)", self.player), lambda state: state.has("Moneybags Unlock - Icy Peak Nancy Door", self.player))

        # Enchanted Towers Rules
        if self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Enchanted Towers", lambda state: has_sparx_health(self, 1, state))
        set_rule(self.multiworld.get_location("Enchanted Towers: Collect the bones. (Ralph)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
        # Skateboarding challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Enchanted Towers: Trick skater I. (Caroline)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        set_rule(self.multiworld.get_location("Enchanted Towers: Trick skater II. (Alex)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Enchanted Towers: Skateboard course record II (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Enchanted Towers: Skateboard course record II (Goal)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Enchanted Towers: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Enchanted Towers", state) >= 500)
        # Note: The life bottle does not require Sgt. Byrd.

        # Spooky Swamp Rules
        # This can be done with a swim in air or a glide out of bounds.
        if self.options.enable_progressive_sparx_logic.value and not self.options.logic_spooky_early.value:
            set_indirect_rule(self, "Spooky Swamp", lambda state: has_sparx_health(self, 1, state) and state.has("Egg", self.player, 25))
        elif not self.options.logic_spooky_early.value:
            set_indirect_rule(self, "Spooky Swamp", lambda state: state.has("Egg", self.player, 25))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Spooky Swamp", lambda state: has_sparx_health(self, 1, state))
        # Can skip Moneybags by damage boosting from the island egg to the end of level.
        if self.options.moneybags_settings.value != MoneybagsOptions.MONEYBAGSSANITY or self.options.logic_spooky_no_moneybags.value:
            # Technically possible without Sheila completion with a glide out of bounds, but there's no reason to add an option for this at this time.
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins II. (Michele)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state) and state.can_reach_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player))
        else:
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player), lambda state: is_level_completed(self, "Sheila's Alp", state) and state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins II. (Michele)", self.player), lambda state: is_level_completed(self, "Sheila's Alp", state) and state.can_reach_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player) and state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            set_rule(self.multiworld.get_location("Spooky Swamp: Defeat sleepy head. (Herbi)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            # This one is doable with a tricky jump from the tea lamp nearest it, but it's easier to just skip Moneybags.
            set_rule(self.multiworld.get_location("Spooky Swamp: Across the treetops. (Frank)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            set_rule(self.multiworld.get_location("Spooky Swamp: Find Shiny the firefly. (Thelonious)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            set_rule(self.multiworld.get_location("Spooky Swamp Complete", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Spooky Swamp: Destroy all piranha signs (Skill Point)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Spooky Swamp: Destroy all piranha signs (Goal)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
        if Spyro3LocationCategory.GEM_50 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Spooky Swamp: 50% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Spooky Swamp", state) >= 250)
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Spooky Swamp: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Spooky Swamp", state) >= 375)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Spooky Swamp: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Spooky Swamp", state) >= 500)

        # Bamboo Terrace Rules
        # This requires a swim in air or a glide out of bounds.
        if self.options.enable_progressive_sparx_logic.value and not self.options.logic_bamboo_early.value:
            set_indirect_rule(self, "Bamboo Terrace", lambda state: has_sparx_health(self, 1, state) and state.has("Egg", self.player, 30))
        elif not self.options.logic_bamboo_early.value:
            set_indirect_rule(self, "Bamboo Terrace", lambda state: state.has("Egg", self.player, 30))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Bamboo Terrace", lambda state: has_sparx_health(self, 1, state))
        # This requires a swim in air.
        if not self.options.logic_bamboo_bentley_early.value:
            set_rule(self.multiworld.get_location("Bamboo Terrace: Smash to the mountain top. (Brubeck)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Bamboo Terrace: Life Bottle in Bentley Sub-Area", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state))
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Bamboo Terrace: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Bamboo Terrace", state) >= 375)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Bamboo Terrace: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Bamboo Terrace", state) >= 500)

        # Country Speedway Rules
        # This requires a swim in air.
        if not self.options.logic_country_early.value:
            set_indirect_rule(self, "Country Speedway", lambda state: state.has("Egg", self.player, 36))
        # Hunter speedway challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Country Speedway: Hunter's rescue mission. (Roberto)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))

        # Sgt. Byrd's Base Rules
        # This requires a swim in air or a glide out of bounds.
        if self.options.enable_progressive_sparx_logic.value and self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not self.options.logic_byrd_early.value:
            set_indirect_rule(self, "Sgt. Byrd's Base", lambda state: has_sparx_health(self, 1, state) and is_companion_unlocked(self, "Sgt. Byrd", state))
        elif self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not self.options.logic_byrd_early.value:
            set_indirect_rule(self, "Sgt. Byrd's Base", lambda state: is_companion_unlocked(self, "Sgt. Byrd", state))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Sgt. Byrd's Base", lambda state: has_sparx_health(self, 1, state))

        # Spike's Arena Rules
        # With progressive Sparx logic on, everything past this point implicitly requires 1 health.
        set_indirect_rule(self, "Spike", lambda state: is_level_completed(self,"Icy Peak", state) and \
                is_level_completed(self,"Enchanted Towers", state) and \
                is_level_completed(self,"Spooky Swamp", state) and \
                is_level_completed(self,"Bamboo Terrace", state) and \
                is_level_completed(self,"Sgt. Byrd's Base", state))

        # Spider Town Rules
        set_indirect_rule(self, "Spider Town", lambda state: is_boss_defeated(self,"Spike", state))

        # Evening Lake Rules
        if self.options.enable_world_keys:
            set_indirect_rule(self, "Evening Lake", lambda state: is_boss_defeated(self, "Spike", state) and has_world_keys(self, 2, state))
        else:
            set_indirect_rule(self, "Evening Lake", lambda state: is_boss_defeated(self, "Spike", state))

        # Frozen Altars Rules
        # In hwd's randomizer, any Evening Lake level can be in any portal, so require 65 eggs and Bentley access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Frozen Altars", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
                else:
                    set_indirect_rule(self, "Frozen Altars", lambda state: state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Frozen Altars", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65))
                else:
                    set_indirect_rule(self, "Frozen Altars", lambda state: state.has("Egg", self.player, 65))

        # Requires a proxy or getting onto the nearby wall and gliding out of bounds
        if not self.options.logic_frozen_bentley_early.value:
            # 0 gems in Bentley subarea.
            set_rule(self.multiworld.get_location("Frozen Altars: Box the yeti. (Aly)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state))
            set_rule(self.multiworld.get_location("Frozen Altars: Box the yeti again! (Ricco)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state) and state.can_reach_location("Frozen Altars: Box the yeti. (Aly)", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Frozen Altars: Beat yeti in two rounds (Skill Point)", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state) and state.can_reach_location("Frozen Altars: Box the yeti. (Aly)", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Frozen Altars: Beat yeti in two rounds (Goal)", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state) and state.can_reach_location("Frozen Altars: Box the yeti. (Aly)", self.player))
        # Requires a proxy.
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY and not self.options.logic_frozen_cat_hockey_no_moneybags:
            # 0 gems in cat hockey subarea.
            set_rule(self.multiworld.get_location("Frozen Altars: Catch the ice cats. (Ba'ah)", self.player), lambda state: state.has("Moneybags Unlock - Frozen Altars Cat Hockey Door", self.player))

        # Lost Fleet Rules
        # In hwd's randomizer, any Evening Lake level can be in any portal, so require 65 eggs and Bentley access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Lost Fleet", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
                else:
                    set_indirect_rule(self, "Lost Fleet", lambda state: state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Lost Fleet", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65))
                else:
                    set_indirect_rule(self, "Lost Fleet", lambda state: state.has("Egg", self.player, 65))
        # Skateboarding challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Lost Fleet: Skate race the rhynocs. (Oliver)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        set_rule(self.multiworld.get_location("Lost Fleet: Skate race Hunter. (Aiden)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: Skateboard record time (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: Skateboard record time (Goal)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: Life Bottle in Skateboarding Sub-Area", self.player), lambda state: is_boss_defeated(self, "Scorch", state))
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Lost Fleet", state) >= 600)

        # Fireworks Factory Rules
        # In hwd's randomizer, any Evening Lake level can be in any portal, so require 65 eggs and Bentley access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Fireworks Factory", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
                else:
                    set_indirect_rule(self, "Fireworks Factory", lambda state: state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Fireworks Factory", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65))
                else:
                    set_indirect_rule(self, "Fireworks Factory", lambda state: state.has("Egg", self.player, 65))
        # Requires either a zombie swim in air or a glide out of bounds.
        elif not self.options.logic_fireworks_early.value:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(self, "Fireworks Factory", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 50))
            else:
                set_indirect_rule(self, "Fireworks Factory", lambda state: state.has("Egg", self.player, 50))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Fireworks Factory", lambda state: has_sparx_health(self, 2, state))
        # This requires a careful glide to the right "antenna" of the subarea hut.
        if not self.options.logic_fireworks_agent_9_early.value:
            set_rule(self.multiworld.get_location("Fireworks Factory: You're doomed! (Patty)", self.player), lambda state: is_level_completed(self,"Agent 9's Lab", state))
            set_rule(self.multiworld.get_location("Fireworks Factory: You're still doomed! (Donovan)", self.player), lambda state: is_level_completed(self,"Agent 9's Lab", state) and state.can_reach_location("Fireworks Factory: You're doomed! (Patty)", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Fireworks Factory: Find Agent 9's powerup (Skill Point)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Fireworks Factory: Find Agent 9's powerup (Goal)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Fireworks Factory: Life Bottle in Agent 9 Sub-Area", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Fireworks Factory: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Fireworks Factory", state) >= 450)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Fireworks Factory: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Fireworks Factory", state) >= 600)

        # Charmed Ridge Rules
        # In hwd's randomizer, any Evening Lake level can be in any portal, so require 65 eggs and Bentley access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Charmed Ridge", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
                else:
                    set_indirect_rule(self, "Charmed Ridge", lambda state: state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Charmed Ridge", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65))
                else:
                    set_indirect_rule(self, "Charmed Ridge", lambda state: state.has("Egg", self.player, 65))
        # Requires a zombie swim in air.
        elif not self.options.logic_charmed_early.value:
            if self.options.enable_progressive_sparx_logic.value:
                set_indirect_rule(self, "Charmed Ridge", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 58))
            else:
                set_indirect_rule(self, "Charmed Ridge", lambda state: state.has("Egg", self.player, 58))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Charmed Ridge", lambda state: has_sparx_health(self, 2, state))
        # Can glide through a part of the wall with no collision.  A proxy to end of level is possible, but this is harder and grants less access.
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY and not self.options.logic_charmed_no_moneybags.value:
            set_rule(self.multiworld.get_location("Charmed Ridge: Rescue the Fairy Princess. (Sakura)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Glide to the tower. (Moe)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Egg in the cave. (Benjamin)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Jack and the beanstalk I. (Shelley)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Jack and the beanstalk II. (Chuck)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge Complete", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Cat witch chaos. (Abby)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state) and state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Skill Point)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state) and state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
                set_rule(self.multiworld.get_location("Charmed Ridge: The Impossible Tower (Skill Point)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Goal)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state) and state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
                set_rule(self.multiworld.get_location("Charmed Ridge: The Impossible Tower (Goal)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
        else:
            set_rule(self.multiworld.get_location("Charmed Ridge: Cat witch chaos. (Abby)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Skill Point)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Goal)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
        if Spyro3LocationCategory.GEM_25 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Charmed Ridge: 25% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Charmed Ridge", state) >= 150)
        if Spyro3LocationCategory.GEM_50 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Charmed Ridge: 50% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Charmed Ridge", state) >= 300)
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Charmed Ridge: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Charmed Ridge", state) >= 450)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Charmed Ridge: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Charmed Ridge", state) >= 600)

        # Honey Speedway Rules
        # In hwd's randomizer, any Evening Lake level can be in any portal, so require 65 eggs and Bentley access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Honey Speedway", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
                else:
                    set_indirect_rule(self, "Honey Speedway", lambda state: state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Honey Speedway", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65))
                else:
                    set_indirect_rule(self, "Honey Speedway", lambda state: state.has("Egg", self.player, 65))
        # Can be done with a zombie swim in air or a glide out of bounds.
        elif not self.options.logic_honey_early.value:
            set_indirect_rule(self, "Honey Speedway", lambda state: state.has("Egg", self.player, 65))
        # Hunter speedway challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Honey Speedway: Hunter's narrow escape. (Nori)", self.player), lambda state: is_boss_defeated(self, "Scorch", state))

        # Bentley's Outpost Rules
        # This requires a zombie swim in air or a glide out of bounds.
        # In hwd's randomizer, any Evening Lake level can be in any portal, so require 65 eggs and Bentley access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Bentley's Outpost", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
                else:
                    set_indirect_rule(self, "Bentley's Outpost", lambda state: state.has("Egg", self.player, 65) and state.has("Moneybags Unlock - Bentley", self.player))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Bentley's Outpost", lambda state: has_sparx_health(self, 2, state) and state.has("Egg", self.player, 65))
                else:
                    set_indirect_rule(self, "Bentley's Outpost", lambda state: state.has("Egg", self.player, 65))
        elif self.options.moneybags_settings.value != MoneybagsOptions.VANILLA and not self.options.logic_bentley_early.value:
            set_indirect_rule(self, "Bentley's Outpost", lambda state: is_companion_unlocked(self, "Bentley", state))

        # Scorch's Pit Rules
        # Everything after this point implicitly requires 2 health if progressive Sparx health is on.
        set_indirect_rule(self, "Scorch", lambda state: is_level_completed(self,"Frozen Altars", state) and \
                is_level_completed(self,"Lost Fleet", state) and \
                is_level_completed(self,"Fireworks Factory", state) and \
                is_level_completed(self,"Charmed Ridge", state) and \
                is_level_completed(self,"Bentley's Outpost", state))

        # Starfish Reef Rules
        set_indirect_rule(self, "Starfish Reef", lambda state: is_boss_defeated(self,"Scorch", state))

        # Midnight Mountain Rules
        if self.options.enable_world_keys:
            set_indirect_rule(self, "Midnight Mountain", lambda state: is_boss_defeated(self, "Scorch", state) and has_world_keys(self, 3, state))
        else:
            set_indirect_rule(self, "Midnight Mountain", lambda state: is_boss_defeated(self, "Scorch", state))
        set_rule(self.multiworld.get_location("Midnight Mountain Home: Egg for sale. (Al)", self.player), lambda state: is_boss_defeated(self,"Sorceress", state))
        set_rule(self.multiworld.get_location("Midnight Mountain Home: Moneybags Chase Complete", self.player), lambda state: is_boss_defeated(self, "Sorceress", state))

        # Crystal Islands Rules
        # In hwd's randomizer, any Midnight Mountain level can be in any portal, so require 90 eggs and Agent 9 access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Crystal Islands", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
                else:
                    set_indirect_rule(self, "Crystal Islands", lambda state: state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Crystal Islands", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90))
                else:
                    set_indirect_rule(self, "Crystal Islands", lambda state: state.has("Egg", self.player, 90))
        # Can defeat the Sorceress or perform a swim in air.
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY and not self.options.logic_crystal_no_moneybags.value:
            # Moneybags locks 475 gems.
            set_rule(self.multiworld.get_location("Crystal Islands: Reach the crystal tower. (Lloyd)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands: Ride the slide. (Elloise)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands: Fly to the hidden egg. (Grace)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands: Catch the flying thief. (Max)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands Complete", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands: Whack a mole. (Hank)", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state) and (is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player)))
        else:
            set_rule(self.multiworld.get_location("Crystal Islands: Whack a mole. (Hank)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state))
        if Spyro3LocationCategory.GEM_50 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Crystal Islands: 50% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Crystal Islands", state) >= 350)
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Crystal Islands: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Crystal Islands", state) >= 525)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Crystal Islands: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Crystal Islands", state) >= 700)

        # Desert Ruins Rules
        # In hwd's randomizer, any Midnight Mountain level can be in any portal, so require 90 eggs and Agent 9 access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Desert Ruins", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
                else:
                    set_indirect_rule(self, "Desert Ruins", lambda state: state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Desert Ruins", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90))
                else:
                    set_indirect_rule(self, "Desert Ruins", lambda state: state.has("Egg", self.player, 90))
        set_rule(self.multiworld.get_location("Desert Ruins: Krash Kangaroo I. (Lester)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        set_rule(self.multiworld.get_location("Desert Ruins: Krash Kangaroo II. (Pete)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        # Can defeat the Sorceress, proxy off a scorpion, or do a terrain jump to end of level.
        if self.options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY and not self.options.logic_desert_no_moneybags.value:
            # 79 gems in Sheila subarea. 252 are locked behind Moneybags.
            set_rule(self.multiworld.get_location("Desert Ruins: Raid the tomb. (Marty)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            set_rule(self.multiworld.get_location("Desert Ruins: Shark shootin'. (Sadie)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            set_rule(self.multiworld.get_location("Desert Ruins Complete", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Desert Ruins: Destroy all seaweed (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Desert Ruins: Destroy all seaweed (Goal)", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Desert Ruins: Life Bottle near Sharks Sub-Area", self.player), lambda state: is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
        if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Desert Ruins: 75% Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Desert Ruins", state) >= 525)
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Desert Ruins: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Desert Ruins", state) >= 700)

        # Haunted Tomb Rules
        # No known way to skip into Haunted Tomb.
        # In hwd's randomizer, any Midnight Mountain level can be in any portal, so require 90 eggs and Agent 9 access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Haunted Tomb", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
                else:
                    set_indirect_rule(self, "Haunted Tomb", lambda state: state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Haunted Tomb", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90))
                else:
                    set_indirect_rule(self, "Haunted Tomb", lambda state: state.has("Egg", self.player, 90))
        else:
            set_indirect_rule(self, "Haunted Tomb", lambda state: state.has("Egg", self.player, 70))
        set_rule(self.multiworld.get_location("Haunted Tomb: Clear the caves. (Roxy)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))

        # Dino Mines Rules
        # No known way to skip into Dino Mines.
        # In hwd's randomizer, any Midnight Mountain level can be in any portal, so require 90 eggs and Agent 9 access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Dino Mines", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
                else:
                    set_indirect_rule(self, "Dino Mines", lambda state: state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Dino Mines", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90))
                else:
                    set_indirect_rule(self, "Dino Mines", lambda state: state.has("Egg", self.player, 90))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Dino Mines", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 80))
        else:
            set_indirect_rule(self, "Dino Mines", lambda state: state.has("Egg", self.player, 80))
        set_rule(self.multiworld.get_location("Dino Mines: Gunfight at the Jurassic Corral. (Sharon)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        set_rule(self.multiworld.get_location("Dino Mines: Take it to the bank. (Sergio)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state) and state.can_reach_location("Dino Mines: Gunfight at the Jurassic Corral. (Sharon)", self.player))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Dino Mines: Hit the secret dino (Skill Point)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Dino Mines: Hit the secret dino (Goal)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        if Spyro3LocationCategory.GEM in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Dino Mines: All Gems", self.player), lambda state: get_gems_accessible_in_level(self, "Dino Mines", state) >= 700)

        # Harbor Speedway Rules
        # No known way to skip into Harbor Speedway.
        # In hwd's randomizer, any Midnight Mountain level can be in any portal, so require 90 eggs and Agent 9 access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Harbor Speedway", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
                else:
                    set_indirect_rule(self, "Harbor Speedway", lambda state: state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Harbor Speedway", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90))
                else:
                    set_indirect_rule(self, "Harbor Speedway", lambda state: state.has("Egg", self.player, 90))
        else:
            set_indirect_rule(self, "Harbor Speedway", lambda state: state.has("Egg", self.player, 90))

        # Agent 9's Lab Rules
        # No known way to skip into Agent 9's Lab, other than beating the Sorceress.
        # In hwd's randomizer, any Midnight Mountain level can be in any portal, so require 90 eggs and Agent 9 access for
        # each since we have no way to tell which portal is which level.
        if self.options.enable_hwd_randomizer.value:
            if self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Agent 9's Lab", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
                else:
                    set_indirect_rule(self, "Agent 9's Lab", lambda state: state.has("Egg", self.player, 90) and (is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state)))
            else:
                if self.options.enable_progressive_sparx_logic.value:
                    set_indirect_rule(self, "Agent 9's Lab", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 90))
                else:
                    set_indirect_rule(self, "Agent 9's Lab", lambda state: state.has("Egg", self.player, 90))
        elif self.options.moneybags_settings.value != MoneybagsOptions.VANILLA:
            set_indirect_rule(self, "Agent 9's Lab", lambda state: is_companion_unlocked(self, "Agent 9", state) or is_boss_defeated(self, "Sorceress", state))

        # Sorceress' Lair Rules
        if not self.options.logic_sorceress_early.value and self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Sorceress", lambda state: has_sparx_health(self, 3, state) and state.has("Egg", self.player, 100))
        elif not self.options.logic_sorceress_early.value:
            set_indirect_rule(self, "Sorceress", lambda state: state.has("Egg", self.player, 100))
        elif self.options.enable_progressive_sparx_logic.value:
            set_indirect_rule(self, "Sorceress", lambda state: has_sparx_health(self, 3, state))

        # Bugbot Factory Rules
        set_indirect_rule(self, "Bugbot Factory", lambda state: is_boss_defeated(self,"Sorceress", state))

        # Super Bonus Round Rules
        # Ensure all gems are in logic.
        set_indirect_rule(
            self,
            "Super Bonus Round",
            lambda state: is_boss_defeated(self, "Sorceress", state) and state.has("Egg", self.player, 149) and has_all_gems(self, state)
        )

        # Inventory Rules
        if Spyro3LocationCategory.TOTAL_GEM in self.enabled_location_categories:
            for i in range(40):
                gems = 500 * (i + 1)
                if gems <= self.options.max_total_gem_checks.value:
                    set_rule(self.multiworld.get_location(f"Total Gems: {gems}", self.player), lambda state, gems=gems: has_total_accessible_gems(self, state, gems))
                else:
                    break

                
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_s3_code = {item.name: item.s3_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        hints = {}
        
        for location in self.multiworld.get_filled_locations():


            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_s3_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].s3_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_s3_code[location.item.name])
                else:
                    locations_target.append(0)

        if self.options.zoe_gives_hints.value > 0:
            hints = generateHints(self.player, self.options.zoe_gives_hints.value, self)
        

        slot_data = {
            "options": {
                "goal": self.options.goal.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "enable_25_pct_gem_checks": self.options.enable_25_pct_gem_checks.value,
                "enable_50_pct_gem_checks": self.options.enable_50_pct_gem_checks.value,
                "enable_75_pct_gem_checks": self.options.enable_75_pct_gem_checks.value,
                "enable_gem_checks": self.options.enable_gem_checks.value,
                "enable_total_gem_checks": self.options.enable_total_gem_checks.value,
                "max_total_gem_checks": self.options.max_total_gem_checks.value,
                #"enable_gemsanity_checks": self.options.enable_gemsanity_checks.value,
                "enable_skillpoint_checks": self.options.enable_skillpoint_checks.value,
                "enable_life_bottle_checks": self.options.enable_life_bottle_checks.value,
                "sparx_power_settings": self.options.sparx_power_settings.value,
                "moneybags_settings": self.options.moneybags_settings.value,
                "enable_world_keys": self.options.enable_world_keys.value,
                "enable_filler_extra_lives": self.options.enable_filler_extra_lives.value,
                "enable_filler_invincibility": self.options.enable_filler_invincibility.value,
                "enable_filler_color_change": self.options.enable_filler_color_change.value,
                "enable_filler_big_head_mode": self.options.enable_filler_big_head_mode.value,
                "enable_filler_heal_sparx": self.options.enable_filler_heal_sparx.value,
                "trap_filler_percent": self.options.trap_filler_percent.value,
                "enable_trap_damage_sparx": self.options.enable_trap_damage_sparx.value,
                "enable_trap_sparxless": self.options.enable_trap_sparxless.value,
                #"enable_trap_lag": self.options.enable_trap_lag.value,
                "enable_progressive_sparx_health": self.options.enable_progressive_sparx_health.value,
                "enable_progressive_sparx_logic": self.options.enable_progressive_sparx_logic.value,
                "zoe_gives_hints": self.options.zoe_gives_hints.value,
                "enable_hwd_randomizer": self.options.enable_hwd_randomizer.value,
                "easy_skateboarding": self.options.easy_skateboarding.value,
                "easy_boxing": self.options.easy_boxing.value,
                "easy_sheila_bombing": self.options.easy_sheila_bombing.value,
                "easy_tanks": self.options.easy_tanks.value,
                "easy_subs": self.options.easy_subs.value,
                "easy_bluto": self.options.easy_bluto.value,
                "easy_sleepyhead": self.options.easy_sleepyhead.value,
                "easy_shark_riders": self.options.easy_shark_riders.value,
                "easy_whackamole": self.options.easy_whackamole.value,
                "easy_tunnels": self.options.easy_tunnels.value,
                "logic_sunny_sheila_early": self.options.logic_sunny_sheila_early.value,
                "logic_cloud_backwards": self.options.logic_cloud_backwards.value,
                "logic_molten_early": self.options.logic_molten_early.value,
                "logic_molten_byrd_early": self.options.logic_molten_byrd_early.value,
                "logic_molten_thieves_no_moneybags": self.options.logic_molten_thieves_no_moneybags.value,
                "logic_seashell_early": self.options.logic_seashell_early.value,
                "logic_mushroom_early": self.options.logic_mushroom_early.value,
                "logic_sheila_early": self.options.logic_sheila_early.value,
                "logic_spooky_early": self.options.logic_spooky_early.value,
                "logic_spooky_no_moneybags": self.options.logic_spooky_no_moneybags.value,
                "logic_bamboo_early": self.options.logic_bamboo_early.value,
                "logic_bamboo_bentley_early": self.options.logic_bamboo_bentley_early.value,
                "logic_country_early": self.options.logic_country_early.value,
                "logic_byrd_early": self.options.logic_byrd_early.value,
                "logic_frozen_bentley_early": self.options.logic_frozen_bentley_early.value,
                "logic_frozen_cat_hockey_no_moneybags": self.options.logic_frozen_cat_hockey_no_moneybags.value,
                "logic_fireworks_early": self.options.logic_fireworks_early.value,
                "logic_fireworks_agent_9_early": self.options.logic_fireworks_agent_9_early.value,
                "logic_charmed_early": self.options.logic_charmed_early.value,
                "logic_charmed_no_moneybags": self.options.logic_charmed_no_moneybags.value,
                "logic_honey_early": self.options.logic_honey_early.value,
                "logic_bentley_early": self.options.logic_bentley_early.value,
                "logic_crystal_no_moneybags": self.options.logic_crystal_no_moneybags.value,
                "logic_desert_no_moneybags": self.options.logic_desert_no_moneybags.value,
                "logic_sorceress_early": self.options.logic_sorceress_early.value
            },
            "hints": hints,
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
