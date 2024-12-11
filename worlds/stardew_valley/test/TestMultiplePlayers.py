from . import SVTestCase, setup_multiworld
from .. import True_
from ..options import FestivalLocations, StartingMoney
from ..strings.festival_check_names import FestivalCheck


def get_access_rule(multiworld, player: int, location_name: str):
    return multiworld.get_location(location_name, player).access_rule


class TestDifferentSettings(SVTestCase):

    def test_different_festival_settings(self):
        options_no_festivals = {FestivalLocations.internal_name: FestivalLocations.option_disabled}
        options_easy_festivals = {FestivalLocations.internal_name: FestivalLocations.option_easy}
        options_hard_festivals = {FestivalLocations.internal_name: FestivalLocations.option_hard}

        multiplayer_options = [options_no_festivals, options_easy_festivals, options_hard_festivals]
        multiworld = setup_multiworld(multiplayer_options)

        self.check_location_rule(multiworld, 1, FestivalCheck.egg_hunt, False)
        self.check_location_rule(multiworld, 2, FestivalCheck.egg_hunt, True, True)
        self.check_location_rule(multiworld, 3, FestivalCheck.egg_hunt, True, True)

    def test_different_money_settings(self):
        options_no_festivals_unlimited_money = {FestivalLocations.internal_name: FestivalLocations.option_disabled,
                                                StartingMoney.internal_name: -1}
        options_no_festivals_limited_money = {FestivalLocations.internal_name: FestivalLocations.option_disabled,
                                              StartingMoney.internal_name: 5000}
        options_easy_festivals_unlimited_money = {FestivalLocations.internal_name: FestivalLocations.option_easy,
                                                  StartingMoney.internal_name: -1}
        options_easy_festivals_limited_money = {FestivalLocations.internal_name: FestivalLocations.option_easy,
                                                StartingMoney.internal_name: 5000}
        options_hard_festivals_unlimited_money = {FestivalLocations.internal_name: FestivalLocations.option_hard,
                                                  StartingMoney.internal_name: -1}
        options_hard_festivals_limited_money = {FestivalLocations.internal_name: FestivalLocations.option_hard,
                                                StartingMoney.internal_name: 5000}

        multiplayer_options = [options_no_festivals_unlimited_money, options_no_festivals_limited_money,
                               options_easy_festivals_unlimited_money, options_easy_festivals_limited_money,
                               options_hard_festivals_unlimited_money, options_hard_festivals_limited_money]
        multiworld = setup_multiworld(multiplayer_options)

        self.check_location_rule(multiworld, 1, FestivalCheck.rarecrow_4, False)
        self.check_location_rule(multiworld, 2, FestivalCheck.rarecrow_4, False)

        self.check_location_rule(multiworld, 3, FestivalCheck.rarecrow_4, True, True)
        self.check_location_rule(multiworld, 4, FestivalCheck.rarecrow_4, True, False)

        self.check_location_rule(multiworld, 5, FestivalCheck.rarecrow_4, True, True)
        self.check_location_rule(multiworld, 6, FestivalCheck.rarecrow_4, True, False)

    def test_money_rule_caching(self):
        options_festivals_limited_money = {FestivalLocations.internal_name: FestivalLocations.option_easy,
                                           StartingMoney.internal_name: 5000}

        multiplayer_options = [options_festivals_limited_money, options_festivals_limited_money]
        multiworld = setup_multiworld(multiplayer_options)

        player_1_rarecrow_2 = get_access_rule(multiworld, 1, FestivalCheck.rarecrow_2)
        player_1_rarecrow_4 = get_access_rule(multiworld, 1, FestivalCheck.rarecrow_4)
        player_2_rarecrow_2 = get_access_rule(multiworld, 2, FestivalCheck.rarecrow_2)
        player_2_rarecrow_4 = get_access_rule(multiworld, 2, FestivalCheck.rarecrow_4)

        with self.subTest("Rules are not cached between players"):
            self.assertNotEqual(id(player_1_rarecrow_2), id(player_2_rarecrow_2))
            self.assertNotEqual(id(player_1_rarecrow_4), id(player_2_rarecrow_4))

        with self.subTest("Rules are cached for the same player"):
            self.assertEqual(id(player_1_rarecrow_2), id(player_1_rarecrow_4))
            self.assertEqual(id(player_2_rarecrow_2), id(player_2_rarecrow_4))

    def check_location_rule(self, multiworld, player: int, location_name: str, should_exist: bool, should_be_true: bool = False):
        has = "has" if should_exist else "doesn't have"
        rule = "without access rule" if should_be_true else f"with access rule"
        rule_text = f" {rule}" if should_exist else ""
        with self.subTest(f"Player {player} {has} {location_name}{rule_text}"):
            locations = multiworld.get_locations(player)
            locations_names = {location.name for location in locations}
            if not should_exist:
                self.assertNotIn(location_name, locations_names)
                return None

            self.assertIn(location_name, locations_names)
            access_rule = get_access_rule(multiworld, player, location_name)
            if should_be_true:
                self.assertEqual(access_rule, True_())
            else:
                self.assertNotEqual(access_rule, True_())
            return access_rule
