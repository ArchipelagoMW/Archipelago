from worlds.witness.test import WitnessTestBase, WitnessMultiworldTestBase


class TestSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
    }

    def test_progressive_symbols(self):
        progressive_dots = self.get_items_by_name("Progressive Dots")
        self.assertEquals(len(progressive_dots), 2)

        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player)
        )
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )

        self.collect(progressive_dots.pop())

        self.assertTrue(
            self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player)
        )
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )

        self.collect(progressive_dots.pop())

        self.assertTrue(
            self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player)
        )
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
        }
    ]

    common_options = {
        "shuffle_discarded_panels": True,
        "early_symbol_item": False,
    }

    def test_arrows(self):
        self.assertFalse(self.get_items_by_name("Arrows", 1))
        self.assertTrue(self.get_items_by_name("Arrows", 2))
        self.assertFalse(self.get_items_by_name("Arrows", 3))

    def test_correct_symbol_requirements(self):
        desert_discard = "0x17CE7"
        triangles = frozenset({frozenset({'Triangles'})})
        arrows = frozenset({frozenset({'Arrows'})})

        self.assertEqual(self.multiworld.worlds[1].player_logic.REQUIREMENTS_BY_HEX[desert_discard], triangles)
        self.assertEqual(self.multiworld.worlds[2].player_logic.REQUIREMENTS_BY_HEX[desert_discard], arrows)
        self.assertEqual(self.multiworld.worlds[3].player_logic.REQUIREMENTS_BY_HEX[desert_discard], triangles)
