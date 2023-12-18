from . import TestSHard, TestSHardOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestTopazPassageSHard(TestSHard):

    def test_toy_block_tower(self):
        self.starting_regions = ['Toy Block Tower (entrance)']
        self.run_location_tests([
            ['Toy Block Tower - Tower Exterior Top Box', False, []],
            ['Toy Block Tower - Tower Exterior Top Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Tower Exterior Top Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Digging Room Box', False, []],
            ['Toy Block Tower - Digging Room Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Digging Room Box', False, [], ['Dash Attack']],
            ['Toy Block Tower - Digging Room Box', True, ['Progressive Grab', 'Progressive Grab', 'Dash Attack']],

            ['Toy Block Tower - Bonfire Block Box', False, []],
            ['Toy Block Tower - Bonfire Block Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Bonfire Block Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Escape Ledge Box', False, []],
            ['Toy Block Tower - Escape Ledge Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Escape Ledge Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - CD Box', False, []],
            ['Toy Block Tower - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - CD Box', True, ['Progressive Grab', 'Progressive Grab']],
        ])

    def test_the_big_board(self):
        self.starting_regions = ['The Big Board (entrance)']
        self.run_location_tests([
            ['The Big Board - Hard Fire Room Box', False, []],
            ['The Big Board - Hard Fire Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Hard Fire Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Hard Enemy Room Box', False, []],
            ['The Big Board - Hard Enemy Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Hard Enemy Room Box', False, [], ['Progressive Grab']],
            ['The Big Board - Hard Enemy Room Box', True, ['Progressive Ground Pound', 'Progressive Grab']],

            ['The Big Board - Fat Room Box', False, []],
            ['The Big Board - Fat Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Fat Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Flat Room Box', False, []],
            ['The Big Board - Flat Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Flat Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - CD Box', False, []],
            ['The Big Board - CD Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - CD Box', True, ['Progressive Ground Pound']],
        ])

    def test_doodle_woods(self):
        self.starting_regions = ['Doodle Woods (entrance)']
        self.run_location_tests([
            ['Doodle Woods - Gray Square Box', False, []],
            ['Doodle Woods - Gray Square Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - Gray Square Box', True, ['Progressive Ground Pound']],

            ['Doodle Woods - Pink Circle Box', False, []],
            ['Doodle Woods - Pink Circle Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - Pink Circle Box', True, ['Progressive Ground Pound']],

            ['Doodle Woods - Purple Square Box', True, []],

            ['Doodle Woods - Blue Circle Box', False, []],
            ['Doodle Woods - Blue Circle Box', False, [], ['Enemy Jump']],
            ['Doodle Woods - Blue Circle Box', True, ['Enemy Jump']],

            ['Doodle Woods - CD Box', True, []],
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

            ['Domino Row - Swimming Room Escape Box', False, []],
            ['Domino Row - Swimming Room Escape Box', False, [], ['Swim']],
            ['Domino Row - Swimming Room Escape Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Domino Row - Swimming Room Escape Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Swimming Room Escape Box', True, ['Swim', 'Head Smash']],

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


class TestTopazPassageSHardOpenPortal(TestSHardOpenPortal, TestTopazPassageSHard):

    def test_domino_row(self):
        self.starting_regions = ['Domino Row (entrance)']
        self.run_location_tests([
            ['Domino Row - Racing Box', True, []],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Head Smash']],

            ['Domino Row - Swimming Room Escape Box', False, []],
            ['Domino Row - Swimming Room Escape Box', False, [], ['Swim']],
            ['Domino Row - Swimming Room Escape Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Domino Row - Swimming Room Escape Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - Swimming Room Escape Box', True, ['Swim', 'Head Smash']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Head Smash']],
        ])
