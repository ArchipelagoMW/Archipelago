import json
from itertools import product
from pathlib import Path

from BaseClasses import CollectionState
from Fill import distribute_items_restrictive

from .cm_mock_test_case import CMMockTestCase
from .bases import CMTestBase
from ..items import item_table
from ..locations import BoardStage, location_table
from ..options import PieceLocations, ProgressionItemization
from ..rules import (
    determine_difficulty,
    determine_relaxation,
    meets_chessmen_expectations,
    meets_material_expectations,
)
from ..logic_projection import WorldLogicProjection
from ..semantic_projection import SemanticSeeds


class TestFundamentalLogicProjectionEnvelope(CMMockTestCase):
    MAXIMA = {
        "Chessmen": 12,
        "Material": 10,
        "Castler": 2,
        "Progressive Consul": 2,
    }

    def projector(self, stable: bool = False) -> WorldLogicProjection:
        world = self.create_mock_world()
        world.options.progression_itemization = ProgressionItemization(
            ProgressionItemization.option_fundamental
        )
        world.options.piece_locations = PieceLocations(
            PieceLocations.option_stable if stable else PieceLocations.option_chaos
        )
        projector = WorldLogicProjection(
            world.options,
            SemanticSeeds("11", "22", "33", "44", "55"),
        )
        projector.set_obtainable_counts(self.MAXIMA)
        return projector

    def test_envelope_never_exceeds_exact_active_material_at_every_stage(self):
        projector = self.projector()
        representatives = (
            {},
            {"Chessmen": 1},
            {"Chessmen": 4, "Material": 3, "Castler": 1},
            {
                "Chessmen": 8,
                "Material": 7,
                "Castler": 2,
                "Progressive Consul": 1,
            },
            dict(self.MAXIMA),
        )
        for stage in BoardStage:
            for counts in representatives:
                with self.subTest(stage=stage, counts=counts):
                    self.assertLessEqual(
                        projector.metrics_from_counts(counts, stage).material,
                        projector.exact_active_material(counts, stage),
                    )
                    self.assertLessEqual(
                        projector.metrics_from_counts(counts, stage).chessmen,
                        projector.exact_active_non_primary_count(counts, stage),
                    )

    def test_every_single_increment_is_monotonic_for_material_and_castlers(self):
        projector = self.projector()
        axes = tuple(self.MAXIMA)
        for stage in BoardStage:
            for chessmen in range(self.MAXIMA["Chessmen"] + 1):
                for material in range(self.MAXIMA["Material"] + 1):
                    for castlers in range(self.MAXIMA["Castler"] + 1):
                        for consuls in range(self.MAXIMA["Progressive Consul"] + 1):
                            counts = {
                                "Chessmen": chessmen,
                                "Material": material,
                                "Castler": castlers,
                                "Progressive Consul": consuls,
                            }
                            current = projector.metrics_from_counts(counts, stage)
                            for axis in axes:
                                if counts[axis] >= self.MAXIMA[axis]:
                                    continue
                                future_counts = dict(counts)
                                future_counts[axis] += 1
                                future = projector.metrics_from_counts(
                                    future_counts, stage
                                )
                                self.assertGreaterEqual(
                                    future.material,
                                    current.material,
                                    (stage, counts, axis),
                                )
                                self.assertGreaterEqual(
                                    future.castlers,
                                    current.castlers,
                                    (stage, counts, axis),
                                )
                                self.assertGreaterEqual(
                                    future.chessmen,
                                    current.chessmen,
                                    (stage, counts, axis),
                                )

    def test_stable_and_chaos_expose_identical_metrics(self):
        stable = self.projector(stable=True)
        chaos = self.projector(stable=False)
        counts = {
            "Chessmen": 9,
            "Material": 8,
            "Castler": 2,
            "Progressive Consul": 1,
        }
        for stage in BoardStage:
            self.assertEqual(
                stable.metrics_from_counts(counts, stage),
                chaos.metrics_from_counts(counts, stage),
            )

    def test_material_overflow_cannot_reduce_logic_chessmen(self):
        projector = self.projector()
        projector.set_obtainable_counts(
            {
                "Chessmen": 42,
                "Material": 42,
                "Castler": 2,
                "Progressive Consul": 2,
                "Progressive King Promotion": 2,
            }
        )
        before = projector.metrics_from_counts(
            {"Chessmen": 20, "Material": 17},
            BoardStage.Board8x8,
        )
        after = projector.metrics_from_counts(
            {"Chessmen": 20, "Material": 18},
            BoardStage.Board8x8,
        )
        self.assertGreaterEqual(after.material, before.material)
        self.assertGreaterEqual(after.chessmen, before.chessmen)

    def test_over_cap_counts_normalize_to_contract_maxima(self):
        projector = self.projector()
        contract_maxima = projector.maxima
        projector.set_obtainable_counts(contract_maxima)
        over_cap = {name: 999 for name in contract_maxima}
        for stage in BoardStage:
            self.assertEqual(
                projector.metrics_from_counts(contract_maxima, stage),
                projector.metrics_from_counts(over_cap, stage),
            )
            self.assertEqual(
                projector.exact_active_material(contract_maxima, stage),
                projector.exact_active_material(over_cap, stage),
            )

    def test_king_promotion_increment_is_additive_and_bounded(self):
        projector = self.projector()
        counts = {"Chessmen": 8, "Material": 7, "Castler": 2}
        for stage in BoardStage:
            previous = projector.metrics_from_counts(counts, stage).material
            for promotions in (1, 2):
                promoted = dict(counts, **{"Progressive King Promotion": promotions})
                logic = projector.metrics_from_counts(promoted, stage).material
                self.assertEqual(previous + 425, logic)
                self.assertLessEqual(
                    logic,
                    projector.exact_active_material(promoted, stage),
                )
                previous = logic

    def test_full_upgrade_composition_uses_non_pawn_capacity(self):
        projector = self.projector()
        projector.set_obtainable_counts(projector.maxima)
        expected = (15, 19, 39, 47, 71)
        for stage, capacity in zip(BoardStage, expected):
            metrics = projector.metrics_from_counts(projector.maxima, stage)
            self.assertEqual(capacity, metrics.chessmen)
            self.assertEqual(capacity * 100 + 2 * 425, metrics.material)

    def test_all_pawn_states_keep_future_upgrade_safe_chessmen_floor(self):
        projector = self.projector()
        projector.set_obtainable_counts(projector.maxima)
        counts = {"Chessmen": 107, "Material": 0}
        for stage, non_pawn_capacity in zip(
            BoardStage,
            (15, 19, 39, 47, 71),
        ):
            metrics = projector.metrics_from_counts(counts, stage)
            self.assertEqual(non_pawn_capacity, metrics.chessmen)
            self.assertEqual(non_pawn_capacity * 100, metrics.material)


