from . import CV64TestBase


class WarpTest(CV64TestBase):
    options = {
        "special1s_per_warp": 3,
        "total_special1s": 21
    }

    def testWarps(self):
        for i in range(1, 8):
            self.assertFalse(self.can_reach_entrance(f"Warp {i}"))
            self.collect([self.get_item_by_name("Special1")] * 2)
            self.assertFalse(self.can_reach_entrance(f"Warp {i}"))
            self.collect([self.get_item_by_name("Special1")] * 1)
            self.assertTrue(self.can_reach_entrance(f"Warp {i}"))


class CastleWallTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "starting_stage": 1
    }

    def testDoors(self):
        self.assertFalse(self.can_reach_entrance(f"Left Tower door"))
        self.collect([self.get_item_by_name("Left Tower Key")] * 1)
        self.assertTrue(self.can_reach_entrance(f"Left Tower door"))


class VillaTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "starting_stage": 2
    }

    def testDoors(self):
        self.assertFalse(self.can_reach_entrance("To Storeroom door"))
        self.collect([self.get_item_by_name("Storeroom Key")] * 1)
        self.assertTrue(self.can_reach_entrance("To Storeroom door"))
        self.assertFalse(self.can_reach_entrance("To Archives door"))
        self.collect([self.get_item_by_name("Archives Key")] * 1)
        self.assertTrue(self.can_reach_entrance("To Archives door"))
        self.assertFalse(self.can_reach_entrance("To maze gate"))
        self.assertFalse(self.can_reach_entrance("Copper door"))
        self.collect([self.get_item_by_name("Garden Key")] * 1)
        self.assertTrue(self.can_reach_entrance("To maze gate"))
        self.assertFalse(self.can_reach_entrance("Copper door"))
        self.collect([self.get_item_by_name("Copper Key")] * 1)
        self.assertTrue(self.can_reach_entrance("Copper door"))


class CastleCenterTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "starting_stage": 5
    }

    def testDoors(self):
        self.assertFalse(self.can_reach_entrance("Torture Chamber door"))
        self.collect([self.get_item_by_name("Chamber Key")] * 1)
        self.assertTrue(self.can_reach_entrance("Torture Chamber door"))
        self.assertFalse(self.can_reach_entrance("Lower sealed cracked wall"))
        self.assertFalse(self.can_reach_entrance("Upper cracked wall"))
        self.collect([self.get_item_by_name("Magical Nitro")] * 1)
        self.assertFalse(self.can_reach_entrance("Upper cracked wall"))
        self.assertFalse(self.can_reach_entrance("Lower sealed cracked wall"))
        self.collect([self.get_item_by_name("Mandragora")] * 1)
        self.assertTrue(self.can_reach_entrance("Upper cracked wall"))
        self.assertFalse(self.can_reach_entrance("Lower sealed cracked wall"))
        self.collect([self.get_item_by_name("Magical Nitro")] * 1)
        self.assertFalse(self.can_reach_entrance("Lower sealed cracked wall"))
        self.collect([self.get_item_by_name("Mandragora")] * 1)
        self.assertTrue(self.can_reach_entrance("Upper cracked wall"))


class ExecutionTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "starting_stage": 7
    }

    def testDoors(self):
        self.assertFalse(self.can_reach_entrance("Execution gate"))
        self.collect([self.get_item_by_name("Execution Key")] * 1)
        self.assertTrue(self.can_reach_entrance("Execution gate"))


class ScienceTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "starting_stage": 8
    }

    def testDoors(self):
        self.assertFalse(self.can_reach_entrance("Science Door 1"))
        self.collect([self.get_item_by_name("Science Key1")] * 1)
        self.assertTrue(self.can_reach_entrance("Science Door 1"))
        self.assertFalse(self.can_reach_entrance("To Science Door 2"))
        self.assertFalse(self.can_reach_entrance("Science Door 3"))
        self.collect([self.get_item_by_name("Science Key2")] * 1)
        self.assertTrue(self.can_reach_entrance("To Science Door 2"))
        self.assertFalse(self.can_reach_entrance("Science Door 3"))
        self.collect([self.get_item_by_name("Science Key3")] * 1)
        self.assertTrue(self.can_reach_entrance("Science Door 3"))


class ClocktowerTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "starting_stage": 11
    }

    def testDoors(self):
        self.assertFalse(self.can_reach_entrance("To Clocktower Door 1"))
        self.assertFalse(self.can_reach_entrance("To Clocktower Door 2"))
        self.assertFalse(self.can_reach_entrance("Clocktower Door 3"))
        self.collect([self.get_item_by_name("Clocktower Key1")] * 1)
        self.assertTrue(self.can_reach_entrance("To Clocktower Door 1"))
        self.assertFalse(self.can_reach_entrance("To Clocktower Door 2"))
        self.assertFalse(self.can_reach_entrance("Clocktower Door 3"))
        self.collect([self.get_item_by_name("Clocktower Key2")] * 1)
        self.assertTrue(self.can_reach_entrance("To Clocktower Door 2"))
        self.assertFalse(self.can_reach_entrance("Clocktower Door 3"))
        self.collect([self.get_item_by_name("Clocktower Key3")] * 1)
        self.assertTrue(self.can_reach_entrance("Clocktower Door 3"))


