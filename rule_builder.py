import dataclasses
import itertools
import operator
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Literal, TypeVar, cast

from typing_extensions import Never, Self, override

from BaseClasses import Entrance

if TYPE_CHECKING:
    from BaseClasses import CollectionState, Item, Location, MultiWorld
    from NetUtils import JSONMessagePart
    from Options import CommonOptions, Option
    from worlds.AutoWorld import World
else:
    World = object

Operator = Literal["eq", "ne", "gt", "lt", "ge", "le", "contains"]

OPERATORS = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "contains": operator.contains,
}

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class OptionFilter(Generic[T]):
    option: "type[Option[T]]"
    value: T
    operator: Operator = "eq"


@dataclasses.dataclass()
class Rule:
    """Base class for a static rule used to generate an access rule"""

    options: "Iterable[OptionFilter[Any]]" = dataclasses.field(default=(), kw_only=True)
    """An iterable of OptionFilters to restrict what options are required for this rule to be active"""

    def _passes_options(self, options: "CommonOptions") -> bool:
        """Tests if the given world options pass the requirements for this rule"""
        for option_filter in self.options:
            option_name = next(
                (name for name, cls in options.__class__.type_hints.items() if cls is option_filter.option),
                None,
            )
            if option_name is None:
                raise ValueError(f"Cannot find option: {option_filter.option.__name__}")
            opt = cast("Option[Any] | None", getattr(options, option_name, None))
            if opt is None:
                raise ValueError(f"Invalid option: {option_name}")

            if not OPERATORS[option_filter.operator](opt.value, option_filter.value):
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

    def to_json(self) -> Mapping[str, Any]:
        """Returns a JSON-serializable definition of this rule"""
        args = {
            field.name: getattr(self, field.name, None) for field in dataclasses.fields(self) if field.name != "options"
        }
        args["options"] = [dataclasses.asdict(o) for o in self.options]
        return {
            "rule": self.__class__.__name__,
            "args": args,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Self:
        return cls(**data.get("args", {}))

    def __and__(self, other: "Rule") -> "Rule":
        """Combines two rules into an And rule"""
        if isinstance(self, And):
            if isinstance(other, And):
                if self.options == other.options:
                    return And(*self.children, *other.children, options=self.options)
            else:
                return And(*self.children, other, options=self.options)
        elif isinstance(other, And):
            return And(self, *other.children, options=other.options)
        return And(self, other)

    def __or__(self, other: "Rule") -> "Rule":
        """Combines two rules into an Or rule"""
        if isinstance(self, Or):
            if isinstance(other, Or):
                if self.options == other.options:
                    return Or(*self.children, *other.children, options=self.options)
            else:
                return Or(*self.children, other, options=self.options)
        elif isinstance(other, Or):
            return Or(self, *other.children, options=other.options)
        return Or(self, other)

    def __bool__(self) -> Never:
        raise TypeError("Use & or | to combine rules, or use `is not None` for boolean tests")

    @override
    def __str__(self) -> str:
        options = f"options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({options})"

    @dataclasses.dataclass(kw_only=True, frozen=True)
    class Resolved:
        """A resolved rule for a given world that can be used as an access rule"""

        player: int
        """The player this rule is for"""

        cacheable: bool = dataclasses.field(repr=False, default=True)
        """If this rule should be cached in the state"""

        always_true: ClassVar[bool] = False
        """Whether this rule always evaluates to True, used to short-circuit logic"""

        always_false: ClassVar[bool] = False
        """Whether this rule always evaluates to True, used to short-circuit logic"""

        @override
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
            """Returns a list of printJSON messages that explain the logic for this rule"""
            return [{"type": "text", "text": self.__class__.__name__}]


@dataclasses.dataclass()
class True_(Rule):
    """A rule that always returns True"""

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)
        always_true: ClassVar[bool] = True

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return True

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [{"type": "color", "color": "green", "text": "True"}]


@dataclasses.dataclass()
class False_(Rule):
    """A rule that always returns False"""

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)
        always_false: ClassVar[bool] = True

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return False

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [{"type": "color", "color": "salmon", "text": "False"}]


