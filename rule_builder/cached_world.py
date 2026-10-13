from collections import defaultdict
from typing import ClassVar, cast

from typing_extensions import override

from BaseClasses import CollectionState, Item, MultiWorld, Region
from worlds.AutoWorld import LogicMixin, World

from .rules import Rule


class CachedRuleBuilderWorld(World):
    """A World subclass that provides helpers for interacting with the rule builder"""

    rule_item_dependencies: dict[str, set[int]]
    """A mapping of item name to set of rule ids"""

    rule_region_dependencies: dict[str, set[int]]
    """A mapping of region name to set of rule ids"""

    rule_location_dependencies: dict[str, set[int]]
    """A mapping of location name to set of rule ids"""

    rule_entrance_dependencies: dict[str, set[int]]
    """A mapping of entrance name to set of rule ids"""

    item_mapping: ClassVar[dict[str, str]] = {}
    """A mapping of actual item name to logical item name.
    Useful when there are multiple versions of a collected item but the logic only uses one. For example:
    item = Item("Currency x500"), rule = Has("Currency", count=1000), item_mapping = {"Currency x500": "Currency"}"""

    rule_caching_enabled: ClassVar[bool] = True
    """Flag to inform rules that the caching system for this world is enabled. It should not be overridden."""

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld, player)
        self.rule_item_dependencies = defaultdict(set)
        self.rule_region_dependencies = defaultdict(set)
        self.rule_location_dependencies = defaultdict(set)
        self.rule_entrance_dependencies = defaultdict(set)

    @override
    def register_rule_dependencies(self, resolved_rule: Rule.Resolved) -> None:
        for item_name, rule_ids in resolved_rule.item_dependencies().items():
            self.rule_item_dependencies[item_name] |= rule_ids
        for region_name, rule_ids in resolved_rule.region_dependencies().items():
            self.rule_region_dependencies[region_name] |= rule_ids
        for location_name, rule_ids in resolved_rule.location_dependencies().items():
            self.rule_location_dependencies[location_name] |= rule_ids
        for entrance_name, rule_ids in resolved_rule.entrance_dependencies().items():
            self.rule_entrance_dependencies[entrance_name] |= rule_ids

    def register_rule_builder_dependencies(self) -> None:
        """Register all rules that depend on locations or entrances with their dependencies"""
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

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if changed and self.rule_item_dependencies:
            player_results = cast(dict[int, bool], state.rule_builder_cache[self.player])  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            mapped_name = self.item_mapping.get(item.name, "")
            rule_ids = self.rule_item_dependencies[item.name] | self.rule_item_dependencies[mapped_name]
            for rule_id in rule_ids:
                if player_results.get(rule_id, None) is False:
                    del player_results[rule_id]

        return changed

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if not changed:
            return changed

        player_results = cast(dict[int, bool], state.rule_builder_cache[self.player])  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
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
        if self.rule_region_dependencies:
            player_results = cast(dict[int, bool], state.rule_builder_cache[self.player])  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            for rule_id in self.rule_region_dependencies[region.name]:
                player_results.pop(rule_id, None)


class CachedRuleBuilderLogicMixin(LogicMixin):
    multiworld: MultiWorld  # pyright: ignore[reportUninitializedInstanceVariable]
    rule_builder_cache: dict[int, dict[int, bool]]  # pyright: ignore[reportUninitializedInstanceVariable]

    def init_mixin(self, multiworld: "MultiWorld") -> None:
        players = multiworld.get_all_ids()
        self.rule_builder_cache = {player: {} for player in players}

    def copy_mixin(self, new_state: "CachedRuleBuilderLogicMixin") -> "CachedRuleBuilderLogicMixin":
        new_state.rule_builder_cache = {
            player: player_results.copy() for player, player_results in self.rule_builder_cache.items()
        }
        return new_state
