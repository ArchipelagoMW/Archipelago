from ... import options
from ...test import SVTestBase


class TestBooksLogic(SVTestBase):
    options = {
        options.Booksanity.internal_name: options.Booksanity.option_all,
    }

    def test_need_weapon_for_mapping_cave_systems(self):
        self.collect_all_the_money()

        location = self.multiworld.get_location("Read Mapping Cave Systems", self.player)

        self.assert_reach_location_false(location, self.multiworld.state)

        self.collect("Progressive Weapon")

        self.assert_reach_location_true(location, self.multiworld.state)


