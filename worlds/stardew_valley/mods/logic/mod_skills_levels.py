from typing import Tuple

from ...mods.mod_data import ModNames
from ...options import Mods
from ...strings.ap_names.mods.mod_items import SkillLevel


def get_mod_skill_levels(mods: Mods) -> Tuple[str]:
    skills_items = []
    if ModNames.luck_skill in mods:
        skills_items.append(SkillLevel.luck)
    if ModNames.socializing_skill in mods:
        skills_items.append(SkillLevel.socializing)
    if ModNames.magic in mods:
        skills_items.append(SkillLevel.magic)
    if ModNames.archaeology in mods:
        skills_items.append(SkillLevel.archaeology)
    if ModNames.binning_skill in mods:
        skills_items.append(SkillLevel.binning)
    if ModNames.cooking_skill in mods:
        skills_items.append(SkillLevel.cooking)
    return tuple(skills_items)
