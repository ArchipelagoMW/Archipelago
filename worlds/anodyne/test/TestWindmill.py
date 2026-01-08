from . import AnodyneTestBase
from ..Data.Regions import Windmill, Crowd, Bedroom, Cell, Space, Suburb, Red_Cave


class TestVanillaWindmill(AnodyneTestBase):
    options = {
        "split_windmill": "false",
        "big_key_shuffle": "any_world",
        "custom_nexus_gates_open": [Windmill.area_name(), Red_Cave.area_name(), Crowd.area_name(), Bedroom.area_name()],
    }

    def test_requirement(self):
        self.collect_by_name("Broom")  # collect just to re-evaluate reachable regions

        self.assertFalse(self.can_reach_region(Windmill.DEFAULT))
        self.assertFalse(self.can_reach_region(Cell.DEFAULT))
        self.assertFalse(self.can_reach_region(Space.DEFAULT))
        self.assertFalse(self.can_reach_region(Suburb.DEFAULT))

        self.collect_by_name("Red Key")
        self.collect_by_name("Blue Key")

        self.assertTrue(self.can_reach_region(Windmill.DEFAULT))
        self.assertTrue(self.can_reach_region(Cell.DEFAULT))
        self.assertTrue(self.can_reach_region(Space.DEFAULT))
        self.assertTrue(self.can_reach_region(Suburb.DEFAULT))


class TestSplitWindmill(AnodyneTestBase):
    options = {
        "split_windmill": "true",
        "big_key_shuffle": "any_world",
        "custom_nexus_gates_open": [Windmill.area_name(), Red_Cave.area_name(), Crowd.area_name(), Bedroom.area_name()],
    }

    def test_requirement(self):
        self.collect_by_name("Broom")  # collect just to re-evaluate reachable regions

        self.assertFalse(self.can_reach_region(Windmill.DEFAULT))
        self.assertFalse(self.can_reach_region(Cell.DEFAULT))
        self.assertFalse(self.can_reach_region(Space.DEFAULT))
        self.assertFalse(self.can_reach_region(Suburb.DEFAULT))

        self.collect_by_name("Red Key")
        self.collect_by_name("Blue Key")

        self.assertTrue(self.can_reach_region(Windmill.DEFAULT))
        self.assertFalse(self.can_reach_region(Cell.DEFAULT))
        self.assertFalse(self.can_reach_region(Space.DEFAULT))
        self.assertFalse(self.can_reach_region(Suburb.DEFAULT))

        self.collect_by_name(f"{Bedroom.area_name()} Statue")
        self.assertTrue(self.can_reach_region(Suburb.DEFAULT))

        self.collect_by_name(f"{Red_Cave.area_name()} Statue")
        self.assertTrue(self.can_reach_region(Cell.DEFAULT))

        self.collect_by_name(f"{Crowd.area_name()} Statue")
        self.assertTrue(self.can_reach_region(Space.DEFAULT))
