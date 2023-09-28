from . import TunicTestBase


class TestAccess(TunicTestBase):
    def test_temple_access(self):
        # test whether you can get into the temple without laurels
        self.collect_all_but(["Hero's Laurels", "Lantern"])
        self.assertEqual(self.can_reach_location("Sealed Temple - Page Pickup"), False)
        self.collect_by_name(["Lantern"])
        self.assertEqual(self.can_reach_location("Sealed Temple - Page Pickup"), True)

    def test_wells(self):
        # test whether you can get into the temple without laurels
        locations = ["Coins in the Well - 3 Coins", "Coins in the Well - 6 Coins", "Coins in the Well - 10 Coins",
                     "Coins in the Well - 15 Coins"]
        items = [["Golden Coin"]]
        self.assertAccessDependency(locations, items)


class TestHexQuest(TunicTestBase):
    options = {"hexagon_quest": "true"}

    def test_hexquest_victory(self):
        location = ["The Heir"]
        item = [["Gold Questagon"]]
        self.assertAccessDependency(location, item)


class TestNormalGoal(TunicTestBase):
    options = {"hexagon_quest": "false"}

    def test_normal_goal(self):
        location = ["The Heir"]
        items = [["Red Questagon", "Blue Questagon", "Green Questagon"]]
        self.assertAccessDependency(location, items)
