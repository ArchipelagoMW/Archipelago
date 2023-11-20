from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .. import options
from ..stardew_rule import StardewRule, True_
from ..strings.region_names import Region


class ArcadeLogicMixin(RegionLogicMixin, ReceivedLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arcade = self

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        if self.options.arcade_machine_locations != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        jotpk_buffs = ("JotPK: Progressive Boots", "JotPK: Progressive Gun", "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate")
        return self.received(jotpk_buffs, power_level)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        if self.options.arcade_machine_locations != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        return self.received("Junimo Kart: Extra Life", power_level)

    def has_junimo_kart_max_level(self) -> StardewRule:
        play_rule = self.region.can_reach(Region.junimo_kart_3)
        if self.options.arcade_machine_locations != options.ArcadeMachineLocations.option_full_shuffling:
            return play_rule
        return self.arcade.has_junimo_kart_power_level(8)
