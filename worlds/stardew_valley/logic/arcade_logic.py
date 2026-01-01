from .base_logic import BaseLogic, BaseLogicMixin
from .. import options
from ..stardew_rule import StardewRule, True_
from ..strings.region_names import Region


class ArcadeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arcade = ArcadeLogic(*args, **kwargs)


class ArcadeLogic(BaseLogic):

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        if self.options.arcade_machine_locations != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        jotpk_buffs = ("JotPK: Progressive Boots", "JotPK: Progressive Gun", "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate")
        return self.logic.received_n(*jotpk_buffs, count=power_level)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        if self.options.arcade_machine_locations != options.ArcadeMachineLocations.option_full_shuffling:
            return True_()
        return self.logic.received("Junimo Kart: Extra Life", power_level)

    def has_junimo_kart_max_level(self) -> StardewRule:
        play_rule = self.logic.region.can_reach(Region.junimo_kart_3)
        if self.options.arcade_machine_locations != options.ArcadeMachineLocations.option_full_shuffling:
            return play_rule
        return self.logic.arcade.has_junimo_kart_power_level(8)
