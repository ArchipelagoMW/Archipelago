import dataclasses
import importlib
import operator
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Literal, cast

from typing_extensions import Never, Self, TypeVar, dataclass_transform, override

from BaseClasses import CollectionState, Entrance, Item, Location, MultiWorld, Region
from NetUtils import JSONMessagePart
from Options import CommonOptions, Option

if TYPE_CHECKING:
    from worlds.AutoWorld import World
else:
    World = object


class RuleWorldMixin(World):
    """A World mixin that provides helpers for interacting with the rule builder"""

    rule_ids: dict[int, "Rule.Resolved"]
    """A mapping of ids to resolved rules"""

    rule_item_dependencies: dict[str, set[int]]
    """A mapping of item name to set of rule ids"""

    rule_region_dependencies: dict[str, set[int]]
    """A mapping of region name to set of rule ids"""

    rule_location_dependencies: dict[str, set[int]]
    """A mapping of location name to set of rule ids"""

    rule_entrance_dependencies: dict[str, set[int]]
    """A mapping of entrance name to set of rule ids"""

    completion_rule: "Rule.Resolved | None" = None
    """The resolved rule used for the completion condition of this world"""

    true_rule: "Rule.Resolved"
    """A pre-initialized rule for this world that always returns True"""

    false_rule: "Rule.Resolved"
    """A pre-initialized rule for this world that always returns False"""

    item_mapping: ClassVar[dict[str, str]] = {}
    """A mapping of actual item name to logical item name.
    Useful when there are multiple versions of a collected item but the logic only uses one. For example:
    item = Item("Currency x500"), rule = Has("Currency", count=1000), item_mapping = {"Currency x500": "Currency"}"""

    rule_caching_enabled: ClassVar[bool] = True
    """Enable or disable the rule result caching system"""

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld, player)
        self.rule_ids = {}
        self.rule_item_dependencies = defaultdict(set)
        self.rule_region_dependencies = defaultdict(set)
        self.rule_location_dependencies = defaultdict(set)
        self.rule_entrance_dependencies = defaultdict(set)
        self.true_rule = self.resolve_rule(True_())
        self.false_rule = self.resolve_rule(False_())

    @classmethod
    def get_rule_cls(cls, name: str) -> type["Rule[Self]"]:
        """Returns the world-registered or default rule with the given name"""
        return CustomRuleRegister.get_rule_cls(cls.game, name)

    @classmethod
    def rule_from_dict(cls, data: Mapping[str, Any]) -> "Rule[Self]":
        """Create a rule instance from a serialized dict representation"""
        name = data.get("rule", "")
        rule_class = cls.get_rule_cls(name)
        return rule_class.from_dict(data, cls)

    def resolve_rule(self, rule: "Rule[Self]") -> "Rule.Resolved":
        """Returns a resolved rule registered with the caching system for this world"""
        resolved_rule = rule.resolve(self)
        resolved_rule = self.simplify_rule(resolved_rule)
        return self.get_cached_rule(resolved_rule)

    def get_cached_rule(self, resolved_rule: "Rule.Resolved") -> "Rule.Resolved":
        """Returns a cached instance of a resolved rule based on the hash"""
        rule_hash = hash(resolved_rule)
        if rule_hash in self.rule_ids:
            return self.rule_ids[rule_hash]
        self.rule_ids[rule_hash] = resolved_rule
        return resolved_rule

    def register_rule_dependencies(self, resolved_rule: "Rule.Resolved") -> None:
        """Registers a rule's item, region, location, and entrance dependencies to this world instance"""
        if not self.rule_caching_enabled:
            return
        for item_name, rule_ids in resolved_rule.item_dependencies().items():
            self.rule_item_dependencies[item_name] |= rule_ids
        for region_name, rule_ids in resolved_rule.region_dependencies().items():
            self.rule_region_dependencies[region_name] |= rule_ids
        for location_name, rule_ids in resolved_rule.location_dependencies().items():
            self.rule_location_dependencies[location_name] |= rule_ids
        for entrance_name, rule_ids in resolved_rule.entrance_dependencies().items():
            self.rule_entrance_dependencies[entrance_name] |= rule_ids

    def register_rule_connections(self, resolved_rule: "Rule.Resolved", entrance: Entrance) -> None:
        """Register indirect connections for this entrance based on the rule's dependencies"""
        for indirect_region in resolved_rule.region_dependencies().keys():
            self.multiworld.register_indirect_condition(self.get_region(indirect_region), entrance)

    def register_dependencies(self) -> None:
        """Register all rules that depend on locations or entrances with their dependencies"""
        if not self.rule_caching_enabled:
            return

        for location_name, rule_ids in self.rule_location_dependencies.items():
            try:
                location = self.get_location(location_name)
            except KeyError:
                continue
            if not isinstance(location.access_rule, Rule.Resolved):
                continue
            for item_name in location.access_rule.item_dependencies():
                self.rule_item_dependencies[item_name] |= rule_ids
            for region_name in location.access_rule.region_dependencies():
                self.rule_region_dependencies[region_name] |= rule_ids

        for entrance_name, rule_ids in self.rule_entrance_dependencies.items():
            try:
                entrance = self.get_entrance(entrance_name)
            except KeyError:
                continue
            if not isinstance(entrance.access_rule, Rule.Resolved):
                continue
            for item_name in entrance.access_rule.item_dependencies():
                self.rule_item_dependencies[item_name] |= rule_ids
            for region_name in entrance.access_rule.region_dependencies():
                self.rule_region_dependencies[region_name] |= rule_ids

    def set_rule(self, spot: Location | Entrance, rule: "Rule[Self]") -> None:
        """Resolve and set a rule on a location or entrance"""
        resolved_rule = self.resolve_rule(rule)
        self.register_rule_dependencies(resolved_rule)
        spot.access_rule = resolved_rule
        if self.explicit_indirect_conditions and isinstance(spot, Entrance):
            self.register_rule_connections(resolved_rule, spot)

    def create_entrance(
        self,
        from_region: Region,
        to_region: Region,
        rule: "Rule[Self] | None" = None,
        name: str | None = None,
    ) -> Entrance | None:
        """Try to create an entrance between regions with the given rule, skipping it if the rule resolves to False"""
        resolved_rule = None
        if rule is not None:
            resolved_rule = self.resolve_rule(rule)
            if resolved_rule.always_false:
                return None
            self.register_rule_dependencies(resolved_rule)

        entrance = from_region.connect(to_region, name)
        if resolved_rule:
            entrance.access_rule = resolved_rule
        if resolved_rule is not None:
            self.register_rule_connections(resolved_rule, entrance)
        return entrance

    def set_completion_rule(self, rule: "Rule[Self]") -> None:
        """Set the completion rule for this world"""
        resolved_rule = self.resolve_rule(rule)
        self.register_rule_dependencies(resolved_rule)
        self.multiworld.completion_condition[self.player] = resolved_rule
        self.completion_rule = resolved_rule

    def simplify_rule(self, rule: "Rule.Resolved") -> "Rule.Resolved":
        """Simplify and optimize a resolved rule"""
        if isinstance(rule, And.Resolved):
            return self._simplify_and(rule)
        if isinstance(rule, Or.Resolved):
            return self._simplify_or(rule)
        return rule

    def _simplify_and(self, rule: "And.Resolved") -> "Rule.Resolved":
        children_to_process = list(rule.children)
        clauses: list[Rule.Resolved] = []
        items: dict[str, int] = {}
        true_rule: Rule.Resolved | None = None

        while children_to_process:
            child = self.simplify_rule(children_to_process.pop(0))
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
            return true_rule or self.false_rule

        has_cls = cast(type[Has[Self]], self.get_rule_cls("Has"))
        has_all_cls = cast(type[HasAll[Self]], self.get_rule_cls("HasAll"))
        has_all_items: list[str] = []
        for item, count in items.items():
            if count == 1:
                has_all_items.append(item)
            else:
                clauses.append(
                    self.get_cached_rule(
                        has_cls.Resolved(item, count, player=rule.player, caching_enabled=self.rule_caching_enabled)
                    )
                )

        if len(has_all_items) == 1:
            clauses.append(
                self.get_cached_rule(
                    has_cls.Resolved(has_all_items[0], player=rule.player, caching_enabled=self.rule_caching_enabled)
                )
            )
        elif len(has_all_items) > 1:
            clauses.append(
                self.get_cached_rule(
                    has_all_cls.Resolved(
                        tuple(has_all_items),
                        player=rule.player,
                        caching_enabled=self.rule_caching_enabled,
                    )
                )
            )

        if len(clauses) == 1:
            return clauses[0]
        return And.Resolved(tuple(clauses), player=rule.player, caching_enabled=self.rule_caching_enabled)

    def _simplify_or(self, rule: "Or.Resolved") -> "Rule.Resolved":
        children_to_process = list(rule.children)
        clauses: list[Rule.Resolved] = []
        items: dict[str, int] = {}

        while children_to_process:
            child = self.simplify_rule(children_to_process.pop(0))
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
            return self.false_rule

        has_cls = cast(type[Has[Self]], self.get_rule_cls("Has"))
        has_any_cls = cast(type[HasAny[Self]], self.get_rule_cls("HasAny"))
        has_any_items: list[str] = []
        for item, count in items.items():
            if count == 1:
                has_any_items.append(item)
            else:
                clauses.append(
                    self.get_cached_rule(
                        has_cls.Resolved(item, count, player=rule.player, caching_enabled=self.rule_caching_enabled)
                    )
                )

        if len(has_any_items) == 1:
            clauses.append(
                self.get_cached_rule(
                    has_cls.Resolved(has_any_items[0], player=rule.player, caching_enabled=self.rule_caching_enabled)
                )
            )
        elif len(has_any_items) > 1:
            clauses.append(
                self.get_cached_rule(
                    has_any_cls.Resolved(
                        tuple(has_any_items),
                        player=rule.player,
                        caching_enabled=self.rule_caching_enabled,
                    )
                )
            )

        if len(clauses) == 1:
            return clauses[0]
        return Or.Resolved(tuple(clauses), player=rule.player, caching_enabled=self.rule_caching_enabled)

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if changed and self.rule_caching_enabled and self.rule_item_dependencies:
            player_results = state.rule_cache[self.player]
            mapped_name = self.item_mapping.get(item.name, "")
            rule_ids = self.rule_item_dependencies[item.name] | self.rule_item_dependencies[mapped_name]
            for rule_id in rule_ids:
                if player_results.get(rule_id, None) is False:
                    del player_results[rule_id]

        return changed

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if not changed or not self.rule_caching_enabled:
            return changed

        player_results = state.rule_cache[self.player]
        if self.rule_item_dependencies:
            mapped_name = self.item_mapping.get(item.name, "")
            rule_ids = self.rule_item_dependencies[item.name] | self.rule_item_dependencies[mapped_name]
            for rule_id in rule_ids:
                player_results.pop(rule_id, None)

        # clear all region dependent caches as none can be trusted
        if self.rule_region_dependencies:
            for rule_ids in self.rule_region_dependencies.values():
                for rule_id in rule_ids:
                    player_results.pop(rule_id, None)

        # clear all location dependent caches as they may have lost region access
        if self.rule_location_dependencies:
            for rule_ids in self.rule_location_dependencies.values():
                for rule_id in rule_ids:
                    player_results.pop(rule_id, None)

        # clear all entrance dependent caches as they may have lost region access
        if self.rule_entrance_dependencies:
            for rule_ids in self.rule_entrance_dependencies.values():
                for rule_id in rule_ids:
                    player_results.pop(rule_id, None)

        return changed

    @override
    def reached_region(self, state: CollectionState, region: Region) -> None:
        super().reached_region(state, region)
        if self.rule_caching_enabled and self.rule_region_dependencies:
            player_results = state.rule_cache[self.player]
            for rule_id in self.rule_region_dependencies[region.name]:
                player_results.pop(rule_id, None)


