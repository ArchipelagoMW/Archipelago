from .base_logic import BaseLogic
from ..stardew_rule import StardewRule, And, Or, Has, Count


class HasLogicMixin(BaseLogic[None]):
    # Should be cached
    def has(self, item: str) -> StardewRule:
        return Has(item, self.registry.item_rules)

    def has_all(self, *items: str):
        assert items, "Can't have all of no items."

        return And(*(self.has(item) for item in items))

    def has_any(self, *items: str):
        assert items, "Can't have any of no items."

        return Or(*(self.has(item) for item in items))

    def has_n(self, *items: str, count: int):
        return self.count(count, *(self.has(item) for item in items))

    @staticmethod
    def count(count: int, *rules: StardewRule) -> StardewRule:
        assert rules, "Can't create a Count conditions without rules"
        assert len(rules) >= count, "Count need at least as many rules as the count"

        if count == 1:
            return Or(*rules)

        if count == len(rules):
            return And(*rules)

        return Count(list(rules), count)
