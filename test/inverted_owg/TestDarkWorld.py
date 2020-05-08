from test.inverted_owg.TestInvertedOWG import TestInvertedOWG


class TestDarkWorld(TestInvertedOWG):

    def testSouthDarkWorld(self):
        self.run_location_tests([
            ["Hype Cave - Top", True, []],

            ["Hype Cave - Middle Right", True, []],

            ["Hype Cave - Middle Left", True, []],

            ["Hype Cave - Bottom", True, []],

            ["Hype Cave - Generous Guy", True, []],

            ["Stumpy", True, []],

            ["Digging Game", True, []],
        ])

    def testWestDarkWorld(self):
        self.run_location_tests([
            ["Brewery", True, []],

            ["C-Shaped House", True, []],

            ["Chest Game", True, []],

            ["Peg Cave", False, []],
            ["Peg Cave", False, [], ['Hammer']],
            ["Peg Cave", True, ['Hammer', 'Pegasus Boots']],

            ["Bumper Cave Ledge", False, []],
            ["Bumper Cave Ledge", True, ['Pegasus Boots']],

            ["Blacksmith", False, []],
            ["Blacksmith", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Blacksmith", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots', 'Moon Pearl']],

            ["Purple Chest", False, []],
            ["Purple Chest", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Purple Chest", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots', 'Moon Pearl']],
        ])

    def testEastDarkWorld(self):
        self.run_location_tests([
            ["Catfish", False, []],
            ["Catfish", True, ['Pegasus Boots']],

            #todo: Qirn Jump
            #["Pyramid", True, []],
            ["Pyramid", False, []],
            ["Pyramid", True, ['Pegasus Boots']],
            ["Pyramid", True, ['Flippers']],

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