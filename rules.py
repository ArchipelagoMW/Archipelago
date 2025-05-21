import dataclasses
import itertools
import operator
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from Options import CommonOptions, Option
    from worlds.AutoWorld import World

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
    options: dict[str, Any] = dataclasses.field(default_factory=dict, kw_only=True)
    """A mapping of option_name to value"""

    def _passes_options(self, options: "CommonOptions") -> bool:
        for key, value in self.options:
            parts = key.split("__", maxsplit=1)
            option_name = parts[0]
            operator = parts[1] if len(parts) > 1 else "eq"
            opt: Option = getattr(options, option_name)
            if not OPERATORS[operator](opt.value, value):
                return False
        return True

    def _instantiate(self, world: "World") -> "Instance":
        return self.Instance(player=world.player)

    def resolve(self, world: "World") -> "Instance":
        if not self._passes_options(world.options):
            return False_.Instance(player=world.player)

        instance = self._instantiate(world)
        rule_hash = hash(instance)
        if rule_hash not in world.rule_cache:
            world.rule_cache[rule_hash] = instance
        return world.rule_cache[rule_hash]

    @dataclasses.dataclass(kw_only=True, frozen=True)
    class Instance:
        player: int
        cacheable: bool = dataclasses.field(repr=False, default=True)

        always_true: ClassVar = False
        always_false: ClassVar = False

        def __hash__(self) -> int:
            return hash((self.__class__.__name__, *[getattr(self, f.name) for f in dataclasses.fields(self)]))

        def _evaluate(self, state: "CollectionState") -> bool: ...

        def evaluate(self, state: "CollectionState") -> bool:
            result = self._evaluate(state)
            if self.cacheable:
                state._astalon_rule_results[self.player][id(self)] = result  # type: ignore
            return result

        def test(self, state: "CollectionState") -> bool:
            cached_result = None
            if self.cacheable:
                cached_result = state._astalon_rule_results[self.player].get(id(self))  # type: ignore
            if cached_result is not None:
                return cached_result
            return self.evaluate(state)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {}

        def indirect_regions(self) -> tuple[str, ...]:
            return ()


@dataclasses.dataclass()
class True_(Rule):
    @dataclasses.dataclass(frozen=True)
    class Instance(Rule.Instance):
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)
        always_true = True

        def _evaluate(self, state: "CollectionState") -> bool:
            return True


@dataclasses.dataclass()
class False_(Rule):
    @dataclasses.dataclass(frozen=True)
    class Instance(Rule.Instance):
        cacheable: bool = dataclasses.field(repr=False, default=False, init=False)
        always_false = True

        def _evaluate(self, state: "CollectionState") -> bool:
            return False


@dataclasses.dataclass(init=False)
class NestedRule(Rule):
    children: "tuple[Rule, ...]"

    def __init__(self, *children: "Rule", options: dict[str, Any] | None = None) -> None:
        super().__init__(options=options or {})
        self.children = children

    def _instantiate(self, world: "World") -> "Instance":
        children = [c.resolve(world) for c in self.children]
        return self.Instance(tuple(children), player=world.player).simplify()  # type: ignore

    @dataclasses.dataclass(frozen=True)
    class Instance(Rule.Instance):
        children: "tuple[Rule.Instance, ...]"

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

        def simplify(self) -> "Rule.Instance":
            return self


@dataclasses.dataclass(init=False)
class And(NestedRule):
    @dataclasses.dataclass(frozen=True)
    class Instance(NestedRule.Instance):
        def _evaluate(self, state: "CollectionState") -> bool:
            for rule in self.children:
                if not rule.test(state):
                    return False
            return True

        def simplify(self) -> "Rule.Instance":
            children_to_process = list(self.children)
            clauses: list[Rule.Instance] = []
            items: list[str] = []
            true_rule: Rule.Instance | None = None

            while children_to_process:
                child = children_to_process.pop(0)
                if child.always_false:
                    # false always wins
                    return child
                if child.always_true:
                    # dedupe trues
                    true_rule = child
                    continue
                if isinstance(child, And.Instance):
                    children_to_process.extend(child.children)
                    continue

                if isinstance(child, Has.Instance) and child.count == 1:
                    items.append(child.item)
                elif isinstance(child, HasAll.Instance):
                    items.extend(child.items)
                else:
                    clauses.append(child)

            if not clauses and not items:
                return true_rule or False_.Instance(player=self.player)
            if items:
                if len(items) == 1:
                    item_rule = Has.Instance(items[0], player=self.player)
                else:
                    item_rule = HasAll.Instance(tuple(items), player=self.player)
                if not clauses:
                    return item_rule
                clauses.append(item_rule)

            if len(clauses) == 1:
                return clauses[0]
            return And.Instance(
                tuple(clauses),
                player=self.player,
                cacheable=self.cacheable and all(c.cacheable for c in clauses),
            )


@dataclasses.dataclass(init=False)
class Or(NestedRule):
    @dataclasses.dataclass(frozen=True)
    class Instance(NestedRule.Instance):
        def _evaluate(self, state: "CollectionState") -> bool:
            for rule in self.children:
                if rule.test(state):
                    return True
            return False

        def simplify(self) -> "Rule.Instance":
            children_to_process = list(self.children)
            clauses: list[Rule.Instance] = []
            items: list[str] = []

            while children_to_process:
                child = children_to_process.pop(0)
                if child.always_true:
                    # true always wins
                    return child
                if child.always_false:
                    # falses can be ignored
                    continue
                if isinstance(child, Or.Instance):
                    children_to_process.extend(child.children)
                    continue

                if isinstance(child, Has.Instance) and child.count == 1:
                    items.append(child.item)
                elif isinstance(child, HasAny.Instance):
                    items.extend(child.items)
                else:
                    clauses.append(child)

            if not clauses and not items:
                return False_.Instance(player=self.player)
            if items:
                if len(items) == 1:
                    item_rule = Has.Instance(items[0], player=self.player)
                else:
                    item_rule = HasAny.Instance(tuple(items), player=self.player)
                if not clauses:
                    return item_rule
                clauses.append(item_rule)

            if len(clauses) == 1:
                return clauses[0]
            return Or.Instance(
                tuple(clauses),
                player=self.player,
                cacheable=self.cacheable and all(c.cacheable for c in clauses),
            )


@dataclasses.dataclass()
class Has(Rule):
    item: str
    count: int = 1

    @dataclasses.dataclass(frozen=True)
    class Instance(Rule.Instance):
        item: str
        count: int = 1

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has(self.item, self.player, count=self.count)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item: {id(self)}}


@dataclasses.dataclass()
class HasAll(Rule):
    items: tuple[str, ...]

    @dataclasses.dataclass(frozen=True)
    class Instance(Rule.Instance):
        items: tuple[str, ...]

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has_all(self.items, self.player)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.items}


@dataclasses.dataclass()
class HasAny(Rule):
    items: tuple[str, ...]

    @dataclasses.dataclass(frozen=True)
    class Instance(Rule.Instance):
        items: tuple[str, ...]

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has_any(self.items, self.player)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in self.items}
