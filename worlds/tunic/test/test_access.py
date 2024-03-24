from . import TunicTestBase
from .. import options


class TestAccess(TunicTestBase):
    # test whether you can get into the temple without laurels
    def test_temple_access(self):
        self.collect_all_but(["Hero's Laurels", "Lantern"])
        self.assertFalse(self.can_reach_location("Sealed Temple - Page Pickup"))
        self.collect_by_name(["Lantern"])
        self.assertTrue(self.can_reach_location("Sealed Temple - Page Pickup"))

    # test that the wells function properly. Since fairies is written the same way, that should succeed too
    def test_wells(self):
        self.collect_all_but(["Golden Coin"])
        self.assertFalse(self.can_reach_location("Coins in the Well - 3 Coins"))
        self.collect_by_name(["Golden Coin"])
        self.assertTrue(self.can_reach_location("Coins in the Well - 3 Coins"))


class TestStandardShuffle(TunicTestBase):
    options = {options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true}

    # test that you need to get holy cross to open the hc door in overworld
    def test_hc_door(self):
        self.assertFalse(self.can_reach_location("Fountain Cross Door - Page Pickup"))
        self.collect_by_name("Pages 42-43 (Holy Cross)")
        self.assertTrue(self.can_reach_location("Fountain Cross Door - Page Pickup"))


class TestHexQuestShuffle(TunicTestBase):
    options = {options.HexagonQuest.internal_name: options.HexagonQuest.option_true,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true}

    # test that you need the gold questagons to open the hc door in overworld
    def test_hc_door_hex_shuffle(self):
        self.assertFalse(self.can_reach_location("Fountain Cross Door - Page Pickup"))
        self.collect_by_name("Gold Questagon")
        self.assertTrue(self.can_reach_location("Fountain Cross Door - Page Pickup"))


class TestHexQuestNoShuffle(TunicTestBase):
    options = {options.HexagonQuest.internal_name: options.HexagonQuest.option_true,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_false}

    # test that you can get the item behind the overworld hc door with nothing and no ability shuffle
    def test_hc_door_no_shuffle(self):
        self.assertTrue(self.can_reach_location("Fountain Cross Door - Page Pickup"))


class TestNormalGoal(TunicTestBase):
    options = {options.HexagonQuest.internal_name: options.HexagonQuest.option_false}

    # test that you need the three colored hexes to reach the Heir in standard
    def test_normal_goal(self):
        location = ["The Heir"]
        items = [["Red Questagon", "Blue Questagon", "Green Questagon"]]
        self.assertAccessDependency(location, items)


class TestER(TunicTestBase):
    options = {options.EntranceRando.internal_name: options.EntranceRando.option_yes,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true,
               options.HexagonQuest.internal_name: options.HexagonQuest.option_false}

    def test_overworld_hc_chest(self):
        # test to see that static connections are working properly -- this chest requires holy cross and is in Overworld
        self.assertFalse(self.can_reach_location("Overworld - [Southwest] Flowers Holy Cross"))
        self.collect_by_name(["Pages 42-43 (Holy Cross)"])
        self.assertTrue(self.can_reach_location("Overworld - [Southwest] Flowers Holy Cross"))
