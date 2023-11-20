from functools import cached_property

from Utils import cache_self1
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..mods.logic.magic_logic import MagicLogic
from ..stardew_rule import StardewRule, Or, False_
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.performance_names import Performance

valid_weapons = (APWeapon.weapon, APWeapon.sword, APWeapon.club, APWeapon.dagger)


class CombatLogic:
    received: ReceivedLogicMixin
    region: RegionLogicMixin
    magic: MagicLogic

    def __init__(self, player: int, received: ReceivedLogicMixin, region: RegionLogicMixin):
        self.player = player
        self.region = region
        self.received = received

    def set_magic(self, magic: MagicLogic):
        self.magic = magic

    @cache_self1
    def can_fight_at_level(self, level: str) -> StardewRule:
        if level == Performance.basic:
            return self.has_any_weapon | self.magic.has_any_spell()
        if level == Performance.decent:
            return self.has_decent_weapon | self.magic.has_decent_spells()
        if level == Performance.good:
            return self.has_good_weapon | self.magic.has_good_spells()
        if level == Performance.great:
            return self.has_great_weapon | self.magic.has_great_spells()
        if level == Performance.galaxy:
            return self.has_galaxy_weapon | self.magic.has_amazing_spells()
        if level == Performance.maximum:
            return self.has_galaxy_weapon | self.magic.has_amazing_spells()  # Someday we will have the ascended weapons in AP
        return False_()

    @cached_property
    def has_any_weapon(self) -> StardewRule:
        return self.received(valid_weapons, 1)

    @cached_property
    def has_decent_weapon(self) -> StardewRule:
        return Or(*(self.received(weapon, 2) for weapon in valid_weapons))

    @cached_property
    def has_good_weapon(self) -> StardewRule:
        return Or(*(self.received(weapon, 3) for weapon in valid_weapons))

    @cached_property
    def has_great_weapon(self) -> StardewRule:
        return Or(*(self.received(weapon, 4) for weapon in valid_weapons))

    @cached_property
    def has_galaxy_weapon(self) -> StardewRule:
        return Or(*(self.received(weapon, 5) for weapon in valid_weapons))
