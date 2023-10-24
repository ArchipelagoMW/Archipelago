from enum import IntEnum
from typing import Any, List, Dict, Set, Callable, Optional, TextIO

from BaseClasses import ItemClassification, CollectionState, Region, Entrance, Location, Tutorial, LocationProgressType
from worlds.AutoWorld import World, WebWorld

from .Overcooked2Levels import Overcooked2Dlc, Overcooked2Level, Overcooked2GenericLevel
from .Locations import Overcooked2Location, oc2_location_name_to_id, oc2_location_id_to_name
from .Options import OC2Options, OC2OnToggle, LocationBalancingMode, DeathLinkMode
from .Items import item_table, Overcooked2Item, item_name_to_id, item_id_to_name, item_to_unlock_event, item_frequencies, dlc_exclusives
from .Logic import has_requirements_for_level_star, has_requirements_for_level_access, level_shuffle_factory, is_item_progression, is_useful


class Overcooked2Web(WebWorld):
    theme = "partyTime"

    bug_report_page = "https://github.com/toasterparty/oc2-modding/issues"
    setup_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Overcooked! 2 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["toasterparty"]
    )

    tutorials = [setup_en]


class PrepLevelMode(IntEnum):
    original = 0
    excluded = 1
    ayce = 2


class Overcooked2World(World):
    """
    Overcooked! 2 is a frantically paced arcade cooking game where
    players race against the clock to complete orders for points. Bring
    peace to the Onion Kingdom once again by recovering lost items and abilities,
    earning stars to unlock levels, and defeating the unbread horde. Levels are
    randomized to increase gameplay variety. Play with up to 4 friends.
    """

    # Autoworld API

    game = "Overcooked! 2"
    web = Overcooked2Web()
    required_client_version = (0, 3, 8)
    topology_present: bool = False
    data_version = 3

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = oc2_location_id_to_name
    location_name_to_id = oc2_location_name_to_id

    options_dataclass = OC2Options
    options: OC2Options
    itempool: List[Overcooked2Item]

    # Helper Functions

    def is_level_horde(self, level_id: int) -> bool:
        return self.options.include_horde_levels and \
            (self.level_mapping is not None) and \
            level_id in self.level_mapping.keys() and \
            self.level_mapping[level_id].is_horde

    def create_item(self, item: str, classification: ItemClassification = ItemClassification.progression) -> Overcooked2Item:
        return Overcooked2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str, classification: ItemClassification) -> Overcooked2Item:
        return Overcooked2Item(event, classification, None, self.player)

    def place_event(self, location_name: str, item_name: str,
                    classification: ItemClassification = ItemClassification.progression_skip_balancing):
        location: Location = self.multiworld.get_location(location_name, self.player)
        location.place_locked_item(self.create_event(item_name, classification))

    def add_region(self, region_name: str):
        region = Region(
            region_name,
            self.player,
            self.multiworld,
        )
        self.multiworld.regions.append(region)

    def connect_regions(self, source: str, target: str, rule: Optional[Callable[[CollectionState], bool]] = None):
        sourceRegion = self.multiworld.get_region(source, self.player)
        targetRegion = self.multiworld.get_region(target, self.player)

        connection = Entrance(self.player, '', sourceRegion)
        if rule:
            connection.access_rule = rule

        sourceRegion.exits.append(connection)
        connection.connect(targetRegion)

    def add_level_location(
        self,
        region_name: str,
        location_name: str,
        level_id: int,
        stars: int,
        is_event: bool = False,
        priority=False,
    ) -> None:

        if is_event:
            location_id = None
        else:
            location_id = level_id

        region = self.multiworld.get_region(region_name, self.player)
        location = Overcooked2Location(
            self.player,
            location_name,
            location_id,
            region,
        )

        location.event = is_event

        if priority:
            location.progress_type = LocationProgressType.PRIORITY
        else:
            location.progress_type = LocationProgressType.DEFAULT

        # if level_id is none, then it's the 6-6 edge case
        if level_id is None:
            level_id = 36
        if self.level_mapping is not None and level_id in self.level_mapping:
            level = self.level_mapping[level_id]
        else:
            level = Overcooked2GenericLevel(level_id)

        completion_condition: Callable[[CollectionState], bool] = \
            lambda state, level=level, stars=stars: \
            has_requirements_for_level_star(state, level, stars, self.player)
        location.access_rule = completion_condition

        region.locations.append(
            location
        )

    def get_n_random_locations(self, n: int) -> List[int]:
        """Return a list of n random non-repeating level locations"""
        levels = list()

        if n == 0:
            return levels

        for level in Overcooked2Level():
            if level.level_id == 36:
                continue
            elif not self.options.kevin_levels and level.level_id > 36:
                break

            levels.append(level.level_id)

        self.multiworld.random.shuffle(levels)
        return levels[:n]

    def get_priority_locations(self) -> List[int]:
        """Randomly generate list of priority locations, thus insulating this game
        from the negative effects of being shuffled with games that contain large
        ammounts of filler"""

        if self.multiworld.players == 1:
            # random priority locations have no desirable effect on solo seeds
            return list()

        balancing_mode = self.options.location_balancing

        if balancing_mode == LocationBalancingMode.disabled:
            # Location balancing is disabled, progression density is purely determined by filler
            return list()

        # Count how many progression items are required for this overcooked instance
        game_item_count = len(self.itempool)
        game_progression_count = 0
        for item in self.itempool:
            if item.classification == ItemClassification.progression:
                game_progression_count += 1
        game_progression_density = game_progression_count/game_item_count

        if balancing_mode == LocationBalancingMode.full:
            # Location balancing will be employed in an attempt to keep the number of
            # progression locations and proression items as close to equal as possible
            return self.get_n_random_locations(game_progression_count)

        assert balancing_mode == LocationBalancingMode.compromise

        # Count how many progression items are shuffled between all games
        total_item_count = len(self.multiworld.itempool)
        total_progression_count = 0

        for item in self.multiworld.itempool:
            if item.classification == ItemClassification.progression:
                total_progression_count += 1
        total_progression_density = total_progression_count/total_item_count

        if total_progression_density >= game_progression_density:
            # This game has more filler than the average of all other games.
            # It is not in need of location balancing
            return list()

        # Calculate the midpoint between the two ratios
        target_progression_ratio = (game_progression_density - total_progression_density) / 2.0 + total_progression_density
        target_progression_count = int((target_progression_ratio * game_item_count) + 0.5) # I'm sorry I round like an old person

        # Location balancing will be employed in an attempt to find a compromise at
        # the half-way point between natural probability and full artifical balancing
        return self.get_n_random_locations(target_progression_count)

    # Helper Data

    player_name: str
    level_unlock_counts: Dict[int, int]  # level_id, stars to purchase
    level_mapping: Dict[int, Overcooked2GenericLevel]  # level_id, level
    enabled_dlc: Set[Overcooked2Dlc]

    # Autoworld Hooks

    def generate_early(self):
        self.player_name = self.multiworld.player_name[self.player]

        # 0.0 to 1.0 where 1.0 is World Record
        self.star_threshold_scale = self.options.star_threshold_scale / 100.0

        # Parse DLCOptionSet back into enums
        self.enabled_dlc = {Overcooked2Dlc(x) for x in self.options.include_dlcs.value}

        # Generate level unlock requirements such that the levels get harder to unlock
        # the further the game has progressed, and levels progress radially rather than linearly
        self.level_unlock_counts = level_unlock_requirement_factory(self.options.stars_to_win.value)

        # Assign new kitchens to each spot on the overworld using pure random chance and nothing else
        if self.options.shuffle_level_order:
            self.level_mapping = \
                level_shuffle_factory(
                    self.multiworld.random,
                    self.options.prep_levels != PrepLevelMode.excluded,
                    self.options.include_horde_levels.result,
                    self.options.kevin_levels.result,
                    self.enabled_dlc,
                    self.player_name,
                )
        else:
            self.level_mapping = None
            if Overcooked2Dlc.STORY not in self.enabled_dlc:
                raise Exception(f"Invalid OC2 settings({self.player_name}) Need either Level Shuffle disabled or 'Story' DLC enabled")

            self.enabled_dlc = {Overcooked2Dlc.STORY}

    def set_location_priority(self) -> None:
        priority_locations = self.get_priority_locations()
        for level in Overcooked2Level():
            if level.level_id in priority_locations:
                location: Location = self.multiworld.get_location(level.location_name_item, self.player)
                location.progress_type = LocationProgressType.PRIORITY


    def create_regions(self) -> None:
        # Menu -> Overworld
        self.add_region("Menu")
        self.add_region("Overworld")
        self.connect_regions("Menu", "Overworld")

        # Create and populate "regions" (a.k.a. levels)
        for level in Overcooked2Level():
            if not self.options.kevin_levels and level.level_id > 36:
                break

            # Create Region (e.g. "1-1")
            self.add_region(level.level_name)

            # Add Location to house progression item (1-star)
            if level.level_id == 36:
                # 6-6 doesn't have progression, but it does have victory condition which is placed later
                self.add_level_location(
                    level.level_name,
                    level.location_name_item,
                    None,
                    1,
                )
            else:
                # Location to house progression item
                self.add_level_location(
                    level.level_name,
                    level.location_name_item,
                    level.level_id,
                    1,
                )

                # Location to house level completed event
                self.add_level_location(
                    level.level_name,
                    level.location_name_level_complete,
                    level.level_id,
                    1,
                    is_event=True,
                )

            # Add Locations to house star aquisition events
            if self.is_level_horde(level.level_id):
                # in randomizer, horde levels grant a single star
                star_counts = [1]
            else:
                star_counts = [1, 2, 3]

            for n in star_counts:
                self.add_level_location(
                    level.level_name,
                    level.location_name_star_event(n),
                    level.level_id,
                    n,
                    is_event=True,
                )

            # Overworld -> Level
            required_star_count: int = self.level_unlock_counts[level.level_id]
            if level.level_id % 6 != 1 and level.level_id <= 36:
                previous_level_completed_event_name: str = Overcooked2GenericLevel(
                    level.level_id - 1).shortname.split(" ")[1] + " Level Complete"
            else:
                previous_level_completed_event_name = None

            level_access_rule: Callable[[CollectionState], bool] = \
                lambda state, level_name=level.level_name, previous_level_completed_event_name=previous_level_completed_event_name, required_star_count=required_star_count: \
                has_requirements_for_level_access(state, level_name, previous_level_completed_event_name, required_star_count, self.options.ramp_tricks.result, self.player)
            self.connect_regions("Overworld", level.level_name, level_access_rule)

            # Level --> Overworld
            self.connect_regions(level.level_name, "Overworld")

        completion_condition: Callable[[CollectionState], bool] = lambda state: \
            state.has("Victory", self.player)
        self.multiworld.completion_condition[self.player] = completion_condition


    def create_items(self):
        self.itempool = []

        # Make Items
        # useful = list()
        # filler = list()
        # progression = list()
        for item_name in item_table:            
            if item_name in item_frequencies:
                freq = item_frequencies[item_name]
            else:
                freq = 1
            
            if freq <= 0:
                # not used
                continue

            if item_name in dlc_exclusives:
                if not any(x in dlc_exclusives[item_name] for x in self.enabled_dlc):
                    # Item is always useless with these settings
                    continue

            if not self.options.include_horde_levels and item_name in ["Calmer Unbread", "Coin Purse"]:
                # skip horde-specific items if no horde levels
                continue

            if not self.options.kevin_levels:
                if item_name.startswith("Kevin"):
                    # skip kevin items if no kevin levels
                    continue

                if item_name == "Dark Green Ramp":
                    # skip dark green ramp if there's no Kevin-1 to reveal it
                    continue

            if is_item_progression(item_name, self.level_mapping, self.options.kevin_levels):
                # progression.append(item_name)
                classification = ItemClassification.progression
            else:
                if (is_useful(item_name)):
                    # useful.append(item_name)
                    classification = ItemClassification.useful
                else:
                    # filler.append(item_name)
                    classification = ItemClassification.filler

            while freq > 0:
                self.itempool.append(self.create_item(item_name, classification))
                classification = ItemClassification.useful  # only the first progressive item can be progression
                freq -= 1

        # print(f"progression: {progression}")
        # print(f"useful: {useful}")
        # print(f"filler: {filler}")

        # Fill any free space with filler
        pool_count = len(oc2_location_name_to_id)
        if not self.options.kevin_levels:
            pool_count -= 8

        while len(self.itempool) < pool_count:
            self.itempool.append(self.create_item("Bonus Star", ItemClassification.useful))

        self.multiworld.itempool += self.itempool


    def place_events(self):
        # Add Events (Star Acquisition)
        for level in Overcooked2Level():
            if not self.options.kevin_levels and level.level_id > 36:
                break

            if level.level_id != 36:
                self.place_event(level.location_name_level_complete, level.event_name_level_complete)

            if self.is_level_horde(level.level_id):
                # in randomizer, horde levels grant a single star
                star_counts = [1]
            else:
                star_counts = [1, 2, 3]

            for n in star_counts:
                self.place_event(level.location_name_star_event(n), "Star")

        # Add Victory Condition
        self.place_event("6-6 Completed", "Victory")

    def set_rules(self):
        pass

    def generate_basic(self) -> None:
        self.place_events()
        self.set_location_priority()

    # Items get distributed to locations

    def fill_json_data(self) -> Dict[str, Any]:
        mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.player_name}"

        # Serialize Level Order
        story_level_order = dict()

        if self.options.shuffle_level_order:
            for level_id in self.level_mapping:
                level: Overcooked2GenericLevel = self.level_mapping[level_id]
                story_level_order[str(level_id)] = {
                    "DLC": level.dlc.value,
                    "LevelID": level.level_id,
                }

        custom_level_order = dict()
        custom_level_order["Story"] = story_level_order

        # Serialize Unlock Requirements
        level_purchase_requirements = dict()
        for level_id in self.level_unlock_counts:
            level_purchase_requirements[str(level_id)] = self.level_unlock_counts[level_id]

        # Override Vanilla Unlock Chain Behavior
        # (all worlds accessible from the start and progressible in any order)
        level_unlock_requirements = dict()
        level_force_reveal = [
            1,   # 1-1
            7,   # 2-1
            13,  # 3-1
            19,  # 4-1
            25,  # 5-1
            31,  # 6-1
        ]
        for level_id in range(1, 37):
            if (level_id not in level_force_reveal):
                level_unlock_requirements[str(level_id)] = level_id - 1

        # Set Kevin Unlock Requirements
        if self.options.kevin_levels:
            def kevin_level_to_keyholder_level_id(level_id: int) -> Optional[int]:
                location = self.multiworld.find_item(f"Kevin-{level_id-36}", self.player)
                if location.player != self.player:
                    return None  # This kevin level will be unlocked by the server at runtime
                level_id = oc2_location_name_to_id[location.name]
                return level_id

            for level_id in range(37, 45):
                keyholder_level_id = kevin_level_to_keyholder_level_id(level_id)
                if keyholder_level_id is not None:
                    level_unlock_requirements[str(level_id)] = keyholder_level_id

        # Place Items at Level Completion Screens (local only)
        on_level_completed: Dict[str, list[Dict[str, str]]] = dict()
        locations = self.multiworld.get_filled_locations(self.player)
        for location in locations:
            if location.item.code is None:
                continue  # it's an event
            if location.item.player != self.player:
                continue  # not for us
            level_id = str(oc2_location_name_to_id[location.name])
            on_level_completed[level_id] = [item_to_unlock_event(location.item.name)]

        # Put it all together
        star_threshold_scale = self.options.star_threshold_scale / 100

        base_data = {
            # Changes Inherent to rando
            "DisableAllMods": False,
            "UnlockAllChefs": True,
            "UnlockAllDLC": True,
            "DisplayFPS": True,
            "SkipTutorial": True,
            "SkipAllOnionKing": True,
            "SkipTutorialPopups": True,
            "RevealAllLevels": False,
            "PurchaseAllLevels": False,
            "CheatsEnabled": False,
            "ImpossibleTutorial": True,
            "ForbidDLC": True,
            "ForceSingleSaveSlot": True,
            "DisableNGP": True,
            "LevelForceReveal": level_force_reveal,
            "SaveFolderName": mod_name,
            "CustomOrderTimeoutPenalty": 10,
            "LevelForceHide": [37, 38, 39, 40, 41, 42, 43, 44],
            "LocalDeathLink": self.options.deathlink != DeathLinkMode.disabled,
            "BurnTriggersDeath": self.options.deathlink == DeathLinkMode.death_and_overcook,

            # Game Modifications
            "LevelPurchaseRequirements": level_purchase_requirements,
            "Custom66TimerScale": max(0.4, 0.25 + (1.0 - star_threshold_scale)*0.6),
            "ShortHordeLevels": self.options.short_horde_levels.result,
            "CustomLevelOrder": custom_level_order,

            # Items (Starting Inventory)
            "CustomOrderLifetime": 70.0,  # 100 is original
            "DisableWood": True,
            "DisableCoal": True,
            "DisableOnePlate": True,
            "DisableFireExtinguisher": True,
            "DisableBellows": True,
            "PlatesStartDirty": True,
            "MaxTipCombo": 2,
            "DisableDash": True,
            "WeakDash": True,
            "DisableThrow": True,
            "DisableCatch": True,
            "DisableControlStick": True,
            "DisableWokDrag": True,
            # "DisableRampButton": True, # Unused
            "DisableGreenRampButton" : True,
            "DisableYellowRampButton" : True,
            "DisableBlueRampButton" : True,
            "DisablePinkRampButton" : True,
            "DisableGreyRampButton" : True,
            "DisableRedRampButton" : True,
            "DisablePurpleRampButton" : True,
            "WashTimeMultiplier": 1.4,
            "BurnSpeedMultiplier": 1.43,
            "MaxOrdersOnScreenOffset": -2,
            "ChoppingTimeScale": 1.4,
            "BackpackMovementScale": 0.75,
            "RespawnTime": 10.0,
            "CarnivalDispenserRefactoryTime": 4.0,
            "LevelUnlockRequirements": level_unlock_requirements,
            "LockedEmotes": [0, 1, 2, 3, 4, 5],
            "StarOffset": 0,
            "AggressiveHorde": True,
            "DisableEarnHordeMoney": True,

            # Item Unlocking
            "OnLevelCompleted": on_level_completed,
        }

        # Set remaining data in the options dict
        bugs = ["FixDoubleServing", "FixSinkBug", "FixControlStickThrowBug", "FixEmptyBurnerThrow"]
        for bug in bugs:
            base_data[bug] = self.options.fix_bugs.result
        base_data["PreserveCookingProgress"] = self.options.always_preserve_cooking_progress.result
        base_data["TimerAlwaysStarts"] = self.options.prep_levels == PrepLevelMode.ayce
        base_data["LevelTimerScale"] = 0.666 if self.options.shorter_level_duration else 1.0
        base_data["LeaderboardScoreScale"] = {
            "FourStars": 1.0,
            "ThreeStars": star_threshold_scale,
            "TwoStars": star_threshold_scale * 0.75,
            "OneStar": star_threshold_scale * 0.35,
        }
        base_data["AlwaysServeOldestOrder"] = self.options.always_serve_oldest_order.result

        return base_data

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.fill_json_data()

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if not self.options.shuffle_level_order:
            return

        world: Overcooked2World = self
        spoiler_handle.write(f"\n\n{self.player_name}'s Level Order:\n\n")
        for overworld_id in world.level_mapping:
            overworld_name = Overcooked2GenericLevel(overworld_id).shortname.split("Story ")[1]
            kitchen_name = world.level_mapping[overworld_id].shortname
            spoiler_handle.write(f'{overworld_name} | {kitchen_name}\n')


def level_unlock_requirement_factory(stars_to_win: int) -> Dict[int, int]:
    level_unlock_counts = dict()
    level = 1
    sublevel = 1
    for n in range(1, 37):
        progress: float = float(n)/36.0
        progress *= progress  # x^2 curve

        star_count = int(progress*float(stars_to_win))
        min = (n-1)*3
        if (star_count > min):
            star_count = min

        level_id = (level-1)*6 + sublevel

        # print("%d-%d (%d) = %d" % (level, sublevel, level_id, star_count))

        level_unlock_counts[level_id] = star_count

        level += 1
        if level > 6:
            level = 1
            sublevel += 1

    # force sphere 1 to 0 stars to help keep our promises to the item fill algo
    level_unlock_counts[1] = 0  # 1-1
    level_unlock_counts[7] = 0  # 2-1
    level_unlock_counts[19] = 0  # 4-1

    # Force 5-1 into sphere 1 to help things out
    level_unlock_counts[25] = 1  # 5-1

    for n in range(37, 46):
        level_unlock_counts[n] = 0

    return level_unlock_counts
