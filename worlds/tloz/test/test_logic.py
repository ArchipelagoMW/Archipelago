from BaseClasses import ItemClassification
from . import TLOZTestBase
from .. import Locations

class WeaponLogicEasyTest(TLOZTestBase):
    options = {
        "weapon_logic": "easy",
        "expanded_pool": "true"
    }
    boss_events = ["Boss 1 Defeated", "Boss 2 Defeated", "Boss 3 Defeated", "Boss 4 Defeated",
                   "Boss 5 Defeated", "Boss 6 Defeated", "Boss 7 Defeated", "Boss 8 Defeated", "Boss 9 Defeated", ]
    supplementary_items = [*boss_events, "Candle", "Red Candle", "Raft", "Stepladder", "Recorder", "Bow", "Arrow", "Silver Arrow"]

    def test_sword(self) -> None:
        """Test the locations that will require the Sword: all dungeon locations"""
        locations = Locations.all_level_locations
        items = [["Sword", "White Sword", "Magical Sword", *WeaponLogicEasyTest.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_white_sword(self) -> None:
        """Test the locations that will require the White Sword: all levels 4+"""

        locations = [*Locations.level_locations[3], *Locations.level_locations[4], *Locations.level_locations[5],
                     *Locations.level_locations[6], *Locations.level_locations[7], *Locations.level_locations[8], ]
        items = [["White Sword", *WeaponLogicEasyTest.supplementary_items], ["Magical Sword", *WeaponLogicEasyTest.supplementary_items]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_magical_sword(self) -> None:
        """Test the locations that will require the Magical Sword: levels 6, 8, and 9"""

        locations = [*Locations.level_locations[5], *Locations.level_locations[7], *Locations.level_locations[8], ]
        items = [["Magical Sword"]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

class WeaponLogicModerateTest(TLOZTestBase):
    options = {
        "weapon_logic": "moderate",
        "expanded_pool": "true"
    }

    def test_sword(self) -> None:
        """Test the locations that will require the Sword: all dungeon locations"""
        locations = Locations.all_level_locations
        items = [["Sword"], ["White Sword"], ["Magical Sword"]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_white_sword_or_magical_rod(self) -> None:
        """Test the locations that will require the White Sword or Magical Rod: all levels 4+"""
        locations = [*Locations.level_locations[3], *Locations.level_locations[4], *Locations.level_locations[5],
                     *Locations.level_locations[6], *Locations.level_locations[7], *Locations.level_locations[8], ]
        items = [["White Sword"], ["Magical Sword"], ["Magical Rod"]]
        self.assertAccessDependency(locations, items, only_check_listed=True)
