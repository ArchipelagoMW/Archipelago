from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from ..stardew_rule import StardewRule, True_
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.region_names import Region
from ..strings.tool_names import Tool


class ActionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = ActionLogic(*args, **kwargs)


class ActionLogic(BaseLogic):

    def can_watch(self, channel: str = None):
        tv_rule = True_()
        if channel is None:
            return tv_rule
        return self.logic.received(channel) & tv_rule

    def can_pan_at(self, region: str, material: str) -> StardewRule:
        return self.logic.region.can_reach(region) & self.logic.tool.has_tool(Tool.pan, material)

    @cache_self1
    def can_open_geode(self, geode: str) -> StardewRule:
        blacksmith_access = self.logic.region.can_reach(Region.blacksmith)
        geodes = [Geode.geode, Geode.frozen, Geode.magma, Geode.omni]
        if geode == Generic.any:
            return blacksmith_access & self.logic.or_(*(self.logic.has(geode_type) for geode_type in geodes))
        return blacksmith_access & self.logic.has(geode)
