from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...mods.mod_data import ModNames
from ...options import Mods
from ...stardew_rule import Count, StardewRule, False_
from ...strings.ap_names.skill_level_names import ModSkillLevel
from ...strings.region_names import MagicRegion
from ...strings.spells import MagicSpell


class MagicLogic:
    player: int
    mods: Mods
    received: ReceivedLogicMixin
    region: RegionLogicMixin

    def __init__(self, player: int, mods: Mods, received: ReceivedLogicMixin, region: RegionLogicMixin):
        self.player = player
        self.mods = mods
        self.received = received
        self.region = region

    def can_use_clear_debris_instead_of_tool_level(self, level: int) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        return self.received(MagicSpell.clear_debris) & self.can_use_altar() & self.received(ModSkillLevel.magic_level, level)

    def can_use_altar(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        return self.region.can_reach(MagicRegion.altar)

    def has_any_spell(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        return self.can_use_altar()

    def has_attack_spell_count(self, count: int) -> StardewRule:
        attack_spell_rule = [self.received(MagicSpell.fireball), self.received(MagicSpell.frostbite), self.received(MagicSpell.shockwave),
                             self.received(MagicSpell.spirit), self.received(MagicSpell.meteor)]
        return Count(count, attack_spell_rule)

    def has_support_spell_count(self, count: int) -> StardewRule:
        support_spell_rule = [self.can_use_altar(), self.received(ModSkillLevel.magic_level, 2),
                              self.received(MagicSpell.descend), self.received(MagicSpell.heal),
                              self.received(MagicSpell.tendrils)]
        return Count(count, support_spell_rule)

    def has_decent_spells(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        magic_resource_rule = self.can_use_altar() & self.received(ModSkillLevel.magic_level, 2)
        magic_attack_options_rule = self.has_attack_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule

    def has_good_spells(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        magic_resource_rule = self.can_use_altar() & self.received(ModSkillLevel.magic_level, 4)
        magic_attack_options_rule = self.has_attack_spell_count(2)
        magic_support_options_rule = self.has_support_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def has_great_spells(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        magic_resource_rule = self.can_use_altar() & self.received(ModSkillLevel.magic_level, 6)
        magic_attack_options_rule = self.has_attack_spell_count(3)
        magic_support_options_rule = self.has_support_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def has_amazing_spells(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        magic_resource_rule = self.can_use_altar() & self.received(ModSkillLevel.magic_level, 8)
        magic_attack_options_rule = self.has_attack_spell_count(4)
        magic_support_options_rule = self.has_support_spell_count(2)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def can_blink(self) -> StardewRule:
        if ModNames.magic not in self.mods:
            return False_()
        return self.received(MagicSpell.blink) & self.can_use_altar()
