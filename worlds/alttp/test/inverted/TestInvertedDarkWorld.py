from .TestInverted import TestInverted


class TestInvertedDarkWorld(TestInverted):

    def testNorthWest(self):
        self.run_location_tests([
            ["Brewery", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Brewery", True, ['Bomb Upgrade (+5)']],

            ["C-Shaped House", True, []],

            ["Chest Game", True, []],

            ["Peg Cave", False, []],
            ["Peg Cave", False, [], ['Hammer']],
            ["Peg Cave", False, [], ['Progressive Glove', 'Magic Mirror']],
            ["Peg Cave", True, ['Hammer', 'Progressive Glove', 'Progressive Glove']],
            ["Peg Cave", True, ['Hammer', 'Progressive Glove', 'Magic Mirror', 'Moon Pearl']],
            ["Peg Cave", True, ['Hammer', 'Beat Agahnim 1', 'Magic Mirror']],

            ["Bumper Cave Ledge", False, []],
            ["Bumper Cave Ledge", False, [], ['Moon Pearl']],
            ["Bumper Cave Ledge", False, [], ['Cape']],
            ["Bumper Cave Ledge", False, [], ['Progressive Glove']],
            ["Bumper Cave Ledge", False, [], ['Magic Mirror']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Magic Mirror', 'Progressive Glove', 'Hammer']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Magic Mirror', 'Progressive Glove', 'Beat Agahnim 1']],

            ["Blacksmith", False, []],
            ["Blacksmith", False, [], ['Progressive Glove', 'Magic Mirror']],
            ["Blacksmith", True, ['Progressive Glove', 'Progressive Glove', 'Moon Pearl']],
            ["Blacksmith", True, ['Beat Agahnim 1', 'Magic Mirror']],
            ["Blacksmith", True, ['Progressive Glove', 'Hammer', 'Magic Mirror', 'Moon Pearl']],

            ["Purple Chest", False, []],
            ["Purple Chest", False, [], ['Progressive Glove', 'Magic Mirror']],
            ["Purple Chest", True, ['Progressive Glove', 'Progressive Glove', 'Moon Pearl']],
            ["Purple Chest", True, ['Beat Agahnim 1', 'Magic Mirror']],
            ["Purple Chest", True, ['Progressive Glove', 'Hammer', 'Magic Mirror', 'Moon Pearl']],
        ])

    def testNorthEast(self):
        self.run_location_tests([
            ["Catfish", False, []],
            ["Catfish", False, [], ['Progressive Glove', 'Flippers']],
            ["Catfish", False, [], ['Progressive Glove', 'Magic Mirror']],
            ["Catfish", False, [], ['Progressive Glove', 'Moon Pearl']],
            ["Catfish", True, ['Beat Agahnim 1', 'Magic Mirror', 'Progressive Glove']],
            ["Catfish", True, ['Beat Agahnim 1', 'Moon Pearl', 'Magic Mirror', 'Flippers']],
            ["Catfish", True, ['Progressive Glove', 'Hammer']],
            ["Catfish", True, ['Progressive Glove', 'Flippers']],
            ["Catfish", True, ['Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Moon Pearl']],

            ["Pyramid", False, []],
            ["Pyramid", True, ['Beat Agahnim 1', 'Magic Mirror']],
            ["Pyramid", True, ['Hammer']],
            ["Pyramid", True, ['Flippers']],
            ["Pyramid", True, ['Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Moon Pearl']],

            ["Pyramid Fairy - Left", False, []],
            ["Pyramid Fairy - Left", False, [], ['Magic Mirror']],
            ["Pyramid Fairy - Left", False, [], ['Crystal 5']],
            ["Pyramid Fairy - Left", False, [], ['Crystal 6']],
            ["Pyramid Fairy - Left", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Hammer', 'Progressive Glove', 'Moon Pearl']],
            ["Pyramid Fairy - Left", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Moon Pearl']],
            ["Pyramid Fairy - Left", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Beat Agahnim 1']],

            ["Pyramid Fairy - Right", False, []],
            ["Pyramid Fairy - Right", False, [], ['Magic Mirror']],
            ["Pyramid Fairy - Right", False, [], ['Crystal 5']],
            ["Pyramid Fairy - Right", False, [], ['Crystal 6']],
            ["Pyramid Fairy - Right", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Hammer', 'Progressive Glove', 'Moon Pearl']],
            ["Pyramid Fairy - Right", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Moon Pearl']],
            ["Pyramid Fairy - Right", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Beat Agahnim 1']],
        ])

    def testSouth(self):
        self.run_location_tests([
            ["Hype Cave - Top", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Middle Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Middle Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Bottom", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Generous Guy", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)']],

            ["Stumpy", True, []],

            ["Digging Game", True, []],

            ["Link's House", True, []],
        ])

    def testMireArea(self):
        self.run_location_tests([
            ["Mire Shed - Left", False, []],
            ["Mire Shed - Left", True, ['Flute']],
            ["Mire Shed - Left", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Mire Shed - Right", False, []],
            ["Mire Shed - Right", True, ['Flute']],
            ["Mire Shed - Right", True, ['Magic Mirror', 'Beat Agahnim 1']],

        ])