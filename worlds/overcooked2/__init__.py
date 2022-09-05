import os
import json

from enum import Enum
from typing import Callable, Dict, Any, List, Optional

from BaseClasses import ItemClassification, CollectionState, Region, Entrance, Location, RegionType, Tutorial
from worlds.AutoWorld import World, WebWorld

from .Overcooked2Levels import Overcooked2Level, Overcooked2GenericLevel, level_shuffle_factory
from .Locations import Overcooked2Location, oc2_location_name_to_id, oc2_location_id_to_name
from .Options import overcooked_options, OC2Options, OC2OnToggle
from .Items import item_table, is_progression, Overcooked2Item, item_name_to_id, item_id_to_name, item_to_unlock_event, item_frequencies
from .Logic import has_requirements_for_level_star, has_requirements_for_level_access


class Overcooked2Web(WebWorld):
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
    Overcooked! 2 is a franticly paced cooking arcade game where
    players race against the clock to complete orders for points. Bring
    peace to the Onion Kingdom once again by recovering lost items and abilities,
    earning stars to unlock levels, and defeating the unbread horde. Levels are
    randomized to increase gameplay variety. Best enjoyed with a friend or three.
    """

    # Autoworld API

    game = "Overcooked! 2"
    web = Overcooked2Web()
    option_definitions = overcooked_options
    topology_present: bool = False
    remote_items: bool = True
    remote_start_inventory: bool = False
    data_version = 0
    base_id = 0

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = oc2_location_id_to_name
    location_name_to_id = oc2_location_name_to_id

    options: Dict[str, Any]
    itempool: List[Overcooked2Item]

    def __init__(self, *args):
        super().__init__(*args)
        self.itempool = []
    # Helper Functions

    def create_item(self, item: str) -> Overcooked2Item:
        if is_progression(item):
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return Overcooked2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str) -> Overcooked2Item:
        return Overcooked2Item(event, ItemClassification.progression_skip_balancing, None, self.player)

    def place_event(self,  location_name: str, item_name: str):
        location: Location = self.world.get_location(location_name, self.player)
        location.place_locked_item(self.create_event(item_name))

    def add_region(self, region_name: str):
        region = Region(
            region_name,
            RegionType.Generic,
            region_name,
            self.player,
            self.world,
        )
        self.world.regions.append(region)

    def connect_regions(self, source: str, target: str, rule: Optional[Callable[[CollectionState], bool]] = None):
        sourceRegion = self.world.get_region(source, self.player)
        targetRegion = self.world.get_region(target, self.player)

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

        region = self.world.get_region(region_name, self.player)
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
        return OC2Options({option.__name__: getattr(self.world, name)[self.player].result
                          if issubclass(option, OC2OnToggle) else getattr(self.world, name)[self.player].value
                           for name, option in overcooked_options.items()})

    # Helper Data

    level_unlock_counts: dict[int, int]  # level_id, stars to purchase
    level_mapping: dict[int, Overcooked2GenericLevel]  # level_id, level

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
                level_shuffle_factory(self.world.random, self.options["PrepLevels"] != PrepLevelMode.excluded)
        else:
            self.level_mapping = None

    def create_regions(self) -> None:
        # Menu -> Overworld
        self.add_region("Menu")
        self.add_region("Overworld")
        self.connect_regions("Menu", "Overworld")

        for level in Overcooked2Level():
            level_name = level.level_name()

            # Create Region (e.g. "1-1")
            self.add_region(level_name)

            # Add Location to house progression item (1-star)
            # 6-6 doesn't either, but it does have victory condition which is placed later
            if level.level_id() == 36:
                self.add_level_location(
                    level_name,
                    level.location_name_completed(),
                    None,
                    1,
                )
            else:
                self.add_level_location(
                    level_name,
                    level.location_name_completed(),
                    level.level_id(),
                    1,
                )

            # Add Locations to house star aquisition events
            for n in [1, 2, 3]:
                self.add_level_location(
                    level_name,
                    level.location_name_star_event(n),
                    level.level_id(),
                    n,
                    is_event=True,
                )

            # Overworld -> Level
            required_star_count: int = self.level_unlock_counts[level.level_id()]
            if level.level_id() % 6 != 1:
                previous_level_name: str = Overcooked2GenericLevel(level.level_id()-1).shortname().split(" ")[1]
            else:
                previous_level_name = None

            level_access_rule: Callable[[CollectionState], bool] = \
                lambda state, level_name=level_name, previous_level_name=previous_level_name, required_star_count=required_star_count: \
                has_requirements_for_level_access(state, level_name, previous_level_name, required_star_count, self.player)
            self.connect_regions("Overworld", level_name, level_access_rule)

            # Level --> Overworld
            self.connect_regions(level_name, "Overworld")

        completion_condition: Callable[[CollectionState], bool] = lambda state: \
            state.has("Victory", self.player)
        self.world.completion_condition[self.player] = completion_condition

    def create_items(self):
        # Make Items with multiple instances
        for item_name in item_frequencies:
            freq = item_frequencies[item_name]
            self.itempool += [self.create_item(item_name) for _ in range(freq)]

        # Make Items with one instance
        for item_name in item_table:
            if item_name not in item_frequencies:
                self.itempool.append(self.create_item(item_name))

        # Fill any free space with filler
        while len(self.itempool) < len(oc2_location_name_to_id):
            self.itempool.append(self.create_item("Bonus Star"))

        self.world.itempool += self.itempool

    def set_rules(self):
        pass

    def generate_basic(self) -> None:
        # Add Events (Star Acquisition)
        for level in Overcooked2Level():
            for n in [1, 2, 3]:
                self.place_event(level.location_name_star_event(n), "Star")
        
        # Add Victory Condition
        self.place_event("6-6 Completed", "Victory")

    # Items get distributed to locations

    def generate_output(self, output_directory: str) -> None:
        if self.world.players != 1:
            return

        mod_name = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}"
        data = self.fill_json_data()
        # Save to disk

        filepath = os.path.join(output_directory, mod_name + ".oc2.json")
        with open(filepath, "w") as file:
            json.dump(data, file)

    def fill_json_data(self) -> Dict[str, Any]:
        mod_name = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}"

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
        def kevin_level_to_keyholder_level_id(level_id: int) -> Optional[int]:
            location = self.world.find_item(f"Kevin-{level_id-36}", self.player)
            if location.player != self.player:
                return None  # This kevin level will be unlocked by the server at runtime
            level_id = oc2_location_name_to_id[location.name]
            return level_id
        for level_id in range(37, 45):
            keyholder_level_id = kevin_level_to_keyholder_level_id(level_id)
            if keyholder_level_id is not None:
                level_unlock_requirements[str(level_id)] = keyholder_level_id

        # Place Items at Level Completion Screens (local only)
        on_level_completed: dict[str, list[dict[str, str]]] = dict()
        regions = self.world.get_regions(self.player)
        for region in regions:
            for location in region.locations:
                if location.item is None:
                    continue
                if location.item.code is None:
                    continue # it's an event
                if location.item.player != self.player:
                    continue # not for us
                level_id = str(oc2_location_name_to_id[location.name])
                on_level_completed[level_id] = [item_to_unlock_event(location.item.name)]

        # Put it all together

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
            "CheatsEnabled": True,  # TODO: off for release
            "ImpossibleTutorial": True,
            "LevelForceReveal": level_force_reveal,
            "SaveFolderName": mod_name,

            # Game Modifications
            "LevelPurchaseRequirements": level_purchase_requirements,
            "Custom66TimerScale": 0.5,

            "CustomLevelOrder": custom_level_order,

            # Items (Starting Inventory)
            "CustomOrderLifetime": 80.0,  # 100 seconds is original
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
            "WashTimeMultiplier": 1.5,
            "BurnSpeedMultiplier": 1.5,
            "MaxOrdersOnScreenOffset": -2,
            "ChoppingTimeScale": 1.4,
            "BackpackMovementScale": 0.7,
            "RespawnTime": 10.0,
            "CarnivalDispenserRefactoryTime": 4.0,
            "LevelUnlockRequirements": level_unlock_requirements,
            "LockedEmotes": [0, 1, 2, 3, 4, 5],
            "StarOffset": 0,

            # Item Unlocking
            "OnLevelCompleted": on_level_completed,
        }

        # Set remaining data in the options dict
        bugs = ["FixDoubleServing", "FixSinkBug", "FixControlStickThrowBug", "FixEmptyBurnerThrow"]
        for bug in bugs:
            self.options[bug] = self.options["FixBugs"]
        self.options["PreserveCookingProgress"] = self.options["AlwaysPreserveCookingProgress"]
        self.options["TimerAlwaysStarts"] = self.options["PrepLevels"] == PrepLevelMode.ayce
        self.options["LevelTimerScale"] = 0.666 if self.options["ShorterLevelDuration"] else 1.0
        star_threshold_scale = self.options["StarThresholdScale"] / 100
        self.options["LeaderboardScoreScale"] = {
            "FourStars": 1.0,
            "ThreeStars": star_threshold_scale,
            "TwoStars": star_threshold_scale * 0.8,
            "OneStar": star_threshold_scale * 0.4,
        }

        base_data.update(self.options)
        return base_data

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.fill_json_data()

def level_unlock_requirement_factory(stars_to_win: int) -> dict[int, int]:
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

    for n in range(37, 46):
        level_unlock_counts[n] = 0

    return level_unlock_counts
