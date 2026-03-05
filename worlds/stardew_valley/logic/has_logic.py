from .base_logic import BaseLogic
from ..stardew_rule import StardewRule, And, Or, Has, Count, true_, false_, HasProgressionPercent


class HasLogicMixin(BaseLogic):
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

    def has_progress_percent(self, percent: int):
        assert percent >= 0, "Can't have a negative progress percent"
        assert percent <= 100, "Can't have a progress percent over 100"

        return HasProgressionPercent(self.player, percent)

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
    def and_(*rules: StardewRule, allow_empty: bool = False) -> StardewRule:
        """
        :param rules: The rules to combine
        :param allow_empty: If True, return true_ when no rules are given. Otherwise, raise an error.
        """
        if not rules:
            assert allow_empty, "Can't create a And conditions without rules"
            return true_

        if len(rules) == 1:
            return rules[0]

        return And(*rules)

    @staticmethod
    def or_(*rules: StardewRule, allow_empty: bool = False) -> StardewRule:
        """
          :param rules: The rules to combine
          :param allow_empty: If True, return false_ when no rules are given. Otherwise, raise an error.
          """
        if not rules:
            assert allow_empty, "Can't create a Or conditions without rules"
            return false_

        if len(rules) == 1:
            return rules[0]

        return Or(*rules)
