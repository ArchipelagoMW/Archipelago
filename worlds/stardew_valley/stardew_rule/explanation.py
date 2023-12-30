from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterable, Protocol, runtime_checkable

from BaseClasses import CollectionState

max_explanation_depth = 10


@runtime_checkable
class ExplainableRule(Protocol):

    @abstractmethod
    def __call__(self, state: CollectionState) -> bool:
        ...

    def explain(self, state: CollectionState, expected=True) -> RuleExplanation:
        return RuleExplanation(self, state, expected)


@dataclass
class RuleExplanation:
    rule: ExplainableRule
    state: CollectionState
    expected: bool
    sub_rules: Iterable[ExplainableRule] = field(default_factory=list)

    def summary(self, depth=0):
        return "  " * depth + f"{str(self.rule)} -> {self.result}"

    def __str__(self, depth=0):
        if not self.sub_rules or depth >= max_explanation_depth:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(RuleExplanation.__str__(i, depth + 1)
                                                      if i.result is not self.expected else i.summary(depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    def __repr__(self, depth=0):
        if not self.sub_rules or depth >= max_explanation_depth:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(RuleExplanation.__repr__(i, depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    @cached_property
    def result(self):
        return self.rule(self.state)

    @cached_property
    def explained_sub_rules(self):
        return [i.explain(self.state) for i in self.sub_rules]
