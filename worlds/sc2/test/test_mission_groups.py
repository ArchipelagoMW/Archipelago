import unittest
from .. import mission_groups


class TestMissionGroups(unittest.TestCase):
    def test_all_mission_groups_are_defined_and_nonempty(self) -> None:
        for mission_group_name in mission_groups.MissionGroupNames.get_all_group_names():
            self.assertIn(mission_group_name, mission_groups.mission_groups)
            self.assertTrue(mission_groups.mission_groups[mission_group_name])
