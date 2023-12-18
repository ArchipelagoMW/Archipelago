from . import TestNormal, TestNormalOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestEmeraldPassageNormal(TestNormal):

    def test_palm_tree_paradise(self):
        self.starting_regions = ['Palm Tree Paradise (entrance)']
        self.run_location_tests([
            ['Palm Tree Paradise - First Box', True, []],

            ['Palm Tree Paradise - Box Before Cave', True, []],

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

            ['Wildflower Fields - CD Box', False, []],
            ['Wildflower Fields - CD Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - CD Box', False, [], ['Swim']],
            ['Wildflower Fields - CD Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - Full Health Item Box', False, []],
            ['Wildflower Fields - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Full Health Item Box', False, [], ['Swim']],
            ['Wildflower Fields - Full Health Item Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],
        ])

    def test_mystic_lake(self):
        self.starting_regions = ['Mystic Lake (entrance)']
        self.run_location_tests([
            ['Mystic Lake - Air Pocket Box', False, []],
            ['Mystic Lake - Air Pocket Box', False, [], ['Swim']],
            ['Mystic Lake - Air Pocket Box', False, [], ['Head Smash']],
            ['Mystic Lake - Air Pocket Box', True,
             ['Swim', 'Head Smash']],

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
            ['Mystic Lake - Full Health Item Box', False, [], ['Swim']],
            ['Mystic Lake - Full Health Item Box', False, [], ['Head Smash']],
            ['Mystic Lake - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Mystic Lake - Full Health Item Box', True,
             ['Swim', 'Head Smash', 'Progressive Grab']],
        ])

    def test_monsoon_jungle(self):
        self.starting_regions = ['Monsoon Jungle (entrance)']
        self.run_location_tests([
            ['Monsoon Jungle - Spiky Box', False, []],
            ['Monsoon Jungle - Spiky Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Spiky Box', True,
             ['Progressive Ground Pound']],

            ['Monsoon Jungle - Fat Plummet Box', False, []],
            ['Monsoon Jungle - Fat Plummet Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Fat Plummet Box', True,
             ['Progressive Ground Pound']],

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
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Swim']],
            ['Monsoon Jungle - Full Health Item Box', True,
             ['Progressive Ground Pound', 'Swim']],
        ])

    def test_cractus(self):
        self.starting_regions = ['Emerald Passage Boss']
        self.run_location_tests([
            ['Cractus', False, []],
            ['Cractus', False, [], ['Progressive Ground Pound']],
            ['Cractus', True, ['Progressive Ground Pound']],
        ])


class TestEmeraldPassageNormalOpenPortal(TestNormalOpenPortal, TestEmeraldPassageNormal):

    def test_wildflower_fields(self):
        self.starting_regions = ['Wildflower Fields (entrance)']
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

    def test_mystic_lake(self):
        self.starting_regions = ['Mystic Lake (entrance)']
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

    def test_monsoon_jungle(self):
        self.starting_regions = ['Monsoon Jungle (entrance)']
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