@dataclasses.dataclass(init=False)
class NestedRule(Rule):
    children: "tuple[Rule, ...]"

    def __init__(self, *children: "Rule", options: "Iterable[OptionFilter[Any]]" = ()) -> None:
        super().__init__(options=options)
        self.children = children

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Rule.Resolved":
        children = [c.resolve(world) for c in self.children]
        return self.Resolved(tuple(children), player=world.player).simplify()

    @override
    def to_json(self) -> Mapping[str, Any]:
        return {
            "rule": self.__class__.__name__,
            "options": self.options,
            "children": [c.to_json() for c in self.children],
        }

    @override
    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Self:
        return cls(*data.get("children", []), options=data.get("options", ()))

    @override
    def __str__(self) -> str:
        children = ", ".join(str(c) for c in self.children)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({children}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        children: "tuple[Rule.Resolved, ...]"

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            combined_deps: dict[str, set[int]] = {}
            for child in self.children:
                for item_name, rules in child.item_dependencies().items():
                    if item_name in combined_deps:
                        combined_deps[item_name] |= rules
                    else:
                        combined_deps[item_name] = {id(self), *rules}
            return combined_deps

        @override
        def indirect_regions(self) -> tuple[str, ...]:
            return tuple(itertools.chain.from_iterable(child.indirect_regions() for child in self.children))

        def simplify(self) -> "Rule.Resolved":
            return self


@dataclasses.dataclass(init=False)
class And(NestedRule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(NestedRule.Resolved):
        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            for rule in self.children:
                if not rule.test(state):
                    return False
            return True

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " & "})
                messages.extend(child.explain(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def simplify(self) -> "Rule.Resolved":
            children_to_process = list(self.children)
            clauses: list[Rule.Resolved] = []
            items: dict[str, int] = {}
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

                if isinstance(child, Has.Resolved):
                    if child.item_name not in items or items[child.item_name] < child.count:
                        items[child.item_name] = child.count
                elif isinstance(child, HasAll.Resolved):
                    for item in child.item_names:
                        if item not in items:
                            items[item] = 1
                else:
                    clauses.append(child)

            if not clauses and not items:
                return true_rule or False_.Resolved(player=self.player)

            has_all_items: list[str] = []
            for item, count in items.items():
                if count == 1:
                    has_all_items.append(item)
                else:
                    clauses.append(Has.Resolved(item, count, player=self.player))

            if len(has_all_items) == 1:
                clauses.append(Has.Resolved(has_all_items[0], player=self.player))
            elif len(has_all_items) > 1:
                clauses.append(HasAll.Resolved(tuple(has_all_items), player=self.player))

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
        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            for rule in self.children:
                if rule.test(state):
                    return True
            return False

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " | "})
                messages.extend(child.explain(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def simplify(self) -> "Rule.Resolved":
            children_to_process = list(self.children)
            clauses: list[Rule.Resolved] = []
            items: dict[str, int] = {}

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

                if isinstance(child, Has.Resolved):
                    if child.item_name not in items or child.count < items[child.item_name]:
                        items[child.item_name] = child.count
                elif isinstance(child, HasAny.Resolved):
                    for item in child.item_names:
                        items[item] = 1
                else:
                    clauses.append(child)

            if not clauses and not items:
                return False_.Resolved(player=self.player)

            has_any_items: list[str] = []
            for item, count in items.items():
                if count == 1:
                    has_any_items.append(item)
                else:
                    clauses.append(Has.Resolved(item, count, player=self.player))

            if len(has_any_items) == 1:
                clauses.append(Has.Resolved(has_any_items[0], player=self.player))
            elif len(has_any_items) > 1:
                clauses.append(HasAny.Resolved(tuple(has_any_items), player=self.player))

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

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(self.item_name, self.count, player=world.player)

    @override
    def __str__(self) -> str:
        count = f", count={self.count}" if self.count > 1 else ""
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.item_name}{count}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_name: str
        count: int = 1

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has(self.item_name, self.player, count=self.count)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: {id(self)}}

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            messages: list[JSONMessagePart] = [{"type": "text", "text": "Has "}]
            if self.count > 1:
                messages.append({"type": "color", "color": "cyan", "text": str(self.count)})
                messages.append({"type": "text", "text": "x "})
            messages.append({"type": "item_name", "flags": 0b001, "text": self.item_name, "player": self.player})
            return messages


