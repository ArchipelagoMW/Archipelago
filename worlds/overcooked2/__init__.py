import os
import json

from typing import Callable

from BaseClasses import MultiWorld, ItemClassification, CollectionState, Region, Entrance, Location, RegionType
from ..AutoWorld import World, WebWorld

from .Overcooked2Levels import Overcooked2Level, Overcooked2GameWorld, Overcooked2GenericLevel, level_shuffle_factory
from .Locations import Overcooked2Location, location_name_to_id
from .Options import overcooked_options
from .Items import item_table, is_progression, Overcooked2Item, item_name_to_id, item_id_to_name
from .Locations import location_id_to_name, location_name_to_id
from .Logic import has_requirements_for_level_star


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

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

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

    def connect_regions(self, source: str, target: str, rule: Callable[[CollectionState], bool] | None = None):
        sourceRegion = self.world.get_region(source, self.player)
        targetRegion = self.world.get_region(target, self.player)

        connection = Entrance(self.player, '', sourceRegion)
        if rule is not None:
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
        completion_condition: Callable[[CollectionState], bool] = lambda state: \
            has_requirements_for_level_star(state, self.level_mapping[level_id], stars)

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
        location.access_rule = completion_condition

        region.locations.append(
            location
        )

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
    level_mapping: dict[int, Overcooked2GenericLevel]  # level_id, level

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
        # the further the game has progressed, and levels progress radially rather than linearly
        self.level_unlock_counts = level_unlock_requirement_factory(self.stars_to_win)

        # Assign new kitchens to each spot on the overworld using pure random chance and nothing else
        self.level_mapping = level_shuffle_factory(self.world.random)

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
            level_access_rule: Callable[[CollectionState], bool] = lambda state: \
                state.has("Star", self.player, self.level_unlock_counts[level.level_id()])
            self.connect_regions("Overworld", level_name, level_access_rule)

            # Level --> Overworld
            self.connect_regions(level_name, "Overworld")

        completion_condition: Callable[[CollectionState], bool] = lambda state: \
            state.can_reach(
                self.world.get_location(
                    "6-6 Completed",
                    self.player,
                )
        )
        self.world.completion_condition[self.player] = completion_condition

    def create_items(self):
        # Add Items
        self.world.itempool += [self.create_item(item_name)
                                for item_name in item_table]

    def set_rules(self):
        pass

    def generate_basic(self) -> None:
        # Add Events (Star Acquisition)
        for level in Overcooked2Level():
            for n in [1, 2, 3]:
                self.place_event(level.location_name_star_event(n), "Star")

    # Items get distributed to locations

    def generate_output(self, output_directory: str) -> None:
        mod_name = f"AP-{self.world.seed_name}-P{self.player}-{self.world.player_name[self.player]}"

        # Serialize Level Order
        story_level_order = dict()

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

        # Put it all together

        data = {
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
            "LevelForceReveal": [
                1,   # 1-1
                7,   # 2-1
                13,  # 3-1
                19,  # 4-1
                25,  # 5-1
                31,  # 6-1
            ],
            "SaveFolderName": mod_name,

            # Quality of Life
            "DisplayLeaderboardScores": self.display_leaderboard_scores,
            "AlwaysServeOldestOrder": self.display_leaderboard_scores,
            "PreserveCookingProgress": self.always_preserve_cooking_progress,
            "FixDoubleServing": self.fix_bugs,
            "FixSinkBug": self.fix_bugs,
            "FixControlStickThrowBug": self.fix_bugs,
            "FixEmptyBurnerThrow": self.fix_bugs,
            "TimerAlwaysStarts": self.always_preserve_cooking_progress,

            # Game Modifications
            "LevelPurchaseRequirements": level_purchase_requirements,
            "LeaderboardScoreScale": {
                "FourStars": 1.0,
                "ThreeStars": self.star_threshold_scale,
                "TwoStars": self.star_threshold_scale*0.666,
                "OneStar": self.star_threshold_scale*0.25
            },
            "Custom66TimerScale": 0.6,

            "CustomLevelOrder": custom_level_order,

            # Items (Starting Inventory)
            "CustomOrderLifetime": 66.6,  # 2/3rd of original
            "DisableWood": True,
            "DisableCoal": True,
            "DisableOnePlate": True,
            "DisableFireExtinguisher": True,
            "DisableBellows": True,
            "PlatesStartDirty": True,
            "MaxTipCombo": 2,
            "DisableDash": True,
            "DisableThrow": True,
            "DisableCatch": True,
            "DisableControlStick": True,
            "DisableWokDrag": True,
            "WashTimeMultiplier": 0.666,
            "BurnSpeedMultiplier": 1.75,
            "MaxOrdersOnScreenOffset": -2,
            "ChoppingTimeScale": 0.666,
            "BackpackMovementScale": 0.666,
            "RespawnTime": 10.0,
            "CarnivalDispenserRefactoryTime": 3.0,
            # "LevelUnlockRequirements": { # TODO
            #     "37": 1,
            #     "38": 2,
            #     "39": 4,
            #     "40": 1,
            #     "41": 2,
            #     "42": 3,
            #     "43": 3,
            #     "44": 3
            # },
        }

        # Save to disk

        filepath = os.path.join(output_directory, mod_name + ".json")
        with open(filepath, "w") as file:
            json.dump(data, file)


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
