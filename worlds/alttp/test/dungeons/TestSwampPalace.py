from .TestDungeon import TestDungeon


class TestSwampPalace(TestDungeon):

    def testSwampPalace(self):
        self.starting_regions = ['Swamp Palace (Entrance)']
        self.run_tests([
            ["Swamp Palace - Entrance", False, []],
            ["Swamp Palace - Entrance", False, [], ['Flippers']],
            ["Swamp Palace - Entrance", False, [], ['Open Floodgate']],
            ["Swamp Palace - Entrance", True, ['Open Floodgate', 'Flippers']],

            ["Swamp Palace - Big Chest", False, []],
            ["Swamp Palace - Big Chest", False, [], ['Flippers']],
            ["Swamp Palace - Big Chest", False, [], ['Open Floodgate']],
            ["Swamp Palace - Big Chest", False, [], ['Hammer']],
            ["Swamp Palace - Big Chest", False, [], ['Big Key (Swamp Palace)']],
            ["Swamp Palace - Big Chest", False, [], ['Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)']],
            ["Swamp Palace - Big Chest", True, ['Open Floodgate', 'Big Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer']],

            ["Swamp Palace - West Side Switch Chest", False, []],
            ["Swamp Palace - West Side Switch Chest", False, [], ['Flippers']],
            ["Swamp Palace - West Side Switch Chest", False, [], ['Open Floodgate']],
            ["Swamp Palace - West Side Switch Chest", False, [], ['Hammer']],
            ["Swamp Palace - West Side Switch Chest", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - West Side Switch Chest", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer']],

            ["Swamp Palace - Bomb Wall", False, []],
            ["Swamp Palace - Bomb Wall", False, [], ['Flippers']],
            ["Swamp Palace - Bomb Wall", False, [], ['Open Floodgate']],
            ["Swamp Palace - Bomb Wall", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - Bomb Wall", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Swamp Palace - Bomb Wall", True, ['Bomb Upgrade (+5)', 'Open Floodgate', 'Small Key (Swamp Palace)', 'Flippers']],

            ["Swamp Palace - West Side Free Chest", False, []],
            ["Swamp Palace - West Side Free Chest", False, [], ['Flippers']],
            ["Swamp Palace - West Side Free Chest", False, [], ['Open Floodgate']],
            ["Swamp Palace - West Side Free Chest", False, [], ['Hammer']],
            ["Swamp Palace - West Side Free Chest", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - West Side Free Chest", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer']],

            ["Swamp Palace - South Loop", False, []],
            ["Swamp Palace - South Loop", False, [], ['Flippers']],
            ["Swamp Palace - South Loop", False, [], ['Open Floodgate']],
            ["Swamp Palace - South Loop", False, [], ['Hammer']],
            ["Swamp Palace - South Loop", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - South Loop", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer']],

            ["Swamp Palace - Flooded Room - Left", False, []],
            ["Swamp Palace - Flooded Room - Left", False, [], ['Flippers']],
            ["Swamp Palace - Flooded Room - Left", False, [], ['Open Floodgate']],
            ["Swamp Palace - Flooded Room - Left", False, [], ['Hammer']],
            ["Swamp Palace - Flooded Room - Left", False, [], ['Hookshot']],
            ["Swamp Palace - Flooded Room - Left", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - Flooded Room - Left", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)',  'Small Key (Swamp Palace)', 'Flippers', 'Hammer', 'Hookshot']],

            ["Swamp Palace - Flooded Room - Right", False, []],
            ["Swamp Palace - Flooded Room - Right", False, [], ['Flippers']],
            ["Swamp Palace - Flooded Room - Right", False, [], ['Open Floodgate']],
            ["Swamp Palace - Flooded Room - Right", False, [], ['Hammer']],
            ["Swamp Palace - Flooded Room - Right", False, [], ['Hookshot']],
            ["Swamp Palace - Flooded Room - Right", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - Flooded Room - Right", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer', 'Hookshot']],

            ["Swamp Palace - Waterfall Room", False, []],
            ["Swamp Palace - Waterfall Room", False, [], ['Flippers']],
            ["Swamp Palace - Waterfall Room", False, [], ['Open Floodgate']],
            ["Swamp Palace - Waterfall Room", False, [], ['Hammer']],
            ["Swamp Palace - Waterfall Room", False, [], ['Hookshot']],
            ["Swamp Palace - Waterfall Room", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - Waterfall Room", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer', 'Hookshot']],

            ["Swamp Palace - Boss", False, []],
            ["Swamp Palace - Boss", False, [], ['Flippers']],
            ["Swamp Palace - Boss", False, [], ['Open Floodgate']],
            ["Swamp Palace - Boss", False, [], ['Hammer']],
            ["Swamp Palace - Boss", False, [], ['Hookshot']],
            ["Swamp Palace - Boss", False, [], ['Small Key (Swamp Palace)']],
            ["Swamp Palace - Boss", True, ['Open Floodgate', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Small Key (Swamp Palace)', 'Flippers', 'Hammer', 'Hookshot']],
        ])