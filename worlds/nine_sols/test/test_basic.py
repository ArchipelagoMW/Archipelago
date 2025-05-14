from .bases import NineSolsTestBase


class TestDefaultWorld(NineSolsTestBase):
    options = {}

    def test_default_world(self):
        self.assertEqual(self.getLocationCount(), 323)  # 318 default locations + 5 events

        # we don't assert on the whole slot_data dict because e.g. apworld_version would be tautological
        # instead we assert on the set of keys to make sure we haven't forgotten to test a new one
        slot_data = self.world.fill_slot_data()
        self.assertSetEqual(set(slot_data.keys()), {
            'apworld_version',
            'skip_soulscape_platforming'
        })
        # now for the "real" slot_data tests on our default world:
        self.assertEqual(slot_data['skip_soulscape_platforming'], 0)

        # breathing tests for logic assertion helpers
        self.assertReachableWith("Central Hall: Examine Launch Memoral", [])
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

    def test_default_world(self):
        self.assertEqual(
            self.multiworld.get_location("Kuafu's Vital Sanctum", self.player).item.name,
            "Seal of Kuafu"
        )


class TestSkipSoulscapePlatforming(NineSolsTestBase):
    options = {
        "skip_soulscape_platforming": True
    }

    def test_default_world(self):
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
