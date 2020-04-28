from test.vanilla.TestVanilla import TestVanilla


class TestDeathMountain(TestVanilla):

    def testWestDeathMountain(self):
        self.run_location_tests([
            ["Ether Tablet", False, []],
            ["Ether Tablet", False, [], ['Progressive Glove', 'Flute']],
            ["Ether Tablet", False, [], ['Lamp', 'Flute']],
            ["Ether Tablet", False, [], ['Magic Mirror', 'Hookshot']],
            ["Ether Tablet", False, [], ['Magic Mirror', 'Hammer']],
            ["Ether Tablet", False, ['Progressive Sword'], ['Progressive Sword']],
            ["Ether Tablet", False, [], ['Book of Mudora']],
            ["Ether Tablet", True, ['Flute', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword']],
            ["Ether Tablet", True, ['Progressive Glove', 'Lamp', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword']],
            ["Ether Tablet", True, ['Flute', 'Hammer', 'Hookshot', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword']],
            ["Ether Tablet", True, ['Progressive Glove', 'Lamp', 'Hammer', 'Hookshot', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword']],

            ["Old Man", False, []],
            ["Old Man", False, [], ['Progressive Glove', 'Flute']],
            ["Old Man", False, [], ['Lamp']],
            ["Old Man", True, ['Flute', 'Lamp']],
            ["Old Man", True, ['Progressive Glove', 'Lamp']],

            ["Spectacle Rock Cave", False, []],
            ["Spectacle Rock Cave", False, [], ['Progressive Glove', 'Flute']],
            ["Spectacle Rock Cave", False, [], ['Lamp', 'Flute']],
            ["Spectacle Rock Cave", True, ['Flute']],
            ["Spectacle Rock Cave", True, ['Progressive Glove', 'Lamp']],

            ["Spectacle Rock", False, []],
            ["Spectacle Rock", False, [], ['Progressive Glove', 'Flute']],
            ["Spectacle Rock", False, [], ['Lamp', 'Flute']],
            ["Spectacle Rock", False, [], ['Magic Mirror']],
            ["Spectacle Rock", True, ['Flute', 'Magic Mirror']],
            ["Spectacle Rock", True, ['Progressive Glove', 'Lamp', 'Magic Mirror']],
        ])
