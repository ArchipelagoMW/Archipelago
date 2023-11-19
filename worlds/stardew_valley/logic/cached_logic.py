from typing import Dict, Hashable

from ..stardew_rule import StardewRule


class CachedRules:
    cached_rules: Dict[Hashable, StardewRule]

    def __init__(self):
        self.cached_rules = dict()


class CachedLogic:
    player: int
    cached_rules: CachedRules

    def __init__(self, player: int, cached_rules: CachedRules):
        self.player = player
        self.cached_rules = cached_rules
        self.name = type(self).__name__
