from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .. import options
from ..options import ArcadeMachineLocations
from ..stardew_rule import StardewRule, True_
from ..strings.region_names import Region


class ArcadeLogic:
    player: int
    arcade_option: ArcadeMachineLocations
    received = ReceivedLogic
    region: RegionLogic

    def __init__(self, player: int, arcade_option: ArcadeMachineLocations, received: ReceivedLogic, region: RegionLogic):
        self.player = player
        self.arcade_option = arcade_option
        self.received = received
        self.region = region

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        if self.arcade_option != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        jotpk_buffs = ("JotPK: Progressive Boots", "JotPK: Progressive Gun", "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate")
        return self.received(jotpk_buffs, power_level)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        if self.arcade_option != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        return self.received("Junimo Kart: Extra Life", power_level)

    def has_junimo_kart_max_level(self) -> StardewRule:
        play_rule = self.region.can_reach(Region.junimo_kart_3)
        if self.arcade_option != options.ArcadeMachineLocations.option_full_shuffling:
            return play_rule
        return self.has_junimo_kart_power_level(8)
