import functools
import random
import time
from typing import Dict, Callable, Hashable, Iterable

from ..stardew_rule import StardewRule

rule_calls = 0
rule_creations = 0
time_creating_rules = 0


class CachedRules:
    cached_rules: Dict[Hashable, StardewRule]

    def __init__(self):
        self.cached_rules = dict()

    def try_get_rule(self, key: str, create_rule, *args, **kwargs) -> StardewRule:
        if key not in self.cached_rules:
            self.cached_rules[key] = create_rule(*args, **kwargs)
        return self.cached_rules[key]

    def try_get_rule_without_cache(self, key: Hashable, create_rule: Callable[[], StardewRule]) -> StardewRule:
        return create_rule()

    def try_get_rule_with_stats(self, key: Hashable, create_rule: Callable[[], StardewRule]) -> StardewRule:
        global rule_calls, rule_creations, time_creating_rules
        rule_calls += 1
        if key not in self.cached_rules:
            rule_creations += 1
            time_before = time.time()
            self.cached_rules[key] = create_rule()
            time_after = time.time()
            time_creating_rules += (time_after - time_before)
        if rule_calls % 100000 == 0:
            cached_calls = rule_calls - rule_creations
            percent_cached_calls = round((cached_calls / rule_calls) * 100)
            percent_real_calls = 100 - percent_cached_calls
            time_saved = (time_creating_rules / percent_real_calls) * 100
            print(
                f"Rule Creations/Calls: {rule_creations}/{rule_calls} ({cached_calls} cached calls [{percent_cached_calls}%] saving {time_saved}s"
                f" for a total of {time_creating_rules}s creating rules)")
        return self.cached_rules[key]


class CachedLogic:
    player: int
    cached_rules: CachedRules

    def __init__(self, player: int, cached_rules: CachedRules):
        self.player = player
        self.cached_rules = cached_rules
        self.name = type(self).__name__

    def get_cache_key(self, method: Callable, *parameters) -> Hashable:
        assert not any(isinstance(p, Iterable) for p in parameters)
        return self.name, method.__name__, str(parameters)
        # return f"{type(self).__name__} {method.__name__} {' '.join(map(str, parameters))}"


def cache_rule(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = self.get_cache_key(func, *args, **kwargs)
        return self.cached_rules.try_get_rule(key, func, self, *args, **kwargs)
    return wrapper


time_getting_keys = 0
time_getting_rules = 0


def cache_rule_with_profiling(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        global time_getting_keys, time_getting_rules
        time_before_key = time.time()
        key = self.get_cache_key(func, *args)
        time_between = time.time()
        rule = self.cached_rules.try_get_rule(key, lambda: func(self, *args, **kwargs))
        time_after_rule = time.time()
        time_getting_keys += (time_between - time_before_key)
        time_getting_rules += (time_after_rule - time_between)
        if random.random() < 0.0001:
            print(f"Time Getting Keys: {time_getting_keys} seconds")
            print(f"Time Getting Rules: {time_getting_rules} seconds")
        return rule

    return wrapper


function_call_numbers = dict()
function_total_times = dict()


def profile_rule(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = f"{self.__class__.__name__} {func.__name__}"
        key_params = f"{self.__class__.__name__} {func.__name__} {args}"

        if key not in function_call_numbers:
            function_call_numbers[key] = 0
        if key_params not in function_call_numbers:
            function_call_numbers[key_params] = 0
        if key not in function_total_times:
            function_total_times[key] = 0
        if key_params not in function_total_times:
            function_total_times[key_params] = 0

        time_before = time.time()
        result = func(self, *args, **kwargs)
        time_after = time.time()
        time_used = time_after - time_before

        function_call_numbers[key] += 1
        function_call_numbers[key_params] += 1
        function_total_times[key] += time_used
        function_total_times[key_params] += time_used

        return result

    return wrapper
