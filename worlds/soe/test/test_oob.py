import typing
from . import SoETestBase


class OoBTest(SoETestBase):
    """Tests that 'on' doesn't put out-of-bounds in logic. This is also the test base for OoB in logic."""
    options: typing.Dict[str, typing.Any] = {"out_of_bounds": "on"}

    def testOoBAccess(self):
        in_logic = self.options["out_of_bounds"] == "logic"

        # some locations that just need a weapon + OoB
        oob_reachable = [
            "Aquagoth", "Sons of Sth.", "Mad Monk", "Magmar",  # OoB can use volcano shop to skip rock skip
            "Levitate", "Fireball", "Drain", "Speed",
            "E. Crustacia #107", "Energy Core #285", "Vanilla Gauge #57",
        ]
        # some locations that should still be unreachable
        oob_unreachable = [
            "Tiny", "Rimsala",
            "Barrier", "Call Up", "Reflect", "Force Field", "Stop",  # Stop guy doesn't spawn for the other entrances
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

        self.assertLocationReachability(reachable=oob_reachable, unreachable=oob_unreachable, satisfied=False)
        self.collect_by_name("Gladiator Sword")
        self.assertLocationReachability(reachable=oob_reachable, unreachable=oob_unreachable, satisfied=in_logic)
        self.collect_by_name("Diamond Eye")
        self.assertLocationReachability(reachable=de_reachable, unreachable=de_unreachable, satisfied=in_logic)

    def testOoBGoal(self):
        # still need Energy Core with OoB if sequence breaks are not in logic
        for item in ["Gladiator Sword", "Diamond Eye", "Wheel", "Gauge"]:
            self.collect_by_name(item)
        self.assertBeatable(False)
        self.collect_by_name("Energy Core")
        self.assertBeatable(True)


class OoBInLogicTest(OoBTest):
    """Tests that stuff that should be reachable/unreachable with out-of-bounds actually is."""
    options: typing.Dict[str, typing.Any] = {"out_of_bounds": "logic"}
