from .TestDungeon import TestDungeon


class TestTowerOfHera(TestDungeon):

    def testTowerOfHera(self):
        self.starting_regions = ['Tower of Hera (Bottom)']
        self.run_tests([
            ["Tower of Hera - Basement Chest", False, []],
            ["Tower of Hera - Basement Chest", False, [], ['Small Key (Tower of Hera)']],
            ["Tower of Hera - Basement Chest", False, [], ['Lamp', 'Fire Rod']],
            ["Tower of Hera - Basement Chest", True, ['Small Key (Tower of Hera)', 'Lamp', 'Bomb Upgrade (50)']],
            ["Tower of Hera - Basement Chest", True, ['Small Key (Tower of Hera)', 'Fire Rod']],

            ["Tower of Hera - Basement Cage", False, []],
            ["Tower of Hera - Basement Cage", True, ['Bomb Upgrade (50)']],
            ["Tower of Hera - Basement Cage", True, ['Progressive Sword']],

            ["Tower of Hera - Entryway Chest", False, []],
            ["Tower of Hera - Entryway Chest", True, ['Bomb Upgrade (50)']],
            ["Tower of Hera - Entryway Chest", True, ['Progressive Sword']],

            ["Tower of Hera - South of Big Chest", False, []],
            ["Tower of Hera - South of Big Chest", False, [], ['Big Key (Tower of Hera)']],
            ["Tower of Hera - South of Big Chest", True, ['Big Key (Tower of Hera)', 'Progressive Sword']],

            ["Tower of Hera - Big Chest", False, []],
            ["Tower of Hera - Big Chest", False, [], ['Big Key (Tower of Hera)']],
            ["Tower of Hera - Big Chest", True, ['Big Key (Tower of Hera)', 'Progressive Sword']],

            ["Tower of Hera - Boss", False, []],
            ["Tower of Hera - Boss", False, [], ['Big Key (Tower of Hera)']],
            ["Tower of Hera - Boss", False, [], ['Progressive Sword', 'Hammer']],
            ["Tower of Hera - Boss", True, ['Progressive Sword', 'Big Key (Tower of Hera)']],
            ["Tower of Hera - Boss", True, ['Hammer', 'Big Key (Tower of Hera)']],
        ])