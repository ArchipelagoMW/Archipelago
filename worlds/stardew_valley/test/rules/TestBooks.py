from ..bases import SVTestBase
from ... import options


class TestBooksLogic(SVTestBase):
    options = {
        options.Booksanity.internal_name: options.Booksanity.option_all,
    }

    def test_can_get_mapping_cave_systems_with_weapon_and_time(self):
        self.collect_lots_of_money(0.95)
        self.collect("Progressive Bookseller Days", 2)
        self.collect("Bookseller Stock: Progressive Rare Books", 2)
        self.assert_cannot_reach_location("Read Mapping Cave Systems")

        self.collect("Landslide Removed")
        self.collect("Progressive Pickaxe")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.collect("Progressive Mine Elevator")
        self.assert_cannot_reach_location("Read Mapping Cave Systems")

        self.collect("Progressive Weapon")
        self.assert_can_reach_location("Read Mapping Cave Systems")