@dataclasses.dataclass(init=False)
class HasAll(Rule):
    """A rule that checks if the player has all of the given items"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    def __init__(self, *item_names: str, options: "Iterable[OptionFilter[Any]]" = ()) -> None:
        super().__init__(options=options)
        self.item_names = tuple(sorted(set(item_names)))

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Rule.Resolved":
        if len(self.item_names) == 0:
            return True_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(self.item_names, player=world.player)

    @override
    def __str__(self) -> str:
        items = ", ".join(self.item_names)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has_all(self.item_names, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
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

    def __init__(self, *item_names: str, options: "Iterable[OptionFilter[Any]]" = ()) -> None:
        super().__init__(options=options)
        self.item_names = tuple(sorted(set(item_names)))

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Rule.Resolved":
        if len(self.item_names) == 0:
            return True_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(self.item_names, player=world.player)

    @override
    def __str__(self) -> str:
        items = ", ".join(self.item_names)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has_any(self.item_names, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
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
    """The name of the location to test access to"""

    parent_region_name: str = ""
    """The name of the location's parent region. If not specified it will be resolved when the rule is resolved"""

    skip_indirect_connection: bool = False
    """Skip finding the location's parent region.
    Do not use this if this rule is for an entrance and explicit_indirect_conditions is True
    """

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        parent_region_name = self.parent_region_name
        if not parent_region_name and not self.skip_indirect_connection:
            location = world.get_location(self.location_name)
            if not location.parent_region:
                raise ValueError(f"Location {location.name} has no parent region")
            parent_region_name = location.parent_region.name
        return self.Resolved(self.location_name, parent_region_name, player=world.player)

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.location_name}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        location_name: str
        parent_region_name: str
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return state.can_reach_location(self.location_name, self.player)

        @override
        def indirect_regions(self) -> tuple[str, ...]:
            if self.parent_region_name:
                return (self.parent_region_name,)
            return ()

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "Reached Location "},
                {"type": "location_name", "text": self.location_name, "player": self.player},
            ]


@dataclasses.dataclass()
class CanReachRegion(Rule):
    region_name: str

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(self.region_name, player=world.player)

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.region_name}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        region_name: str
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return state.can_reach_region(self.region_name, self.player)

        @override
        def indirect_regions(self) -> tuple[str, ...]:
            return (self.region_name,)

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "Reached Region "},
                {"type": "color", "color": "yellow", "text": self.region_name},
            ]


@dataclasses.dataclass()
class CanReachEntrance(Rule):
    entrance_name: str

    @override
    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(self.entrance_name, player=world.player)

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.entrance_name}{options})"

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        entrance_name: str
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return state.can_reach_entrance(self.entrance_name, self.player)

        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "Reached Entrance "},
                {"type": "entrance_name", "text": self.entrance_name, "player": self.player},
            ]


class RuleWorldMixin(World):
    rule_ids: dict[int, Rule.Resolved]
    rule_dependencies: dict[str, set[int]]

    custom_rule_classes: ClassVar[dict[str, type[Rule]]]

    def __init__(self, multiworld: "MultiWorld", player: int) -> None:
        super().__init__(multiworld, player)
        self.rule_ids = {}
        self.rule_dependencies = defaultdict(set)

    @classmethod
    def rule_from_json(cls, data: Mapping[str, Any]) -> "Rule":
        name = data.get("rule", "")
        if name not in DEFAULT_RULES and name not in getattr(cls, "custom_rule_classes", {}):
            raise ValueError("Rule not found")
        rule_class = cls.custom_rule_classes[name] or DEFAULT_RULES.get(name)
        return rule_class.from_json(data)

    def resolve_rule(self, rule: "Rule") -> "Rule.Resolved":
        resolved_rule = rule.resolve(self)
        for item_name, rule_ids in resolved_rule.item_dependencies().items():
            self.rule_dependencies[item_name] |= rule_ids
        return resolved_rule

    def register_rule_connections(self, resolved_rule: "Rule.Resolved", entrance: "Entrance") -> None:
        for indirect_region in resolved_rule.indirect_regions():
            self.multiworld.register_indirect_condition(self.get_region(indirect_region), entrance)

    def set_rule(self, spot: "Location | Entrance", rule: "Rule") -> None:
        resolved_rule = self.resolve_rule(rule)
        spot.access_rule = resolved_rule.test
        if self.explicit_indirect_conditions and isinstance(spot, Entrance):
            self.register_rule_connections(resolved_rule, spot)

    @override
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        changed = super().collect(state, item)
        if changed and getattr(self, "rule_dependencies", None):
            player_results: dict[int, bool] = state.rule_cache[self.player]
            for rule_id in self.rule_dependencies[item.name]:
                _ = player_results.pop(rule_id, None)
        return changed

    @override
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        changed = super().remove(state, item)
        if changed and getattr(self, "rule_dependencies", None):
            player_results: dict[int, bool] = state.rule_cache[self.player]
            for rule_id in self.rule_dependencies[item.name]:
                _ = player_results.pop(rule_id, None)
        return changed


DEFAULT_RULES = {
    rule_name: rule_class
    for rule_name, rule_class in locals().items()
    if isinstance(rule_class, type) and issubclass(rule_class, Rule) and rule_class is not Rule
}
