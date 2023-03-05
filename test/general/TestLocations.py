import unittest
from collections import Counter
from worlds.AutoWorld import AutoWorldRegister, call_all
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

    def testLocationCreationSteps(self):
        """Tests that Regions and Locations aren't created after `create_items`."""
        gen_steps = ("generate_early", "create_regions", "create_items")
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)
                multiworld._recache()
                region_count = len(multiworld.get_regions())
                location_count = len(multiworld.get_locations())

                call_all(multiworld, "set_rules")
                self.assertEqual(region_count, len(multiworld.get_regions()),
                                 f"{game_name} modified region count during rule creation")
                self.assertEqual(location_count, len(multiworld.get_locations()),
                                 f"{game_name} modified locations count during rule creation")

                multiworld._recache()
                call_all(multiworld, "generate_basic")
                self.assertEqual(region_count, len(multiworld.get_regions()),
                                 f"{game_name} modified region count during generate_basic")
                self.assertGreaterEqual(location_count, len(multiworld.get_locations()),
                                        f"{game_name} modified locations count during generate_basic")

                multiworld._recache()
                call_all(multiworld, "pre_fill")
                self.assertEqual(region_count, len(multiworld.get_regions()),
                                 f"{game_name} modified region count during pre_fill")
                self.assertGreaterEqual(location_count, len(multiworld.get_locations()),
                                        f"{game_name} modified locations count during pre_fill")
