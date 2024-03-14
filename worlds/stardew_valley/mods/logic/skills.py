from typing import List, Union
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
from ...stardew_rule import Count, StardewRule, False_
from ... import options


def append_mod_skill_level(skills_items: List[str], active_mods):
    if ModNames.luck_skill in active_mods:
        skills_items.append("Luck Level")
    if ModNames.socializing_skill in active_mods:
        skills_items.append("Socializing Level")
    if ModNames.magic in active_mods:
        skills_items.append("Magic Level")
    if ModNames.archaeology in active_mods:
        skills_items.append("Archaeology Level")
    if ModNames.binning_skill in active_mods:
        skills_items.append("Binning Level")
    if ModNames.cooking_skill in active_mods:
        skills_items.append("Cooking Level")


def can_earn_mod_skill_level(logic, skill: str, level: int) -> StardewRule:
    if ModNames.luck_skill in logic.options.mods and skill == ModSkill.luck:
        return can_earn_luck_skill_level(logic, level)
    if ModNames.magic in logic.options.mods and skill == ModSkill.magic:
        return can_earn_magic_skill_level(logic, level)
    if ModNames.socializing_skill in logic.options.mods and skill == ModSkill.socializing:
        return can_earn_socializing_skill_level(logic, level)
    if ModNames.archaeology in logic.options.mods and skill == ModSkill.archaeology:
        return can_earn_archaeology_skill_level(logic, level)
    if ModNames.cooking_skill in logic.options.mods and skill == ModSkill.cooking:
        return can_earn_cooking_skill_level(logic, level)
    if ModNames.binning_skill in logic.options.mods and skill == ModSkill.binning:
        return can_earn_binning_skill_level(logic, level)
    return False_()


def can_earn_luck_skill_level(vanilla_logic, level: int) -> StardewRule:
    if level >= 6:
        return vanilla_logic.can_fish_chests() | vanilla_logic.can_open_geode(Geode.magma)
    else:
        return vanilla_logic.can_fish_chests() | vanilla_logic.can_open_geode(Geode.geode)


def can_earn_magic_skill_level(vanilla_logic, level: int) -> StardewRule:
    spell_count = [vanilla_logic.received(MagicSpell.clear_debris), vanilla_logic.received(MagicSpell.water),
                   vanilla_logic.received(MagicSpell.blink), vanilla_logic.received(MagicSpell.fireball),
                   vanilla_logic.received(MagicSpell.frostbite),
                   vanilla_logic.received(MagicSpell.descend), vanilla_logic.received(MagicSpell.tendrils),
                   vanilla_logic.received(MagicSpell.shockwave),
                   vanilla_logic.received(MagicSpell.meteor),
                   vanilla_logic.received(MagicSpell.spirit)]
    return magic.can_use_altar(vanilla_logic) & Count(level, spell_count)


def can_earn_socializing_skill_level(vanilla_logic, level: int) -> StardewRule:
    villager_count = []
    for villager in all_villagers:
        if villager.mod_name in vanilla_logic.options.mods or villager.mod_name is None:
            villager_count.append(vanilla_logic.can_earn_relationship(villager.name, level))
    return Count(level * 2, villager_count)


def can_earn_archaeology_skill_level(vanilla_logic, level: int) -> StardewRule:
    if level >= 6:
        return vanilla_logic.can_do_panning() | vanilla_logic.has_tool(Tool.hoe, ToolMaterial.gold)
    else:
        return vanilla_logic.can_do_panning() | vanilla_logic.has_tool(Tool.hoe, ToolMaterial.basic)


def can_earn_cooking_skill_level(vanilla_logic, level: int) -> StardewRule:
    if level >= 6:
        return vanilla_logic.can_cook() & vanilla_logic.can_fish() & vanilla_logic.can_reach_region(Region.saloon) & \
            vanilla_logic.has_building(Building.coop) & vanilla_logic.has_building(Building.barn)
    else:
        return vanilla_logic.can_cook()


def can_earn_binning_skill_level(vanilla_logic, level: int) -> StardewRule:
    if level >= 6:
        return vanilla_logic.can_reach_region(Region.town) & vanilla_logic.has(Machine.recycling_machine) & \
            (vanilla_logic.can_fish() | vanilla_logic.can_crab_pot())
    else:
        return vanilla_logic.can_reach_region(Region.town) | (vanilla_logic.has(Machine.recycling_machine) &
                                                     (vanilla_logic.can_fish() | vanilla_logic.can_crab_pot()))
