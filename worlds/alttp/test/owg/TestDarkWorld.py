from .TestVanillaOWG import TestVanillaOWG


class TestDarkWorld(TestVanillaOWG):

    def testSouthDarkWorld(self):
        self.run_location_tests([
            ["Hype Cave - Top", False, []],
            ["Hype Cave - Top", False, [], ['Moon Pearl']],
            ["Hype Cave - Top", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hype Cave - Top", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Top", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Top", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Top", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Top", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Middle Right", False, []],
            ["Hype Cave - Middle Right", False, [], ['Moon Pearl']],
            ["Hype Cave - Middle Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hype Cave - Middle Right", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Middle Right", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Middle Right", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Middle Right", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Middle Right", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Middle Left", False, []],
            ["Hype Cave - Middle Left", False, [], ['Moon Pearl']],
            ["Hype Cave - Middle Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hype Cave - Middle Left", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Middle Left", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Middle Left", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Middle Left", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Middle Left", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Bottom", False, []],
            ["Hype Cave - Bottom", False, [], ['Moon Pearl']],
            ["Hype Cave - Bottom", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hype Cave - Bottom", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Bottom", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Bottom", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Bottom", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Bottom", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Generous Guy", False, []],
            ["Hype Cave - Generous Guy", False, [], ['Moon Pearl']],
            ["Hype Cave - Generous Guy", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hype Cave - Generous Guy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Generous Guy", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Generous Guy", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Generous Guy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Generous Guy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Stumpy", False, []],
            ["Stumpy", False, [], ['Moon Pearl']],
            ["Stumpy", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Stumpy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Stumpy", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Stumpy", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Stumpy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Stumpy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Digging Game", False, []],
            ["Digging Game", False, [], ['Moon Pearl']],
            ["Digging Game", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Digging Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Digging Game", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Digging Game", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Digging Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Digging Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']]
        ])

    def testEastDarkWorld(self):
        self.run_location_tests([
            ["Catfish", False, []],
            ["Catfish", False, [], ['Moon Pearl']],
            ["Catfish", False, [], ['Progressive Glove', 'Pegasus Boots']],
            ["Catfish", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Catfish", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove']],
            ["Catfish", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Catfish", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Pyramid", False, []],
            ["Pyramid", False, [], ['Beat Agahnim 1', 'Moon Pearl', 'Magic Mirror']],
            ["Pyramid", False, [], ['Beat Agahnim 1', 'Moon Pearl', 'Pegasus Boots']],
            ["Pyramid", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Pyramid", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Pyramid", True, ['Beat Agahnim 1']],
            ["Pyramid", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Pyramid", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Pyramid Fairy - Left", False, []],
            ["Pyramid Fairy - Left", False, [], ['Pegasus Boots', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Pyramid Fairy - Left", False, [], ['Pegasus Boots', 'Moon Pearl', 'Crystal 5']],
            ["Pyramid Fairy - Left", False, [], ['Pegasus Boots', 'Moon Pearl', 'Crystal 6']],
            ["Pyramid Fairy - Left", False, [], ['Magic Mirror', 'Crystal 5']],
            ["Pyramid Fairy - Left", False, [], ['Magic Mirror', 'Crystal 6']],
            ["Pyramid Fairy - Left", False, [], ['Magic Mirror', 'Moon Pearl']],
            ["Pyramid Fairy - Left", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Hammer']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Progressive Glove', 'Hammer']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot', 'Magic Mirror']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Flippers', 'Hookshot', 'Magic Mirror']],
            ["Pyramid Fairy - Left", True, ['Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Flute', 'Magic Mirror']],
            ["Pyramid Fairy - Left", True, ['Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Lamp', 'Magic Mirror']],

            ["Pyramid Fairy - Right", False, []],
            ["Pyramid Fairy - Right", False, [], ['Pegasus Boots', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Pyramid Fairy - Right", False, [], ['Pegasus Boots', 'Moon Pearl', 'Crystal 5']],
            ["Pyramid Fairy - Right", False, [], ['Pegasus Boots', 'Moon Pearl', 'Crystal 6']],
            ["Pyramid Fairy - Right", False, [], ['Magic Mirror', 'Crystal 5']],
            ["Pyramid Fairy - Right", False, [], ['Magic Mirror', 'Crystal 6']],
            ["Pyramid Fairy - Right", False, [], ['Magic Mirror', 'Moon Pearl']],
            ["Pyramid Fairy - Right", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Hammer']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Progressive Glove', 'Hammer']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot', 'Magic Mirror']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Flippers', 'Hookshot', 'Magic Mirror']],
            ["Pyramid Fairy - Right", True, ['Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Flute', 'Magic Mirror']],
            ["Pyramid Fairy - Right", True, ['Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Lamp', 'Magic Mirror']],

            ["Ganon", False, []],
            ["Ganon", False, [], ['Moon Pearl']],
            ["Ganon", False, [], ['Beat Agahnim 2']],
        ])

    def testWestDarkWorld(self):
        self.run_location_tests([
            ["Brewery", False, []],
            ["Brewery", False, [], ['Moon Pearl']],
            ["Brewery", False, [], ['Pegasus Boots', 'Magic Mirror', 'Hookshot', 'Progressive Glove']],
            ["Brewery", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Brewery", True, ['Moon Pearl', 'Flute', 'Magic Mirror']],
            ["Brewery", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Brewery", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Brewery", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Brewery", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["C-Shaped House", False, []],
            ["C-Shaped House", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["C-Shaped House", True, ['Moon Pearl', 'Pegasus Boots']],
            ["C-Shaped House", True, ['Magic Mirror', 'Pegasus Boots']],
            ["C-Shaped House", True, ['Magic Mirror', 'Flute']],
            ["C-Shaped House", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["C-Shaped House", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["C-Shaped House", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["C-Shaped House", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Chest Game", False, []],
            ["Chest Game", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Chest Game", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Chest Game", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Chest Game", True, ['Magic Mirror', 'Flute']],
            ["Chest Game", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Chest Game", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Chest Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Chest Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Peg Cave", False, []],
            ["Peg Cave", False, [], ['Moon Pearl']],
            ["Peg Cave", False, [], ['Hammer']],
            ["Peg Cave", False, ['Progressive Glove'], ['Pegasus Boots', 'Progressive Glove']],
            ["Peg Cave", True, ['Moon Pearl', 'Hammer', 'Pegasus Boots']],
            ["Peg Cave", True, ['Moon Pearl', 'Hammer', 'Progressive Glove', 'Progressive Glove']],

            ["Bumper Cave Ledge", False, []],
            ["Bumper Cave Ledge", False, [], ['Moon Pearl']],
            ["Bumper Cave Ledge", False, [], ['Cape', 'Pegasus Boots']],
            ["Bumper Cave Ledge", False, [], ['Progressive Glove', 'Pegasus Boots']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Progressive Glove', 'Progressive Glove']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Progressive Glove', 'Hammer']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],

            ["Blacksmith", False, []],
            ["Blacksmith", False, ['Progressive Glove'], ['Progressive Glove']],
            ["Blacksmith", False, [], ['Moon Pearl']],
            ["Blacksmith", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Purple Chest", False, []],
            ["Purple Chest", False, ['Progressive Glove'], ['Progressive Glove']],
            ["Purple Chest", False, [], ['Moon Pearl']],
            ["Purple Chest", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']]


        ])

    def testMireArea(self):
        self.run_location_tests([
            ["Mire Shed - Left", False, []],
            ["Mire Shed - Left", False, ['Progressive Glove'], ['Progressive Glove', 'Pegasus Boots']],
            ["Mire Shed - Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Mire Shed - Left", False, [], ['Flute', 'Pegasus Boots']],
            ["Mire Shed - Left", True, ['Moon Pearl', 'Flute', 'Progressive Glove', 'Progressive Glove']],
            ["Mire Shed - Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Mire Shed - Left", True, ['Magic Mirror', 'Flute', 'Progressive Glove', 'Progressive Glove']],

            ["Mire Shed - Right", False, []],
            ["Mire Shed - Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Mire Shed - Right", False, ['Progressive Glove'], ['Progressive Glove', 'Pegasus Boots']],
            ["Mire Shed - Right", False, [], ['Flute', 'Pegasus Boots']],
            ["Mire Shed - Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Mire Shed - Right", True, ['Magic Mirror', 'Flute', 'Progressive Glove', 'Progressive Glove']],
            ["Mire Shed - Right", True, ['Moon Pearl', 'Flute', 'Progressive Glove', 'Progressive Glove']],
        ])