from typing import Union, Optional, Tuple

from .base_logic import BaseLogic, BaseLogicMixin
from ..stardew_rule import StardewRule, True_, Received, And, Or, TotalReceived


class ReceivedLogicMixin(BaseLogic[None], BaseLogicMixin):
    # Should be cached
    def received(self, items: Union[str, Tuple[str, ...]], count: Optional[int] = 1) -> StardewRule:
        if count <= 0 or not items:
            return True_()

        if isinstance(items, str):
            return Received(items, self.player, count)

        if count is None:
            return And(*(self.received(item) for item in items))

        if count == 1:
            return Or(*(self.received(item) for item in items))

        return TotalReceived(count, items, self.player)
