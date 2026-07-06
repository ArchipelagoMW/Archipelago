from rule_builder.cached_world import CachedRuleBuilderWorld
from . import PotionCraftOptions

class PotionCraftBase(CachedRuleBuilderWorld):
    options_dataclass = PotionCraftOptions
    options: PotionCraftOptions

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)