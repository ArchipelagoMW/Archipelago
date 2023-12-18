from . import TestNormal, TestNormalOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestRubyPassageNormal(TestNormal):

    def test_the_curious_factory(self):
        self.starting_regions = ['The Curious Factory (entrance)']
        self.run_location_tests([
            ['The Curious Factory - First Drop Box', True, []],

            ['The Curious Factory - Early Escape Box', True, []],

            ['The Curious Factory - Late Escape Box', True, []],

            ['The Curious Factory - Frog Switch Room Box', True, []],

            ['The Curious Factory - CD Box', True, []],
        ])

    def test_the_toxic_landfill(self):
        self.starting_regions = ['The Toxic Landfill (entrance)']
        self.run_location_tests([
            ['The Toxic Landfill - Portal Room Box', False, []],
            ['The Toxic Landfill - Portal Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Portal Room Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Portal Room Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Portal Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - Fat Room Box', False, []],
            ['The Toxic Landfill - Fat Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Fat Room Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Fat Room Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Fat Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - Spring Room Box', False, []],
            ['The Toxic Landfill - Spring Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Spring Room Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Spring Room Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Spring Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - Ledge Box', False, []],
            ['The Toxic Landfill - Ledge Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Ledge Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Ledge Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Ledge Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - CD Box', False, []],
            ['The Toxic Landfill - CD Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - CD Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - CD Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - CD Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - Full Health Item Box', False, []],
            ['The Toxic Landfill - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Full Health Item Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Full Health Item Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Full Health Item Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],
        ])

    def test_40_below_fridge(self):
        self.starting_regions = ['40 Below Fridge (entrance)']
        self.run_location_tests([
            ['40 Below Fridge - Looping Room Box', False, []],
            ['40 Below Fridge - Looping Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge - Looping Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound']],

            ['40 Below Fridge - Maze Room Box', False, []],
            ['40 Below Fridge - Maze Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge - Maze Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound']],

            ['40 Below Fridge - Snowman Puzzle Upper Box', False, []],
            ['40 Below Fridge - Snowman Puzzle Upper Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge - Snowman Puzzle Upper Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound']],

            ['40 Below Fridge - Snowman Puzzle Lower Box', False, []],
            ['40 Below Fridge - Snowman Puzzle Lower Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge - Snowman Puzzle Lower Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound']],

            ['40 Below Fridge - CD Box', False, []],
            ['40 Below Fridge - CD Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge - CD Box', False, [], ['Head Smash']],
            ['40 Below Fridge - CD Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Head Smash']],
        ])

    def test_pinball_zone(self):
        self.starting_regions = ['Pinball Zone (entrance)']
        self.run_location_tests([
            ['Pinball Zone - Rolling Room Box', False, []],
            ['Pinball Zone - Rolling Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Rolling Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Rolling Room Box', False, [], ['Head Smash']],
            ['Pinball Zone - Rolling Room Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],

            ['Pinball Zone - Fruit Room Box', False, []],
            ['Pinball Zone - Fruit Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Fruit Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Fruit Room Box', False, [], ['Head Smash']],
            ['Pinball Zone - Fruit Room Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],

            ['Pinball Zone - Jungle Room Box', False, []],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Jungle Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Jungle Room Box', False, [], ['Head Smash']],
            ['Pinball Zone - Jungle Room Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],

            ['Pinball Zone - Snow Room Box', False, []],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Snow Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Snow Room Box', False, [], ['Head Smash']],
            ['Pinball Zone - Snow Room Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],

            ['Pinball Zone - CD Box', False, []],
            ['Pinball Zone - CD Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - CD Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - CD Box', False, [], ['Head Smash']],
            ['Pinball Zone - CD Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],

            ['Pinball Zone - Full Health Item Box', False, []],
            ['Pinball Zone - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Pinball Zone - Full Health Item Box', False, [], ['Head Smash']],
            ['Pinball Zone - Full Health Item Box', False,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],
            ['Pinball Zone - Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound', 'Head Smash']],
        ])

    def test_cuckoo_condor(self):
        self.starting_regions = ['Ruby Passage Boss']
        self.run_location_tests([
            ['Cuckoo Condor', False, []],
            ['Cuckoo Condor', False, [], ['Progressive Grab']],
            ['Cuckoo Condor', True, ['Progressive Grab']],
        ])


class TestRubyPassageNormalOpenPortal(TestNormalOpenPortal, TestRubyPassageNormal):

    def test_pinball_zone(self):
        self.starting_regions = ['Pinball Zone (entrance)']
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
