from worlds.alttp.PotShuffle import FilledPot, POT_SWITCH

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
                ["Eastern Palace - Big Key Chest", True, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)', 'Progressive Bow']],

                #@todo: Advanced?
                ["Eastern Palace - Boss", False, []],
                ["Eastern Palace - Boss", False, [], ['Lamp']],
                ["Eastern Palace - Boss", False, [], ['Progressive Bow']],
                ["Eastern Palace - Boss", False, [], ['Big Key (Eastern Palace)']],
                ["Eastern Palace - Boss", False, ['Small Key (Eastern Palace)', 'Small Key (Eastern Palace)']],
                ["Eastern Palace - Boss", True, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)', 'Progressive Bow', 'Big Key (Eastern Palace)']]
            ])

    def testEasternPalacePotShuffleBigKeyChestLogic(self):
        self.starting_regions = ["Eastern Palace"]

        vanilla_switch_state = self.get_test_pot_shuffle_state({
            0xB8: (
                FilledPot(96, 13, 11),
                FilledPot(88, 16, 11),
                FilledPot(104, 16, POT_SWITCH),
            ),
        })
        self.rebuild_with_pot_shuffle(vanilla_switch_state)
        self.run_tests([
            ["Eastern Palace - Big Key Chest", False, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)']],
            ["Eastern Palace - Big Key Chest", True, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)', 'Progressive Bow']],
        ])

        moved_switch_state = self.get_test_pot_shuffle_state({
            0xB8: (
                FilledPot(96, 13, POT_SWITCH),
                FilledPot(88, 16, 11),
                FilledPot(104, 16, 11),
            ),
        })
        self.rebuild_with_pot_shuffle(moved_switch_state)
        self.run_tests([
            ["Eastern Palace - Big Key Chest", True, ['Lamp', 'Small Key (Eastern Palace)', 'Small Key (Eastern Palace)']],
        ])
