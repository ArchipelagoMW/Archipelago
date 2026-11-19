from Options import OptionError

from .bases import Dota2TestBase
from ..challenges import CHALLENGE_FAMILIES, FAMILIES, VALUES, rune_check, match_challenges, completed_quests, stat_checks, resolve_values, challenge_values
from ..dota_api import DotaMatchData, challenge_data, damage_by_type
from ..options import CheckValues


def sample_match(**fields) -> DotaMatchData:
    base = dict(match_id=1, hero_id=1, kills=0, deaths=0, assists=0, purchase=[], last_hits=0, denies=0,
                win=1, dewards=0, rosh=0)
    return DotaMatchData(**{**base, **fields})


class DefaultSeed(Dota2TestBase):
    def test_all_challenges_in_seed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertTrue({name for names in CHALLENGE_FAMILIES.values() for name in names} <= names)
        # Quests have a lower and a full target by default
        self.assertTrue({"Stack 10 Camps in Total", "Stack 20 Camps in Total", "Heal 15000 in Total", "Deal 120000 Magical Damage in Total"} <= names)
        self.assertNotIn("Stack 30 Camps in Total", names)
        self.assertIn("Stack 5 Camps in a Match", names)
        self.assertNotIn("Stack 10 Camps in a Match", names)
        self.assertTrue({"Heal 2000 in a Match", "Deal 25000 Physical Damage in a Match", "Land a 500 Magical Hit",
                         "Stun Enemies for 60s in a Match", "Stun Enemies for 400s in Total"} <= names)
        self.assertIn("Get 15 Kill(s)", names)
        self.assertNotIn("Get 5 Kill(s)", names)

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
        "check_values": {"Short Win Minutes": 25, "Kills": 8, "Last Hits": [250, 75, 150, 400, 600], "Total Camps Stacked": 30},
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
        self.assertEqual(values["Long Win Minutes"], 60)

    def test_stat_checks_in_seed(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Get 8 Kill(s)", names)
        self.assertNotIn("Get 15 Kill(s)", names)
        self.assertTrue({f"Get {n} Last Hits" for n in (75, 150, 250, 400, 600)} <= names)
        self.assertIn("Stack 30 Camps in Total", names)
        self.assertNotIn("Stack 10 Camps in Total", names)


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
                    {"Short Win Minutes": [20, 30]}, {"Kills": "lots"}, {"Last Hits": 460}, {"Total Camps Stacked": [10, 12]}, {"Camps Stacked": 7}):
            with self.assertRaises(ValueError, msg=bad):
                CheckValues(bad)

    def test_stat_checks(self) -> None:
        values = resolve_values({"Kills": [15, 1, 5]})
        checks = stat_checks(sample_match(kills=12, last_hits=460, camps_stacked=6), values)
        self.assertEqual(checks, ["Get 1 Kill(s)", "Get 5 Kill(s)", "Get 450 Last Hits", "Stack 5 Camps in a Match"])

    def test_match_challenges(self) -> None:
        values = resolve_values({})
        match = sample_match(first_blood=True, runes={"5": 2, "7": 0}, position=4,
                             duration=25 * 60, all_players_stayed=False, team_roshan_kills=1)
        checks = match_challenges(match, values)
        self.assertIn("Get First Blood", checks)
        self.assertIn("Pick up a Bounty Rune", checks)
        self.assertNotIn("Pick up a Water Rune", checks)
        self.assertEqual(rune_check("Wisdom"), "Use a Shrine of Wisdom")
        self.assertIn("Win as Position 4", checks)
        # Short but with a leaver or a bot: not a short win
        self.assertNotIn("Win a Short Match", checks)
        self.assertIn("Win a Match Where Your Team Took Roshan", checks)
        self.assertEqual(completed_quests({"camps_stacked": 15, "wards_placed": 3}, values), ["Stack 10 Camps in Total"])
        self.assertEqual(completed_quests({"camps_stacked": 20}, resolve_values({"Total Camps Stacked": 30})), [])
        self.assertEqual(completed_quests({"rune_pickups": 45}, values), ["Pick up 20 Runes in Total"])

    def test_rune_pickups_skip_shrines(self) -> None:
        me = {"player_slot": 0, "runes": {"5": 3, "8": 4, "1": 1}}
        self.assertEqual(challenge_data({"players": [me]}, me)["rune_pickups"], 4)

    def test_damage_by_type(self) -> None:
        me = {"damage_inflictor": {"null": 5000, "lina_laguna_blade": 3000, "juggernaut_omni_slash": 900,
                                   "pudge_meat_hook": 700, "blade_mail": 400},
              "hero_hits": {"null": 50, "lina_laguna_blade": 4, "juggernaut_omni_slash": 9, "pudge_meat_hook": 3},
              "max_hero_hit": {"value": 1200, "inflictor": "lina_laguna_blade"}}
        d = damage_by_type(me)
        # Attacks and Omni Slash are physical; Laguna Blade and Meat Hook (pure) magical; items neither
        self.assertEqual((d["physical_damage"], d["magical_damage"]), (5900, 3700))
        self.assertEqual((d["physical_hit"], d["magical_hit"]), (100, 1200))


class OriginalNames(Dota2TestBase):
    options = {"check_values": {"Kills": [1, 5, 10]}}

    def test_original_stat_names_keep_their_ids(self) -> None:
        # Seeds from the original apworld named these checks the same way, with the same ids
        ids = self.world.location_name_to_id
        self.assertEqual([ids["Get 1 Kill(s)"], ids["Get 5 Kill(s)"], ids["Get 10 Kill(s)"]], [7711739, 7711740, 7711741])


class TooManyChecksOff(Dota2TestBase):
    options = {"disabled_checks": ["Purchases", "Quests", "Runes", "Positions", "Kills", "Assists"],
               "primordial_fragments_to_win": 50}
    auto_construct = False

    def test_refused(self) -> None:
        with self.assertRaises(OptionError):
            self.world_setup()


class SeedThresholds(Dota2TestBase):
    def test_thresholds_from_old_seed_names(self) -> None:
        # A seed from the original apworld: three stat checks per stat by name, and no check_values
        old_seed = {"Get 1 Kill(s)", "Get 5 Kill(s)", "Get 10 Kill(s)", "Get 75 Last Hits", "Get 125 Last Hits"}
        values = challenge_values({}, old_seed)
        self.assertEqual(values["Kills"], [1, 5, 10])
        self.assertEqual(values["Assists"], [])
        checks = stat_checks(sample_match(kills=6, last_hits=200), values)
        self.assertEqual(checks, ["Get 1 Kill(s)", "Get 5 Kill(s)", "Get 75 Last Hits", "Get 125 Last Hits"])
