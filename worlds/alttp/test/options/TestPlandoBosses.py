import unittest
from BaseClasses import PlandoOptions
from Options import PlandoBosses


class SingleBosses(PlandoBosses):
    bosses = {"B1", "B2"}
    locations = {"L1", "L2"}

    option_vanilla = 0
    option_shuffle = 1

    @staticmethod
    def can_place_boss(boss: str, location: str) -> bool:
        if boss == "b1" and location == "l1":
            return False
        return True


class MultiBosses(SingleBosses):
    bosses = SingleBosses.bosses  # explicit copy required
    locations = SingleBosses.locations
    duplicate_bosses = True

    option_singularity = 2  # required when duplicate_bosses = True


class TestPlandoBosses(unittest.TestCase):
    def testCI(self):
        """Bosses, locations and modes are supposed to be case-insensitive"""
        self.assertEqual(MultiBosses.from_any("L1-B2").value, "l1-b2;vanilla")
        self.assertEqual(MultiBosses.from_any("ShUfFlE").value, SingleBosses.option_shuffle)

    def testRandom(self):
        """Validate random is random"""
        import random
        random.seed(0)
        value1 = MultiBosses.from_any("random")
        random.seed(0)
        value2 = MultiBosses.from_text("random")
        self.assertEqual(value1, value2)
        for n in range(0, 100):
            if MultiBosses.from_text("random") != value1:
                break
        else:
            raise Exception("random is not random")

    def testShuffleMode(self):
        """Test that simple modes (no Plando) work"""
        self.assertEqual(MultiBosses.from_any("shuffle"), MultiBosses.option_shuffle)
        self.assertNotEqual(MultiBosses.from_any("vanilla"), MultiBosses.option_shuffle)

    def testPlacement(self):
        """Test that valid placements work and invalid placements fail"""
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l1-b1")
        MultiBosses.from_any("l1-b2;l2-b1")

    def testMixed(self):
        """Test that shuffle is applied for remaining locations"""
        self.assertIn("shuffle", MultiBosses.from_any("l1-b2;l2-b1;shuffle").value)
        self.assertIn("vanilla", MultiBosses.from_any("l1-b2;l2-b1").value)

    def testUnknown(self):
        """Test that unknown values throw exceptions"""
        # unknown boss
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l1-b0")
        # unknown location
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l0-b1")
        # swapped boss-location
        with self.assertRaises(ValueError):
            MultiBosses.from_any("b2-b2")
        # boss name in place of mode (no singularity)
        with self.assertRaises(ValueError):
            SingleBosses.from_any("b1")
        with self.assertRaises(ValueError):
            SingleBosses.from_any("l2-b2;b1")
        # location name in place of mode
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l1")
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l2-b2;l1")
        # mode name in place of location
        with self.assertRaises(ValueError):
            MultiBosses.from_any("shuffle-b2;vanilla")
        with self.assertRaises(ValueError):
            MultiBosses.from_any("shuffle-b2;l2-b2")
        # mode name in place of boss
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l2-shuffle;vanilla")
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l1-shuffle;l2-b2")

    def testOrder(self):
        """Can't use mode in random places"""
        with self.assertRaises(ValueError):
            MultiBosses.from_any("shuffle;l2-b2")

    def testDuplicateBoss(self):
        """Can place the same boss twice"""
        MultiBosses.from_any("l1-b2;l2-b2")
        with self.assertRaises(ValueError):
            SingleBosses.from_any("l1-b2;l2-b2")

    def testDuplicateLocation(self):
        """Can't use the same location twice"""
        with self.assertRaises(ValueError):
            MultiBosses.from_any("l1-b2;l1-b2")

    def testSingularity(self):
        """Test automatic singularity mode"""
        self.assertIn(";singularity", MultiBosses.from_any("b2").value)

    def testPlandoOptions(self):
        """Test that plando options verification works"""
        plandoed_string = "l1-b2;l2-b1"
        mixed_string = "l1-b2;shuffle"
        regular_string = "shuffle"
        plandoed = MultiBosses.from_any(plandoed_string)
        mixed = MultiBosses.from_any(mixed_string)
        regular = MultiBosses.from_any(regular_string)

        # plando should work with boss plando
        plandoed.verify(None, "Player", PlandoOptions.bosses)
        self.assertTrue(plandoed.value.startswith(plandoed_string))
        # plando should fall back to default without boss plando
        plandoed.verify(None, "Player", PlandoOptions.items)
        self.assertEqual(plandoed, MultiBosses.option_vanilla)
        # mixed should fall back to mode
        mixed.verify(None, "Player", PlandoOptions.items)  # should produce a warning and still work
        self.assertEqual(mixed, MultiBosses.option_shuffle)
        # mode stuff should just work
        regular.verify(None, "Player", PlandoOptions.items)
        self.assertEqual(regular, MultiBosses.option_shuffle)
