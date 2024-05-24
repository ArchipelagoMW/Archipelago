
import unittest
from .. import MissionGroups

class TestMissionGroups(unittest.TestCase):
    def test_all_mission_groups_are_defined_and_nonempty(self) -> None:
        for mission_group_name in MissionGroups.MissionGroupNames.get_all_group_names():
            self.assertIn(mission_group_name, MissionGroups.mission_groups)
            self.assertTrue(MissionGroups.mission_groups[mission_group_name])
