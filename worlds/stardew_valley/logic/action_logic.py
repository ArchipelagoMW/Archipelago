from .has_logic import HasLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from ..stardew_rule import StardewRule, True_, Or
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.region_names import Region


class ActionLogic:
    player: int
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic

    def __init__(self, player: int, received: ReceivedLogic, has: HasLogic, region: RegionLogic):
        self.player = player
        self.received = received
        self.has = has
        self.region = region

    def can_watch(self, channel: str = None):
        tv_rule = True_()
        if channel is None:
            return tv_rule
        return self.received(channel) & tv_rule

    def can_do_panning(self, item: str = Generic.any) -> StardewRule:
        return self.received("Glittering Boulder Removed")

    def can_open_geode(self, geode: str) -> StardewRule:
        blacksmith_access = self.region.can_reach(Region.blacksmith)
        geodes = [Geode.geode, Geode.frozen, Geode.magma, Geode.omni]
        if geode == Generic.any:
            return blacksmith_access & Or([self.has(geode_type) for geode_type in geodes])
        return blacksmith_access & self.has(geode)
