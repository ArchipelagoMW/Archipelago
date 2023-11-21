from typing import Iterable, Union, Hashable

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .combat_logic import CombatLogicMixin
from .region_logic import RegionLogicMixin
from .time_logic import TimeLogicMixin, MAX_MONTHS
from ..data.monster_data import StardewMonster, all_monsters_by_name
from ..stardew_rule import StardewRule, Or, And


class MonsterLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monster = MonsterLogic(*args, **kwargs)


class MonsterLogic(BaseLogic[Union[MonsterLogicMixin, RegionLogicMixin, CombatLogicMixin, TimeLogicMixin]]):
    def can_kill(self, monster: Union[str, StardewMonster], amount_tier: int = 0) -> StardewRule:
        if isinstance(monster, str):
            monster = all_monsters_by_name[monster]
        region_rule = self.logic.region.can_reach_any(monster.locations)
        combat_rule = self.logic.combat.can_fight_at_level(monster.difficulty)
        if amount_tier <= 0:
            amount_tier = 0
        time_rule = self.logic.time.has_lived_months(amount_tier * 2)
        return region_rule & combat_rule & time_rule

    @cache_self1
    def can_kill_max(self, monster: StardewMonster) -> StardewRule:
        return self.logic.monster.can_kill(monster, MAX_MONTHS)

    # Should be cached
    def can_kill_any(self, monsters: (Iterable[StardewMonster], Hashable), amount_tier: int = 0) -> StardewRule:
        rules = [self.logic.monster.can_kill(monster, amount_tier) for monster in monsters]
        return Or(*rules)

    # Should be cached
    def can_kill_all(self, monsters: (Iterable[StardewMonster], Hashable), amount_tier: int = 0) -> StardewRule:
        rules = [self.logic.monster.can_kill(monster, amount_tier) for monster in monsters]
        return And(*rules)
