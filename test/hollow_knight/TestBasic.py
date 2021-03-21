from test.hollow_knight import TestVanilla


class TestBasic(TestVanilla):

    def testSimple(self):
        self.run_location_tests([
            ["200_Geo-False_Knight_Chest", True, [], []],
            ["380_Geo-Soul_Master_Chest", False, [], ["Mantis_Claw"]],
        ])