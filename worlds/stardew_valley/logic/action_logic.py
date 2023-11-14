from functools import lru_cache

from .cached_logic import CachedLogic
from .has_logic import HasLogic, CachedRules
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from ..stardew_rule import StardewRule, True_, Or
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.region_names import Region


class ActionLogic(CachedLogic):
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic

    def __init__(self, player: int, cached_rules: CachedRules, received: ReceivedLogic, has: HasLogic,
                 region: RegionLogic):
        super().__init__(player, cached_rules)
        self.received = received
        self.has = has
        self.region = region

    def can_watch(self, channel: str = None):
        tv_rule = True_()
        if channel is None:
            return tv_rule
        return self.received(channel) & tv_rule

    def can_pan(self) -> StardewRule:
        return self.received("Glittering Boulder Removed") & self.region.can_reach(Region.mountain)

    def can_pan_at(self, region: str) -> StardewRule:
        return self.region.can_reach(region) & self.can_pan()

    @lru_cache(maxsize=None)
    def can_open_geode(self, geode: str) -> StardewRule:
        blacksmith_access = self.region.can_reach(Region.blacksmith)
        geodes = [Geode.geode, Geode.frozen, Geode.magma, Geode.omni]
        if geode == Generic.any:
            return blacksmith_access & Or([self.has(geode_type) for geode_type in geodes])
        return blacksmith_access & self.has(geode)
