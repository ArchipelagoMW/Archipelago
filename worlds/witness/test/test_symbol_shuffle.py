from worlds.witness.test import WitnessTestBase, WitnessMultiworldTestBase


class TestSymbols(WitnessTestBase):
    options = {
        "early_symbol_item": False,
    }

    def test_progressive_symbols(self):
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player)
        )
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )

        self.collect(self.world.create_item("Progressive Dots"))

        self.assertTrue(
            self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player)
        )
        self.assertFalse(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )

        self.collect(self.world.create_item("Progressive Dots"))

        self.assertTrue(
            self.multiworld.state.can_reach("Outside Tutorial Shed Row 5", "Location", self.player)
        )
        self.assertTrue(
            self.multiworld.state.can_reach("Outside Tutorial Outpost Entry Panel", "Location", self.player)
        )


class TestArrows(WitnessMultiworldTestBase):
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
    }

    def test_arrows(self):
        self.assertFalse(self.get_items_by_name("Arrows", 1))
        self.assertTrue(self.get_items_by_name("Arrows", 2))
        self.assertFalse(self.get_items_by_name("Arrows", 3))