class DraculaNoneTest(CV64TestBase):
    options = {
        "draculas_condition": 0,
        "stage_shuffle": True,
        "starting_stage": 5,
    }

    def testDraculaNoneCondition(self):
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.collect([self.get_item_by_name("Left Tower Key"),
                      self.get_item_by_name("Garden Key"),
                      self.get_item_by_name("Copper Key"),
                      self.get_item_by_name("Science Key1"),
                      self.get_item_by_name("Science Key2"),
                      self.get_item_by_name("Science Key3"),
                      self.get_item_by_name("Clocktower Key1"),
                      self.get_item_by_name("Clocktower Key2"),
                      self.get_item_by_name("Clocktower Key3")] * 1)
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.collect([self.get_item_by_name("Special1")] * 7)
        self.assertTrue(self.can_reach_entrance("Dracula's door"))


class DraculaSpecialTest(CV64TestBase):
    options = {
        "draculas_condition": 3
    }

    def testDraculaSpecialCondition(self):
        self.assertFalse(self.can_reach_entrance("Clocktower Door 3"))
        self.collect([self.get_item_by_name("Left Tower Key"),
                      self.get_item_by_name("Garden Key"),
                      self.get_item_by_name("Copper Key"),
                      self.get_item_by_name("Magical Nitro"),
                      self.get_item_by_name("Mandragora"),
                      self.get_item_by_name("Clocktower Key1"),
                      self.get_item_by_name("Clocktower Key2"),
                      self.get_item_by_name("Clocktower Key3")] * 2)
        self.assertTrue(self.can_reach_entrance("Clocktower Door 3"))
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.collect([self.get_item_by_name("Special2")] * 9)
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.collect([self.get_item_by_name("Special2")] * 1)
        self.assertTrue(self.can_reach_entrance("Dracula's door"))


class DraculaCrystalTest(CV64TestBase):
    options = {
        "draculas_condition": 1,
        "stage_shuffle": True,
        "starting_stage": 5,
        "hard_logic": True
    }

    def testDraculaCrystalCondition(self):
        self.assertFalse(self.can_reach_entrance("Slope Jump to boss tower"))
        self.collect([self.get_item_by_name("Left Tower Key"),
                      self.get_item_by_name("Garden Key"),
                      self.get_item_by_name("Copper Key"),
                      self.get_item_by_name("Science Key1"),
                      self.get_item_by_name("Science Key2"),
                      self.get_item_by_name("Science Key3"),
                      self.get_item_by_name("Clocktower Key1"),
                      self.get_item_by_name("Clocktower Key2"),
                      self.get_item_by_name("Clocktower Key3")] * 1)
        self.assertFalse(self.can_reach_entrance("Slope Jump to boss tower"))
        self.collect([self.get_item_by_name("Special1")] * 7)
        self.assertTrue(self.can_reach_entrance("Slope Jump to boss tower"))
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.collect([self.get_item_by_name("Magical Nitro"),
                      self.get_item_by_name("Mandragora")] * 1)
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.assertFalse(self.can_reach_entrance("Lower sealed cracked wall"))
        self.collect([self.get_item_by_name("Magical Nitro"),
                      self.get_item_by_name("Mandragora")] * 1)
        self.assertTrue(self.can_reach_entrance("Lower sealed cracked wall"))
        self.assertTrue(self.can_reach_entrance("Dracula's door"))


class DraculaBossTest(CV64TestBase):
    options = {
        "draculas_condition": 2,
        "stage_shuffle": True,
        "starting_stage": 5,
        "hard_logic": True,
        "bosses_required": 16
    }

    def testDraculaBossCondition(self):
        self.assertFalse(self.can_reach_entrance("Slope Jump to boss tower"))
        self.collect([self.get_item_by_name("Left Tower Key"),
                      self.get_item_by_name("Garden Key"),
                      self.get_item_by_name("Copper Key"),
                      self.get_item_by_name("Science Key1"),
                      self.get_item_by_name("Science Key2"),
                      self.get_item_by_name("Science Key3"),
                      self.get_item_by_name("Clocktower Key1"),
                      self.get_item_by_name("Clocktower Key2"),
                      self.get_item_by_name("Clocktower Key3")] * 1)
        self.assertFalse(self.can_reach_entrance("Slope Jump to boss tower"))
        self.collect([self.get_item_by_name("Special1")] * 7)
        self.assertTrue(self.can_reach_entrance("Slope Jump to boss tower"))
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.collect([self.get_item_by_name("Magical Nitro"),
                      self.get_item_by_name("Mandragora")] * 1)
        self.assertFalse(self.can_reach_entrance("Dracula's door"))
        self.assertFalse(self.can_reach_entrance("Lower sealed cracked wall"))
        self.collect([self.get_item_by_name("Magical Nitro"),
                      self.get_item_by_name("Mandragora")] * 1)
        self.assertTrue(self.can_reach_entrance("Lower sealed cracked wall"))
        self.assertTrue(self.can_reach_entrance("Dracula's door"))


class LizardTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "draculas_condition": 2,
        "starting_stage": 4
    }

    def testLizardManTrio(self):
        self.assertTrue(self.can_reach_location("Underground Waterway: Lizard-man trio"))
