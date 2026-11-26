from typing import ClassVar

from ..resource_state_vars import rs_get_value, rs_set_value
from ..resource_state_vars.health_manager import HealthManager
from .bases import NoStepHK, StateVarSetup


class TestHPManager(StateVarSetup, NoStepHK):
    key = "$HPSM"
    resource: ClassVar[dict[str, int]] = {}
    cs: ClassVar[dict[str, int]] = {}
    prep_vars = ()

    def assert_spent_health(self, rs, lazy: int, white: int, blue: int):
        healths = rs_get_value(rs, "LAZYSPENTHP"), rs_get_value(rs, "SPENTHP"), rs_get_value(rs, "SPENTBLUEHP")
        self.assertEqual(healths, (lazy, white, blue), (
            f"Expected LAZYSPENTHP={'max' if lazy == HealthManager.max_damage else lazy}, "
            f"SPENTHP={white}, SPENTBLUEHP={blue}, but were {healths} instead."
        ))

    def test_strict_early(self):
        rs, cs = self.get_initialized_args()
        manager = self.get_handler()

        states = list(manager.determine_hp(rs, cs))
        self.assertEqual(len(states), 2)
        for s in states:
            self.assertTrue(manager.is_hp_determined(s))
        oc = next(s for s in states if rs_get_value(s, "OVERCHARMED"))
        noc = next(s for s in states if rs_get_value(s, "CANNOTOVERCHARM"))
        self.assertFalse(rs_get_value(oc, "CANNOTOVERCHARM"))
        self.assertFalse(rs_get_value(noc, "OVERCHARMED"))

        oc_damage = self.get_one_state(manager.take_damage, oc, cs, 1)
        self.assertEqual(rs_get_value(oc_damage, "SPENTHP"), 2)
        noc_damage = self.get_one_state(manager.take_damage, noc, cs, 1)
        self.assertEqual(rs_get_value(noc_damage, "SPENTHP"), 1)

    def test_lazy_to_strict(self):
        rs, cs = self.get_initialized_args()
        manager = self.get_handler()

        for i in range(1, 3):
            rs = self.get_one_state(manager.take_damage, rs, cs, 1)
            self.assert_spent_health(rs, i, 0, 0)
            assert not manager.is_hp_determined(rs), "HP was set to determined after lazy damage"
        for i in range(3, 5):
            rs = self.get_one_state(manager.take_damage, rs, cs, 1)
            self.assert_spent_health(rs, manager.max_damage, i, 0)
            assert manager.is_hp_determined(rs), "HP was not set to determined after taking too much lazy damage"
        rets = list(manager.take_damage(rs, cs, 1))
        assert not rets, "States were returned after taking enough damage to kill"


class TestJoniHP(StateVarSetup, NoStepHK):
    key = "$HPSM"
    resource: ClassVar[dict[str, int]] = {"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0, "CANNOTOVERCHARM": 1}
    cs: ClassVar[dict[str, int]] = {"Joni's_Blessing": 1}
    prep_vars = ()
    notch_override = 4

    def test_joni_info(self):
        rs, cs = self.get_initialized_args()
        manager = self.get_handler()
        joni_handler = self.get_handler("$EQUIPPEDCHARM[Joni's_Blessing]")
        joni_equipped, rs = joni_handler.try_equip(rs, cs)
        self.assertTrue(joni_equipped)
        rs = rs_set_value(rs, "CANNOTOVERCHARM", 1)

        rs = next(manager.determine_hp(rs, cs))
        hp = manager.get_hp_info(rs, cs)
        assert hp.max_white_hp == 7, f"Expected Max White HP to be 7 but was {hp.max_white_hp}"
        assert hp.current_white_hp == 7, f"Expected Current White HP to be 7 but was {hp.current_white_hp}"
        assert hp.current_blue_hp == 0, f"Expected Current Blue HP to be 7 but was {hp.current_blue_hp}"