class TestLegacyLogicProjectionEnvelope(CMMockTestCase):
    MAXIMA = {
        "Progressive Pawn": 5,
        "Progressive Minor Piece": 3,
        "Progressive Major Piece": 2,
        "Progressive Major To Queen": 2,
        "Progressive Jack": 2,
        "Progressive Consul": 1,
    }

    def projector(self, stable: bool = False) -> WorldLogicProjection:
        world = self.create_mock_world()
        world.options.progression_itemization = ProgressionItemization(
            ProgressionItemization.option_legacy
        )
        world.options.piece_locations = PieceLocations(
            PieceLocations.option_stable if stable else PieceLocations.option_chaos
        )
        projector = WorldLogicProjection(
            world.options,
            SemanticSeeds("11", "22", "33", "44", "55"),
        )
        projector.set_obtainable_counts(self.MAXIMA)
        return projector

    def test_envelope_never_exceeds_exact_active_material_at_every_stage(self):
        projector = self.projector()
        representatives = (
            {},
            {"Progressive Pawn": 1},
            {
                "Progressive Pawn": 3,
                "Progressive Minor Piece": 2,
                "Progressive Major Piece": 1,
                "Progressive Major To Queen": 1,
            },
            {
                "Progressive Pawn": 5,
                "Progressive Minor Piece": 3,
                "Progressive Major Piece": 2,
                "Progressive Major To Queen": 2,
                "Progressive Jack": 2,
                "Progressive Consul": 1,
            },
        )
        for stage in BoardStage:
            for counts in representatives:
                with self.subTest(stage=stage, counts=counts):
                    self.assertLessEqual(
                        projector.metrics_from_counts(counts, stage).material,
                        projector.exact_active_material(counts, stage),
                    )

    def test_every_single_legacy_increment_keeps_material_nondecreasing(self):
        projector = self.projector()
        axes = tuple(self.MAXIMA)
        ranges = tuple(range(self.MAXIMA[axis] + 1) for axis in axes)
        for stage in BoardStage:
            for coordinates in product(*ranges):
                counts = dict(zip(axes, coordinates))
                current = projector.metrics_from_counts(counts, stage).material
                for axis in axes:
                    if counts[axis] >= self.MAXIMA[axis]:
                        continue
                    future_counts = dict(counts)
                    future_counts[axis] += 1
                    self.assertGreaterEqual(
                        projector.metrics_from_counts(
                            future_counts, stage
                        ).material,
                        current,
                        (stage, counts, axis),
                    )
                    self.assertGreaterEqual(
                        projector.metrics_from_counts(
                            future_counts, stage
                        ).chessmen,
                        projector.metrics_from_counts(counts, stage).chessmen,
                        (stage, counts, axis),
                    )
                    self.assertGreaterEqual(
                        projector.metrics_from_counts(
                            future_counts, stage
                        ).castlers,
                        projector.metrics_from_counts(counts, stage).castlers,
                        (stage, counts, axis),
                    )

    def test_frozen_pawn_overflow_forwardness_regression(self):
        fixture = (
            Path(__file__).parent
            / "fixtures"
            / "projection-v2"
            / "cases.json"
        )
        document = json.loads(fixture.read_text(encoding="utf-8"))
        case = next(
            case
            for case in document["cases"]
            if case["id"] == "pawn-overflow-forwardness-blocked"
        )
        self.assertEqual(3_200, case["output"]["exact_active_material"])

        projector = self.projector()
        projector.set_obtainable_counts(case["input"]["item_counts"])
        metrics = projector.metrics_from_counts(
            case["input"]["item_counts"],
            BoardStage.Board8x8,
        )
        self.assertEqual(32, metrics.chessmen)
        self.assertEqual(3_200, metrics.material)

    def test_legacy_stable_and_chaos_expose_identical_metrics(self):
        stable = self.projector(stable=True)
        chaos = self.projector(stable=False)
        counts = dict(self.MAXIMA)
        for stage in BoardStage:
            self.assertEqual(
                stable.metrics_from_counts(counts, stage),
                chaos.metrics_from_counts(counts, stage),
            )

    def test_legacy_king_promotion_increment_is_additive_and_bounded(self):
        projector = self.projector()
        counts = {
            "Progressive Pawn": 4,
            "Progressive Minor Piece": 2,
            "Progressive Major Piece": 2,
            "Progressive Major To Queen": 1,
            "Progressive Jack": 1,
        }
        for stage in BoardStage:
            previous = projector.metrics_from_counts(counts, stage).material
            for promotions in (1, 2):
                promoted = dict(counts, **{"Progressive King Promotion": promotions})
                logic = projector.metrics_from_counts(promoted, stage).material
                self.assertEqual(previous + 425, logic)
                self.assertLessEqual(
                    logic,
                    projector.exact_active_material(promoted, stage),
                )
                previous = logic

    def test_legacy_chessmen_uses_combined_capacity(self):
        projector = self.projector()
        projector.set_obtainable_counts(projector.maxima)
        total_owned = sum(
            projector.maxima[name]
            for name in (
                "Progressive Pawn",
                "Progressive Minor Piece",
                "Progressive Major Piece",
                "Progressive Jack",
                "Progressive Consul",
            )
        )
        for stage, capacity in zip(BoardStage, (39, 49, 69, 83, 107)):
            active = min(total_owned, capacity)
            metrics = projector.metrics_from_counts(projector.maxima, stage)
            self.assertEqual(active, metrics.chessmen)
            self.assertEqual(active * 100 + 2 * 425, metrics.material)


