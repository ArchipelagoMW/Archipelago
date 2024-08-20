from .base_logic import BaseLogic
from ..stardew_rule import StardewRule, And, Or, Has, Count, true_, false_


class HasLogicMixin(BaseLogic[None]):
    true_ = true_
    false_ = false_

    # Should be cached
    def has(self, item: str) -> StardewRule:
        return Has(item, self.registry.item_rules)

    def has_all(self, *items: str):
        assert items, "Can't have all of no items."

        return self.logic.and_(*(self.has(item) for item in items))

    def has_any(self, *items: str):
        assert items, "Can't have any of no items."

        return self.logic.or_(*(self.has(item) for item in items))

    def has_n(self, *items: str, count: int):
        return self.count(count, *(self.has(item) for item in items))

    @staticmethod
    def count(count: int, *rules: StardewRule) -> StardewRule:
        assert rules, "Can't create a Count conditions without rules"
        assert len(rules) >= count, "Count need at least as many rules as the count"
        assert count > 0, "Count can't be negative"

        count -= sum(r is true_ for r in rules)
        rules = list(r for r in rules if r is not true_)

        if count <= 0:
            return true_

        if len(rules) == 1:
            return rules[0]

        if count == 1:
            return Or(*rules)

        if count == len(rules):
            return And(*rules)

        return Count(rules, count)

    @staticmethod
    def and_(*rules: StardewRule) -> StardewRule:
        assert rules, "Can't create a And conditions without rules"

        if len(rules) == 1:
            return rules[0]

        return And(*rules)

    @staticmethod
    def or_(*rules: StardewRule) -> StardewRule:
        assert rules, "Can't create a Or conditions without rules"

        if len(rules) == 1:
            return rules[0]

        return Or(*rules)
