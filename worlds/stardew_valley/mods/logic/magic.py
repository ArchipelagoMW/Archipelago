from ...strings.region_names import MagicRegion
from ...mods.mod_data import ModNames
from ...strings.spells import MagicSpell
from ...strings.ap_names.skill_level_names import ModSkillLevel
from ...stardew_rule import Count, StardewRule, False_
from ... import options


def can_use_clear_debris_instead_of_tool_level(vanilla_logic, level: int) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    return vanilla_logic.received(MagicSpell.clear_debris) & can_use_altar(vanilla_logic) & vanilla_logic.received(ModSkillLevel.magic_level, level)


def can_use_altar(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    return vanilla_logic.can_reach_region(MagicRegion.altar)


def has_any_spell(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    return can_use_altar(vanilla_logic)


def has_attack_spell_count(vanilla_logic, count: int) -> StardewRule:
    attack_spell_rule = [vanilla_logic.received(MagicSpell.fireball), vanilla_logic.received(
        MagicSpell.frostbite), vanilla_logic.received(MagicSpell.shockwave), vanilla_logic.received(MagicSpell.spirit),
                         vanilla_logic.received(MagicSpell.meteor)
                         ]
    return Count(count, attack_spell_rule)


def has_support_spell_count(vanilla_logic, count: int) -> StardewRule:
    support_spell_rule = [can_use_altar(vanilla_logic), vanilla_logic.received(ModSkillLevel.magic_level, 2),
                          vanilla_logic.received(MagicSpell.descend), vanilla_logic.received(MagicSpell.heal),
                          vanilla_logic.received(MagicSpell.tendrils)]
    return Count(count, support_spell_rule)


def has_decent_spells(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    magic_resource_rule = can_use_altar(vanilla_logic) & vanilla_logic.received(ModSkillLevel.magic_level, 2)
    magic_attack_options_rule = has_attack_spell_count(vanilla_logic, 1)
    return magic_resource_rule & magic_attack_options_rule


def has_good_spells(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    magic_resource_rule = can_use_altar(vanilla_logic) & vanilla_logic.received(ModSkillLevel.magic_level, 4)
    magic_attack_options_rule = has_attack_spell_count(vanilla_logic, 2)
    magic_support_options_rule = has_support_spell_count(vanilla_logic, 1)
    return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule


def has_great_spells(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    magic_resource_rule = can_use_altar(vanilla_logic) & vanilla_logic.received(ModSkillLevel.magic_level, 6)
    magic_attack_options_rule = has_attack_spell_count(vanilla_logic, 3)
    magic_support_options_rule = has_support_spell_count(vanilla_logic, 1)
    return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule


def has_amazing_spells(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    magic_resource_rule = can_use_altar(vanilla_logic) & vanilla_logic.received(ModSkillLevel.magic_level, 8)
    magic_attack_options_rule = has_attack_spell_count(vanilla_logic, 4)
    magic_support_options_rule = has_support_spell_count(vanilla_logic, 2)
    return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule


def can_blink(vanilla_logic) -> StardewRule:
    if ModNames.magic not in vanilla_logic.options.mods:
        return False_()
    return vanilla_logic.received(MagicSpell.blink) & can_use_altar(vanilla_logic)
