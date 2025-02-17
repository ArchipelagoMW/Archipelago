from collections import defaultdict

from ..Names import itemName
from . import BanjoTooieTestBase


class TrapTestBase(BanjoTooieTestBase):
    class Pool:
        def __init__(self):
            self.trap_distribution = defaultdict(int)
            self.filler_distribution = defaultdict(int)

    def pool(self) -> Pool:
        pool = self.Pool()
        for item in self.world.multiworld.itempool:
            if item.trap:
                pool.trap_distribution[item.name] += 1
            if item.filler:
                pool.filler_distribution[item.name] += 1

        return pool


class TestTrapsDisabled(TrapTestBase):
    options = {
        "traps": "false",
        "nestsanity": "false",
        "extra_trebleclefs_count": 0,
        "bass_clef_amount": 0,
        # to add 16 filler items
        "randomize_bk_moves": 0,
        "cheato_rewards": "true",
        "honeyb_rewards": "true",
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 16
        assert sum(pool.trap_distribution.values()) == 0


class TestTrapsDisabledWithNestsanity(TrapTestBase):
    options = {
        "traps": "false",
        "nestsanity": "true",
        "extra_trebleclefs_count": 0,
        "bass_clef_amount": 0,
        "randomize_bk_moves": 2,
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert pool.filler_distribution[itemName.ENEST] + pool.filler_distribution[itemName.FNEST] == 450 + 23
        assert sum(pool.trap_distribution.values()) == 0


class TestTrapsEnabled(TrapTestBase):
    options = {
        "traps": "true",
        "nestsanity": "false",
        "extra_trebleclefs_count": 0,
        "bass_clef_amount": 0,
        # to add 16 filler items
        "randomize_bk_moves": 0,
        "cheato_rewards": "true",
        "honeyb_rewards": "true",
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert sum(pool.trap_distribution.values()) == 16


class TestTrapsEnabledExtraClefs(TrapTestBase):
    options = {
        "traps": "true",
        "randomize_bk_moves": 2,
        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert sum(pool.trap_distribution.values()) == 30 + 21 * 3


class TestTrapsEnabledWithNestsanity(TrapTestBase):
    options = {
        "traps": "true",
        "randomize_bk_moves": 2,
        "nestsanity": "true",
        "traps_nests_ratio": 50,
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0
        assert sum(pool.trap_distribution.values()) == int(0.5 * (315 + 135)) + 23
        assert pool.filler_distribution[itemName.ENEST] == 158  # 315 * 0.5
        assert pool.filler_distribution[itemName.FNEST] == 67  # 135 * 0.5


class TestTrapsEnabledRespectDistribution(TrapTestBase):
    options = {
        "traps": "true",
        "randomize_bk_moves": 2,
        # nests config
        "nestsanity": "true",
        "traps_nests_ratio": 100,
        # notes config
        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
        # weights
        "golden_eggs_weight": 1,
        "trip_trap_weight": 1,
        "slip_trap_weight": 50,
        "transform_trap_weight": 50,
        "squish_trap_weight": 100,
        "tip_trap_weight": 100,
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0

        expected_traps = 315 + 135 + 23 + 30 + 3 * 21  ##566
        assert sum(pool.trap_distribution.values()) == expected_traps

        assert pool.trap_distribution[itemName.GEGGS] < 10
        assert pool.trap_distribution[itemName.TTRAP] < 10

        assert pool.trap_distribution[itemName.STRAP] > 50
        assert pool.trap_distribution[itemName.STRAP] < 150

        assert pool.trap_distribution[itemName.TRTRAP] > 50
        assert pool.trap_distribution[itemName.TRTRAP] < 150

        assert pool.trap_distribution[itemName.SQTRAP] > 150

        assert pool.trap_distribution[itemName.TITRAP] > 150


class TestTrapsEnabledDisableTraps(TrapTestBase):
    options = {
        "traps": "true",
        "randomize_bk_moves": 2,
        # nests config
        "nestsanity": "true",
        "traps_nests_ratio": 100,
        # notes config
        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
        # weights
        "golden_eggs_weight": 0,
        "trip_trap_weight": 50,
        "slip_trap_weight": 50,
        "transform_trap_weight": 50,
        "squish_trap_weight": 0,
        "tip_trap_weight": 50,
    }

    def test_trap_pool(self) -> None:
        pool = super().pool()

        assert pool.filler_distribution[itemName.NONE] == 0

        assert pool.trap_distribution[itemName.GEGGS] == 0
        assert pool.trap_distribution[itemName.SQTRAP] == 0
