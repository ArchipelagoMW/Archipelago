import dataclasses
from collections.abc import Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Final, Generic, Never, Self, cast

from typing_extensions import TypeVar, dataclass_transform, override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart

from .options import OptionFilter

if TYPE_CHECKING:
    from worlds.AutoWorld import World

    TWorld = TypeVar("TWorld", bound=World, contravariant=True, default=World)  # noqa: PLC0105
else:
    TWorld = TypeVar("TWorld")


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

    resolved_rules: ClassVar[dict[int, "Rule.Resolved"]] = {}
    """A cached of resolved rules to turn each unique one into a singleton"""

    custom_rules: ClassVar[dict[str, dict[str, type["Rule[Any]"]]]] = {}
    """A mapping of game name to mapping of rule name to rule class to hold custom rules implemented by worlds"""

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

    @override
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        rule = super().__call__(*args, **kwds)
        rule_hash = hash(rule)
        if rule_hash in cls.resolved_rules:
            return cls.resolved_rules[rule_hash]
        cls.resolved_rules[rule_hash] = rule
        return rule

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

    options: Iterable[OptionFilter] = dataclasses.field(default=(), kw_only=True)
    """An iterable of OptionFilters to restrict what options are required for this rule to be active"""

    filtered_resolution: bool = dataclasses.field(default=False, kw_only=True)
    """If this rule should default to True or False when filtered by its options"""

    game_name: ClassVar[str]
    """The name of the game this rule belongs to, default rules belong to 'Archipelago'"""

    def __post_init__(self) -> None:
        if not isinstance(self.options, tuple):
            self.options = tuple(self.options)

    def _instantiate(self, world: TWorld) -> "Resolved":
        """Create a new resolved rule for this world"""
        return self.Resolved(player=world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    def resolve(self, world: TWorld) -> "Resolved":
        """Resolve a rule with the given world"""
        for option_filter in self.options:
            if not option_filter.check(world.options):
                return True_().resolve(world) if self.filtered_resolution else False_().resolve(world)
        return self._instantiate(world)

    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this rule"""
        args = {
            field.name: getattr(self, field.name, None)
            for field in dataclasses.fields(self)
            if field.name not in ("options", "filtered_resolution")
        }
        return {
            "rule": self.__class__.__qualname__,
            "options": [o.to_dict() for o in self.options],
            "filtered_resolution": self.filtered_resolution,
            "args": args,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        """Returns a new instance of this rule from a serialized dict representation"""
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(**data.get("args", {}), options=options, filtered_resolution=data.get("filtered_resolution", False))

    def __and__(self, other: "Rule[Any] | Iterable[OptionFilter] | OptionFilter") -> "Rule[TWorld]":
        """Combines two rules or a rule and an option filter into an And rule"""
        if isinstance(other, OptionFilter):
            other = (other,)
        if isinstance(other, Iterable):
            if not other:
                return self
            return Filtered(self, options=other)
        if self.options == other.options:
            if isinstance(self, And):
                if isinstance(other, And):
                    return And(*self.children, *other.children, options=self.options)
                return And(*self.children, other, options=self.options)
            if isinstance(other, And):
                return And(self, *other.children, options=other.options)
        return And(self, other)

    def __rand__(self, other: "Rule[Any] | Iterable[OptionFilter] | OptionFilter") -> "Rule[TWorld]":
        return self.__and__(other)

    def __or__(self, other: "Rule[Any] | Iterable[OptionFilter] | OptionFilter") -> "Rule[TWorld]":
        """Combines two rules or a rule and an option filter into an Or rule"""
        if isinstance(other, OptionFilter):
            other = (other,)
        if isinstance(other, Iterable):
            if not other:
                return self
            return Or(self, True_(options=other))
        if self.options == other.options:
            if isinstance(self, Or):
                if isinstance(other, Or):
                    return Or(*self.children, *other.children, options=self.options)
                return Or(*self.children, other, options=self.options)
            if isinstance(other, Or):
                return Or(self, *other.children, options=self.options)
        return Or(self, other)

    def __ror__(self, other: "Rule[Any] | Iterable[OptionFilter] | OptionFilter") -> "Rule[TWorld]":
        return self.__or__(other)

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
        elif cls.__module__ != "rule_builder.rules":
            raise TypeError("You cannot define custom rules for the base Archipelago world")
        cls.game_name = game

    class Resolved(metaclass=CustomRuleRegister):
        """A resolved rule for a given world that can be used as an access rule"""

        _: dataclasses.KW_ONLY

        player: int
        """The player this rule is for"""

        caching_enabled: bool = dataclasses.field(repr=False, default=False, kw_only=True)
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

            player_results = cast(dict[int, bool], state.rule_builder_cache[self.player])  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            cached_result = player_results.get(id(self))
            if cached_result is not None:
                return cached_result

            result = self._evaluate(state)
            player_results[id(self)] = result
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
    """A base rule class that takes an iterable of other rules as an argument and does logic based on them"""

    children: tuple[Rule[TWorld], ...]
    """The child rules this rule's logic is based on"""

    def __init__(
        self,
        *children: Rule[TWorld],
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.children = children

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        children = [c.resolve(world) for c in self.children]
        return self.Resolved(
            tuple(children),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data["args"]
        data["children"] = [c.to_dict() for c in self.children]
        return data

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        children = [world_cls.rule_from_dict(c) for c in data.get("children", ())]
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*children, options=options, filtered_resolution=data.get("filtered_resolution", False))

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

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        children_to_process = [c.resolve(world) for c in self.children]
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
            elif isinstance(child, HasAllCounts.Resolved):
                for item, count in child.item_counts:
                    if item not in items or items[item] < count:
                        items[item] = count
            else:
                clauses.append(child)

        if not clauses and not items:
            return true_rule or False_().resolve(world)

        if len(items) == 1:
            item, count = next(iter(items.items()))
            clauses.append(Has(item, count).resolve(world))
        elif items and all(count == 1 for count in items.values()):
            clauses.append(HasAll(*items).resolve(world))
        elif items:
            clauses.append(HasAllCounts(items).resolve(world))

        if len(clauses) == 1:
            return clauses[0]

        return And.Resolved(
            tuple(clauses),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

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

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        children_to_process = [c.resolve(world) for c in self.children]
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
            elif isinstance(child, HasAnyCount.Resolved):
                for item, count in child.item_counts:
                    if item not in items or items[item] < count:
                        items[item] = count
            else:
                clauses.append(child)

        if not clauses and not items:
            return False_().resolve(world)

        if len(items) == 1:
            item, count = next(iter(items.items()))
            clauses.append(Has(item, count).resolve(world))
        elif items and all(count == 1 for count in items.values()):
            clauses.append(HasAny(*items).resolve(world))
        elif items:
            clauses.append(HasAnyCount(items).resolve(world))

        if len(clauses) == 1:
            return clauses[0]

        return Or.Resolved(
            tuple(clauses),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

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
class WrapperRule(Rule[TWorld], game="Archipelago"):
    """A base rule class that wraps another rule to provide extra logic or data"""

    child: Rule[TWorld]
    """The child rule being wrapped"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(
            self.child.resolve(world),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data["args"]
        data["child"] = self.child.to_dict()
        return data

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        child = data.get("child")
        if child is None:
            raise ValueError("Child rule cannot be None")
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(
            world_cls.rule_from_dict(child),
            options=options,
            filtered_resolution=data.get("filtered_resolution", False),
        )

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
class Filtered(WrapperRule[TWorld], game="Archipelago"):
    """A convenience rule to wrap an existing rule with an options filter"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.child.resolve(world)


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
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "color", "color": color, "text": self.item_name})
            else:
                messages.append({"type": "item_name", "flags": 0b001, "text": self.item_name, "player": self.player})
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

    def __init__(
        self,
        *item_names: str,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.item_names = tuple(sorted(set(item_names)))

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0:
            # match state.has_all
            return True_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(
            self.item_names,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options, filtered_resolution=data.get("filtered_resolution", False))

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
                    messages.append({"type": "color", "color": "green", "text": item})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": item})
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

    def __init__(
        self,
        *item_names: str,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.item_names = tuple(sorted(set(item_names)))

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0:
            # match state.has_any
            return False_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(
            self.item_names,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options, filtered_resolution=data.get("filtered_resolution", False))

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
                    messages.append({"type": "color", "color": "green", "text": item})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": item})
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
            return True_().resolve(world)
        if len(self.item_counts) == 1:
            item = next(iter(self.item_counts))
            return Has(item, self.item_counts[item]).resolve(world)
        return self.Resolved(
            tuple(self.item_counts.items()),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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
                    messages.append({"type": "color", "color": "green", "text": item})
                    messages.append({"type": "text", "text": f" x{count}"})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, (item, count) in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": item})
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
            return False_().resolve(world)
        if len(self.item_counts) == 1:
            item = next(iter(self.item_counts))
            return Has(item, self.item_counts[item]).resolve(world)
        return self.Resolved(
            tuple(self.item_counts.items()),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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
                    messages.append({"type": "color", "color": "green", "text": item})
                    messages.append({"type": "text", "text": f" x{count}"})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, (item, count) in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": item})
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

    def __init__(
        self,
        *item_names: str,
        count: int = 1,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.item_names = tuple(sorted(set(item_names)))
        self.count = count

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0:
            # match state.has_from_list
            return False_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0], self.count).resolve(world)
        return self.Resolved(
            self.item_names,
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options, filtered_resolution=data.get("filtered_resolution", False))

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
            color = "green" if found_count >= self.count else "salmon"
            messages = [
                {"type": "text", "text": "Has "},
                {
                    "type": "color",
                    "color": color,
                    "text": f"{found_count}/{self.count}",
                },
                {"type": "text", "text": " items from ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, item in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "green", "text": item})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": item})
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

    def __init__(
        self,
        *item_names: str,
        count: int = 1,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.item_names = tuple(sorted(set(item_names)))
        self.count = count

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if len(self.item_names) == 0 or len(self.item_names) < self.count:
            # match state.has_from_list_unique
            return False_().resolve(world)
        if len(self.item_names) == 1:
            return Has(self.item_names[0]).resolve(world)
        return self.Resolved(
            self.item_names,
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        args = {**data.get("args", {})}
        item_names = args.pop("item_names", ())
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        return cls(*item_names, **args, options=options, filtered_resolution=data.get("filtered_resolution", False))

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
            color = "green" if found_count >= self.count else "salmon"
            messages = [
                {"type": "text", "text": "Has "},
                {"type": "color", "color": color, "text": f"{found_count}/{self.count}"},
                {"type": "text", "text": " unique items from ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, item in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "green", "text": item})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, item in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": item})
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
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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
        return self.Resolved(
            self.region_name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

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
            caching_enabled=getattr(world, "rule_caching_enabled", False),
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


DEFAULT_RULES: "Final[dict[str, type[Rule[World]]]]" = {
    rule_name: cast("type[Rule[World]]", rule_class)
    for rule_name, rule_class in locals().items()
    if isinstance(rule_class, type) and issubclass(rule_class, Rule) and rule_class is not Rule
}
