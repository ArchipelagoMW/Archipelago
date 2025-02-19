from typing import Dict, Set, List, Iterable

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from Options import OptionError
from .Options import DSTOptions, dontstarvetogether_option_groups, dontstarvetogether_option_presets
from . import Regions, Rules, ItemPool, Util
from .Constants import VERSION, PHASE, SEASON, SEASONS_PASSED, SPECIAL_TAGS
from .Locations import location_data_table, location_name_to_id
from .Items import item_data_table, item_name_to_id

from BaseClasses import Item, Tutorial, ItemClassification

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="DontStarveTogetherClient")


components.append(Component("Don't Starve Together Client", func=launch_client,
                            component_type=Type.CLIENT))

class DSTWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Don't Starve Together game.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Dragon Wolf Leo"]
    )]
    option_groups = dontstarvetogether_option_groups
    options_presets = dontstarvetogether_option_presets
    theme = "ice"

class DSTWorld(World):
    """
    Don't Starve Together is a game where you are thrown into a strange and unexplored world full of odd creatures,
    hidden dangers, and ancient secrets known as "The Constant". You must gather resources to craft items and build
    structures and farms to help you protect yourself, survive, and most importantly, not starve.
    """
    game = "Don't Starve Together"

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    options_dataclass = DSTOptions  # assign the options dataclass to the world
    options: DSTOptions  # typing for option results
    topology_present = False
    web = DSTWeb()

    item_name_groups = {"all": set(item_data_table.keys())}

    dst_itempool: ItemPool.DSTItemPool

    def __init__(self, multiworld, player):
        self.dst_itempool = ItemPool.DSTItemPool()
        super().__init__(multiworld, player)

    def generate_early(self):
        _IS_BOSS_GOAL = self.options.goal.value == self.options.goal.option_bosses_any or self.options.goal.value == self.options.goal.option_bosses_all

        # Warn shuffling starting recipes with creature locations disabled and nothing in start inventory
        if self.options.shuffle_starting_recipes.value and not self.options.creature_locations.value and not len(self.options.start_inventory):
            print(f"{self.multiworld.get_player_name(self.player)} (Don't Starve Together): Warning! Shuffle Starting Recipes without Creature Locations. "\
                "Player will potentially have no reachable checks in Sphere 1!"
            )

        # Get regions bosses are in
        _auto_regions = set()
        if _IS_BOSS_GOAL:
            self.options.days_to_survive.value = 0
            # Build boss regions
            _BOSS_REGIONS:Dict[str, Set[str]] = {}
            for region_tag in ["cave", "ruins", "archive", "ocean", "moonquay", "moonstorm"]:
                _BOSS_REGIONS[region_tag] = set()
                for bossname in [k for k in self.options.required_bosses.valid_keys if k != "Random"]:
                    if region_tag in location_data_table.get(bossname).tags:
                        _BOSS_REGIONS[region_tag].add(bossname)
            # Merge into the groups that are used by the settings
            _BOSS_REGIONS["ruins"].update(_BOSS_REGIONS["archive"])
            _BOSS_REGIONS["ocean"].update(_BOSS_REGIONS["moonquay"])

            # Compile valid bosses for random choice
            def build_boss_pool(possible_bosses:Iterable[str]) -> List[str]:
                _boss_pool:Set[str] = set(possible_bosses)

                # Filter the random boss pool based on region options
                if self.options.cave_regions.value == self.options.cave_regions.option_none:
                    _boss_pool.difference_update(_BOSS_REGIONS["cave"], _BOSS_REGIONS["ruins"])
                elif self.options.cave_regions.value == self.options.cave_regions.option_light:
                    _boss_pool.difference_update(_BOSS_REGIONS["ruins"])

                if self.options.ocean_regions.value == self.options.ocean_regions.option_none:
                    _boss_pool.difference_update(_BOSS_REGIONS["ocean"], _BOSS_REGIONS["moonstorm"])
                elif self.options.ocean_regions.value == self.options.ocean_regions.option_light:
                    _boss_pool.difference_update(_BOSS_REGIONS["moonstorm"])

                # Filter the random boss pool based on day phase and season
                is_enabled_in_tag_group = Util.create_tag_group_validation_fn(self.options)
                for bossname in _boss_pool.copy():
                    if "seasonal" in location_data_table[bossname].tags:
                        _boss_pool.discard(bossname)
                    else:
                        for _type in [SEASON, PHASE, SEASONS_PASSED, SPECIAL_TAGS]:
                            if not is_enabled_in_tag_group(_type, location_data_table[bossname].tags):
                                _boss_pool.discard(bossname)

                # Sort to make choice deterministic
                _boss_pool_as_sorted_list = list(_boss_pool)
                _boss_pool_as_sorted_list.sort()
                return _boss_pool_as_sorted_list

            # Choose a random boss if random is selected
            if "Random" in self.options.required_bosses.value or not len(self.options.required_bosses.value):
                self.options.required_bosses.value.discard("Random")
                boss_pool = build_boss_pool(
                    self.options.required_bosses.value.copy() if len(self.options.required_bosses.value)
                    else {k for k in self.options.required_bosses.valid_keys if k != "Random"}
                )
                if not len(boss_pool):
                    # May be an invalid selection for settings; choose from everything
                    boss_pool = build_boss_pool({k for k in self.options.required_bosses.valid_keys if k != "Random"})

                if not len(boss_pool):
                    raise OptionError(f"{self.player_name} (Don't Starve Together): "\
                    "No valid boss can be selected from player settings.")

                # Pick random boss from the boss pool
                self.options.required_bosses.value.clear()
                self.options.required_bosses.value.add(self.random.choice(boss_pool))


            # Set valid auto regions for selected bosses
            for regionname, group in _BOSS_REGIONS.items():
                for bossname in group:
                    if bossname in self.options.required_bosses.value:
                        _auto_regions.add(regionname)


            # If bosses_all is chosen with only one boss chosen, change goal to bosses_any
            if self.options.goal.value == self.options.goal.option_bosses_all and len(self.options.required_bosses.value) == 1:
                self.options.goal.value = self.options.goal.option_bosses_any

        else: # if not _IS_BOSS_GOAL
            # Clear the goal bosses. There isn't a "None" option, but "Random" will have to do.
            self.options.required_bosses.value.clear()
            self.options.required_bosses.value.add("Random")

        # Force ocean regions to light if Crab King is not a check
        if (
            self.options.ocean_regions.value == self.options.ocean_regions.option_full
            and self.options.boss_locations.value < self.options.boss_locations.option_all
            and not (
                _IS_BOSS_GOAL
                and len(self.options.required_bosses.value.intersection({"Celestial Champion", "Crab King"}))
            )
        ):
            self.options.ocean_regions.value = self.options.ocean_regions.option_light

        # Set auto regions
        if self.options.cave_regions.value == self.options.cave_regions.option_auto:
            self.options.cave_regions.value = self.options.cave_regions.option_none
            if _IS_BOSS_GOAL:
                if "ruins" in _auto_regions:
                    self.options.cave_regions.value = self.options.cave_regions.option_full
                elif "cave" in _auto_regions:
                    self.options.cave_regions.value = self.options.cave_regions.option_light

        if self.options.ocean_regions.value == self.options.ocean_regions.option_auto:
            self.options.ocean_regions.value = self.options.ocean_regions.option_none
            if _IS_BOSS_GOAL:
                if "moonstorm" in _auto_regions:
                    self.options.ocean_regions.value = self.options.ocean_regions.option_full
                elif "ocean" in _auto_regions:
                    self.options.ocean_regions.value = self.options.ocean_regions.option_light

        # Auto set logic options
        ADVANCED_PLAYER_BIAS = self.options.skill_level.current_key != "easy"
        EXPERT_PLAYER_BIAS = self.options.skill_level.current_key == "expert"
        if self.options.lighting_logic.current_key == "auto":
            self.options.lighting_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.weapon_logic.current_key == "auto":
            self.options.weapon_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.season_gear_logic.current_key == "auto":
            self.options.season_gear_logic.value = 0 if ADVANCED_PLAYER_BIAS else 2
        if self.options.base_making_logic.current_key == "auto":
            self.options.base_making_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.backpack_logic.current_key == "auto":
            self.options.backpack_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.healing_logic.current_key == "auto":
            self.options.healing_logic.value = 0 if ADVANCED_PLAYER_BIAS else 2

        # Create itempools
        self.dst_itempool.decide_itempools(self)

    def create_item(self, name: str) -> Item:
        """
        Item creation function for DST, intended for external calls. Using this function directly will always produce a progression item.
        If creating items within the world, use dst_itempool's create_items to get default classification.
        """
        item = self.dst_itempool.create_item(self, name)
        item.classification = ItemClassification.progression # Force spawned items to be progression so they could be in logic
        return item

    def create_items(self) -> None:
        self.dst_itempool.create_items(self)

    def get_filler_item_name(self) -> str:
        return self.dst_itempool.get_filler_item_name(self)

    def create_regions(self):
        Regions.create_regions(self.multiworld, self.player, self.options, self.dst_itempool)
        Rules.set_rules(self, self.dst_itempool) # create_items needs rules set first

    def set_rules(self) -> None:
        pass

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        # Add crafting stations to hint information
        def get_station_from_tags(tags: Set[str]) -> str:
            return (
                "Science Machine" if "science" in tags and "tier_1" in tags
                else "Alchemy Engine" if "science" in tags and "tier_2" in tags
                else "Prestihatitor" if "magic" in tags and "tier_1" in tags
                else "Shadow Manipulator" if "magic" in tags and "tier_2" in tags
                else "Think Tank" if "seafaring" in tags
                else "Celestial Orb" if "celestial" in tags and "tier_1" in tags
                else "Celestial Altar" if "celestial" in tags and "tier_2" in tags
                else "Broken Pseudoscience Station" if "ancient" in tags and "tier_1" in tags
                else "Ancient Pseudoscience Station" if "ancient" in tags and "tier_2" in tags
                else "Crabby Hermit (Friendship Level 1)" if "hermitcrab" in tags and "tier_1" in tags
                else "Crabby Hermit (Friendship Level 3)" if "hermitcrab" in tags and "tier_2" in tags
                else "Crabby Hermit (Friendship Level 6)" if "hermitcrab" in tags and "tier_3" in tags
                else "Crabby Hermit (Friendship Level 8)" if "hermitcrab" in tags and "tier_4" in tags
                else "Vanilla"
            )
        hint_information:Dict[int, str] = {}
        for data in location_data_table.values():
            if "research" in data.tags:
                hint_information[data.address] = get_station_from_tags(data.tags)
            elif "cooking" in data.tags:
                hint_information[data.address] = "Portable Crock Pot" if "warly" in data.tags else "Crock Pot"
        hint_data[self.player] = hint_information

    def fill_slot_data(self):
        slot_data = {
            "generator_version":    VERSION,
            "death_link":           bool(self.options.death_link.value),
            "goal":                 self.options.goal.current_key,
            "crafting_mode":        self.options.crafting_mode.current_key,
            "locked_items_local_id":list(self.dst_itempool.locked_items_local_id),
            # World settings
            "is_caves_enabled":     bool(self.options.cave_regions.value != self.options.cave_regions.option_none),
            "seasons":              list(self.options.seasons.value),
            "starting_season":      self.options.starting_season.current_key,
            "unlockable_seasons":   bool(self.options.season_flow.current_key.startswith("unlockable")),
            "day_phases":           list(self.options.day_phases.value),
            "character":            "Warly" if self.options.cooking_locations.value == self.options.cooking_locations.option_warly_enabled else "Any",
        }
        if slot_data["goal"] == "survival":
            slot_data["days_to_survive"] = self.options.days_to_survive.value
        else:
            slot_data["goal_locations"] = [location_name_to_id[loc_name] for loc_name in self.options.required_bosses.value]
        return slot_data