from typing import Iterable, Union, Optional

from .cached_logic import CachedLogic, cache_rule, CachedRules
from ..stardew_rule import StardewRule, True_, Received, And, Or, TotalReceived


class ReceivedLogic(CachedLogic):

    def __init__(self, player: int, cached_rules: CachedRules):
        super().__init__(player, cached_rules)

    def __call__(self, *args, **kwargs) -> StardewRule:
        count = 1
        if len(args) >= 2:
            count = args[1]
        return self.received(args[0], count)

    @cache_rule
    def received(self, items: Union[str, Iterable[str]], count: Optional[int] = 1) -> StardewRule:
        if count <= 0 or not items:
            return True_()

        if isinstance(items, str):
            return Received(items, self.player, count)

        if count is None:
            return And(self.received(item) for item in items)

        if count == 1:
            return Or(self.received(item) for item in items)

        return TotalReceived(count, items, self.player)

