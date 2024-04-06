from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..stardew_rule import StardewRule, True_, Or
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.region_names import Region


class ActionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = ActionLogic(*args, **kwargs)


class ActionLogic(BaseLogic[Union[ActionLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin]]):

    def can_watch(self, channel: str = None):
        tv_rule = True_()
        if channel is None:
            return tv_rule
        return self.logic.received(channel) & tv_rule

    def can_pan(self) -> StardewRule:
        return self.logic.received("Glittering Boulder Removed") & self.logic.region.can_reach(Region.mountain)

    def can_pan_at(self, region: str) -> StardewRule:
        return self.logic.region.can_reach(region) & self.logic.action.can_pan()

    @cache_self1
    def can_open_geode(self, geode: str) -> StardewRule:
        blacksmith_access = self.logic.region.can_reach(Region.blacksmith)
        geodes = [Geode.geode, Geode.frozen, Geode.magma, Geode.omni]
        if geode == Generic.any:
            return blacksmith_access & Or(*(self.logic.has(geode_type) for geode_type in geodes))
        return blacksmith_access & self.logic.has(geode)
