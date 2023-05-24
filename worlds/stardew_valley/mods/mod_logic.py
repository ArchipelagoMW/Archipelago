from typing import List
from ..data.region_data import SVRegion
from .mod_data import ModNames
from ..data.villagers_data import all_villagers
from ..stardew_rule import Count, StardewRule
from .. import options
from ..options import StardewOptions

# Attempt to inject new methods into logic that can be easily commented out.


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


def can_earn_mod_skill_level(who, skill: str, level: int, tool_rule: StardewRule) -> StardewRule:
    mod_tool_rule = tool_rule
    if ModNames.luck_skill in who.options[options.Mods]:
        if skill == "Luck":
            mod_tool_rule = can_earn_luck_skill_level(who, level)
    if ModNames.magic in who.options[options.Mods]:
        if skill == "Magic":
            mod_tool_rule = can_earn_magic_skill_level(who, level)
    if ModNames.socializing_skill in who.options[options.Mods]:
        if skill == "Socializing":
            mod_tool_rule = can_earn_socializing_skill_level(who, level)
    if ModNames.archaeology in who.options[options.Mods]:
        if skill == "Archaeology":
            mod_tool_rule = can_earn_archaeology_skill_level(who, level)
    if ModNames.cooking_skill in who.options[options.Mods]:
        if skill == "Cooking":
            mod_tool_rule = can_earn_cooking_skill_level(who, level)
    if ModNames.binning_skill in who.options[options.Mods]:
        if skill == "Binning":
            mod_tool_rule = can_earn_binning_skill_level(who, level)
    if mod_tool_rule != tool_rule:
        return mod_tool_rule
    return tool_rule


def can_earn_luck_skill_level(who, level: int) -> StardewRule:
    if level >= 6:
        return who.can_fish_chests() | who.can_open_geode("Magma Geode")
    else:
        return who.can_fish_chests() | who.can_open_geode("Geode")

 
def can_earn_magic_skill_level(who, level: int) -> StardewRule:
    roof_count = min(level, 9)
    return who.can_earn_spell_count(roof_count)


def can_earn_socializing_skill_level(who, level: int) -> StardewRule:
    villager_count = []
    for villager in all_villagers:
        if villager.mod_name in who.options[options.Mods] or villager.mod_name is None:
            villager_count.append(who.can_earn_relationship(villager.name, level))
    return Count(level * 2, villager_count)


def can_earn_archaeology_skill_level(who, level: int) -> StardewRule:
    if level >= 6:
        return who.can_do_panning() | who.has_tool("Hoe", "Gold")
    else:
        return who.can_do_panning() | who.has_tool("Hoe", "Basic")


def can_earn_cooking_skill_level(who, level: int) -> StardewRule:
    if level >= 6:
        return who.can_cook() & who.can_fish() & who.can_reach_region(SVRegion.saloon) & \
                        who.has_building("Coop") & who.has_building("Barn")
    else:
        return who.can_cook()


def can_earn_binning_skill_level(who, level: int) -> StardewRule:
    if level >= 6:
        return who.can_reach_region(SVRegion.town) & who.has("Recycling Machine") & \
                        (who.can_fish() | who.can_crab_pot())
    else:
        return who.can_reach_region(SVRegion.town) | (who.has("Recycling Machine") &
                                                               (who.can_fish() | who.can_crab_pot()))
