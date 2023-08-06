from typing import List, Iterable
from ...mods.mod_data import ModNames


def get_mod_skill_levels(mods: Iterable[str]) -> List[str]:
    skills_items = []
    if ModNames.luck_skill in mods:
        skills_items.append("Luck Level")
    if ModNames.socializing_skill in mods:
        skills_items.append("Socializing Level")
    if ModNames.magic in mods:
        skills_items.append("Magic Level")
    if ModNames.archaeology in mods:
        skills_items.append("Archaeology Level")
    if ModNames.binning_skill in mods:
        skills_items.append("Binning Level")
    if ModNames.cooking_skill in mods:
        skills_items.append("Cooking Level")
    return skills_items