class TestFundamentalStageCertificates(CMTestBase):
    options = {
        "goal": "progressive",
        "progression_itemization": "fundamental",
        "difficulty": "grandmaster",
    }

    def test_later_geometry_certifies_earlier_strength_locations(self):
        state = CollectionState(self.multiworld)
        locations = (
            ("Checkmate Minima", "Board Files"),
            ("Checkmate Maxima", "Board Ranks"),
            ("Checkmate 10x10", "Board Files"),
            ("Checkmate 12x10", "Board Ranks"),
        )
        for location_name, unlock_name in locations:
            location = self.multiworld.get_location(location_name, self.player)
            self.assertFalse(location.can_reach(state), location_name)
            self.world.collect(state, self.world.create_item(unlock_name))
            self.assertTrue(location.can_reach(state), location_name)

    def test_fundamental_chessmen_keeps_progressive_pocket_credit(self):
        state = CollectionState(self.multiworld)
        for _ in range(50):
            self.world.collect(state, self.world.create_item("Chessmen"))
        self.assertEqual(
            15,
            self.world.logic_projection.metrics(
                state, self.player, BoardStage.Board8x8
            ).chessmen,
        )
        self.assertFalse(
            meets_chessmen_expectations(
                state, 16, self.player, 3, True, self.world,
                BoardStage.Board8x8,
            )
        )
        self.world.collect(state, self.world.create_item("Progressive Pocket"))
        self.assertTrue(
            meets_chessmen_expectations(
                state, 16, self.player, 3, True, self.world,
                BoardStage.Board8x8,
            )
        )

    def test_capture_everything_uses_effective_twelve_by_ten_stage(self):
        location = self.multiworld.get_location("Capture Everything", self.player)
        state = CollectionState(self.multiworld)
        self.collect_all_but(
            {"Board Files", "Board Ranks", "Victory", "Progressive Pocket Gems"},
            state,
        )

        self.world.collect(state, self.world.create_item("Board Files"))
        self.world.collect(state, self.world.create_item("Board Ranks"))
        self.assertFalse(location.can_reach(state))

        self.world.collect(state, self.world.create_item("Board Files"))
        self.assertTrue(location.can_reach(state))

    def test_capture_everything_keeps_stage_local_strength_requirements(self):
        location = self.multiworld.get_location("Capture Everything", self.player)
        state = CollectionState(self.multiworld)
        for item_name, count in (
            ("Chessmen", 21),
            ("Material", 30),
            ("Board Files", 2),
            ("Board Ranks", 1),
        ):
            for _ in range(count):
                self.world.collect(state, self.world.create_item(item_name))

        difficulty = determine_difficulty(self.world.options)
        relaxation = determine_relaxation(self.world.options)
        self.assertTrue(
            meets_material_expectations(
                state,
                location_table["Capture Everything"].material_expectations_grand,
                self.player,
                difficulty,
                relaxation,
                self.world,
                BoardStage.Board12x10,
            )
        )
        self.assertEqual(
            21,
            self.world.logic_projection.metrics(
                state, self.player, BoardStage.Board12x10
            ).chessmen,
        )
        self.assertFalse(location.can_reach(state))

        self.world.collect(state, self.world.create_item("Chessmen"))
        self.assertTrue(location.can_reach(state))

    def test_capture_everything_cannot_hold_geometry_unlocks(self):
        location = self.multiworld.get_location("Capture Everything", self.player)
        self.assertFalse(location.item_rule(self.world.create_item("Board Files")))
        self.assertFalse(location.item_rule(self.world.create_item("Board Ranks")))


