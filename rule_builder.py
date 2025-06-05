import dataclasses
import itertools
import operator
from collections import defaultdict
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Self

from worlds.AutoWorld import World

if TYPE_CHECKING:
    from BaseClasses import CollectionState, Entrance, Item, MultiWorld
    from NetUtils import JSONMessagePart
    from Options import CommonOptions, Option

OPERATORS = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "contains": operator.contains,
}


@dataclasses.dataclass()
class Rule:
    """Base class for a static rule used to generate a"""

    options: dict[str, Any] = dataclasses.field(default_factory=dict, kw_only=True)
    """A mapping of option_name to value to restrict what options are required for this rule to be active.
    An operator can be specified with a double underscore and the operator after the option name, eg `opt__le`
    """

    def _passes_options(self, options: "CommonOptions") -> bool:
        """Tests if the given world options pass the requirements for this rule"""
        for key, value in self.options:
            parts = key.split("__", maxsplit=1)
            option_name = parts[0]
            operator = parts[1] if len(parts) > 1 else "eq"
            opt: Option[Any] = getattr(options, option_name)
            if not OPERATORS[operator](opt.value, value):
                return False
        return True

    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        """Create a new resolved rule for this world"""
        return self.Resolved(player=world.player)

    def resolve(self, world: "RuleWorldMixin") -> "Resolved":
        """Resolve a rule with the given world"""
        if not self._passes_options(world.options):
            return False_.Resolved(player=world.player)

        instance = self._instantiate(world)
        rule_hash = hash(instance)
        if rule_hash not in world.rule_ids:
            world.rule_ids[rule_hash] = instance
        return world.rule_ids[rule_hash]

    def to_json(self) -> Any:
        """Returns a JSON-serializable definition of this rule"""
        return {
            "rule": self.__class__.__name__,
            "args": {field.name: getattr(self, field.name, None) for field in dataclasses.fields(self)},
        }

    @classmethod
    def from_json(cls, data: Any) -> Self:
        if not isinstance(data, Mapping):
            raise ValueError("Invalid data format for parsed json")
        return cls(**data.get("args", {}))

    @dataclasses.dataclass(kw_only=True, frozen=True)
    class Resolved:
        """A resolved rule for a given world that can be used as an access rule"""

        player: int
        """The player this rule is for"""

        cacheable: bool = dataclasses.field(repr=False, default=True)
        """If this rule should be cached in the state"""

        always_true: ClassVar = False
        """Whether this rule always evaluates to True, used to short-circuit logic"""

        always_false: ClassVar = False
        """Whether this rule always evaluates to True, used to short-circuit logic"""

        def __hash__(self) -> int:
            return hash((self.__class__.__name__, *[getattr(self, f.name) for f in dataclasses.fields(self)]))

        def _evaluate(self, state: "CollectionState") -> bool:
            """Calculate this rule's result with the given state"""
            ...

        def evaluate(self, state: "CollectionState") -> bool:
            """Evaluate this rule's result with the given state and cache the result if applicable"""
            result = self._evaluate(state)
            if self.cacheable:
                state.rule_cache[self.player][id(self)] = result
            return result

        def test(self, state: "CollectionState") -> bool:
            """Evaluate this rule's result with the given state, using the cached value if possible"""
            cached_result = None
            if self.cacheable:
                cached_result = state.rule_cache[self.player].get(id(self))
            if cached_result is not None:
                return cached_result
            return self.evaluate(state)

        def item_dependencies(self) -> dict[str, set[int]]:
            """Returns a mapping of item name to set of object ids to be used for cache invalidation"""
            return {}

        def indirect_regions(self) -> tuple[str, ...]:
            """Returns a tuple of region names this rule is indirectly connected to"""
            return ()

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [{"type": "text", "text": self.__class__.__name__}]


@dataclasses.dataclass()
class True_(Rule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)
        always_true = True

        def _evaluate(self, state: "CollectionState") -> bool:
            return True

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [{"type": "color", "color": "green", "text": "True"}]


@dataclasses.dataclass()
class False_(Rule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)
        always_false = True

        def _evaluate(self, state: "CollectionState") -> bool:
            return False

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [{"type": "color", "color": "salmon", "text": "False"}]


