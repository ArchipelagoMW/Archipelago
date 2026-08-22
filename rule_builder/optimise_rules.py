"""
Applies some optimisations to Rule Builder rules, by turning them into lambdas, thus reducing call overhead.

In some cases, a lambda cannot be easily constructed, so one of the rule's methods is pre-bound instead, cutting out the
overhead from the method-resolution-order lookup and method-binding steps when calling the rule normally.
"""

from collections.abc import Callable
from typing import Any, TypeAlias

from BaseClasses import DEFAULT_COLLECTION_RULE, CollectionRule, CollectionState, Entrance, Location
from rule_builder.rules import (
    And,
    CanReachEntrance,
    CanReachLocation,
    CanReachRegion,
    False_,
    Has,
    HasAll,
    HasAllCounts,
    HasAny,
    HasAnyCount,
    HasFromList,
    HasFromListUnique,
    HasGroup,
    HasGroupUnique,
    Or,
    Rule,
    True_,
    WrapperRule,
)
from worlds.AutoWorld import World

RuleMemodict: TypeAlias = dict[int, tuple[CollectionRule, CollectionRule]]
OptimiseFunc: TypeAlias = "Callable[[OptimisedRuleBuilderWorldMixin, Rule.Resolved, RuleMemodict], CollectionRule]"
always_true = DEFAULT_COLLECTION_RULE


def always_false(state: CollectionState):
    return False


