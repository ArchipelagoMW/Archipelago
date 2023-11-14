import time

from BaseClasses import get_seed
from .. import SVTestCase, minimal_locations_maximal_items, allsanity_options_without_mods, \
    allsanity_options_with_mods, setup_multiworld, default_options

number_generations = 5


def performance_test_multiworld(tester, options, option_text):
    number_players = len(options)
    total_time = 0
    all_times = {}
    for i in range(number_generations):
        seed = get_seed()
        time_before = time.time()
        multiworld = setup_multiworld(options, seed)
        time_after = time.time()
        elapsed_time = time_after - time_before
        total_time += elapsed_time
        all_times[i] = elapsed_time
    size = size_name(number_players)
    average_time = total_time / number_generations
    # Remove outliers
    num_outliers = 0
    for world in all_times:
        if all_times[world] > average_time * 4:
            num_outliers += 1
            total_time -= all_times[world]
    average_time = total_time / (number_generations - num_outliers)
    print(f"{option_text}:")
    print(f"\tGenerated {(number_generations - num_outliers)} {size} multiworlds in {total_time} seconds")
    print(f"\tAverage time per world: {average_time} seconds")
    return average_time


def size_name(number_players):
    if number_players == 1:
        return "solo"
    elif number_players == 2:
        return "duo"
    elif number_players == 3:
        return "trio"
    return f"{number_players}-player"


class TestIndividualAllsanityOptions(SVTestCase):

    def test_solo(self):
        if self.skip_performance_tests:
            return
        times = dict()
        allsanity_options = allsanity_options_without_mods()
        for option1 in allsanity_options:
            for option2 in allsanity_options:
                if option1 == option2:
                    continue
                options_text = f"{option1}: {allsanity_options[option1]}, {option2}: {allsanity_options[option2]}"
                with self.subTest(options_text):
                    multiworld_options = dict(minimal_locations_maximal_items())
                    multiworld_options[option1] = allsanity_options[option1]
                    multiworld_options[option2] = allsanity_options[option2]
                    times[options_text] = performance_test_multiworld(self, [multiworld_options], options_text)
        sorted_times = sorted(times, key=lambda x: times[x], reverse=True)
        for options in sorted_times:
            print(f"{options}: {times[options]}")
