from . import TestHard, TestHardOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestRubyPassageHard(TestHard):

    def test_the_curious_factory(self):
        self.starting_regions = ['The Curious Factory (entrance)']
        self.run_location_tests([
            ['The Curious Factory - Thin Gap Box', True, []],

            ['The Curious Factory - Conveyor Room Box', True, []],

            ['The Curious Factory - Underground Chamber Box', True, []],

            ['The Curious Factory - Gear Elevator Box', False, []],
            ['The Curious Factory - Gear Elevator Box', False, [], ['Dash Attack']],
            ['The Curious Factory - Gear Elevator Box', True, ['Dash Attack']],

            ['The Curious Factory - CD Box', True, []],
        ])

    def test_the_toxic_landfill(self):
        self.starting_regions = ['The Toxic Landfill (entrance)']
        self.run_location_tests([
            ['The Toxic Landfill - Box Above Portal', False, []],
            ['The Toxic Landfill - Box Above Portal', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Box Above Portal', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Box Above Portal', False, [], ['Head Smash']],
            ['The Toxic Landfill - Box Above Portal', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - Fat Room Box', False, []],
            ['The Toxic Landfill - Fat Room Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Fat Room Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Fat Room Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Fat Room Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash']],

            ['The Toxic Landfill - Current Circle Box', False, []],
            ['The Toxic Landfill - Current Circle Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Current Circle Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Current Circle Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Current Circle Box', False, [], ['Swim']],
            ['The Toxic Landfill - Current Circle Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash', 'Swim']],

            ['The Toxic Landfill - Transformation Puzzle Box', False, []],
            ['The Toxic Landfill - Transformation Puzzle Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - Transformation Puzzle Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - Transformation Puzzle Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - Transformation Puzzle Box', False, ['Progressive Grab'], ['Progressive Grab', 'Enemy Jump']],
            ['The Toxic Landfill - Transformation Puzzle Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash',
              'Progressive Grab', 'Progressive Grab']],
            ['The Toxic Landfill - Transformation Puzzle Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Dash Attack', 'Head Smash', 'Enemy Jump']],

            ['The Toxic Landfill - CD Box', False, []],
            ['The Toxic Landfill - CD Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill - CD Box', False, [], ['Dash Attack']],
            ['The Toxic Landfill - CD Box', False, [], ['Head Smash']],
            ['The Toxic Landfill - CD Box', True,
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


class TestRubyPassageHardOpenPortal(TestHardOpenPortal, TestRubyPassageHard):

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
