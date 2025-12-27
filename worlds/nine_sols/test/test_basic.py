from .bases import NineSolsTestBase


class TestDefaultWorld(NineSolsTestBase):
    options = {}

    def test_default_world(self):
        self.assertEqual(self.getLocationCount(), 324)  # 318 default locations + 6 events

        # we don't assert on the whole slot_data dict because e.g. apworld_version would be tautological
        # instead we assert on the set of keys to make sure we haven't forgotten to test a new one
        slot_data = self.world.fill_slot_data()
        self.assertSetEqual(set(slot_data.keys()), {
            'apworld_version',
            'skip_soulscape_platforming',
            'seals_for_eigong',
            'seals_for_ethereal',
            'seals_for_prison',
            'jade_costs',
            'first_root_node_name',
            'logic_difficulty',
            'shop_unlocks',
            'kuafu_shop_unlock_sol_seals',
            'chiyou_shop_unlock_sol_seals',
            'kuafu_extra_inventory_unlock_sol_seals',
            'prevent_weakened_prison_state',
        })
        # now for the "real" slot_data tests on our default world:
        self.assertEqual(slot_data['skip_soulscape_platforming'], 0)
        self.assertEqual(slot_data['seals_for_eigong'], 8)
        self.assertEqual(slot_data['seals_for_ethereal'], 4)
        self.assertEqual(slot_data['seals_for_prison'], 3)
        self.assertEqual(slot_data['jade_costs'], 'vanilla')
        self.assertEqual(slot_data['first_root_node_name'], 'apeman_facility_monitoring')
        self.assertEqual(slot_data['logic_difficulty'], 0)
        self.assertEqual(slot_data['shop_unlocks'], 0)
        self.assertEqual(slot_data['kuafu_shop_unlock_sol_seals'], 1)
        self.assertEqual(slot_data['chiyou_shop_unlock_sol_seals'], 3)
        self.assertEqual(slot_data['kuafu_extra_inventory_unlock_sol_seals'], 5)
        self.assertEqual(slot_data['prevent_weakened_prison_state'], 0)

        # breathing tests for logic assertion helpers
        self.assertReachableWith("Central Hall: Examine Launch Memorial", [])
        self.assertNotReachableWith("Central Hall: Examine Council Tenets", [])
        self.assertReachableWith("Central Hall: Examine Council Tenets", [
            "Mystic Nymph: Scout Mode"
        ])

        # control for TestSkipSoulscapePlatforming
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [])
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash"
        ])
        self.assertReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",  # to reach CC
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",  # to trigger Lady E
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash", "Tai-Chi Kick"  # to reach and defeat Lady E
        ])


class TestShuffleSolSealsOff(NineSolsTestBase):
    options = {
        "shuffle_sol_seals": False
    }

    def test_shuffle_sol_seals_false(self):
        self.assertEqual(
            self.multiworld.get_location("Kuafu's Vital Sanctum", self.player).item.name,
            "Seal of Kuafu"
        )


class TestSkipSoulscapePlatforming(NineSolsTestBase):
    options = {
        "skip_soulscape_platforming": True
    }

    def test_skip_soulscape_platforming(self):
        # when the soulscape is skipped, TCK is no longer logically necessary to reach Lady E
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [])
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",
            "Event - Lady Ethereal Soulscape Unlocked"
        ])
        self.assertReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",  # to reach CC
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",  # to trigger Lady E
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash"  # to reach and defeat Lady E
        ])


class TestSolSealCounts(NineSolsTestBase):
    options = {
        "seals_for_ethereal": 1,
        "seals_for_prison": 2,
        "skip_soulscape_platforming": True,  # to make the relevant logic slightly simpler
    }

    def test_one_seal_for_ethereal(self):
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [])
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",  # to reach CC
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash",  # to reach and defeat Lady E
        ])
        self.assertReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",  # to reach CC
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash",  # to reach and defeat Lady E
            "Seal of Kuafu",  # only 1 seal to trigger Lady E
        ])

    def test_two_seals_for_prison(self):
        self.assertNotReachableWith("Prison: Near Root Node", [])
        self.assertNotReachableWith("Prison: Near Root Node", [
            "Mystic Nymph: Scout Mode", "Charged Strike", "Air Dash", "Tai-Chi Kick",  # to reach CC and FGH
        ])
        self.assertNotReachableWith("Prison: Near Root Node", [
            "Mystic Nymph: Scout Mode", "Charged Strike", "Air Dash", "Tai-Chi Kick",  # to reach CC and FGH
            "Seal of Kuafu",  # 1 seal is not enough
        ])
        self.assertReachableWith("Prison: Near Root Node", [
            "Mystic Nymph: Scout Mode", "Charged Strike", "Air Dash", "Tai-Chi Kick",  # to reach CC and FGH
            "Seal of Kuafu", "Seal of Goumang",  # 2 seals (and nymph) to trigger prison
        ])
