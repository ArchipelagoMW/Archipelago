from ... import options
from ...test import SVTestBase


class TestBooksLogic(SVTestBase):
    options = {
        options.Booksanity.internal_name: options.Booksanity.option_all,
    }

    def test_can_get_mapping_cave_systems_with_weapon_and_time(self):
        self.collect_months(12)
        self.assert_cannot_reach_location("Read Mapping Cave Systems")

        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.assert_cannot_reach_location("Read Mapping Cave Systems")

        self.collect("Progressive Weapon")
        self.assert_can_reach_location("Read Mapping Cave Systems")
