import unittest
from .. import location_groups
from ..mission_tables import SC2Mission, MissionFlag


class TestLocationGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.location_groups = location_groups.get_location_groups()

    def test_location_categories_have_a_group(self) -> None:
        self.assertIn('Victory', self.location_groups)
        self.assertIn(f'{SC2Mission.LIBERATION_DAY.mission_name}: Victory', self.location_groups['Victory'])
        self.assertIn(f'{SC2Mission.IN_UTTER_DARKNESS.mission_name}: Defeat', self.location_groups['Victory'])
        self.assertIn('Vanilla', self.location_groups)
        self.assertIn(f'{SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name}: Close Relic', self.location_groups['Vanilla'])
        self.assertIn('Extra', self.location_groups)
        self.assertIn(f'{SC2Mission.SMASH_AND_GRAB.mission_name}: First Forcefield Area Busted', self.location_groups['Extra'])
        self.assertIn('Challenge', self.location_groups)
        self.assertIn(f'{SC2Mission.ZERO_HOUR.mission_name}: First Hatchery', self.location_groups['Challenge'])
        self.assertIn('Mastery', self.location_groups)
        self.assertIn(f'{SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name}: Protoss Cleared', self.location_groups['Mastery'])

    def test_missions_have_a_group(self) -> None:
        self.assertIn(SC2Mission.LIBERATION_DAY.mission_name, self.location_groups)
        self.assertIn(f'{SC2Mission.LIBERATION_DAY.mission_name}: Victory', self.location_groups[SC2Mission.LIBERATION_DAY.mission_name])
        self.assertIn(f'{SC2Mission.LIBERATION_DAY.mission_name}: Special Delivery', self.location_groups[SC2Mission.LIBERATION_DAY.mission_name])

    def test_race_swapped_locations_share_a_group(self) -> None:
        self.assertIn(MissionFlag.HasRaceSwap, SC2Mission.ZERO_HOUR.flags)
        ZERO_HOUR = 'Zero Hour'
        self.assertNotEqual(ZERO_HOUR, SC2Mission.ZERO_HOUR.mission_name)
        self.assertIn(ZERO_HOUR, self.location_groups)
        self.assertIn(f'{ZERO_HOUR}: Victory', self.location_groups)
        self.assertIn(f'{SC2Mission.ZERO_HOUR.mission_name}: Victory', self.location_groups[f'{ZERO_HOUR}: Victory'])
        self.assertIn(f'{SC2Mission.ZERO_HOUR_P.mission_name}: Victory', self.location_groups[f'{ZERO_HOUR}: Victory'])
        self.assertIn(f'{SC2Mission.ZERO_HOUR_Z.mission_name}: Victory', self.location_groups[f'{ZERO_HOUR}: Victory'])
