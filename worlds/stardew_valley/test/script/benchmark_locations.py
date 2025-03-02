"""
Copy of the script in test/benchmark, adapted to Stardew Valley.

Run with `python -m worlds.stardew_valley.test.script.benchmark_locations --options minimal_locations_maximal_items`
"""

import argparse
import collections
import gc
import logging
import os
import sys
import time
import typing

from BaseClasses import CollectionState, Location
from Utils import init_logging
from worlds.stardew_valley.stardew_rule.rule_explain import explain
from ... import test


def run_locations_benchmark():
    init_logging("Benchmark Runner")
    logger = logging.getLogger("Benchmark")

    class BenchmarkRunner:
        gen_steps: typing.Tuple[str, ...] = (
            "generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")
        rule_iterations: int = 100_000

        @staticmethod
        def format_times_from_counter(counter: collections.Counter[str], top: int = 5) -> str:
            return "\n".join(f"  {time:.4f} in {name}" for name, time in counter.most_common(top))

        def location_test(self, test_location: Location, state: CollectionState, state_name: str) -> float:
            with TimeIt(f"{test_location.game} {self.rule_iterations} "
                        f"runs of {test_location}.access_rule({state_name})", logger) as t:
                for _ in range(self.rule_iterations):
                    test_location.access_rule(state)
                # if time is taken to disentangle complex ref chains,
                # this time should be attributed to the rule.
                gc.collect()
            return t.dif

        def main(self):
            game = "Stardew Valley"
            summary_data: typing.Dict[str, collections.Counter[str]] = {
                "empty_state": collections.Counter(),
                "all_state": collections.Counter(),
            }
            try:
                parser = argparse.ArgumentParser()
                parser.add_argument('--options', help="Define the option set to use, from the preset in test/__init__.py .", type=str, required=True)
                parser.add_argument('--seed', help="Define the seed to use.", type=int, required=True)
                parser.add_argument('--location', help="Define the specific location to benchmark.", type=str, default=None)
                parser.add_argument('--state', help="Define the state in which the location will be benchmarked.", type=str, default=None)
                args = parser.parse_args()
                options_set = args.options
                options = getattr(test, options_set)()
                seed = args.seed
                location = args.location
                state = args.state

                multiworld = test.setup_solo_multiworld(options, seed)
                gc.collect()

                if location:
                    locations = [multiworld.get_location(location, 1)]
                else:
                    locations = sorted(multiworld.get_unfilled_locations())

                all_state = multiworld.get_all_state(False)
                for location in locations:
                    if state != "all_state":
                        time_taken = self.location_test(location, multiworld.state, "empty_state")
                        summary_data["empty_state"][location.name] = time_taken

                    if state != "empty_state":
                        time_taken = self.location_test(location, all_state, "all_state")
                        summary_data["all_state"][location.name] = time_taken

                total_empty_state = sum(summary_data["empty_state"].values())
                total_all_state = sum(summary_data["all_state"].values())

                logger.info(f"{game} took {total_empty_state / len(locations):.4f} "
                            f"seconds per location in empty_state and {total_all_state / len(locations):.4f} "
                            f"in all_state. (all times summed for {self.rule_iterations} runs.)")
                logger.info(f"Top times in empty_state:\n"
                            f"{self.format_times_from_counter(summary_data['empty_state'])}")
                logger.info(f"Top times in all_state:\n"
                            f"{self.format_times_from_counter(summary_data['all_state'])}")

                if len(locations) == 1:
                    logger.info(str(explain(locations[0].access_rule, all_state, False)))

            except Exception as e:
                logger.exception(e)

    runner = BenchmarkRunner()
    runner.main()


class TimeIt:
    def __init__(self, name: str, time_logger=None):
        self.name = name
        self.logger = time_logger
        self.timer = None
        self.end_timer = None

    def __enter__(self):
        self.timer = time.perf_counter()
        return self

    @property
    def dif(self):
        return self.end_timer - self.timer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.end_timer:
            self.end_timer = time.perf_counter()
        if self.logger:
            self.logger.info(f"{self.dif:.4f} seconds in {self.name}.")


def change_home():
    """Allow scripts to run from "this" folder."""
    old_home = os.path.dirname(__file__)
    sys.path.remove(old_home)
    new_home = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    os.chdir(new_home)
    sys.path.append(new_home)
    # fallback to local import
    sys.path.append(old_home)

    from Utils import local_path
    local_path.cached_path = new_home


if __name__ == "__main__":
    run_locations_benchmark()
