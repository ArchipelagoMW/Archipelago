from dataclasses import dataclass, field
from typing import Dict

from ..options import StardewValleyOptions
from ..stardew_rule import StardewRule


@dataclass(frozen=False)
class LogicRegistry:
    player: int
    options: StardewValleyOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    sapling_rules: Dict[str, StardewRule] = field(default_factory=dict)
    tree_fruit_rules: Dict[str, StardewRule] = field(default_factory=dict)
    seed_rules: Dict[str, StardewRule] = field(default_factory=dict)
    cooking_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crafting_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crop_rules: Dict[str, StardewRule] = field(default_factory=dict)
    fish_rules: Dict[str, StardewRule] = field(default_factory=dict)
    museum_rules: Dict[str, StardewRule] = field(default_factory=dict)
    festival_rules: Dict[str, StardewRule] = field(default_factory=dict)
    quest_rules: Dict[str, StardewRule] = field(default_factory=dict)


class BaseLogic:
    player: int
    registry: LogicRegistry

    def __init__(self, player: int, registry: LogicRegistry):
        self.player = player
        self.registry = registry
