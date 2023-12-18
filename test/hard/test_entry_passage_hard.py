from . import TestHard, TestHardOpenPortal


# Format:
# [location, expected_result, given_items, [excluded_items]]
class TestEntryPassageHard(TestHard):

    def test_hall_of_hieroglyphs(self):
        self.starting_regions = ['Hall of Hieroglyphs (entrance)']
        self.run_location_tests([
            ['Hall of Hieroglyphs - First Jewel Box', False, []],
            ['Hall of Hieroglyphs - First Jewel Box', False, [], ['Dash Attack']],
            ['Hall of Hieroglyphs - First Jewel Box', False, [], ['Progressive Grab']],
            ['Hall of Hieroglyphs - First Jewel Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Hall of Hieroglyphs - First Jewel Box', True,
             ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Hall of Hieroglyphs - Second Jewel Box', False, []],
            ['Hall of Hieroglyphs - Second Jewel Box', False, [], ['Dash Attack']],
            ['Hall of Hieroglyphs - Second Jewel Box', False, [], ['Progressive Grab']],
            ['Hall of Hieroglyphs - Second Jewel Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Hall of Hieroglyphs - Second Jewel Box', True,
             ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Hall of Hieroglyphs - Third Jewel Box', False, []],
            ['Hall of Hieroglyphs - Third Jewel Box', False, [], ['Dash Attack']],
            ['Hall of Hieroglyphs - Third Jewel Box', False, [], ['Progressive Grab']],
            ['Hall of Hieroglyphs - Third Jewel Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Hall of Hieroglyphs - Third Jewel Box', True,
             ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Hall of Hieroglyphs - Fourth Jewel Box', False, []],
            ['Hall of Hieroglyphs - Fourth Jewel Box', False, [], ['Dash Attack']],
            ['Hall of Hieroglyphs - Fourth Jewel Box', False, [], ['Progressive Grab']],
            ['Hall of Hieroglyphs - Fourth Jewel Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Hall of Hieroglyphs - Fourth Jewel Box', True,
             ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Hall of Hieroglyphs - Full Health Item Box', False, []],
            ['Hall of Hieroglyphs - Full Health Item Box', False, [], ['Dash Attack']],
            ['Hall of Hieroglyphs - Full Health Item Box', False, [], ['Progressive Grab']],
            ['Hall of Hieroglyphs - Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Hall of Hieroglyphs - Full Health Item Box', True,
             ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],
        ])

    def test_spoiled_rotten(self):
        self.starting_regions = ['Entry Passage Boss']
        self.run_location_tests([
            ['Spoiled Rotten', True, []],
        ])


class TestEntryPassageHardOpenPortal(TestHardOpenPortal, TestEntryPassageHard):
    pass
