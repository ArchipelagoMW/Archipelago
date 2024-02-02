from ...options import Difficulty, Logic, Portal
from .test_advanced import TestAdvancedNormal, TestAdvancedHard, TestAdvancedSHard
from .test_open_portals import TestNormalOpenPortal, TestHardOpenPortal, TestSHardOpenPortal


class TestAdvancedNormalOpenPortal(TestAdvancedNormal, TestNormalOpenPortal):
    options = {'difficulty': Difficulty.option_normal,
               'logic': Logic.option_advanced,
               'portal': Portal.option_open}

    def _test_pinball_zone(self):
        self.run_location_tests([
            ['Pinball Zone - Rolling Room Box', False, []],
            ['Pinball Zone - Rolling Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Rolling Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Fruit Room Box', False, []],
            ['Pinball Zone - Fruit Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Fruit Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Jungle Room Box', False, []],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Jungle Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [],
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [],
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - Full Health Item Box', False, []],
            ['Pinball Zone - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Pinball Zone - Full Health Item Box', False, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', True, []],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Grab']],

            ['Domino Row - Swimming Detour Box', False, []],
            ['Domino Row - Swimming Detour Box', False, [], ['Swim']],
            ['Domino Row - Swimming Detour Box', False, [], ['Head Smash']],
            ['Domino Row - Swimming Detour Box', True, ['Swim', 'Head Smash']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Grab']],
        ])


class TestAdvancedHardOpenPortal(TestAdvancedHard, TestHardOpenPortal):
    options = {'difficulty': Difficulty.option_hard,
               'logic': Logic.option_advanced,
               'portal': Portal.option_open}

    def _test_pinball_zone(self):
        self.run_location_tests([
            ['Pinball Zone - Rolling Room Box', False, []],
            ['Pinball Zone - Rolling Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Rolling Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Fruit Room Box', False, []],
            ['Pinball Zone - Fruit Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Fruit Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Jungle Room Box', False, []],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Jungle Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [],
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [],
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - Full Health Item Box', False, []],
            ['Pinball Zone - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Pinball Zone - Full Health Item Box', False, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', True, []],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Grab']],

            ['Domino Row - Swimming Detour Box', False, []],
            ['Domino Row - Swimming Detour Box', False, [], ['Swim']],
            ['Domino Row - Swimming Detour Box', False, [], ['Head Smash']],
            ['Domino Row - Swimming Detour Box', True, ['Swim', 'Head Smash']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Grab']],
        ])


class TestAdvancedSHardOpenPortal(TestAdvancedSHard, TestSHardOpenPortal):
    options = {'difficulty': Difficulty.option_s_hard,
               'logic': Logic.option_advanced,
               'portal': Portal.option_open}

    def _test_pinball_zone(self):
        self.run_location_tests([
            ['Pinball Zone - Switch Room Box', False, []],
            ['Pinball Zone - Switch Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Switch Room Box', False,
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - Switch Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Switch Room Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - Fruit Room Box', False, []],
            ['Pinball Zone - Fruit Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Fruit Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Jungle Room Box', False, []],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Jungle Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [],
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [],
             ['Progressive Grab'], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Pinball Zone - Pink Room Full Health Item Box', False, []],
            ['Pinball Zone - Pink Room Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Pink Room Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Pinball Zone - Pink Room Full Health Item Box', False, ['Progressive Grab', 'Progressive Ground Pound']],
            ['Pinball Zone - Pink Room Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Pinball Zone - Rolling Room Full Health Item Box', False, []],
            ['Pinball Zone - Rolling Room Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Rolling Room Full Health Item Box', True, ['Progressive Grab']],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', True, []],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Grab']],

            ['Domino Row - Swimming Room Escape Box', False, []],
            ['Domino Row - Swimming Room Escape Box', False, [], ['Swim']],
            ['Domino Row - Swimming Room Escape Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Swimming Room Escape Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Grab']],
        ])
