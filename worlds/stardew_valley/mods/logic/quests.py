from typing import Union
from ...strings.quest_names import ModQuest
from ..mod_data import ModNames
from ...strings.food_names import Meal, Beverage
from ...strings.monster_drop_names import Loot
from ...strings.villager_names import ModNPC
from ...strings.season_names import Season
from ...strings.region_names import Region


def get_modded_quest_rules(vanilla_logic, active_mods):
    quests = {}
    if ModNames.juna in active_mods:
        quests.update({
            ModQuest.JunaCola: vanilla_logic.has_relationship(ModNPC.juna, 3) & vanilla_logic.has(Beverage.joja_cola),
            ModQuest.JunaSpaghetti: vanilla_logic.has_relationship(ModNPC.juna, 6) & vanilla_logic.has(Meal.spaghetti)
        })

    if ModNames.ginger in active_mods:
        quests.update({
            ModQuest.MrGinger: vanilla_logic.has_relationship(ModNPC.mr_ginger, 6) & vanilla_logic.has(Loot.void_essence)
        })

    if ModNames.ayeisha in active_mods:
        quests.update({
            ModQuest.AyeishaEnvelope: (vanilla_logic.has_season(Season.spring) | vanilla_logic.has_season(Season.fall)) &
                                      vanilla_logic.can_reach_region(Region.mountain),
            ModQuest.AyeishaRing: vanilla_logic.has_season(Season.winter) & vanilla_logic.can_reach_region(Region.forest)
        })

    return quests
