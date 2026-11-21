from dataclasses import FrozenInstanceError
import unittest

from ..geometry_progression import (
    BoardStage,
    MaterialCalibration,
    build_geometry_progression,
    geometry_for_stage,
)
from ..locations import location_names_for_stage, location_table


class TestGeometryMetadata(unittest.TestCase):
    def test_board_stage_values_map_to_immutable_geometry_metadata(self):
        expected = {
            -1: ("6x8", 6, 8, (0, 0), (6, 5), "Checkmate 6x8", 4_902_100, True),
            0: ("8x8", 8, 8, (1, 0), (8, 7), "Checkmate Minima", 4_902_098, True),
            1: ("10x8", 10, 8, (2, 0), (10, 9), "Checkmate Maxima", 4_902_099, True),
            2: ("10x10", 10, 10, (2, 1), (10, 9), "Checkmate 10x10", 4_902_105, True),
            3: ("12x10", 12, 10, (3, 1), (12, 11), "Checkmate 12x10", 4_902_106, True),
            4: ("12x12", 12, 12, (3, 2), (12, 11), "Checkmate 12x12", 4_902_107, False),
        }

        for value, profile in expected.items():
            with self.subTest(value=value):
                metadata = geometry_for_stage(value)
                (
                    stage_id,
                    files,
                    ranks,
                    unlocks,
                    cpu_counts,
                    location_name,
                    location_code,
                    selectable,
                ) = profile
                self.assertEqual(BoardStage(value), metadata.stage)
                self.assertEqual(stage_id, metadata.stage_id)
                self.assertEqual((files, ranks), (metadata.files, metadata.ranks))
                self.assertEqual(
                    unlocks,
                    (
                        metadata.unlocks.board_files,
                        metadata.unlocks.board_ranks,
                    ),
                )
                self.assertEqual(
                    cpu_counts,
                    (
                        metadata.cpu_pawn_count,
                        metadata.cpu_non_king_count,
                    ),
                )
                self.assertEqual(location_name, metadata.victory.location_name)
                self.assertEqual(location_code, metadata.victory.location_code)
                self.assertEqual(selectable, metadata.selectable)

        self.assertIs(
            MaterialCalibration.UNSUPPORTED,
            geometry_for_stage(BoardStage.Board6x8).victory.material_calibration,
        )
        with self.assertRaises(FrozenInstanceError):
            geometry_for_stage(0).files = 10


class TestGeometryProgression(unittest.TestCase):
    def test_plan_derives_contiguous_stages_unlock_counts_and_victory(self):
        plan = build_geometry_progression(-1, 3)

        self.assertEqual(
            (
                BoardStage.Board6x8,
                BoardStage.Board8x8,
                BoardStage.Board10x8,
                BoardStage.Board10x10,
                BoardStage.Board12x10,
            ),
            tuple(metadata.stage for metadata in plan.stages),
        )
        self.assertEqual(
            (0, 0),
            (
                plan.precollected_unlocks.board_files,
                plan.precollected_unlocks.board_ranks,
            ),
        )
        self.assertEqual(
            (3, 1),
            (
                plan.generated_unlocks.board_files,
                plan.generated_unlocks.board_ranks,
            ),
        )
        self.assertIs(plan.stages[-1], plan.endpoint)
        self.assertIs(plan.endpoint.victory, plan.victory)
        with self.assertRaises(FrozenInstanceError):
            plan.generated_unlocks = plan.precollected_unlocks

    def test_plan_rejects_reversed_unselectable_and_unknown_bounds(self):
        invalid_plans = (
            ((2, 1), "start board stage 2 must not follow end board stage 1"),
            ((2, 3), "start board stage 2 is not selectable"),
            ((0, 4), "end board stage 4 is legacy-only and not selectable"),
            ((-2, 3), "start board stage must be between -1 and 4; got -2"),
            ((True, 3), "start board stage must be an integer"),
        )

        for bounds, message in invalid_plans:
            with self.subTest(bounds=bounds):
                with self.assertRaisesRegex(ValueError, message):
                    build_geometry_progression(*bounds)

    def test_legacy_ordered_plan_retains_twelve_by_twelve_for_tracker_compatibility(self):
        from ..geometry_progression import build_legacy_ordered_progression

        plan = build_legacy_ordered_progression(BoardStage.Board8x8)

        self.assertEqual(
            (
                BoardStage.Board8x8,
                BoardStage.Board10x8,
                BoardStage.Board10x10,
                BoardStage.Board12x10,
                BoardStage.Board12x12,
            ),
            tuple(metadata.stage for metadata in plan.stages),
        )
        self.assertEqual((2, 2), (
            plan.generated_unlocks.board_files,
            plan.generated_unlocks.board_ranks,
        ))
        self.assertFalse(plan.endpoint.selectable)

    def test_plan_accepts_equal_bounds_and_later_selectable_starts(self):
        compact = build_geometry_progression(-1, -1)
        later = build_geometry_progression(1, 3)

        self.assertEqual(
            (BoardStage.Board6x8,),
            tuple(metadata.stage for metadata in compact.stages),
        )
        self.assertEqual(
            (0, 0),
            (
                compact.generated_unlocks.board_files,
                compact.generated_unlocks.board_ranks,
            ),
        )
        self.assertEqual(
            (
                BoardStage.Board10x8,
                BoardStage.Board10x10,
                BoardStage.Board12x10,
            ),
            tuple(metadata.stage for metadata in later.stages),
        )


