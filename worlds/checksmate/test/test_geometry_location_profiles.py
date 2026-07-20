from .bases import CMTestBase
from ..locations import (
    BoardStage,
    TacticsMode,
    location_names_for_stage,
    location_table,
    stage_id,
    tactics_mode_for_options,
)


class TestGeometryLocationProfiles(CMTestBase):
    options = {"goal": "single", "enable_tactics": "all"}

    EXPECTED_TOTALS = {
        BoardStage.Board8x8: {"all": 71, "turns": 65, "none": 61},
        BoardStage.Board10x8: {"all": 86, "turns": 80, "none": 76},
        BoardStage.Board10x10: {"all": 87, "turns": 81, "none": 77},
        BoardStage.Board12x10: {"all": 102, "turns": 96, "none": 92},
        BoardStage.Board12x12: {"all": 103, "turns": 97, "none": 93},
    }

    NEW_LOCATION_IDS = {
        "Checkmate 10x10": 4_902_105,
        "Checkmate 12x10": 4_902_106,
        "Checkmate 12x12": 4_902_107,
        "Capture Pawn K": 4_902_103,
        "Capture Pawn L": 4_902_104,
        "Capture Piece Queen's Outer Attendant": 4_902_111,
        "Capture Piece King's Outer Attendant": 4_902_112,
        "Capture 11 Pawns": 4_902_124,
        "Capture 12 Pawns": 4_902_125,
        "Capture 10 Pieces": 4_902_126,
        "Capture 11 Pieces": 4_902_127,
        "Capture 10 Of Each": 4_902_132,
        "Capture 11 Of Each": 4_902_133,
        "Capture Any 19": 4_902_087,
        "Capture Any 20": 4_902_088,
        "Capture Any 21": 4_902_089,
        "Capture Any 22": 4_902_090,
    }

    def test_cumulative_stage_totals_match_contract(self):
        for stage, tactics_totals in self.EXPECTED_TOTALS.items():
            for tactics_mode, expected in tactics_totals.items():
                with self.subTest(stage=stage, tactics=tactics_mode):
                    self.assertEqual(
                        expected,
                        len(location_names_for_stage(stage, tactics_mode)),
                    )

    def test_location_ids_are_unique_and_new_ids_are_exact(self):
        codes = [data.code for data in location_table.values() if data.code is not None]
        self.assertEqual(len(codes), len(set(codes)))
        self.assertEqual(
            self.NEW_LOCATION_IDS,
            {name: location_table[name].code for name in self.NEW_LOCATION_IDS},
        )

    def test_typed_profile_metadata_replaces_sentinels_and_magic_cases(self):
        self.assertIsNone(
            location_table["Capture Pawn I"].material_expectations
        )
        capture_everything = location_table["Capture Everything"]
        self.assertEqual(
            4020,
            capture_everything.material_requirement(False),
        )
        self.assertEqual(
            8050,
            capture_everything.material_requirement(True),
        )
        self.assertEqual(14, capture_everything.chessmen_requirement(False))
        self.assertEqual(22, capture_everything.chessmen_requirement(True))
        self.assertEqual(
            BoardStage.Board12x10,
            capture_everything.stage_requirement(True),
        )
        self.assertEqual("12x12", stage_id(BoardStage.Board12x12))
        self.assertIs(
            TacticsMode.ALL,
            tactics_mode_for_options(self.world.options),
        )

    def test_single_and_non_single_generated_location_sets(self):
        self.assertEqual(
            set(location_names_for_stage(BoardStage.Board8x8)),
            {location.name for location in self.multiworld.get_locations(self.player)},
        )

    def test_victory_is_locked_for_goal(self):
        self.assertEqual(
            "Victory",
            self.multiworld.get_location("Checkmate Minima", self.player).item.name,
        )


