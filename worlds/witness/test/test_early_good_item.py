from BaseClasses import ItemClassification, LocationProgressType
from Fill import distribute_items_restrictive

from ..test import WitnessTestBase


class TestEarlySymbolItemFalse(WitnessTestBase):
    options = {
        "early_symbol_item": False,

        "shuffle_symbols": True,
        "shuffle_doors": "off",
        "shuffle_boat": False,
        "shuffle_lasers": False,
        "obelisk_keys": False,
    }

    def setUp(self) -> None:
        if self.auto_construct:
            self.world_setup(seed=1)  # Magic seed to prevent false positive

    def test_early_good_item(self) -> None:
        distribute_items_restrictive(self.multiworld)

        gate_open = self.multiworld.get_location("Tutorial Gate Open", 1)

        self.assertFalse(
            gate_open.item is None or gate_open.item.classification & ItemClassification.progression,
            "Early Good Item was off, yet a Symbol item ended up on Tutorial Gate Open.",
        )


class TestEarlySymbolItemTrue(WitnessTestBase):
    options = {
        "early_symbol_item": True,

        "shuffle_symbols": True,
        "shuffle_doors": "off",
        "shuffle_boat": False,
        "shuffle_lasers": False,
        "obelisk_keys": False,
    }

    def test_early_good_item(self) -> None:
        distribute_items_restrictive(self.multiworld)

        gate_open = self.multiworld.get_location("Tutorial Gate Open", 1)

        self.assertTrue(gate_open.item is not None, "Somehow, no item got placed on Tutorial Gate Open.")

        self.assertTrue(
            gate_open.item is not None and gate_open.item.classification & ItemClassification.progression,
            "Early Good Item was off, yet a Symbol item ended up on Tutorial Gate Open.",
        )


class TestEarlySymbolItemTrueButExcluded(WitnessTestBase):
    options = {
        "early_symbol_item": True,

        "shuffle_symbols": True,
        "shuffle_doors": "off",
        "shuffle_boat": False,
        "shuffle_lasers": False,
        "obelisk_keys": False,
    }

    def setUp(self) -> None:
        super().setUp()
        self.multiworld.get_location("Tutorial Gate Open", 1).progress_type = LocationProgressType.EXCLUDED

    def test_early_good_item(self) -> None:
        distribute_items_restrictive(self.multiworld)

        gate_open = self.multiworld.get_location("Tutorial Gate Open", 1)

        self.assertTrue(gate_open.item is not None, "Somehow, no item got placed on Tutorial Gate Open.")

        self.assertFalse(
            gate_open.item is None or gate_open.item.classification & ItemClassification.progression,
            "Tutorial Gate Open was excluded, yet it still received an early Symbol item.",
        )
