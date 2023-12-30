from typing import Union, Optional, Tuple

from .base_logic import BaseLogic
from ..stardew_rule import StardewRule, True_, And, Or, Has, Count


class HasLogicMixin(BaseLogic[None]):
    # Should be cached
    def has(self, items: Union[str, Tuple[str, ...]], count: Optional[int] = None) -> StardewRule:
        if isinstance(items, str):
            return Has(items, self.registry.item_rules)

        if len(items) == 0:
            return True_()

        if count is None or count == len(items):
            return And(*(self.has(item) for item in items))

        if count == 1:
            return Or(*(self.has(item) for item in items))

        return self.count(count, *(self.has(item) for item in items))

    @staticmethod
    def count(count: int, *rules: StardewRule) -> StardewRule:
        assert rules, "Can't create a Count conditions without rules"
        assert len(rules) >= count, "Count need at least as many rules at the count"

        return Count(list(rules), count)
