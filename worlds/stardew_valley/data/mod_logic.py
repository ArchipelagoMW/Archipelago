from typing import List
from .region_data import SVRegion
from .villagers_data import all_villagers
from ..stardew_rule import False_
from .. import options
from ..options import StardewOptions

# Attempt to inject new methods into logic that can be easily commented out.


def append_mod_skill_level(skills_items: List[str], world_options: StardewOptions):
    if "Luck Skill" in world_options[options.Mods]:
        skills_items.append("Luck Level")
    if "Socializing Skill" in world_options[options.Mods]:
        skills_items.append("Socializing Level")
    if "Magic" in world_options[options.Mods]:
        skills_items.append("Magic Level")
    if "Archaeology" in world_options[options.Mods]:
        skills_items.append("Archaeology Level")
    if "Binning Skill" in world_options[options.Mods]:
        skills_items.append("Binning Level")
    if "Cooking Skill" in world_options[options.Mods]:
        skills_items.append("Cooking Level")


def can_earn_mod_skill_level(rule, skill: str, level: int, tool_rule: bool):
    mod_tool_rule = tool_rule
    if "Luck Skill" in rule.options[options.Mods]:
        if skill == "Luck":
            if level >= 6:
                mod_tool_rule = rule.can_fish_chests() | rule.can_open_geode("Magma Geode")
            else:
                mod_tool_rule = rule.can_fish_chests() | rule.can_open_geode("Geode")
    if "Magic" in rule.options[options.Mods]:
        if skill == "Magic":
            if level >= 6:
                mod_tool_rule = rule.can_earn_spell_count(10)
            else:
                mod_tool_rule = rule.can_earn_spell_count(5)
    if "Socializing Skill" in rule.options[options.Mods]:
        if skill == "Socializing":
            villager_count = 0
            for villager in all_villagers:
                if villager.mod_name in rule.options[options.Mods]:
                    if rule.can_earn_relationship(villager.name, level):
                        villager_count += 1
            if villager_count < level * 2:
                mod_tool_rule = False_()
    if "Archaeology" in rule.options[options.Mods]:
        if skill == "Archaeology":
            if level >= 6:
                mod_tool_rule = rule.can_do_panning() | rule.can_mine_in_the_mines_floor_81_120()
            else:
                mod_tool_rule = rule.can_do_panning() | rule.can_mine_in_the_mines_floor_1_40()
    if "Cooking Skill" in rule.options[options.Mods]:
        if skill == "Cooking":
            mod_tool_rule = rule.can_cook()
            # This really needs cooking tiers because better food gives more experience.
    if "Binning Skill" in rule.options[options.Mods]:
        if skill == "Binning":
            regions = [SVRegion.town, SVRegion.mountain]
            if level >= 6:
                mod_tool_rule = rule.can_reach_all_regions(regions) & rule.has("Recycling Machine")
            else:
                mod_tool_rule = rule.can_reach_region(SVRegion.town)
    if mod_tool_rule != tool_rule:
        return mod_tool_rule
    return tool_rule

    # Mod Logic
