from . import TestNormal, TestNormalOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestTopazPassageNormal(TestNormal):

    def test_toy_block_tower(self):
        self.starting_regions = ['Toy Block Tower (entrance)']
        self.run_location_tests([
            ['Toy Block Tower - Toy Car Overhang Box', False, []],
            ['Toy Block Tower - Toy Car Overhang Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Toy Car Overhang Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Hidden Tower Room Box', False, []],
            ['Toy Block Tower - Hidden Tower Room Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Hidden Tower Room Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Fire Box', False, []],
            ['Toy Block Tower - Fire Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Fire Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Red Pipe Box', False, []],
            ['Toy Block Tower - Red Pipe Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Red Pipe Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - CD Box', False, []],
            ['Toy Block Tower - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - CD Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Full Health Item Box', False, []],
            ['Toy Block Tower - Full Health Item Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Full Health Item Box', False, [], ['Dash Attack']],
            ['Toy Block Tower - Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Grab', 'Dash Attack']],
        ])

    def test_the_big_board(self):
        self.starting_regions = ['The Big Board (entrance)']
        self.run_location_tests([
            ['The Big Board - First Box', False, []],
            ['The Big Board - First Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - First Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Normal Fire Room Box', False, []],
            ['The Big Board - Normal Fire Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Normal Fire Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Normal Enemy Room Box', False, []],
            ['The Big Board - Normal Enemy Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Normal Enemy Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Toy Car Box', False, []],
            ['The Big Board - Toy Car Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Toy Car Box', True, ['Progressive Ground Pound']],

            ['The Big Board - CD Box', False, []],
            ['The Big Board - CD Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - CD Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Full Health Item Box', False, []],
            ['The Big Board - Full Health Item Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Full Health Item Box', False, [], ['Progressive Grab']],
            ['The Big Board - Full Health Item Box', False, [], ['Enemy Jump']],
            ['The Big Board - Full Health Item Box', True,
             ['Progressive Ground Pound', 'Progressive Grab', 'Enemy Jump']],
        ])

    def test_doodle_woods(self):
        self.starting_regions = ['Doodle Woods (entrance)']
        self.run_location_tests([
            ['Doodle Woods - Box Behind Wall', True, []],

            ['Doodle Woods - Orange Escape Box', True, []],

            ['Doodle Woods - Buried Door Box', True, []],

            ['Doodle Woods - Blue Escape Box', True, []],

            ['Doodle Woods - CD Box', False, []],
            ['Doodle Woods - CD Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - CD Box', True, ['Progressive Ground Pound']],
        ])

    def test_domino_row(self):
        self.starting_regions = ['Domino Row (entrance)']
        self.run_location_tests([
            ['Domino Row - Racing Box', False, []],
            ['Domino Row - Racing Box', False, [], ['Swim']],
            ['Domino Row - Racing Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Racing Box', True, ['Swim', 'Head Smash']],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Head Smash']],

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
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Head Smash']],
        ])

    def test_aerodent(self):
        self.starting_regions = ['Topaz Passage Boss']
        self.run_location_tests([
            ['Aerodent', False, []],
            ['Aerodent', False, [], ['Progressive Grab']],
            ['Aerodent', True, ['Progressive Grab']],
        ])


class TestTopazPassageNormalOpenPortal(TestNormalOpenPortal, TestTopazPassageNormal):

    def test_domino_row(self):
        self.starting_regions = ['Domino Row (entrance)']
        self.run_location_tests([
            ['Domino Row - Racing Box', True, []],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Head Smash']],

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
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Head Smash']],
        ])
