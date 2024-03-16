import math
from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from ..data.villagers_data import Villager
from ..options import Friendsanity
from ..stardew_rule import StardewRule, True_
from ..strings.region_names import Region
from ..strings.villager_names import NPC


class PetLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pet = PetLogic(*args, **kwargs)


class PetLogic(BaseLogic[Union[RegionLogicMixin, ReceivedLogicMixin, TimeLogicMixin, ToolLogicMixin]]):
    def has_hearts(self, hearts: int = 1) -> StardewRule:
        if hearts <= 0:
            return True_()
        if self.options.friendsanity == Friendsanity.option_none or self.options.friendsanity == Friendsanity.option_bachelors:
            return self.can_befriend_pet(hearts)
        return self.received_hearts(NPC.pet, hearts)

    def received_hearts(self, npc: Union[str, Villager], hearts: int) -> StardewRule:
        if isinstance(npc, Villager):
            return self.received_hearts(npc.name, hearts)
        return self.logic.received(self.heart(npc), math.ceil(hearts / self.options.friendsanity_heart_size))

    def can_befriend_pet(self, hearts: int) -> StardewRule:
        if hearts <= 0:
            return True_()
        points = hearts * 200
        points_per_month = 12 * 14
        points_per_water_month = 18 * 14
        farm_rule = self.logic.region.can_reach(Region.farm)
        time_with_water_rule = self.logic.tool.can_water(0) & self.logic.time.has_lived_months(points // points_per_water_month)
        time_without_water_rule = self.logic.time.has_lived_months(points // points_per_month)
        time_rule = time_with_water_rule | time_without_water_rule
        return farm_rule & time_rule

    def heart(self, npc: Union[str, Villager]) -> str:
        if isinstance(npc, str):
            return f"{npc} <3"
        return self.heart(npc.name)
