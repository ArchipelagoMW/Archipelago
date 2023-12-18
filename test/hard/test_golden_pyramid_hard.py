from . import TestHard, TestHardOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestGoldenPyramidHard(TestHard):

    def test_golden_passage(self):
        self.starting_regions = ['Golden Passage (entrance)']
        self.run_location_tests([
            ['Golden Passage - Current Puzzle Box', False, []],
            ['Golden Passage - Current Puzzle Box', False, [], ['Swim']],
            ['Golden Passage - Current Puzzle Box', True, ['Swim']],

            ['Golden Passage - River Box', False, []],
            ['Golden Passage - River Box', False, [], ['Swim']],
            ['Golden Passage - River Box', True, ['Swim']],

            ['Golden Passage - Bat Room Box', False, []],
            ['Golden Passage - Bat Room Box', False, [], ['Swim']],
            ['Golden Passage - Bat Room Box', True, ['Swim']],

            ['Golden Passage - Mad Scienstein Box', False, []],
            ['Golden Passage - Mad Scienstein Box', False, [], ['Swim']],
            ['Golden Passage - Mad Scienstein Box', False, [], ['Progressive Ground Pound']],
            ['Golden Passage - Mad Scienstein Box', True, ['Swim', 'Progressive Ground Pound']],
        ])

    def test_golden_diva(self):
        self.starting_regions = ['Golden Pyramid Boss']
        self.run_location_tests([
            ['Golden Diva', False, []],
            ['Golden Diva', False, [], ['Progressive Grab']],
            ['Golden Diva', True, ['Progressive Grab']],
        ])


class TestGoldenPyramidHardOpenPortal(TestHardOpenPortal, TestGoldenPyramidHard):
    pass