class OptimisedRuleBuilderWorldMixin(World):
    """A World subclass that provides helpers for interacting with the rule builder.
    Just define your world as `class MyWorld(OptimisedRuleBuilderWorldMixin, World)` and enjoy the speeed.
    """

    debug_rule_builder: bool = False
    """Tells if rules should be optimised or not. Optimising will cut out everything that help understanding the rules,
    but will make the rules run much faster. Set to true if you need, for instance, to use the `explain` methods."""
    resolved_to_optimise: dict[type[Rule.Resolved], OptimiseFunc]
    """You can add custom rules to this if you have any custom rules that can be optimised."""
    _memodict: RuleMemodict
    """Cache for quick access of the rules already optimised."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._memodict = {}
        self.resolved_to_optimise = {
            True_.Resolved: optimise_true,
            False_.Resolved: optimise_false,
            And.Resolved: optimise_and,
            Or.Resolved: optimise_or,
            WrapperRule.Resolved: optimise_wrapper,
            Has.Resolved: optimise_has,
            HasAll.Resolved: optimise_has_all,
            HasAny.Resolved: optimise_has_any,
            HasAllCounts.Resolved: optimise_has_all_counts,
            HasAnyCount.Resolved: optimise_has_any_count,
            HasFromList.Resolved: optimise_has_from_list,
            HasFromListUnique.Resolved: optimise_has_from_list_unique,
            HasGroup.Resolved: optimise_has_group,
            HasGroupUnique.Resolved: optimise_has_group_unique,
            CanReachLocation.Resolved: optimise_can_reach_location,
            CanReachRegion.Resolved: optimise_can_reach_region,
            CanReachEntrance.Resolved: optimise_can_reach_entrance,
        }

    def cleanup_optimisation_cache(self):
        """YOU must call this method at the end of the world `set_rules`."""
        # We can't just override `set_rules`. It would be overridden again by world implementation.
        del self._memodict

    def set_rule(self, spot: Location | Entrance, rule: CollectionRule | Rule[Any]) -> None:
        # We need to call super first so indirect conditions and dependencies are evaluated. Optimise after that.
        super().set_rule(spot, rule)
        if not self.debug_rule_builder:
            optimised = optimise_rule(self, spot.access_rule, self._memodict)
            spot.access_rule = optimised

    def set_completion_rule(self, rule: CollectionRule | Rule[Any]) -> None:
        super().set_completion_rule(rule)
        if not self.debug_rule_builder:
            completion_condition = self.multiworld.completion_condition[self.player]
            optimised = optimise_rule(self, completion_condition, self._memodict)
            self.multiworld.completion_condition[self.player] = optimised


def optimise_true(
    world: OptimisedRuleBuilderWorldMixin, rule: True_.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    return always_true


def optimise_false(
    world: OptimisedRuleBuilderWorldMixin, rule: False_.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    return always_false


def optimise_and(world: OptimisedRuleBuilderWorldMixin, rule: And.Resolved, memodict: RuleMemodict) -> CollectionRule:
    optimised_rules = [optimise_rule(world, r, memodict) for r in rule.children]
    return optimise_and_children(optimised_rules)


def optimise_or(world: OptimisedRuleBuilderWorldMixin, rule: Or.Resolved, memodict: RuleMemodict) -> CollectionRule:
    optimised_rules = [optimise_rule(world, r, memodict) for r in rule.children]
    return optimise_or_children(optimised_rules)


def optimise_wrapper(
    world: OptimisedRuleBuilderWorldMixin, rule: WrapperRule.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    return optimise_rule(world, rule.child, memodict)


def optimise_has(world: OptimisedRuleBuilderWorldMixin, rule: Has.Resolved, memodict: RuleMemodict) -> CollectionRule:
    if rule.count < 1:
        return always_true
    if rule.count == 1:
        return lambda state, p=rule.player, i=rule.item_name: state.prog_items[p][i] >= 1
    return lambda state, p=rule.player, i=rule.item_name, c=rule.count: state.prog_items[p][i] >= c


def optimise_has_all(
    world: OptimisedRuleBuilderWorldMixin, rule: HasAll.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    if len(rule.item_names) <= 1:
        # This should only happen if a world is creating HasAll.Resolved instances manually, instead of using
        # HasAll.resolve().
        return optimise_rule(world, HasAll(*rule.item_names).resolve(world), memodict)

    def optimised(state: CollectionState, p=rule.player, items=rule.item_names):
        player_prog_items = state.prog_items[p]
        for item in items:
            if not player_prog_items[item]:
                return False
        return True

    return optimised


def optimise_has_any(
    world: OptimisedRuleBuilderWorldMixin, rule: HasAny.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    if len(rule.item_names) <= 1:
        # This should only happen if a world is creating HasAny.Resolved instances manually, instead of using
        # HasAny.resolve().
        return optimise_rule(world, HasAny(*rule.item_names).resolve(world), memodict)

    def optimised(state: CollectionState, p=rule.player, items=rule.item_names):
        player_prog_items = state.prog_items[p]
        for item in items:
            if player_prog_items[item]:
                return True
        return False

    return optimised


def optimise_has_all_counts(
    world: OptimisedRuleBuilderWorldMixin, rule: HasAllCounts.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    if len(rule.item_counts) <= 1:
        # This should only happen if a world is creating HasAllCounts.Resolved instances manually, instead of using
        # HasAllCounts.resolve().
        return optimise_rule(world, HasAllCounts(dict(rule.item_counts)).resolve(world), memodict)

    original_counts = dict(rule.item_counts)
    cleaned_counts = {}

    single_counts = []
    multi_counts = {}
    for item, count in rule.item_counts:
        if count < 1:
            continue
        if count == 1:
            single_counts.append(item)
        else:
            multi_counts[item] = count
        cleaned_counts[item] = count
    if cleaned_counts != original_counts:
        # Re-optimise with the cleaned counts.
        return optimise_rule(world, HasAllCounts(cleaned_counts).resolve(world), memodict)

    if single_counts:
        if not multi_counts:
            return optimise_rule(world, HasAll(*single_counts).resolve(world), memodict)

        def optimised(
            state: CollectionState,
            p=rule.player,
            item_counts=tuple(multi_counts.items()),  # noqa: B008
            single_items=tuple(single_counts),
        ):
            player_prog_items = state.prog_items[p]
            for item in single_items:
                if not player_prog_items[item]:
                    return False
            for item, count in item_counts:
                if player_prog_items[item] < count:
                    return False
            return True
    else:
        assert multi_counts, "Unreachable: No single_counts and no multi_counts"
        if len(set(multi_counts.values())) == 1:
            # All counts are the same.
            def optimised(
                state: CollectionState,
                p=rule.player,
                items=tuple(multi_counts),
                c=next(iter(multi_counts.values())),  # noqa: B008
            ):
                player_prog_items = state.prog_items[p]
                for item in items:
                    if player_prog_items[item] < c:
                        return False
                return True
        else:

            def optimised(
                state: CollectionState,
                p=rule.player,
                item_counts=tuple(multi_counts.items()),  # noqa: B008
            ):
                player_prog_items = state.prog_items[p]
                for item, count in item_counts:
                    if player_prog_items[item] < count:
                        return False
                return True

    return optimised


def optimise_has_any_count(
    world: OptimisedRuleBuilderWorldMixin, rule: HasAnyCount.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    if len(rule.item_counts) <= 1:
        # This should only happen if a world is creating HasAnyCount.Resolved instances manually, instead of using
        # HasAnyCount.resolve().
        return optimise_rule(world, HasAnyCount(dict(rule.item_counts)).resolve(world), memodict)

    original_counts = dict(rule.item_counts)
    cleaned_counts = {}

    single_counts = []
    multi_counts = {}
    for item, count in rule.item_counts:
        if count < 1:
            continue
        if count == 1:
            single_counts.append(item)
        else:
            multi_counts[item] = count
        cleaned_counts[item] = count
    if cleaned_counts != original_counts:
        # Re-optimise with the cleaned counts.
        return optimise_rule(world, HasAnyCount(cleaned_counts).resolve(world), memodict)

    if single_counts:
        if not multi_counts:
            return optimise_rule(world, HasAny(*single_counts).resolve(world), memodict)

        def optimised(
            state: CollectionState,
            p=rule.player,
            item_counts=tuple(multi_counts.items()),  # noqa: B008
            single_items=tuple(single_counts),
        ):
            player_prog_items = state.prog_items[p]
            for item in single_items:
                if player_prog_items[item]:
                    return True
            for item, count in item_counts:
                if player_prog_items[item] >= count:
                    return True
            return False
    else:
        assert multi_counts, "Unreachable: No single_counts and no multi_counts"
        if len(set(multi_counts.values())) == 1:
            # All counts are the same.
            def optimised(
                state: CollectionState,
                p=rule.player,
                items=tuple(multi_counts),
                c=next(iter(multi_counts.values())),  # noqa: B008
            ):
                player_prog_items = state.prog_items[p]
                for item in items:
                    if player_prog_items[item] >= c:
                        return True
                return False
        else:

            def optimised(
                state: CollectionState,
                p=rule.player,
                item_counts=tuple(multi_counts.items()),  # noqa: B008
            ):
                player_prog_items = state.prog_items[p]
                for item, count in item_counts:
                    if player_prog_items[item] >= count:
                        return True
                return False

    return optimised


def optimise_has_from_list(
    world: OptimisedRuleBuilderWorldMixin, rule: HasFromList.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    if len(rule.item_names) <= 1:
        # This should only happen if a world is creating HasFromList.Resolved instances manually, instead of using
        # HasFromList.resolve().
        return optimise_rule(world, HasFromList(*rule.item_names, count=rule.count).resolve(world), memodict)

    if rule.count > 1:

        def optimised(state: CollectionState, p=rule.player, items=rule.item_names, c=rule.count):
            found = 0
            player_prog_items = state.prog_items[p]
            for item_name in items:
                found += player_prog_items[item_name]
                if found >= c:
                    return True
            return False
    else:

        def optimised(state: CollectionState, p=rule.player, items=rule.item_names):
            found = 0
            player_prog_items = state.prog_items[p]
            for item_name in items:
                found += player_prog_items[item_name]
                if found >= 1:
                    return True
            return False

    return optimised


def optimise_has_from_list_unique(
    world: OptimisedRuleBuilderWorldMixin, rule: HasFromListUnique.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    if len(rule.item_names) <= 1 or len(rule.item_names) < rule.count:
        # This should only happen if a world is creating HasFromList.Resolved instances manually, instead of using
        # HasFromList.resolve().
        return optimise_rule(world, HasFromListUnique(*rule.item_names, count=rule.count).resolve(world), memodict)

    if rule.count == len(rule.item_names):
        return optimise_rule(world, HasAll(*rule.item_names).resolve(world), memodict)

    if rule.count == 1:
        return optimise_rule(world, HasAny(*rule.item_names).resolve(world), memodict)

    def optimised(state: CollectionState, p=rule.player, items=rule.item_names, c=rule.count):
        found = 0
        player_prog_items = state.prog_items[p]
        for item_name in items:
            found += player_prog_items[item_name] > 0
            if found >= c:
                return True
        return False

    return optimised


def optimise_has_group(
    world: OptimisedRuleBuilderWorldMixin, rule: HasGroup.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    # HasGroup is just HasFromList with nicer rule explanations.
    return optimise_rule(world, HasFromList(*rule.item_names, count=rule.count).resolve(world), memodict)


def optimise_has_group_unique(
    world: OptimisedRuleBuilderWorldMixin, rule: HasGroupUnique.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    # HasGroupUnique is just HasFromListUnique with nicer rule explanations.
    return optimise_rule(world, HasFromListUnique(*rule.item_names, count=rule.count).resolve(world), memodict)


def optimise_can_reach_location(
    world: OptimisedRuleBuilderWorldMixin, rule: CanReachLocation.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    rule_world = world.multiworld.worlds[rule.player]
    location = rule_world.get_location(rule.location_name)
    return location.can_reach


def optimise_can_reach_region(
    world: OptimisedRuleBuilderWorldMixin, rule: CanReachRegion.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    rule_world = world.multiworld.worlds[rule.player]
    region = rule_world.get_region(rule.region_name)
    return region.can_reach


def optimise_can_reach_entrance(
    world: OptimisedRuleBuilderWorldMixin, rule: CanReachEntrance.Resolved, memodict: RuleMemodict
) -> CollectionRule:
    rule_world = world.multiworld.worlds[rule.player]
    entrance = rule_world.get_entrance(rule.entrance_name)
    return entrance.can_reach


def optimise_rule(world: OptimisedRuleBuilderWorldMixin, rule: CollectionRule | Rule.Resolved, memodict: RuleMemodict):
    t = memodict.get(id(rule))
    if t is not None:
        return t[0]
    rule_type = type(rule)
    if not isinstance(rule, Rule.Resolved):
        # The rule is not a Rule Builder rule.
        optimised = rule
    elif rule.always_true:
        optimised = always_true
    elif rule.always_false:
        optimised = always_false
    elif rule_type.__call__ is not Rule.Resolved.__call__:
        # If __call__ is overridden, optimisation is not possible beyond pre-binding the method.
        optimised = rule.__call__
    elif rule.caching_enabled:
        # Trying to optimise when caching is enabled would be more complex, so just pre-bind the _evaluate/__call__
        # method instead.
        optimised = rule.__call__
    elif rule_type in world.resolved_to_optimise:
        optimised = world.resolved_to_optimise[rule_type](world, rule, memodict)
    # WrapperRules are more likely to be subclassed, so check for subclasses also.
    elif isinstance(rule, WrapperRule.Resolved) and rule_type._evaluate is WrapperRule.Resolved._evaluate:
        rule: WrapperRule.Resolved
        optimised = optimise_rule(world, rule.child, memodict)
    else:
        # The rule is not a supported type for optimisation, but caching is disabled and __call__ is default, so the
        # best that can be done is pre-binding the _evaluate method.
        optimised = rule._evaluate
    # The original rule is also stored to ensure that it is not garbage collected for the lifetime of the memodict,
    # ensuring that the id() key remains valid.
    memodict[id(optimised)] = optimised, rule
    return optimised


def optimise_and_children(children: list[CollectionRule]) -> CollectionRule:
    if len(children) == 0:
        return always_true

    # ~68% of the duration of a loop.
    if len(children) == 1:
        return children[0]

    # ~72% of the duration of a loop.
    if len(children) == 2:
        return lambda state, a=children[0], b=children[1]: a(state) and b(state)

    # ~90% of the duration of a loop from here on.
    if len(children) == 3:
        return lambda state, a=children[0], b=children[1], c=children[2]: a(state) and b(state) and c(state)

    if len(children) == 4:
        return lambda state, a=children[0], b=children[1], c=children[2], d=children[3]: (
            a(state) and b(state) and c(state) and d(state)
        )

    if len(children) == 5:
        return lambda state, a=children[0], b=children[1], c=children[2], d=children[3], e=children[4]: (
            a(state) and b(state) and c(state) and d(state) and e(state)
        )

    if len(children) == 6:
        return lambda state, a=children[0], b=children[1], c=children[2], d=children[3], e=children[4], f=children[5]: (
            a(state) and b(state) and c(state) and d(state) and e(state) and f(state)
        )

    def loop_rule(state, rules=tuple(children)):
        for rule in rules:
            if not rule(state):
                return False
        return True

    return loop_rule


def optimise_or_children(children: list[CollectionRule]) -> CollectionRule:
    if len(children) == 0:
        return always_false

    # ~68% of the duration of a loop.
    if len(children) == 1:
        return children[0]

    # ~72% of the duration of a loop.
    if len(children) == 2:
        return lambda state, a=children[0], b=children[1]: a(state) or b(state)

    # ~90% of the duration of a loop from here on.
    if len(children) == 3:
        return lambda state, a=children[0], b=children[1], c=children[2]: a(state) or b(state) or c(state)

    if len(children) == 4:
        return lambda state, a=children[0], b=children[1], c=children[2], d=children[3]: (
            a(state) or b(state) or c(state) or d(state)
        )

    if len(children) == 5:
        return lambda state, a=children[0], b=children[1], c=children[2], d=children[3], e=children[4]: (
            a(state) or b(state) or c(state) or d(state) or e(state)
        )

    if len(children) == 6:
        return lambda state, a=children[0], b=children[1], c=children[2], d=children[3], e=children[4], f=children[5]: (
            a(state) or b(state) or c(state) or d(state) or e(state) or f(state)
        )

    def loop_rule(state, rules=tuple(children)):
        for rule in rules:
            if rule(state):
                return True
        return False

    return loop_rule
