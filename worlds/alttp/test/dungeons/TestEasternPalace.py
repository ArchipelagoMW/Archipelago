from .TestDungeon import TestDungeon


class TestEasternPalace(TestDungeon):

    def testEastern(self):
        self.starting_regions = ["Eastern Palace"]
        self.run_tests([
                ["Eastern Palace - Compass Chest", True, []],

                ["Eastern Palace - Cannonball Chest", True, []],

                ["Eastern Palace - Big Chest", False, []],
                ["Eastern Palace - Big Chest", False, [], ['Big Key (Eastern Palace)']],
                ["Eastern Palace - Big Chest", True, ['Big Key (Eastern Palace)']],

                ["Eastern Palace - Map Chest", True, []],

                ["Eastern Palace - Big Key Chest", False, []],
                ["Eastern Palace - Big Key Chest", False, [], ['Lamp']],
                ["Eastern Palace - Big Key Chest", True, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)', 'Progressive Sword']],

                #@todo: Advanced?
                ["Eastern Palace - Boss", False, []],
                ["Eastern Palace - Boss", False, [], ['Lamp']],
                ["Eastern Palace - Boss", False, [], ['Progressive Bow']],
                ["Eastern Palace - Boss", False, [], ['Big Key (Eastern Palace)']],
                ["Eastern Palace - Boss", False, ['Small Key (Eastern Palace)', 'Small Key (Eastern Palace)']],
                ["Eastern Palace - Boss", True, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)', 'Progressive Bow', 'Big Key (Eastern Palace)']]
            ])
