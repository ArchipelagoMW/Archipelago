from typing import Union

from .magic_logic import MagicLogicMixin
from ...data.villagers_data import all_villagers
from ...logic.action_logic import ActionLogicMixin
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.building_logic import BuildingLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.fishing_logic import FishingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...mods.mod_data import ModNames
from ...options import SkillProgression
from ...stardew_rule import StardewRule, False_, True_
from ...strings.ap_names.mods.mod_items import SkillLevel
from ...strings.craftable_names import ModCraftable, ModMachine
from ...strings.building_names import Building
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


class ModSkillLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, ActionLogicMixin, RelationshipLogicMixin, BuildingLogicMixin,
ToolLogicMixin, FishingLogicMixin, CookingLogicMixin, MagicLogicMixin]]):
    def has_mod_level(self, skill: str, level: int) -> StardewRule:
        if level <= 0:
            return True_()

        if self.options.skill_progression == SkillProgression.option_progressive:
            return self.logic.received(f"{skill} Level", level)

        return self.can_earn_mod_skill_level(skill, level)

    def can_earn_mod_skill_level(self, skill: str, level: int) -> StardewRule:
        if ModNames.luck_skill in self.options.mods and skill == ModSkill.luck:
            return self.can_earn_luck_skill_level(level)
        if ModNames.magic in self.options.mods and skill == ModSkill.magic:
            return self.can_earn_magic_skill_level(level)
        if ModNames.socializing_skill in self.options.mods and skill == ModSkill.socializing:
            return self.can_earn_socializing_skill_level(level)
        if ModNames.archaeology in self.options.mods and skill == ModSkill.archaeology:
            return self.can_earn_archaeology_skill_level(level)
        if ModNames.cooking_skill in self.options.mods and skill == ModSkill.cooking:
            return self.can_earn_cooking_skill_level(level)
        if ModNames.binning_skill in self.options.mods and skill == ModSkill.binning:
            return self.can_earn_binning_skill_level(level)
        return False_()

    def can_earn_luck_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.fishing.can_fish_chests() | self.logic.action.can_open_geode(Geode.magma)
        if level >= 3:
            return self.logic.fishing.can_fish_chests() | self.logic.action.can_open_geode(Geode.geode)
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
        for villager in all_villagers:
            if villager.mod_name in self.options.mods or villager.mod_name is None:
                villager_count.append(self.logic.relationship.can_earn_relationship(villager.name, level))
        return self.logic.count(level * 2, *villager_count)

    def can_earn_archaeology_skill_level(self, level: int) -> StardewRule:
        shifter_rule = True_()
        preservation_rule = True_()
        if self.options.skill_progression == self.options.skill_progression.option_progressive:
            shifter_rule = self.logic.has(ModCraftable.water_shifter)
            preservation_rule = self.logic.has(ModMachine.hardwood_preservation_chamber)
        if level >= 8:
            return (self.logic.action.can_pan() & self.logic.tool.has_tool(Tool.hoe, ToolMaterial.gold)) & shifter_rule & preservation_rule
        if level >= 5:
            return (self.logic.action.can_pan() & self.logic.tool.has_tool(Tool.hoe, ToolMaterial.iron)) & shifter_rule
        if level >= 3:
            return self.logic.action.can_pan() | self.logic.tool.has_tool(Tool.hoe, ToolMaterial.copper)
        return self.logic.action.can_pan() | self.logic.tool.has_tool(Tool.hoe, ToolMaterial.basic)

    def can_earn_cooking_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.cooking.can_cook() & self.logic.region.can_reach(Region.saloon) & \
                self.logic.building.has_building(Building.coop) & self.logic.building.has_building(Building.barn)
        else:
            return self.logic.cooking.can_cook()

    def can_earn_binning_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.has(Machine.recycling_machine)
        else:
            return True_()  # You can always earn levels 1-5 with trash cans
