from . import OuterWildsTestBase
from ..items import repeatable_filler_weights

trap_names = [
    "Ship Damage Trap",
    "Audio Trap",
    "Nap Trap",
]


class TestNoTrapsWorld(OuterWildsTestBase):
    options = {
        "trap_chance": 0
    }

    def test_no_traps_all_filler(self):
        for t in trap_names:
            self.assertEqual(len(self.get_items_by_name(t)), 0)

        filler_counts = (len(self.get_items_by_name(name)) for name in repeatable_filler_weights.keys())
        self.assertTrue(any(filler_counts))


class TestAllTrapsWorld(OuterWildsTestBase):
    options = {
        "trap_chance": 100
    }

    def test_all_traps_no_filler(self):
        trap_counts = (len(self.get_items_by_name(name)) for name in trap_names)
        self.assertTrue(any(trap_counts))

        for f in repeatable_filler_weights.keys():
            self.assertEqual(len(self.get_items_by_name(f)), 0)


class TestAllAudioTrapsWorld(OuterWildsTestBase):
    options = {
        "trap_chance": 100,
        "trap_type_weights": {
            "Ship Damage Trap": 0,
            "Nap Trap": 0,
            "Audio Trap": 1,
        }
    }

    def test_all_audio_traps(self):
        self.assertGreater(len(self.get_items_by_name("Audio Trap")), 0)

        for t in (t for t in trap_names if t != "Audio Trap"):
            self.assertEqual(len(self.get_items_by_name(t)), 0)

        for f in repeatable_filler_weights.keys():
            self.assertEqual(len(self.get_items_by_name(f)), 0)


class TestAllShipDamageTrapsWorld(OuterWildsTestBase):
    options = {
        "trap_chance": 100,
        "trap_type_weights": {
            "Ship Damage Trap": 1,
            "Nap Trap": 0,
            "Audio Trap": 0,
        }
    }

    def test_all_ship_damage_traps(self):
        self.assertGreater(len(self.get_items_by_name("Ship Damage Trap")), 0)

        for t in (t for t in trap_names if t != "Ship Damage Trap"):
            self.assertEqual(len(self.get_items_by_name(t)), 0)

        for f in repeatable_filler_weights.keys():
            self.assertEqual(len(self.get_items_by_name(f)), 0)


class TestEveryKindOfTrapWorld(OuterWildsTestBase):
    # this test is technically non-deterministic, but the odds of failure are very low,
    # especially if we keep the seed fixed
    seed = 1
    options = {
        "trap_chance": 100,
        "trap_type_weights": {
            "Ship Damage Trap": 1,
            "Nap Trap": 1,
            "Audio Trap": 1,
        }
    }

    def test_every_kind_of_trap(self):
        for t in trap_names:
            self.assertGreater(len(self.get_items_by_name(t)), 0)

        for f in repeatable_filler_weights.keys():
            self.assertEqual(len(self.get_items_by_name(f)), 0)
