from test.dungeons.TestDungeon import TestDungeon


class TestDesertPalace(TestDungeon):

    def testDesertPalace(self):
        self.starting_regions = ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)']
        self.run_tests([
            ["Desert Palace - Map Chest", True, []],

            ["Desert Palace - Big Chest", False, []],
            ["Desert Palace - Big Chest", False, [], ['Big Key (Desert Palace)']],
            ["Desert Palace - Big Chest", True, ['Big Key (Desert Palace)']],

            ["Desert Palace - Torch", False, []],
            ["Desert Palace - Torch", False, [], ['Pegasus Boots']],
            ["Desert Palace - Torch", True, ['Pegasus Boots']],

            ["Desert Palace - Compass Chest", False, []],
            ["Desert Palace - Compass Chest", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Compass Chest", True, ['Small Key (Desert Palace)']],

            #@todo: Require a real weapon for enemizer?
            ["Desert Palace - Big Key Chest", False, []],
            ["Desert Palace - Big Key Chest", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Big Key Chest", True, ['Small Key (Desert Palace)']],

            ["Desert Palace - Boss", False, []],
            ["Desert Palace - Boss", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Big Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Lamp', 'Fire Rod']],
            ["Desert Palace - Boss", False, [], ['Progressive Sword', 'Hammer', 'Fire Rod', 'Ice Rod', 'Progressive Bow', 'Cane of Somaria', 'Cane of Byrna']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Fire Rod']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Progressive Sword']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Hammer']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Ice Rod']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Cane of Somaria']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Cane of Byrna']],
        ])