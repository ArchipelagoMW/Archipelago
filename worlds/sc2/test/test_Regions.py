import unittest
from .TestBase import Sc2TestBase
from .. import Regions
from .. import Options, MissionTables

class TestGridsizes(unittest.TestCase):
    def test_grid_sizes_meet_specs(self):
        self.assertEqual((2, 4, 1), Regions.get_grid_dimensions(7))
        self.assertEqual((2, 4, 0), Regions.get_grid_dimensions(8))
        self.assertEqual((3, 3, 0), Regions.get_grid_dimensions(9))
        self.assertEqual((2, 5, 0), Regions.get_grid_dimensions(10))
        self.assertEqual((3, 4, 1), Regions.get_grid_dimensions(11))
        self.assertEqual((3, 4, 0), Regions.get_grid_dimensions(12))
        self.assertEqual((3, 5, 0), Regions.get_grid_dimensions(15))
        self.assertEqual((4, 4, 0), Regions.get_grid_dimensions(16))
        self.assertEqual((4, 6, 0), Regions.get_grid_dimensions(24))
        self.assertEqual((5, 5, 0), Regions.get_grid_dimensions(25))
        self.assertEqual((5, 6, 1), Regions.get_grid_dimensions(29))
        self.assertEqual((5, 7, 2), Regions.get_grid_dimensions(33))


class TestGridGeneration(Sc2TestBase):
    options = {
        "mission_order": Options.MissionOrder.option_grid,
        "excluded_missions": [MissionTables.SC2Mission.ZERO_HOUR.mission_name,],
        "enable_hots_missions": False,
        "enable_prophecy_missions": True,
    }

    def test_size_matches_exclusions(self):
        self.assertNotIn(MissionTables.SC2Mission.ZERO_HOUR.mission_name, self.multiworld.regions)
        # WoL has 29 missions. -1 for Zero Hour being excluded, +1 for the automatically-added menu location
        self.assertEqual(len(self.multiworld.regions), 29)


if __name__ == '__main__':
    unittest.main(verbosity=2)
