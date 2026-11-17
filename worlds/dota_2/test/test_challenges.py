from .bases import Dota2TestBase
from ..challenges import CHALLENGE_CHECKS, FAMILIES, VALUES, match_challenges, completed_quests
from ..dota_api import DotaMatchData
from ..options import CheckValues


class ChallengesOnByDefault(Dota2TestBase):
    def test_all_challenges_in_seed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertTrue(set(CHALLENGE_CHECKS) <= names)

    def test_default_values_in_slot_data(self) -> None:
        values = self.world.fill_slot_data()["check_values"]
        self.assertEqual(values, {name: default for name, (default, _, _) in VALUES.items()})


class DisabledChallenges(Dota2TestBase):
    options = {
        "disabled_checks": ["Runes", "Kill a Courier"],
        "check_values": {"Short Win Minutes": 25},
    }

    def test_disabled_checks_removed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for name in FAMILIES["Runes"] + ["Kill a Courier"]:
            self.assertNotIn(name, names)
        self.assertIn("Get First Blood", names)

    def test_changed_value_in_slot_data(self) -> None:
        values = self.world.fill_slot_data()["check_values"]
        self.assertEqual(values["Short Win Minutes"], 25)
        self.assertEqual(values["Long Win Minutes"], 60)


class ChallengeRules(Dota2TestBase):
    def test_value_out_of_range_refused(self) -> None:
        with self.assertRaises(ValueError):
            CheckValues({"Short Win Minutes": 5})

    def test_match_challenges(self) -> None:
        values = {name: default for name, (default, _, _) in VALUES.items()}
        match = DotaMatchData(match_id=1, hero_id=1, kills=0, deaths=0, assists=0, purchase=[], last_hits=0, denies=0,
                              win=1, dewards=0, rosh=0, first_blood=True, runes={"5": 2, "7": 0}, position=4,
                              duration=25 * 60, all_players_stayed=False, team_roshan_kills=2)
        checks = match_challenges(match, values)
        self.assertIn("Get First Blood", checks)
        self.assertIn("Pick up a Bounty Rune", checks)
        self.assertNotIn("Pick up a Water Rune", checks)
        self.assertIn("Win as Position 4", checks)
        # Short but with a leaver or a bot: not a short win
        self.assertNotIn("Win a Short Match", checks)
        self.assertIn("Win a Match Where Your Team Took Roshan", checks)
        self.assertEqual(completed_quests({"camps_stacked": 10, "wards_placed": 3}, values), ["Quest: Stack Camps"])
