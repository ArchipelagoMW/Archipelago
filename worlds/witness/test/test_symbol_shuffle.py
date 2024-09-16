from ..test import WitnessMultiworldTestBase, WitnessTestBase


class TestSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
    }

    def test_progressive_symbols(self) -> None:
        """
        Test that Dots & Full Dots are correctly replaced by 2x Progressive Dots,
        and test that Dots puzzles and Full Dots puzzles require 1 and 2 copies of this item respectively.
        """

        progressive_dots = self.get_items_by_name("Progressive Dots")
        self.assertEqual(len(progressive_dots), 2)

        self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )

        self.collect(progressive_dots.pop())

        self.assertTrue(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )

        self.collect(progressive_dots.pop())

        self.assertTrue(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))
        self.assertTrue(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )


class TestSymbolRequirementsMultiworld(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "puzzle_randomization": "sigma_normal",
        },
        {
            "puzzle_randomization": "sigma_expert",
        },
        {
            "puzzle_randomization": "none",
        },
        {
            "puzzle_randomization": "umbra_variety",
        }
    ]

    common_options = {
        "shuffle_discarded_panels": True,
        "early_symbol_item": False,
    }

    def test_arrows_exist_and_are_required_in_expert_seeds_only(self) -> None:
        """
        In sigma_expert, Discarded Panels require Arrows.
        In sigma_normal, Discarded Panels require Triangles, and Arrows shouldn't exist at all as an item.
        """

        with self.subTest("Test that Arrows exist only in the expert seed."):
            self.assertFalse(self.get_items_by_name("Arrows", 1))
            self.assertTrue(self.get_items_by_name("Arrows", 2))
            self.assertFalse(self.get_items_by_name("Arrows", 3))
            self.assertTrue(self.get_items_by_name("Arrows", 4))

        with self.subTest("Test that Discards ask for Triangles in normal, but Arrows in expert."):
            desert_discard = "0x17CE7"
            triangles = frozenset({frozenset({"Triangles"})})
            arrows = frozenset({frozenset({"Arrows"})})
            both = frozenset({frozenset({"Triangles", "Arrows"})})

            self.assertEqual(self.multiworld.worlds[1].player_logic.REQUIREMENTS_BY_HEX[desert_discard], triangles)
            self.assertEqual(self.multiworld.worlds[2].player_logic.REQUIREMENTS_BY_HEX[desert_discard], arrows)
            self.assertEqual(self.multiworld.worlds[3].player_logic.REQUIREMENTS_BY_HEX[desert_discard], triangles)
            self.assertEqual(self.multiworld.worlds[4].player_logic.REQUIREMENTS_BY_HEX[desert_discard], both)
