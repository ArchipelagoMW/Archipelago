from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from ..mods.logic.magic_logic import MagicLogic
from ..stardew_rule import StardewRule, Or
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.performance_names import Performance
from ..strings.region_names import Region

valid_weapons = [APWeapon.weapon, APWeapon.sword, APWeapon.club, APWeapon.dagger]


class CombatLogic:
    player: int
    received: ReceivedLogic
    region: RegionLogic
    magic: MagicLogic

    def __init__(self, player: int, received: ReceivedLogic, region: RegionLogic):
        self.player = player
        self.region = region
        self.received = received
        self.has_any_weapon_rule = self.can_buy_weapon(self.has_received_any_weapon())
        self.has_decent_weapon_rule = self.can_buy_weapon(self.has_received_decent_weapon())
        self.has_good_weapon_rule = self.can_buy_weapon(self.has_received_good_weapon())
        self.has_great_weapon_rule = self.can_buy_weapon(self.has_received_great_weapon())
        self.has_galaxy_weapon_rule = self.can_buy_weapon(self.has_received_galaxy_weapon())

    def set_magic(self, magic: MagicLogic):
        self.magic = magic

    def can_fight_at_level(self, level: str) -> StardewRule:
        if level == Performance.basic:
            return self.has_any_weapon() | self.magic.has_any_spell()
        if level == Performance.decent:
            return self.has_decent_weapon() | self.magic.has_decent_spells()
        if level == Performance.good:
            return self.has_good_weapon() | self.magic.has_good_spells()
        if level == Performance.great:
            return self.has_great_weapon() | self.magic.has_great_spells()
        if level == Performance.galaxy:
            return self.has_galaxy_weapon() | self.magic.has_amazing_spells()
        if level == Performance.maximum:
            return self.has_galaxy_weapon() | self.magic.has_amazing_spells()  # Someday we will have the ascended weapons in AP

    def has_any_weapon(self) -> StardewRule:
        return self.has_any_weapon_rule

    def has_decent_weapon(self) -> StardewRule:
        return self.has_decent_weapon_rule

    def has_good_weapon(self) -> StardewRule:
        return self.has_good_weapon_rule

    def has_great_weapon(self) -> StardewRule:
        return self.has_great_weapon_rule

    def has_galaxy_weapon(self) -> StardewRule:
        return self.has_galaxy_weapon_rule

    def has_received_any_weapon(self) -> StardewRule:
        return self.received(valid_weapons, 1)

    def has_received_decent_weapon(self) -> StardewRule:
        return Or(self.received(weapon, 2) for weapon in valid_weapons)

    def has_received_good_weapon(self) -> StardewRule:
        return Or(self.received(weapon, 3) for weapon in valid_weapons)

    def has_received_great_weapon(self) -> StardewRule:
        return Or(self.received(weapon, 4) for weapon in valid_weapons)

    def has_received_galaxy_weapon(self) -> StardewRule:
        return Or(self.received(weapon, 5) for weapon in valid_weapons)

    def can_buy_weapon(self, weapon_rule: StardewRule = None) -> StardewRule:
        adventure_guild_rule = self.region.can_reach(Region.adventurer_guild)
        if weapon_rule is None:
            return adventure_guild_rule
        return adventure_guild_rule & weapon_rule
