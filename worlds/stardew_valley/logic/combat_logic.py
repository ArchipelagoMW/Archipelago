from functools import cached_property

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..options import Monstersanity
from ..stardew_rule import StardewRule, False_
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.ap_names.event_names import Event
from ..strings.boot_names import tier_by_boots
from ..strings.performance_names import Performance
from ..strings.region_names import Region

valid_weapons = (APWeapon.weapon, APWeapon.sword, APWeapon.club, APWeapon.dagger)


class CombatLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.combat = CombatLogic(*args, **kwargs)


class CombatLogic(BaseLogic):
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
        return self.logic.received(Event.received_progressive_weapon)

    @cached_property
    def has_decent_weapon(self) -> StardewRule:
        return self.logic.received(Event.received_progressive_weapon, 2)

    @cached_property
    def has_good_weapon(self) -> StardewRule:
        return self.logic.received(Event.received_progressive_weapon, 3)

    @cached_property
    def has_great_weapon(self) -> StardewRule:
        return self.logic.received(Event.received_progressive_weapon, 4)

    @cached_property
    def has_galaxy_weapon(self) -> StardewRule:
        return self.logic.received(Event.received_progressive_weapon, 5)

    @cached_property
    def has_slingshot(self) -> StardewRule:
        return self.logic.received(APWeapon.slingshot)

    @cache_self1
    def has_specific_boots(self, boots: str) -> StardewRule:
        tier = tier_by_boots[boots]
        if tier >= 4 and self.options.monstersanity == Monstersanity.option_none:
            tier = 3  # no tier 4 boots in the pool, instead tier 4 boots can be purchased after tier 3 is received
        return self.logic.received(APWeapon.footwear, tier) & self.logic.region.can_reach(Region.adventurer_guild)
