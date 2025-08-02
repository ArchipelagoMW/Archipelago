from ..test.bases import WitnessMultiworldTestBase, WitnessTestBase


class TestProgressiveSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
        "puzzle_randomization": "umbra_variety",
        "progressive_symbols": {
            "Progressive Dots",
            "Progressive Symmetry",
            "Progressive Stars",
            "Progressive Squares",
            "Progressive Shapers",
            "Progressive Discard Symbols"
        }
    }

    def test_progressive_symbols(self) -> None:
        """
        Test that Full Dots are correctly replaced by 2x Progressive Dots,
        and test that Dots puzzles and Full Dots puzzles require 1 and 2 copies of this item respectively.
        """

        expected_quantities = {
            # Individual items that are replaced by progressive items
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

            # Progressive items
            "Progressive Dots": 2,
            "Progressive Symmetry": 2,
            "Progressive Stars": 2,
            "Progressive Squares": 2,
            "Progressive Shapers": 3,
            "Progressive Discard Symbols": 2,

            # Individual items that still exist because they aren't a part of any progressive chain
            "Sound Dots": 1,
        }

        self.assert_quantities_in_itempool(expected_quantities)

        with self.subTest("Verify that Dots panels need 1 copy of Progressive Dots and Full Dots panel need 2 copies"):
            self.collect_all_but("Progressive Dots")
            progressive_dots = self.get_items_by_name("Progressive Dots")
            self.assertEqual(len(progressive_dots), 2)

            self.assertFalse(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertTrue(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

        with self.subTest("Verify proguseful status of progressive & alias items"):
            self.assert_item_exists_and_is_proguseful("Progressive Symmetry", proguseful=False)
            self.assert_item_exists_and_is_proguseful("Sound Dots", proguseful=False)

            self.assert_item_exists_and_is_proguseful("Progressive Dots")
            self.assert_item_exists_and_is_proguseful("Progressive Stars")
            self.assert_item_exists_and_is_proguseful("Progressive Squares")
            self.assert_item_exists_and_is_proguseful("Progressive Shapers")
            self.assert_item_exists_and_is_proguseful("Progressive Discard Symbols")


class TestIndependentSecondStageSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
        "puzzle_randomization": "umbra_variety",
        "progressive_symbols": {},
        "second_stage_symbols_act_independently": {
            "Full Dots",
            "Stars + Same Colored Symbol",
            "Colored Dots",
        },
        "shuffle_doors": "doors",
    }

    def test_independent_second_stage_symbols(self) -> None:
        expected_quantities = {
            # Progressive items shouldn't exist
            "Progressive Dots": 0,
            "Progressive Symmetry": 0,
            "Progressive Stars": 0,
            "Progressive Squares": 0,
            "Progressive Shapers": 0,
            "Progressive Discard Symbols": 0,

            # Dots and Stars are replaced by Sparse Dots and Simple Stars
            "Dots": 0,
            "Stars": 0,
            "Sparse Dots": 1,
            "Simple Stars": 1,

            # None of the symbols are progressive, so they should all exist
            "Full Dots": 1,
            "Symmetry": 1,
            "Colored Dots": 1,
            "Stars + Same Colored Symbol": 1,
            "Black/White Squares": 1,
            "Colored Squares": 1,
            "Shapers": 1,
            "Rotated Shapers": 1,
            "Negative Shapers": 1,
            "Triangles": 1,
            "Arrows": 1,
            "Sound Dots": 1,
        }

        self.assert_quantities_in_itempool(expected_quantities)

        with self.subTest("Verify that Full Dots panels only need Full Dots"):
            self.collect_by_name("Black/White Squares")
            self.collect_by_name("Triangles")
            self.collect_by_name("Outside Tutorial Outpost Exit (Door)")

            self.assertFalse(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Exit Panel", "Location", self.player)
            )
            self.collect_by_name("Full Dots")
            self.assertTrue(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Exit Panel", "Location", self.player)
            )

        with self.subTest("Verify that Stars + Same Colored Symbol panels only need Stars + Same Colored Symbol"):
            self.collect_by_name("Eraser")
            self.collect_by_name("Quarry Entry 1 (Door)")
            self.collect_by_name("Quarry Entry 2 (Door)")

            self.assertFalse(
                self.multiworld.state.can_reach("Quarry Stoneworks Entry Left Panel", "Location", self.player)
            )
            self.collect_by_name("Stars + Same Colored Symbol")
            self.assertTrue(
                self.multiworld.state.can_reach("Quarry Stoneworks Entry Left Panel", "Location", self.player)
            )

        with self.subTest("Verify that non-symmetry Colored Dots panels only need Colored Dots"):
            self.collect_by_name("Symmetry Island Lower (Door)")
            self.collect_by_name("Symmetry Island Upper (Door)")

            self.assertFalse(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.collect_by_name("Colored Dots")
            self.assertTrue(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )

        with self.subTest("Verify proguseful status of progressive & alias items"):
            self.assert_item_exists_and_is_proguseful("Full Dots", proguseful=False)
            self.assert_item_exists_and_is_proguseful("Stars + Same Colored Symbol", proguseful=False)
            self.assert_item_exists_and_is_proguseful("Arrows", proguseful=False)  # Variety

            self.assert_item_exists_and_is_proguseful("Sparse Dots")
            self.assert_item_exists_and_is_proguseful("Simple Stars")
            self.assert_item_exists_and_is_proguseful("Triangles")  # Variety


class TestDependentSecondStageSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
        "puzzle_randomization": "umbra_variety",
        "progressive_symbols": {},
        "second_stage_symbols_act_independently": {},
        "shuffle_doors": "doors",
    }

    def test_dependent_second_stage_symbols(self) -> None:
        expected_quantities = {
            # Progressive items shouldn't exist
            "Progressive Dots": 0,
            "Progressive Symmetry": 0,
            "Progressive Stars": 0,
            "Progressive Squares": 0,
            "Progressive Shapers": 0,
            "Progressive Discard Symbols": 0,

            # Dots and Stars are NOT replaced by Sparse Dots and Simple Stars
            "Dots": 1,
            "Stars": 1,
            "Sparse Dots": 0,
            "Simple Stars": 0,

            # None of the symbols are progressive, so they should all exist
            "Full Dots": 1,
            "Symmetry": 1,
            "Colored Dots": 1,
            "Stars + Same Colored Symbol": 1,
            "Black/White Squares": 1,
            "Colored Squares": 1,
            "Shapers": 1,
            "Rotated Shapers": 1,
            "Negative Shapers": 1,
            "Triangles": 1,
            "Arrows": 1,
            "Sound Dots": 1,
        }

        self.assert_quantities_in_itempool(expected_quantities)

        with self.subTest("Verify that Full Dots panels need Dots as well"):
            self.collect_by_name("Black/White Squares")
            self.collect_by_name("Triangles")
            self.collect_by_name("Outside Tutorial Outpost Exit (Door)")

            self.assertFalse(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Exit Panel", "Location", self.player))
            self.collect_by_name("Full Dots")
            self.assertFalse(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Exit Panel", "Location", self.player))
            self.collect_by_name("Dots")
            self.assertTrue(
                self.multiworld.state.can_reach("Outside Tutorial Outpost Exit Panel", "Location", self.player)
            )

        with self.subTest("Verify that Stars + Same Colored Symbol panels need Stars as well"):
            self.collect_by_name("Eraser")
            self.collect_by_name("Quarry Entry 1 (Door)")
            self.collect_by_name("Quarry Entry 2 (Door)")

            self.assertFalse(
                self.multiworld.state.can_reach("Quarry Stoneworks Entry Left Panel", "Location", self.player)
            )
            self.collect_by_name("Stars + Same Colored Symbol")
            self.assertFalse(
                self.multiworld.state.can_reach("Quarry Stoneworks Entry Left Panel", "Location", self.player)
            )
            self.collect_by_name("Stars")
            self.assertTrue(
                self.multiworld.state.can_reach("Quarry Stoneworks Entry Left Panel", "Location", self.player)
            )

        with self.subTest("Verify that non-symmetry Colored Dots panels need Symmetry as well"):
            self.collect_by_name("Symmetry Island Lower (Door)")
            self.collect_by_name("Symmetry Island Upper (Door)")

            self.assertFalse(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.collect_by_name("Colored Dots")
            self.assertFalse(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.collect_by_name("Symmetry")
            self.assertTrue(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )

        with self.subTest("Verify proguseful status of progressive & alias items"):
            self.assert_item_exists_and_is_proguseful("Full Dots", proguseful=False)
            self.assert_item_exists_and_is_proguseful("Stars + Same Colored Symbol", proguseful=False)
            self.assert_item_exists_and_is_proguseful("Arrows", proguseful=False)  # Variety

            self.assert_item_exists_and_is_proguseful("Dots")
            self.assert_item_exists_and_is_proguseful("Stars")
            self.assert_item_exists_and_is_proguseful("Triangles")  # Variety


class TestAlternateProgressiveDots(WitnessTestBase):
    options = {
        "early_symbol_item": False,
        "puzzle_randomization": "umbra_variety",
        "progressive_symbols": {
            "Progressive Dots",
            "Progressive Symmetry"
        },
        "second_stage_symbols_act_independently": {
            "Full Dots",
            "Stars + Same Colored Symbol",
            "Colored Dots",
        },
        "colored_dots_are_progressive_dots": True,
        "sound_dots_are_progressive_dots": True,
        "shuffle_doors": "doors",
    }

    def test_alternate_progressive_dots(self) -> None:
        expected_quantities = {
            # Progressive Dots chain now has 4 members
            "Progressive Dots": 4,

            # Dots items don't exist because Progressive Dots is on.
            # For this test, this includes Colored Dots and Sound Dots as well
            "Dots": 0,
            "Sparse Dots": 0,
            "Colored Dots": 0,
            "Sound Dots": 0,
            "Full Dots": 0,

            # Progressive Symmetry no longer exists, because Colored Dots is part of the Progressive Dots chain instead
            "Progressive Symmetry": 0,

            # Other Progressive Symbols don't exist
            "Progressive Stars": 0,
            "Progressive Squares": 0,
            "Progressive Shapers": 0,
            "Progressive Discard Symbols": 0,

            # Other standalone items exist, because they are not progressive
            "Symmetry": 1,
            "Stars + Same Colored Symbol": 1,
            "Black/White Squares": 1,
            "Colored Squares": 1,
            "Shapers": 1,
            "Rotated Shapers": 1,
            "Negative Shapers": 1,
            "Triangles": 1,
            "Arrows": 1,

            # This test is set to have independent symbols, so Simple Stars exist instead of Stars
            "Stars": 0,
            "Simple Stars": 1,
        }

        self.assert_quantities_in_itempool(expected_quantities)

        self.collect_all_but(["Progressive Dots", "Symmetry"])  # Skip Symmetry so we can also test a little quirk
        progressive_dots = self.get_items_by_name("Progressive Dots")
        self.assertEqual(len(progressive_dots), 4)

        with self.subTest("Test that one copy of Progressive Dots unlocks Dots panels"):
            self.assertFalse(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertFalse(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.assertFalse(self.multiworld.state.can_reach("Jungle Popup Wall 6", "Location", self.player))
            self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertFalse(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.assertFalse(self.multiworld.state.can_reach("Jungle Popup Wall 6", "Location", self.player))
            self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

        with self.subTest("Test that two copies of Progressive Dots unlocks Colored Dots panels"):
            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            # Also test here that these "Colored Dots" act independently from Symmetry like they are supposed to
            self.assertTrue(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.assertFalse(self.multiworld.state.can_reach("Jungle Popup Wall 6", "Location", self.player))
            self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

        with self.subTest("Test that three copies of Progressive Dots unlocks Sound Dots panels"):
            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertTrue(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.assertTrue(self.multiworld.state.can_reach("Jungle Popup Wall 6", "Location", self.player))
            self.assertFalse(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

        with self.subTest("Test that four copies of Progressive Dots unlocks Full Dots panels"):
            self.collect(progressive_dots.pop())

            self.assertTrue(self.multiworld.state.can_reach("Tutorial Patio Floor", "Location", self.player))
            self.assertTrue(
                self.multiworld.state.can_reach("Symmetry Island Laser Blue 3", "Location", self.player)
            )
            self.assertTrue(self.multiworld.state.can_reach("Jungle Popup Wall 6", "Location", self.player))
            self.assertTrue(self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player))

        with self.subTest("Verify proguseful status of progressive & alias items"):
            self.assert_item_exists_and_is_proguseful("Progressive Dots")
            self.assert_item_exists_and_is_proguseful("Simple Stars")


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
