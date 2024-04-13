from typing import Optional

from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from ..stardew_rule import StardewRule, Received, And, Or, TotalReceived


class ReceivedLogicMixin(BaseLogic[HasLogicMixin], BaseLogicMixin):
    # Should be cached
    def received(self, item: str, count: Optional[int] = 1) -> StardewRule:
        assert count >= 0, "Can't receive a negative amount of item."

        return Received(item, self.player, count)

    def received_all(self, *items: str):
        assert items, "Can't receive all of no items."

        return And(*(self.received(item) for item in items))

    def received_any(self, *items: str):
        assert items, "Can't receive any of no items."

        return Or(*(self.received(item) for item in items))

    def received_once(self, *items: str, count: int):
        assert items, "Can't receive once of no items."
        assert count >= 0, "Can't receive a negative amount of item."

        return self.logic.count(count, *(self.received(item) for item in items))

    def received_n(self, *items: str, count: int):
        assert items, "Can't receive n of no items."
        assert count >= 0, "Can't receive a negative amount of item."

        return TotalReceived(count, items, self.player)
