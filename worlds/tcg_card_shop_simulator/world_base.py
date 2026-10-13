from rule_builder.cached_world import CachedRuleBuilderWorld
from worlds.AutoWorld import World
from .options import TCGSimulatorOptions



class TCGSimulatorBase(CachedRuleBuilderWorld):
    options_dataclass = TCGSimulatorOptions
    options: TCGSimulatorOptions

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)