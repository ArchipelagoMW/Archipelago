from .TestVanillaOWG import TestVanillaOWG


class TestDungeons(TestVanillaOWG):

    def testFirstDungeonChests(self):
        self.run_location_tests([
            ["Hyrule Castle - Map Chest", True, []],
            ["Hyrule Castle - Map Guard Key Drop", True, []],

            ["Sanctuary", True, []],

            ["Sewers - Secret Room - Left", False, []],
            ["Sewers - Secret Room - Left", True, ['Progressive Glove']],
            ["Sewers - Secret Room - Left", True, ['Lamp', 'Small Key (Hyrule Castle)']],

            ["Eastern Palace - Compass Chest", True, []],

            ["Desert Palace - Map Chest", False, []],
            ["Desert Palace - Map Chest", True, ['Pegasus Boots']],
            ["Desert Palace - Map Chest", True, ['Book of Mudora']],
            ["Desert Palace - Map Chest", True, ['Flute', 'Progressive Glove', 'Progressive Glove', 'Magic Mirror']],

            ["Desert Palace - Boss", False, []],
            ["Desert Palace - Boss", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Big Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Lamp', 'Fire Rod']],
            ["Desert Palace - Boss", True, ['Progressive Sword', 'Small Key (Desert Palace)', 'Pegasus Boots', 'Lamp', 'Big Key (Desert Palace)']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Pegasus Boots', 'Fire Rod', 'Big Key (Desert Palace)']],

            ["Tower of Hera - Basement Cage", False, []],
            ["Tower of Hera - Basement Cage", False, [], ['Pegasus Boots', "Flute", "Progressive Glove"]],
            ["Tower of Hera - Basement Cage", False, [], ['Pegasus Boots', "Flute", "Lamp"]],
            ["Tower of Hera - Basement Cage", False, [], ['Pegasus Boots', "Magic Mirror", "Hammer"]],
            ["Tower of Hera - Basement Cage", False, [], ['Pegasus Boots', "Magic Mirror", "Hookshot"]],
            ["Tower of Hera - Basement Cage", True, ['Pegasus Boots']],
            ["Tower of Hera - Basement Cage", True, ["Flute", "Magic Mirror"]],
            ["Tower of Hera - Basement Cage", True, ["Progressive Glove", "Lamp", "Magic Mirror"]],
            ["Tower of Hera - Basement Cage", True, ["Flute", "Hookshot", "Hammer"]],
            ["Tower of Hera - Basement Cage", True, ["Progressive Glove", "Lamp", "Magic Mirror"]],

            ["Castle Tower - Room 03", False, []],
            ["Castle Tower - Room 03", False, ['Progressive Sword'], ['Progressive Sword', 'Cape', 'Beat Agahnim 1']],
            ["Castle Tower - Room 03", False, [], ['Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Room 03", True, ['Progressive Sword', 'Progressive Sword']],
            ["Castle Tower - Room 03", True, ['Cape', 'Progressive Bow']],
            ["Castle Tower - Room 03", True, ['Beat Agahnim 1', 'Fire Rod']],

            ["Palace of Darkness - Shooter Room", False, []],
            ["Palace of Darkness - Shooter Room", False, [], ['Moon Pearl']],
            ["Palace of Darkness - Shooter Room", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Palace of Darkness - Shooter Room", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Palace of Darkness - Shooter Room", True, ['Moon Pearl', 'Hammer', 'Progressive Glove']],

            ["Palace of Darkness - Shooter Room", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Swamp Palace - Entrance", False, []],
            ["Swamp Palace - Entrance", False, [], ['Magic Mirror']],
            ["Swamp Palace - Entrance", False, [], ['Moon Pearl']],
            ["Swamp Palace - Entrance", False, [], ['Flippers']],
            ["Swamp Palace - Entrance", True, ['Magic Mirror', 'Moon Pearl', 'Flippers', 'Pegasus Boots']],
            ["Swamp Palace - Entrance", True, ['Magic Mirror', 'Moon Pearl', 'Flippers', 'Flute']],
            ["Swamp Palace - Entrance", True, ['Magic Mirror', 'Moon Pearl', 'Flippers', 'Hammer', 'Progressive Glove']],
            ["Swamp Palace - Entrance", True, ['Magic Mirror', 'Moon Pearl', 'Flippers', 'Progressive Glove', 'Progressive Glove']],

            ["Skull Woods - Compass Chest", False, []],
            ["Skull Woods - Compass Chest", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Skull Woods - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Skull Woods - Big Chest", False, []],
            ["Skull Woods - Big Chest", False, [], ['Big Key (Skull Woods)']],
            #todo: Bomb Jump in logic?
            #["Skull Woods - Big Chest", True, ['Magic Mirror', 'Pegasus Boots', 'Big Key (Skull Woods)']],
            ["Skull Woods - Big Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Big Key (Skull Woods)']],

            ["Skull Woods - Big Key Chest", False, []],
            ["Skull Woods - Big Key Chest", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Skull Woods - Big Key Chest", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Skull Woods - Bridge Room", False, []],
            ["Skull Woods - Bridge Room", False, [], ['Moon Pearl']],
            ["Skull Woods - Bridge Room", False, [], ['Fire Rod']],
            ["Skull Woods - Bridge Room", True, ['Moon Pearl', 'Pegasus Boots', 'Fire Rod']],

            ["Thieves' Town - Map Chest", False, []],
            ["Thieves' Town - Map Chest", False, [], ['Moon Pearl']],
            ["Thieves' Town - Map Chest", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Ice Palace - Compass Chest", False, []],
            ["Ice Palace - Compass Chest", False, [], ['Fire Rod', 'Bombos']],
            ["Ice Palace - Compass Chest", False, [], ['Fire Rod', 'Progressive Sword']],
            ["Ice Palace - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Flippers', 'Fire Rod']],
            ["Ice Palace - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Flippers', 'Bombos', 'Progressive Sword']],
            ["Ice Palace - Compass Chest", True, ['Progressive Glove', 'Progressive Glove', 'Fire Rod']],
            ["Ice Palace - Compass Chest", True, ['Progressive Glove', 'Progressive Glove', 'Bombos', 'Progressive Sword']],

            ["Misery Mire - Bridge Chest", False, []],
            ["Misery Mire - Bridge Chest", False, [], ['Moon Pearl']],
            ["Misery Mire - Bridge Chest", False, [], ['Ether']],
            ["Misery Mire - Bridge Chest", False, [], ['Progressive Sword']],
            ["Misery Mire - Bridge Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Ether', 'Progressive Sword']],

            ["Turtle Rock - Compass Chest", False, []],
            ["Turtle Rock - Compass Chest", False, [], ['Cane of Somaria']],
            #todo: does clip require sword?
            #["Turtle Rock - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],
            ["Turtle Rock - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Progressive Sword']],
            ["Turtle Rock - Compass Chest", True, ['Moon Pearl', 'Pegasus Boots', 'Cane of Somaria', 'Progressive Sword', 'Quake']],
            ["Turtle Rock - Compass Chest", True, ['Pegasus Boots', 'Magic Mirror', 'Cane of Somaria', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)', 'Small Key (Turtle Rock)']],

            ["Turtle Rock - Chain Chomps", False, []],
            #todo: does clip require sword?
            #["Turtle Rock - Chain Chomps", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Turtle Rock - Chain Chomps", True, ['Moon Pearl', 'Pegasus Boots', 'Progressive Sword']],
            ["Turtle Rock - Chain Chomps", True, ['Pegasus Boots', 'Magic Mirror']],

            ["Turtle Rock - Crystaroller Room", False, []],
            ["Turtle Rock - Crystaroller Room", False, [], ['Big Key (Turtle Rock)']],
            #todo: does clip require sword?
            #["Turtle Rock - Crystaroller Room", True, ['Moon Pearl', 'Pegasus Boots', 'Big Key (Turtle Rock)']],
            ["Turtle Rock - Crystaroller Room", True, ['Moon Pearl', 'Pegasus Boots', 'Big Key (Turtle Rock)', 'Progressive Sword']],
            ["Turtle Rock - Crystaroller Room", True, ['Moon Pearl', 'Pegasus Boots', 'Big Key (Turtle Rock)', 'Hookshot']],
            ["Turtle Rock - Crystaroller Room", True, ['Pegasus Boots', 'Magic Mirror', 'Big Key (Turtle Rock)']],

            ["Ganons Tower - Hope Room - Left", False, []],
            ["Ganons Tower - Hope Room - Left", False, ['Moon Pearl', 'Crystal 1']],
            ["Ganons Tower - Hope Room - Left", False, ['Pegasus Boots', 'Crystal 1']],
            ["Ganons Tower - Hope Room - Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Ganons Tower - Hope Room - Left", True, ['Pegasus Boots', 'Hammer', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7']],
        ])