from .TestInvertedOWG import TestInvertedOWG


class TestDungeons(TestInvertedOWG):

    def testFirstDungeonChests(self):
        self.run_location_tests([
            ["Hyrule Castle - Map Chest", False, []],
            ["Hyrule Castle - Map Chest", True, ['Beat Agahnim 1']],
            ["Hyrule Castle - Map Chest", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hyrule Castle - Map Chest", True, ['Magic Mirror', 'Pegasus Boots']],

            ["Sanctuary", False, []],
            ["Sanctuary", False, ['Beat Agahnim 1']],
            ["Sanctuary", True, ['Magic Mirror', 'Beat Agahnim 1']],
            ["Sanctuary", True, ['Lamp', 'Beat Agahnim 1', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)']],
            ["Sanctuary", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Sanctuary", True, ['Magic Mirror', 'Pegasus Boots']],

            ["Sewers - Secret Room - Left", False, []],
            ["Sewers - Secret Room - Left", True, ['Moon Pearl', 'Progressive Glove', 'Pegasus Boots']],
            ["Sewers - Secret Room - Left", True, ['Moon Pearl', 'Pegasus Boots', 'Lamp', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)']],
            ["Sewers - Secret Room - Left", True, ['Magic Mirror', 'Pegasus Boots', 'Lamp', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)']],
            ["Sewers - Secret Room - Left", True, ['Bomb Upgrade (+5)', 'Beat Agahnim 1', 'Lamp', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)', 'Small Key (Hyrule Castle)']],

            ["Eastern Palace - Compass Chest", False, []],
            ["Eastern Palace - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Eastern Palace - Compass Chest", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Eastern Palace - Compass Chest", True, ['Beat Agahnim 1']],

            ["Desert Palace - Map Chest", False, []],
            ["Desert Palace - Map Chest", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Desert Palace - Map Chest", True, ['Book of Mudora', 'Magic Mirror', 'Pegasus Boots']],

            ["Desert Palace - Boss", False, []],
            ["Desert Palace - Boss", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Big Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Lamp', 'Fire Rod']],
            ["Desert Palace - Boss", True, ['Progressive Sword', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Moon Pearl', 'Pegasus Boots', 'Lamp']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Moon Pearl', 'Pegasus Boots', 'Fire Rod']],

            ["Tower of Hera - Basement Cage", False, []],
            ["Tower of Hera - Basement Cage", False, [], ['Moon Pearl']],
            ["Tower of Hera - Basement Cage", True, ['Pegasus Boots', 'Moon Pearl', 'Bomb Upgrade (50)']],
            ["Tower of Hera - Basement Cage", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Sword']],

            ["Castle Tower - Room 03", False, []],
            ["Castle Tower - Room 03", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Room 03", True, ['Pegasus Boots', 'Progressive Sword']],
            ["Castle Tower - Room 03", True, ['Pegasus Boots', 'Progressive Bow']],

            # Qirn Jump
            ["Palace of Darkness - Shooter Room", True, []],

            ["Swamp Palace - Entrance", False, []],
            ["Swamp Palace - Entrance", False, [], ['Magic Mirror']],
            ["Swamp Palace - Entrance", False, [], ['Flippers']],
            ["Swamp Palace - Entrance", True, ['Magic Mirror', 'Flippers', 'Pegasus Boots']],
            ["Swamp Palace - Entrance", True, ['Magic Mirror', 'Flippers', 'Beat Agahnim 1']],

            ["Skull Woods - Compass Chest", True, []],

            ["Skull Woods - Big Chest", False, []],
            ["Skull Woods - Big Chest", False, [], ['Big Key (Skull Woods)']],
            ["Skull Woods - Big Chest", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Skull Woods - Big Chest", True, ['Bomb Upgrade (+5)', 'Big Key (Skull Woods)']],

            ["Skull Woods - Big Key Chest", True, []],

            ["Skull Woods - Bridge Room", False, []],
            ["Skull Woods - Bridge Room", False, [], ['Fire Rod']],
            ["Skull Woods - Bridge Room", True, ['Fire Rod']],

            ["Thieves' Town - Map Chest", True, []],

            ["Ice Palace - Compass Chest", False, []],
            ["Ice Palace - Compass Chest", False, [], ['Fire Rod', 'Bombos', 'Progressive Sword']],
            # Qirn Jump
            ["Ice Palace - Compass Chest", True, ['Fire Rod', 'Small Key (Ice Palace)']],
            ["Ice Palace - Compass Chest", True, ['Bombos', 'Progressive Sword', 'Small Key (Ice Palace)']],

            ["Misery Mire - Bridge Chest", False, []],
            ["Misery Mire - Bridge Chest", False, [], ['Ether']],
            ["Misery Mire - Bridge Chest", False, [], ['Progressive Sword']],
            ["Misery Mire - Bridge Chest", True, ['Pegasus Boots', 'Ether', 'Progressive Sword']],

            ["Turtle Rock - Compass Chest", False, []],
            ["Turtle Rock - Compass Chest", False, [], ['Cane of Somaria']],
            ["Turtle Rock - Compass Chest", True, ['Pegasus Boots', 'Magic Mirror', 'Moon Pearl', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Compass Chest", True, ['Pegasus Boots', 'Quake', 'Progressive Sword', 'Cane of Somaria']],

            ["Turtle Rock - Chain Chomps", False, []],
            ["Turtle Rock - Chain Chomps", False, ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Hookshot', 'Progressive Sword', 'Progressive Bow', 'Blue Boomerang', 'Red Boomerang', 'Cane of Somaria', 'Fire Rod', 'Ice Rod']],
            ["Turtle Rock - Chain Chomps", True, ['Bomb Upgrade (+5)', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Hookshot', 'Pegasus Boots']],
            ["Turtle Rock - Chain Chomps", True, ['Progressive Bow', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Blue Boomerang', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Red Boomerang', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Cane of Somaria', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Fire Rod', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Ice Rod', 'Pegasus Boots', 'Magic Mirror', 'Moon Pearl']],
            ["Turtle Rock - Chain Chomps", True, ['Progressive Sword', 'Progressive Sword', 'Pegasus Boots']],

            ["Turtle Rock - Crystaroller Room", False, []],
            ["Turtle Rock - Crystaroller Room", True, ['Pegasus Boots', 'Magic Mirror', 'Moon Pearl', 'Big Key (Turtle Rock)']],
            ["Turtle Rock - Crystaroller Room", True, ['Pegasus Boots', 'Magic Mirror', 'Moon Pearl', 'Lamp', 'Cane of Somaria']],

            ["Ganons Tower - Hope Room - Left", False, []],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 1']],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 2']],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 3']],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 4']],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 5']],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 6']],
            ["Ganons Tower - Hope Room - Left", False, [], ['Crystal 7']],
            ["Ganons Tower - Hope Room - Left", True, ['Beat Agahnim 1', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7']],
            ["Ganons Tower - Hope Room - Left", True, ['Pegasus Boots', 'Magic Mirror', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7']],
            ["Ganons Tower - Hope Room - Left", True, ['Pegasus Boots', 'Moon Pearl', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7']],
        ])