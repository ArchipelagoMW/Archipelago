import time
from typing import Dict, Callable

from ..stardew_rule import StardewRule

rule_calls = 0
rule_creations = 0
time_creating_rules = 0


class CachedRules:
    cached_rules: Dict[str, StardewRule]

    def __init__(self):
        self.cached_rules = dict()

    def try_get_rule(self, key: str, create_rule: Callable[[], StardewRule]) -> StardewRule:
        if key not in self.cached_rules:
            self.cached_rules[key] = create_rule()
        return self.cached_rules[key]

    def try_get_rule_without_cache(self, key: str, create_rule: Callable[[], StardewRule]) -> StardewRule:
        return create_rule()

    def try_get_rule_with_stats(self, key: str, create_rule: Callable[[], StardewRule]) -> StardewRule:
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
            print(f"Rule Creations/Calls: {rule_creations}/{rule_calls} ({cached_calls} cached calls [{percent_cached_calls}%] saving {time_saved}s"
                  f" for a total of {time_creating_rules}s creating rules)")
        return self.cached_rules[key]
