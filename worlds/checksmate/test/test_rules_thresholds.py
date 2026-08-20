from BaseClasses import CollectionState

from ..locations import BoardStage
from ..rules import meets_chessmen_expectations, meets_material_expectations
from .bases import CMTestBase


STAGES = (
    BoardStage.Board8x8,
    BoardStage.Board10x8,
    BoardStage.Board12x10,
)


class ThresholdMixin:
    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)

    def state_with(self, counts: dict[str, int]) -> CollectionState:
        state = CollectionState(self.multiworld)
        for name, count in counts.items():
            for _ in range(count):
                self.assertTrue(
                    self.world.collect(state, self.world.create_item(name))
                )
        return state

    def material_meets(
        self,
        state: CollectionState,
        amount: int,
        stage: BoardStage,
    ) -> bool:
        return meets_material_expectations(
            state,
            amount,
            self.player,
            1.0,
            0,
            self.world,
            stage,
        )

    def chessmen_meet(
        self,
        state: CollectionState,
        count: int,
        stage: BoardStage,
    ) -> bool:
        return meets_chessmen_expectations(
            state,
            count,
            self.player,
            0,
            world=self.world,
            stage=stage,
        )


class TestLegacyThresholds(ThresholdMixin, CMTestBase):
    options = {
        "goal": "progressive",
        "difficulty": "grandmaster",
        "progression_itemization": "legacy",
    }

    def test_stage_local_material_and_chessmen_thresholds(self) -> None:
        state = self.state_with({
            "Progressive Pawn": 20,
            "Progressive Minor Piece": 10,
            "Progressive Major Piece": 10,
            "Progressive Major To Queen": 5,
            "Progressive Jack": 5,
        })

        self.assertEqual(
            [(3500, 35), (3900, 39), (4500, 45)],
            [
                (
                    self.world.logic_projection.metrics(
                        state,
                        self.player,
                        stage,
                    ).material,
                    self.world.logic_projection.metrics(
                        state,
                        self.player,
                        stage,
                    ).chessmen,
                )
                for stage in STAGES
            ],
        )
        self.assertEqual(
            [False, True, True],
            [self.material_meets(state, 3800, stage) for stage in STAGES],
        )
        self.assertEqual(
            [False, True, True],
            [self.chessmen_meet(state, 38, stage) for stage in STAGES],
        )
        self.assertEqual(
            [False, False, True],
            [self.material_meets(state, 4300, stage) for stage in STAGES],
        )
        self.assertEqual(
            [False, False, True],
            [self.chessmen_meet(state, 42, stage) for stage in STAGES],
        )


class TestFundamentalThresholds(ThresholdMixin, CMTestBase):
    options = {
        "goal": "progressive",
        "difficulty": "grandmaster",
        "progression_itemization": "fundamental",
    }

    def test_stage_local_material_and_chessmen_thresholds(self) -> None:
        state = self.state_with({
            "Chessmen": 20,
            "Material": 20,
            "Castler": 2,
        })

        self.assertEqual(
            [(8250, 15), (9450, 19), (9635, 20)],
            [
                (
                    self.world.logic_projection.metrics(
                        state,
                        self.player,
                        stage,
                    ).material,
                    self.world.logic_projection.metrics(
                        state,
                        self.player,
                        stage,
                    ).chessmen,
                )
                for stage in STAGES
            ],
        )
        threshold_state = self.state_with({
            "Chessmen": 17,
            "Material": 17,
            "Castler": 2,
        })
        self.assertEqual(
            [False, True, True],
            [self.material_meets(threshold_state, 7800, stage) for stage in STAGES],
        )
        self.assertEqual(
            [False, True, True],
            [self.chessmen_meet(state, 18, stage) for stage in STAGES],
        )
        # Current rule behavior caps an impossible target at the generated
        # stage maximum, so this succeeds below the literal 9500 threshold.
        self.assertEqual(
            [True, True, True],
            [self.material_meets(state, 9500, stage) for stage in STAGES],
        )
        self.assertEqual(
            [False, False, True],
            [self.chessmen_meet(state, 20, stage) for stage in STAGES],
        )
