from .TestDungeon import TestDungeon


class TestIcePalace(TestDungeon):

    def testIcePalace(self):
        self.starting_regions = ['Ice Palace (Entrance)']
        self.run_tests([
            ["Ice Palace - Big Key Chest", False, []],
            ["Ice Palace - Big Key Chest", False, [], ['Hammer']],
            ["Ice Palace - Big Key Chest", False, [], ['Progressive Glove']],
            ["Ice Palace - Big Key Chest", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Big Key Chest", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Big Key Chest", True, ['Progressive Glove', 'Fire Rod', 'Hammer', 'Hookshot', 'Small Key (Ice Palace)']],
            ["Ice Palace - Big Key Chest", True, ['Progressive Glove', 'Bombos', 'Progressive Sword', 'Hammer', 'Hookshot', 'Small Key (Ice Palace)']],
            #@todo: Change from item randomizer - Right side key door is only in logic if big key is in there
            #["Ice Palace - Big Key Chest", True, ['Progressive Glove', 'Cane of Byrna', 'Fire Rod', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Big Key Chest", True, ['Progressive Glove', 'Cane of Byrna', 'Bombos', 'Progressive Sword', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Big Key Chest", True, ['Progressive Glove', 'Cape', 'Fire Rod', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Big Key Chest", True, ['Progressive Glove', 'Cape', 'Bombos', 'Progressive Sword', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],

            ["Ice Palace - Compass Chest", False, []],
            ["Ice Palace - Compass Chest", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Compass Chest", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Compass Chest", True, ['Fire Rod']],
            ["Ice Palace - Compass Chest", True, ['Bombos', 'Progressive Sword']],

            ["Ice Palace - Map Chest", False, []],
            ["Ice Palace - Map Chest", False, [], ['Hammer']],
            ["Ice Palace - Map Chest", False, [], ['Progressive Glove']],
            ["Ice Palace - Map Chest", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Map Chest", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Map Chest", True, ['Progressive Glove', 'Fire Rod', 'Hammer', 'Hookshot', 'Small Key (Ice Palace)']],
            ["Ice Palace - Map Chest", True, ['Progressive Glove', 'Bombos', 'Progressive Sword', 'Hammer', 'Hookshot', 'Small Key (Ice Palace)']],
            #["Ice Palace - Map Chest", True, ['Progressive Glove', 'Cane of Byrna', 'Fire Rod', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Map Chest", True, ['Progressive Glove', 'Cane of Byrna', 'Bombos', 'Progressive Sword', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Map Chest", True, ['Progressive Glove', 'Cape', 'Fire Rod', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Map Chest", True, ['Progressive Glove', 'Cape', 'Bombos', 'Progressive Sword', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],

            ["Ice Palace - Spike Room", False, []],
            ["Ice Palace - Spike Room", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Spike Room", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Spike Room", True, ['Fire Rod', 'Hookshot', 'Small Key (Ice Palace)']],
            ["Ice Palace - Spike Room", True, ['Bombos', 'Progressive Sword', 'Hookshot', 'Small Key (Ice Palace)']],
            #["Ice Palace - Spike Room", True, ['Cape', 'Fire Rod', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Spike Room", True, ['Cape', 'Bombos', 'Progressive Sword', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Spike Room", True, ['Cane of Byrna', 'Fire Rod', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],
            #["Ice Palace - Spike Room", True, ['Cane of Byrna', 'Bombos', 'Progressive Sword', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)']],

            ["Ice Palace - Freezor Chest", False, []],
            ["Ice Palace - Freezor Chest", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Freezor Chest", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Freezor Chest", True, ['Fire Rod']],
            ["Ice Palace - Freezor Chest", True, ['Bombos', 'Progressive Sword']],

            ["Ice Palace - Iced T Room", False, []],
            ["Ice Palace - Iced T Room", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Iced T Room", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Iced T Room", True, ['Fire Rod']],
            ["Ice Palace - Iced T Room", True, ['Bombos', 'Progressive Sword']],

            ["Ice Palace - Big Chest", False, []],
            ["Ice Palace - Big Chest", False, [], ['Big Key (Ice Palace)']],
            ["Ice Palace - Big Chest", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Big Chest", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Big Chest", True, ['Big Key (Ice Palace)', 'Fire Rod']],
            ["Ice Palace - Big Chest", True, ['Big Key (Ice Palace)', 'Bombos', 'Progressive Sword']],

            ["Ice Palace - Boss", False, []],
            ["Ice Palace - Boss", False, [], ['Hammer']],
            ["Ice Palace - Boss", False, [], ['Progressive Glove']],
            ["Ice Palace - Boss", False, [], ['Big Key (Ice Palace)']],
            ["Ice Palace - Boss", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Boss", False, [], ['Fire Rod', 'Progressive Sword']],
            # need hookshot now to reach the right side for the 6th key
            ["Ice Palace - Boss", True, ['Progressive Glove', 'Big Key (Ice Palace)', 'Fire Rod', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)', 'Hookshot']],
            ["Ice Palace - Boss", True, ['Progressive Glove', 'Big Key (Ice Palace)', 'Fire Rod', 'Hammer', 'Cane of Somaria', 'Small Key (Ice Palace)', 'Hookshot']],
            ["Ice Palace - Boss", True, ['Progressive Glove', 'Big Key (Ice Palace)', 'Bombos', 'Progressive Sword', 'Hammer', 'Small Key (Ice Palace)', 'Small Key (Ice Palace)', 'Hookshot']],
            ["Ice Palace - Boss", True, ['Progressive Glove', 'Big Key (Ice Palace)', 'Bombos', 'Progressive Sword', 'Hammer', 'Cane of Somaria', 'Small Key (Ice Palace)', 'Hookshot']],
        ])