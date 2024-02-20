from .TestInvertedOWG import TestInvertedOWG


class TestDarkWorld(TestInvertedOWG):

    def testSouthDarkWorld(self):
        self.run_location_tests([
            ["Hype Cave - Top", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Middle Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Middle Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Bottom", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Generous Guy", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)']],

            ["Stumpy", True, []],

            ["Digging Game", True, []],
        ])

    def testWestDarkWorld(self):
        self.run_location_tests([
            ["Brewery", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Brewery", True, ['Bomb Upgrade (+5)']],

            ["C-Shaped House", True, []],

            ["Chest Game", True, []],

            ["Peg Cave", False, []],
            ["Peg Cave", False, [], ['Hammer']],
            ["Peg Cave", True, ['Hammer', 'Pegasus Boots']],

            ["Bumper Cave Ledge", False, []],
            ["Bumper Cave Ledge", True, ['Pegasus Boots']],

            ["Blacksmith", False, []],
            ["Blacksmith", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Blacksmith", True, ['Progressive Glove', 'Progressive Glove', 'Moon Pearl']],

            ["Purple Chest", False, []],
            ["Purple Chest", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Purple Chest", True, ['Progressive Glove', 'Progressive Glove', 'Moon Pearl']],
        ])

    def testEastDarkWorld(self):
        self.run_location_tests([
            ["Catfish", False, []],
            ["Catfish", True, ['Pegasus Boots']],

            ["Pyramid", True, []],

            ["Pyramid Fairy - Left", False, []],
            ["Pyramid Fairy - Left", False, [], ['Magic Mirror']],
            ["Pyramid Fairy - Left", False, [], ['Crystal 5']],
            ["Pyramid Fairy - Left", False, [], ['Crystal 6']],
            ["Pyramid Fairy - Left", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Pegasus Boots']],

            ["Pyramid Fairy - Right", False, []],
            ["Pyramid Fairy - Right", False, [], ['Magic Mirror']],
            ["Pyramid Fairy - Right", False, [], ['Crystal 5']],
            ["Pyramid Fairy - Right", False, [], ['Crystal 6']],
            ["Pyramid Fairy - Right", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Pegasus Boots']],
        ])

    def testMireArea(self):
        self.run_location_tests([
            ["Mire Shed - Left", False, []],
            ["Mire Shed - Left", True, ['Pegasus Boots']],

            ["Mire Shed - Right", False, []],
            ["Mire Shed - Right", True, ['Pegasus Boots']],
        ])