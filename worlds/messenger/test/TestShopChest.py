from BaseClasses import ItemClassification, CollectionState
from . import MessengerTestBase
from .. import PowerSeals


class NoLogicTest(MessengerTestBase):
    options = {
        "enable_logic": "false",
        "goal": "power_seal_hunt",
    }

    def testChestAccess(self):
        """Test to make sure we can win even though we can't reach the chest."""
        self.assertEqual(self.can_reach_location("Shop Chest"), False)
        self.assertBeatable(True)


class AllSealsRequired(MessengerTestBase):
    options = {
        "shuffle_seals": "false",
        "goal": "power_seal_hunt",
    }

    def testSealsShuffled(self):
        """Shuffle seals should be forced on when shop chest is the goal so test it."""
        self.assertTrue(self.multiworld.shuffle_seals[1])

    def testChestAccess(self):
        """Defaults to a total of 45 power seals in the pool and required."""
        with self.subTest("Access Dependency"):
            self.assertEqual(len([seal for seal in self.multiworld.itempool if seal.name == "Power Seal"])
                             , self.multiworld.total_seals[1])
            locations = ["Shop Chest"]
            items = [["Power Seal"]]
            self.assertAccessDependency(locations, items)
            self.multiworld.state = CollectionState(self.multiworld)

        self.assertEqual(self.can_reach_location("Shop Chest"), False)
        self.assertBeatable(False)
        self.collect_all_but(["Power Seal", "Shop Chest", "Rescue Phantom"])
        self.assertEqual(self.can_reach_location("Shop Chest"), False)
        self.assertBeatable(False)
        self.collect_by_name("Power Seal")
        self.assertEqual(self.can_reach_location("Shop Chest"), True)
        self.assertBeatable(True)


class HalfSealsRequired(MessengerTestBase):
    options = {
        "goal": "power_seal_hunt",
        "percent_seals_required": 50,
    }

    def testSealsAmount(self):
        """Should have 45 power seals in the item pool and half that required"""
        self.assertEqual(self.multiworld.total_seals[1], 45)
        self.assertEqual(self.multiworld.worlds[1].total_seals, 45)
        self.assertEqual(self.multiworld.worlds[1].required_seals, 22)
        total_seals = [seal for seal in self.multiworld.itempool if seal.name == "Power Seal"]
        required_seals = [seal for seal in total_seals if seal.classification == ItemClassification.progression_skip_balancing]
        self.assertEqual(len(total_seals), 45)
        self.assertEqual(len(required_seals), 22)


class ThirtyThirtySeals(MessengerTestBase):
    options = {
        "goal": "power_seal_hunt",
        "total_seals": 30,
        "percent_seals_required": 34,
    }

    def testSealsAmount(self):
        """Should have 30 power seals in the pool and 33 percent of that required."""
        self.assertEqual(self.multiworld.total_seals[1], 30)
        self.assertEqual(self.multiworld.worlds[1].total_seals, 30)
        self.assertEqual(self.multiworld.worlds[1].required_seals, 10)
        total_seals = [seal for seal in self.multiworld.itempool if seal.name == "Power Seal"]
        required_seals = [seal for seal in total_seals if seal.classification == ItemClassification.progression_skip_balancing]
        self.assertEqual(len(total_seals), 30)
        self.assertEqual(len(required_seals), 10)
