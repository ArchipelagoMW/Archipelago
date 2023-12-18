from . import TestHard, TestHardOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestEmeraldPassageHard(TestHard):

    def test_palm_tree_paradise(self):
        self.starting_regions = ['Palm Tree Paradise (entrance)']
        self.run_location_tests([
            ['Palm Tree Paradise - Ledge Box', True, []],

            ['Palm Tree Paradise - Hidden Box', True, []],

            ['Palm Tree Paradise - Platform Cave Jewel Box', True, []],

            ['Palm Tree Paradise - Ladder Cave Box', True, []],

            ['Palm Tree Paradise - CD Box', True, []],

            ['Palm Tree Paradise - Full Health Item Box', True, []],
        ])

    def test_wildflower_fields(self):
        self.starting_regions = ['Wildflower Fields (entrance)']
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
            ['Wildflower Fields - 8-Shaped Cave Box', False, [], ['Swim']],
            ['Wildflower Fields - 8-Shaped Cave Box', False, [], ['Progressive Grab']],
            ['Wildflower Fields - 8-Shaped Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim', 'Progressive Grab']],

            ['Wildflower Fields - Beezley Box', False, []],
            ['Wildflower Fields - Beezley Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Beezley Box', False, [], ['Swim']],
            ['Wildflower Fields - Beezley Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - CD Box', False, []],
            ['Wildflower Fields - CD Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - CD Box', False, [], ['Swim']],
            ['Wildflower Fields - CD Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],
        ])

    def test_mystic_lake(self):
        self.starting_regions = ['Mystic Lake (entrance)']
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
            ['Mystic Lake - Full Health Item Box', False, [], ['Swim']],
            ['Mystic Lake - Full Health Item Box', False, [], ['Head Smash']],
            ['Mystic Lake - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Mystic Lake - Full Health Item Box', True, ['Swim', 'Head Smash', 'Progressive Grab']],
        ])

    def test_monsoon_jungle(self):
        self.starting_regions = ['Monsoon Jungle (entrance)']
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
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Swim']],
            ['Monsoon Jungle - Full Health Item Box', True, ['Progressive Ground Pound', 'Swim']],
        ])

    def test_cractus(self):
        self.starting_regions = ['Emerald Passage Boss']
        self.run_location_tests([
            ['Cractus', False, []],
            ['Cractus', False, [], ['Progressive Ground Pound']],
            ['Cractus', True, ['Progressive Ground Pound']],
        ])


class TestEmeraldPassageHardOpenPortal(TestHardOpenPortal, TestEmeraldPassageHard):

    def test_wildflower_fields(self):
        self.starting_regions = ['Wildflower Fields (entrance)']
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

    def test_mystic_lake(self):
        self.starting_regions = ['Mystic Lake (entrance)']
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

    def test_monsoon_jungle(self):
        self.starting_regions = ['Monsoon Jungle (entrance)']
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
