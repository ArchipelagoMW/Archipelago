from typing import Optional

from BaseClasses import ItemClassification
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .logic_event import all_events
from ..items import item_table
from ..stardew_rule import StardewRule, Received, TotalReceived


class ReceivedLogicMixin(BaseLogic[HasLogicMixin], BaseLogicMixin):
    def received(self, item: str, count: Optional[int] = 1) -> StardewRule:
        assert count >= 0, "Can't receive a negative amount of item."

        if item in all_events:
            return Received(item, self.player, count, event=True)

        assert item_table[item].classification & ItemClassification.progression, f"Item [{item_table[item].name}] has to be progression to be used in logic"
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

        for item in items:
            assert item_table[item].classification & ItemClassification.progression, f"Item [{item_table[item].name}] has to be progression to be used in logic"

        return TotalReceived(count, items, self.player)
