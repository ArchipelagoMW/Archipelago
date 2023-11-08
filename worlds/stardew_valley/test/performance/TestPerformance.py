import time

from BaseClasses import get_seed
from .. import SVTestCase, minimal_locations_maximal_items, allsanity_options_without_mods, \
    allsanity_options_with_mods, setup_multiworld, default_options

number_generations = 25
acceptable_deviation = 4


def performance_test_multiworld(tester, options, acceptable_time_per_player):
    number_players = len(options)
    acceptable_average_time = acceptable_time_per_player * number_players
    total_time = 0
    all_times = {}
    for i in range(number_generations):
        seed = get_seed()
        with tester.subTest(f"Seed: {seed}"):
            time_before = time.time()
            multiworld = setup_multiworld(options, seed)
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
    acceptable_time_per_player = 0.05
    options = default_options()

    def test_solo(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        # seed = 47965111899197590996
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_duo(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_5_player(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_10_player(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)


class TestMinLocationMaxItems(SVTestCase):
    acceptable_time_per_player = 0.6
    options = minimal_locations_maximal_items()

    def test_solo(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_duo(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_5_player(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_10_player(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)


class TestAllsanityWithoutMods(SVTestCase):
    acceptable_time_per_player = 0.1
    options = allsanity_options_without_mods()

    def test_solo(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_duo(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_5_player(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_10_player(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)


# class TestAllsanityWithMods(SVTestCase):
#
#     def test_allsanity_with_mods_has_at_least_locations(self):
#         allsanity_options = allsanity_options_with_mods()
#         multiworld = setup_solo_multiworld(allsanity_options)
