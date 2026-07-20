from functools import cached_property
from typing import Iterable, Union, Hashable

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .time_logic import MAX_MONTHS
from ..data import monster_data
from ..data.fish_data import ginger_island_river
from ..stardew_rule import StardewRule
from ..strings.generic_names import Generic
from ..strings.region_names import Region


class MonsterLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monster = MonsterLogic(*args, **kwargs)


class MonsterLogic(BaseLogic):

    @cached_property
    def all_monsters_by_name(self):
        return monster_data.all_monsters_by_name_given_content_packs(self.content.registered_packs)

    @cached_property
    def all_monsters_by_category(self):
        return monster_data.all_monsters_by_category_given_content_packs(self.content.registered_packs)

    def can_kill(self, monster: Union[str, monster_data.StardewMonster], amount_tier: int = 0) -> StardewRule:
        if amount_tier <= 0:
            amount_tier = 0
        time_rule = self.logic.time.has_lived_months(amount_tier)

        if isinstance(monster, str):
            if monster == Generic.any:
                return self.logic.monster.can_kill_any(self.all_monsters_by_name.values()) & time_rule

            monster = self.all_monsters_by_name[monster]
        region_rule = self.logic.region.can_reach_any(*monster.locations)
        combat_rule = self.logic.combat.can_fight_at_level(monster.difficulty)

        return region_rule & combat_rule & time_rule

    @cache_self1
    def can_kill_many(self, monster: Union[str, monster_data.StardewMonster]) -> StardewRule:
        return self.logic.monster.can_kill(monster, MAX_MONTHS / 3)

    @cache_self1
    def can_kill_max(self, monster: Union[str, monster_data.StardewMonster]) -> StardewRule:
        return self.logic.monster.can_kill(monster, MAX_MONTHS)

    # Should be cached
    def can_kill_any(self, monsters: (Iterable[Union[str, monster_data.StardewMonster]], Hashable), amount_tier: int = 0) -> StardewRule:
        return self.logic.or_(*(self.logic.monster.can_kill(monster, amount_tier) for monster in monsters))

    # Should be cached
    def can_kill_all(self, monsters: (Iterable[Union[str, monster_data.StardewMonster]], Hashable), amount_tier: int = 0) -> StardewRule:
        return self.logic.and_(*(self.logic.monster.can_kill(monster, amount_tier) for monster in monsters))

    def can_complete_all_monster_slaying_goals(self) -> StardewRule:
        rules = [self.logic.time.has_lived_max_months]
        exclude_island = not self.content.is_enabled(ginger_island_river)
        island_regions = [Region.volcano_floor_5, Region.volcano_floor_10, Region.island_west, Region.dangerous_skull_cavern]
        for category in self.all_monsters_by_category:
            if exclude_island and all(all(location in island_regions for location in monster.locations)
                                      for monster in self.all_monsters_by_category[category]):
                continue
            rules.append(self.logic.monster.can_kill_any(self.all_monsters_by_category[category]))

        return self.logic.and_(*rules)
