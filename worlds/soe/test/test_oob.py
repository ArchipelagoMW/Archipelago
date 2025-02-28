import typing
from . import SoETestBase


class OoBTest(SoETestBase):
    """Tests that 'on' doesn't put out-of-bounds in logic. This is also the test base for OoB in logic."""
    options: typing.Dict[str, typing.Any] = {"out_of_bounds": "on"}

    def test_oob_access(self) -> None:
        in_logic = self.options["out_of_bounds"] == "logic"

        # some locations that just need a weapon + OoB
        oob_reachable = [
            "Aquagoth", "Sons of Sth.", "Mad Monk", "Magmar",  # OoB can use volcano shop to skip rock skip
            "Levitate", "Fireball", "Speed",
            "E. Crustacia #107", "Energy Core #285", "Vanilla Gauge #57",
        ]
        # some locations that should still be unreachable
        oob_unreachable = [
            "Tiny", "Rimsala",
            "Barrier", "Drain", "Call Up", "Reflect", "Force Field", "Stop",  # Stop guy only spawns from one entrance
            "Pyramid bottom #118", "Tiny's hideout #160", "Tiny's hideout #161", "Greenhouse #275",
        ]
        # OoB + Diamond Eyes
        de_reachable = [
            "Tiny's hideout #160",
        ]
        # still unreachable
        de_unreachable = [
            "Tiny",
            "Tiny's hideout #161",
        ]

        with self.subTest("No items", oob_logic=in_logic):
            self.assertLocationReachability(reachable=oob_reachable, unreachable=oob_unreachable, satisfied=False)
        with self.subTest("Cutting Weapon", oob_logic=in_logic):
            self.collect_by_name("Gladiator Sword")
            self.assertLocationReachability(reachable=oob_reachable, unreachable=oob_unreachable, satisfied=in_logic)
        with self.subTest("Cutting Weapon + DEs", oob_logic=in_logic):
            self.collect_by_name("Diamond Eye")
            self.assertLocationReachability(reachable=de_reachable, unreachable=de_unreachable, satisfied=in_logic)

    def test_real_axe(self) -> None:
        in_logic = self.options["out_of_bounds"] == "logic"

        # needs real Bronze Axe+, regardless of OoB
        real_axe_required = [
            "Drain",
            "Drain Cave #180",
            "Drain Cave #181",
        ]
        also_des_required = [
            "Double Drain",
        ]

        with self.subTest("No Axe", oob_logic=in_logic):
            self.collect_by_name("Gladiator Sword")
            self.assertLocationReachability(reachable=real_axe_required, satisfied=False)
        with self.subTest("Bronze Axe", oob_logic=in_logic):
            self.collect_by_name("Bronze Axe")
            self.assertLocationReachability(reachable=real_axe_required, satisfied=True)
        with self.subTest("Knight Basher", oob_logic=in_logic):
            self.remove_by_name("Bronze Axe")
            self.collect_by_name("Knight Basher")
            self.assertLocationReachability(reachable=real_axe_required, satisfied=True)
            self.assertLocationReachability(reachable=also_des_required, satisfied=False)
        with self.subTest("Knight Basher + DEs", oob_logic=in_logic):
            self.collect_by_name("Diamond Eye")
            self.assertLocationReachability(reachable=also_des_required, satisfied=True)

    def test_oob_goal(self) -> None:
        # still need Energy Core with OoB if sequence breaks are not in logic
        for item in ["Gladiator Sword", "Diamond Eye", "Wheel", "Gauge"]:
            self.collect_by_name(item)
        self.assertBeatable(False)
        self.collect_by_name("Energy Core")
        self.assertBeatable(True)


class OoBInLogicTest(OoBTest):
    """Tests that stuff that should be reachable/unreachable with out-of-bounds actually is."""
    options: typing.Dict[str, typing.Any] = {"out_of_bounds": "logic"}
