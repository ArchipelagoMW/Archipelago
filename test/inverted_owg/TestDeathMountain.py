from test.inverted_owg.TestInvertedOWG import TestInvertedOWG


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
            ["Paradox Cave Lower - Far Left", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Left", False, []],
            ["Paradox Cave Lower - Left", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Left", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Middle", False, []],
            ["Paradox Cave Lower - Middle", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Middle", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Right", False, []],
            ["Paradox Cave Lower - Right", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Right", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Lower - Far Right", False, []],
            ["Paradox Cave Lower - Far Right", False, [], ['Moon Pearl']],
            ["Paradox Cave Lower - Far Right", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Upper - Left", False, []],
            ["Paradox Cave Upper - Left", False, [], ['Moon Pearl']],
            ["Paradox Cave Upper - Left", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Paradox Cave Upper - Right", False, []],
            ["Paradox Cave Upper - Right", False, [], ['Moon Pearl']],
            ["Paradox Cave Upper - Right", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Mimic Cave", False, []],
            ["Mimic Cave", False, [], ['Moon Pearl']],
            ["Mimic Cave", False, [], ['Hammer']],
            ["Mimic Cave", True, ['Moon Pearl', 'Hammer', 'Pegasus Boots']],

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
            # ER doesn't put in an extra potion
            #["Spike Cave", True, ['Bottle', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cape']],
            ["Spike Cave", True, ['Bottle', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cape', 'Moon Pearl']],
            ["Spike Cave", True, ['Bottle', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cane of Byrna']],
            ["Spike Cave", True, ['Magic Upgrade (1/2)', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cape']],
            ["Spike Cave", True, ['Magic Upgrade (1/2)', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cane of Byrna']],
            ["Spike Cave", True, ['Magic Upgrade (1/4)', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cape']],
            ["Spike Cave", True, ['Magic Upgrade (1/4)', 'Hammer', 'Progressive Glove', 'Pegasus Boots', 'Cane of Byrna']],
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
            ["Hookshot Cave - Bottom Right", True, ['Pegasus Boots']],

            ["Hookshot Cave - Bottom Left", False, []],
            ["Hookshot Cave - Bottom Left", False, [], ['Hookshot']],
            ["Hookshot Cave - Bottom Left", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Bottom Left", True, ['Pegasus Boots', 'Hookshot']],

            ["Hookshot Cave - Top Left", False, []],
            ["Hookshot Cave - Top Left", False, [], ['Hookshot']],
            ["Hookshot Cave - Top Left", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Top Left", True, ['Pegasus Boots', 'Hookshot']],

            ["Hookshot Cave - Top Right", False, []],
            ["Hookshot Cave - Top Right", False, [], ['Hookshot']],
            ["Hookshot Cave - Top Right", False, [], ['Progressive Glove', 'Pegasus Boots', 'Magic Mirror']],
            ["Hookshot Cave - Top Right", True, ['Pegasus Boots', 'Hookshot']],
        ])