import time

from Fill import distribute_items_restrictive, balance_multiworld_progression
from worlds import AutoWorld
from .. import SVTestCase, minimal_locations_maximal_items, allsanity_options_without_mods, setup_multiworld, default_options

# [get_seed() for i in range(25)]
default_seeds = [26726304721450259037, 19493037639362170392, 44164721370906817114, 26474738898839084739, 69120175480542843820, 48149350148064597489,
                 75234106657911542927, 48255445659788767477, 51403062784428569537, 83505207683697218321, 31443992552358718495, 32042780995456241834,
                 84919554258352630308, 85389057393026193188, 50198031915976050326, 77769362918960755651, 51141990932126554176, 25055921617426839758,
                 68571386399161661782, 10489282145478582746, 82013340299462479898, 6654626230008781183, 49570869596326935545, 37049567542350773517,
                 7595094757324306210]
number_generations = len(default_seeds)
acceptable_deviation = 4


def performance_test_multiworld(tester, options, acceptable_time_per_player, skip_fill=True):
    number_players = len(options)
    acceptable_average_time = acceptable_time_per_player * number_players
    total_time = 0
    all_times = {}
    for i, seed in enumerate(default_seeds):
        with tester.subTest(f"Seed: {seed}"):
            time_before = time.time()

            print(f"Starting world setup")
            multiworld = setup_multiworld(options, seed)
            if not skip_fill:
                distribute_items_restrictive(multiworld)
                AutoWorld.call_all(multiworld, 'post_fill')
                if multiworld.players > 1:
                    balance_multiworld_progression(multiworld)

            time_after = time.time()
            elapsed_time = time_after - time_before
            total_time += elapsed_time
            all_times[i] = elapsed_time
            print(f"Multiworld {i + 1}/{number_generations} [{seed}] generated in {elapsed_time} seconds")
            # tester.assertLessEqual(elapsed_time, acceptable_average_time * acceptable_deviation)
    size = size_name(number_players)
    average_time = total_time / number_generations
    # Remove outliers
    num_outliers = 0
    for world in all_times:
        if all_times[world] > average_time * 4:
            num_outliers += 1
            total_time -= all_times[world]
    average_time = total_time / (number_generations - num_outliers)
    print(f"Generated {(number_generations - num_outliers)} {size} multiworlds in {total_time} seconds")
    print(f"Average time per world: {average_time} seconds (Acceptable: {acceptable_average_time})")
    tester.assertLessEqual(average_time, acceptable_average_time)


def size_name(number_players):
    if number_players == 1:
        return "solo"
    elif number_players == 2:
        return "duo"
    elif number_players == 3:
        return "trio"
    return f"{number_players}-player"


class TestDefaultOptions(SVTestCase):
    acceptable_time_per_player = 0.04
    options = default_options()

    def test_solo(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        # seed = 47965111899197590996
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_duo(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_5_player(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_10_player(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)


class TestMinLocationMaxItems(SVTestCase):
    acceptable_time_per_player = 0.08
    options = minimal_locations_maximal_items()

    def test_solo(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_duo(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_5_player(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_10_player(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)


class TestAllsanityWithoutMods(SVTestCase):
    acceptable_time_per_player = 0.07
    options = allsanity_options_without_mods()

    def test_solo(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_duo(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_5_player(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

    def test_10_player(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player, self.skip_fill)

# class TestAllsanityWithMods(SVTestCase):
#
#     def test_allsanity_with_mods_has_at_least_locations(self):
#         allsanity_options = allsanity_options_with_mods()
#         multiworld = setup_solo_multiworld(allsanity_options)
