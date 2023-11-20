from typing import Union, Optional, Tuple

from .base_logic import BaseLogic
from ..stardew_rule import StardewRule, True_, And, Or, Has, Count


class HasLogicMixin(BaseLogic):
    def __call__(self, *args, **kwargs) -> StardewRule:
        count = None
        if len(args) >= 2:
            count = args[1]
        return self.has(args[0], count)

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

        return Count(count, (self.has(item) for item in items))
