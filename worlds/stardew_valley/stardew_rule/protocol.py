from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Tuple, runtime_checkable

from BaseClasses import CollectionState


@runtime_checkable
class StardewRule(Protocol):

    @abstractmethod
    def __call__(self, state: CollectionState) -> bool:
        ...

    @abstractmethod
    def __and__(self, other: StardewRule):
        ...

    @abstractmethod
    def __or__(self, other: StardewRule):
        ...

    @abstractmethod
    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        ...
