from ..Items import SuitUpgrade
from ..data.Tricks import TrickDifficulty
from . import MetroidPrimeTestBase


class TestTricksNotEnabled(MetroidPrimeTestBase):
    options = {"trick_difficulty": TrickDifficulty.No_Tricks.value}

    def test_trick_difficulty_allows_access(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == False


class TestTrickDifficulty(MetroidPrimeTestBase):
    options = {
        "trick_difficulty": TrickDifficulty.Easy.value,
    }

    def test_trick_difficulty_allows_access(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == True


class TestTrickAllowListWithoutDifficulty(MetroidPrimeTestBase):
    options = {
        "trick_allow_list": ["Landing Site Scan Dash", "Alcove Escape"],
        "trick_difficulty": TrickDifficulty.No_Tricks.value,
    }

    def test_trick_allow_list_allows_access_without_difficulty(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == True


class TestTrickListsWithDifficulty(MetroidPrimeTestBase):
    options = {
        "trick_allow_list": ["Crashed Frigate Scan Dash"],
        "trick_deny_list": [
            "Landing Site Scan Dash",
        ],
        "trick_difficulty": TrickDifficulty.Easy.value,
    }

    def test_trick_deny_list_denies_access(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == False

    def test_trick_allow_list_allows_access_wit_difficulty(self):
        self.collect_by_name(SuitUpgrade.Missile_Expansion.value)
        self.collect_by_name(SuitUpgrade.Morph_Ball.value)
        assert self.can_reach_location("Tallon Overworld: Frigate Crash Site") == True
