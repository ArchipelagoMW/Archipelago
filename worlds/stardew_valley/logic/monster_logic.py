from .combat_logic import CombatLogic
from .region_logic import RegionLogic
from .time_logic import TimeLogic
from .. import StardewOptions
from ..data.monster_data import StardewMonster
from ..stardew_rule import StardewRule


class MonsterLogic:
    player: int
    options: StardewOptions
    region: RegionLogic
    time: TimeLogic
    combat: CombatLogic

    def __init__(self, player: int, options: StardewOptions, region: RegionLogic, time: TimeLogic, combat: CombatLogic):
        self.player = player
        self.options: options
        self.region = region
        self.time = time
        self.combat = combat

    def can_kill(self, monster: StardewMonster, amount_tier: int = 0) -> StardewRule:
        region_rule = self.region.can_reach_any(monster.locations)
        combat_rule = self.combat.can_fight_at_level(monster.difficulty)
        if amount_tier <= 0:
            amount_tier = 0
        time_rule = self.time.has_lived_months(amount_tier * 2)
        return region_rule & combat_rule & time_rule

