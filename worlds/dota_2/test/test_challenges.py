from Options import OptionError

from .bases import Dota2TestBase
from ..challenges import CHALLENGE_CHECKS, FAMILIES, VALUES, match_challenges, completed_quests, stat_checks, resolve_values
from ..dota_api import DotaMatchData
from ..options import CheckValues


def sample_match(**fields) -> DotaMatchData:
    base = dict(match_id=1, hero_id=1, kills=0, deaths=0, assists=0, purchase=[], last_hits=0, denies=0,
                win=1, dewards=0, rosh=0)
    return DotaMatchData(**{**base, **fields})


class DefaultSeed(Dota2TestBase):
    def test_all_challenges_in_seed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertTrue(set(CHALLENGE_CHECKS) <= names)
        self.assertIn("Kills #1", names)
        self.assertNotIn("Kills #2", names)

    def test_original_hero_pool(self) -> None:
        self.assertEqual(len(self.world.starting_hero_pool), 30)
        self.assertEqual([len(g) for g in self.world.hero_groups], [14] * 6 + [13])
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Win with Hero from Group 7", names)
        self.assertNotIn("Win with Hero from Group 8", names)

    def test_default_values_in_slot_data(self) -> None:
        values = self.world.fill_slot_data()["check_values"]
        self.assertEqual(values, resolve_values({}))
        self.assertEqual(values["Kills"], [15])


class CustomSeed(Dota2TestBase):
    options = {
        "starting_heroes": 50,
        "hero_groups": 12,
        "disabled_checks": ["Runes", "Kill a Courier", "Legs Wins", "Divine Rapier"],
        "check_values": {"Short Win Minutes": 25, "Kills": 8, "Last Hits": [250, 75, 150, 400, 600]},
    }

    def test_hero_pool(self) -> None:
        self.assertEqual(len(self.world.starting_hero_pool), 50)
        sizes = [len(g) for g in self.world.hero_groups]
        self.assertEqual(len(sizes), 12)
        self.assertEqual(sum(sizes) + 50, len(self.world.all_heroes))
        self.assertLessEqual(max(sizes) - min(sizes), 1)
        self.assertEqual(self.multiworld.itempool.count(self.world.create_item("Progressive Group Unlock")), 12)
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Win with Hero from Group 12", names)
        self.assertNotIn("Win with Hero from Group 13", names)

    def test_disabled_checks_removed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for name in FAMILIES["Runes"] + FAMILIES["Legs Wins"] + ["Kill a Courier", "Divine Rapier"]:
            self.assertNotIn(name, names)
        self.assertIn("Get First Blood", names)
        self.assertIn("Win as a Melee Hero", names)

    def test_changed_values_in_slot_data(self) -> None:
        values = self.world.fill_slot_data()["check_values"]
        self.assertEqual(values["Short Win Minutes"], 25)
        self.assertEqual(values["Kills"], [8])
        self.assertEqual(values["Last Hits"], [75, 150, 250, 400, 600])
        self.assertEqual(values["Long Win Minutes"], 50)

    def test_stat_checks_in_seed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Kills #1", names)
        self.assertNotIn("Kills #2", names)
        self.assertTrue({f"Last Hits #{n}" for n in range(1, 6)} <= names)


class NoPurchases(Dota2TestBase):
    options = {"disabled_checks": ["Purchases"]}

    def test_no_component_unlocks(self) -> None:
        self.assertFalse(any(item.name.startswith("Unlock ") for item in self.multiworld.itempool))


class ChallengeRules(Dota2TestBase):
    def test_value_out_of_range_refused(self) -> None:
        with self.assertRaises(ValueError):
            CheckValues({"Short Win Minutes": 5})

    def test_stat_values_checked(self) -> None:
        CheckValues({"Kills": 8, "Assists": [5, 20]})
        for bad in ({"Kills": 0}, {"Kills": [1, 2, 3, 4, 5, 6]}, {"Kills": [5, 5]}, {"Kills": []},
                    {"Short Win Minutes": [20, 30]}, {"Kills": "lots"}):
            with self.assertRaises(ValueError, msg=bad):
                CheckValues(bad)

    def test_stat_checks(self) -> None:
        values = resolve_values({"Kills": [15, 1, 5]})
        checks = stat_checks(sample_match(kills=12, last_hits=410), values)
        self.assertEqual(checks, ["Kills #1", "Kills #2", "Last Hits #1"])

    def test_match_challenges(self) -> None:
        values = resolve_values({})
        match = sample_match(first_blood=True, runes={"5": 2, "7": 0}, position=4,
                             duration=25 * 60, all_players_stayed=False, team_roshan_kills=1)
        checks = match_challenges(match, values)
        self.assertIn("Get First Blood", checks)
        self.assertIn("Pick up a Bounty Rune", checks)
        self.assertNotIn("Pick up a Water Rune", checks)
        self.assertIn("Win as Position 4", checks)
        # Short but with a leaver or a bot: not a short win
        self.assertNotIn("Win a Short Match", checks)
        self.assertIn("Win a Match Where Your Team Took Roshan", checks)
        self.assertEqual(completed_quests({"camps_stacked": 20, "wards_placed": 3}, values), ["Stack Camps"])


class TooManyChecksOff(Dota2TestBase):
    options = {"disabled_checks": ["Purchases", "Quests", "Runes", "Positions", "Kills", "Assists"],
               "primordial_fragments_to_win": 50}
    auto_construct = False

    def test_refused(self) -> None:
        with self.assertRaises(OptionError):
            self.world_setup()
