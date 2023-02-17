from .TestInvertedMinor import TestInvertedMinor


class TestInvertedDarkWorld(TestInvertedMinor):

    def testNorthWest(self):
        self.run_location_tests([
            ["Brewery", True, []],

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
            ["Catfish", True, ['Beat Agahnim 1', 'Moon Pearl', 'Magic Mirror']],
            ["Catfish", True, ['Progressive Glove']],

            ["Pyramid", True, []],

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
            ["Hype Cave - Top", True, []],

            ["Hype Cave - Middle Right", True, []],

            ["Hype Cave - Middle Left", True, []],

            ["Hype Cave - Bottom", True, []],

            ["Hype Cave - Generous Guy", True, []],

            ["Stumpy", True, []],

            ["Digging Game", True, []],

            ["Link's House", True, []],
        ])

    def testMireArea(self):
        self.run_location_tests([
            ["Mire Shed - Left", False, []],
            ["Mire Shed - Left", False, [], ['Flute', 'Magic Mirror']],
            ["Mire Shed - Left", True, ['Flute']],

            ["Mire Shed - Right", False, []],
            ["Mire Shed - Right", False, [], ['Flute', 'Magic Mirror']],
            ["Mire Shed - Right", True, ['Flute']],
        ])