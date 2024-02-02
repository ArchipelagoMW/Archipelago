from .test_normal import TestNormal
from .test_hard import TestHard
from .test_s_hard import TestSHard


class TestAdvancedNormal(TestNormal):
    options = {'difficulty': 0, 'logic': 1}

    def _test_doodle_woods(self):
        self.run_location_tests([
            ['Doodle Woods - Box Behind Wall', True, []],

            ['Doodle Woods - Orange Escape Box', True, []],

            ['Doodle Woods - Buried Door Box', True, []],

            ['Doodle Woods - Blue Escape Box', True, []],

            ['Doodle Woods - CD Box', False, []],
            ['Doodle Woods - CD Box', False, [], ['Progressive Ground Pound', 'Progressive Grab']],
            ['Doodle Woods - CD Box', True, ['Progressive Ground Pound']],
            ['Doodle Woods - CD Box', True, ['Progressive Grab']],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', False, []],
            ['Domino Row - Racing Box', False, [], ['Swim']],
            ['Domino Row - Racing Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Racing Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Grab']],

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

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat', False, []],
            ['Catbat', False, [], ['Progressive Ground Pound']],
            ['Catbat', True, ['Progressive Ground Pound']],
        ])

class TestAdvancedHard(TestHard):
    options = {'difficulty': 1, 'logic': 1}

    def _test_doodle_woods(self):
        self.run_location_tests([
            ['Doodle Woods - Gray Square Box', False, []],
            ['Doodle Woods - Gray Square Box', False, [],
             ['Progressive Ground Pound', 'Progressive Grab']],
            ['Doodle Woods - Gray Square Box', True, ['Progressive Ground Pound']],
            ['Doodle Woods - Gray Square Box', True, ['Progressive Grab']],

            ['Doodle Woods - Pink Circle Box', False, []],
            ['Doodle Woods - Pink Circle Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - Pink Circle Box', True, ['Progressive Ground Pound']],

            ['Doodle Woods - Purple Square Box', True, []],

            ['Doodle Woods - Blue Circle Box', False, []],
            ['Doodle Woods - Blue Circle Box', False, [], ['Enemy Jump']],
            ['Doodle Woods - Blue Circle Box', True, ['Enemy Jump']],

            ['Doodle Woods - CD Box', True, []],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', False, []],
            ['Domino Row - Racing Box', False, [], ['Swim']],
            ['Domino Row - Racing Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Racing Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Grab']],

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

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat', False, []],
            ['Catbat', False, [], ['Progressive Ground Pound']],
            ['Catbat', True, ['Progressive Ground Pound']],
        ])

class TestAdvancedSHard(TestSHard):
    options = {'difficulty': 2, 'logic': 1}

    def _test_doodle_woods(self):
        self.run_location_tests([
            ['Doodle Woods - Gray Square Box', False, []],
            ['Doodle Woods - Gray Square Box', False, [],
             ['Progressive Ground Pound', 'Progressive Grab']],
            ['Doodle Woods - Gray Square Box', True, ['Progressive Ground Pound']],
            ['Doodle Woods - Gray Square Box', True, ['Progressive Grab']],

            ['Doodle Woods - Pink Circle Box', False, []],
            ['Doodle Woods - Pink Circle Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - Pink Circle Box', True, ['Progressive Ground Pound']],

            ['Doodle Woods - Purple Square Box', True, []],

            ['Doodle Woods - Blue Circle Box', False, []],
            ['Doodle Woods - Blue Circle Box', False, [], ['Enemy Jump']],
            ['Doodle Woods - Blue Circle Box', True, ['Enemy Jump']],

            ['Doodle Woods - CD Box', True, []],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', False, []],
            ['Domino Row - Racing Box', False, [], ['Swim']],
            ['Domino Row - Racing Box', False, [],
             ['Progressive Ground Pound', 'Head Smash', 'Progressive Grab']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Racing Box', True, ['Swim', 'Head Smash']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Grab']],

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

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat', False, []],
            ['Catbat', False, [], ['Progressive Ground Pound']],
            ['Catbat', True, ['Progressive Ground Pound']],
        ])
