from ..test import WitnessMultiworldTestBase, WitnessTestBase


class TestSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
        "puzzle_randomization": "umbra_variety",
        "progressive_symbols": {
            "Progressive Dots",
            "Progressive Symmetry",
            "Progressive Stars",
            "Progressive Squares",
            "Progressive Shapers",
            "Progressive Line-Counting Symbols"
        }
    }

    def test_progressive_symbols(self) -> None:
        """
        Test that Full Dots are correctly replaced by 2x Progressive Dots,
        and test that Dots puzzles and Full Dots puzzles require 1 and 2 copies of this item respectively.
        """

        expected_quantities = {
            "Progressive Dots": 2,
            "Progressive Symmetry": 2,
            "Progressive Stars": 2,
            "Progressive Squares": 2,
            "Progressive Shapers": 3,
            "Progressive Line-Counting Symbols": 2,
            "Dots": 0,
            "Sparse Dots": 0,
            "Full Dots": 0,
            "Symmetry": 0,
            "Colored Dots": 0,
            "Stars": 0,
            "Simple Stars": 0,
            "Stars + Same Colored Symbol": 0,
            "Black/White Squares": 0,
            "Colored Squares": 0,
            "Shapers": 0,
            "Rotated Shapers": 0,
            "Negative Shapers": 0,
            "Triangles": 0,
            "Arrows": 0,
        }

        for item, expected_quantity in expected_quantities.items():
            with self.subTest(f"Verify that there are {expected_quantity} copies of {item} in the itempool."):
                found_items = self.get_items_by_name(item)
                self.assertEqual(len(found_items), expected_quantity)

        with self.subTest(f"Verify that Dots panels need 1 copy of Progressive Dots and Full Dots panel need 2 copies"):
            self.collect_all_but("Progressive Dots")
            progressive_dots = self.get_items_by_name("Progressive Dots")
            self.assertEqual(len(progressive_dots), 2)

            self.assertFalse(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertFalse(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
            )

            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertFalse(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
            )

            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
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
