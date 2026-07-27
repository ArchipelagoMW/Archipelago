import dataclasses
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any, Self

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from rule_builder.rules import NestedRule, Rule, True_

if TYPE_CHECKING:
    from .. import KH1World


@dataclasses.dataclass()
class HasCappedSum(Rule["KH1World"], game="Kingdom Hearts"):
    
    item_caps: Mapping[str, int]
    threshold: int

    @override
    def _instantiate(self, world: "KH1World") -> Rule.Resolved:
        return self.Resolved(
            tuple(self.item_caps.items()),
            self.threshold,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        item_caps: tuple[tuple[str, int], ...]
        threshold: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            player_prog_items = state.prog_items[self.player]
            total = sum(min(player_prog_items[item], cap) for item, cap in self.item_caps)
            return total >= self.threshold

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item, _ in self.item_caps}

        @override
        def __str__(self) -> str:
            items = ", ".join(f"{item} (max {cap})" for item, cap in self.item_caps)
            return f"Has {self.threshold} from capped sum of ({items})"


@dataclasses.dataclass(init=False)
class AtLeast(NestedRule["KH1World"], game="Kingdom Hearts"):

    count: int

    def __init__(
        self,
        count: int,
        *children: Rule["KH1World"],
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(*children, options=options, filtered_resolution=filtered_resolution)
        self.count = count

    @override
    def _instantiate(self, world: "KH1World") -> Rule.Resolved:
        if self.count <= 0:
            return True_().resolve(world)
        children = [c.resolve(world) for c in self.children]
        return self.Resolved(
            tuple(children),
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def to_dict(self) -> dict[str, Any]:
        output = super().to_dict()
        output["count"] = self.count
        return output

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[KH1World]") -> Self:
        children = [world_cls.rule_from_dict(c) for c in data.get("children", ())]
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(
            data["count"],
            *children,
            options=options,
            filtered_resolution=data.get("filtered_resolution", False),
        )

    class Resolved(NestedRule.Resolved):
        count: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            count = self.count
            for rule in self.children:
                if rule(state):
                    if count == 1:
                        return True
                    count -= 1
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                messages: list[JSONMessagePart] = [
                    {"type": "text", "text": "At least "},
                    {"type": "color", "color": "cyan", "text": str(self.count)},
                    {"type": "text", "text": " of ("},
                ]
            else:
                satisfied_count = sum(1 if child(state) else 0 for child in self.children)
                messages = [
                    {"type": "text", "text": "At least "},
                    {"type": "color", "color": "cyan", "text": f"{satisfied_count}/{self.count}"},
                    {"type": "text", "text": " of ("},
                ]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": ", "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = ", ".join(c.explain_str(state) for c in self.children)
            if state is None:
                return f"At least {self.count} of ({clauses})"
            satisfied_count = sum(1 if child(state) else 0 for child in self.children)
            return f"At least {satisfied_count}/{self.count} of ({clauses})"

        @override
        def __str__(self) -> str:
            clauses = ", ".join(str(c) for c in self.children)
            return f"At least {self.count} of ({clauses})"
