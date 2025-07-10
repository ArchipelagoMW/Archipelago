from abc import ABC
from typing import Tuple

from BaseClasses import CollectionState
from .protocol import StardewRule


class LiteralStardewRule(StardewRule, ABC):
    value: bool

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self.value

    def __call__(self, state: CollectionState) -> bool:
        return self.value

    def __repr__(self):
        return str(self.value)


class True_(LiteralStardewRule):  # noqa
    value = True

    def __new__(cls, _cache=[]):  # noqa
        # Only one single instance will be ever created.
        if not _cache:
            _cache.append(super(True_, cls).__new__(cls))
        return _cache[0]

    def __or__(self, other) -> StardewRule:
        return self

    def __and__(self, other) -> StardewRule:
        return other


class False_(LiteralStardewRule):  # noqa
    value = False

    def __new__(cls, _cache=[]):  # noqa
        # Only one single instance will be ever created.
        if not _cache:
            _cache.append(super(False_, cls).__new__(cls))
        return _cache[0]

    def __or__(self, other) -> StardewRule:
        return other

    def __and__(self, other) -> StardewRule:
        return self


false_ = False_()
true_ = True_()
assert false_
assert true_
