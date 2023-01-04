from .TestDungeon import TestDungeon


class TestThievesTown(TestDungeon):
    
    def testThievesTown(self):
        self.starting_regions = ['Thieves Town (Entrance)']
        self.run_tests([
            ["Thieves' Town - Attic", False, []],
            ["Thieves' Town - Attic", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Attic", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Attic", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)']],

            ["Thieves' Town - Big Key Chest", True, []],

            ["Thieves' Town - Map Chest", True, []],

            ["Thieves' Town - Compass Chest", True, []],

            ["Thieves' Town - Ambush Chest", True, []],

            ["Thieves' Town - Big Chest", False, []],
            ["Thieves' Town - Big Chest", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Big Chest", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Big Chest", False, [], ['Hammer']],
            ["Thieves' Town - Big Chest", True, ['Hammer', 'Small Key (Thieves Town)', 'Big Key (Thieves Town)']],

            ["Thieves' Town - Blind's Cell", False, []],
            ["Thieves' Town - Blind's Cell", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Blind's Cell", True, ['Big Key (Thieves Town)']],

            ["Thieves' Town - Boss", False, []],
            ["Thieves' Town - Boss", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Boss", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Boss", False, [], ['Hammer', 'Progressive Sword', 'Cane of Somaria', 'Cane of Byrna']],
            ["Thieves' Town - Boss", True, ['Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Hammer']],
            ["Thieves' Town - Boss", True, ['Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Progressive Sword']],
            ["Thieves' Town - Boss", True, ['Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Cane of Somaria']],
            ["Thieves' Town - Boss", True, ['Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Cane of Byrna']],
        ])