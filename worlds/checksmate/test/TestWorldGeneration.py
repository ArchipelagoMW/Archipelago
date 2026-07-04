from .bases import CMTestBase
from ..Options import DEFAULT_PIECE_UPGRADE_RATIO, VALID_PIECE_UPGRADE_PREFERENCES


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

    def test_piece_upgrade_ratio_in_slot_data_default(self):
        """Preference Ratio should always be exported, defaulting to DEFAULT_PIECE_UPGRADE_RATIO."""
        slot_data = self.world.fill_slot_data()
        self.assertIn("piece_upgrade_ratio", slot_data)
        self.assertEqual(slot_data["piece_upgrade_ratio"], DEFAULT_PIECE_UPGRADE_RATIO)

    def test_fair_board_guarantee_in_slot_data_default(self):
        """Default none (0) should appear in fill_slot_data output."""
        slot_data = self.world.fill_slot_data()
        self.assertIn("fair_board_guarantee", slot_data)
        self.assertEqual(slot_data["fair_board_guarantee"], 0)


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


class TestWorldGenerationPawnUpgradesConfigure(CMTestBase):
    options = {
        "fairy_chess_pawn_upgrades": "configure",
        "piece_upgrade_preferences": FUTURE_CONFIGURE_PREFERENCES,
    }

    def test_piece_upgrade_preferences_configure_round_trip(self):
        """Configure should send the configured ordered preference list."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 3)
        self.assertEqual(slot_data["piece_upgrade_preferences"], FUTURE_CONFIGURE_PREFERENCES)


class TestWorldGenerationPawnUpgradesConfigureEmpty(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": "configure"}

    def test_piece_upgrade_preferences_configure_empty_falls_back_to_off(self):
        """Configure with no list should send the legacy off preference list."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 3)
        self.assertEqual(slot_data["piece_upgrade_preferences"], OFF_PREFERENCES)


class TestWorldGenerationPiecePriorityOverridesList(CMTestBase):
    options = {
        "fairy_chess_pawn_upgrades": "configure",
        "piece_upgrade_preferences": FUTURE_CONFIGURE_PREFERENCES,
        "piece_upgrade_priority": {"new-pawn": -1, "pawn-to-minor": 5},
    }

    def test_piece_upgrade_priority_takes_precedence_over_list(self):
        """Preference Priority, when set, takes precedence over Piece Upgrade Preferences."""
        slot_data = self.world.fill_slot_data()
        preferences = slot_data["piece_upgrade_preferences"]
        self.assertIsInstance(preferences, dict)
        self.assertEqual(set(preferences.keys()), VALID_PIECE_UPGRADE_PREFERENCES)
        self.assertEqual(preferences["new-pawn"], -1)
        self.assertEqual(preferences["pawn-to-minor"], 5)
        # Unset actions default to priority 1.
        self.assertEqual(preferences["better-pawn"], 1)


class TestWorldGenerationPiecePriorityOverridesLegacyPreset(CMTestBase):
    options = {
        "fairy_chess_pawn_upgrades": "pool",
        "piece_upgrade_priority": {"queen-to-amazon": 9},
    }

    def test_piece_upgrade_priority_takes_precedence_over_legacy_preset(self):
        """Preference Priority applies regardless of Pawn Upgrades mode, including legacy presets."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 1)
        preferences = slot_data["piece_upgrade_preferences"]
        self.assertIsInstance(preferences, dict)
        self.assertNotEqual(preferences, POOL_PREFERENCES)
        self.assertEqual(preferences["queen-to-amazon"], 9)
        self.assertEqual(preferences["new-pawn"], 1)


class TestWorldGenerationPieceUpgradeRatioOverride(CMTestBase):
    options = {"piece_upgrade_ratio": {"new-pawn": 1, "better-pawn": 2}}

    def test_piece_upgrade_ratio_override_merges_with_defaults(self):
        """Overridden ratio actions replace their default weight; unset actions keep their default."""
        slot_data = self.world.fill_slot_data()
        ratio = slot_data["piece_upgrade_ratio"]
        self.assertEqual(ratio["new-pawn"], 1)
        self.assertEqual(ratio["better-pawn"], 2)
        self.assertEqual(ratio["pawn-to-minor"], DEFAULT_PIECE_UPGRADE_RATIO["pawn-to-minor"])


class TestWorldGenerationFairBoardGuarantee(CMTestBase):
    options = {"fair_board_guarantee": "standard_count"}

    def test_fair_board_guarantee_round_trip(self):
        """Setting Fair Board Guarantee should round-trip through fill_slot_data, independent of Pawn Upgrades."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fair_board_guarantee"], 1)
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 0)

