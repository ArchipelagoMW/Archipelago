from . import SoETestBase


class TestFragmentGoal(SoETestBase):
    options = {
        "energy_core": "fragments",
        "available_fragments": 21,
        "required_fragments": 20,
    }

    def testFragments(self):
        self.collect_by_name(["Gladiator Sword", "Diamond Eye", "Wheel", "Gauge"])
        self.assertBeatable(False)  # 0 fragments
        fragments = self.get_items_by_name("Energy Core Fragment")
        victory = self.get_item_by_name("Victory")
        self.collect(fragments[:-2])  # 1 too few
        self.assertEqual(self.count("Energy Core Fragment"), 19)
        self.assertBeatable(False)
        self.collect(fragments[-2:-1])  # exact
        self.assertEqual(self.count("Energy Core Fragment"), 20)
        self.assertBeatable(True)
        self.remove([victory])  # reset
        self.collect(fragments[-1:])  # 1 extra
        self.assertEqual(self.count("Energy Core Fragment"), 21)
        self.assertBeatable(True)

    def testNoWeapon(self):
        self.collect_by_name(["Diamond Eye", "Wheel", "Gauge", "Energy Core Fragment"])
        self.assertBeatable(False)

    def testNoRocket(self):
        self.collect_by_name(["Gladiator Sword", "Diamond Eye", "Wheel", "Energy Core Fragment"])
        self.assertBeatable(False)


class TestShuffleGoal(SoETestBase):
    options = {
        "energy_core": "shuffle",
    }

    def testCore(self):
        self.collect_by_name(["Gladiator Sword", "Diamond Eye", "Wheel", "Gauge"])
        self.assertBeatable(False)
        self.collect_by_name(["Energy Core"])
        self.assertBeatable(True)

    def testNoWeapon(self):
        self.collect_by_name(["Diamond Eye", "Wheel", "Gauge", "Energy Core"])
        self.assertBeatable(False)

    def testNoRocket(self):
        self.collect_by_name(["Gladiator Sword", "Diamond Eye", "Wheel", "Energy Core"])
        self.assertBeatable(False)