class TestSixByEightLocationProfile(unittest.TestCase):
    def test_prologue_has_a_novel_uncalibrated_checkmate_identity(self):
        profile = geometry_for_stage(BoardStage.Board6x8).victory
        location = location_table[profile.location_name]
        self.assertEqual(4_902_100, location.code)
        self.assertEqual(BoardStage.Board6x8, location.required_stage)
        self.assertIs(MaterialCalibration.UNSUPPORTED, location.material_calibration)
        self.assertIsNone(location.material_requirement(False))
        self.assertIsNone(location.material_requirement(True))
        self.assertEqual(
            (57, 51, 47),
            tuple(
                len(location_names_for_stage(BoardStage.Board6x8, mode))
                for mode in ("all", "turns", "none")
            ),
        )
        compact_locations = set(
            location_names_for_stage(BoardStage.Board6x8)
        )
        self.assertIn("Checkmate 6x8", compact_locations)
        self.assertNotIn("Checkmate Minima", compact_locations)
        self.assertIn("Capture Pawn F", compact_locations)
        self.assertNotIn("Capture Pawn G", compact_locations)
        self.assertIn("Capture Piece Queen's Rook", compact_locations)
        self.assertEqual(
            4_902_008,
            location_table["Capture Piece Queen's Rook"].code,
        )
        self.assertNotIn("Capture Piece Queen", compact_locations)
        self.assertNotIn("Capture Piece King's Rook", compact_locations)
        self.assertIn("Capture 6 Pawns", compact_locations)
        self.assertNotIn("Capture 7 Pawns", compact_locations)
        self.assertIn("Capture 5 Pieces", compact_locations)
        self.assertNotIn("Capture 6 Pieces", compact_locations)
        self.assertIn("Capture 5 Of Each", compact_locations)
        self.assertNotIn("Capture 6 Of Each", compact_locations)
        self.assertIn("Capture Any 10", compact_locations)
        self.assertNotIn("Capture Any 11", compact_locations)
        self.assertFalse(location_table["Capture Pawn G"].compact_available)
        self.assertFalse(
            location_table["Capture Piece Queen"].compact_available
        )
        self.assertFalse(
            location_table["Capture Any 11"].compact_available
        )

        self.assertEqual(4_902_098, location_table["Checkmate Minima"].code)
        self.assertNotIn(
            "Checkmate 6x8",
            location_names_for_stage(BoardStage.Board8x8),
        )
        self.assertIn(
            "Checkmate 6x8",
            location_names_for_stage(
                BoardStage.Board8x8,
                progression_start=BoardStage.Board6x8,
            ),
        )


if __name__ == "__main__":
    unittest.main()
