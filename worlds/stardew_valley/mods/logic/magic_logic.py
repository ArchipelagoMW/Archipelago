from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...mods.mod_data import ModNames
from ...stardew_rule import StardewRule
from ...strings.ap_names.skill_level_names import ModSkillLevel
from ...strings.region_names import MagicRegion
from ...strings.spells import MagicSpell, all_spells


class MagicLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.magic = MagicLogic(*args, **kwargs)


# TODO add logic.mods.magic for altar
class MagicLogic(BaseLogic):
    def can_use_clear_debris_instead_of_tool_level(self, level: int) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        return self.logic.received(MagicSpell.clear_debris) & self.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, level)

    def can_use_altar(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        return self.logic.region.can_reach(MagicRegion.altar) & self.logic.received_any(*all_spells)

    def has_any_spell(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        return self.can_use_altar()

    def has_attack_spell_count(self, count: int) -> StardewRule:
        attack_spell_rule = [self.logic.received(MagicSpell.fireball), self.logic.received(MagicSpell.frostbite), self.logic.received(MagicSpell.shockwave),
                             self.logic.received(MagicSpell.spirit), self.logic.received(MagicSpell.meteor)]
        return self.logic.count(count, *attack_spell_rule)

    def has_support_spell_count(self, count: int) -> StardewRule:
        support_spell_rule = [self.can_use_altar(), self.logic.received(ModSkillLevel.magic_level, 2),
                              self.logic.received(MagicSpell.descend), self.logic.received(MagicSpell.heal),
                              self.logic.received(MagicSpell.tendrils)]
        return self.logic.count(count, *support_spell_rule)

    def has_decent_spells(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        magic_resource_rule = self.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, 2)
        magic_attack_options_rule = self.has_attack_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule

    def has_good_spells(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        magic_resource_rule = self.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, 4)
        magic_attack_options_rule = self.has_attack_spell_count(2)
        magic_support_options_rule = self.has_support_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def has_great_spells(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        magic_resource_rule = self.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, 6)
        magic_attack_options_rule = self.has_attack_spell_count(3)
        magic_support_options_rule = self.has_support_spell_count(1)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def has_amazing_spells(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        magic_resource_rule = self.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, 8)
        magic_attack_options_rule = self.has_attack_spell_count(4)
        magic_support_options_rule = self.has_support_spell_count(2)
        return magic_resource_rule & magic_attack_options_rule & magic_support_options_rule

    def can_blink(self) -> StardewRule:
        if not self.content.is_enabled(ModNames.magic):
            return self.logic.false_

        return self.logic.received(MagicSpell.blink) & self.can_use_altar()
