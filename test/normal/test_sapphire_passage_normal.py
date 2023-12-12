from . import TestNormal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestSapphirePassageNormal(TestNormal):

    def test_crescent_moon_village(self):
        self.starting_regions = ['Crescent Moon Village (entrance)']
        self.run_location_tests([
            ['Crescent Moon Village - Agile Bat Box', False, []],
            ['Crescent Moon Village - Agile Bat Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Agile Bat Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Agile Bat Box', True, ['Head Smash', 'Dash Attack']],

            ['Crescent Moon Village - Metal Platform Box', False, []],
            ['Crescent Moon Village - Metal Platform Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Metal Platform Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Metal Platform Box', True, ['Head Smash', 'Dash Attack']],

            ['Crescent Moon Village - Rolling Box', False, []],
            ['Crescent Moon Village - Rolling Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Rolling Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Rolling Box', True, ['Head Smash', 'Dash Attack']],

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
            ['Arabian Night - Onomi Box', True, ['Swim']],

            ['Arabian Night - Flying Carpet Overhang Box', False, []],
            ['Arabian Night - Flying Carpet Overhang Box', False, [], ['Swim']],
            ['Arabian Night - Flying Carpet Overhang Box', True, ['Swim']],

            ['Arabian Night - Zombie Plummet Box', False, []],
            ['Arabian Night - Zombie Plummet Box', False, [], ['Swim']],
            ['Arabian Night - Zombie Plummet Box', True, ['Swim']],

            ['Arabian Night - Sewer Box', False, []],
            ['Arabian Night - Sewer Box', False, [], ['Swim']],
            ['Arabian Night - Sewer Box', True, ['Swim']],

            ['Arabian Night - CD Box', False, []],
            ['Arabian Night - CD Box', False, [], ['Swim']],
            ['Arabian Night - CD Box', True, ['Swim']],
        ])

    def test_fiery_cavern(self):
        self.starting_regions = ['Fiery Cavern (entrance)']
        self.run_location_tests([
            ['Fiery Cavern - Lava Dodging Box', False, []],
            ['Fiery Cavern - Lava Dodging Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Lava Dodging Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Lava Dodging Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Lava Dodging Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

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
            ['Hotel Horror - 1F Hallway Box', False, []],
            ['Hotel Horror - 1F Hallway Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - 1F Hallway Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Hotel Horror - 2F Hallway Box', False, []],
            ['Hotel Horror - 2F Hallway Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - 2F Hallway Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Hotel Horror - 3F Hallway Box', False, []],
            ['Hotel Horror - 3F Hallway Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - 3F Hallway Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Hotel Horror - 4F Hallway Box', False, []],
            ['Hotel Horror - 4F Hallway Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - 4F Hallway Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Hotel Horror - CD Box', False, []],
            ['Hotel Horror - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - CD Box', True, ['Progressive Grab', 'Progressive Grab']],
        ])

    def test_catbat(self):
        self.starting_regions = ['Sapphire Passage Boss']
        self.run_location_tests([
            ['Catbat', False, []],
            ['Catbat', False, [], ['Progressive Ground Pound']],
            ['Catbat', True, ['Progressive Ground Pound']],
        ])
