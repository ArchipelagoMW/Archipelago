import unittest
from collections import Counter
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def testCreateDuplicateLocations(self):
        """Tests that no two Locations share a name."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            multiworld = setup_solo_multiworld(world_type)
            locations = Counter(multiworld.get_locations())
            if locations:
                self.assertLessEqual(locations.most_common(1)[0][1], 1,
                                     f"{world_type.game} has duplicate of location {locations.most_common(1)}")

    def testLocationsInDatapackage(self):
        """Tests that created locations not filled before fill starts exist in the datapackage."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                multiworld = setup_solo_multiworld(world_type)
                locations = multiworld.get_unfilled_locations()  # do unfilled locations to avoid Events
                for location in locations:
                    self.assertIn(location.name, world_type.location_name_to_id)
                    self.assertEqual(location.address, world_type.location_name_to_id[location.name])
