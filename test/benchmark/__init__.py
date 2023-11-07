if __name__ == "__main__":
    from argparse import Namespace
    import logging
    import time
    import gc
    import collections
    import typing

    # makes this module runnable from its folder.
    import sys
    import os
    sys.path.remove(os.path.dirname(__file__))
    new_home = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    os.chdir(new_home)
    sys.path.append(new_home)

    from Utils import init_logging, local_path
    local_path.cached_path = new_home
    from BaseClasses import MultiWorld, CollectionState
    from worlds import AutoWorld
    from worlds.AutoWorld import call_all

    init_logging("Benchmark Runner")
    logger = logging.getLogger("Benchmark")


    class TimeIt:
        def __init__(self, name: str, log: bool = True):
            self.name = name
            self.log = log
            self.timer = None
            self.end_timer = None

        def __enter__(self):
            self.timer = time.perf_counter()
            return self

        def end(self):
            self.end_timer = time.perf_counter()

        @property
        def dif(self):
            return self.end_timer - self.timer

        def __exit__(self, exc_type, exc_val, exc_tb):
            if not self.end_timer:
                self.end_timer = time.perf_counter()
            logger.info(f"{self.dif:.4f} seconds in {self.name}.")

    class BenchmarkRunner:
        gen_steps: typing.Tuple[str, ...] = (
            "generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")
        rule_iterations: int = 100_000

        @staticmethod
        def format_times_from_counter(counter: collections.Counter[str], top: int = 5) -> str:
            return "\n".join(f"  {time:.4f} in {name}" for name, time in counter.most_common(top))

        def main(self):
            for game in AutoWorld.AutoWorldRegister.world_types:
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
                    args = Namespace()
                    for name, option in AutoWorld.AutoWorldRegister.world_types[game].options_dataclass.type_hints.items():
                        setattr(args, name, {
                            1: option.from_any(getattr(option, "default"))
                        })
                    multiworld.set_options(args)

                    gc.collect()
                    for step in self.gen_steps:
                        with TimeIt(f"{game} step {step}"):
                            call_all(multiworld, step)
                            gc.collect()

                    all_state = multiworld.get_all_state(False)
                    locations = multiworld.get_unfilled_locations()

                    for location in locations:
                        with TimeIt(f"{game} {self.rule_iterations} runs of {location}.access_rule(empty_state)") as t:
                            for _ in range(self.rule_iterations):
                                location.access_rule(multiworld.state)
                            # if time is taken to disentangle complex ref chains,
                            # this time should be attributed to the rule.
                            gc.collect()
                            t.end()
                            summary_data["empty_state"][location.name] = t.dif

                        with TimeIt(f"{game} {self.rule_iterations} runs of {location}.access_rule(all_state)"):
                            for _ in range(self.rule_iterations):
                                location.access_rule(all_state)
                            # if time is taken to disentangle complex ref chains,
                            # this time should be attributed to the rule.
                            gc.collect()
                            t.end()
                            summary_data["all_state"][location.name] = t.dif

                    if locations:
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
