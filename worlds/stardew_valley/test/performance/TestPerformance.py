import os
import time
import unittest
from dataclasses import dataclass
from statistics import mean, median, variance, stdev
from typing import List

from BaseClasses import get_seed
from Fill import distribute_items_restrictive, balance_multiworld_progression
from worlds import AutoWorld
from .. import SVTestCase, minimal_locations_maximal_items, setup_multiworld, default_6_x_x, allsanity_no_mods_6_x_x, allsanity_mods_6_x_x

assert default_6_x_x
assert allsanity_no_mods_6_x_x

default_number_generations = 25
acceptable_deviation = 4


@dataclass
class PerformanceResults:
    case: SVTestCase

    amount_of_players: int
    results: List[float]
    acceptable_mean: float

    def __repr__(self):
        size = size_name(self.amount_of_players)

        total_time = sum(self.results)
        mean_time = mean(self.results)
        median_time = median(self.results)
        stdev_time = stdev(self.results, mean_time)
        variance_time = variance(self.results, mean_time)

        return f"""Generated {len(self.results)} {size} multiworlds in {total_time:.2f} seconds. Average {mean_time:.2f} seconds (Acceptable: {self.acceptable_mean:.2f})
Mean: {mean_time:.2f} Median: {median_time:.2f} Stdeviation: {stdev_time:.2f} Variance: {variance_time:.4f} Deviation percent: {stdev_time / mean_time:.2%}"""


class SVPerformanceTestCase(SVTestCase):
    acceptable_time_per_player: float
    results: List[PerformanceResults]

    # Set False to not call the fill in the tests"""
    skip_fill: bool = True
    # Set True to print results as CSV"""
    csv: bool = False

    @classmethod
    def setUpClass(cls) -> None:
        performance_tests_key = "performance"
        if performance_tests_key not in os.environ or os.environ[performance_tests_key] != "True":
            raise unittest.SkipTest("Performance tests disabled")

        super().setUpClass()

        fill_tests_key = "fill"
        if fill_tests_key in os.environ:
            cls.skip_fill = os.environ[fill_tests_key] != "True"

        fixed_seed_key = "fixed_seed"
        if fixed_seed_key in os.environ:
            cls.fixed_seed = bool(os.environ[fixed_seed_key])
        else:
            cls.fixed_seed = False

        number_generations_key = "number_gen"
        if number_generations_key in os.environ:
            cls.number_generations = int(os.environ[number_generations_key])
        else:
            cls.number_generations = default_number_generations

        csv_key = "csv"
        if csv_key in os.environ:
            cls.csv = bool(os.environ[csv_key])

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.csv:
            csved_results = (f"{type(result.case).__name__},{result.amount_of_players},{val:.6f}"
                             for result in cls.results for val in result.results)
            for r in csved_results:
                print(r)
        else:
            case = None
            for result in cls.results:
                if type(result.case) is not case:
                    case = type(result.case)
                    print(case.__name__)
                print(result)
            print()

        super().tearDownClass()

    def performance_test_multiworld(self, options):
        amount_of_players = len(options)
        acceptable_average_time = self.acceptable_time_per_player * amount_of_players
        total_time = 0
        all_times = []
        seeds = [get_seed() for _ in range(self.number_generations)] if not self.fixed_seed else [85635032403287291967] * self.number_generations

        for i, seed in enumerate(seeds):
            with self.subTest(f"Seed: {seed}"):
                time_before = time.time()

                print("Starting world setup")
                multiworld = setup_multiworld(options, seed)
                if not self.skip_fill:
                    distribute_items_restrictive(multiworld)
                    AutoWorld.call_all(multiworld, 'post_fill')
                    if multiworld.players > 1:
                        balance_multiworld_progression(multiworld)

                time_after = time.time()
                elapsed_time = time_after - time_before
                total_time += elapsed_time
                all_times.append(elapsed_time)
                print(f"Multiworld {i + 1}/{self.number_generations} [{seed}] generated in {elapsed_time:.4f} seconds")
                # tester.assertLessEqual(elapsed_time, acceptable_average_time * acceptable_deviation)

        self.results.append(PerformanceResults(self, amount_of_players, all_times, acceptable_average_time))
        self.assertLessEqual(mean(all_times), acceptable_average_time)


def size_name(number_players):
    if number_players == 1:
        return "solo"
    elif number_players == 2:
        return "duo"
    elif number_players == 3:
        return "trio"
    return f"{number_players}-player"


class TestDefaultOptions(SVPerformanceTestCase):
    acceptable_time_per_player = 2
    options = default_6_x_x()
    results = []

    def test_solo(self):
        number_players = 1
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    def test_duo(self):
        number_players = 2
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    def test_5_player(self):
        number_players = 5
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    @unittest.skip
    def test_10_player(self):
        number_players = 10
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)


class TestMinLocationMaxItems(SVPerformanceTestCase):
    acceptable_time_per_player = 0.3
    options = minimal_locations_maximal_items()
    results = []

    def test_solo(self):
        number_players = 1
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    def test_duo(self):
        number_players = 2
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    def test_5_player(self):
        number_players = 5
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    def test_10_player(self):
        number_players = 10
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)


class TestAllsanityWithoutMods(SVPerformanceTestCase):
    acceptable_time_per_player = 10
    options = allsanity_no_mods_6_x_x()
    results = []

    def test_solo(self):
        number_players = 1
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    def test_duo(self):
        number_players = 2
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    @unittest.skip
    def test_5_player(self):
        number_players = 5
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    @unittest.skip
    def test_10_player(self):
        number_players = 10
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)


class TestAllsanityWithMods(SVPerformanceTestCase):
    acceptable_time_per_player = 25
    options = allsanity_mods_6_x_x()
    results = []

    @unittest.skip
    def test_solo(self):
        number_players = 1
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)

    @unittest.skip
    def test_duo(self):
        number_players = 2
        multiworld_options = [self.options] * number_players
        self.performance_test_multiworld(multiworld_options)
