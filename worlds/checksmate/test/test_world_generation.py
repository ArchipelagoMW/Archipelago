import random

from Fill import distribute_items_restrictive

from .bases import CMTestBase
from ..options import (
    DEFAULT_PIECE_UPGRADE_RATIO,
    FairyChessPawnUpgrades,
    LEGACY_PAWN_UPGRADE_PREFERENCES,
    VALID_PIECE_UPGRADE_PREFERENCES,
)


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
        """The default option set can be filled into a complete, reachable world."""
        distribute_items_restrictive(self.multiworld)
        spheres = list(self.multiworld.get_spheres())
        self.assertTrue(spheres)
        self.assertTrue(all(spheres))
        self.assertTrue(all(location.item is not None for location in self.multiworld.get_locations()))

    def test_repeated_slot_data_is_stable_without_advancing_world_rng(self):
        initial_state = self.world.random.getstate()
        first = self.world.fill_slot_data()
        expected_order = [0] * 4 + [1] * 4 + [2] * 4
        random.Random(first["pocket_seed"]).shuffle(expected_order)
        self.assertEqual(expected_order, first["pocket_order"])
        self.assertEqual(initial_state, self.world.random.getstate())

        second = self.world.fill_slot_data()
        self.assertEqual(first, second)
        self.assertEqual(initial_state, self.world.random.getstate())

        first["pocket_order"][0] = 99
        self.assertEqual(expected_order, self.world.fill_slot_data()["pocket_order"])

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

    def test_current_default_client_contract(self):
        slot_data = self.world.fill_slot_data()
        expected_keys = {
            "army",
            "apmw_contract",
            "castling_location_count",
            "death_link",
            "difficulty",
            "enable_tactics",
            "fair_board_guarantee",
            "fairy_chess_army",
            "fairy_chess_pawn_upgrades",
            "fairy_chess_pawns",
            "fairy_chess_pieces",
            "fairy_chess_pieces_configure",
            "goal",
            "geometry_unlock_items",
            "major_piece_limit_by_type",
            "logic_obtainable_counts",
            "material_item_value",
            "max_pocket",
            "major_seed",
            "minor_piece_limit_by_type",
            "minor_seed",
            "pawn_seed",
            "piece_locations",
            "piece_types",
            "progression_itemization",
            "piece_upgrade_preferences",
            "piece_upgrade_priority",
            "piece_upgrade_ratio",
            "pocket_limit_by_pocket",
            "pocket_order",
            "pocket_seed",
            "queen_piece_limit_by_type",
            "queen_seed",
            "required_chess_client_version",
            "total_queens",
        }
        expected_options = {
            "army": [0],
            "death_link": 0,
            "difficulty": 1,
            "enable_tactics": 1,
            "fair_board_guarantee": 0,
            "fairy_chess_army": 0,
            "fairy_chess_pawn_upgrades": 0,
            "fairy_chess_pawns": 0,
            "fairy_chess_pieces": 0,
            "fairy_chess_pieces_configure": [
                "Camel",
                "Cannon",
                "Clobberers",
                "FIDE",
                "Nutty",
                "Petal",
                "Rookies",
            ],
            "goal": 1,
            "castling_location_count": 2,
            "geometry_unlock_items": {
                "Board Files": "board-file-unlock",
                "Board Ranks": "board-rank-unlock",
            },
            "major_piece_limit_by_type": 0,
            "material_item_value": 400,
            "max_pocket": 12,
            "minor_piece_limit_by_type": 0,
            "piece_locations": 0,
            "piece_types": 1,
            "progression_itemization": "legacy",
            "piece_upgrade_preferences": OFF_PREFERENCES,
            "piece_upgrade_priority": {},
            "piece_upgrade_ratio": DEFAULT_PIECE_UPGRADE_RATIO,
            "pocket_limit_by_pocket": 4,
            "queen_piece_limit_by_type": 0,
            "required_chess_client_version": "0.4.0",
        }

        self.assertEqual(expected_keys, set(slot_data))
        self.assertEqual(
            expected_options,
            {key: slot_data[key] for key in expected_options},
        )
        self.assertNotIn("piece_upgrade_proportion", slot_data)
        self.assertEqual("f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15",
                         slot_data["apmw_contract"]["manifest_sha256"])
        self.assertEqual("0.4.0", slot_data["apmw_contract"]["minimum_client_version"])
        self.assertEqual(
            self.world.pool_accounting.used_count("Progressive Major To Queen"),
            slot_data["total_queens"],
        )
        self.assertEqual(
            self.world.logic_projection.obtainable_counts(),
            slot_data["logic_obtainable_counts"],
        )
        for seed_name in ("pocket_seed", "pawn_seed", "minor_seed", "major_seed", "queen_seed"):
            self.assertIsInstance(slot_data[seed_name], int)
            self.assertGreaterEqual(slot_data[seed_name], 0)
            self.assertLess(slot_data[seed_name], 2 ** 31)
        self.assertEqual([0] * 4 + [1] * 4 + [2] * 4, sorted(slot_data["pocket_order"]))

    def test_current_pawn_upgrade_enum_and_action_key_spellings(self):
        self.assertEqual(
            {
                "off": 0,
                "pool": 1,
                "max": 2,
                "configure": 3,
            },
            {
                name: FairyChessPawnUpgrades.from_any(name).value
                for name in ("off", "pool", "max", "configure")
            },
        )
        self.assertIn(
            "more-pawn",
            LEGACY_PAWN_UPGRADE_PREFERENCES[FairyChessPawnUpgrades.option_off],
        )
        self.assertIn("more-pawn", VALID_PIECE_UPGRADE_PREFERENCES)
        self.assertEqual(1, DEFAULT_PIECE_UPGRADE_RATIO["more-pawn"])


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
    options = {"piece_upgrade_ratio": {"new-pawn": 1, "more-pawn": 5, "better-pawn": 2}}

    def test_piece_upgrade_ratio_override_merges_with_defaults(self):
        """Overridden ratio actions replace their default weight; unset actions keep their default."""
        slot_data = self.world.fill_slot_data()
        ratio = slot_data["piece_upgrade_ratio"]
        self.assertEqual(ratio["new-pawn"], 1)
        self.assertEqual(ratio["more-pawn"], 5)
        self.assertEqual(ratio["better-pawn"], 2)
        self.assertEqual(ratio["pawn-to-minor"], DEFAULT_PIECE_UPGRADE_RATIO["pawn-to-minor"])


class TestWorldGenerationFairBoardGuarantee(CMTestBase):
    options = {"fair_board_guarantee": "standard_count"}

    def test_fair_board_guarantee_round_trip(self):
        """Setting Fair Board Guarantee should round-trip through fill_slot_data, independent of Pawn Upgrades."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fair_board_guarantee"], 1)
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 0)
