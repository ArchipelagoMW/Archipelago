from ...strings.region_names import MagicRegion
from ...mods.mod_data import ModNames
from ...strings.spells import MagicSpell
from ...strings.ap_names.skill_level_names import ModSkillLevel
from ...stardew_rule import Count, StardewRule, False_
from ... import options


def can_use_clear_debris_instead_of_tool_level(self, level: int) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    return self.received(MagicSpell.clear_debris) & can_use_altar(self) & self.received(ModSkillLevel.magic_level, level)


def can_use_altar(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    return self.can_reach_region(MagicRegion.altar)


def has_any_spell(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    return can_use_altar(self)


def has_attack_spell_count(self, count: int) -> StardewRule:
    attack_spell_rule = [self.received(MagicSpell.fireball), self.received(
        MagicSpell.frostbite), self.received(MagicSpell.shockwave), self.received(MagicSpell.spirit),
                         self.received(MagicSpell.meteor)
                         ]
    return Count(count, attack_spell_rule)


def has_support_spell_count(self, count: int) -> StardewRule:
    support_spell_rule = [can_use_altar(self), self.received(ModSkillLevel.magic_level, 2)
                          ]
    return Count(count, support_spell_rule)


def has_decent_spells(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    magic_resource_rule = can_use_altar(self) & self.received(ModSkillLevel.magic_level, 2)
    magic_attack_options_rule = has_attack_spell_count(self, 1)
    return magic_resource_rule & magic_attack_options_rule


def has_good_spells(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    magic_resource_rule = can_use_altar(self) & self.received(ModSkillLevel.magic_level, 4)
    magic_attack_options_rule = has_attack_spell_count(self, 2)
    magic_support_options_rule = has_support_spell_count(self, 1)
    return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule


def has_great_spells(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    magic_resource_rule = can_use_altar(self) & self.received(ModSkillLevel.magic_level, 6)
    magic_attack_options_rule = has_attack_spell_count(self, 3)
    magic_support_options_rule = has_support_spell_count(self, 1)
    return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule


def has_amazing_spells(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    magic_resource_rule = can_use_altar(self) & self.received(ModSkillLevel.magic_level, 8)
    magic_attack_options_rule = has_attack_spell_count(self, 4)
    magic_support_options_rule = has_support_spell_count(self, 2)
    return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule


def can_blink(self) -> StardewRule:
    if ModNames.magic not in self.options[options.Mods]:
        return False_()
    return self.received(MagicSpell.blink) & can_use_altar(self)
