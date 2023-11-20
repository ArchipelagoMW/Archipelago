from __future__ import annotations

from typing import TypeVar, Generic

from ..options import StardewValleyOptions


class LogicRegistry:

    def __init__(self):
        self.item_rules = {}
        self.sapling_rules = {}
        self.tree_fruit_rules = {}
        self.seed_rules = {}
        self.cooking_rules = {}
        self.crafting_rules = {}
        self.crop_rules = {}
        self.fish_rules = {}
        self.museum_rules = {}
        self.festival_rules = {}
        self.quest_rules = {}
        self.building_rules = {}


class BaseLogicMixin:
    def __init__(self, *args, **kwargs):
        pass


T = TypeVar("T", bound=BaseLogicMixin)


class BaseLogic(BaseLogicMixin, Generic[T]):
    player: int
    registry: LogicRegistry
    options: StardewValleyOptions
    logic: T

    def __init__(self, player: int, registry: LogicRegistry, options: StardewValleyOptions, logic: T):
        super().__init__(player, registry, options, logic)
        self.player = player
        self.registry = registry
        self.options = options
        self.logic = logic
