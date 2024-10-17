from .TestDungeon import TestDungeon


class TestSkullWoods(TestDungeon):

    def testSkullWoodsFrontAllEntrances(self):
        self.starting_regions = ['Skull Woods First Section', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)']
        self.run_tests([
            ["Skull Woods - Big Chest", False, []],
            ["Skull Woods - Big Chest", False, [], ['Big Key (Skull Woods)']],
            ["Skull Woods - Big Chest", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Skull Woods - Big Chest", True, ['Bomb Upgrade (+5)', 'Big Key (Skull Woods)']],

            ["Skull Woods - Compass Chest", True, []],

            ["Skull Woods - Map Chest", True, []],

            ["Skull Woods - Pot Prison", True, []],

            ["Skull Woods - Pinball Room", True, []]
        ])

    def testSkullWoodsFrontOnly(self):
        self.starting_regions = ['Skull Woods First Section']
        self.run_tests([
            ["Skull Woods - Big Chest", False, []],
            ["Skull Woods - Big Chest", False, [], ['Never in logic']],

            ["Skull Woods - Compass Chest", False, []],
            ["Skull Woods - Compass Chest", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Compass Chest", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']],

            ["Skull Woods - Map Chest", True, []],

            ["Skull Woods - Pot Prison", False, []],
            ["Skull Woods - Pot Prison", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Pot Prison", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']],

            ["Skull Woods - Pinball Room", False, []],
            ["Skull Woods - Pinball Room", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Pinball Room", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']],
        ])

    def testSkullWoodsLeftOnly(self):
        self.starting_regions = ['Skull Woods First Section (Left)']
        self.remove_exits = ['Skull Woods First Section Exit']
        self.run_tests([
            ["Skull Woods - Big Chest", False, []],
            ["Skull Woods - Big Chest", False, [], ['Never in logic']],

            ["Skull Woods - Compass Chest", True, []],

            ["Skull Woods - Map Chest", False, []],
            ["Skull Woods - Map Chest", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Map Chest", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']],

            ["Skull Woods - Pot Prison", True, []],

            ["Skull Woods - Pinball Room", True, []]
        ])

    def testSkullWoodsBackOnly(self):
        self.starting_regions = ['Skull Woods First Section (Top)']
        self.remove_exits = ['Skull Woods First Section Exit']
        self.run_tests([
            ["Skull Woods - Big Chest", False, []],
            ["Skull Woods - Big Chest", False, [], ['Big Key (Skull Woods)']],
            ["Skull Woods - Big Chest", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Skull Woods - Big Chest", True, ['Bomb Upgrade (+5)', 'Big Key (Skull Woods)']],

            ["Skull Woods - Compass Chest", False, []],
            ["Skull Woods - Compass Chest", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Compass Chest", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']],

            ["Skull Woods - Map Chest", True, []],

            ["Skull Woods - Pot Prison", False, []],
            ["Skull Woods - Pot Prison", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Pot Prison", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']],

            ["Skull Woods - Pinball Room", False, []],
            ["Skull Woods - Pinball Room", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Pinball Room", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)']]
        ])

    def testSkullWoodsMiddle(self):
        self.starting_regions = ['Skull Woods Second Section']
        self.remove_exits = ['Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)']
        self.run_tests([["Skull Woods - Big Key Chest", True, []]])

    def testSkullWoodsBack(self):
        self.starting_regions = ['Skull Woods Final Section (Entrance)']
        self.run_tests([
            ["Skull Woods - Bridge Room", True, []],

            ["Skull Woods - Boss", False, []],
            ["Skull Woods - Boss", False, [], ['Fire Rod']],
            ["Skull Woods - Boss", False, [], ['Progressive Sword']],
            ["Skull Woods - Boss", False, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)'], ['Small Key (Skull Woods)']],
            ["Skull Woods - Boss", True, ['Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Small Key (Skull Woods)', 'Fire Rod', 'Progressive Sword']],
        ])