from ... import options
from ...test import SVTestBase


class TestBooksLogic(SVTestBase):
    options = {
        options.Booksanity.internal_name: options.Booksanity.option_all,
    }

    def test_need_weapon_for_mapping_cave_systems(self):
        self.collect_lots_of_money(0.5)

        location = self.multiworld.get_location("Read Mapping Cave Systems", self.player)

        self.assert_cannot_reach_location(location, self.multiworld.state)

        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.assert_cannot_reach_location(location, self.multiworld.state)

        self.collect("Progressive Weapon")
        self.assert_can_reach_location(location, self.multiworld.state)
