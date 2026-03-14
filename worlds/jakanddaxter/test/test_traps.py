from BaseClasses import ItemClassification
from .bases import JakAndDaxterTestBase


class NoTrapsTest(JakAndDaxterTestBase):
    options = {
        "filler_power_cells_replaced_with_traps": 0,
        "filler_orb_bundles_replaced_with_traps": 0,
        "trap_weights": {"Trip Trap": 1},
    }

    def test_trap_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Trip Trap"
                     and item.classification == ItemClassification.trap])
        self.assertEqual(0, count)

    def test_prog_power_cells_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Power Cell"
                     and item.classification == ItemClassification.progression_skip_balancing])
        self.assertEqual(72, count)

    def test_fill_power_cells_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Power Cell"
                     and item.classification == ItemClassification.filler])
        self.assertEqual(29, count)


class SomeTrapsTest(JakAndDaxterTestBase):
    options = {
        "filler_power_cells_replaced_with_traps": 10,
        "filler_orb_bundles_replaced_with_traps": 10,
        "trap_weights": {"Trip Trap": 1},
    }

    def test_trap_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Trip Trap"
                     and item.classification == ItemClassification.trap])
        self.assertEqual(10, count)

    def test_prog_power_cells_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Power Cell"
                     and item.classification == ItemClassification.progression_skip_balancing])
        self.assertEqual(72, count)

    def test_fill_power_cells_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Power Cell"
                     and item.classification == ItemClassification.filler])
        self.assertEqual(19, count)


class MaximumTrapsTest(JakAndDaxterTestBase):
    options = {
        "filler_power_cells_replaced_with_traps": 100,
        "filler_orb_bundles_replaced_with_traps": 100,
        "trap_weights": {"Trip Trap": 1},
    }

    def test_trap_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Trip Trap"
                     and item.classification == ItemClassification.trap])
        self.assertEqual(29, count)

    def test_prog_power_cells_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Power Cell"
                     and item.classification == ItemClassification.progression_skip_balancing])
        self.assertEqual(72, count)

    def test_fill_power_cells_count(self):
        count = len([item.name for item in self.multiworld.itempool
                     if item.name == "Power Cell"
                     and item.classification == ItemClassification.filler])
        self.assertEqual(0, count)