@dataclasses.dataclass(init=False)
class NestedRule(Rule):
    children: "tuple[Rule, ...]"

    def __init__(self, *children: "Rule", options: dict[str, Any] | None = None) -> None:
        super().__init__(options=options or {})
        self.children = children

    def _instantiate(self, world: "RuleWorldMixin") -> "Rule.Resolved":
        children = [c.resolve(world) for c in self.children]
        return self.Resolved(tuple(children), player=world.player).simplify()

    def to_json(self) -> Any:
        return {
            "rule": self.__class__.__name__,
            "options": self.options,
            "children": [c.to_json() for c in self.children],
        }

    @classmethod
    def from_json(cls, data: Any) -> Self:
        if not isinstance(data, Mapping):
            raise ValueError("Invalid data format for parsed json")
        return cls(*data.get("children", []), options=data.get("options"))

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        children: "tuple[Rule.Resolved, ...]"

        def item_dependencies(self) -> dict[str, set[int]]:
            combined_deps: dict[str, set[int]] = {}
            for child in self.children:
                for item_name, rules in child.item_dependencies().items():
                    if item_name in combined_deps:
                        combined_deps[item_name] |= rules
                    else:
                        combined_deps[item_name] = {id(self), *rules}
            return combined_deps

        def indirect_regions(self) -> tuple[str, ...]:
            return tuple(itertools.chain.from_iterable(child.indirect_regions() for child in self.children))

        def simplify(self) -> "Rule.Resolved":
            return self