class TestGeometryLocationProfilesProgressive(TestGeometryLocationProfiles):
    options = {"goal": "progressive", "enable_tactics": "all", "difficulty": "grandmaster"}

    def test_single_and_non_single_generated_location_sets(self):
        self.assertEqual(
            set(location_names_for_stage(BoardStage.Board12x12)),
            {location.name for location in self.multiworld.get_locations(self.player)},
        )

    def test_victory_is_locked_for_goal(self):
        self.assertEqual(
            "Victory",
            self.multiworld.get_location("Checkmate 12x12", self.player).item.name,
        )

    def test_checkmates_require_their_geometry_stage(self):
        state = self.multiworld.state
        self.collect_all_but(
            {"Board Files", "Board Ranks", "Progressive Pocket Gems", "Victory"},
            state,
        )

        self.assertFalse(self.multiworld.get_location("Checkmate Maxima", self.player).can_reach(state))
        self.world.collect(state, self.world.create_item("Board Files"))
        self.assertTrue(self.multiworld.get_location("Checkmate Maxima", self.player).can_reach(state))
        self.assertFalse(self.multiworld.get_location("Checkmate 10x10", self.player).can_reach(state))

        self.world.collect(state, self.world.create_item("Board Ranks"))
        self.assertTrue(self.multiworld.get_location("Checkmate 10x10", self.player).can_reach(state))
        self.assertFalse(self.multiworld.get_location("Checkmate 12x10", self.player).can_reach(state))

        self.world.collect(state, self.world.create_item("Board Files"))
        self.assertTrue(self.multiworld.get_location("Checkmate 12x10", self.player).can_reach(state))
        self.assertFalse(self.multiworld.get_location("Checkmate 12x12", self.player).can_reach(state))

        self.world.collect(state, self.world.create_item("Board Ranks"))
        self.assertTrue(self.multiworld.get_location("Checkmate 12x12", self.player).can_reach(state))

    def test_capture_everything_requires_twelve_files(self):
        state = self.multiworld.state
        self.collect_all_but(
            {"Board Files", "Board Ranks", "Progressive Pocket Gems", "Victory"},
            state,
        )
        location = self.multiworld.get_location("Capture Everything", self.player)

        self.world.collect(state, self.world.create_item("Board Files"))
        self.world.collect(state, self.world.create_item("Board Ranks"))
        self.assertFalse(location.can_reach(state))

        self.world.collect(state, self.world.create_item("Board Files"))
        self.assertTrue(location.can_reach(state))


class TestGeometryLocationProfilesOrdered(CMTestBase):
    options = {"goal": "ordered_progressive", "enable_tactics": "all"}

    def test_full_location_set_and_final_victory(self):
        self.assertEqual(
            set(location_names_for_stage(BoardStage.Board12x12)),
            {location.name for location in self.multiworld.get_locations(self.player)},
        )
        self.assertEqual(
            "Board Files",
            self.multiworld.get_location("Checkmate Minima", self.player).item.name,
        )
        self.assertEqual(
            "Board Ranks",
            self.multiworld.get_location("Checkmate Maxima", self.player).item.name,
        )
        self.assertEqual(
            "Board Files",
            self.multiworld.get_location("Checkmate 10x10", self.player).item.name,
        )
        self.assertEqual(
            "Board Ranks",
            self.multiworld.get_location("Checkmate 12x10", self.player).item.name,
        )
        self.assertEqual(
            "Victory",
            self.multiworld.get_location("Checkmate 12x12", self.player).item.name,
        )


class TestGeometryLocationProfilesSuper(CMTestBase):
    options = {"goal": "super", "enable_tactics": "all"}

    def test_full_location_set_and_final_victory(self):
        self.assertEqual(
            set(location_names_for_stage(BoardStage.Board12x12)),
            {location.name for location in self.multiworld.get_locations(self.player)},
        )
        self.assertEqual(
            "Victory",
            self.multiworld.get_location("Checkmate 12x12", self.player).item.name,
        )
