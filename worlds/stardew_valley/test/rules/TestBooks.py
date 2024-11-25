from ... import options
from ...test import SVTestBase


class TestBooksLogic(SVTestBase):
    options = {
        options.Booksanity.internal_name: options.Booksanity.option_all,
    }

    def test_can_get_mapping_cave_systems_with_weapon_and_time(self):
        self.collect_months(12)
        self.assert_location_cannot_be_reached("Read Mapping Cave Systems")

        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.assert_location_cannot_be_reached("Read Mapping Cave Systems")

        self.collect("Progressive Weapon")
        self.assert_location_can_be_reached("Read Mapping Cave Systems")

    def test_can_get_mapping_cave_systems_with_money(self):
        self.collect_lots_of_money(0.5)
        self.assert_location_can_be_reached("Read Mapping Cave Systems")
