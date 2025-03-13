from .. import options
from . import WL4TestBase


class TestEntrances(WL4TestBase):
    def test_passage_access(self):
        self.starting_regions = []
        self.run_entrance_tests([
            ['Entry Passage Entrance', True, []],
            ['Emerald Passage Entrance', True, []],
            ['Ruby Passage Entrance', True, []],
            ['Topaz Passage Entrance', True, []],
            ['Sapphire Passage Entrance', True, []],

            ['Golden Pyramid Entrance', False, []],
            ['Golden Pyramid Entrance', False, ['Emerald Passage Clear']],
            ['Golden Pyramid Entrance', False, ['Ruby Passage Clear']],
            ['Golden Pyramid Entrance', False, ['Topaz Passage Clear']],
            ['Golden Pyramid Entrance', False, ['Sapphire Passage Clear']],
            ['Golden Pyramid Entrance', True,
             ['Emerald Passage Clear', 'Ruby Passage Clear',
              'Topaz Passage Clear', 'Sapphire Passage Clear']],
        ])


class TestEntrancesBasic(TestEntrances):
    options = {'open_doors': options.OpenDoors.option_off, 'required_jewels': 0}

#   def test_entry_levels(self):
#       self.starting_regions = ['Hall of Hieroglyphs - Entrance']
#       self.run_entrance_tests([
#           ['Entry Passage Boss Door', False, []],
#           ['Entry Passage Boss Door', False, [], ['Dash Attack']],
#           ['Entry Passage Boss Door', False, [], ['Progressive Grab']],
#           ['Entry Passage Boss Door', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
#           ['Entry Passage Boss Door', True,
#            ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],
#       ])

    def test_emerald_levels(self):
        self.starting_regions = ['Palm Tree Paradise', 'Wildflower Fields - Entrance',
                                 'Mystic Lake - Entrance', 'Monsoon Jungle - Entrance']
        self.run_entrance_tests([
            ['Wildflower Fields Entrance', True, []],

            ['Mystic Lake Entrance', False, []],
            ['Mystic Lake Entrance', False, [], ['Swim']],
            ['Mystic Lake Entrance', False,
             ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Mystic Lake Entrance', True,
             ['Swim', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Monsoon Jungle Entrance', False, []],
            ['Monsoon Jungle Entrance', False, [], ['Swim']],
            ['Monsoon Jungle Entrance', False, [], ['Head Smash']],
            ['Monsoon Jungle Entrance', True, ['Swim', 'Head Smash']],

            ['Emerald Passage Boss Door', False, []],
            ['Emerald Passage Boss Door', False, [], ['Progressive Ground Pound']],
            ['Emerald Passage Boss Door', True, ['Progressive Ground Pound']],
        ])

    def test_ruby_levels(self):
        self.starting_regions = ['The Curious Factory', 'The Toxic Landfill - Entrance',
                                 '40 Below Fridge - Entrance', 'Pinball Zone - Entrance']
        self.run_entrance_tests([
            ['The Toxic Landfill Entrance', True, []],

            ['40 Below Fridge Entrance', False, []],
            ['40 Below Fridge Entrance', False, [], ['Dash Attack']],
            ['40 Below Fridge Entrance', False, [], ['Head Smash']],
            ['40 Below Fridge Entrance', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge Entrance', True,
             ['Dash Attack', 'Head Smash', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Pinball Zone Entrance', False, []],
            ['Pinball Zone Entrance', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Pinball Zone Entrance', True, ['Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Ruby Passage Boss Door', False, []],
            ['Ruby Passage Boss Door', False, [], ['Progressive Grab']],
            ['Ruby Passage Boss Door', False, [], ['Progressive Ground Pound']],
            ['Ruby Passage Boss Door', False, [], ['Head Smash']],
            ['Ruby Passage Boss Door', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],
        ])

    def test_topaz_levels(self):
        self.starting_regions = ['Toy Block Tower - Entrance', 'The Big Board - Entrance',
                                 'Doodle Woods', 'Domino Row - Entrance']
        self.run_entrance_tests([
            ['The Big Board Entrance', False, []],
            ['The Big Board Entrance', False, ['Progressive Grab'], ['Progressive Grab']],
            ['The Big Board Entrance', True, ['Progressive Grab', 'Progressive Grab']],

            ['Doodle Woods Entrance', False, []],
            ['Doodle Woods Entrance', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods Entrance', True, ['Progressive Ground Pound']],

            ['Domino Row Entrance', True, []],

            ['Topaz Passage Boss Door', False, []],
            ['Topaz Passage Boss Door', False, [], ['Swim']],
            ['Topaz Passage Boss Door', False, [], ['Progressive Ground Pound']],
            ['Topaz Passage Boss Door', True, ['Swim', 'Progressive Ground Pound']],
        ])

    def test_sapphire_levels(self):
        self.starting_regions = ['Crescent Moon Village - Entrance', 'Arabian Night - Entrance',
                                 'Fiery Cavern - Entrance', 'Hotel Horror - Entrance']
        self.run_entrance_tests([
            ['Arabian Night Entrance', False, []],
            ['Arabian Night Entrance', False, [], ['Dash Attack']],
            ['Arabian Night Entrance', False, [], ['Head Smash']],
            ['Arabian Night Entrance', True, ['Dash Attack', 'Head Smash']],

            ['Fiery Cavern Entrance', False, []],
            ['Fiery Cavern Entrance', False, [], ['Swim']],
            ['Fiery Cavern Entrance', True, ['Swim']],

            ['Hotel Horror Entrance', False, []],
            ['Hotel Horror Entrance', False, [], ['Head Smash']],
            ['Hotel Horror Entrance', False, [], ['Dash Attack']],
            ['Hotel Horror Entrance', False, [], ['Progressive Ground Pound']],
            ['Hotel Horror Entrance', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Sapphire Passage Boss Door', False, []],
            ['Sapphire Passage Boss Door', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Sapphire Passage Boss Door', True, ['Progressive Grab', 'Progressive Grab']],
        ])

    def test_golden_pyramid(self):
        self.starting_regions = ['Golden Passage - Entrance']
        self.run_entrance_tests([
            ['Golden Pyramid Boss Door', False, []],
            ['Golden Pyramid Boss Door', False, [], ['Swim']],
            ['Golden Pyramid Boss Door', False, [], ['Progressive Ground Pound']],
            ['Golden Pyramid Boss Door', False, [], ['Progressive Grab']],
            ['Golden Pyramid Boss Door', True, ['Swim', 'Progressive Ground Pound', 'Progressive Grab']],
        ])


class TestEntrancesAdvanced(TestEntrances):
    options = {'logic': options.Logic.option_advanced, 'open_doors': options.OpenDoors.option_off, 'required_jewels': 0}

    def test_topaz_levels(self):
        self.starting_regions = ['Toy Block Tower - Entrance', 'The Big Board - Entrance',
                                 'Doodle Woods', 'Domino Row - Entrance']
        self.run_entrance_tests([
            ['The Big Board Entrance', False, []],
            ['The Big Board Entrance', False, ['Progressive Grab'], ['Progressive Grab']],
            ['The Big Board Entrance', True, ['Progressive Grab', 'Progressive Grab']],

            ['Doodle Woods Entrance', False, []],
            ['Doodle Woods Entrance', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods Entrance', True, ['Progressive Ground Pound']],

            ['Domino Row Entrance', True, []],

            ['Topaz Passage Boss Door', False, []],
            ['Topaz Passage Boss Door', False, [], ['Swim']],
            ['Topaz Passage Boss Door', False, [], ['Progressive Ground Pound', 'Head Smash',
                                            'Progressive Grab']],
            ['Topaz Passage Boss Door', True, ['Swim', 'Progressive Ground Pound']],
            ['Topaz Passage Boss Door', True, ['Swim', 'Head Smash']],
            ['Topaz Passage Boss Door', True, ['Swim', 'Progressive Grab']],
        ])


class TestEntrancesOpenPortal(TestEntrances):
    options = {'portal': options.Portal.option_open, 'open_doors': options.OpenDoors.option_off, 'required_jewels': 0}

    def test_sapphire_levels(self):
        self.starting_regions = ['Crescent Moon Village - Entrance', 'Arabian Night - Entrance',
                                 'Fiery Cavern - Entrance', 'Hotel Horror - Entrance']
        self.run_entrance_tests([
            ['Arabian Night Entrance', False, []],
            ['Arabian Night Entrance', False, [], ['Dash Attack']],
            ['Arabian Night Entrance', False, [], ['Head Smash']],
            ['Arabian Night Entrance', True, ['Dash Attack', 'Head Smash']],

            ['Fiery Cavern Entrance', True, []],

            ['Hotel Horror Entrance', False, []],
            ['Hotel Horror Entrance', False, [], ['Head Smash']],
            ['Hotel Horror Entrance', False, [], ['Dash Attack']],
            ['Hotel Horror Entrance', False, [], ['Progressive Ground Pound']],
            ['Hotel Horror Entrance', True, ['Dash Attack', 'Progressive Ground Pound', 'Head Smash']],

            ['Sapphire Passage Boss Door', True, []],
        ])


class TestEntrancesOpenDoors(TestEntrances):
    options = {'open_doors': options.OpenDoors.option_open, 'required_jewels': 0}

#   def test_entry_levels(self):
#       self.starting_regions = []
#       self.run_entrance_tests([
#           ['Entry Passage Boss Door', True, []],
#       ])

    def test_emerald_levels(self):
        self.starting_regions = []
        self.run_entrance_tests([
            ['Wildflower Fields Entrance', True, []],
            ['Mystic Lake Entrance', True, []],
            ['Monsoon Jungle Entrance', True, []],
            ['Emerald Passage Boss Door', True, []],
        ])

    def test_ruby_levels(self):
        self.starting_regions = []
        self.run_entrance_tests([
            ['The Toxic Landfill Entrance', True, []],
            ['40 Below Fridge Entrance', True, []],
            ['Pinball Zone Entrance', True, []],
            ['Ruby Passage Boss Door', True, []],
        ])

    def test_topaz_levels(self):
        self.starting_regions = []
        self.run_entrance_tests([
            ['The Big Board Entrance', True, []],
            ['Doodle Woods Entrance', True, []],
            ['Domino Row Entrance', True, []],
            ['Topaz Passage Boss Door', True, []],
        ])

    def test_sapphire_levels(self):
        self.starting_regions = []
        self.run_entrance_tests([
            ['Arabian Night Entrance', True, []],
            ['Fiery Cavern Entrance', True, []],
            ['Hotel Horror Entrance', True, []],
            ['Sapphire Passage Boss Door', True, []],
        ])

    def test_golden_pyramid(self):
        self.starting_regions = ['Golden Pyramid']
        self.run_entrance_tests([
            ['Golden Pyramid Boss Door', True, []],
        ])


class TestEntrancesOpenDoorsExceptPyramid(TestEntrancesOpenDoors):
    options = {'open_doors': options.OpenDoors.option_closed_diva, 'required_jewels': 0}

    def test_golden_pyramid(self):
        self.starting_regions = ['Golden Passage - Entrance']
        self.run_entrance_tests([
            ['Golden Pyramid Boss Door', False, []],
            ['Golden Pyramid Boss Door', False, [], ['Swim']],
            ['Golden Pyramid Boss Door', False, [], ['Progressive Ground Pound']],
            ['Golden Pyramid Boss Door', False, [], ['Progressive Grab']],
            ['Golden Pyramid Boss Door', True, ['Swim', 'Progressive Ground Pound', 'Progressive Grab']],
        ])


REQUIRED_JEWELS = options.RequiredJewels.default


class TestBossAccess(TestEntrances):
    options = {'open_doors': options.OpenDoors.option_open}

    def test_bosses(self):
        self.starting_regions = ['Monsoon Jungle - Entrance', 'Pinball Zone - Entrance',
                                 'Domino Row - Entrance', 'Hotel Horror - Entrance',
                                 'Golden Passage - Entrance']
        self.run_entrance_tests([
#           ['Entry Passage Boss Door', False, []],
#           ['Entry Passage Boss Door', False,
#            [], ['Top Right Entry Jewel Piece']],
#           ['Entry Passage Boss Door', False,
#            [], ['Top Left Entry Jewel Piece']],
#           ['Entry Passage Boss Door', False,
#            [], ['Bottom Right Entry Jewel Piece']],
#           ['Entry Passage Boss Door', False,
#            [], ['Bottom Left Entry Jewel Piece']],
#           ['Entry Passage Boss Door', True,
#            ['Top Right Entry Jewel Piece', 'Top Left Entry Jewel Piece',
#             'Bottom Right Entry Jewel Piece', 'Bottom Left Entry Jewel Piece']],

            ['Emerald Passage Boss Door', False, []],
            ['Emerald Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Emerald Piece'], ['Top Right Emerald Piece']],
            ['Emerald Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Emerald Piece'], ['Top Left Emerald Piece']],
            ['Emerald Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Emerald Piece'], ['Bottom Right Emerald Piece']],
            ['Emerald Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Emerald Piece'], ['Bottom Left Emerald Piece']],
            ['Emerald Passage Boss Door', True,
             REQUIRED_JEWELS * ['Top Right Emerald Piece', 'Top Left Emerald Piece',
                  'Bottom Right Emerald Piece', 'Bottom Left Emerald Piece']],

            ['Ruby Passage Boss Door', False, []],
            ['Ruby Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Ruby Piece'], ['Top Right Ruby Piece']],
            ['Ruby Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Ruby Piece'], ['Top Left Ruby Piece']],
            ['Ruby Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Ruby Piece'], ['Bottom Right Ruby Piece']],
            ['Ruby Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Ruby Piece'], ['Bottom Left Ruby Piece']],
            ['Ruby Passage Boss Door', True,
             REQUIRED_JEWELS * ['Top Right Ruby Piece', 'Top Left Ruby Piece',
                  'Bottom Right Ruby Piece', 'Bottom Left Ruby Piece']],

            ['Topaz Passage Boss Door', False, []],
            ['Topaz Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Topaz Piece'], ['Top Right Topaz Piece']],
            ['Topaz Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Topaz Piece'], ['Top Left Topaz Piece']],
            ['Topaz Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Topaz Piece'], ['Bottom Right Topaz Piece']],
            ['Topaz Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Topaz Piece'], ['Bottom Left Topaz Piece']],
            ['Topaz Passage Boss Door', True,
             REQUIRED_JEWELS * ['Top Right Topaz Piece', 'Top Left Topaz Piece',
                  'Bottom Right Topaz Piece', 'Bottom Left Topaz Piece']],

            ['Sapphire Passage Boss Door', False, []],
            ['Sapphire Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Sapphire Piece'], ['Top Right Sapphire Piece']],
            ['Sapphire Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Sapphire Piece'], ['Top Left Sapphire Piece']],
            ['Sapphire Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Sapphire Piece'], ['Bottom Right Sapphire Piece']],
            ['Sapphire Passage Boss Door', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Sapphire Piece'], ['Bottom Left Sapphire Piece']],
            ['Sapphire Passage Boss Door', True,
             REQUIRED_JEWELS * ['Top Right Sapphire Piece', 'Top Left Sapphire Piece',
                  'Bottom Right Sapphire Piece', 'Bottom Left Sapphire Piece']],

            ['Golden Pyramid Boss Door', False, []],
            ['Golden Pyramid Boss Door', False,
             [], ['Top Right Golden Jewel Piece']],
            ['Golden Pyramid Boss Door', False,
             [], ['Top Left Golden Jewel Piece']],
            ['Golden Pyramid Boss Door', False,
             [], ['Bottom Right Golden Jewel Piece']],
            ['Golden Pyramid Boss Door', False,
             [], ['Bottom Left Golden Jewel Piece']],
            ['Golden Pyramid Boss Door', True,
             ['Top Right Golden Jewel Piece', 'Top Left Golden Jewel Piece',
              'Bottom Right Golden Jewel Piece', 'Bottom Left Golden Jewel Piece']],
        ])


class TestBossAccessNoJewelsKeysy(TestEntrances):
    options = {
        'required_jewels': 0,
        'open_doors': options.OpenDoors.option_open,
    }
    def test_bosses(self):
        self.starting_regions = ['Golden Pyramid']
        self.run_entrance_tests([
#           ['Entry Passage Boss Door', True, []],
            ['Emerald Passage Boss Door', True, []],
            ['Ruby Passage Boss Door', True, []],
            ['Topaz Passage Boss Door', True, []],
            ['Sapphire Passage Boss Door', True, []],
            ['Golden Pyramid Boss Door', True, []],
        ])
