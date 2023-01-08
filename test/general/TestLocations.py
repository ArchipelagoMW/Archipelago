import unittest
from worlds.AutoWorld import AutoWorldRegister
from . import setup_default_world


class TestBase(unittest.TestCase):
    def testCreateDuplicateLocations(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if game_name in {"Final Fantasy"}:
                continue
            multiworld = setup_default_world(world_type)
            locations = [location for location in multiworld.get_locations() if location.address is not None]
            for location_name in world_type.location_name_to_id:
                self.assertLessEqual(len([location for location in locations if location.name == location_name]), 1,
                                     f"{world_type.game} has duplicate of location {location_name}")
