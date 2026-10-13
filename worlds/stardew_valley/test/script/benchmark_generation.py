"""
Generate a game while monitoring the location access rules calls and their performance.

Run with `python -m worlds.stardew_valley.test.script.generate_monitor_rules --options minimal_locations_maximal_items`
"""

import argparse
import gc
import time
from collections import defaultdict
from dataclasses import dataclass, field
from functools import wraps

from BaseClasses import CollectionState, get_seed
from Fill import distribute_items_restrictive, FillError
from test.general import gen_steps
from worlds import AutoWorld
from ..bases import setup_solo_multiworld
from ..options import presets
from ... import StardewValleyWorld
from ...rules import StardewRuleCollector
from ...stardew_rule import StardewRule


@dataclass(frozen=True)
class RuleCall:
    start_ns: int
    end_ns: int
    result: bool

    @property
    def duration_ns(self) -> int:
        return self.end_ns - self.start_ns


@dataclass(frozen=True)
class PerformanceMonitoringStardewRule(StardewRule):
    location: str
    delegate: StardewRule
    calls: list[RuleCall] = field(default_factory=list)

    def __call__(self, state: CollectionState) -> bool:
        start = time.perf_counter_ns()
        result = self.delegate(state)
        end = time.perf_counter_ns()
        self.calls.append(RuleCall(start, end, result))
        return result

    def __and__(self, other: StardewRule):
        raise NotImplementedError()

    def __or__(self, other: StardewRule):
        raise NotImplementedError()

    def evaluate_while_simplifying(self, state: CollectionState) -> tuple[StardewRule, bool]:
        raise NotImplementedError()


def write_results(monitored_rules: list[PerformanceMonitoringStardewRule], output_file: str) -> None:
    with open(output_file, 'w+') as results_file:

        results_file.write("name,start_ns,end_ns,duration,result\n")
        for rule in monitored_rules:
            for call in rule.calls:
                results_file.write(f"\"{rule.location}\",{call.start_ns},{call.end_ns},{call.end_ns - call.start_ns},{call.result}\n")


