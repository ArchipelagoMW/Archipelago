from .bases import OuterWildsTestBase
from ..options import EarlyKeyItem, Spawn


class TestRandomWarpDeterminism(OuterWildsTestBase):
    options = {
        "randomize_warp_platforms": True,
    }
    seed = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)

    def test_determinism(self):
        self.assertListEqual(self.world.warps, [
            ('SS', 'ATT'),
            ('ATP', 'ET'),
            ('BHF', 'BHT'),
            ('GD', 'THT'),
            ('BHNG', 'WHS'),
            ('ST', 'ETT'),
            ('GDT', 'TH'),
        ])


class TestHGTSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
    }


class TestHGTSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
        "randomize_warp_platforms": True,
    }


class TestTHSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
    }


class TestTHSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
        "randomize_warp_platforms": True,
    }


class TestBHSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
    }


class TestBHSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "randomize_warp_platforms": True,
    }


class TestGDSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_giants_deep,
    }


class TestGDSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_giants_deep,
        "randomize_warp_platforms": True,
    }


class TestHGTSpawnRandomWarpEKI(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
        "randomize_warp_platforms": True,
        "early_key_item": EarlyKeyItem.option_nomai_warp_codes,
    }


class TestStrangerSpawnSLMEKI(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": True,
        "spawn": Spawn.option_stranger,
        "early_key_item": EarlyKeyItem.option_stranger_light_modulator,
    }


class TestRandomNonVanillaSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_random_non_vanilla,
    }


class TestRandomNonVanillaSpawnWithDLC(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": True,
        "spawn": Spawn.option_random_non_vanilla,
    }
