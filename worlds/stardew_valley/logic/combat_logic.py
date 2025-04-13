from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..mods.logic.magic_logic import MagicLogicMixin
from ..stardew_rule import StardewRule, False_
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.performance_names import Performance

valid_weapons = (APWeapon.weapon, APWeapon.sword, APWeapon.club, APWeapon.dagger)


class CombatLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.combat = CombatLogic(*args, **kwargs)


class CombatLogic(BaseLogic[Union[HasLogicMixin, CombatLogicMixin, RegionLogicMixin, ReceivedLogicMixin, MagicLogicMixin]]):
    @cache_self1
    def can_fight_at_level(self, level: str) -> StardewRule:
        if level == Performance.basic:
            return self.logic.combat.has_any_weapon | self.logic.magic.has_any_spell()
        if level == Performance.decent:
            return self.logic.combat.has_decent_weapon | self.logic.magic.has_decent_spells()
        if level == Performance.good:
            return self.logic.combat.has_good_weapon | self.logic.magic.has_good_spells()
        if level == Performance.great:
            return self.logic.combat.has_great_weapon | self.logic.magic.has_great_spells()
        if level == Performance.galaxy:
            return self.logic.combat.has_galaxy_weapon | self.logic.magic.has_amazing_spells()
        if level == Performance.maximum:
            return self.logic.combat.has_galaxy_weapon | self.logic.magic.has_amazing_spells()  # Someday we will have the ascended weapons in AP
        return False_()

    @cached_property
    def has_any_weapon(self) -> StardewRule:
        return self.logic.received_any(*valid_weapons)

    @cached_property
    def has_decent_weapon(self) -> StardewRule:
        return self.logic.or_(*(self.logic.received(weapon, 2) for weapon in valid_weapons))

    @cached_property
    def has_good_weapon(self) -> StardewRule:
        return self.logic.or_(*(self.logic.received(weapon, 3) for weapon in valid_weapons))

    @cached_property
    def has_great_weapon(self) -> StardewRule:
        return self.logic.or_(*(self.logic.received(weapon, 4) for weapon in valid_weapons))

    @cached_property
    def has_galaxy_weapon(self) -> StardewRule:
        return self.logic.or_(*(self.logic.received(weapon, 5) for weapon in valid_weapons))

    @cached_property
    def has_slingshot(self) -> StardewRule:
        return self.logic.received(APWeapon.slingshot)
