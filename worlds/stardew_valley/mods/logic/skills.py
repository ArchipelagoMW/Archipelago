from typing import List
from . import magic
from ...strings.building_names import Building
from ...strings.geode_names import Geode
from ...strings.region_names import Region
from ...strings.skill_names import ModSkill
from ...strings.spells import MagicSpell
from ...strings.machine_names import Machine
from ...strings.tool_names import Tool, ToolMaterial
from ...mods.mod_data import ModNames
from ...data.villagers_data import all_villagers
from ...stardew_rule import Count, StardewRule, True_
from ... import options
from ...options import StardewOptions


def append_mod_skill_level(skills_items: List[str], world_options: StardewOptions):
    if ModNames.luck_skill in world_options[options.Mods]:
        skills_items.append("Luck Level")
    if ModNames.socializing_skill in world_options[options.Mods]:
        skills_items.append("Socializing Level")
    if ModNames.magic in world_options[options.Mods]:
        skills_items.append("Magic Level")
    if ModNames.archaeology in world_options[options.Mods]:
        skills_items.append("Archaeology Level")
    if ModNames.binning_skill in world_options[options.Mods]:
        skills_items.append("Binning Level")
    if ModNames.cooking_skill in world_options[options.Mods]:
        skills_items.append("Cooking Level")


def can_earn_mod_skill_level(logic, skill: str, level: int) -> StardewRule:
    if ModNames.luck_skill in logic.options[options.Mods] and skill == ModSkill.luck:
        return can_earn_luck_skill_level(logic, level)
    if ModNames.magic in logic.options[options.Mods] and skill == ModSkill.magic:
        return can_earn_magic_skill_level(logic, level)
    if ModNames.socializing_skill in logic.options[options.Mods] and skill == ModSkill.socializing:
        return can_earn_socializing_skill_level(logic, level)
    if ModNames.archaeology in logic.options[options.Mods] and skill == ModSkill.archaeology:
        return can_earn_archaeology_skill_level(logic, level)
    if ModNames.cooking_skill in logic.options[options.Mods] and skill == ModSkill.cooking:
        return can_earn_cooking_skill_level(logic, level)
    if ModNames.binning_skill in logic.options[options.Mods] and skill == ModSkill.binning:
        return can_earn_binning_skill_level(logic, level)
    return True_()


def can_earn_luck_skill_level(self, level: int) -> StardewRule:
    if level >= 6:
        return self.can_fish_chests() | self.can_open_geode(Geode.magma)
    else:
        return self.can_fish_chests() | self.can_open_geode(Geode.geode)


def can_earn_magic_skill_level(self, level: int) -> StardewRule:
    spell_count = [self.received(MagicSpell.clear_debris), self.received(MagicSpell.water),
                   self.received(MagicSpell.blink), self.received(MagicSpell.fireball),
                   self.received(MagicSpell.frostbite),
                   self.received(MagicSpell.descend), self.received(MagicSpell.tendrils),
                   self.received(MagicSpell.shockwave),
                   self.received(MagicSpell.meteor),
                   self.received(MagicSpell.spirit)]
    return magic.can_use_altar(self) & Count(level, spell_count)


def can_earn_socializing_skill_level(self, level: int) -> StardewRule:
    villager_count = []
    for villager in all_villagers:
        if villager.mod_name in self.options[options.Mods] or villager.mod_name is None:
            villager_count.append(self.can_earn_relationship(villager.name, level))
    return Count(level * 2, villager_count)


def can_earn_archaeology_skill_level(self, level: int) -> StardewRule:
    if level >= 6:
        return self.can_do_panning() | self.has_tool(Tool.hoe, ToolMaterial.gold)
    else:
        return self.can_do_panning() | self.has_tool(Tool.hoe, ToolMaterial.basic)


def can_earn_cooking_skill_level(self, level: int) -> StardewRule:
    if level >= 6:
        return self.can_cook() & self.can_fish() & self.can_reach_region(Region.saloon) & \
            self.has_building(Building.coop) & self.has_building(Building.barn)
    else:
        return self.can_cook()


def can_earn_binning_skill_level(self, level: int) -> StardewRule:
    if level >= 6:
        return self.can_reach_region(Region.town) & self.has(Machine.recycling_machine) & \
            (self.can_fish() | self.can_crab_pot())
    else:
        return self.can_reach_region(Region.town) | (self.has(Machine.recycling_machine) &
                                                     (self.can_fish() | self.can_crab_pot()))
