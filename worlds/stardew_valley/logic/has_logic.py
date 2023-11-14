from functools import lru_cache
from typing import Dict, Union, Optional, Tuple

from .cached_logic import CachedLogic, CachedRules
from ..stardew_rule import StardewRule, True_, And, Or, Has, Count


class HasLogic(CachedLogic):
    item_rules: Dict[str, StardewRule]

    def __init__(self, player: int, cached_rules: CachedRules, item_rules: Dict[str, StardewRule]):
        super().__init__(player, cached_rules)
        self.item_rules = item_rules

    def __call__(self, *args, **kwargs) -> StardewRule:
        count = None
        if len(args) >= 2:
            count = args[1]
        return self.has(args[0], count)

    @lru_cache(maxsize=None)
    def has(self, items: Union[str, Tuple[str]], count: Optional[int] = None) -> StardewRule:
        if isinstance(items, str):
            return Has(items, self.item_rules)

        if len(items) == 0:
            return True_()

        if count is None or count == len(items):
            return And(self.has(item) for item in items)

        if count == 1:
            return Or(self.has(item) for item in items)

        return Count(count, (self.has(item) for item in items))
