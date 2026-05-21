from collections.abc import Iterable
from dataclasses import dataclass
from itertools import zip_longest
from typing import ClassVar

from test.param import classvar_matrix

from ..charms import charm_name_to_id, charm_names
from ..resource_state_vars import dict_to_rs, rs, rs_get_value, rs_set_value
from ..resource_state_vars.equip_charm import EquipCharmVariable
from .bases import NoStepHK, StateVarSetup

charm_item_names = list(charm_name_to_id.keys())


@dataclass
class Inputs:
    notches: int
    notch_costs: Iterable[int]
    equip_results: Iterable[bool]
    ended_overcharmed: bool


class TestBasicEquips(StateVarSetup, NoStepHK):
    key = "$EQUIPPEDCHARM[Gathering_Swarm]"
    cs: ClassVar[dict[str, int]] = {"Gathering_Swarm": 1}
    resource: ClassVar[dict[str, int]] = {}
    prep_vars = ()
    notch_override = 1

    def test_basic_equip(self):
        rs, cs = self.get_initialized_args()
        handler = self.get_handler()

        equipped, rs = handler.try_equip(rs, cs)
        self.assertFalse(equipped)
        self.assertFalse(handler.is_equipped(rs))
        self.assertEqual(rs_get_value(rs, "USEDNOTCHES"), 0)
        self.assertEqual(rs_get_value(rs, "MAXNOTCHCOST"), 0)

        rs = rs_set_value(rs, "NOPASSEDCHARMEQUIP", 0)
        res_bool, res_state = handler._try_equip(rs, cs)
        self.assertTrue(res_bool)
        # test original state
        self.assertFalse(handler.is_equipped(rs))
        self.assertEqual(rs_get_value(rs, "USEDNOTCHES"), 0)
        self.assertEqual(rs_get_value(rs, "MAXNOTCHCOST"), 0)
        # test output state
        self.assertTrue(handler.is_equipped(res_state))
        self.assertEqual(rs_get_value(res_state, "USEDNOTCHES"), 1)
        self.assertEqual(rs_get_value(res_state, "MAXNOTCHCOST"), 1)

        other = rs  # for later

        rs = handler.set_unequippable(rs)
        res_bool, rs = handler.try_equip(rs, cs)
        self.assertFalse(res_bool)
        self.assertEqual(rs_get_value(rs, "USEDNOTCHES"), 0)
        self.assertEqual(rs_get_value(rs, "MAXNOTCHCOST"), 0)

        other_bool, other = handler.try_equip(other, cs)
        self.assertTrue(other_bool)
        self.assertEqual(rs_get_value(other, "USEDNOTCHES"), 1)
        self.assertEqual(rs_get_value(other, "MAXNOTCHCOST"), 1)

        other_bool, other = handler.try_equip(other, cs)
        self.assertTrue(other_bool)
        self.assertEqual(rs_get_value(other, "USEDNOTCHES"), 1)
        self.assertEqual(rs_get_value(other, "MAXNOTCHCOST"), 1)


equip_notch_matrix = [
    Inputs(1, (1,), (True,), False),
    Inputs(3, (1, 2, 1), (True, True, True), True),
    Inputs(3, (1, 2, 2), (True, True, False), False),
    Inputs(3, (2, 2, 1), (True, True, False), True),
    Inputs(3, (2, 2, 0), (True, True, True), True),
    Inputs(3, (4, 1, 1), (True, True, True), True),
    Inputs(3, (4, 1, 1, 1), (True, True, True, False), True),
    Inputs(3, (1, 1, 1, 4), (True, True, True, False), False),
    Inputs(3, (0, 1, 0), (True, True, True), False),
]


@classvar_matrix(matrix_vars=equip_notch_matrix)
class TestEquipNotch(StateVarSetup, NoStepHK):
    resource: ClassVar[dict[str, int]] = {"NOPASSEDCHARMEQUIP": 0}
    prep_vars = ()

    charm_count: int

    matrix_vars: Inputs
    notches: int
    equip_results: Iterable[bool]
    ended_overcharmed: bool

    def setUp(self):
        self.charm_count = len(self.matrix_vars.notch_costs)
        self.options = {"PlandoCharmCosts": {
            charm_name: self.matrix_vars.notch_costs[i]
            for i, charm_name in zip(
                range(self.charm_count),
                charm_names,
                strict=False,
            )
        }}
        super().setUp()
        self.cs = dict.fromkeys(charm_item_names[:self.charm_count], 1)
        self.notch_override = self.matrix_vars.notches

        self.equip_results = self.matrix_vars.equip_results
        self.ended_overcharmed = self.matrix_vars.ended_overcharmed

    def test_equip_sequence(self):
        rs, cs = self.get_initialized_args()
        handlers = [self.get_handler(f"$EQUIPPEDCHARM[{key}]") for key in charm_item_names[:self.charm_count]]

        for i in range(self.charm_count):
            result, rs = handlers[i].try_equip(rs, cs)
            assert result == self.equip_results[i]

        assert rs_get_value(rs, "OVERCHARMED") == self.ended_overcharmed


class TestGenerateCharmCombos(StateVarSetup, NoStepHK):
    resource: ClassVar[dict[str, int]] = {"NOPASSEDCHARMEQUIP": 0}
    prep_vars = ()

    charm_count: int = 2
    notch_costs: Iterable[int] = (3, 6)
    expecteds: ClassVar[list[rs]] = [
        dict_to_rs({"NOPASSEDCHARMEQUIP": 0, "noCHARM1": 1, "noCHARM2": 1}),
        dict_to_rs({"NOPASSEDCHARMEQUIP": 0, "CHARM1": 1, "noCHARM2": 1, "USEDNOTCHES": 3, "MAXNOTCHCOST": 3}),
        dict_to_rs({"NOPASSEDCHARMEQUIP": 0, "noCHARM1": 1, "CHARM2": 1,
                    "OVERCHARMED": 1,  "USEDNOTCHES": 6, "MAXNOTCHCOST": 6}),
    ]
    notch_override = 3

    def setUp(self):
        self.options = {"PlandoCharmCosts": {
            charm_name: self.notch_costs[i]
            for i, charm_name in zip(
                range(self.charm_count),
                charm_names,
                strict=False,
            )
        }}
        super().setUp()
        self.cs = dict.fromkeys(charm_item_names[:self.charm_count], 1)

    def test_combos(self):
        rs, cs = self.get_initialized_args()
        rs = rs_set_value(rs, "NOFLOWER", 0)  # TODO: get rid of this exception probably
        handlers = [self.get_handler(f"$EQUIPPEDCHARM[{key}]") for key in charm_item_names[:self.charm_count]]

        output_states = EquipCharmVariable.generate_charm_combinations(rs, cs, handlers)

        for state, expected in zip_longest(output_states, self.expecteds):
            # if states is longer or shorter than expecteds one side will be None and fail the compare
            self.assertEqual(state, expected)
            for handler in handlers:
                self.assertTrue(handler.is_determined(state, cs))