class TestLegacyRuleProjection(CMTestBase):
    options = {
        "goal": "single",
        "progression_itemization": "legacy",
        "difficulty": "grandmaster",
    }

    def test_raw_pocket_material_does_not_gate_v2_legacy_rules(self):
        state = CollectionState(self.multiworld)
        for _ in range(12):
            self.world.collect(state, self.world.create_item("Progressive Pocket"))
        self.assertGreater(
            12 * item_table["Progressive Pocket"].material,
            location_table["Capture Pawn D"].material_expectations,
        )
        self.assertEqual(
            0,
            self.world.logic_projection.metrics(
                state, self.player, BoardStage.Board8x8
            ).material,
        )
        self.assertFalse(
            self.multiworld.get_location(
                "Capture Pawn D", self.player
            ).can_reach(state)
        )

    def test_legacy_chessmen_keeps_progressive_pocket_credit(self):
        state = CollectionState(self.multiworld)
        for _ in range(50):
            self.world.collect(state, self.world.create_item("Progressive Pawn"))
        self.assertEqual(
            32,
            self.world.logic_projection.metrics(
                state, self.player, BoardStage.Board8x8
            ).chessmen,
        )
        self.assertFalse(
            meets_chessmen_expectations(
                state, 33, self.player, 3, False, self.world,
                BoardStage.Board8x8,
            )
        )
        self.world.collect(state, self.world.create_item("Progressive Pocket"))
        self.assertTrue(
            meets_chessmen_expectations(
                state, 33, self.player, 3, False, self.world,
                BoardStage.Board8x8,
            )
        )