TWorld = TypeVar("TWorld", bound=RuleWorldMixin, contravariant=True, default=RuleWorldMixin)  # noqa: PLC0105

Operator = Literal["eq", "ne", "gt", "lt", "ge", "le", "contains"]

OPERATORS: dict[Operator, Callable[..., bool]] = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "contains": operator.contains,
}
operator_strings: dict[Operator, str] = {
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "lt": "<",
    "ge": ">=",
    "le": "<=",
}

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class OptionFilter(Generic[T]):
    option: type[Option[T]]
    value: T
    operator: Operator = "eq"

    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this option filter"""
        return {
            "option": f"{self.option.__module__}.{self.option.__name__}",
            "value": self.value,
            "operator": self.operator,
        }

    def check(self, options: CommonOptions) -> bool:
        """Tests the given options dataclass to see if it passes this option filter"""
        option_name = next(
            (name for name, cls in options.__class__.type_hints.items() if cls is self.option),
            None,
        )
        if option_name is None:
            raise ValueError(f"Cannot find option {self.option.__name__} in options class {options.__class__.__name__}")
        opt = cast(Option[Any] | None, getattr(options, option_name, None))
        if opt is None:
            raise ValueError(f"Invalid option: {option_name}")

        return OPERATORS[self.operator](opt.value, self.value)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Returns a new OptionFilter instance from a dict representation"""
        if "option" not in data or "value" not in data:
            raise ValueError("Missing required value and/or option")

        option_path = data["option"]
        try:
            option_mod_name, option_cls_name = option_path.rsplit(".", 1)
            option_module = importlib.import_module(option_mod_name)
            option = getattr(option_module, option_cls_name, None)
        except (ValueError, ImportError) as e:
            raise ValueError(f"Cannot parse option '{option_path}'") from e
        if option is None or not issubclass(option, Option):
            raise ValueError(f"Invalid option '{option_path}' returns type '{option}' instead of Option subclass")

        value = data["value"]
        operator = data.get("operator", "eq")
        return cls(option=cast(type[Option[Any]], option), value=value, operator=operator)

    @classmethod
    def multiple_from_dict(cls, data: Iterable[dict[str, Any]]) -> tuple["OptionFilter[Any]", ...]:
        """Returns a tuple of OptionFilters instances from an iterable of dict representations"""
        return tuple(cls.from_dict(o) for o in data)

    @override
    def __str__(self) -> str:
        op = operator_strings.get(self.operator, self.operator)
        return f"{self.option.__name__} {op} {self.value}"


