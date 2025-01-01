from . import LoonylandTestBase
from ..options import *


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

    def test_minimal_options(self) -> None:
        #self.assertBeatable(True)
        self.test_all_state_can_reach_everything()

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

    def test_minimal_options(self) -> None:
        self.test_all_state_can_reach_everything()


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

    def test_vanilla_options(self) -> None:
        self.test_all_state_can_reach_everything()

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

    def test_full_options_evil(self) -> None:
        self.test_all_state_can_reach_everything()


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

    def test_full_options_evil(self) -> None:
        self.test_all_state_can_reach_everything()

