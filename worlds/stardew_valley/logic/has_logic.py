from typing import Dict, Union, Optional, Iterable, Sized, List

from ..stardew_rule import StardewRule, True_, And, Or, Has, Count


class HasLogic:
    player: int
    item_rules: Dict[str, StardewRule]

    def __init__(self, player: int, item_rules: Dict[str, StardewRule]):
        self.player = player
        self.item_rules = item_rules

    def __call__(self, *args, **kwargs) -> StardewRule:
        count = None
        if len(args) >= 2:
            count = args[1]
        return self.has(args[0], count)

    def has(self, items: Union[str, List[str]], count: Optional[int] = None) -> StardewRule:
        if isinstance(items, str):
            return Has(items, self.item_rules)

        if len(items) == 0:
            return True_()

        if count is None or count == len(items):
            return And(self.has(item) for item in items)

        if count == 1:
            return Or(self.has(item) for item in items)

        return Count(count, (self.has(item) for item in items))

