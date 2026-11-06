from ..options import (
    Badges,
    DeathLink,
    Difficulty,
    LongChecks,
    MonsterDolls,
    MultipleSaves,
    OverpoweredCheats,
    Remix,
    WinCondition,
)
from . import LoonylandTestBase


class TestMinimalOptions(LoonylandTestBase):
    options = {
        "win_condition": WinCondition.option_evilizer,
        "badges_required": 1,
        "difficulty": Difficulty.option_beginner,
        "long_checks": LongChecks.option_excluded,
        "multisave": MultipleSaves.option_disabled,
        "remix": Remix.option_excluded,
        "overpowered_cheats": OverpoweredCheats.option_excluded,
        "badges": Badges.option_none,
        "dolls": MonsterDolls.option_none,
        "death_link": DeathLink.option_false,
    }


class TestMinimalOptionsBadges(LoonylandTestBase):
    options = {
        "win_condition": WinCondition.option_badges,
        "badges_required": 26,
        "difficulty": Difficulty.option_beginner,
        "long_checks": LongChecks.option_excluded,
        "multisave": MultipleSaves.option_disabled,
        "remix": Remix.option_excluded,
        "overpowered_cheats": OverpoweredCheats.option_excluded,
        "badges": Badges.option_vanilla,
        "dolls": MonsterDolls.option_none,
        "death_link": DeathLink.option_false,
    }


class TestVanillaOptions(LoonylandTestBase):
    options = {
        "win_condition": WinCondition.option_evilizer,
        "badges_required": 1,
        "difficulty": Difficulty.option_beginner,
        "long_checks": LongChecks.option_excluded,
        "multisave": MultipleSaves.option_enabled,
        "remix": Remix.option_included,
        "overpowered_cheats": OverpoweredCheats.option_included,
        "badges": Badges.option_vanilla,
        "dolls": MonsterDolls.option_vanilla,
        "death_link": DeathLink.option_false,
    }


class TestFullOptionsEvil(LoonylandTestBase):
    options = {
        "win_condition": WinCondition.option_evilizer,
        "badges_required": 1,
        "difficulty": Difficulty.option_beginner,
        "long_checks": LongChecks.option_included,
        "multisave": MultipleSaves.option_enabled,
        "remix": Remix.option_included,
        "overpowered_cheats": OverpoweredCheats.option_included,
        "badges": Badges.option_full,
        "dolls": MonsterDolls.option_full,
        "death_link": DeathLink.option_false,
    }


class TestFullOptionsBadges(LoonylandTestBase):
    options = {
        "win_condition": WinCondition.option_badges,
        "badges_required": 40,
        "difficulty": Difficulty.option_beginner,
        "long_checks": LongChecks.option_included,
        "multisave": MultipleSaves.option_enabled,
        "remix": Remix.option_included,
        "overpowered_cheats": OverpoweredCheats.option_included,
        "badges": Badges.option_full,
        "dolls": MonsterDolls.option_full,
        "death_link": DeathLink.option_false,
    }
