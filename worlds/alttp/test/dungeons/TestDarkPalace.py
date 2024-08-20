from .TestDungeon import TestDungeon


class TestDarkPalace(TestDungeon):

    def testDarkPalace(self):
        self.starting_regions = ['Palace of Darkness (Entrance)']
        key = 'Small Key (Palace of Darkness)'
        self.run_tests([
            ["Palace of Darkness - Shooter Room", True, []],

            ["Palace of Darkness - The Arena - Ledge", False, []],
            ["Palace of Darkness - The Arena - Ledge", False, [], ['Progressive Bow']],
            ["Palace of Darkness - The Arena - Ledge", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Palace of Darkness - The Arena - Ledge", True, ['Progressive Bow', 'Bomb Upgrade (+5)']],

            ["Palace of Darkness - Map Chest", False, []],
            ["Palace of Darkness - Map Chest", False, [], ['Progressive Bow']],
            ["Palace of Darkness - Map Chest", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Palace of Darkness - Map Chest", True, ['Progressive Bow', 'Bomb Upgrade (+5)']],
            ["Palace of Darkness - Map Chest", True, ['Progressive Bow', 'Pegasus Boots']],

            #Lower requirement for self-locking key
            #No lower requirement when bow/hammer is out of logic
            ["Palace of Darkness - Big Key Chest", False, []],
            ["Palace of Darkness - Big Key Chest", False, [key]*5, [key]],
            ["Palace of Darkness - Big Key Chest", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Palace of Darkness - Big Key Chest", True, [key]*6 + ['Bomb Upgrade (+5)']],

            ["Palace of Darkness - The Arena - Bridge", False, []],
            ["Palace of Darkness - The Arena - Bridge", False, [], [key, 'Progressive Bow']],
            ["Palace of Darkness - The Arena - Bridge", False, [], [key, 'Hammer']],
            ["Palace of Darkness - The Arena - Bridge", False, [], [key, 'Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Palace of Darkness - The Arena - Bridge", True, [key]],
            ["Palace of Darkness - The Arena - Bridge", True, ['Progressive Bow', 'Hammer', 'Bomb Upgrade (+5)']],
            ["Palace of Darkness - The Arena - Bridge", True, ['Progressive Bow', 'Hammer', 'Pegasus Boots']],

            ["Palace of Darkness - Stalfos Basement", False, []],
            ["Palace of Darkness - Stalfos Basement", False, [], [key, 'Progressive Bow']],
            ["Palace of Darkness - Stalfos Basement", False, [], [key, 'Hammer']],
            ["Palace of Darkness - Stalfos Basement", False, [], [key, 'Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Palace of Darkness - Stalfos Basement", True, [key]],
            ["Palace of Darkness - Stalfos Basement", True, ['Progressive Bow', 'Hammer', 'Bomb Upgrade (+5)']],
            ["Palace of Darkness - Stalfos Basement", True, ['Progressive Bow', 'Hammer', 'Pegasus Boots']],

            ["Palace of Darkness - Compass Chest", False, []],
            ["Palace of Darkness - Compass Chest", False, [key]*3, [key]],
            ["Palace of Darkness - Compass Chest", True, [key]*4],

            #@todo: Advanced?
            ["Palace of Darkness - Dark Basement - Left", False, []],
            ["Palace of Darkness - Dark Basement - Left", False, [], ['Lamp']],
            ["Palace of Darkness - Dark Basement - Left", False, [key]*3, [key]],
            ["Palace of Darkness - Dark Basement - Left", True, ['Lamp'] + [key]*4],

            ["Palace of Darkness - Dark Basement - Right", False, []],
            ["Palace of Darkness - Dark Basement - Right", False, [], ['Lamp']],
            ["Palace of Darkness - Dark Basement - Right", False, [key] * 3, [key]],
            ["Palace of Darkness - Dark Basement - Right", True, ['Lamp'] + [key] * 4],

            ["Palace of Darkness - Harmless Hellway", False, []],
            ["Palace of Darkness - Harmless Hellway", False, [key]*5, [key]],
            ["Palace of Darkness - Harmless Hellway", True, [key]*6],

            ["Palace of Darkness - Dark Maze - Top", False, []],
            ["Palace of Darkness - Dark Maze - Top", False, [], ['Lamp']],
            ["Palace of Darkness - Dark Maze - Top", False, [key]*5, [key]],
            ["Palace of Darkness - Dark Maze - Top", True, ['Lamp'] + [key]*6],

            ["Palace of Darkness - Dark Maze - Bottom", False, []],
            ["Palace of Darkness - Dark Maze - Bottom", False, [], ['Lamp']],
            ["Palace of Darkness - Dark Maze - Bottom", False, [key]*5, [key]],
            ["Palace of Darkness - Dark Maze - Bottom", True, ['Lamp'] + [key]*6],

            ["Palace of Darkness - Big Chest", False, []],
            ["Palace of Darkness - Big Chest", False, [], ['Lamp']],
            ["Palace of Darkness - Big Chest", False, [], ['Big Key (Palace of Darkness)']],
            ["Palace of Darkness - Big Chest", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Palace of Darkness - Big Chest", False, [key]*5, [key]],
            ["Palace of Darkness - Big Chest", True, ['Bomb Upgrade (+5)', 'Lamp', 'Big Key (Palace of Darkness)'] + [key]*6],

            ["Palace of Darkness - Boss", False, []],
            ["Palace of Darkness - Boss", False, [], ['Lamp']],
            ["Palace of Darkness - Boss", False, [], ['Hammer']],
            ["Palace of Darkness - Boss", False, [], ['Progressive Bow']],
            ["Palace of Darkness - Boss", False, [], ['Big Key (Palace of Darkness)']],
            ["Palace of Darkness - Boss", False, [key]*5, [key]],
            ["Palace of Darkness - Boss", True, ['Lamp', 'Hammer', 'Progressive Bow', 'Big Key (Palace of Darkness)'] + [key]*6],
        ])