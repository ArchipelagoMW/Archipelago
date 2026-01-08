from . import AnodyneTestBase
from ..Data.Regions import Red_Cave

class TestProgressiveRedCave(AnodyneTestBase):
    options = {
        "red_grotto_access": "progressive",
        "nexus_gates_open": "early",
    }

    def test_requirement(self):
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertFalse(self.can_reach_region(Red_Cave.left))
        self.assertFalse(self.can_reach_region(Red_Cave.right))
        self.assertFalse(self.can_reach_region(Red_Cave.top))

        progressive_red_cave = self.get_items_by_name("Progressive Red Grotto")

        self.collect(progressive_red_cave[0])
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertTrue(self.can_reach_region(Red_Cave.left))
        self.assertFalse(self.can_reach_region(Red_Cave.right))
        self.assertFalse(self.can_reach_region(Red_Cave.top))

        self.collect(progressive_red_cave[1])
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertTrue(self.can_reach_region(Red_Cave.left))
        self.assertTrue(self.can_reach_region(Red_Cave.right))
        self.assertFalse(self.can_reach_region(Red_Cave.top))

        self.collect(progressive_red_cave[2])
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertTrue(self.can_reach_region(Red_Cave.left))
        self.assertTrue(self.can_reach_region(Red_Cave.right))
        self.assertTrue(self.can_reach_region(Red_Cave.top))


class TestVanillaRedCave(AnodyneTestBase):
    options = {
        "red_grotto_access": "vanilla",
        "nexus_gates_open": "early",
        "small_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.collect_by_name("Broom")  # collect just to re-evaluate reachable regions

        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertTrue(self.can_reach_region(Red_Cave.left))
        self.assertTrue(self.can_reach_region(Red_Cave.right))
        self.assertFalse(self.can_reach_region(Red_Cave.top))

        small_key = self.get_items_by_name("Small Key (Red Grotto)")

        self.collect(small_key[0])
        self.collect(small_key[1])
        self.collect(small_key[2])
        self.collect(small_key[3])
        self.collect(small_key[4])
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertTrue(self.can_reach_region(Red_Cave.left))
        self.assertTrue(self.can_reach_region(Red_Cave.right))
        self.assertFalse(self.can_reach_region(Red_Cave.top))

        self.collect(small_key[5])
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Cave.bottom))
        self.assertTrue(self.can_reach_region(Red_Cave.Isaac))
        self.assertTrue(self.can_reach_region(Red_Cave.left))
        self.assertTrue(self.can_reach_region(Red_Cave.right))
        self.assertTrue(self.can_reach_region(Red_Cave.top))