class _ShuffledGeometrySphereMixin:
    def test_geometry_unlock_placements_are_stage_safe_and_sphered(self):
        distribute_items_restrictive(self.multiworld)
        spheres = list(self.multiworld.get_spheres())
        self.assertTrue(spheres)
        self.assertTrue(all(spheres), "Generated an unreachable sphere")

        placed = {"Board Files": 0, "Board Ranks": 0}
        for sphere in spheres:
            for location in sphere:
                if location.item is None or location.item.name not in placed:
                    continue
                placed[location.item.name] += 1
                required_stage = location_table[location.name].required_stage
                if location.item.name == "Board Files":
                    self.assertEqual(BoardStage.Board8x8, required_stage)
                else:
                    self.assertLessEqual(required_stage, BoardStage.Board10x8)
        self.assertGreaterEqual(placed["Board Files"], 1)
        self.assertEqual(2, placed["Board Ranks"])


class TestProgressiveGeometrySpheres(_ShuffledGeometrySphereMixin, CMTestBase):
    options = {
        "goal": "progressive",
        "progression_itemization": "fundamental",
        "difficulty": "grandmaster",
    }


class TestSuperGeometrySpheres(_ShuffledGeometrySphereMixin, CMTestBase):
    options = {
        "goal": "super",
        "progression_itemization": "fundamental",
        "difficulty": "grandmaster",
    }


class TestOrderedGeometrySpheres(CMTestBase):
    options = {
        "goal": "ordered_progressive",
        "progression_itemization": "fundamental",
        "difficulty": "grandmaster",
    }

    def test_ordered_unlock_chain_appears_in_successive_spheres(self):
        distribute_items_restrictive(self.multiworld)
        spheres = list(self.multiworld.get_spheres())
        self.assertTrue(all(spheres), "Ordered geometry chain self-locked")
        sphere_index = {
            location.name: index
            for index, sphere in enumerate(spheres)
            for location in sphere
        }
        chain = (
            "Checkmate Minima",
            "Checkmate Maxima",
            "Checkmate 10x10",
            "Checkmate 12x10",
            "Checkmate 12x12",
        )
        self.assertEqual(
            sorted(sphere_index[name] for name in chain),
            [sphere_index[name] for name in chain],
        )
        self.assertEqual(
            ("Board Files", "Board Ranks", "Board Files", "Board Ranks", "Victory"),
            tuple(
                self.multiworld.get_location(name, self.player).item.name
                for name in chain
            ),
        )
