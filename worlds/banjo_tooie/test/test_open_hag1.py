from ..Names import itemName
from ..Options import OpenHag1, VictoryCondition
from . import BanjoTooieTestBase


class TestProgressionJiggies(BanjoTooieTestBase):
    options = {
        "jingaling_jiggy": "false"
    }

    def _test_progression_jiggies(self, expected_progression_jiggies) -> None:
        assert expected_progression_jiggies == len([
            item.name for item in self.multiworld.itempool
            if item.name == itemName.JIGGY
            and item.advancement
        ])


class TestOpenHag1WithHag1(TestProgressionJiggies):
    options = {
        **TestProgressionJiggies.options,
        "open_hag1": OpenHag1.option_true,
        "victory_condition": VictoryCondition.option_hag1
    }

    def test_progression_jiggies(self):
        self._test_progression_jiggies(60)


class TestOpenHag1WithBossesHag1(TestProgressionJiggies):
    options = {
        **TestProgressionJiggies.options,
        "open_hag1": OpenHag1.option_true,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1
    }

    def test_progression_jiggies(self):
        self._test_progression_jiggies(60)


class TestOpenHag1WithBosses(TestProgressionJiggies):
    options = {
        **TestProgressionJiggies.options,
        "open_hag1": OpenHag1.option_true,
        "victory_condition": VictoryCondition.option_boss_hunt
    }

    def test_progression_jiggies(self):
        self._test_progression_jiggies(60)


class TestClosedHag1WithHag1(TestProgressionJiggies):
    options = {
        **TestProgressionJiggies.options,
        "open_hag1": OpenHag1.option_false,
        "victory_condition": VictoryCondition.option_hag1
    }

    def test_progression_jiggies(self):
        self._test_progression_jiggies(75)


class TestClosedHag1WithBossesHag1(TestProgressionJiggies):
    options = {
        **TestProgressionJiggies.options,
        "open_hag1": OpenHag1.option_false,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1
    }

    def test_progression_jiggies(self):
        self._test_progression_jiggies(60)


class TestClosedHag1WithBosses(TestProgressionJiggies):
    options = {
        **TestProgressionJiggies.options,
        "open_hag1": OpenHag1.option_false,
        "victory_condition": VictoryCondition.option_boss_hunt
    }

    def test_progression_jiggies(self):
        self._test_progression_jiggies(60)
