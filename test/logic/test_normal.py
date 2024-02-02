from .. import WL4TestBase

class TestNormal(WL4TestBase):
    options = {'difficulty': 0}

    def test_entry_passage(self):
        self.starting_regions = ['Hall of Hieroglyphs (entrance)',
                                 'Entry Passage Boss']
        self._test_hall_of_hieroglyphs()
        self._test_spoiled_rotten()

    def test_emerald_passage(self):
        self.starting_regions = ['Palm Tree Paradise (entrance)',
                                 'Wildflower Fields (entrance)',
                                 'Mystic Lake (entrance)',
                                 'Monsoon Jungle (entrance)',
                                 'Emerald Passage Boss']
        self._test_palm_tree_paradise()
        self._test_wildflower_fields()
        self._test_mystic_lake()
        self._test_monsoon_jungle()
        self._test_cractus()

    def test_ruby_passage(self):
        self.starting_regions = ['The Curious Factory (entrance)',
                                 'The Toxic Landfill (entrance)',
                                 '40 Below Fridge (entrance)',
                                 'Pinball Zone (entrance)',
                                 'Ruby Passage Boss']
        self._test_the_curious_factory()
        self._test_the_toxic_landfill()
        self._test_40_below_fridge()
        self._test_pinball_zone()
        self._test_cuckoo_condor()

    def test_topaz_passage(self):
        self.starting_regions = ['Toy Block Tower (entrance)',
                                 'The Big Board (entrance)',
                                 'Doodle Woods (entrance)',
                                 'Domino Row (entrance)',
                                 'Topaz Passage Boss']
        self._test_toy_block_tower()
        self._test_the_big_board()
        self._test_doodle_woods()
        self._test_domino_row()
        self._test_aerodent()

    def test_sapphire_passage(self):
        self.starting_regions = ['Crescent Moon Village (entrance)',
                                 'Arabian Night (entrance)',
                                 'Fiery Cavern (entrance)',
                                 'Hotel Horror (entrance)',
                                 'Sapphire Passage Boss']
        self._test_crescent_moon_village()
        self._test_arabian_night()
        self._test_fiery_cavern()
        self._test_hotel_horror()
        self._test_catbat()

    def test_golden_pyramid(self):
        self.starting_regions = ['Golden Pyramid Boss',
                                 'Golden Passage (entrance)']
        self._test_golden_passage()
        self._test_golden_diva()

    def _test_hall_of_hieroglyphs(self):
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

    def _test_spoiled_rotten(self):
        self.run_location_tests([
            ['Spoiled Rotten', True, []],
        ])

    def _test_palm_tree_paradise(self):
        self.run_location_tests([
            ['Palm Tree Paradise - First Box', True, []],

            ['Palm Tree Paradise - Box Before Cave', True, []],

            ['Palm Tree Paradise - Platform Cave Jewel Box', True, []],

            ['Palm Tree Paradise - Ladder Cave Box', True, []],

            ['Palm Tree Paradise - CD Box', True, []],

            ['Palm Tree Paradise - Full Health Item Box', True, []],
        ])

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

    def _test_mystic_lake(self):
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

    def _test_monsoon_jungle(self):
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

    def _test_cractus(self):
        self.run_location_tests([
            ['Cractus', False, []],
            ['Cractus', False, [], ['Progressive Ground Pound']],
            ['Cractus', True, ['Progressive Ground Pound']],
        ])

    def _test_the_curious_factory(self):
        self.run_location_tests([
            ['The Curious Factory - First Drop Box', True, []],

            ['The Curious Factory - Early Escape Box', True, []],

            ['The Curious Factory - Late Escape Box', True, []],

            ['The Curious Factory - Frog Switch Room Box', True, []],

            ['The Curious Factory - CD Box', True, []],
        ])

    def _test_the_toxic_landfill(self):
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

    def _test_40_below_fridge(self):
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

    def _test_pinball_zone(self):
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

    def _test_cuckoo_condor(self):
        self.run_location_tests([
            ['Cuckoo Condor', False, []],
            ['Cuckoo Condor', False, [], ['Progressive Grab']],
            ['Cuckoo Condor', True, ['Progressive Grab']],
        ])

    def _test_toy_block_tower(self):
        self.run_location_tests([
            ['Toy Block Tower - Toy Car Overhang Box', False, []],
            ['Toy Block Tower - Toy Car Overhang Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Toy Car Overhang Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Hidden Tower Room Box', False, []],
            ['Toy Block Tower - Hidden Tower Room Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Hidden Tower Room Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Fire Box', False, []],
            ['Toy Block Tower - Fire Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Fire Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Red Pipe Box', False, []],
            ['Toy Block Tower - Red Pipe Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Red Pipe Box', True,
             ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - CD Box', False, []],
            ['Toy Block Tower - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - CD Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Full Health Item Box', False, []],
            ['Toy Block Tower - Full Health Item Box', False,
             ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Full Health Item Box', False, [], ['Dash Attack']],
            ['Toy Block Tower - Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Grab', 'Dash Attack']],
        ])

    def _test_the_big_board(self):
        self.run_location_tests([
            ['The Big Board - First Box', False, []],
            ['The Big Board - First Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - First Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Normal Fire Room Box', False, []],
            ['The Big Board - Normal Fire Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Normal Fire Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Normal Enemy Room Box', False, []],
            ['The Big Board - Normal Enemy Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Normal Enemy Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Toy Car Box', False, []],
            ['The Big Board - Toy Car Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Toy Car Box', True, ['Progressive Ground Pound']],

            ['The Big Board - CD Box', False, []],
            ['The Big Board - CD Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - CD Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Full Health Item Box', False, []],
            ['The Big Board - Full Health Item Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Full Health Item Box', False, [], ['Progressive Grab']],
            ['The Big Board - Full Health Item Box', False, [], ['Enemy Jump']],
            ['The Big Board - Full Health Item Box', True,
             ['Progressive Ground Pound', 'Progressive Grab', 'Enemy Jump']],
        ])

    def _test_doodle_woods(self):
        self.run_location_tests([
            ['Doodle Woods - Box Behind Wall', True, []],

            ['Doodle Woods - Orange Escape Box', True, []],

            ['Doodle Woods - Buried Door Box', True, []],

            ['Doodle Woods - Blue Escape Box', True, []],

            ['Doodle Woods - CD Box', False, []],
            ['Doodle Woods - CD Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - CD Box', True, ['Progressive Ground Pound']],
        ])

    def _test_domino_row(self):
        self.run_location_tests([
            ['Domino Row - Racing Box', False, []],
            ['Domino Row - Racing Box', False, [], ['Swim']],
            ['Domino Row - Racing Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Racing Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - Rolling Box', False, []],
            ['Domino Row - Rolling Box', False, [], ['Swim']],
            ['Domino Row - Rolling Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Rolling Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - Swimming Detour Box', False, []],
            ['Domino Row - Swimming Detour Box', False, [], ['Swim']],
            ['Domino Row - Swimming Detour Box', False, [], ['Head Smash']],
            ['Domino Row - Swimming Detour Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Swimming Detour Box', True,
             ['Swim', 'Progressive Ground Pound', 'Head Smash']],

            ['Domino Row - Keyzer Room Box', False, []],
            ['Domino Row - Keyzer Room Box', False, [], ['Swim']],
            ['Domino Row - Keyzer Room Box', False, [], ['Progressive Ground Pound']],
            ['Domino Row - Keyzer Room Box', True, ['Swim', 'Progressive Ground Pound']],

            ['Domino Row - CD Box', False, []],
            ['Domino Row - CD Box', False, [], ['Swim']],
            ['Domino Row - CD Box', True, ['Swim', 'Progressive Ground Pound']],
        ])

    def _test_aerodent(self):
        self.run_location_tests([
            ['Aerodent', False, []],
            ['Aerodent', False, [], ['Progressive Grab']],
            ['Aerodent', True, ['Progressive Grab']],
        ])

    def _test_crescent_moon_village(self):
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

    def _test_arabian_night(self):
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

    def _test_fiery_cavern(self):
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

    def _test_hotel_horror(self):
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

    def _test_catbat(self):
        self.run_location_tests([
            ['Catbat', False, []],
            ['Catbat', False, [], ['Progressive Ground Pound']],
            ['Catbat', False, [], ['Enemy Jump']],
            ['Catbat', True, ['Progressive Ground Pound', 'Enemy Jump']],
        ])

    def _test_golden_passage(self):
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

    def _test_golden_diva(self):
        self.run_location_tests([
            ['Golden Diva', False, []],
            ['Golden Diva', False, [], ['Progressive Grab']],
            ['Golden Diva', True, ['Progressive Grab']],
        ])
