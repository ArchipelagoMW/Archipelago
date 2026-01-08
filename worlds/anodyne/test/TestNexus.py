from . import AnodyneTestBase
from ..Data.Regions import Apartment, Red_Cave, Beach, Windmill, Bedroom, Blue, Cell, Circus, Fields, Red_Sea, Street, \
    Overworld, Space, Cliffs, Crowd, Hotel, Suburb


class TestCustomNexusGates1(AnodyneTestBase):
    options = {
        "custom_nexus_gates_open": [Red_Cave.area_name()],
        "big_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_region(Apartment.floor_1))
        self.assertTrue(self.can_reach_region(Beach.DEFAULT))
        self.assertFalse(self.can_reach_region(Bedroom.entrance))
        self.assertFalse(self.can_reach_region(Blue.DEFAULT))
        self.assertFalse(self.can_reach_region(Cell.DEFAULT))
        self.assertFalse(self.can_reach_region(Circus.DEFAULT))
        self.assertTrue(self.can_reach_region(Fields.DEFAULT))
        self.assertTrue(self.can_reach_region(Red_Cave.exit))
        self.assertTrue(self.can_reach_region(Red_Cave.top))
        self.assertFalse(self.can_reach_region(Red_Cave.left))
        self.assertFalse(self.can_reach_region(Red_Cave.right))
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Sea.DEFAULT))
        self.assertTrue(self.can_reach_region(Street.DEFAULT))


class TestCustomNexusGates2(AnodyneTestBase):
    options = {
        "custom_nexus_gates_open": [Windmill.area_name()],
        "big_key_shuffle": "any_world",
        "start_broom": "normal",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_region(Apartment.floor_1))
        self.assertFalse(self.can_reach_region(Beach.DEFAULT))
        self.assertFalse(self.can_reach_region(Bedroom.entrance))
        self.assertFalse(self.can_reach_region(Blue.DEFAULT))
        self.assertFalse(self.can_reach_region(Cell.DEFAULT))
        self.assertFalse(self.can_reach_region(Circus.DEFAULT))
        self.assertFalse(self.can_reach_region(Fields.DEFAULT))
        self.assertFalse(self.can_reach_region(Red_Cave.top))
        self.assertFalse(self.can_reach_region(Red_Cave.left))
        self.assertFalse(self.can_reach_region(Red_Cave.right))
        self.assertFalse(self.can_reach_region(Red_Cave.center))
        self.assertFalse(self.can_reach_region(Red_Sea.DEFAULT))
        self.assertTrue(self.can_reach_region(Windmill.entrance))
        self.assertTrue(self.can_reach_region(Street.DEFAULT))


class TestCustomNexusGates3(AnodyneTestBase):
    options = {
        "custom_nexus_gates_open": [Cell.area_name(), Space.area_name(), Suburb.area_name()],
        "big_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_region(Apartment.floor_1))
        self.assertTrue(self.can_reach_region(Beach.DEFAULT))
        self.assertTrue(self.can_reach_region(Bedroom.entrance))  # through the front, because of Street
        self.assertFalse(self.can_reach_region(Blue.DEFAULT))
        self.assertTrue(self.can_reach_region(Cell.DEFAULT))
        self.assertTrue(self.can_reach_region(Circus.DEFAULT))
        self.assertTrue(self.can_reach_region(Fields.DEFAULT))
        self.assertTrue(self.can_reach_region(Red_Cave.top))
        self.assertFalse(self.can_reach_region(Red_Cave.left))
        self.assertFalse(self.can_reach_region(Red_Cave.right))
        self.assertTrue(self.can_reach_region(Red_Cave.center))
        self.assertTrue(self.can_reach_region(Red_Sea.DEFAULT))
        self.assertTrue(self.can_reach_region(Overworld.DEFAULT))
        self.assertTrue(self.can_reach_region(Overworld.post_windmill))
        self.assertTrue(self.can_reach_region(Space.DEFAULT))
        self.assertTrue(self.can_reach_region(Cliffs.DEFAULT))
        self.assertTrue(self.can_reach_region(Cliffs.post_windmill))
        self.assertFalse(self.can_reach_region(Crowd.floor_1))
        self.assertTrue(self.can_reach_region(Hotel.roof))
        self.assertFalse(self.can_reach_region(Hotel.floor_1))
        self.assertTrue(self.can_reach_region(Street.DEFAULT))
