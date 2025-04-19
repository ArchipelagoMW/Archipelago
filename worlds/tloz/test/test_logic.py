import typing

from BaseClasses import ItemClassification
from . import TLOZTestBase
from .. import Locations

class LogicTestBase(TLOZTestBase):
    boss_events = ["Boss 1 Defeated", "Boss 2 Defeated", "Boss 3 Defeated", "Boss 4 Defeated",
                   "Boss 5 Defeated", "Boss 6 Defeated", "Boss 7 Defeated", "Boss 8 Defeated", "Boss 9 Defeated"]
    supplementary_items = [*boss_events, "Candle", "Red Candle", "Raft", "Stepladder", "Recorder", "Bow", "Arrow",
                           "Silver Arrow"]

class WeaponLogicEasyTest(LogicTestBase):
    options = {
        "WeaponLogic": "easy",
        "DefenseLogic": "hard",
        "ExpandedPool": "true",
        "StartingPosition": "very_dangerous",
    }

    def test_sword(self) -> None:
        """Test the locations that will require the Sword: all dungeon locations"""
        locations = Locations.all_level_locations
        items = [["Sword", "White Sword", "Magical Sword", *LogicTestBase.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_white_sword(self) -> None:
        """Test the locations that will require the White Sword: all levels 4+"""

        locations = [*Locations.level_locations[3], *Locations.level_locations[4], *Locations.level_locations[5],
                     *Locations.level_locations[6], *Locations.level_locations[7], *Locations.level_locations[8], ]
        items = [["White Sword", "Magical Sword", *LogicTestBase.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_magical_sword(self) -> None:
        """Test the locations that will require the Magical Sword: levels 6, 8, and 9"""

        locations = [*Locations.level_locations[5], *Locations.level_locations[7], *Locations.level_locations[8], ]
        items = [["Magical Sword", *LogicTestBase.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

class WeaponLogicModerateTest(LogicTestBase):
    options = {
        "WeaponLogic": "moderate",
        "DefenseLogic": "hard",
        "ExpandedPool": "true",
        "StartingPosition": "very_dangerous"
    }

    def test_sword(self) -> None:
        """Test the locations that will require the Sword: all dungeon locations"""
        locations = Locations.all_level_locations
        items = [["Sword", "White Sword", "Magical Sword", *LogicTestBase.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_white_sword(self) -> None:
        """Test the locations that will require the White Sword: all levels 4+"""
        locations = [*Locations.level_locations[3], *Locations.level_locations[4], *Locations.level_locations[5],
                     *Locations.level_locations[6], *Locations.level_locations[7], *Locations.level_locations[8], ]
        items = [["White Sword", "Magical Sword", *LogicTestBase.supplementary_items],
                 ["Magical Rod", "Magical Sword", *LogicTestBase.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

class DefenseLogicEasyTest(LogicTestBase):
    options = {
        "WeaponLogic": "hard",
        "DefenseLogic": "easy",
        "ExpandedPool": "true",
        "StartingPosition": "very_dangerous"
    }

    def test_hearts_needed(self):
        items_held = [[*LogicTestBase.supplementary_items, "Heart Container", "Heart Container", "Heart Container"]]
        for level in Locations.level_locations:
            locations = [*level]
            self.assertAccessDependency(locations, items_held, only_check_listed=True)
            items_held[0].append("Heart Container")