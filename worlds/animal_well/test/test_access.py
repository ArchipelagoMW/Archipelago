from . import AWTestBase
from ..names import ItemNames as iname, LocationNames as lname


class TestAccess(AWTestBase):
    # test that you can't get to the B. Ball chest until you have the K. Shards or the Ball
    def test_bball_access(self) -> None:
        self.collect_all_but([iname.ball, iname.k_shard])
        self.assertFalse(self.can_reach_location(lname.b_ball_chest))
        self.collect_by_name([iname.k_shard])
        self.assertTrue(self.can_reach_location(lname.b_ball_chest))

    def test_truth_egg_access(self) -> None:
        self.collect_all_but([iname.disc, iname.m_disc])
        self.assertFalse(self.can_reach_location(lname.egg_truth))
        self.collect_by_name([iname.m_disc])
        self.assertTrue(self.can_reach_location(lname.egg_truth))

    def test_flute_chest_access(self) -> None:
        self.assertFalse(self.can_reach_location(lname.flute_chest))
        self.collect_by_name([iname.egg_lf, iname.egg_red, iname.egg_ice, iname.egg_big,
                              iname.egg_golden, iname.egg_bubble, iname.egg_moon, iname.egg_virtual])
        self.assertTrue(self.can_reach_location(lname.flute_chest))

    def test_depraved_egg_access(self) -> None:
        self.assertFalse(self.can_reach_location(lname.egg_depraved))
        self.collect_by_name([iname.remote])
        self.assertTrue(self.can_reach_location(lname.egg_depraved))


class TestBunnyAccess(AWTestBase):
    options = {
        "bunnies_as_checks": "all_bunnies",
    }

    # test that the B.B. Wand event functions properly
    def test_bubble_long(self) -> None:
        self.collect_all_but([iname.bubble.value, iname.bubble_long_real.value]),
        self.assertFalse(self.can_reach_location(lname.bunny_water_spike))
        self.collect_by_name([iname.bubble.value]),
        self.assertTrue(self.can_reach_location(lname.bunny_water_spike))


class TestDiscHopHard(AWTestBase):
    options = {
        "disc_hopping": "multiple",
    }

    # test that you require the disc only to get to the truth egg if multiple disc hops are enabled
    def test_truth_egg(self) -> None:
        self.assertFalse(self.can_reach_location(lname.egg_truth))
        self.collect_by_name([iname.m_disc])
        self.assertTrue(self.can_reach_location(lname.egg_truth))
