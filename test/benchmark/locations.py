def run_locations_benchmark():
    import argparse
    import logging
    import gc
    import collections
    import typing
    import sys

    from time_it import TimeIt

    from Utils import init_logging
    from BaseClasses import MultiWorld, CollectionState, Location
    from worlds import AutoWorld
    from worlds.AutoWorld import call_all

    init_logging("Benchmark Runner")
    logger = logging.getLogger("Benchmark")

    class BenchmarkRunner:
        gen_steps: typing.Tuple[str, ...] = (
            "generate_early",
            "create_regions",
            "create_items",
            "set_rules",
            "connect_entrances",
            "generate_basic",
            "pre_fill",
        )

        rule_iterations: int = 100_000

        if sys.version_info >= (3, 9):
            @staticmethod
            def format_times_from_counter(counter: collections.Counter[str], top: int = 5) -> str:
                return "\n".join(f"  {time:.4f} in {name}" for name, time in counter.most_common(top))
        else:
            @staticmethod
            def format_times_from_counter(counter: collections.Counter, top: int = 5) -> str:
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
            for game in sorted(AutoWorld.AutoWorldRegister.world_types):
                summary_data: typing.Dict[str, collections.Counter[str]] = {
                    "empty_state": collections.Counter(),
                    "all_state": collections.Counter(),
                }
                try:
                    multiworld = MultiWorld(1)
                    multiworld.game[1] = game
                    multiworld.player_name = {1: "Tester"}
                    multiworld.set_seed(0)
                    multiworld.state = CollectionState(multiworld)
                    args = argparse.Namespace()
                    for name, option in AutoWorld.AutoWorldRegister.world_types[game].options_dataclass.type_hints.items():
                        setattr(args, name, {
                            1: option.from_any(getattr(option, "default"))
                        })
                    multiworld.set_options(args)

                    gc.collect()
                    for step in self.gen_steps:
                        with TimeIt(f"{game} step {step}", logger):
                            call_all(multiworld, step)
                            gc.collect()

                    locations = sorted(multiworld.get_unfilled_locations())
                    if not locations:
                        continue

                    all_state = multiworld.get_all_state(False)
                    for location in locations:
                        time_taken = self.location_test(location, multiworld.state, "empty_state")
                        summary_data["empty_state"][location.name] = time_taken

                        time_taken = self.location_test(location, all_state, "all_state")
                        summary_data["all_state"][location.name] = time_taken

                    total_empty_state = sum(summary_data["empty_state"].values())
                    total_all_state = sum(summary_data["all_state"].values())

                    logger.info(f"{game} took {total_empty_state/len(locations):.4f} "
                                f"seconds per location in empty_state and {total_all_state/len(locations):.4f} "
                                f"in all_state. (all times summed for {self.rule_iterations} runs.)")
                    logger.info(f"Top times in empty_state:\n"
                                f"{self.format_times_from_counter(summary_data['empty_state'])}")
                    logger.info(f"Top times in all_state:\n"
                                f"{self.format_times_from_counter(summary_data['all_state'])}")

                except Exception as e:
                    logger.exception(e)

    runner = BenchmarkRunner()
    runner.main()


if __name__ == "__main__":
    from path_change import change_home
    change_home()
    run_locations_benchmark()
