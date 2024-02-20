from .TestInverted import TestInverted


class TestInvertedTurtleRock(TestInverted):

    def testTurtleRock(self):
        self.run_location_tests([
            ["Turtle Rock - Compass Chest", False, []],
            ["Turtle Rock - Compass Chest", False, [], ['Cane of Somaria']],
            ["Turtle Rock - Compass Chest", False, [], ['Quake', 'Magic Mirror']],
            ["Turtle Rock - Compass Chest", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Quake', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Compass Chest", True, ['Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria']],
            ["Turtle Rock - Compass Chest", True, ['Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria']],
            ["Turtle Rock - Compass Chest", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Compass Chest", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Compass Chest", True, ['Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Compass Chest", True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],

            ["Turtle Rock - Chain Chomps", False, []],
            ["Turtle Rock - Chain Chomps", False, [], ['Magic Mirror', 'Cane of Somaria']],
            ["Turtle Rock - Chain Chomps", False, ['Small Key (Turtle Rock)'], ['Magic Mirror', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Chain Chomps", True, ['Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Chain Chomps", True, ['Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Chain Chomps", True, ['Bomb Upgrade (+5)', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],
            ["Turtle Rock - Chain Chomps", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot']],
            ["Turtle Rock - Chain Chomps", True, ['Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot']],
            ["Turtle Rock - Chain Chomps", True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Fire Rod']],

            ["Turtle Rock - Roller Room - Left", False, []],
            ["Turtle Rock - Roller Room - Left", False, [], ['Cane of Somaria']],
            ["Turtle Rock - Roller Room - Left", False, [], ['Fire Rod']],
            ["Turtle Rock - Roller Room - Left", False, [], ['Quake', 'Magic Mirror']],
            ["Turtle Rock - Roller Room - Left", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Quake', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Left", True, ['Fire Rod', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria']],
            ["Turtle Rock - Roller Room - Left", True, ['Fire Rod', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria']],
            ["Turtle Rock - Roller Room - Left", True, ['Fire Rod', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Left", True, ['Fire Rod', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Left", True, ['Moon Pearl', 'Fire Rod', 'Flute', 'Magic Mirror', 'Hookshot', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Left", True, ['Fire Rod', 'Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],

            ["Turtle Rock - Roller Room - Right", False, []],
            ["Turtle Rock - Roller Room - Right", False, [], ['Cane of Somaria']],
            ["Turtle Rock - Roller Room - Right", False, [], ['Fire Rod']],
            ["Turtle Rock - Roller Room - Right", False, [], ['Quake', 'Magic Mirror']],
            ["Turtle Rock - Roller Room - Right", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Quake', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Right", True, ['Fire Rod', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria']],
            ["Turtle Rock - Roller Room - Right", True, ['Fire Rod', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria']],
            ["Turtle Rock - Roller Room - Right", True, ['Fire Rod', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Right", True, ['Fire Rod', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Right", True, ['Moon Pearl', 'Fire Rod', 'Flute', 'Magic Mirror', 'Hookshot', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Roller Room - Right", True, ['Fire Rod', 'Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],

            ["Turtle Rock - Big Chest", False, []],
            ["Turtle Rock - Big Chest", False, [], ['Big Key (Turtle Rock)']],
            ["Turtle Rock - Big Chest", False, [], ['Magic Mirror', 'Cane of Somaria']],
            ["Turtle Rock - Big Chest", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Magic Mirror', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Chest", True, ['Bomb Upgrade (+5)', 'Big Key (Turtle Rock)', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Chest", True, ['Bomb Upgrade (+5)', 'Big Key (Turtle Rock)', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Chest", True, ['Big Key (Turtle Rock)', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cane of Somaria']],
            ["Turtle Rock - Big Chest", True, ['Big Key (Turtle Rock)', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Hookshot']],
            ["Turtle Rock - Big Chest", True, ['Big Key (Turtle Rock)', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot']],
            ["Turtle Rock - Big Chest", True, ['Big Key (Turtle Rock)', 'Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot']],
            ["Turtle Rock - Big Chest", True, ['Big Key (Turtle Rock)', 'Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Cane of Somaria']],
            ["Turtle Rock - Big Chest", True, ['Big Key (Turtle Rock)', 'Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Hookshot']],

            ["Turtle Rock - Big Key Chest", False, []],
            ["Turtle Rock - Big Key Chest", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Key Chest", True, ['Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Key Chest", True, ['Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            # Mirror in from ledge, use left side entrance, have enough keys to get to the chest
            ["Turtle Rock - Big Key Chest", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Key Chest", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Key Chest", True, ['Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Big Key Chest", True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],

            ["Turtle Rock - Crystaroller Room", False, []],
            ["Turtle Rock - Crystaroller Room", False, [], ['Big Key (Turtle Rock)', 'Magic Mirror']],
            ["Turtle Rock - Crystaroller Room", False, [], ['Big Key (Turtle Rock)', 'Cane of Somaria']],
            ["Turtle Rock - Crystaroller Room", False, [], ['Big Key (Turtle Rock)', 'Lamp']],
            ["Turtle Rock - Crystaroller Room", False, [], ['Magic Mirror', 'Cane of Somaria']],
            ["Turtle Rock - Crystaroller Room", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Magic Mirror', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Crystaroller Room", True, ['Big Key (Turtle Rock)', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Crystaroller Room", True, ['Big Key (Turtle Rock)', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Crystaroller Room", True, ['Big Key (Turtle Rock)', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],
            ["Turtle Rock - Crystaroller Room", True, ['Big Key (Turtle Rock)', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot']],
            ["Turtle Rock - Crystaroller Room", True, ['Big Key (Turtle Rock)', 'Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot']],
            ["Turtle Rock - Crystaroller Room", True, ['Big Key (Turtle Rock)', 'Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror']],
            ["Turtle Rock - Crystaroller Room", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cane of Somaria']],
            ["Turtle Rock - Crystaroller Room", True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Cane of Somaria']],
            ["Turtle Rock - Crystaroller Room", True, ['Lamp', 'Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot', 'Cane of Somaria']],

            ["Turtle Rock - Boss", False, []],
            ["Turtle Rock - Boss", False, [], ['Cane of Somaria']],
            ["Turtle Rock - Boss", False, [], ['Ice Rod']],
            ["Turtle Rock - Boss", False, [], ['Fire Rod']],
            ["Turtle Rock - Boss", False, [], ['Progressive Sword', 'Hammer']],
            ["Turtle Rock - Boss", False, [], ['Big Key (Turtle Rock)']],
            ["Turtle Rock - Boss", False, [], ['Magic Mirror', 'Lamp']],
            ["Turtle Rock - Boss", False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Small Key (Turtle Rock)']],
            ["Turtle Rock - Boss", True, ['Ice Rod', 'Fire Rod', 'Lamp', 'Flute', 'Quake', 'Progressive Sword', 'Progressive Sword', 'Cane of Somaria', 'Bottle', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Big Key (Turtle Rock)']],
            ["Turtle Rock - Boss", True, ['Ice Rod', 'Fire Rod', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Progressive Sword', 'Cane of Somaria', 'Bottle', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Big Key (Turtle Rock)']],
            ["Turtle Rock - Boss", True, ['Ice Rod', 'Fire Rod', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Progressive Sword', 'Cane of Somaria', 'Magic Upgrade (1/2)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)','Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Big Key (Turtle Rock)']],
            ["Turtle Rock - Boss", True, ['Ice Rod', 'Fire Rod', 'Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Hammer', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Big Key (Turtle Rock)']],
            ["Turtle Rock - Boss", True, ['Ice Rod', 'Fire Rod', 'Flute', 'Magic Mirror', 'Moon Pearl', 'Hookshot', 'Hammer', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Big Key (Turtle Rock)']]

        ])



    def testEyeBridge(self):
        for location in ["Turtle Rock - Eye Bridge - Top Right", "Turtle Rock - Eye Bridge - Top Left",
                         "Turtle Rock - Eye Bridge - Bottom Right", "Turtle Rock - Eye Bridge - Bottom Left"]:
            self.run_location_tests([
            [location, False, []],
            [location, False, ['Progressive Shield', 'Progressive Shield'], ['Progressive Shield', 'Cape', 'Cane of Byrna']],
            [location, False, [], ['Big Key (Turtle Rock)', 'Magic Mirror']],
            [location, False, [], ['Magic Mirror', 'Cane of Somaria']],
            [location, False, [], ['Magic Mirror', 'Lamp']],
            [location, False, ['Small Key (Turtle Rock)', 'Small Key (Turtle Rock)'], ['Magic Mirror', 'Small Key (Turtle Rock)']],
            [location, True, ['Big Key (Turtle Rock)', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Lamp', 'Cane of Byrna']],
            [location, True, ['Big Key (Turtle Rock)', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Cane of Byrna']],
            [location, True, ['Big Key (Turtle Rock)', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Lamp', 'Cape']],
            [location, True, ['Big Key (Turtle Rock)', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Cape']],
            [location, True, ['Big Key (Turtle Rock)', 'Flute', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Lamp', 'Progressive Shield', 'Progressive Shield', 'Progressive Shield']],
            [location, True, ['Big Key (Turtle Rock)', 'Lamp', 'Progressive Glove', 'Quake', 'Progressive Sword', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Progressive Shield', 'Progressive Shield', 'Progressive Shield']],

            # Mirroring into Eye Bridge does not require Cane of Somaria
            [location, True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cane of Byrna']],
            [location, True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Cane of Byrna']],
            [location, True, ['Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot', 'Cane of Byrna']],
            [location, True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Cane of Byrna']],
            [location, True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Cape']],
            [location, True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Cape']],
            [location, True, ['Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot', 'Cape']],
            [location, True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Cape']],
            [location, True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove', 'Progressive Shield', 'Progressive Shield', 'Progressive Shield']],
            [location, True, ['Lamp', 'Magic Mirror', 'Progressive Glove', 'Moon Pearl', 'Hookshot', 'Progressive Shield', 'Progressive Shield', 'Progressive Shield']],
            [location, True, ['Moon Pearl', 'Flute', 'Magic Mirror', 'Hookshot', 'Progressive Shield', 'Progressive Shield', 'Progressive Shield']],
            [location, True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror', 'Progressive Shield', 'Progressive Shield', 'Progressive Shield']],
            ]
            )
