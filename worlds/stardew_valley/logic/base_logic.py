from __future__ import annotations

import typing
from typing import Dict, Collection

from ..content.game_content import StardewContent
from ..options import StardewValleyOptions
from ..stardew_rule import StardewRule

if typing.TYPE_CHECKING:
    from .logic import StardewLogic


class LogicRegistry:

    def __init__(self):
        self.item_rules: Dict[str, StardewRule] = {}
        self.seed_rules: Dict[str, StardewRule] = {}
        self.cooking_rules: Dict[str, StardewRule] = {}
        self.crafting_rules: Dict[str, StardewRule] = {}
        self.crop_rules: Dict[str, StardewRule] = {}
        self.artisan_good_rules: Dict[str, StardewRule] = {}
        self.fish_rules: Dict[str, StardewRule] = {}
        self.museum_rules: Dict[str, StardewRule] = {}
        self.festival_rules: Dict[str, StardewRule] = {}
        self.quest_rules: Dict[str, StardewRule] = {}
        self.special_order_rules: Dict[str, StardewRule] = {}

        self.sve_location_rules: Dict[str, StardewRule] = {}


class BaseLogicMixin:
    def __init__(self, *args, **kwargs):
        pass


class BaseLogic(BaseLogicMixin):
    player: int
    registry: LogicRegistry
    options: StardewValleyOptions
    content: StardewContent
    regions: Collection[str]
    logic: StardewLogic

    def __init__(self, player: int, registry: LogicRegistry, options: StardewValleyOptions, content: StardewContent, regions: Collection[str],
                 logic: StardewLogic):
        super().__init__(player, registry, options, content, regions, logic)
        self.player = player
        self.registry = registry
        self.options = options
        self.content = content
        self.regions = regions
        self.logic = logic
