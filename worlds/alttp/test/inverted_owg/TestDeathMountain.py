from .TestInvertedOWG import TestInvertedOWG


class TestDeathMountain(TestInvertedOWG):

    def testWestDeathMountain(self):
        self.run_location_tests([
            ["Old Man", False, []],
            ["Old Man", False, [], ['Lamp']],
            ["Old Man", True, ['Pegasus Boots', 'Lamp']],

            ["Spectacle Rock Cave", False, []],
            ["Spectacle Rock Cave", True, ['Pegasus Boots']],
        ])

    def testEastDeathMountain(self):
        self.run_location_tests([
            ["Spiral Cave", False, []],
            ["Spiral Cave", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Spiral Cave", False, [], ['Moon Pearl', 'Progressive Sword']],
            ["Spiral Cave", True, ['Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Lamp', 'Progressive Sword']],
            ["Spiral Cave", True, ['Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Pegasus Boots', 'Progressive Sword']],
            ["Spiral Cave", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Far Left", False, []],
            ["Paradox Cave Lower - Far Left", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Far Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Left", False, []],
            ["Paradox Cave Lower - Left", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Middle", False, []],
            ["Paradox Cave Lower - Middle", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Middle", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Right", False, []],
            ["Paradox Cave Lower - Right", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Far Right", False, []],
            ["Paradox Cave Lower - Far Right", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Far Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Upper - Left", False, []],
            ["Paradox Cave Upper - Left", False, [], ['Moon Pearl']],
            ["Paradox Cave Upper - Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Paradox Cave Upper - Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Upper - Right", False, []],
            ["Paradox Cave Upper - Right", False, [], ['Moon Pearl']],
            ["Paradox Cave Upper - Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Paradox Cave Upper - Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Pegasus Boots']],

            ["Mimic Cave", False, []],
            ["Mimic Cave", False, [], ['Moon Pearl']],
            ["Mimic Cave", False, [], ['Hammer']],
            ["Mimic Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Hammer', 'Pegasus Boots']],

            ["Ether Tablet", False, []],
            ["Ether Tablet", False, ['Progressive Sword'], ['Progressive Sword']],
            ["Ether Tablet", False, [], ['Book of Mudora']],
            ["Ether Tablet", False, [], ['Moon Pearl']],
            ["Ether Tablet", True, ['Pegasus Boots', 'Moon Pearl', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword']],

            ["Spectacle Rock", False, []],
            ["Spectacle Rock", False, [], ['Moon Pearl']],
            ["Spectacle Rock", True, ['Moon Pearl', 'Pegasus Boots']],
        ])


    def testWestDarkWorldDeathMountain(self):
        self.run_location_tests([
            ["Spike Cave", False, []],
            ["Spike Cave", False, [], ['Progressive Glove']],
            ["Spike Cave", False, [], ['Hammer']],
            ["Spike Cave", False, [], ['Cape', 'Cane of Byrna']],
            ["Spike Cave", False, [], ['Cane of Byrna', 'AnyBottle', 'Magic Upgrade (1/2)']],
            ["Spike Cave", False, [], ['AnyBottle', 'Magic Upgrade (1/2)', 'Pegasus Boots', 'Boss Heart Container', 'Piece of Heart', 'Sanctuary Heart Container']],
            ["Spike Cave", True, ['Bottle', 'Hammer', 'Progressive Glove', 'Lamp', 'Cape']],
            # Change from base ER - this fork places a blue potion in dark world
            ["Spike Cave", True, ['Bottle', 'Hammer', 'Progressive Glove', 'Lamp', 'Cane of Byrna']],
            ["Spike Cave", True, ['Bottle', 'Hammer', 'Progressive Glove', 'Flute', 'Cane of Byrna']],
            ["Spike Cave", True, ['Magic Upgrade (1/2)', 'Hammer', 'Progressive Glove', 'Lamp', 'Cape']],
            ["Spike Cave", True, ['Magic Upgrade (1/2)', 'Hammer', 'Progressive Glove', 'Flute', 'Cape']],
            ["Spike Cave", True, ['Magic Upgrade (1/2)', 'Hammer', 'Progressive Glove', 'Lamp', 'Cane of Byrna']],
            ["Spike Cave", True, ['Magic Upgrade (1/2)', 'Hammer', 'Progressive Glove', 'Flute', 'Cane of Byrna']],
            ["Spike Cave", True, ['Pegasus Boots', 'Hammer', 'Progressive Glove', 'Cane of Byrna']],
            ["Spike Cave", True, ['Boss Heart Container', 'Hammer', 'Progressive Glove', 'Lamp', 'Cane of Byrna']],
            ["Spike Cave", True, ['Boss Heart Container', 'Hammer', 'Progressive Glove', 'Flute', 'Cane of Byrna']],
        ])

    def testEastDarkWorldDeathMountain(self):
        self.run_location_tests([
            ["Superbunny Cave - Top", False, []],
            ["Superbunny Cave - Top", True, ['Pegasus Boots']],

            ["Superbunny Cave - Bottom", False, []],
            ["Superbunny Cave - Bottom", True, ['Pegasus Boots']],

            ["Hookshot Cave - Bottom Right", False, []],
            ["Hookshot Cave - Bottom Right", False, [], ['Hookshot', 'Pegasus Boots']],
            ["Hookshot Cave - Bottom Right", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Bottom Right", True, ['Pegasus Boots', 'Bomb Upgrade (50)']],

            ["Hookshot Cave - Bottom Left", False, []],
            ["Hookshot Cave - Bottom Left", False, [], ['Hookshot']],
            ["Hookshot Cave - Bottom Left", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Bottom Left", True, ['Pegasus Boots', 'Hookshot', 'Bomb Upgrade (50)']],

            ["Hookshot Cave - Top Left", False, []],
            ["Hookshot Cave - Top Left", False, [], ['Hookshot']],
            ["Hookshot Cave - Top Left", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Top Left", True, ['Pegasus Boots', 'Hookshot', 'Bomb Upgrade (50)']],

            ["Hookshot Cave - Top Right", False, []],
            ["Hookshot Cave - Top Right", False, [], ['Hookshot']],
            ["Hookshot Cave - Top Right", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Top Right", True, ['Pegasus Boots', 'Hookshot', 'Bomb Upgrade (50)']],
        ])