@dataclasses.dataclass(init=False)
class And(NestedRule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(NestedRule.Resolved):
        def _evaluate(self, state: "CollectionState") -> bool:
            for rule in self.children:
                if not rule.test(state):
                    return False
            return True

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " & "})
                messages.extend(child.explain(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        def simplify(self) -> "Rule.Resolved":
            children_to_process = list(self.children)
            clauses: list[Rule.Resolved] = []
            items: set[str] = set()
            true_rule: Rule.Resolved | None = None

            while children_to_process:
                child = children_to_process.pop(0)
                if child.always_false:
                    # false always wins
                    return child
                if child.always_true:
                    # dedupe trues
                    true_rule = child
                    continue
                if isinstance(child, And.Resolved):
                    children_to_process.extend(child.children)
                    continue

                if isinstance(child, Has.Resolved) and child.count == 1:
                    items.add(child.item_name)
                elif isinstance(child, HasAll.Resolved):
                    items.update(child.item_names)
                else:
                    clauses.append(child)

            if not clauses and not items:
                return true_rule or False_.Resolved(player=self.player)
            if items:
                if len(items) == 1:
                    item_rule = Has.Resolved(items.pop(), player=self.player)
                else:
                    item_rule = HasAll.Resolved(tuple(items), player=self.player)
                if not clauses:
                    return item_rule
                clauses.append(item_rule)

            if len(clauses) == 1:
                return clauses[0]
            return And.Resolved(
                tuple(clauses),
                player=self.player,
                cacheable=self.cacheable and all(c.cacheable for c in clauses),
            )


@dataclasses.dataclass(init=False)
class Or(NestedRule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(NestedRule.Resolved):
        def _evaluate(self, state: "CollectionState") -> bool:
            for rule in self.children:
                if rule.test(state):
                    return True
            return False

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " | "})
                messages.extend(child.explain(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        def simplify(self) -> "Rule.Resolved":
            children_to_process = list(self.children)
            clauses: list[Rule.Resolved] = []
            items: set[str] = set()

            while children_to_process:
                child = children_to_process.pop(0)
                if child.always_true:
                    # true always wins
                    return child
                if child.always_false:
                    # falses can be ignored
                    continue
                if isinstance(child, Or.Resolved):
                    children_to_process.extend(child.children)
                    continue

                if isinstance(child, Has.Resolved) and child.count == 1:
                    items.add(child.item_name)
                elif isinstance(child, HasAny.Resolved):
                    items.update(child.item_names)
                else:
                    clauses.append(child)

            if not clauses and not items:
                return False_.Resolved(player=self.player)
            if items:
                if len(items) == 1:
                    item_rule = Has.Resolved(items.pop(), player=self.player)
                else:
                    item_rule = HasAny.Resolved(tuple(items), player=self.player)
                if not clauses:
                    return item_rule
                clauses.append(item_rule)

            if len(clauses) == 1:
                return clauses[0]
            return Or.Resolved(
                tuple(clauses),
                player=self.player,
                cacheable=self.cacheable and all(c.cacheable for c in clauses),
            )


@dataclasses.dataclass()
class Has(Rule):
    item_name: str
    count: int = 1

    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(self.item_name, self.count, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_name: str
        count: int = 1

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has(self.item_name, self.player, count=self.count)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: {id(self)}}

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [{"type": "text", "text": "Has "}]
            if self.count > 1:
                messages.append({"type": "color", "color": "cyan", "text": str(self.count)})
                messages.append({"type": "text", "text": "x "})
            messages.append(
                {"type": "item_name", "flags": 0b001, "text": self.item_name, "player": self.player}
            )
            return messages


@dataclasses.dataclass(init=False)
class HasAll(Rule):
    """A rule that checks if the player has all of the given items"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    def __init__(self, *item_names: str, options: dict[str, Any] | None = None) -> None:
        super().__init__(options=options or {})
        self.item_names = item_names

    def _instantiate(self, world: "RuleWorldMixin") -> "Rule.Resolved":
        if len(self.item_names) == 0:
            return True_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(self.item_names, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has_all(self.item_names, self.player)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [
                {"type": "text", "text": "Has "},
                {"type": "color", "color": "cyan", "text": "all"},
                {"type": "text", "text": " of ("},
            ]
            for i, item in enumerate(self.item_names):
                if i > 0:
                    messages.append({"type": "text", "text": ", "})
                messages.append({"type": "item_name", "flags": 0b001, "text": item, "player": self.player})
            messages.append({"type": "text", "text": ")"})
            return messages


@dataclasses.dataclass()
class HasAny(Rule):
    """A rule that checks if the player has at least one of the given items"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    def __init__(self, *item_names: str, options: dict[str, Any] | None = None) -> None:
        super().__init__(options=options or {})
        self.item_names = item_names

    def _instantiate(self, world: "RuleWorldMixin") -> "Rule.Resolved":
        if len(self.item_names) == 0:
            return True_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(self.item_names, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has_any(self.item_names, self.player)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [
                {"type": "text", "text": "Has "},
                {"type": "color", "color": "cyan", "text": "any"},
                {"type": "text", "text": " of ("},
            ]
            for i, item in enumerate(self.item_names):
                if i > 0:
                    messages.append({"type": "text", "text": ", "})
                messages.append({"type": "item_name", "flags": 0b001, "text": item, "player": self.player})
            messages.append({"type": "text", "text": ")"})
            return messages


@dataclasses.dataclass()
class CanReachLocation(Rule):
    location_name: str

    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        location = world.get_location(self.location_name)
        if not location.parent_region:
            raise ValueError(f"Location {location.name} has no parent region")
        return self.Resolved(self.location_name, location.parent_region.name, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        location_name: str
        parent_region_name: str
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.can_reach_location(self.location_name, self.player)

        def indirect_regions(self) -> tuple[str, ...]:
            return (self.parent_region_name,)

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "Reached Location "},
                {"type": "location_name", "text": self.location_name, "player": self.player},
            ]


@dataclasses.dataclass()
class CanReachRegion(Rule):
    region_name: str

    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(self.region_name, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        region_name: str
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.can_reach_region(self.region_name, self.player)

        def indirect_regions(self) -> tuple[str, ...]:
            return (self.region_name,)

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "Reached Region "},
                {"type": "color", "color": "yellow", "text": self.region_name},
            ]


@dataclasses.dataclass()
class CanReachEntrance(Rule):
    entrance_name: str

    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(self.entrance_name, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        entrance_name: str
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.can_reach_entrance(self.entrance_name, self.player)

        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "Reached Entrance "},
                {"type": "entrance_name", "text": self.entrance_name, "player": self.player},
            ]


class RuleWorldMixin(World if TYPE_CHECKING else object):
    rule_ids: dict[int, Rule.Resolved]
    rule_dependencies: dict[str, set[int]]

    custom_rule_classes: ClassVar[dict[str, type[Rule]]]

    def __init__(self, multiworld: "MultiWorld", player: int) -> None:
        super().__init__(multiworld, player)
        self.rule_ids = {}
        self.rule_dependencies = defaultdict(set)

    @classmethod
    def rule_from_json(cls, data: Any) -> "Rule":
        if not isinstance(data, Mapping):
            raise ValueError("Invalid data format for parsed json")
        name = data.get("rule", "")
        if name not in DEFAULT_RULES and (
            not getattr(cls, "custom_rule_classes", None) or name not in cls.custom_rule_classes
        ):
            raise ValueError("Rule not found")
        rule_class = DEFAULT_RULES.get(name) or cls.custom_rule_classes[name]
        if not issubclass(rule_class, Rule):
            raise ValueError("Invalid rule")
        return rule_class.from_json(data)

    def resolve_rule(self, rule: "Rule") -> "Rule.Resolved":
        resolved_rule = rule.resolve(self)
        for item_name, rule_ids in resolved_rule.item_dependencies().items():
            self.rule_dependencies[item_name] |= rule_ids
        return resolved_rule

    def register_rule_connections(self, resolved_rule: "Rule.Resolved", entrance: "Entrance") -> None:
        for indirect_region in resolved_rule.indirect_regions():
            self.multiworld.register_indirect_condition(self.get_region(indirect_region), entrance)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        changed = super().collect(state, item)
        if changed and getattr(self, "rule_dependencies", None):
            player_results: dict[int, bool] = state.rule_cache[self.player]
            for rule_id in self.rule_dependencies[item.name]:
                player_results.pop(rule_id, None)
        return changed

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        changed = super().remove(state, item)
        if changed and getattr(self, "rule_dependencies", None):
            player_results: dict[int, bool] = state.rule_cache[self.player]
            for rule_id in self.rule_dependencies[item.name]:
                player_results.pop(rule_id, None)
        return changed


DEFAULT_RULES = {
    rule_name: rule_class
    for rule_name, rule_class in locals().items()
    if isinstance(rule_class, type) and issubclass(rule_class, Rule) and rule_class is not Rule
}
