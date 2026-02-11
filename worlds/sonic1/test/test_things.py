from Options import Toggle
from worlds.sonic1 import constants
from ..configurable import RingGoal
from . import Sonic1TestBase
from Fill import FillError, fill_restrictive

# We're pretty much checking that the game will generate sanely with all the options

# Defaults... this better work.
class TestBasic(Sonic1TestBase):
    pass
    
class TestFailure(Sonic1TestBase):
    """Confirm that no_local_keys does fail to generate like you'd expect from placement restrictions"""
    options = {
        "no_local_keys": Toggle.option_true
    }

    def test_fill(self):
        """Test that fill raises an error when it can't place any items"""
        self.assertRaises(FillError, fill_restrictive, self.multiworld, self.multiworld.state,
                          [L for L in self.multiworld.worlds[1].get_locations()], self.multiworld.itempool.copy())

class TestNoBuffs(Sonic1TestBase):
    """We want to make sure disabling the goal buff does what we expect"""
    options = { "allow_disable_goal": Toggle.option_true }
    
    def test_no_goal(self):
        self.assertEqual(self.count("Disable GOAL blocks"), 0)

class TestNoBuffs2(Sonic1TestBase):
    """We want to make sure disabling the R buff does what we expect"""
    options = { "allow_disable_r": Toggle.option_true }
    
    def test_no_r(self):
        self.assertEqual(self.count("Disable R blocks"), 0)

class TestHardMode(Sonic1TestBase):
    """This shouldn't actually do anything to world gen ... """
    options = { "hard_mode": Toggle.option_true }
    
    def test_fill_slot(self):
        """Just to be sure it's doing fill right"""
        fsd = self.multiworld.worlds[1].fill_slot_data()
        self.assertEqual(fsd["hard_mode"], 1)
        self.assertEqual(fsd["ring_goal"], RingGoal.default)

class TestNotEnoughRings(Sonic1TestBase):
    options = {"available_rings": 10}

    # this should succed buuuuut....
    def test_fill_correctly(self):
        self.collect_by_name("Shiny Ring")
        self.collect_by_name("Gold Ring")
        fsd = self.multiworld.worlds[1].fill_slot_data()
        self.assertEqual(fsd["ring_goal"], 10)
        self.assertEqual(self.count("Shiny Ring"), 10)
        self.assertEqual(self.count("Gold Ring"), 0)
        self.assertEqual(len([i for i in self.multiworld.itempool if i.name == "Gold Ring"]), 0)

class TestRingGoal(Sonic1TestBase):
    options = {"ring_goal": 0, "available_rings": 10}
    
    def test_fill_correctly(self):
        self.collect_all_but("Labyrinth Key")
        fsd = self.multiworld.worlds[1].fill_slot_data()
        self.assertEqual(fsd["ring_goal"], 0)
        self.assertEqual(self.count("Shiny Ring"), 0)
        self.assertEqual(len([i for i in self.multiworld.itempool if i.name == "Gold Ring"]), 10)

class TestFiller(Sonic1TestBase):
    options = {"boring_filler": Toggle.option_true}
    
    def test_fill_correctly(self):
        self.collect_all_but("Gold Ring")
        for s in constants.silly_filler:
          self.assertEqual(self.count(s[0]), 0)
