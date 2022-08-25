from .Items import is_progression  # this is just a dummy
from ..AutoWorld import World, WebWorld
from .Options import overcooked_options
from .Items import item_table, is_progression, Overcooked2Item
from .Locations import location_id_to_name, location_name_to_id
from BaseClasses import ItemClassification, CollectionState

from .Overcooked2Levels import Overcooked2Level, Overcooked2World
from .Locations import Overcooked2Location, location_name_to_id
from .Logic import Overcooked2Logic

import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType

from random import Random


from typing import Callable


class Overcooked2Web(WebWorld):
    pass


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
    remote_start_inventory: bool = True
    data_version = 0
    base_id = 0

    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id

    # Helper Functions

    def create_item(self, item: str):
        if is_progression(item):
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return Overcooked2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str) -> None:
        return Overcooked2Item(event, ItemClassification.progression_skip_balancing, None, self.player)

    def place_event(self,  location_name: str, item_name: str):
        location: Location = self.world.get_location(location_name)
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

    def connect_regions(self, source: str, target: str, rule: Callable[[CollectionState], bool] | None = None):
        sourceRegion = self.world.get_region(source, self.player)
        targetRegion = self.world.get_region(target, self.player)

        connection = Entrance(self.player, '', sourceRegion)
        if rule is not None:
            connection.access_rule = rule

        sourceRegion.exits.append(connection)
        connection.connect(targetRegion)

    def add_location(
            self, region_name: str, location_name: str, rule: Callable[[CollectionState],
                                                                       bool] | None = None) -> None:
        location = Overcooked2Location(
            self.player,
            location_name,
            self.location_name_to_id[location_name],
            region,
        )

        if rule is not None:
            location.access_rule = rule

        region = self.world.get_region(region_name, self.player)
        region.locations.append(
            location
        )

    def set_location_rule(self, location_name: str, rule):
        location = self.world.get_location(location_name, self.player)
        location.access_rule = rule

    def set_entrance_rule(self, entrance_name: str, rule):
        entrance = self.world.get_entrance(entrance_name, self.player)
        entrance.access_rule = rule

    def can_enter_level(self, state: CollectionState, level_name: str) -> bool:
        return False

    def can_earn_level_star(self, state: CollectionState, level_name: str) -> bool:
        return False

    # YAML Config

    always_serve_oldest_order: bool
    always_preserve_cooking_progress: bool
    always_start_level_timer: bool
    display_leaderboard_scores: bool
    shuffle_level_order: bool
    fix_bugs: bool
    stars_to_win: int
    star_threshold_scale: float

    # Helper Data

    level_unlock_counts: dict[int, int]  # level_id, stars to purchase

    # Autoworld Hooks

    def generate_early(self):
        self.always_serve_oldest_order = self.world.AlwaysServerOldestOrder[self.player].value
        self.always_preserve_cooking_progress = self.world.AlwaysPreserveCookingProgress[self.player].value
        self.always_start_level_timer = self.world.AlwaysStartLevelTimer[self.player].value
        self.display_leaderboard_scores = self.world.DisplayLeaderboardScores[self.player].value
        self.shuffle_level_order = self.world.ShuffleLevelOrder[self.player].value
        self.fix_bugs = self.world.FixBugs[self.player].value
        self.stars_to_win = self.world.StarsToWin[self.player].value

        # 0.0 to 1.0 where 1.0 is World Record
        self.star_threshold_scale = 100.0 / float(self.world.StarThresholdScale[self.player].value)

        # Generate level unlock requirements such that the levels get harder to unlock
        # the further the game has progressed, and levels progress radially rather
        # than linearly
        level_unlock_counts = dict()
        level = 1
        sublevel = 1
        for n in range(1, 37):
            progress: float = float(n)/36.0
            progress *= progress  # x^2 curve

            star_count = int(progress*float(self.stars_to_win))
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
        
        

    # After this step all regions and items have to be in the MultiWorld's regions and itempool.

    def generate_basic(self) -> None:
        # Add Items
        self.world.itempool += [self.create_item(item_name)
                                for item_name in item_table]

        # Add Events (Star Acquisition)
        for level in Overcooked2Level():
            self.place_event(level.location_name_one_star(), "Star")
            self.place_event(level.location_name_two_star(), "Star")
            self.place_event(level.location_name_three_star(), "Star")

    def generate_regions(self) -> None:
        # Menu -> Overworld
        self.add_region("Menu")
        self.add_region("Overworld")
        self.connect_regions("Menu", "Overworld")

        for level in Overcooked2Level():
            level_name = level.level_name()

            # Create Region (e.g. "1-1")
            self.add_region(level_name)

            # Add Locations to store events
            # TODO: Access Rules
            self.add_location(
                level_name,
                level.location_name_one_star(),
            )
            self.add_location(
                level_name,
                level.location_name_two_star(),
            )
            self.add_location(
                level_name,
                level.location_name_three_star(),
            )

            # Overworld -> Level
            level_access_rule: Callable[[CollectionState], bool] = lambda state: \
                state.has("Star", self.player, self.level_unlock_counts[level.level_id()])
            self.connect_regions("Overworld", level_name, level_access_rule)

            # Level --> Overworld
            self.connect_regions(level_name, "Overworld")

        completion_condition: Callable[[CollectionState], bool] = lambda state: \
            state.can_reach(
                self.world.get_location(
                    Overcooked2Level(Overcooked2World.SIX, 6).location_name_one_star(),
                    self.player
                )
        )
        self.world.completion_condition[self.player] = completion_condition

    def generate_output(self, output_directory: str) -> None:
        data = {
            # Implicit to rando
            "DisableAllMods": False,
            "UnlockAllChefs": True,
            "UnlockAllDLC": True,
            "DisplayFPS": True,
            "SkipTutorialPopups": True,

            # Quality of Life
            "DisplayLeaderboardScores": self.display_leaderboard_scores,
            "AlwaysServeOldestOrder": self.display_leaderboard_scores,
            "PreserveCookingProgress": self.always_preserve_cooking_progress,
            "FixDoubleServing": self.fix_bugs,
            "FixSinkBug": self.fix_bugs,
            "FixControlStickThrowBug": self.fix_bugs,
            "FixEmptyBurnerThrow": self.fix_bugs,
            "TimerAlwaysStarts": self.always_preserve_cooking_progress,
            "RevealAllLevels": True,
            "PurchaseAllLevels": True,
            "SkipTutorial": True,
            "CheatsEnabled": True,
            "CustomOrderLifetime": 66.0,
            "LevelUnlockRequirements": {
                "37": 1,
                "38": 2,
                "39": 4,
                "40": 6,
                "41": 2
            },
            "LevelPurchaseRequirements": {
                "38": 5,
                "1": 1
            },
            "LeaderboardScoreScale": {
                "FourStars": 0.01,
                "ThreeStars": 0.01,
                "TwoStars": 0.01,
                "OneStar": 0.01
            },
            "Custom66TimerScale": 1.0,
            "CustomLevelOrder": {
                "Story": {
                    "1": {
                        "DLC": "Campfire Cook Off",
                        "LevelID": 0
                    },
                    "2": {
                        "DLC": "Story",
                        "LevelID": 1
                    },
                    "3": {
                        "DLC": "Campfire Cook Off",
                        "LevelID": 5
                    },
                    "4": {
                        "DLC": "Seasonal",
                        "LevelID": 30
                    },
                    "5": {
                        "DLC": "Campfire Cook Off",
                        "LevelID": 6
                    },
                    "6": {
                        "DLC": "Campfire Cook Off",
                        "LevelID": 7
                    }
                }
            },
            "LevelForceReveal": [36, 37, 38, 40],
            "DisableWood": False,
            "DisableCoal": True,
            "DisableOnePlate": True,
            "DisableFireExtinguisher": True,
            "DisableBellows": True,
            "PlatesStartDirty": True,
            "MaxTipCombo": 3,
            "DisableDash": False,
            "DisableThrow": True,
            "DisableCatch": True,
            "DisableControlStick": True,
            "DisableWokDrag": True,
            "SkipAllOnionKing": True,
            "WashTimeMultiplier": 2.5,
            "BurnSpeedMultiplier": 4.0,
            "MaxOrdersOnScreenOffset": -2,
            "ChoppingTimeScale": 0.5,
            "BackpackMovementScale": 0.666,
            "RespawnTime": 10.0,
            "CarnivalDispenserRefactoryTime": 4.0,
            "SaveFolderName": "test_save_dir"
        }
