from .TestVanilla import TestVanilla


class TestDarkWorld(TestVanilla):

    def testSouthDarkWorld(self):
        self.run_location_tests([
            ["Hype Cave - Top", False, []],
            ["Hype Cave - Top", False, [], ['Moon Pearl']],
            ["Hype Cave - Top", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Middle Right", False, []],
            ["Hype Cave - Middle Right", False, [], ['Moon Pearl']],
            ["Hype Cave - Middle Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Middle Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Middle Left", False, []],
            ["Hype Cave - Middle Left", False, [], ['Moon Pearl']],
            ["Hype Cave - Middle Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Middle Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Bottom", False, []],
            ["Hype Cave - Bottom", False, [], ['Moon Pearl']],
            ["Hype Cave - Bottom", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Bottom", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Hype Cave - Generous Guy", False, []],
            ["Hype Cave - Generous Guy", False, [], ['Moon Pearl']],
            ["Hype Cave - Generous Guy", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Hype Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Stumpy", False, []],
            ["Stumpy", False, [], ['Moon Pearl']],
            ["Stumpy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Stumpy", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Stumpy", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Stumpy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Stumpy", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Digging Game", False, []],
            ["Digging Game", False, [], ['Moon Pearl']],
            ["Digging Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Hammer']],
            ["Digging Game", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Digging Game", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Digging Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Digging Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']]
        ])

    def testWestDarkWorld(self):
        self.run_location_tests([
            ["Brewery", False, []],
            ["Brewery", False, [], ['Moon Pearl']],
            ["Brewery", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Brewery", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Brewery", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Brewery", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Brewery", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["C-Shaped House", False, []],
            ["C-Shaped House", False, [], ['Moon Pearl']],
            ["C-Shaped House", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["C-Shaped House", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["C-Shaped House", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["C-Shaped House", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Chest Game", False, []],
            ["Chest Game", False, [], ['Moon Pearl']],
            ["Chest Game", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Chest Game", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Chest Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Chest Game", True, ['Moon Pearl', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Peg Cave", False, []],
            ["Peg Cave", False, [], ['Moon Pearl']],
            ["Peg Cave", False, [], ['Hammer']],
            ["Peg Cave", False, [], ['Progressive Glove']],
            ["Peg Cave", True, ['Moon Pearl', 'Hammer', 'Progressive Glove', 'Progressive Glove']],

            ["Bumper Cave Ledge", False, []],
            ["Bumper Cave Ledge", False, [], ['Moon Pearl']],
            ["Bumper Cave Ledge", False, [], ['Cape']],
            ["Bumper Cave Ledge", False, [], ['Progressive Glove']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Progressive Glove', 'Progressive Glove']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Progressive Glove', 'Hammer']],
            ["Bumper Cave Ledge", True, ['Moon Pearl', 'Cape', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],

            ["Blacksmith", False, []],
            ["Blacksmith", False, [], ['Progressive Glove']],
            ["Blacksmith", False, [], ['Moon Pearl']],
            ["Blacksmith", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Purple Chest", False, []],
            ["Purple Chest", False, [], ['Progressive Glove']],
            ["Purple Chest", False, [], ['Moon Pearl']],
            ["Purple Chest", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']]
        ])

    def testEastDarkWorld(self):
        self.run_location_tests([
            ["Catfish", False, []],
            ["Catfish", False, [], ['Progressive Glove']],
            ["Catfish", False, [], ['Moon Pearl']],
            ["Catfish", True, ['Moon Pearl', 'Beat Agahnim 1', 'Progressive Glove']],
            ["Catfish", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Catfish", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove', 'Flippers']],

            ["Pyramid", False, []],
            ["Pyramid", False, [], ['Beat Agahnim 1', 'Moon Pearl']],
            ["Pyramid", True, ['Beat Agahnim 1']],
            ["Pyramid", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Pyramid", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove', 'Flippers']],

            ["Pyramid Fairy - Left", False, []],
            ["Pyramid Fairy - Left", False, [], ['Moon Pearl']],
            ["Pyramid Fairy - Left", False, [], ['Crystal 5']],
            ["Pyramid Fairy - Left", False, [], ['Crystal 6']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Hammer']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Progressive Glove', 'Hammer']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot', 'Magic Mirror']],
            ["Pyramid Fairy - Left", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Flippers', 'Hookshot', 'Magic Mirror']],

            ["Pyramid Fairy - Right", False, []],
            ["Pyramid Fairy - Right", False, [], ['Moon Pearl']],
            ["Pyramid Fairy - Right", False, [], ['Crystal 5']],
            ["Pyramid Fairy - Right", False, [], ['Crystal 6']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Hammer']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Progressive Glove', 'Hammer']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot', 'Magic Mirror']],
            ["Pyramid Fairy - Right", True, ['Moon Pearl', 'Crystal 5', 'Crystal 6', 'Beat Agahnim 1', 'Flippers', 'Hookshot', 'Magic Mirror']],

            ["Ganon", False, []],
            ["Ganon", False, [], ['Moon Pearl']],
            ["Ganon", False, [], ['Beat Agahnim 2']],
        ])

    def testMireArea(self):
        self.run_location_tests([
            ["Mire Shed - Left", False, []],
            ["Mire Shed - Left", False, [], ['Progressive Glove']],
            ["Mire Shed - Left", False, [], ['Moon Pearl']],
            ["Mire Shed - Left", False, [], ['Flute']],
            ["Mire Shed - Left", True, ['Moon Pearl', 'Flute', 'Progressive Glove', 'Progressive Glove']],

            ["Mire Shed - Right", False, []],
            ["Mire Shed - Right", False, [], ['Progressive Glove']],
            ["Mire Shed - Right", False, [], ['Moon Pearl']],
            ["Mire Shed - Right", False, [], ['Flute']],
            ["Mire Shed - Right", True, ['Moon Pearl', 'Flute', 'Progressive Glove', 'Progressive Glove']],
        ])
