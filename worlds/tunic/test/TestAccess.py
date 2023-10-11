from . import TunicTestBase
from .. import Options

class TestAccess(TunicTestBase):
    def test_temple_access(self):
        # test whether you can get into the temple without laurels
        self.collect_all_but(["Hero's Laurels", "Lantern"])
        self.assertFalse(self.can_reach_location("Sealed Temple - Page Pickup"))
        self.collect_by_name(["Lantern"])
        self.assertTrue(self.can_reach_location("Sealed Temple - Page Pickup"))

    def test_wells(self):
        # test that the wells function properly. Since fairies is written the same way, that should succeed too
        locations = ["Coins in the Well - 3 Coins", "Coins in the Well - 6 Coins", "Coins in the Well - 10 Coins",
                     "Coins in the Well - 15 Coins"]
        items = [["Golden Coin"]]
        self.assertAccessDependency(locations, items)


class TestHexQuest(TunicTestBase):
    options = {Options.HexagonQuest.internal_name: Options.HexagonQuest.option_true}

    # test that you need the gold hexes to reach the Heir in Hex Quest
    def test_hexquest_victory(self):
        location = ["The Heir"]
        item = [["Gold Questagon"]]
        self.assertAccessDependency(location, item)


class TestNormalGoal(TunicTestBase):
    options = {Options.HexagonQuest.internal_name: Options.HexagonQuest.option_false}

    # test that you need the three colored hexes to reach the Heir in standard
    def test_normal_goal(self):
        location = ["The Heir"]
        items = [["Red Questagon", "Blue Questagon", "Green Questagon"]]
        self.assertAccessDependency(location, items)
