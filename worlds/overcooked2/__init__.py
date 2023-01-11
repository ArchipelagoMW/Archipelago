from enum import Enum
from typing import Callable, Dict, Any, List, Optional

from BaseClasses import ItemClassification, CollectionState, Region, Entrance, Location, RegionType, Tutorial
from worlds.AutoWorld import World, WebWorld

from .Overcooked2Levels import Overcooked2Level, Overcooked2GenericLevel, ITEMS_TO_EXCLUDE_IF_NO_DLC
from .Locations import Overcooked2Location, oc2_location_name_to_id, oc2_location_id_to_name
from .Options import overcooked_options, OC2Options, OC2OnToggle
from .Items import item_table, Overcooked2Item, item_name_to_id, item_id_to_name, item_to_unlock_event, item_frequencies
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


class PrepLevelMode(Enum):
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
    required_client_version = (0, 3, 7)
    option_definitions = overcooked_options
    topology_present: bool = False
    data_version = 2

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = oc2_location_id_to_name
    location_name_to_id = oc2_location_name_to_id

    options: Dict[str, Any]
    itempool: List[Overcooked2Item]


    # Helper Functions

    def is_level_horde(self, level_id: int) -> bool:
        return self.options["IncludeHordeLevels"] and \
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
            RegionType.Generic,
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

    def get_options(self) -> Dict[str, Any]:
        return OC2Options({option.__name__: getattr(self.multiworld, name)[self.player].result
                          if issubclass(option, OC2OnToggle) else getattr(self.multiworld, name)[self.player].value
                           for name, option in overcooked_options.items()})

    # Helper Data

    level_unlock_counts: Dict[int, int]  # level_id, stars to purchase
    level_mapping: Dict[int, Overcooked2GenericLevel]  # level_id, level

    # Autoworld Hooks

    def generate_early(self):
        self.options = self.get_options()

        # 0.0 to 1.0 where 1.0 is World Record
        self.star_threshold_scale = self.options["StarThresholdScale"] / 100.0

        # Generate level unlock requirements such that the levels get harder to unlock
        # the further the game has progressed, and levels progress radially rather than linearly
        self.level_unlock_counts = level_unlock_requirement_factory(self.options["StarsToWin"])

        # Assign new kitchens to each spot on the overworld using pure random chance and nothing else
        if self.options["ShuffleLevelOrder"]:
            self.level_mapping = \
                level_shuffle_factory(
                    self.multiworld.random,
                    self.options["PrepLevels"] != PrepLevelMode.excluded.value,
                    self.options["IncludeHordeLevels"],
                )
        else:
            self.level_mapping = None

    def create_regions(self) -> None:
        # Menu -> Overworld
        self.add_region("Menu")
        self.add_region("Overworld")
        self.connect_regions("Menu", "Overworld")

        for level in Overcooked2Level():
            if not self.options["KevinLevels"] and level.level_id > 36:
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
                has_requirements_for_level_access(state, level_name, previous_level_completed_event_name, required_star_count, self.player)
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
            if not self.options["ShuffleLevelOrder"] and item_name in ITEMS_TO_EXCLUDE_IF_NO_DLC:
                # skip DLC items if no DLC
                continue

            if not self.options["IncludeHordeLevels"] and item_name in ["Calmer Unbread", "Coin Purse"]:
                # skip horde-specific items if no horde levels
                continue
            
            if not self.options["KevinLevels"] and item_name.startswith("Kevin"):
                # skip kevin items if no kevin levels
                continue

            if is_item_progression(item_name, self.level_mapping, self.options["KevinLevels"]):
                # print(f"{item_name} is progression")
                # progression.append(item_name)
                classification = ItemClassification.progression
            else:
                # print(f"{item_name} is filler")
                if (is_useful(item_name)):
                    # useful.append(item_name)
                    classification = ItemClassification.useful
                else:
                    # filler.append(item_name)
                    classification = ItemClassification.filler

            if item_name in item_frequencies:
                freq = item_frequencies[item_name]

                while freq > 0:
                    self.itempool.append(self.create_item(item_name, classification))
                    classification = ItemClassification.useful  # only the first progressive item can be progression
                    freq -= 1
            else:
                self.itempool.append(self.create_item(item_name, classification))

        # print(f"progression: {progression}")
        # print(f"useful: {useful}")
        # print(f"filler: {filler}")

        # Fill any free space with filler
        pool_count = len(oc2_location_name_to_id)
        if not self.options["KevinLevels"]:
            pool_count -= 8

        while len(self.itempool) < pool_count:
            self.itempool.append(self.create_item("Bonus Star", ItemClassification.useful))

        self.multiworld.itempool += self.itempool

    def set_rules(self):
        pass

    def generate_basic(self) -> None:
        # Add Events (Star Acquisition)
        for level in Overcooked2Level():
            if not self.options["KevinLevels"] and level.level_id > 36:
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

    # Items get distributed to locations

    def fill_json_data(self) -> Dict[str, Any]:
        mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.player_name[self.player]}"

        # Serialize Level Order
        story_level_order = dict()

        if self.options["ShuffleLevelOrder"]:
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
        if self.options["KevinLevels"]:
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
        star_threshold_scale = self.options["StarThresholdScale"] / 100

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

            # Game Modifications
            "LevelPurchaseRequirements": level_purchase_requirements,
            "Custom66TimerScale": max(0.4, 0.25 + (1.0 - star_threshold_scale)*0.6),
            "ShortHordeLevels": self.options["ShortHordeLevels"],
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
            "DisableRampButton": True,
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
            self.options[bug] = self.options["FixBugs"]
        self.options["PreserveCookingProgress"] = self.options["AlwaysPreserveCookingProgress"]
        self.options["TimerAlwaysStarts"] = self.options["PrepLevels"] == PrepLevelMode.ayce.value
        self.options["LevelTimerScale"] = 0.666 if self.options["ShorterLevelDuration"] else 1.0
        self.options["LeaderboardScoreScale"] = {
            "FourStars": 1.0,
            "ThreeStars": star_threshold_scale,
            "TwoStars": star_threshold_scale * 0.75,
            "OneStar": star_threshold_scale * 0.35,
        }

        base_data.update(self.options)
        return base_data

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.fill_json_data()


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
