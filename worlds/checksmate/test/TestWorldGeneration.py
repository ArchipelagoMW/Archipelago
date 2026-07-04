from .bases import CMTestBase


OFF_PREFERENCES = ["new-pawn", "more-pawn", "better-pawn", "major-to-queen"]
POOL_PREFERENCES = ["new-pawn", "pool-pawn-upgrade", "more-pawn", "better-pawn", "major-to-queen"]
MAX_PREFERENCES = ["new-pawn", "better-pawn", "more-pawn", "major-to-queen"]
FUTURE_CONFIGURE_PREFERENCES = [
    "minor-to-major",
    "major-to-jack",
    "minor-to-jack",
    "jack-to-queen",
    "queen-to-amazon",
    "major-to-queen",
    "new-pawn",
]


class TestWorldGeneration(CMTestBase):
    def test_full_generation(self):
        """Test that a complete world generates successfully"""
        pass

    def test_fairy_chess_pawn_upgrades_in_slot_data_default(self):
        """Default off (0) should appear in fill_slot_data output."""
        slot_data = self.world.fill_slot_data()
        self.assertIn("fairy_chess_pawn_upgrades", slot_data)
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 0)
        self.assertEqual(slot_data["piece_upgrade_preferences"], OFF_PREFERENCES)


class TestWorldGenerationPawnUpgradesPool(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": 1}

    def test_fairy_chess_pawn_upgrades_round_trip(self):
        """Setting option to pool (1) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 1)
        self.assertEqual(slot_data["piece_upgrade_preferences"], POOL_PREFERENCES)


class TestWorldGenerationPawnUpgradesMax(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": 2}

    def test_fairy_chess_pawn_upgrades_round_trip(self):
        """Setting option to max (2) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 2)
        self.assertEqual(slot_data["piece_upgrade_preferences"], MAX_PREFERENCES)


class TestWorldGenerationPawnUpgradesSuperMax(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": "super_max"}

    def test_fairy_chess_pawn_upgrades_round_trip(self):
        """Setting option to super_max (3) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 3)
        self.assertEqual(slot_data["piece_upgrade_preferences"], MAX_PREFERENCES)


class TestWorldGenerationPawnUpgradesConfigure(CMTestBase):
    options = {
        "fairy_chess_pawn_upgrades": "configure",
        "piece_upgrade_preferences": FUTURE_CONFIGURE_PREFERENCES,
    }

    def test_piece_upgrade_preferences_configure_round_trip(self):
        """Configure should send the configured ordered preference list."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 4)
        self.assertEqual(slot_data["piece_upgrade_preferences"], FUTURE_CONFIGURE_PREFERENCES)


class TestWorldGenerationPawnUpgradesConfigureEmpty(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": "configure"}

    def test_piece_upgrade_preferences_configure_empty_falls_back_to_off(self):
        """Configure with no list should send the legacy off preference list."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 4)
        self.assertEqual(slot_data["piece_upgrade_preferences"], OFF_PREFERENCES)
