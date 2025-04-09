from BaseClasses import ItemClassification, LocationProgressType
from Fill import distribute_items_restrictive

from ..data.utils import cast_not_none
from ..test import WitnessTestBase


class TestEarlySymbolItemFalse(WitnessTestBase):
    options = {
        "early_good_items": {},

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
            cast_not_none(gate_open.item).classification & ItemClassification.progression,
            "Early Good Item was off, yet a Symbol item ended up on Tutorial Gate Open.",
        )


class TestEarlySymbolItemTrue(WitnessTestBase):
    options = {
        "early_good_items": {"Symbol", "Door / Door Panel", "Obelisk Key"},

        "shuffle_symbols": True,
        "shuffle_doors": "panels",
        "shuffle_EPs": "individual",
        "obelisk_keys": True,
    }

    def setUp(self) -> None:
        super().setUp()

    def test_early_good_item(self) -> None:
        """
        The items should be in the order:
        Symbol item on Tutorial Gate Open
        Door item on Tutorial Back Left
        Obelisk Key on Tutorial Back Right
        """

        distribute_items_restrictive(self.multiworld)

        gate_open = self.multiworld.get_location("Tutorial Gate Open", 1)

        self.assertTrue(gate_open.item is not None, "Somehow, no item got placed on Tutorial Gate Open.")

        self.assertTrue(
            cast_not_none(gate_open.item).name in self.world.item_name_groups["Symbols"],
            "Early Good Item was on, yet no Symbol item ended up on Tutorial Gate Open.",
        )

        back_left = self.multiworld.get_location("Tutorial Back Left", 1)

        self.assertTrue(back_left.item is not None, "Somehow, no item got placed on Tutorial Back Left.")

        doors_and_panel_keys = self.world.item_name_groups["Doors"] | self.world.item_name_groups["Panel Keys"]
        self.assertTrue(
            cast_not_none(back_left.item).name in doors_and_panel_keys,
            "Early Good Item was on, yet no Door item ended up on Tutorial Back Left.",
        )

        back_right = self.multiworld.get_location("Tutorial Back Right", 1)

        self.assertTrue(back_right.item is not None, "Somehow, no item got placed on Tutorial Back Right.")

        self.assertTrue(
            cast_not_none(back_right.item).name in self.world.item_name_groups["Obelisk Keys"],
            "Early Good Item was on, yet no Obelisk Key item ended up on Tutorial Back Right.",
        )


class TestEarlySymbolItemTrueButExcluded(WitnessTestBase):
    options = {
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
            cast_not_none(gate_open.item).classification & ItemClassification.progression,
            "Tutorial Gate Open was excluded, yet it still received an early Symbol item.",
        )
