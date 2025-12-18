from .bases import NineSolsTestBase


class TestVanillaLogic(NineSolsTestBase):
    options = {
        "shop_unlocks": "vanilla_like_locations",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(0, len([x for x in self.multiworld.get_items() if x.name == "Progressive Shop Unlock"]))


class TestSolSealsLogic(NineSolsTestBase):
    options = {
        "shop_unlocks": "sol_seals",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(0, len([x for x in self.multiworld.get_items() if x.name == "Progressive Shop Unlock"]))


class TestUnlockItemsLogic(NineSolsTestBase):
    options = {
        "shop_unlocks": "unlock_items",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(3, len([x for x in self.multiworld.get_items() if x.name == "Progressive Shop Unlock"]))
