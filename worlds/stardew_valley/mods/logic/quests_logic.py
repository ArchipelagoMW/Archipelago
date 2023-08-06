from typing import Iterable, Dict

from ...logic.has_logic import HasLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...strings.quest_names import ModQuest
from ..mod_data import ModNames
from ...strings.food_names import Meal, Beverage
from ...strings.monster_drop_names import Loot
from ...strings.villager_names import ModNPC
from ...strings.season_names import Season
from ...strings.region_names import Region
from ...stardew_rule import StardewRule


class QuestLogic:
    mods: Iterable[str]
    has: HasLogic
    region: RegionLogic
    season: SeasonLogic
    relationship: RelationshipLogic

    def __init__(self, mods: Iterable[str], has: HasLogic, region: RegionLogic, season: SeasonLogic, relationship: RelationshipLogic):
        self.mods = mods
        self.has = has
        self.region = region
        self.season = season
        self.relationship = relationship

    def get_modded_quest_rules(self) -> Dict[str, StardewRule]:
        quests = {}
        if ModNames.juna in self.mods:
            quests.update({
                ModQuest.JunaCola: self.relationship.has_hearts(ModNPC.juna, 3) & self.has(Beverage.joja_cola),
                ModQuest.JunaSpaghetti: self.relationship.has_hearts(ModNPC.juna, 6) & self.has(Meal.spaghetti)
            })

        if ModNames.ginger in self.mods:
            quests.update({
                ModQuest.MrGinger: self.relationship.has_hearts(ModNPC.mr_ginger, 6) & self.has(Loot.void_essence)
            })

        if ModNames.ayeisha in self.mods:
            quests.update({
                ModQuest.AyeishaEnvelope: (self.season.has(Season.spring) | self.season.has(Season.fall)) & self.region.can_reach(Region.mountain),
                ModQuest.AyeishaRing: self.season.has(Season.winter) & self.region.can_reach(Region.forest)
            })

        return quests
