from typing import List
from worlds.stardew_valley.strings.region_names import Region
from .mod_data import ModNames
from ..data.villagers_data import all_villagers
from ..stardew_rule import Count, StardewRule, True_
from .. import options
from ..options import StardewOptions

# Attempt to inject new methods into logic that can be easily commented out.
from ..strings.skill_names import ModSkill


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


def can_earn_luck_skill_level(who, level: int) -> StardewRule:
    if level >= 6:
        return who.can_fish_chests() | who.can_open_geode("Magma Geode")
    else:
        return who.can_fish_chests() | who.can_open_geode("Geode")

 
def can_earn_magic_skill_level(who, level: int) -> StardewRule:
    spell_count = [who.received("Spell: Clear Debris"), who.received("Spell: Water"),
                   who.received("Spell: Blink"), who.received("Spell: Fireball"), who.received("Spell: Frostbite"),
                   who.received("Spell: Descend"), who.received("Spell: Tendrils"),
                   who.received("Spell: Shockwave"),
                   who.received("Spell: Meteor"),
                   who.received("Spell: Spirit")]
    return who.can_earn_spells() & Count(level, spell_count)


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
        return who.can_cook() & who.can_fish() & who.can_reach_region(Region.saloon) & \
               who.has_building("Coop") & who.has_building("Barn")
    else:
        return who.can_cook()


def can_earn_binning_skill_level(who, level: int) -> StardewRule:
    if level >= 6:
        return who.can_reach_region(Region.town) & who.has("Recycling Machine") & \
               (who.can_fish() | who.can_crab_pot())
    else:
        return who.can_reach_region(Region.town) | (who.has("Recycling Machine") &
                                                    (who.can_fish() | who.can_crab_pot()))
