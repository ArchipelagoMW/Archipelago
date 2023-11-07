import typing
from . import SoETestBase


class SequenceBreaksTest(SoETestBase):
    """Tests that 'on' doesn't put sequence breaks in logic. This is also the test base for in-logic."""
    options: typing.Dict[str, typing.Any] = {"sequence_breaks": "on"}

    def testSequenceBreaksAccess(self):
        in_logic = self.options["sequence_breaks"] == "logic"

        # some locations that just need any weapon + sequence break
        break_reachable = [
            "Sons of Sth.", "Mad Monk", "Magmar",
            "Fireball",
            "Volcano Room1 #73", "Pyramid top #135",
        ]
        # some locations that should still be unreachable
        break_unreachable = [
            "Aquagoth", "Megataur", "Tiny", "Rimsala",
            "Barrier", "Call Up", "Levitate", "Stop", "Drain", "Escape",
            "Greenhouse #275", "E. Crustacia #107", "Energy Core #285", "Vanilla Gauge #57",
        ]

        self.assertLocationReachability(reachable=break_reachable, unreachable=break_unreachable, satisfied=False)
        self.collect_by_name("Gladiator Sword")
        self.assertLocationReachability(reachable=break_reachable, unreachable=break_unreachable, satisfied=in_logic)
        self.collect_by_name("Spider Claw")  # Gauge now just needs non-sword
        self.assertEqual(self.can_reach_location("Vanilla Gauge #57"), in_logic)
        self.collect_by_name("Bronze Spear")  # Escape now just needs either Megataur or Rimsala dead
        self.assertEqual(self.can_reach_location("Escape"), in_logic)

    def testSequenceBreaksGoal(self):
        in_logic = self.options["sequence_breaks"] == "logic"

        # don't need Energy Core with sequence breaks in logic
        for item in ["Gladiator Sword", "Diamond Eye", "Wheel", "Gauge"]:
            self.assertBeatable(False)
            self.collect_by_name(item)
        self.assertBeatable(in_logic)


class SequenceBreaksInLogicTest(SequenceBreaksTest):
    """Tests that stuff that should be reachable/unreachable with sequence breaks actually is."""
    options: typing.Dict[str, typing.Any] = {"sequence_breaks": "logic"}