def _create_hash_fn(resolved_rule_cls: "CustomRuleRegister") -> Callable[..., int]:
    def hash_impl(self: "Rule.Resolved") -> int:
        return hash(
            (
                self.__class__.__module__,
                self.rule_name,
                *[getattr(self, f.name) for f in dataclasses.fields(self)],
            )
        )

    hash_impl.__qualname__ = f"{resolved_rule_cls.__qualname__}.__hash__"
    return hash_impl


@dataclass_transform(frozen_default=True, field_specifiers=(dataclasses.field, dataclasses.Field))
class CustomRuleRegister(type):
    """A metaclass to contain world custom rules and automatically convert resolved rules to frozen dataclasses"""

    custom_rules: ClassVar[dict[str, dict[str, type["Rule[Any]"]]]] = {}
    """A mapping of game name to mapping of rule name to rule class"""

    rule_name: str = "Rule"
    """The string name of a rule, must be unique per game"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: dict[str, Any],
    ) -> type["CustomRuleRegister"]:
        new_cls = super().__new__(cls, name, bases, namespace, **kwds)
        new_cls.__hash__ = _create_hash_fn(new_cls)
        rule_name = new_cls.__qualname__
        if rule_name.endswith(".Resolved"):
            rule_name = rule_name[:-9]
        new_cls.rule_name = rule_name
        return dataclasses.dataclass(frozen=True)(new_cls)

    @classmethod
    def get_rule_cls(cls, game_name: str, rule_name: str) -> type["Rule[Any]"]:
        """Returns the world-registered or default rule with the given name"""
        custom_rule_classes = cls.custom_rules.get(game_name, {})
        if rule_name not in DEFAULT_RULES and rule_name not in custom_rule_classes:
            raise ValueError(f"Rule '{rule_name}' for game '{game_name}' not found")
        return custom_rule_classes.get(rule_name) or DEFAULT_RULES[rule_name]


@dataclasses.dataclass()
class Rule(Generic[TWorld]):
    """Base class for a static rule used to generate an access rule"""

    options: Iterable[OptionFilter[Any]] = dataclasses.field(default=(), kw_only=True)
    """An iterable of OptionFilters to restrict what options are required for this rule to be active"""

    game_name: ClassVar[str]
    """The name of the game this rule belongs to, default rules belong to 'Archipelago'"""

    def __post_init__(self) -> None:
        if not isinstance(self.options, tuple):
            self.options = tuple(self.options)

    def _instantiate(self, world: TWorld) -> "Resolved":
        """Create a new resolved rule for this world"""
        return self.Resolved(player=world.player, caching_enabled=world.rule_caching_enabled)

    def resolve(self, world: TWorld) -> "Resolved":
        """Resolve a rule with the given world"""
        for option_filter in self.options:
            if not option_filter.check(world.options):
                return world.false_rule
        return self._instantiate(world)

    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this rule"""
        args = {
            field.name: getattr(self, field.name, None) for field in dataclasses.fields(self) if field.name != "options"
        }
        return {
            "rule": self.__class__.__qualname__,
            "options": [o.to_dict() for o in self.options],
            "args": args,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        """Returns a new instance of this rule from a serialized dict representation"""
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(**data.get("args", {}), options=options)

    def __and__(self, other: "Rule[Any]") -> "Rule[TWorld]":
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

    def __or__(self, other: "Rule[Any]") -> "Rule[TWorld]":
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
        """Safeguard to prevent devs from mistakenly doing `rule1 and rule2` and getting the wrong result"""
        raise TypeError("Use & or | to combine rules, or use `is not None` for boolean tests")

    @override
    def __str__(self) -> str:
        options = f"options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({options})"

    @classmethod
    def __init_subclass__(cls, /, game: str) -> None:
        if game != "Archipelago":
            custom_rules = CustomRuleRegister.custom_rules.setdefault(game, {})
            if cls.__qualname__ in custom_rules:
                raise TypeError(f"Rule {cls.__qualname__} has already been registered for game {game}")
            custom_rules[cls.__qualname__] = cls
        elif cls.__module__ != "rule_builder":
            # TODO: test to make sure this works on frozen
            raise TypeError("You cannot define custom rules for the base Archipelago world")
        cls.game_name = game

    class Resolved(metaclass=CustomRuleRegister):
        """A resolved rule for a given world that can be used as an access rule"""

        _: dataclasses.KW_ONLY

        player: int
        """The player this rule is for"""

        caching_enabled: bool = dataclasses.field(repr=False, default=True, kw_only=True)
        """If the world this rule is for has caching enabled"""

        force_recalculate: ClassVar[bool] = False
        """Forces this rule to be recalculated every time it is evaluated.
        Forces any parent composite rules containing this rule to also be recalculated. Implies skip_cache."""

        skip_cache: ClassVar[bool] = False
        """Skips the caching layer when evaluating this rule.
        Composite rules will still respect the caching layer so dependencies functions should be implemented as normal.
        Set to True when rule calculation is trivial."""

        always_true: ClassVar[bool] = False
        """Whether this rule always evaluates to True, used to short-circuit logic"""

        always_false: ClassVar[bool] = False
        """Whether this rule always evaluates to True, used to short-circuit logic"""

        def __post_init__(self) -> None:
            object.__setattr__(
                self,
                "caching_enabled",
                self.caching_enabled and not self.force_recalculate and not self.skip_cache,
            )

        def __call__(self, state: CollectionState) -> bool:
            """Evaluate this rule's result with the given state, using the cached value if possible"""
            if not self.caching_enabled:
                return self._evaluate(state)

            cached_result = state.rule_cache[self.player].get(id(self))
            if cached_result is not None:
                return cached_result

            result = self._evaluate(state)
            state.rule_cache[self.player][id(self)] = result
            return result

        def _evaluate(self, state: CollectionState) -> bool:
            """Calculate this rule's result with the given state"""
            ...

        def item_dependencies(self) -> dict[str, set[int]]:
            """Returns a mapping of item name to set of object ids, used for cache invalidation"""
            return {}

        def region_dependencies(self) -> dict[str, set[int]]:
            """Returns a mapping of region name to set of object ids,
            used for indirect connections and cache invalidation"""
            return {}

        def location_dependencies(self) -> dict[str, set[int]]:
            """Returns a mapping of location name to set of object ids, used for cache invalidation"""
            return {}

        def entrance_dependencies(self) -> dict[str, set[int]]:
            """Returns a mapping of entrance name to set of object ids, used for cache invalidation"""
            return {}

        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            """Returns a list of printJSON messages that explain the logic for this rule"""
            return [{"type": "text", "text": self.rule_name}]

        def explain_str(self, state: CollectionState | None = None) -> str:
            """Returns a human readable string describing this rule"""
            return str(self)

        @override
        def __str__(self) -> str:
            return self.rule_name


@dataclasses.dataclass()
class True_(Rule[TWorld], game="Archipelago"):  # noqa: N801
    """A rule that always returns True"""

    class Resolved(Rule.Resolved):
        always_true: ClassVar[bool] = True
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return True

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [{"type": "color", "color": "green", "text": "True"}]

        @override
        def __str__(self) -> str:
            return "True"


@dataclasses.dataclass()
class False_(Rule[TWorld], game="Archipelago"):  # noqa: N801
    """A rule that always returns False"""

    class Resolved(Rule.Resolved):
        always_false: ClassVar[bool] = True
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [{"type": "color", "color": "salmon", "text": "False"}]

        @override
        def __str__(self) -> str:
            return "False"


@dataclasses.dataclass(init=False)
class NestedRule(Rule[TWorld], game="Archipelago"):
    """A rule that takes an iterable of other rules as an argument and does logic based on them"""

    children: tuple[Rule[TWorld], ...]
    """The child rules this rule's logic is based on"""

    def __init__(self, *children: Rule[TWorld], options: Iterable[OptionFilter[Any]] = ()) -> None:
        super().__init__(options=options)
        self.children = children

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        children = [world.resolve_rule(c) for c in self.children]
        return self.Resolved(tuple(children), player=world.player, caching_enabled=world.rule_caching_enabled)

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data["args"]
        data["children"] = [c.to_dict() for c in self.children]
        return data

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        children = [world_cls.rule_from_dict(c) for c in data.get("children", ())]
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*children, options=options)

    @override
    def __str__(self) -> str:
        children = ", ".join(str(c) for c in self.children)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({children}{options})"

    class Resolved(Rule.Resolved):
        children: tuple[Rule.Resolved, ...]

        def __post_init__(self) -> None:
            object.__setattr__(
                self,
                "force_recalculate",
                self.force_recalculate or any(c.force_recalculate for c in self.children),
            )
            super().__post_init__()

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
        def region_dependencies(self) -> dict[str, set[int]]:
            combined_deps: dict[str, set[int]] = {}
            for child in self.children:
                for region_name, rules in child.region_dependencies().items():
                    if region_name in combined_deps:
                        combined_deps[region_name] |= rules
                    else:
                        combined_deps[region_name] = {id(self), *rules}
            return combined_deps

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            combined_deps: dict[str, set[int]] = {}
            for child in self.children:
                for location_name, rules in child.location_dependencies().items():
                    if location_name in combined_deps:
                        combined_deps[location_name] |= rules
                    else:
                        combined_deps[location_name] = {id(self), *rules}
            return combined_deps

        @override
        def entrance_dependencies(self) -> dict[str, set[int]]:
            combined_deps: dict[str, set[int]] = {}
            for child in self.children:
                for entrance_name, rules in child.entrance_dependencies().items():
                    if entrance_name in combined_deps:
                        combined_deps[entrance_name] |= rules
                    else:
                        combined_deps[entrance_name] = {id(self), *rules}
            return combined_deps