def generate_monitor_rules():
    parser = argparse.ArgumentParser()
    parser.add_argument('--options', help="Define the option set to use, from the preset in test/__init__.py .", type=str, required=True)
    parser.add_argument('--seed', help="Define the seed to use.", type=int)
    script_args = parser.parse_args()
    options_set = script_args.options
    options = getattr(presets, options_set)()
    fixed_seed = script_args.seed

    original_set_location_rule = StardewRuleCollector.set_location_rule
    original_set_entrance_rule = StardewRuleCollector.set_entrance_rule
    original_collect = StardewValleyWorld.collect
    original_remove = StardewValleyWorld.remove
    original_call_single = AutoWorld.call_single
    original_sweep_for_advancements = CollectionState.sweep_for_advancements
    original_update_reachable_regions = CollectionState.update_reachable_regions

    class Run:
        def __init__(self, index: int, seed: int):
            self.index = index
            self.seed = seed
            self.monitored_rules = []
            self.collects = []
            self.removes = []
            self.gen_steps = {}
            self.sweep_for_advancements = []
            self.update_reachable_regions = []

        def apply_patches(self):
            @wraps(original_set_location_rule)
            def patched_set_location_rule(self_, location_name: str, rule: StardewRule) -> None:
                wrapped = PerformanceMonitoringStardewRule("[location] " + location_name, rule)
                self.monitored_rules.append(wrapped)
                original_set_location_rule(self_, location_name, wrapped)

            StardewRuleCollector.set_location_rule = patched_set_location_rule

            @wraps(original_set_entrance_rule)
            def patched_set_entrance_rule(self_, entrance_name: str, rule: StardewRule) -> None:
                wrapped = PerformanceMonitoringStardewRule("[entrance] " + entrance_name, rule)
                self.monitored_rules.append(wrapped)
                original_set_entrance_rule(self_, entrance_name, wrapped)

            StardewRuleCollector.set_entrance_rule = patched_set_entrance_rule

            @wraps(original_collect)
            def patched_collect(*args, **kwargs):
                start = time.perf_counter_ns()
                result = original_collect(*args, **kwargs)
                end = time.perf_counter_ns()
                self.collects.append(end - start)
                return result

            StardewValleyWorld.collect = patched_collect

            @wraps(original_remove)
            def patched_remove(*args, **kwargs):
                start = time.perf_counter_ns()
                result = original_remove(*args, **kwargs)
                end = time.perf_counter_ns()
                self.removes.append(end - start)
                return result

            StardewValleyWorld.remove = patched_remove

            @wraps(AutoWorld.call_single)
            def patched_call_single(self_, method_name: str, *args, **kwargs):
                start = time.perf_counter_ns()
                result = original_call_single(self_, method_name, *args, **kwargs)
                end = time.perf_counter_ns()
                self.gen_steps[method_name] = end - start
                return result

            AutoWorld.call_single = patched_call_single

            @wraps(CollectionState.sweep_for_advancements)
            def patched_sweep_for_advancements(self_, *args, **kwargs):
                start = time.perf_counter_ns()
                original_sweep_for_advancements(self_, *args, **kwargs)
                end = time.perf_counter_ns()
                self.sweep_for_advancements.append(end - start)

            CollectionState.sweep_for_advancements = patched_sweep_for_advancements

            @wraps(CollectionState.update_reachable_regions)
            def patched_update_reachable_regions(self_, *args, **kwargs):
                start = time.perf_counter_ns()
                original_update_reachable_regions(self_, *args, **kwargs)
                end = time.perf_counter_ns()
                self.update_reachable_regions.append(end - start)

            CollectionState.update_reachable_regions = patched_update_reachable_regions

        def run_one_generation(self) -> None:
            multiworld = setup_solo_multiworld(options, self.seed, _cache={})

            fill_start = time.perf_counter_ns()
            distribute_items_restrictive(multiworld)
            fill_end = time.perf_counter_ns()
            self.gen_steps['fill'] = fill_end - fill_start

            # print(explain(multiworld.get_location('Raccoon Request 5', 1).access_rule.delegate, multiworld.state, mode=ExplainMode.CLIENT))

        def print_results(self) -> None:
            sorted_by_duration = sorted(self.monitored_rules, key=lambda r: sum(call.duration_ns for call in r.calls), reverse=True)
            print(f"Top 10 slowest rules for run {self.index + 1} | seed [{self.seed}]:")
            for rule in sorted_by_duration[:10]:
                total_duration = sum(call.duration_ns for call in rule.calls)
                print(f"{rule.location}: {total_duration / 1_000_000:.2f} ms over {len(rule.calls)} calls")
            print(f"Total generation steps took {sum(step for step in self.gen_steps.values()) / 1_000_000_000:.2f} s.\n")

    run_count = 1
    runs = []

    def run_multiple_generations():
        nonlocal run_count
        for i in range(run_count):
            seed = get_seed(fixed_seed)
            print(f"Running generation {i + 1} with seed {seed}")
            run = Run(i, seed)
            run.apply_patches()
            gc.collect()
            try:
                run.run_one_generation()
            except FillError as e:
                print(e)
                run_count -= 1
                continue
            run.print_results()
            runs.append(run)

    def print_cumulative_results():
        grouped: dict[str, list[RuleCall]] = defaultdict(list)
        for run in runs:
            for rule in run.monitored_rules:
                for call in rule.calls:
                    grouped[rule.location].append(call)

        sorted_by_duration = sorted(grouped.items(), key=lambda item: sum(rule_call.duration_ns for rule_call in item[1]), reverse=True)
        print(f"\nCumulative results across all {run_count} runs:")
        for location, calls in sorted_by_duration[:10]:
            total_duration = sum(call.duration_ns for call in calls)
            avg_duration = total_duration / len(calls)
            print(f"{location}: {total_duration / 1_000_000:.2f} ms over {len(calls)} calls ({avg_duration / 1_000_000:.2f} ms on average)")

        sorted_by_avg_duration = sorted(
            grouped.items(),
            key=lambda item: sum(rule_call.duration_ns for rule_call in item[1]) / len(item[1]),
            reverse=True
        )
        print("\nTop 10 average durations across all runs:")
        for location, calls in sorted_by_avg_duration[:10]:
            total_duration = sum(call.duration_ns for call in calls)
            avg_duration = total_duration / len(calls)
            print(f"{location}: average {avg_duration / 1_000_000:.2f} ms over {len(calls)} calls ({total_duration / 1_000_000:.2f} ms total)")

        print("\nStats for collection state:")
        total_rules = sum(call.duration_ns for run in runs for rule in run.monitored_rules for call in rule.calls)
        print(f"Total evaluating rules: {total_rules / 1_000_000:.2f} ms across all runs")
        total_collects = sum(sum(run.collects) for run in runs)
        avg_collects = total_collects / sum(len(run.collects) for run in runs)
        print(f"Total collects: {total_collects / 1_000_000:.2f} ms, average per collect: {avg_collects / 1_000_000:.4f} ms")
        total_removes = sum(sum(run.removes) for run in runs)
        avg_removes = total_removes / sum(len(run.removes) for run in runs) if total_removes else 0
        print(f"Total removes: {total_removes / 1_000_000:.2f} ms, average per remove: {avg_removes / 1_000_000:.4f} ms")
        total_sweep = sum(sum(run.sweep_for_advancements) for run in runs)
        avg_sweep = total_sweep / sum(len(run.sweep_for_advancements) for run in runs) if total_sweep else 0
        print(f"Total sweep for advancements: {total_sweep / 1_000_000:.2f} ms, average per sweep: {avg_sweep / 1_000_000:.4f} ms")
        total_update_reachable = sum(sum(run.update_reachable_regions) for run in runs)
        avg_update_reachable = total_update_reachable / sum(len(run.update_reachable_regions) for run in runs) if total_update_reachable else 0
        print(f"Total update reachable regions: {total_update_reachable / 1_000_000:.2f} ms, average per update: {avg_update_reachable / 1_000_000:.4f} ms")

        print("\nGeneration steps:")
        for step in gen_steps + ('fill',):
            total_time = sum(run.gen_steps.get(step, 0) for run in runs)
            avg_time = total_time / run_count
            print(f"{step}: {total_time / 1_000_000:.2f} ms total, {avg_time / 1_000_000:.4f} ms average")

    run_multiple_generations()
    print_cumulative_results()


if __name__ == "__main__":
    generate_monitor_rules()
