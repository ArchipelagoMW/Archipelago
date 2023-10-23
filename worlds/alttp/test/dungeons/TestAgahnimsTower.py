from .TestDungeon import TestDungeon


class TestAgahnimsTower(TestDungeon):

    def testTower(self):
        self.starting_regions = ['Agahnims Tower']
        self.run_tests([
            ["Castle Tower - Room 03", False, []],
            ["Castle Tower - Room 03", False, [], ['Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Room 03", True, ['Progressive Sword']],

            ["Castle Tower - Dark Maze", False, []],
            ["Castle Tower - Dark Maze", False, [], ['Small Key (Agahnims Tower)']],
            ["Castle Tower - Dark Maze", False, [], ['Lamp']],
            ["Castle Tower - Dark Maze", False, [], ['Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Dark Maze", True, ['Progressive Sword', 'Small Key (Agahnims Tower)', 'Lamp']],

            ["Castle Tower - Dark Archer Key Drop", False, []],
            ["Castle Tower - Dark Archer Key Drop", False, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
            ["Castle Tower - Dark Archer Key Drop", False, [], ['Lamp']],
            ["Castle Tower - Dark Archer Key Drop", False, [], ['Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Dark Archer Key Drop", True, ['Progressive Sword', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Lamp']],

            ["Castle Tower - Circle of Pots Key Drop", False, []],
            ["Castle Tower - Circle of Pots Key Drop", False, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
            ["Castle Tower - Circle of Pots Key Drop", False, [], ['Lamp']],
            ["Castle Tower - Circle of Pots Key Drop", False, [], ['Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Circle of Pots Key Drop", True, ['Progressive Sword', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Lamp']],

            ["Agahnim 1", False, []],
            ["Agahnim 1", False, ['Small Key (Agahnims Tower)'], ['Small Key (Agahnims Tower)']],
            ["Agahnim 1", False, [], ['Progressive Sword']],
            ["Agahnim 1", False, [], ['Lamp']],
            ["Agahnim 1", True, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Lamp', 'Progressive Sword']],
        ])