from .test_normal import TestNormal
from .test_hard import TestHard
from .test_s_hard import TestSHard

class TestNormalOpenPortal(TestNormal):
    options = {'difficulty': 0, 'portal': 1}

    def _test_wildflower_fields(self):
        self.run_location_tests([
            ['Wildflower Fields - Current Cave Box', False, []],
            ['Wildflower Fields - Current Cave Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Current Cave Box', False, [], ['Swim']],
            ['Wildflower Fields - Current Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - Sunflower Jewel Box', False, []],
            ['Wildflower Fields - Sunflower Jewel Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Sunflower Jewel Box', False, [], ['Swim']],
            ['Wildflower Fields - Sunflower Jewel Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - Slope Room Box', False, []],
            ['Wildflower Fields - Slope Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Slope Room Box', False, [], ['Swim']],
            ['Wildflower Fields - Slope Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - Beezley Box', False, []],
            ['Wildflower Fields - Beezley Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Beezley Box', False, [], ['Swim']],
            ['Wildflower Fields - Beezley Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - CD Box', True, []],

            ['Wildflower Fields - Full Health Item Box', False, []],
            ['Wildflower Fields - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Full Health Item Box', False, [], ['Swim']],
            ['Wildflower Fields - Full Health Item Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],
        ])

    def _test_mystic_lake(self):
        self.run_location_tests([
            ['Mystic Lake - Air Pocket Box', False, []],
            ['Mystic Lake - Air Pocket Box', False, [], ['Swim']],
            ['Mystic Lake - Air Pocket Box', True, ['Swim']],

            ['Mystic Lake - Hill Room Box', False, []],
            ['Mystic Lake - Hill Room Box', False, [], ['Swim']],
            ['Mystic Lake - Hill Room Box', False, [], ['Head Smash']],
            ['Mystic Lake - Hill Room Box', True,
             ['Swim', 'Head Smash']],

            ['Mystic Lake - Cavern Box', False, []],
            ['Mystic Lake - Cavern Box', False, [], ['Swim']],
            ['Mystic Lake - Cavern Box', False, [], ['Head Smash']],
            ['Mystic Lake - Cavern Box', True,
             ['Swim', 'Head Smash']],

            ['Mystic Lake - Box Before Bridge', False, []],
            ['Mystic Lake - Box Before Bridge', False, [], ['Swim']],
            ['Mystic Lake - Box Before Bridge', False, [], ['Head Smash']],
            ['Mystic Lake - Box Before Bridge', True,
             ['Swim', 'Head Smash']],

            ['Mystic Lake - CD Box', False, []],
            ['Mystic Lake - CD Box', False, [], ['Swim']],
            ['Mystic Lake - CD Box', False, [], ['Head Smash']],
            ['Mystic Lake - CD Box', False, [], ['Dash Attack']],
            ['Mystic Lake - CD Box', True,
             ['Swim', 'Head Smash', 'Dash Attack']],

            ['Mystic Lake - Full Health Item Box', False, []],
            ['Mystic Lake - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Mystic Lake - Full Health Item Box', True, ['Progressive Grab']],
        ])

    def _test_monsoon_jungle(self):
        self.run_location_tests([
            ['Monsoon Jungle - Spiky Box', False, []],
            ['Monsoon Jungle - Spiky Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Spiky Box', True,
             ['Progressive Ground Pound']],

            ['Monsoon Jungle - Fat Plummet Box', True, []],

            ['Monsoon Jungle - Descent Box', False, []],
            ['Monsoon Jungle - Descent Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Descent Box', True,
             ['Progressive Ground Pound']],

            ['Monsoon Jungle - Buried Cave Box', False, []],
            ['Monsoon Jungle - Buried Cave Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Buried Cave Box', True,
             ['Progressive Ground Pound']],

            ['Monsoon Jungle - CD Box', False, []],
            ['Monsoon Jungle - CD Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - CD Box', True,
             ['Progressive Ground Pound']],

            ['Monsoon Jungle - Full Health Item Box', False, []],
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Swim']],
            ['Monsoon Jungle - Full Health Item Box', True, ['Swim']],
        ])

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
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Jungle Room Box', True,
             ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

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
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - Swimming Detour Box', False, []],
            ['Domino Row - Swimming Detour Box', False, [], ['Swim']],
            ['Domino Row - Swimming Detour Box', False, [], ['Head Smash']],
            ['Domino Row - Swimming Detour Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Swimming Detour Box', True,
             ['Swim', 'Head Smash', 'Progressive Ground Pound']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
        ])

    def _test_crescent_moon_village(self):
        self.run_location_tests([
            ['Crescent Moon Village - Agile Bat Box', False, []],
            ['Crescent Moon Village - Agile Bat Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Agile Bat Box', True, ['Head Smash']],

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

    def _test_arabian_night(self):
        self.run_location_tests([
            ['Arabian Night - Onomi Box', True, []],

            ['Arabian Night - Flying Carpet Overhang Box', True, []],

            ['Arabian Night - Zombie Plummet Box', True, []],

            ['Arabian Night - Sewer Box', False, []],
            ['Arabian Night - Sewer Box', False, [], ['Swim']],
            ['Arabian Night - Sewer Box', True, ['Swim']],

            ['Arabian Night - CD Box', False, []],
            ['Arabian Night - CD Box', False, [], ['Swim']],
            ['Arabian Night - CD Box', True, ['Swim']],
        ])

    def _test_fiery_cavern(self):
        self.run_location_tests([
            ['Fiery Cavern - Lava Dodging Box', True, []],

            ['Fiery Cavern - Long Lava Geyser Box', True, []],

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

    def _test_hotel_horror(self):
        self.run_location_tests([
            ['Hotel Horror - 1F Hallway Box', True, []],

            ['Hotel Horror - 2F Hallway Box', True, []],

            ['Hotel Horror - 3F Hallway Box', True, []],

            ['Hotel Horror - 4F Hallway Box', True, []],

            ['Hotel Horror - CD Box', False, []],
            ['Hotel Horror - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - CD Box', True, ['Progressive Grab', 'Progressive Grab']],
        ])

class TestHardOpenPortal(TestHard):
    options = {'difficulty': 1, 'portal': 1}

    def _test_wildflower_fields(self):
        self.run_location_tests([
            ['Wildflower Fields - Current Cave Box', False, []],
            ['Wildflower Fields - Current Cave Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Current Cave Box', False, [], ['Swim']],
            ['Wildflower Fields - Current Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - Sunflower Box', False, []],
            ['Wildflower Fields - Sunflower Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Sunflower Box', False, [], ['Swim']],
            ['Wildflower Fields - Sunflower Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - 8-Shaped Cave Box', False, []],
            ['Wildflower Fields - 8-Shaped Cave Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - 8-Shaped Cave Box', False, [], ['Progressive Grab']],
            ['Wildflower Fields - 8-Shaped Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Progressive Grab']],

            ['Wildflower Fields - Beezley Box', False, []],
            ['Wildflower Fields - Beezley Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Beezley Box', False, [], ['Swim']],
            ['Wildflower Fields - Beezley Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - CD Box', True, []],
        ])

    def _test_mystic_lake(self):
        self.run_location_tests([
            ['Mystic Lake - Large Cave Box', False, []],
            ['Mystic Lake - Large Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Large Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Large Cave Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - Small Cave Box', False, []],
            ['Mystic Lake - Small Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Small Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Small Cave Box', False, [], ['Dash Attack']],
            ['Mystic Lake - Small Cave Box', True, ['Swim', 'Head Smash', 'Dash Attack']],

            ['Mystic Lake - Spring Cave Box', False, []],
            ['Mystic Lake - Spring Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Spring Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Spring Cave Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - Lake Exit Bubble Box', False, []],
            ['Mystic Lake - Lake Exit Bubble Box', False, [], ['Swim']],
            ['Mystic Lake - Lake Exit Bubble Box', False, [], ['Head Smash']],
            ['Mystic Lake - Lake Exit Bubble Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - CD Box', False, []],
            ['Mystic Lake - CD Box', False, [], ['Swim']],
            ['Mystic Lake - CD Box', False, [], ['Head Smash']],
            ['Mystic Lake - CD Box', False, [], ['Dash Attack']],
            ['Mystic Lake - CD Box', True, ['Swim', 'Head Smash', 'Dash Attack']],

            ['Mystic Lake - Full Health Item Box', False, []],
            ['Mystic Lake - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Mystic Lake - Full Health Item Box', True, ['Progressive Grab']],
        ])

    def _test_monsoon_jungle(self):
        self.run_location_tests([
            ['Monsoon Jungle - Escape Climb Box', False, []],
            ['Monsoon Jungle - Escape Climb Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Escape Climb Box', True, ['Progressive Ground Pound']],

            ['Monsoon Jungle - Fat Plummet Box', False, []],
            ['Monsoon Jungle - Fat Plummet Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Fat Plummet Box', True, ['Progressive Ground Pound']],

            ['Monsoon Jungle - Puffy Hallway Box', False, []],
            ['Monsoon Jungle - Puffy Hallway Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Puffy Hallway Box', False, [], ['Dash Attack']],
            ['Monsoon Jungle - Puffy Hallway Box', True,
             ['Progressive Ground Pound', 'Dash Attack']],

            ['Monsoon Jungle - Buried Cave Box', False, []],
            ['Monsoon Jungle - Buried Cave Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Buried Cave Box', False, [], ['Progressive Grab']],
            ['Monsoon Jungle - Buried Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Grab']],

            ['Monsoon Jungle - CD Box', False, []],
            ['Monsoon Jungle - CD Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - CD Box', True, ['Progressive Ground Pound']],

            ['Monsoon Jungle - Full Health Item Box', False, []],
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Swim']],
            ['Monsoon Jungle - Full Health Item Box', True, ['Swim']],
        ])

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
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Jungle Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

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
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - Swimming Detour Box', False, []],
            ['Domino Row - Swimming Detour Box', False, [], ['Swim']],
            ['Domino Row - Swimming Detour Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Swimming Detour Box', False, [], ['Head Smash']],
            ['Domino Row - Swimming Detour Box', True,
             ['Swim', 'Head Smash', 'Progressive Ground Pound']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
        ])

    def _test_crescent_moon_village(self):
        self.run_location_tests([
            ['Crescent Moon Village - Agile Bat Hidden Box', False, []],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Ground Pound']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Grab']],
            ['Crescent Moon Village - Agile Bat Hidden Box', True,
             ['Head Smash', 'Progressive Ground Pound', 'Progressive Grab']],

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

    def _test_arabian_night(self):
        self.run_location_tests([
            # FIXME: You can use the enemies here, too
            ['Arabian Night - Onomi Box', False, []],
            ['Arabian Night - Onomi Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Arabian Night - Onomi Box', True, ['Progressive Ground Pound']],
            ['Arabian Night - Onomi Box', True, ['Head Smash']],

            ['Arabian Night - Flying Carpet Dash Attack Box', False, []],
            ['Arabian Night - Flying Carpet Dash Attack Box', False, [], ['Dash Attack']],
            ['Arabian Night - Flying Carpet Dash Attack Box', True, ['Dash Attack']],

            ['Arabian Night - Kool-Aid Box', False, []],
            ['Arabian Night - Kool-Aid Box', False, [], ['Dash Attack']],
            ['Arabian Night - Kool-Aid Box', True, ['Dash Attack']],

            ['Arabian Night - Sewer Box', False, []],
            ['Arabian Night - Sewer Box', False, [], ['Swim']],
            ['Arabian Night - Sewer Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Arabian Night - Sewer Box', True, ['Swim', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Arabian Night - CD Box', False, []],
            ['Arabian Night - CD Box', False, [], ['Swim']],
            ['Arabian Night - CD Box', True, ['Swim']],
        ])

    def _test_fiery_cavern(self):
        self.run_location_tests([
            ['Fiery Cavern - Ice Beyond Door Box', False, []],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Ice Beyond Door Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Fiery Cavern - Long Lava Geyser Box', True, []],

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

    def _test_hotel_horror(self):
        self.run_location_tests([
            ['Hotel Horror - Room 102 Box', True, []],

            ['Hotel Horror - Room 303 Box', True, []],

            ['Hotel Horror - Room 402 Box', True, []],

            ['Hotel Horror - Exterior Box', True, []],

            ['Hotel Horror - CD Box', False, []],
            ['Hotel Horror - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror - CD Box', True, ['Progressive Grab', 'Progressive Grab']],
        ])

class TestSHardOpenPortal(TestSHard):
    options = {'difficulty': 2, 'portal': 1}

    def _test_wildflower_fields(self):
        self.run_location_tests([
            ['Wildflower Fields - Current Cave Box', False, []],
            ['Wildflower Fields - Current Cave Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Current Cave Box', False, [], ['Swim']],
            ['Wildflower Fields - Current Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - Sunflower Box', False, []],
            ['Wildflower Fields - Sunflower Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Sunflower Box', False, [], ['Swim']],
            ['Wildflower Fields - Sunflower Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - 8-Shaped Cave Box', False, []],
            ['Wildflower Fields - 8-Shaped Cave Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - 8-Shaped Cave Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Wildflower Fields - 8-Shaped Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Progressive Grab', 'Progressive Grab']],

            ['Wildflower Fields - Beezley Box', False, []],
            ['Wildflower Fields - Beezley Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Beezley Box', False, [], ['Swim']],
            ['Wildflower Fields - Beezley Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - CD Box', True, []],
        ])

    def _test_mystic_lake(self):
        self.run_location_tests([
            ['Mystic Lake - Large Cave Box', False, []],
            ['Mystic Lake - Large Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Large Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Large Cave Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - Rock Cave Box', False, []],
            ['Mystic Lake - Rock Cave Box', False, [], ['Progressive Grab']],
            ['Mystic Lake - Rock Cave Box', True, ['Progressive Grab']],

            ['Mystic Lake - Spring Cave Box', False, []],
            ['Mystic Lake - Spring Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Spring Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Spring Cave Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - Lake Exit Bubble Box', False, []],
            ['Mystic Lake - Lake Exit Bubble Box', False, [], ['Swim']],
            ['Mystic Lake - Lake Exit Bubble Box', False, [], ['Head Smash']],
            ['Mystic Lake - Lake Exit Bubble Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - CD Box', False, []],
            ['Mystic Lake - CD Box', False, [], ['Swim']],
            ['Mystic Lake - CD Box', False, [], ['Head Smash']],
            ['Mystic Lake - CD Box', False, [], ['Dash Attack']],
            ['Mystic Lake - CD Box', True, ['Swim', 'Head Smash', 'Dash Attack']],

            ['Mystic Lake - Full Health Item Box', False, []],
            ['Mystic Lake - Full Health Item Box', False, [], ['Swim']],
            ['Mystic Lake - Full Health Item Box', False, [], ['Head Smash']],
            ['Mystic Lake - Full Health Item Box', False, [], ['Dash Attack']],
            ['Mystic Lake - Full Health Item Box', True, ['Swim', 'Head Smash', 'Dash Attack']],
        ])

    def _test_monsoon_jungle(self):
        self.run_location_tests([
            ['Monsoon Jungle - Brown Pipe Cave Box', False, []],
            ['Monsoon Jungle - Brown Pipe Cave Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Brown Pipe Cave Box', True, ['Progressive Ground Pound']],

            ['Monsoon Jungle - Fat Plummet Box', False, []],
            ['Monsoon Jungle - Fat Plummet Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Fat Plummet Box', True, ['Progressive Ground Pound']],

            ['Monsoon Jungle - Puffy Hallway Box', False, []],
            ['Monsoon Jungle - Puffy Hallway Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Puffy Hallway Box', False, [], ['Dash Attack']],
            ['Monsoon Jungle - Puffy Hallway Box', True,
             ['Progressive Ground Pound', 'Dash Attack']],

            ['Monsoon Jungle - Buried Cave Box', False, []],
            ['Monsoon Jungle - Buried Cave Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Buried Cave Box', False, [], ['Progressive Grab']],
            ['Monsoon Jungle - Buried Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Grab']],

            ['Monsoon Jungle - CD Box', False, []],
            ['Monsoon Jungle - CD Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - CD Box', True, ['Progressive Ground Pound']],

            ['Monsoon Jungle - Full Health Item Box', False, []],
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Swim']],
            ['Monsoon Jungle - Full Health Item Box', True, ['Swim']],
        ])

    def _test_pinball_zone(self):
        self.run_location_tests([
            ['Pinball Zone - Switch Room Box', False, []],
            ['Pinball Zone - Switch Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Switch Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Switch Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - Fruit Room Box', False, []],
            ['Pinball Zone - Fruit Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Fruit Room Box', True, ['Progressive Grab']],

            ['Pinball Zone - Jungle Room Box', False, []],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Jungle Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - CD Box', True, ['Progressive Grab', 'Progressive Ground Pound']],

            ['Pinball Zone - Pink Room Full Health Item Box', False, []],
            ['Pinball Zone - Pink Room Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Pink Room Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
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
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],

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
            ['Domino Row - CD Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
        ])

    def _test_crescent_moon_village(self):
        self.run_location_tests([
            ['Crescent Moon Village - Agile Bat Hidden Box', False, []],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Ground Pound']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Grab']],
            ['Crescent Moon Village - Agile Bat Hidden Box', True,
             ['Head Smash', 'Progressive Ground Pound', 'Progressive Grab']],

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

    def _test_arabian_night(self):
        self.run_location_tests([
            ['Arabian Night - Onomi Box', False, []],
            ['Arabian Night - Onomi Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Arabian Night - Onomi Box', True, ['Progressive Ground Pound']],
            ['Arabian Night - Onomi Box', True, ['Head Smash']],

            ['Arabian Night - Flying Carpet Dash Attack Box', False, []],
            ['Arabian Night - Flying Carpet Dash Attack Box', False, [], ['Dash Attack']],
            ['Arabian Night - Flying Carpet Dash Attack Box', True, ['Dash Attack']],

            ['Arabian Night - Kool-Aid Box', False, []],
            ['Arabian Night - Kool-Aid Box', False, [], ['Dash Attack']],
            ['Arabian Night - Kool-Aid Box', True, ['Dash Attack']],

            ['Arabian Night - Sewer Box', False, []],
            ['Arabian Night - Sewer Box', False, [], ['Swim']],
            ['Arabian Night - Sewer Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Arabian Night - Sewer Box', True, ['Swim', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Arabian Night - CD Box', False, []],
            ['Arabian Night - CD Box', False, [], ['Swim']],
            ['Arabian Night - CD Box', True, ['Swim']],
        ])

    def _test_fiery_cavern(self):
        self.run_location_tests([
            ['Fiery Cavern - Ice Beyond Door Box', False, []],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Head Smash']],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Dash Attack']],
            ['Fiery Cavern - Ice Beyond Door Box', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern - Ice Beyond Door Box', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Fiery Cavern - Long Lava Geyser Box', True, []],

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
