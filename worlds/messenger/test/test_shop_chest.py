from BaseClasses import ItemClassification, CollectionState
from . import MessengerTestBase


class AllSealsRequired(MessengerTestBase):
    options = {
        "shuffle_seals": "false",
        "goal": "power_seal_hunt",
    }

    def test_seals_shuffled(self) -> None:
        """Shuffle seals should be forced on when shop chest is the goal so test it."""
        self.assertTrue(self.multiworld.shuffle_seals[self.player])

    def test_chest_access(self) -> None:
        """Defaults to a total of 45 power seals in the pool and required."""
        with self.subTest("Access Dependency"):
            self.assertEqual(len([seal for seal in self.multiworld.itempool if seal.name == "Power Seal"]),
                             self.multiworld.total_seals[self.player])
            locations = ["Rescue Phantom"]
            items = [["Power Seal"]]
            self.assertAccessDependency(locations, items)
            self.multiworld.state = CollectionState(self.multiworld)

        self.assertEqual(self.can_reach_location("Rescue Phantom"), False)
        self.assertBeatable(False)
        self.collect_all_but(["Power Seal", "Rescue Phantom"])
        self.assertEqual(self.can_reach_location("Rescue Phantom"), False)
        self.assertBeatable(False)
        self.collect_by_name("Power Seal")
        self.assertEqual(self.can_reach_location("Rescue Phantom"), True)
        self.assertBeatable(True)


class HalfSealsRequired(MessengerTestBase):
    options = {
        "goal": "power_seal_hunt",
        "percent_seals_required": 50,
    }

    def test_seals_amount(self) -> None:
        """Should have 45 power seals in the item pool and half that required"""
        self.assertEqual(self.multiworld.total_seals[self.player], 45)
        self.assertEqual(self.world.total_seals, 45)
        self.assertEqual(self.world.required_seals, 22)
        total_seals = [seal for seal in self.multiworld.itempool if seal.name == "Power Seal"]
        required_seals = [seal for seal in total_seals
                          if seal.classification == ItemClassification.progression_skip_balancing]
        self.assertEqual(len(total_seals), 45)
        self.assertEqual(len(required_seals), 22)


class ThirtyThirtySeals(MessengerTestBase):
    options = {
        "goal": "power_seal_hunt",
        "total_seals": 30,
        "percent_seals_required": 34,
    }

    def test_seals_amount(self) -> None:
        """Should have 30 power seals in the pool and 33 percent of that required."""
        self.assertEqual(self.multiworld.total_seals[self.player], 30)
        self.assertEqual(self.world.total_seals, 30)
        self.assertEqual(self.world.required_seals, 10)
        total_seals = [seal for seal in self.multiworld.itempool if seal.name == "Power Seal"]
        required_seals = [seal for seal in total_seals
                          if seal.classification == ItemClassification.progression_skip_balancing]
        self.assertEqual(len(total_seals), 30)
        self.assertEqual(len(required_seals), 10)


class MaxSealsNoShards(MessengerTestBase):
    options = {
        "goal": "power_seal_hunt",
        "total_seals": 85,
    }

    def test_seals_amount(self) -> None:
        """Should set total seals to 70 since shards aren't shuffled."""
        self.assertEqual(self.multiworld.total_seals[self.player], 85)
        self.assertEqual(self.world.total_seals, 70)


class MaxSealsWithShards(MessengerTestBase):
    options = {
        "goal": "power_seal_hunt",
        "total_seals": 85,
        "shuffle_shards": "true",
    }

    def test_seals_amount(self) -> None:
        """Should have 85 seals in the pool with all required and be a valid seed."""
        self.assertEqual(self.multiworld.total_seals[self.player], 85)
        self.assertEqual(self.world.total_seals, 85)
        self.assertEqual(self.world.required_seals, 85)
        total_seals = [seal for seal in self.multiworld.itempool if seal.name == "Power Seal"]
        required_seals = [seal for seal in total_seals
                          if seal.classification == ItemClassification.progression_skip_balancing]
        self.assertEqual(len(total_seals), 85)
        self.assertEqual(len(required_seals), 85)