@dataclasses.dataclass(init=False)
class And(NestedRule[TWorld], game="Archipelago"):
    """A rule that only returns true when all child rules evaluate as true"""

    class Resolved(NestedRule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            for rule in self.children:
                if not rule(state):
                    return False
            return True

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " & "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = " & ".join([c.explain_str(state) for c in self.children])
            return f"({clauses})"

        @override
        def __str__(self) -> str:
            clauses = " & ".join([str(c) for c in self.children])
            return f"({clauses})"


@dataclasses.dataclass(init=False)
class Or(NestedRule[TWorld], game="Archipelago"):
    """A rule that returns true when any child rule evaluates as true"""

    class Resolved(NestedRule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            for rule in self.children:
                if rule(state):
                    return True
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " | "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = " | ".join([c.explain_str(state) for c in self.children])
            return f"({clauses})"

        @override
        def __str__(self) -> str:
            clauses = " | ".join([str(c) for c in self.children])
            return f"({clauses})"


@dataclasses.dataclass()
class Wrapper(Rule[TWorld], game="Archipelago"):
    """A rule that wraps another rule to provide extra logic or data"""

    child: Rule[TWorld]
    """The child rule being wrapped"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(
            world.resolve_rule(self.child),
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data["args"]
        data["child"] = self.child.to_dict()
        return data

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        child = data.get("child")
        if child is None:
            raise ValueError("Child rule cannot be None")
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(world_cls.rule_from_dict(child), options=options)

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(Rule.Resolved):
        child: Rule.Resolved

        def __post_init__(self) -> None:
            object.__setattr__(self, "force_recalculate", self.force_recalculate or self.child.force_recalculate)
            super().__post_init__()

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.child(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps: dict[str, set[int]] = {}
            for item_name, rules in self.child.item_dependencies().items():
                deps[item_name] = {id(self), *rules}
            return deps

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            deps: dict[str, set[int]] = {}
            for region_name, rules in self.child.region_dependencies().items():
                deps[region_name] = {id(self), *rules}
            return deps

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            deps: dict[str, set[int]] = {}
            for location_name, rules in self.child.location_dependencies().items():
                deps[location_name] = {id(self), *rules}
            return deps

        @override
        def entrance_dependencies(self) -> dict[str, set[int]]:
            deps: dict[str, set[int]] = {}
            for entrance_name, rules in self.child.entrance_dependencies().items():
                deps[entrance_name] = {id(self), *rules}
            return deps

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": f"{self.rule_name} ["}]
            messages.extend(self.child.explain_json(state))
            messages.append({"type": "text", "text": "]"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            return f"{self.rule_name}[{self.child.explain_str(state)}]"

        @override
        def __str__(self) -> str:
            return f"{self.rule_name}[{self.child}]"


@dataclasses.dataclass()
class Has(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has at least `count` of a given item"""

    item_name: str
    """The item to check for"""

    count: int = 1
    """The count the player is required to have"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(
            self.item_name,
            self.count,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        count = f", count={self.count}" if self.count > 1 else ""
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.item_name}{count}{options})"

    class Resolved(Rule.Resolved):
        item_name: str
        count: int = 1
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has
            return state.prog_items[self.player][self.item_name] >= self.count

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: set()}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            verb = "Missing " if state and not self(state) else "Has "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if self.count > 1:
                messages.append({"type": "color", "color": "cyan", "text": str(self.count)})
                messages.append({"type": "text", "text": "x "})
            item_message: JSONMessagePart = {
                "type": "item_name",
                "flags": 0b001,
                "text": self.item_name,
                "player": self.player,
            }
            if state:
                item_message["color"] = "green" if self(state) else "salmon"
            messages.append(item_message)
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Has" if self(state) else "Missing"
            count = f"{self.count}x " if self.count > 1 else ""
            return f"{prefix} {count}{self.item_name}"

        @override
        def __str__(self) -> str:
            count = f"{self.count}x " if self.count > 1 else ""
            return f"Has {count}{self.item_name}"


@dataclasses.dataclass(init=False)
class HasAll(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has all of the given items"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    def __init__(self, *item_names: str, options: Iterable[OptionFilter[Any]] = ()) -> None:
        super().__init__(options=options)
        self.item_names = tuple(sorted(set(item_names)))

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0:
            # match state.has_all
            return world.true_rule
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(self.item_names, player=world.player, caching_enabled=world.rule_caching_enabled)

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options)

    @override
    def __str__(self) -> str:
        items = ", ".join(self.item_names)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}{options})"

    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_all
            player_prog_items = state.prog_items[self.player]
            for item in self.item_names:
                if not player_prog_items[item]:
                    return False
            return True

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
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

            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            messages = [
                {"type": "text", "text": "Has " if not missing else "Missing "},
                {"type": "color", "color": "cyan", "text": "all" if not missing else "some"},
                {"type": "text", "text": " of ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, item in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "green", "text": item, "player": self.player}
                    )
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "salmon", "text": item, "player": self.player}
                    )
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            prefix = "Has all" if self(state) else "Missing some"
            found_str = f"Found: {', '.join(found)}" if found else ""
            missing_str = f"Missing: {', '.join(missing)}" if missing else ""
            infix = "; " if found and missing else ""
            return f"{prefix} of ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            items = ", ".join(self.item_names)
            return f"Has all of ({items})"


@dataclasses.dataclass(init=False)
class HasAny(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has at least one of the given items"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    def __init__(self, *item_names: str, options: Iterable[OptionFilter[Any]] = ()) -> None:
        super().__init__(options=options)
        self.item_names = tuple(sorted(set(item_names)))

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0:
            # match state.has_any
            return world.false_rule
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(self.item_names, player=world.player, caching_enabled=world.rule_caching_enabled)

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options)

    @override
    def __str__(self) -> str:
        items = ", ".join(self.item_names)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}{options})"

    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_any
            player_prog_items = state.prog_items[self.player]
            for item in self.item_names:
                if player_prog_items[item]:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
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

            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            messages = [
                {"type": "text", "text": "Has " if found else "Missing "},
                {"type": "color", "color": "cyan", "text": "some" if found else "all"},
                {"type": "text", "text": " of ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, item in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "green", "text": item, "player": self.player}
                    )
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "salmon", "text": item, "player": self.player}
                    )
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            prefix = "Has some" if self(state) else "Missing all"
            found_str = f"Found: {', '.join(found)}" if found else ""
            missing_str = f"Missing: {', '.join(missing)}" if missing else ""
            infix = "; " if found and missing else ""
            return f"{prefix} of ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            items = ", ".join(self.item_names)
            return f"Has any of ({items})"


@dataclasses.dataclass()
class HasAllCounts(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has all of the specified counts of the given items"""

    item_counts: dict[str, int]
    """A mapping of item name to count to check for"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_counts) == 0:
            # match state.has_all_counts
            return world.true_rule
        if len(self.item_counts) == 1:
            item = next(iter(self.item_counts))
            return Has(item, self.item_counts[item]).resolve(world)
        return self.Resolved(
            tuple(self.item_counts.items()),
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        items = ", ".join([f"{item} x{count}" for item, count in self.item_counts.items()])
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}{options})"

    class Resolved(Rule.Resolved):
        item_counts: tuple[tuple[str, int], ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_all_counts
            player_prog_items = state.prog_items[self.player]
            for item, count in self.item_counts:
                if player_prog_items[item] < count:
                    return False
            return True

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item, _ in self.item_counts}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": "all"},
                    {"type": "text", "text": " of ("},
                ]
                for i, (item, count) in enumerate(self.item_counts):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "item_name", "flags": 0b001, "text": item, "player": self.player})
                    messages.append({"type": "text", "text": f" x{count}"})
                messages.append({"type": "text", "text": ")"})
                return messages

            found = [(item, count) for item, count in self.item_counts if state.has(item, self.player, count)]
            missing = [(item, count) for item, count in self.item_counts if (item, count) not in found]
            messages = [
                {"type": "text", "text": "Has " if not missing else "Missing "},
                {"type": "color", "color": "cyan", "text": "all" if not missing else "some"},
                {"type": "text", "text": " of ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, (item, count) in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "green", "text": item, "player": self.player}
                    )
                    messages.append({"type": "text", "text": f" x{count}"})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, (item, count) in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "salmon", "text": item, "player": self.player}
                    )
                    messages.append({"type": "text", "text": f" x{count}"})
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            found = [(item, count) for item, count in self.item_counts if state.has(item, self.player, count)]
            missing = [(item, count) for item, count in self.item_counts if (item, count) not in found]
            prefix = "Has all" if self(state) else "Missing some"
            found_str = f"Found: {', '.join([f'{item} x{count}' for item, count in found])}" if found else ""
            missing_str = f"Missing: {', '.join([f'{item} x{count}' for item, count in missing])}" if missing else ""
            infix = "; " if found and missing else ""
            return f"{prefix} of ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            items = ", ".join([f"{item} x{count}" for item, count in self.item_counts])
            return f"Has all of ({items})"


@dataclasses.dataclass()
class HasAnyCount(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has any of the specified counts of the given items"""

    item_counts: dict[str, int]
    """A mapping of item name to count to check for"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_counts) == 0:
            # match state.has_any_count
            return world.false_rule
        if len(self.item_counts) == 1:
            item = next(iter(self.item_counts))
            return Has(item, self.item_counts[item]).resolve(world)
        return self.Resolved(
            tuple(self.item_counts.items()),
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        items = ", ".join([f"{item} x{count}" for item, count in self.item_counts.items()])
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}{options})"

    class Resolved(Rule.Resolved):
        item_counts: tuple[tuple[str, int], ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_any_count
            player_prog_items = state.prog_items[self.player]
            for item, count in self.item_counts:
                if player_prog_items[item] >= count:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item, _ in self.item_counts}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": "any"},
                    {"type": "text", "text": " of ("},
                ]
                for i, (item, count) in enumerate(self.item_counts):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "item_name", "flags": 0b001, "text": item, "player": self.player})
                    messages.append({"type": "text", "text": f" x{count}"})
                messages.append({"type": "text", "text": ")"})
                return messages

            found = [(item, count) for item, count in self.item_counts if state.has(item, self.player, count)]
            missing = [(item, count) for item, count in self.item_counts if (item, count) not in found]
            messages = [
                {"type": "text", "text": "Has " if found else "Missing "},
                {"type": "color", "color": "cyan", "text": "some" if found else "all"},
                {"type": "text", "text": " of ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, (item, count) in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "green", "text": item, "player": self.player}
                    )
                    messages.append({"type": "text", "text": f" x{count}"})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, (item, count) in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "salmon", "text": item, "player": self.player}
                    )
                    messages.append({"type": "text", "text": f" x{count}"})
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            found = [(item, count) for item, count in self.item_counts if state.has(item, self.player, count)]
            missing = [(item, count) for item, count in self.item_counts if (item, count) not in found]
            prefix = "Has some" if self(state) else "Missing all"
            found_str = f"Found: {', '.join([f'{item} x{count}' for item, count in found])}" if found else ""
            missing_str = f"Missing: {', '.join([f'{item} x{count}' for item, count in missing])}" if missing else ""
            infix = "; " if found and missing else ""
            return f"{prefix} of ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            items = ", ".join([f"{item} x{count}" for item, count in self.item_counts])
            return f"Has any of ({items})"


@dataclasses.dataclass(init=False)
class HasFromList(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has at least `count` of the given items"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    count: int = 1
    """The number of items the player needs to have"""

    def __init__(self, *item_names: str, count: int = 1, options: Iterable[OptionFilter[Any]] = ()) -> None:
        super().__init__(options=options)
        self.item_names = tuple(sorted(set(item_names)))
        self.count = count

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0:
            # match state.has_from_list
            return world.false_rule
        if len(self.item_names) == 1:
            return Has(self.item_names[0], self.count).resolve(world)
        return self.Resolved(
            self.item_names,
            self.count,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options)

    @override
    def __str__(self) -> str:
        items = ", ".join(self.item_names)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}, count={self.count}{options})"

    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]
        count: int = 1

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_from_list
            found = 0
            player_prog_items = state.prog_items[self.player]
            for item_name in self.item_names:
                found += player_prog_items[item_name]
                if found >= self.count:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": str(self.count)},
                    {"type": "text", "text": "x items from ("},
                ]
                for i, item in enumerate(self.item_names):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "item_name", "flags": 0b001, "text": item, "player": self.player})
                messages.append({"type": "text", "text": ")"})
                return messages

            found_count = state.count_from_list(self.item_names, self.player)
            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            messages = [
                {"type": "text", "text": "Has "},
                {
                    "type": "color",
                    "color": "green" if found_count >= self.count else "salmon",
                    "text": f"{found_count}/{self.count}",
                },
                {"type": "text", "text": " items from ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, item in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "green", "text": item, "player": self.player}
                    )
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "salmon", "text": item, "player": self.player}
                    )
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            found_count = state.count_from_list(self.item_names, self.player)
            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            found_str = f"Found: {', '.join(found)}" if found else ""
            missing_str = f"Missing: {', '.join(missing)}" if missing else ""
            infix = "; " if found and missing else ""
            return f"Has {found_count}/{self.count} items from ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            items = ", ".join(self.item_names)
            count = f"{self.count}x items" if self.count > 1 else "an item"
            return f"Has {count} from ({items})"


@dataclasses.dataclass(init=False)
class HasFromListUnique(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has at least `count` of the given items, ignoring duplicates of the same item"""

    item_names: tuple[str, ...]
    """A tuple of item names to check for"""

    count: int = 1
    """The number of items the player needs to have"""

    def __init__(self, *item_names: str, count: int = 1, options: Iterable[OptionFilter[Any]] = ()) -> None:
        super().__init__(options=options)
        self.item_names = tuple(sorted(set(item_names)))
        self.count = count

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0 or len(self.item_names) < self.count:
            # match state.has_from_list_unique
            return world.false_rule
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(
            self.item_names,
            self.count,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[RuleWorldMixin]) -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options)

    @override
    def __str__(self) -> str:
        items = ", ".join(self.item_names)
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({items}, count={self.count}{options})"

    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]
        count: int = 1

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_from_list_unique
            found = 0
            player_prog_items = state.prog_items[self.player]
            for item_name in self.item_names:
                found += player_prog_items[item_name] > 0
                if found >= self.count:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": str(self.count)},
                    {"type": "text", "text": "x unique items from ("},
                ]
                for i, item in enumerate(self.item_names):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "item_name", "flags": 0b001, "text": item, "player": self.player})
                messages.append({"type": "text", "text": ")"})
                return messages

            found_count = state.count_from_list_unique(self.item_names, self.player)
            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            messages = [
                {"type": "text", "text": "Has "},
                {
                    "type": "color",
                    "color": "green" if found_count >= self.count else "salmon",
                    "text": f"{found_count}/{self.count}",
                },
                {"type": "text", "text": " unique items from ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, item in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "green", "text": item, "player": self.player}
                    )
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append(
                        {"type": "item_name", "flags": 0b001, "color": "salmon", "text": item, "player": self.player}
                    )
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            found_count = state.count_from_list_unique(self.item_names, self.player)
            found = [item for item in self.item_names if state.has(item, self.player)]
            missing = [item for item in self.item_names if item not in found]
            found_str = f"Found: {', '.join(found)}" if found else ""
            missing_str = f"Missing: {', '.join(missing)}" if missing else ""
            infix = "; " if found and missing else ""
            return f"Has {found_count}/{self.count} unique items from ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            items = ", ".join(self.item_names)
            count = f"{self.count}x unique items" if self.count > 1 else "a unique item"
            return f"Has {count} from ({items})"


@dataclasses.dataclass()
class HasGroup(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has at least `count` of the items present in the specified item group"""

    item_name_group: str
    """The name of the item group containing the items"""

    count: int = 1
    """The number of items the player needs to have"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        item_names = tuple(sorted(world.item_name_groups[self.item_name_group]))
        return self.Resolved(
            self.item_name_group,
            item_names,
            self.count,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        count = f", count={self.count}" if self.count > 1 else ""
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.item_name_group}{count}{options})"

    class Resolved(Rule.Resolved):
        item_name_group: str
        item_names: tuple[str, ...]
        count: int = 1

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_group
            found = 0
            player_prog_items = state.prog_items[self.player]
            for item_name in self.item_names:
                found += player_prog_items[item_name]
                if found >= self.count:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": "Has "}]
            if state is None:
                messages.append({"type": "color", "color": "cyan", "text": str(self.count)})
            else:
                count = state.count_group(self.item_name_group, self.player)
                color = "green" if count >= self.count else "salmon"
                messages.append({"type": "color", "color": color, "text": f"{count}/{self.count}"})
            messages.append({"type": "text", "text": " items from "})
            messages.append({"type": "color", "color": "cyan", "text": self.item_name_group})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            count = state.count_group(self.item_name_group, self.player)
            return f"Has {count}/{self.count} items from {self.item_name_group}"

        @override
        def __str__(self) -> str:
            count = f"{self.count}x items" if self.count > 1 else "an item"
            return f"Has {count} from {self.item_name_group}"


@dataclasses.dataclass()
class HasGroupUnique(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the player has at least `count` of the items present
    in the specified item group, ignoring duplicates of the same item"""

    item_name_group: str
    """The name of the item group containing the items"""

    count: int = 1
    """The number of items the player needs to have"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        item_names = tuple(sorted(world.item_name_groups[self.item_name_group]))
        return self.Resolved(
            self.item_name_group,
            item_names,
            self.count,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        count = f", count={self.count}" if self.count > 1 else ""
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.item_name_group}{count}{options})"

    class Resolved(Rule.Resolved):
        item_name_group: str
        item_names: tuple[str, ...]
        count: int = 1

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has_group_unique
            found = 0
            player_prog_items = state.prog_items[self.player]
            for item_name in self.item_names:
                found += player_prog_items[item_name] > 0
                if found >= self.count:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.item_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": "Has "}]
            if state is None:
                messages.append({"type": "color", "color": "cyan", "text": str(self.count)})
            else:
                count = state.count_group_unique(self.item_name_group, self.player)
                color = "green" if count >= self.count else "salmon"
                messages.append({"type": "color", "color": color, "text": f"{count}/{self.count}"})
            messages.append({"type": "text", "text": " unique items from "})
            messages.append({"type": "color", "color": "cyan", "text": self.item_name_group})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            count = state.count_group_unique(self.item_name_group, self.player)
            return f"Has {count}/{self.count} unique items from {self.item_name_group}"

        @override
        def __str__(self) -> str:
            count = f"{self.count}x unique items" if self.count > 1 else "a unique item"
            return f"Has {count} from {self.item_name_group}"


@dataclasses.dataclass()
class CanReachLocation(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the given location is reachable by the current player"""

    location_name: str
    """The name of the location to test access to"""

    parent_region_name: str = ""
    """The name of the location's parent region. If not specified it will be resolved when the rule is resolved"""

    skip_indirect_connection: bool = False
    """Skip finding the location's parent region.
    Do not use this if this rule is for an entrance and explicit_indirect_conditions is True
    """

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        parent_region_name = self.parent_region_name
        if not parent_region_name and not self.skip_indirect_connection:
            location = world.get_location(self.location_name)
            if not location.parent_region:
                raise ValueError(f"Location {location.name} has no parent region")
            parent_region_name = location.parent_region.name
        return self.Resolved(
            self.location_name,
            parent_region_name,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.location_name}{options})"

    class Resolved(Rule.Resolved):
        location_name: str
        parent_region_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.can_reach_location(self.location_name, self.player)

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            if self.parent_region_name:
                return {self.parent_region_name: {id(self)}}
            return {}

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            return {self.location_name: {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                verb = "Can reach"
            elif self(state):
                verb = "Reached"
            else:
                verb = "Cannot reach"
            return [
                {"type": "text", "text": f"{verb} location "},
                {"type": "location_name", "text": self.location_name, "player": self.player},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Reached" if self(state) else "Cannot reach"
            return f"{prefix} location {self.location_name}"

        @override
        def __str__(self) -> str:
            return f"Can reach location {self.location_name}"


@dataclasses.dataclass()
class CanReachRegion(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the given region is reachable by the current player"""

    region_name: str
    """The name of the region to test access to"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(self.region_name, player=world.player, caching_enabled=world.rule_caching_enabled)

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.region_name}{options})"

    class Resolved(Rule.Resolved):
        region_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.can_reach_region(self.region_name, self.player)

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {self.region_name: {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                verb = "Can reach"
            elif self(state):
                verb = "Reached"
            else:
                verb = "Cannot reach"
            return [
                {"type": "text", "text": f"{verb} region "},
                {"type": "color", "color": "yellow", "text": self.region_name},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Reached" if self(state) else "Cannot reach"
            return f"{prefix} region {self.region_name}"

        @override
        def __str__(self) -> str:
            return f"Can reach region {self.region_name}"


@dataclasses.dataclass()
class CanReachEntrance(Rule[TWorld], game="Archipelago"):
    """A rule that checks if the given entrance is reachable by the current player"""

    entrance_name: str
    """The name of the entrance to test access to"""

    parent_region_name: str = ""
    """The name of the entrance's parent region. If not specified it will be resolved when the rule is resolved"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        parent_region_name = self.parent_region_name
        if not parent_region_name:
            entrance = world.get_entrance(self.entrance_name)
            if not entrance.parent_region:
                raise ValueError(f"Entrance {entrance.name} has no parent region")
            parent_region_name = entrance.parent_region.name
        return self.Resolved(
            self.entrance_name,
            parent_region_name,
            player=world.player,
            caching_enabled=world.rule_caching_enabled,
        )

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.entrance_name}{options})"

    class Resolved(Rule.Resolved):
        entrance_name: str
        parent_region_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.can_reach_entrance(self.entrance_name, self.player)

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            if self.parent_region_name:
                return {self.parent_region_name: {id(self)}}
            return {}

        @override
        def entrance_dependencies(self) -> dict[str, set[int]]:
            return {self.entrance_name: {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                verb = "Can reach"
            elif self(state):
                verb = "Reached"
            else:
                verb = "Cannot reach"
            return [
                {"type": "text", "text": f"{verb} entrance "},
                {"type": "entrance_name", "text": self.entrance_name, "player": self.player},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Reached" if self(state) else "Cannot reach"
            return f"{prefix} entrance {self.entrance_name}"

        @override
        def __str__(self) -> str:
            return f"Can reach entrance {self.entrance_name}"


DEFAULT_RULES = {
    rule_name: cast(type[Rule[RuleWorldMixin]], rule_class)
    for rule_name, rule_class in locals().items()
    if isinstance(rule_class, type) and issubclass(rule_class, Rule) and rule_class is not Rule
}
