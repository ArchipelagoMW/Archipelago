from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...stardew_rule import StardewRule, True_, And
from ...strings.building_names import Building
from ...strings.craftable_names import ModCraftable, ModMachine
from ...strings.geode_names import Geode
from ...strings.machine_names import Machine
from ...strings.region_names import Region
from ...strings.skill_names import ModSkill
from ...strings.spells import MagicSpell
from ...strings.tool_names import Tool, ToolMaterial


class ModSkillLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill = ModSkillLogic(*args, **kwargs)


class ModSkillLogic(BaseLogic):
    def has_mod_level(self, skill: str, level: int) -> StardewRule:
        if level <= 0:
            return True_()

        if self.content.features.skill_progression.is_progressive:
            return self.logic.received(f"{skill} Level", level)

        return self.can_earn_mod_skill_level(skill, level)

    def can_earn_mod_skill_level(self, skill: str, level: int) -> StardewRule:
        if not skill in self.content.skills:
            return self.logic.false_

        if skill == ModSkill.luck:
            return self.can_earn_luck_skill_level(level)
        if skill == ModSkill.magic:
            return self.can_earn_magic_skill_level(level)
        if skill == ModSkill.socializing:
            return self.can_earn_socializing_skill_level(level)
        if skill == ModSkill.archaeology:
            return self.can_earn_archaeology_skill_level(level)
        if skill == ModSkill.cooking:
            return self.can_earn_cooking_skill_level(level)
        if skill == ModSkill.binning:
            return self.can_earn_binning_skill_level(level)

        return self.logic.false_

    def can_earn_luck_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.fishing.can_fish_chests | self.logic.action.can_open_geode(Geode.magma)
        if level >= 3:
            return self.logic.fishing.can_fish_chests | self.logic.action.can_open_geode(Geode.geode)
        return True_()  # You can literally wake up and or get them by opening starting chests.

    def can_earn_magic_skill_level(self, level: int) -> StardewRule:
        spell_count = [self.logic.received(MagicSpell.clear_debris), self.logic.received(MagicSpell.water),
                       self.logic.received(MagicSpell.blink), self.logic.received(MagicSpell.fireball),
                       self.logic.received(MagicSpell.frostbite),
                       self.logic.received(MagicSpell.descend), self.logic.received(MagicSpell.tendrils),
                       self.logic.received(MagicSpell.shockwave),
                       self.logic.received(MagicSpell.meteor),
                       self.logic.received(MagicSpell.spirit)]
        return self.logic.count(level, *spell_count)

    def can_earn_socializing_skill_level(self, level: int) -> StardewRule:
        villager_count = []

        for villager in self.content.villagers.values():
            villager_count.append(self.logic.relationship.can_earn_relationship(villager.name, level))

        return self.logic.count(level * 2, *villager_count)

    def can_earn_archaeology_skill_level(self, level: int) -> StardewRule:
        shifter_rule = True_()
        preservation_rule = True_()
        if self.content.features.skill_progression.is_progressive:
            shifter_rule = self.logic.has(ModCraftable.water_sifter)
            preservation_rule = self.logic.has(ModMachine.hardwood_preservation_chamber)
        if level > 8:
            tool_rule = self.logic.tool.has_pan(ToolMaterial.iridium) & self.logic.tool.has_tool(Tool.hoe, ToolMaterial.gold)
            return tool_rule & shifter_rule & preservation_rule
        if level > 6:
            tool_rule = self.logic.tool.has_pan(ToolMaterial.gold) & self.logic.tool.has_tool(Tool.hoe, ToolMaterial.iron)
            return tool_rule & preservation_rule
        if level >= 3:
            return self.logic.tool.has_pan(ToolMaterial.iron) | self.logic.tool.has_tool(Tool.hoe, ToolMaterial.copper)
        return self.logic.tool.has_pan() | self.logic.tool.has_tool(Tool.hoe, ToolMaterial.basic)

    def can_earn_cooking_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.cooking.can_cook() & self.logic.region.can_reach(Region.saloon) & \
                self.logic.building.has_building(Building.coop) & self.logic.building.has_building(Building.barn)
        else:
            return self.logic.cooking.can_cook()

    def can_earn_binning_skill_level(self, level: int) -> StardewRule:
        if level <= 2:
            return True_()
        binning_rule = [self.logic.has(ModMachine.trash_bin) & self.logic.has(Machine.recycling_machine)]
        if level > 4:
            binning_rule.append(self.logic.has(ModMachine.composter))
        if level > 7:
            binning_rule.append(self.logic.has(ModMachine.recycling_bin))
        if level > 9:
            binning_rule.append(self.logic.has(ModMachine.advanced_recycling_machine))
        return And(*binning_rule)
