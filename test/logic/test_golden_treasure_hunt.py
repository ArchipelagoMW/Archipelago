from .. import WL4TestBase
from ...options import Difficulty, Goal, Logic


class TestNormalTreasureHunt(WL4TestBase):
    options = {'goal': Goal.option_golden_treasure_hunt,
               'difficulty': Difficulty.option_normal}

    def test_treasure_hunt(self):
        self.starting_regions = ['Emerald Passage Boss', 'Ruby Passage Boss',
                                 'Topaz Passage Boss', 'Sapphire Passage Boss']
        self._test_cractus()
        self._test_cuckoo_condor()
        self._test_aerodent()
        self._test_catbat()

    def _test_cractus(self):
        self.run_location_tests([
            ['Cractus - 0:15', False, []],
            ['Cractus - 0:15', False, [], ['Progressive Ground Pound']],
            ['Cractus - 0:15', True, ['Progressive Ground Pound']],

            ['Cractus - 0:35', False, []],
            ['Cractus - 0:35', False, [], ['Progressive Ground Pound']],
            ['Cractus - 0:35', True, ['Progressive Ground Pound']],

            ['Cractus - 0:55', False, []],
            ['Cractus - 0:55', False, [], ['Progressive Ground Pound']],
            ['Cractus - 0:55', True, ['Progressive Ground Pound']],
        ])

    def _test_cuckoo_condor(self):
        self.run_location_tests([
            ['Cuckoo Condor - 0:15', False, []],
            ['Cuckoo Condor - 0:15', False, [], ['Progressive Grab']],
            ['Cuckoo Condor - 0:15', True, ['Progressive Grab']],

            ['Cuckoo Condor - 0:35', False, []],
            ['Cuckoo Condor - 0:35', False, [], ['Progressive Grab']],
            ['Cuckoo Condor - 0:35', True, ['Progressive Grab']],

            ['Cuckoo Condor - 0:55', False, []],
            ['Cuckoo Condor - 0:55', False, [], ['Progressive Grab']],
            ['Cuckoo Condor - 0:55', True, ['Progressive Grab']],
        ])

    def _test_aerodent(self):
        self.run_location_tests([
            ['Aerodent - 0:15', False, []],
            ['Aerodent - 0:15', False, [], ['Progressive Grab']],
            ['Aerodent - 0:15', True, ['Progressive Grab']],

            ['Aerodent - 0:35', False, []],
            ['Aerodent - 0:35', False, [], ['Progressive Grab']],
            ['Aerodent - 0:35', True, ['Progressive Grab']],

            ['Aerodent - 0:55', False, []],
            ['Aerodent - 0:55', False, [], ['Progressive Grab']],
            ['Aerodent - 0:55', True, ['Progressive Grab']],
        ])

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat - 0:15', False, []],
            ['Catbat - 0:15', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:15', False, [], ['Enemy Jump']],
            ['Catbat - 0:15', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Catbat - 0:35', False, []],
            ['Catbat - 0:35', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:35', False, [], ['Enemy Jump']],
            ['Catbat - 0:35', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Catbat - 0:55', False, []],
            ['Catbat - 0:55', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:55', False, [], ['Enemy Jump']],
            ['Catbat - 0:55', True, ['Progressive Ground Pound', 'Enemy Jump']],
        ])


class TestHardTreasureHunt(TestNormalTreasureHunt):
    options = {'goal': Goal.option_golden_treasure_hunt,
               'difficulty': Difficulty.option_hard}


class TestSHardTreasureHunt(TestNormalTreasureHunt):
    options = {'goal': Goal.option_golden_treasure_hunt,
               'difficulty': Difficulty.option_s_hard}

    def _test_cractus(self):
        self.run_location_tests([
            ['Cractus - 0:15', False, []],
            ['Cractus - 0:15', False, [], ['Progressive Ground Pound']],
            ['Cractus - 0:15', False, [], ['Enemy Jump']],
            ['Cractus - 0:15', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Cractus - 0:35', False, []],
            ['Cractus - 0:35', False, [], ['Progressive Ground Pound']],
            ['Cractus - 0:35', False, [], ['Enemy Jump']],
            ['Cractus - 0:35', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Cractus - 0:55', False, []],
            ['Cractus - 0:55', False, [], ['Progressive Ground Pound']],
            ['Cractus - 0:55', False, [], ['Enemy Jump']],
            ['Cractus - 0:55', True, ['Progressive Ground Pound', 'Enemy Jump']],
        ])

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat - 0:15', False, []],
            ['Catbat - 0:15', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:15', False, [], ['Enemy Jump']],
            ['Catbat - 0:15', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Catbat - 0:35', False, []],
            ['Catbat - 0:35', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:35', False, [], ['Enemy Jump']],
            ['Catbat - 0:35', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Catbat - 0:55', False, []],
            ['Catbat - 0:55', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:55', False, [], ['Enemy Jump']],
            ['Catbat - 0:55', True, ['Progressive Ground Pound', 'Enemy Jump']],
        ])


class TestNormalTreasureHuntAdvanced(TestNormalTreasureHunt):
    options = {'goal': Goal.option_golden_treasure_hunt,
               'difficulty': Difficulty.option_normal,
               'logic': Logic.option_advanced}

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat - 0:15', False, []],
            ['Catbat - 0:15', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:15', True, ['Progressive Ground Pound']],

            ['Catbat - 0:35', False, []],
            ['Catbat - 0:35', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:35', True, ['Progressive Ground Pound']],

            ['Catbat - 0:55', False, []],
            ['Catbat - 0:55', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:55', True, ['Progressive Ground Pound']],
        ])


class TestHardTreasureHuntAdvanced(TestNormalTreasureHuntAdvanced):
    options = {'goal': Goal.option_golden_treasure_hunt,
               'difficulty': Difficulty.option_hard,
               'logic': Logic.option_advanced}


class TestSHardTreasureHuntAdvanced(TestNormalTreasureHuntAdvanced):
    options = {'goal': Goal.option_golden_treasure_hunt,
               'difficulty': Difficulty.option_s_hard,
               'logic': Logic.option_advanced}

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat - 0:15', False, []],
            ['Catbat - 0:15', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:15', False, [], ['Enemy Jump']],
            ['Catbat - 0:15', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Catbat - 0:35', False, []],
            ['Catbat - 0:35', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:35', False, [], ['Enemy Jump']],
            ['Catbat - 0:35', True, ['Progressive Ground Pound', 'Enemy Jump']],

            ['Catbat - 0:55', False, []],
            ['Catbat - 0:55', False, [], ['Progressive Ground Pound']],
            ['Catbat - 0:55', False, [], ['Enemy Jump']],
            ['Catbat - 0:55', True, ['Progressive Ground Pound', 'Enemy Jump']],
        ])
