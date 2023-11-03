import time

from BaseClasses import get_seed
from .. import SVTestCase, minimal_locations_maximal_items, allsanity_options_without_mods, \
    allsanity_options_with_mods, setup_multiworld

number_generations = 10
acceptable_deviation = 2


def performance_test_multiworld(tester, options, acceptable_time_per_player):
    number_players = len(options)
    acceptable_average_time = acceptable_time_per_player * number_players
    total_time = 0
    for i in range(number_generations):
        seed = get_seed()
        with tester.subTest(f"Seed: {seed}"):
            time_before = time.time()
            multiworld = setup_multiworld(options, seed)
            time_after = time.time()
            elapsed_time = time_after - time_before
            print(f"Multiworld {i + 1}/{number_generations} [{seed}] generated in {elapsed_time} seconds")
            total_time += elapsed_time
            tester.assertLessEqual(elapsed_time, acceptable_average_time * acceptable_deviation)
    size = size_name(number_players)
    print(f"Generated {number_generations} {size} multiworlds in {total_time} seconds")
    average_time = total_time / number_generations
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


class TestMinLocationMaxItems(SVTestCase):
    acceptable_time_per_player = 0.35
    options = minimal_locations_maximal_items()

    def test_solo_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_duo_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_5_player_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_10_player_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 10
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)


class TestAllsanityWithoutMods(SVTestCase):
    acceptable_time_per_player = 0.35
    options = allsanity_options_without_mods()

    def test_solo_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 1
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_duo_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 2
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_5_player_multiworld(self):
        if self.skip_performance_tests:
            return

        number_players = 5
        multiworld_options = [self.options] * number_players
        performance_test_multiworld(self, multiworld_options, self.acceptable_time_per_player)

    def test_10_player_multiworld(self):
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
