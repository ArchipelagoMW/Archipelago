from . import KDL3TestBase
from .TestGoal import TestNormalGoal


class TestCopyAbilityShuffle(KDL3TestBase):
    options = {
        "goal_speed": "normal",
        "total_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
        "copy_ability_randomization": "enabled",
    }

    def testGoal(self):
        self.assertBeatable(False)
        heart_stars = self.get_items_by_name("Heart Star")
        self.collect(heart_stars[0:14])
        self.assertEqual(self.count("Heart Star"), 14)
        self.assertBeatable(False)
        self.collect(heart_stars[14:15])
        self.assertEqual(self.count("Heart Star"), 15)
        self.assertBeatable(False)
        self.collect_by_name(["Burning", "Cutter", "Kine"])
        self.assertBeatable(True)
        self.remove([self.get_item_by_name("Love-Love Rod")])
        self.collect(heart_stars)
        self.assertEqual(self.count("Heart Star"), 30)
        self.assertBeatable(True)

    def testKine(self):
        self.collect_by_name(["Cutter", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def testCutter(self):
        self.collect_by_name(["Kine", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def testBurning(self):
        self.collect_by_name(["Cutter", "Kine", "Heart Star"])
        self.assertBeatable(False)

    #def testValidAbilitiesForROB(self):


class TestAnimalShuffle(KDL3TestBase):
    options = {
        "goal_speed": "normal",
        "total_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
        "animal_randomization": "full",
    }

    def testGoal(self):
        self.assertBeatable(False)
        heart_stars = self.get_items_by_name("Heart Star")
        self.collect(heart_stars[0:14])
        self.assertEqual(self.count("Heart Star"), 14)
        self.assertBeatable(False)
        self.collect(heart_stars[14:15])
        self.assertEqual(self.count("Heart Star"), 15)
        self.assertBeatable(False)
        self.collect_by_name(["Burning", "Cutter", "Kine"])
        self.assertBeatable(True)
        self.remove([self.get_item_by_name("Love-Love Rod")])
        self.collect(heart_stars)
        self.assertEqual(self.count("Heart Star"), 30)
        self.assertBeatable(True)

    def testKine(self):
        self.collect_by_name(["Cutter", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def testCutter(self):
        self.collect_by_name(["Kine", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def testBurning(self):
        self.collect_by_name(["Cutter", "Kine", "Heart Star"])
        self.assertBeatable(False)

    def testLockedAnimals(self):
        self.assertTrue(self, self.multiworld.get_location("Ripple Field 5 - Animal 2", 1).item.name == "Pitch Spawn")
        self.assertTrue(self, self.multiworld.get_location("Iceberg 4 - Animal 1", 1).item.name == "ChuChu Spawn")
        self.assertTrue(self, self.multiworld.get_location("Sand Canyon 6 - Animal 1", 1).item.name in {"Kine Spawn", "Coo Spawn"})

class testAllShuffle(KDL3TestBase):
    options = {
        "goal_speed": "normal",
        "total_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
        "animal_randomization": "full",
        "copy_ability_randomization": "enabled",
    }

    def testGoal(self):
        self.assertBeatable(False)
        heart_stars = self.get_items_by_name("Heart Star")
        self.collect(heart_stars[0:14])
        self.assertEqual(self.count("Heart Star"), 14)
        self.assertBeatable(False)
        self.collect(heart_stars[14:15])
        self.assertEqual(self.count("Heart Star"), 15)
        self.assertBeatable(False)
        self.collect_by_name(["Burning", "Cutter", "Kine"])
        self.assertBeatable(True)
        self.remove([self.get_item_by_name("Love-Love Rod")])
        self.collect(heart_stars)
        self.assertEqual(self.count("Heart Star"), 30)
        self.assertBeatable(True)

    def testKine(self):
        self.collect_by_name(["Cutter", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def testCutter(self):
        self.collect_by_name(["Kine", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def testBurning(self):
        self.collect_by_name(["Cutter", "Kine", "Heart Star"])
        self.assertBeatable(False)

    def testLockedAnimals(self):
        self.assertTrue(self, self.multiworld.get_location("Ripple Field 5 - Animal 2", 1).item.name == "Pitch Spawn")
        self.assertTrue(self, self.multiworld.get_location("Iceberg 4 - Animal 1", 1).item.name == "ChuChu Spawn")
        self.assertTrue(self, self.multiworld.get_location("Sand Canyon 6 - Animal 1", 1).item.name in {"Kine Spawn", "Coo Spawn"})