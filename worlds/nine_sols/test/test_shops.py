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


class TestShopRando(NineSolsTestBase):
    options = {
        "randomize_shops": True,
    }

    def test_default(self):
        self.assertEqual(self.getNonEventLocationCount(), 361)

        items = self.multiworld.get_items()
        self.assertEqual(0, len([x for x in items if x.name == "Arrow: Cloud Piercer"]))
        self.assertEqual(3, len([x for x in items if x.name == "Progressive Cloud Piercer"]))

        sphere1 = [loc.name for loc in self.multiworld.get_reachable_locations()]
        self.assertIn("3D Printer: 1st Low Cost Purchase", sphere1)
        self.assertNotIn("3D Printer: 1st Medium Cost Purchase", sphere1)

