from typing import Optional

from BaseClasses import ItemClassification
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from ..items import item_table
from ..stardew_rule import StardewRule, Received, TotalReceived
from ..strings.ap_names.event_names import all_events


class ReceivedLogicMixin(BaseLogic[HasLogicMixin], BaseLogicMixin):
    # Should be cached
    def received(self, item: str, count: Optional[int] = 1) -> StardewRule:
        assert count >= 0, "Can't receive a negative amount of item."
        assert item in all_events or item_table[item].classification & ItemClassification.progression, \
            f"Item [{item_table[item].name}] has to be progression to be used in logic"

        return Received(item, self.player, count)

    def received_all(self, *items: str):
        assert items, "Can't receive all of no items."

        return self.logic.and_(*(self.received(item) for item in items))

    def received_any(self, *items: str):
        assert items, "Can't receive any of no items."

        return self.logic.or_(*(self.received(item) for item in items))

    def received_once(self, *items: str, count: int):
        assert items, "Can't receive once of no items."
        assert count >= 0, "Can't receive a negative amount of item."

        return self.logic.count(count, *(self.received(item) for item in items))

    def received_n(self, *items: str, count: int):
        assert items, "Can't receive n of no items."
        assert count >= 0, "Can't receive a negative amount of item."

        return TotalReceived(count, items, self.player)
