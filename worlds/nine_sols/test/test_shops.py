from .bases import NineSolsTestBase


class TestVanillaShopUnlocks(NineSolsTestBase):
    options = {
        "shop_unlocks": "vanilla_like_locations",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(0, len([x for x in self.multiworld.get_items() if x.name == "Progressive Shop Unlock"]))


class TestSolSealsShopUnlocks(NineSolsTestBase):
    options = {
        "shop_unlocks": "sol_seals",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(0, len([x for x in self.multiworld.get_items() if x.name == "Progressive Shop Unlock"]))


class TestUnlockItemsShopUnlocks(NineSolsTestBase):
    options = {
        "shop_unlocks": "unlock_items",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(3, len([x for x in self.multiworld.get_items() if x.name == "Progressive Shop Unlock"]))


class TestItemsWithoutShopRando(NineSolsTestBase):
    options = {
        "randomize_shops": False,
    }

    def test_default(self):
        items = self.multiworld.get_items()
        self.assertEqual(1, len([x for x in items if x.name == "Arrow: Cloud Piercer"]))
        self.assertEqual(0, len([x for x in items if x.name == "Progressive Cloud Piercer"]))
        self.assertEqual(0, len([x for x in items if x.name == "Transmute Unto Wealth"]))
        self.assertEqual(0, len([x for x in items if x.name == "Transmute Unto Life"]))
        self.assertEqual(0, len([x for x in items if x.name == "Transmute Unto Qi"]))
        self.assertEqual(0, len([x for x in items if x.name == "Pipe Upgrade"]))


class TestShopRandoDefaultSpawn(NineSolsTestBase):
    options = {
        "randomize_shops": True,
    }

    def test_default(self):
        self.assertEqual(self.getNonEventLocationCount(), 361)

        items = self.multiworld.get_items()
        self.assertEqual(0, len([x for x in items if x.name == "Arrow: Cloud Piercer"]))
        self.assertEqual(3, len([x for x in items if x.name == "Progressive Cloud Piercer"]))
        self.assertEqual(1, len([x for x in items if x.name == "Transmute Unto Wealth"]))
        self.assertEqual(1, len([x for x in items if x.name == "Transmute Unto Life"]))
        self.assertEqual(1, len([x for x in items if x.name == "Transmute Unto Qi"]))
        self.assertEqual(8, len([x for x in items if x.name == "Pipe Upgrade"]))

        # none of the shop locations are in logic yet
        sphere1 = [loc.name for loc in self.multiworld.get_reachable_locations()]
        self.assertNotIn("3D Printer: 1st Low Cost Purchase", sphere1)
        self.assertNotIn("3D Printer: 1st Medium Cost Purchase", sphere1)

        # being able to reach PR (Central) puts Low Cost in logic
        self.assertNotReachableWith("3D Printer: 1st Low Cost Purchase", [
            "Mystic Nymph: Scout Mode"
        ])
        self.assertReachableWith("3D Printer: 1st Low Cost Purchase", [
            "Mystic Nymph: Scout Mode", "Tai-Chi Kick"
        ])

        # being able to reach ED (Passages) too puts Medium Cost in logic
        self.assertNotReachableWith("3D Printer: 1st Medium Cost Purchase", [
            "Mystic Nymph: Scout Mode", "Tai-Chi Kick", "Air Dash"
        ])
        self.assertReachableWith("3D Printer: 1st Medium Cost Purchase", [
            "Mystic Nymph: Scout Mode", "Tai-Chi Kick", "Air Dash", "Cloud Leap"
        ])

        # finally, being able to reach Factory (MR) via Prison (default 3 seals) too puts High Cost in logic
        self.assertNotReachableWith("3D Printer: 1st High Cost Purchase", [
            "Mystic Nymph: Scout Mode", "Tai-Chi Kick", "Air Dash", "Cloud Leap",
            "Charged Strike",  # to get through Cortex Center
            "Seal of Kuafu", "Seal of Goumang"
        ])
        self.assertReachableWith("3D Printer: 1st High Cost Purchase", [
            "Mystic Nymph: Scout Mode", "Tai-Chi Kick", "Air Dash", "Cloud Leap",
            "Charged Strike",  # to get through Cortex Center
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao"
        ])
