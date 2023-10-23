from .TestDungeon import TestDungeon


class TestGanonsTower(TestDungeon):

    def testGanonsTower(self):
        self.starting_regions = ['Ganons Tower (Entrance)']
        self.run_tests([
            ["Ganons Tower - Bob's Torch", False, []],
            ["Ganons Tower - Bob's Torch", False, [], ['Pegasus Boots']],
            ["Ganons Tower - Bob's Torch", True, ['Pegasus Boots']],

            ["Ganons Tower - DMs Room - Top Left", False, []],
            ["Ganons Tower - DMs Room - Top Left", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Top Left", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Top Left", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - DMs Room - Top Right", False, []],
            ["Ganons Tower - DMs Room - Top Right", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Top Right", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Top Right", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - DMs Room - Bottom Left", False, []],
            ["Ganons Tower - DMs Room - Bottom Left", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Bottom Left", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Bottom Left", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - DMs Room - Bottom Right", False, []],
            ["Ganons Tower - DMs Room - Bottom Right", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Bottom Right", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Bottom Right", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - Randomizer Room - Top Left", False, []],
            ["Ganons Tower - Randomizer Room - Top Left", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Top Left", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Top Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Fire Rod', 'Cane of Somaria']],
            ["Ganons Tower - Randomizer Room - Top Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Randomizer Room - Top Right", False, []],
            ["Ganons Tower - Randomizer Room - Top Right", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Top Right", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Top Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Fire Rod', 'Cane of Somaria']],
            ["Ganons Tower - Randomizer Room - Top Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Randomizer Room - Bottom Left", False, []],
            ["Ganons Tower - Randomizer Room - Bottom Left", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Bottom Left", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Bottom Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Fire Rod', 'Cane of Somaria']],
            ["Ganons Tower - Randomizer Room - Bottom Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Randomizer Room - Bottom Right", False, []],
            ["Ganons Tower - Randomizer Room - Bottom Right", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Bottom Right", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Bottom Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Fire Rod', 'Cane of Somaria']],
            ["Ganons Tower - Randomizer Room - Bottom Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Firesnake Room", False, []],
            ["Ganons Tower - Firesnake Room", False, [], ['Hammer']],
            ["Ganons Tower - Firesnake Room", False, [], ['Hookshot']],
            ["Ganons Tower - Firesnake Room", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Map Chest", False, []],
            ["Ganons Tower - Map Chest", False, [], ['Hammer']],
            ["Ganons Tower - Map Chest", False, [], ['Hookshot', 'Pegasus Boots']],
            ["Ganons Tower - Map Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],
            ["Ganons Tower - Map Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)',  'Hammer', 'Pegasus Boots']],

            ["Ganons Tower - Big Chest", False, []],
            ["Ganons Tower - Big Chest", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Big Chest", True, ['Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Chest", True, ['Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Hope Room - Left", True, []],

            ["Ganons Tower - Hope Room - Right", True, []],

            ["Ganons Tower - Bob's Chest", False, []],
            ["Ganons Tower - Bob's Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Bob's Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Tile Room", False, []],
            ["Ganons Tower - Tile Room", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Tile Room", True, ['Cane of Somaria']],

            ["Ganons Tower - Compass Room - Top Left", False, []],
            ["Ganons Tower - Compass Room - Top Left", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Top Left", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Top Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Compass Room - Top Right", False, []],
            ["Ganons Tower - Compass Room - Top Right", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Top Right", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Top Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Compass Room - Bottom Left", False, []],
            ["Ganons Tower - Compass Room - Bottom Left", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Bottom Left", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Bottom Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Compass Room - Bottom Right", False, []],
            ["Ganons Tower - Compass Room - Bottom Right", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Bottom Right", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Bottom Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Big Key Chest", False, []],
            ["Ganons Tower - Big Key Chest", True, ['Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Key Chest", True, ['Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Big Key Room - Left", False, []],
            ["Ganons Tower - Big Key Room - Left", True, ['Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Key Room - Left", True, ['Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Big Key Room - Right", False, []],
            ["Ganons Tower - Big Key Room - Right", True, ['Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Key Room - Right", True, ['Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Mini Helmasaur Room - Left", False, []],
            ["Ganons Tower - Mini Helmasaur Room - Left", False, [], ['Progressive Bow']],
            ["Ganons Tower - Mini Helmasaur Room - Left", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Mini Helmasaur Room - Left", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Mini Helmasaur Room - Left", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp']],
            ["Ganons Tower - Mini Helmasaur Room - Left", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod']],

            ["Ganons Tower - Mini Helmasaur Room - Right", False, []],
            ["Ganons Tower - Mini Helmasaur Room - Right", False, [], ['Progressive Bow']],
            ["Ganons Tower - Mini Helmasaur Room - Right", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Mini Helmasaur Room - Right", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Mini Helmasaur Room - Right", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp']],
            ["Ganons Tower - Mini Helmasaur Room - Right", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod']],

            ["Ganons Tower - Pre-Moldorm Chest", False, []],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Progressive Bow']],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Pre-Moldorm Chest", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp']],
            ["Ganons Tower - Pre-Moldorm Chest", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod']],

            ["Ganons Tower - Validation Chest", False, []],
            ["Ganons Tower - Validation Chest", False, [], ['Hookshot']],
            ["Ganons Tower - Validation Chest", False, [], ['Progressive Bow']],
            ["Ganons Tower - Validation Chest", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Validation Chest", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Validation Chest", False, [], ['Progressive Sword', 'Hammer']],
            ["Ganons Tower - Validation Chest", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp', 'Hookshot', 'Progressive Sword']],
            ["Ganons Tower - Validation Chest", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Hookshot', 'Progressive Sword']],
            ["Ganons Tower - Validation Chest", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp', 'Hookshot', 'Hammer']],
            ["Ganons Tower - Validation Chest", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Hookshot', 'Hammer']],
        ])