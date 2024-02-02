from .. import WL4TestBase

class TestSHard(WL4TestBase):
    options = {'difficulty': 2}

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
            ['Palm Tree Paradise - Dead End Box', True, []],

            ['Palm Tree Paradise - Hidden Box', True, []],

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

            ['Wildflower Fields - Sunflower Box', False, []],
            ['Wildflower Fields - Sunflower Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - Sunflower Box', False, [], ['Swim']],
            ['Wildflower Fields - Sunflower Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim']],

            ['Wildflower Fields - 8-Shaped Cave Box', False, []],
            ['Wildflower Fields - 8-Shaped Cave Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields - 8-Shaped Cave Box', False, [], ['Swim']],
            ['Wildflower Fields - 8-Shaped Cave Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Wildflower Fields - 8-Shaped Cave Box', True,
             ['Progressive Ground Pound', 'Progressive Ground Pound', 'Swim', 'Progressive Grab', 'Progressive Grab']],

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

    def _test_mystic_lake(self):
        self.run_location_tests([
            ['Mystic Lake - Large Cave Box', False, []],
            ['Mystic Lake - Large Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Large Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Large Cave Box', True, ['Swim', 'Head Smash']],

            ['Mystic Lake - Rock Cave Box', False, []],
            ['Mystic Lake - Rock Cave Box', False, [], ['Swim']],
            ['Mystic Lake - Rock Cave Box', False, [], ['Head Smash']],
            ['Mystic Lake - Rock Cave Box', False, [], ['Progressive Grab']],
            ['Mystic Lake - Rock Cave Box', True, ['Swim', 'Head Smash', 'Progressive Grab']],

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
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle - Full Health Item Box', False, [], ['Swim']],
            ['Monsoon Jungle - Full Health Item Box', True, ['Progressive Ground Pound', 'Swim']],
        ])

    def _test_cractus(self):
        self.run_location_tests([
            ['Cractus', False, []],
            ['Cractus', False, [], ['Progressive Ground Pound']],
            ['Cractus', True, ['Progressive Ground Pound']],
        ])

    def _test_the_curious_factory(self):
        self.run_location_tests([
            ['The Curious Factory - Thin Gap Box', True, []],

            ['The Curious Factory - Conveyor Room Box', True, []],

            ['The Curious Factory - Underground Chamber Box', True, []],

            ['The Curious Factory - Gear Elevator Box', False, []],
            ['The Curious Factory - Gear Elevator Box', False, [], ['Dash Attack']],
            ['The Curious Factory - Gear Elevator Box', True, ['Dash Attack']],

            ['The Curious Factory - CD Box', True, []],
        ])

    def _test_the_toxic_landfill(self):
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
            ['Pinball Zone - Switch Room Box', False, []],
            ['Pinball Zone - Switch Room Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Switch Room Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Switch Room Box', False, [], ['Head Smash']],
            ['Pinball Zone - Switch Room Box', True,
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

            ['Pinball Zone - Pink Room Full Health Item Box', False, []],
            ['Pinball Zone - Pink Room Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Pink Room Full Health Item Box', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Pinball Zone - Pink Room Full Health Item Box', False, [], ['Head Smash']],
            ['Pinball Zone - Pink Room Full Health Item Box', False,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],
            ['Pinball Zone - Pink Room Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound', 'Head Smash']],

            ['Pinball Zone - Rolling Room Full Health Item Box', False, []],
            ['Pinball Zone - Rolling Room Full Health Item Box', False, [], ['Progressive Grab']],
            ['Pinball Zone - Rolling Room Full Health Item Box', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone - Rolling Room Full Health Item Box', False, [], ['Head Smash']],
            ['Pinball Zone - Rolling Room Full Health Item Box', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],
        ])

    def _test_cuckoo_condor(self):
        self.run_location_tests([
            ['Cuckoo Condor', False, []],
            ['Cuckoo Condor', False, [], ['Progressive Grab']],
            ['Cuckoo Condor', True, ['Progressive Grab']],
        ])

    def _test_toy_block_tower(self):
        self.run_location_tests([
            ['Toy Block Tower - Tower Exterior Top Box', False, []],
            ['Toy Block Tower - Tower Exterior Top Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Tower Exterior Top Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Digging Room Box', False, []],
            ['Toy Block Tower - Digging Room Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Digging Room Box', False, [], ['Dash Attack']],
            ['Toy Block Tower - Digging Room Box', True, ['Progressive Grab', 'Progressive Grab', 'Dash Attack']],

            ['Toy Block Tower - Bonfire Block Box', False, []],
            ['Toy Block Tower - Bonfire Block Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Bonfire Block Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - Escape Ledge Box', False, []],
            ['Toy Block Tower - Escape Ledge Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - Escape Ledge Box', True, ['Progressive Grab', 'Progressive Grab']],

            ['Toy Block Tower - CD Box', False, []],
            ['Toy Block Tower - CD Box', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower - CD Box', True, ['Progressive Grab', 'Progressive Grab']],
        ])

    def _test_the_big_board(self):
        self.run_location_tests([
            ['The Big Board - Hard Fire Room Box', False, []],
            ['The Big Board - Hard Fire Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Hard Fire Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Hard Enemy Room Box', False, []],
            ['The Big Board - Hard Enemy Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Hard Enemy Room Box', False, [], ['Progressive Grab']],
            ['The Big Board - Hard Enemy Room Box', True, ['Progressive Ground Pound', 'Progressive Grab']],

            ['The Big Board - Fat Room Box', False, []],
            ['The Big Board - Fat Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Fat Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - Flat Room Box', False, []],
            ['The Big Board - Flat Room Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - Flat Room Box', True, ['Progressive Ground Pound']],

            ['The Big Board - CD Box', False, []],
            ['The Big Board - CD Box', False, [], ['Progressive Ground Pound']],
            ['The Big Board - CD Box', True, ['Progressive Ground Pound']],
        ])

    def _test_doodle_woods(self):
        self.run_location_tests([
            ['Doodle Woods - Gray Square Box', False, []],
            ['Doodle Woods - Gray Square Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - Gray Square Box', True, ['Progressive Ground Pound']],

            ['Doodle Woods - Pink Circle Box', False, []],
            ['Doodle Woods - Pink Circle Box', False, [], ['Progressive Ground Pound']],
            ['Doodle Woods - Pink Circle Box', True, ['Progressive Ground Pound']],

            ['Doodle Woods - Purple Square Box', True, []],

            ['Doodle Woods - Blue Circle Box', False, []],
            ['Doodle Woods - Blue Circle Box', False, [], ['Enemy Jump']],
            ['Doodle Woods - Blue Circle Box', True, ['Enemy Jump']],

            ['Doodle Woods - CD Box', True, []],
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

    def _test_aerodent(self):
        self.run_location_tests([
            ['Aerodent', False, []],
            ['Aerodent', False, [], ['Progressive Grab']],
            ['Aerodent', True, ['Progressive Grab']],
        ])

    def _test_crescent_moon_village(self):
        self.run_location_tests([
            ['Crescent Moon Village - Agile Bat Hidden Box', False, []],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Head Smash']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Dash Attack']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Ground Pound']],
            ['Crescent Moon Village - Agile Bat Hidden Box', False, [], ['Progressive Grab']],
            ['Crescent Moon Village - Agile Bat Hidden Box', True,
             ['Head Smash', 'Dash Attack', 'Progressive Ground Pound', 'Progressive Grab']],

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
            ['Arabian Night - Onomi Box', False, [], ['Swim']],
            ['Arabian Night - Onomi Box', False, [], ['Progressive Ground Pound', 'Head Smash']],
            ['Arabian Night - Onomi Box', True, ['Swim', 'Progressive Ground Pound']],
            ['Arabian Night - Onomi Box', True, ['Swim', 'Head Smash']],

            ['Arabian Night - Flying Carpet Dash Attack Box', False, []],
            ['Arabian Night - Flying Carpet Dash Attack Box', False, [], ['Swim']],
            ['Arabian Night - Flying Carpet Dash Attack Box', False, [], ['Dash Attack']],
            ['Arabian Night - Flying Carpet Dash Attack Box', True, ['Swim', 'Dash Attack']],

            ['Arabian Night - Kool-Aid Box', False, []],
            ['Arabian Night - Kool-Aid Box', False, [], ['Swim']],
            ['Arabian Night - Kool-Aid Box', False, [], ['Dash Attack']],
            ['Arabian Night - Kool-Aid Box', True, ['Swim', 'Dash Attack']],

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
            ['Hotel Horror - Room 102 Box', True, []],
            ['Hotel Horror - Room 303 Box', True, []],
            ['Hotel Horror - Room 402 Box', True, []],
            ['Hotel Horror - Exterior Box', True, []],
            ['Hotel Horror - CD Box', True, []],
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
