from collections.abc import Iterable
from dataclasses import dataclass, field

from test.param import classvar_matrix

from ..resource_state_vars import rs_get_value
from .bases import NoStepHK, StateVarSetup


@dataclass
class Inputs:
    key: str | None = None
    resource: dict[str, int] = field(default_factory=dict)
    cs: dict[str, int] = field(default_factory=dict)
    prep_vars: Iterable[str] = ()

    expecteds: Iterable[Iterable[tuple[int, int, int, int]]] = ()
    expected: tuple[int, int, int, int] | None = None
    limit: int = 0
    spend: int = 0


soul_spend_matrix = [
    Inputs(resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0},
           expecteds=[[(33, 0, 33, 0)], [(66, 0, 66, 0)], [(99, 0, 99, 0)], []]),
    Inputs(resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}, cs={"Vessel_Fragment": 3},
           expecteds=[[(0, 33, 33, 0)], [(33, 33, 33, 0)], [(66, 33, 66, 0)], [(99, 33, 99, 0)], []]),
    Inputs(resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0, "SOULLIMITER": 33},
           expecteds=[[(33, 0, 33, 33)], [(66, 0, 66, 33)], []], limit=33),
]


@classvar_matrix(matrix_vars=soul_spend_matrix)
class TestSoulSpend(StateVarSetup, NoStepHK):
    key = "$SSM"
    matrix_vars: Inputs
    expecteds: Iterable[list[tuple[int, int, int, int]]]
    limit: int = 0

    def setUp(self):
        super().setUp()
        self.resource = self.matrix_vars.resource
        self.cs = self.matrix_vars.cs
        self.prep_vars = self.matrix_vars.prep_vars

        self.expecteds = self.matrix_vars.expecteds
        self.limit = self.matrix_vars.limit

    def test_spend_soul(self):
        rs, cs = self.get_initialized_args()
        manager = self.get_handler()

        if self.limit:
            rs = self.get_one_state(manager.limit_soul, rs, cs, self.limit, True)

        states = [rs]
        for i, expected in enumerate(self.expecteds):
            states = [s for rs in states for s in manager.spend_soul(rs, cs, 33)]
            self.assertEqual([(
                    rs_get_value(s, "SPENTSOUL"),
                    rs_get_value(s, "SPENTRESERVESOUL"),
                    rs_get_value(s, "REQUIREDMAXSOUL"),
                    rs_get_value(s, "SOULLIMITER"),
                ) for s in states], expected, f"Failed on expected index {i}")


soul_restore_matrix = [
    Inputs(expected=(0, 0, 66, 0)),
    Inputs(expected=(0, 0, 66, 0), cs={"Vessel_Fragment": 3}),
    Inputs(expected=(0, 0, 66, 33), limit=33),
]


@classvar_matrix(matrix_vars=soul_restore_matrix)
class TestRestoreSpend(StateVarSetup, NoStepHK):
    key = "$SSM"
    matrix_vars: Inputs
    expected: tuple[int, int, int, int]
    limit: int = 0

    def setUp(self):
        super().setUp()
        self.resource = self.matrix_vars.resource
        self.cs = self.matrix_vars.cs
        self.prep_vars = self.matrix_vars.prep_vars

        assert self.matrix_vars.expected is not None
        self.expected = self.matrix_vars.expected
        self.limit = self.matrix_vars.limit

    def test_restore_soul(self):
        rs, cs = self.get_initialized_args()
        manager = self.get_handler()

        if self.limit:
            rs = self.get_one_state(manager.limit_soul, rs, cs, self.limit, True)
        rs2 = rs

        rs = self.get_one_state(manager.spend_soul, rs, cs, 66)
        rs = self.get_one_state(manager.restore_all_soul, rs, cs, True)
        self.assertEqual((
                    rs_get_value(rs, "SPENTSOUL"),
                    rs_get_value(rs, "SPENTRESERVESOUL"),
                    rs_get_value(rs, "REQUIREDMAXSOUL"),
                    rs_get_value(rs, "SOULLIMITER"),
                ), self.expected, "test one")

        rs2 = self.get_one_state(manager.spend_all_soul, rs2, cs)
        rs2 = self.get_one_state(manager.restore_all_soul, rs2, cs, True)
        self.assertEqual((
                    rs_get_value(rs2, "SPENTSOUL"),
                    rs_get_value(rs2, "SPENTRESERVESOUL"),
                    rs_get_value(rs2, "REQUIREDMAXSOUL"),
                    rs_get_value(rs2, "SOULLIMITER"),
                ), (
                self.expected[0],
                self.expected[1],
                manager.get_soul_info(rs2, cs).max_soul,
                self.expected[3],
                ), "test two")


soul_round_matrix = [
    Inputs(expected=(33, 0, 33, 0)),
    Inputs(cs={"Vessel_Fragment": 3}, expected=(0, 33, 33, 0)),
    Inputs(expected=None, spend=67),
]


@classvar_matrix(matrix_vars=soul_round_matrix)
class TestRoundSpend(StateVarSetup, NoStepHK):
    key = "$SSM"
    matrix_vars: Inputs
    expected: tuple[int, int, int, int] | None
    spend: int = 0

    def setUp(self):
        super().setUp()
        self.resource = self.matrix_vars.resource
        self.cs = self.matrix_vars.cs
        self.prep_vars = self.matrix_vars.prep_vars

        self.expected = self.matrix_vars.expected
        self.spend = self.matrix_vars.spend

    def test_round_spend(self):
        rs, cs = self.get_initialized_args()
        manager = self.get_handler()

        if self.spend:
            rs = self.get_one_state(manager.spend_soul, rs, cs, self.spend)
            rs = self.get_one_state(manager.restore_all_soul, rs, cs, True)

        outputs = list(manager.limit_soul(rs, cs, 33, True))
        outputs = [s for rs in outputs for s in manager.limit_soul(rs, cs, 0, False)]
        if self.expected is None:
            assert not outputs
        else:
            self.assertEqual(len(outputs), 1)
            self.assertEqual((
                        rs_get_value(outputs[0], "SPENTSOUL"),
                        rs_get_value(outputs[0], "SPENTRESERVESOUL"),
                        rs_get_value(outputs[0], "REQUIREDMAXSOUL"),
                        rs_get_value(outputs[0], "SOULLIMITER"),
                    ), self.expected)
