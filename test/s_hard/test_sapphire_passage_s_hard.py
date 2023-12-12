from . import TestSHard


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestSapphirePassageSHard(TestSHard):

    def test_crescent_moon_village(self):
        self.starting_regions = ['Crescent Moon Village (entrance)']
        self.run_location_tests([
            ['Crescent Moon Village - Agile Bat Hidden Box', False, []],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Ground Pound']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Grab']],
            ['Crescent Moon Village - Agile Bat Hidden Box', True,
             ['Head Smash', 'Dash Attack', 'Progressive Ground Pound', 'Progressive Grab']],

            ['Crescent Moon Village - Metal Platform Rolling Box', False, []],
            ['Crescent Moon Village - Metal Platform Rolling Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Metal Platform Rolling Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Metal Platform Rolling Box', True, ['Head Smash', 'Dash Attack']],

            ['Crescent Moon Village - !-Switch Rolling Box', False, []],
            ['Crescent Moon Village - !-Switch Rolling Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - !-Switch Rolling Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - !-Switch Rolling Box', True, ['Head Smash', 'Dash Attack']],

            ['Crescent Moon Village - Sewer Box', False, []],
            ['Crescent Moon Village - Sewer Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Sewer Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Sewer Box', False, [], ['Swim']],
            ['Crescent Moon Village - Sewer Box', True, ['Head Smash', 'Dash Attack', 'Swim']],

            ['Crescent Moon Village - CD Box', False, []],
            ['Crescent Moon Village - CD Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - CD Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - CD Box', True, ['Head Smash', 'Dash Attack']],
        ])

    def test_arabian_night(self):
        self.starting_regions = ['Arabian Night (entrance)']
        self.run_location_tests([
            ['Arabian Night - Onomi Box', False, []],
            ['Arabian Night - Onomi Box', False, [], ['Swim']],
            ['Arabian Night - Onomi Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Arabian Night - Onomi Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Arabian Night - Onomi Box', True, ['Swim', 'Head Smash']],

            ['Arabian Night - Flying Carpet Dash Attack Box', False, []],
            ['Arabian Night - Flying Carpet Dash Attack Box', False, [], ['Swim']],
            ['Arabian Night - Flying Carpet Dash Attack Box', False, [], ['Dash Attack']],
            ['Arabian Night - Flying Carpet Dash Attack Box', True, ['Swim', 'Dash Attack']],

            ['Arabian Night - Kool-Aid Box', False, []],
            ['Arabian Night - Kool-Aid Box', False, [], ['Swim']],
            ['Arabian Night - Kool-Aid Box', False, [], ['Dash Attack']],
            ['Arabian Night - Kool-Aid Box', True, ['Swim', 'Dash Attack']],

            ['Arabian Night - Sewer Box', False, []],
            ['Arabian Night - Sewer Box', False, [], ['Swim']],
            ['Arabian Night - Sewer Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Arabian Night - Sewer Box', True, ['Swim', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Arabian Night - CD Box', False, []],
            ['Arabian Night - CD Box', False, [], ['Swim']],
            ['Arabian Night - CD Box', True, ['Swim']],
        ])

    def test_fiery_cavern(self):
        self.starting_regions = ['Fiery Cavern (entrance)']
        self.run_location_tests([
            ['Fiery Cavern - Ice Beyond Door Box', False, []],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Ice Beyond Door Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Fiery Cavern - Long Lava Geyser Box', False, []],
            ['Fiery Cavern - Long Lava Geyser Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Long Lava Geyser Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Long Lava Geyser Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Long Lava Geyser Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Fiery Cavern - Ice Detour Box', False, []],
            ['Fiery Cavern - Ice Detour Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Ice Detour Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Ice Detour Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Ice Detour Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Fiery Cavern - Snowman Box', False, []],
            ['Fiery Cavern - Snowman Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Snowman Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Snowman Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Snowman Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Fiery Cavern - CD Box', False, []],
            ['Fiery Cavern - CD Box', False, [], ['Head Smash']],
            ['Fiery Cavern - CD Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - CD Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - CD Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],
        ])

    def test_hotel_horror(self):
        self.starting_regions = ['Hotel Horror (entrance)']
        self.run_location_tests([
            ['Hotel Horror - Room 102 Box', True, []],
            ['Hotel Horror - Room 303 Box', True, []],
            ['Hotel Horror - Room 402 Box', True, []],
            ['Hotel Horror - Exterior Box', True, []],
            ['Hotel Horror - CD Box', True, []],
        ])

    def test_catbat(self):
        self.starting_regions = ['Sapphire Passage Boss']
        self.run_location_tests([
            ['Catbat', False, []],
            ['Catbat', False, [], ['Progressive Ground Pound']],
            ['Catbat', True, ['Progressive Ground Pound']],
        ])
