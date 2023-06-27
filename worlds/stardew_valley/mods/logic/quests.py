from ...strings.quest_names import ModQuest
from ..mod_data import ModNames
from ...strings.food_names import Meal, Beverage
from ...strings.monster_drop_names import Loot
from ...strings.villager_names import ModNPC
from ...strings.season_names import Season
from ...strings.region_names import Region
from ...options import StardewOptions
from ... import options


def modded_quests(self, world_options: StardewOptions):
    quests = {}
    if ModNames.juna in world_options[options.Mods]:
        quests.update({
            ModQuest.JunaCola: self.has_relationship(ModNPC.juna, 3) & self.has(Beverage.joja_cola),
            ModQuest.JunaSpaghetti: self.has_relationship(ModNPC.juna, 6) & self.has(Meal.spaghetti)
        })

    if ModNames.ginger in world_options[options.Mods]:
        quests.update({
            ModQuest.MrGinger: self.has_relationship(ModNPC.mr_ginger, 6) & self.has(Loot.void_essence)
        })

    if ModNames.ayeisha in world_options[options.Mods]:
        quests.update({
            ModQuest.AyeishaEnvelope: (self.has_season(Season.spring) | self.has_season(Season.fall)) &
                                      self.can_reach_region(Region.mountain),
            ModQuest.AyeishaRing: self.has_season(Season.winter) & self.can_reach_region(Region.forest)
        })

    return quests
