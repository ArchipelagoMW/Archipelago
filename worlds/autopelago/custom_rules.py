import dataclasses
from collections.abc import Iterable, Mapping
from typing import Any, Self

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, True_, TWorld
from worlds.AutoWorld import World

from .items import item_name_to_rat_count
from .util import GAME_NAME

VARIABLE_NUMBER_COLOR = "cyan"
SATISFIED_COLOR = "green"
UNSATISFIED_COLOR = "salmon"


@dataclasses.dataclass(init=False)
class HasRatCount(Rule[TWorld], game=GAME_NAME):
    rat_count: int

    def __init__(
        self,
        rat_count: int,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.rat_count = rat_count

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if self.rat_count == 0:
            return True_().resolve(world)

        return HasRatCount.Resolved(
            self.rat_count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.rat_count}{options})"

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data["args"]
        data["rat_count"] = self.rat_count
        return data

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        rat_count = data.get("rat_count")
        if not isinstance(rat_count, int):
            raise ValueError("Missing 'rat_count' in HasRatCount rule")
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(rat_count, options=options, filtered_resolution=data.get("filtered_resolution", False))

    class Resolved(Rule.Resolved):
        rat_count: int = 2

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            remaining = self.rat_count
            for item_name, rat_count_per_item in item_name_to_rat_count.items():
                item_count = state.count(item_name, self.player)
                if item_count == 0:
                    continue
                remaining -= item_count * rat_count_per_item
                if remaining <= 0:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            my_id = id(self)
            return {item_name: {my_id} for item_name in item_name_to_rat_count}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            has_or_missing: str
            satisfied_or_unsatisfied_color: str | None
            if state:
                if self(state):
                    has_or_missing = "Has "
                    satisfied_or_unsatisfied_color = SATISFIED_COLOR
                else:
                    has_or_missing = "Missing "
                    satisfied_or_unsatisfied_color = UNSATISFIED_COLOR
            else:
                has_or_missing = "Has "
                satisfied_or_unsatisfied_color = None

            messages: list[JSONMessagePart] = [
                {"type": "text", "text": has_or_missing},
                {"type": "color", "color": VARIABLE_NUMBER_COLOR, "text": str(self.rat_count)},
            ]
            if satisfied_or_unsatisfied_color:
                messages.append({"type": "color", "color": satisfied_or_unsatisfied_color, "text": "rats"})
            else:
                messages.append({"type": "text", "text": "rats"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            return str(self) if state is None or self(state) else \
                f"Missing {self.rat_count} rats"

        @override
        def __str__(self) -> str:
            return f"Has {self.rat_count} rats"
