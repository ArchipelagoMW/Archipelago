from ... import options
from ...test import SVTestBase


class TestBooksLogic(SVTestBase):
    options = {
        options.Booksanity.internal_name: options.Booksanity.option_all,
    }

    def test_need_weapon_for_mapping_cave_systems(self):
        self.collect_lots_of_money(0.5)

        self.assert_location_cannot_be_reached("Read Mapping Cave Systems")

        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.assert_location_cannot_be_reached("Read Mapping Cave Systems")

        self.collect("Progressive Weapon")
        self.assert_location_can_be_reached("Read Mapping Cave Systems")
