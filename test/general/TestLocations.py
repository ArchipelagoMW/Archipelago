import unittest
from collections import Counter
from worlds.AutoWorld import AutoWorldRegister
from . import setup_default_world


class TestBase(unittest.TestCase):
    def testCreateDuplicateLocations(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if game_name in {"Final Fantasy"}:
                continue
            multiworld = setup_default_world(world_type)
            locations = Counter(multiworld.get_locations())
            if locations:
                self.assertLessEqual(locations.most_common(1)[0][1], 1,
                                     f"{world_type.game} has duplicate of location {locations.most_common(1)}")
