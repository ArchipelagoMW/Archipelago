from typing import Dict

from ..mod_data import ModNames
from ...logic.has_logic import HasLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.time_logic import TimeLogic
from ...options import Mods
from ...stardew_rule import StardewRule
from ...strings.artisan_good_names import ArtisanGood
from ...strings.crop_names import Fruit, SVEFruit, SVEVegetable
from ...strings.food_names import Meal, Beverage
from ...strings.forageable_names import SVEForage
from ...strings.material_names import Material
from ...strings.metal_names import Ore, MetalBar
from ...strings.monster_drop_names import Loot
from ...strings.quest_names import ModQuest
from ...strings.region_names import Region, SVERegion
from ...strings.season_names import Season
from ...strings.villager_names import ModNPC
from ...strings.wallet_item_names import Wallet


class ModQuestLogic:
    mods: Mods
    received: ReceivedLogicMixin
    has: HasLogicMixin
    region: RegionLogicMixin
    time: TimeLogic
    season: SeasonLogic
    relationship: RelationshipLogic

    def __init__(self, mods: Mods, received: ReceivedLogicMixin, has: HasLogicMixin, region: RegionLogicMixin, time: TimeLogic, season: SeasonLogic,
                 relationship: RelationshipLogic, ):
        self.mods = mods
        self.received = received
        self.has = has
        self.region = region
        self.time = time
        self.season = season
        self.relationship = relationship

    def get_modded_quest_rules(self) -> Dict[str, StardewRule]:
        quests = dict()
        quests.update(self._get_juna_quest_rules())
        quests.update(self._get_mr_ginger_quest_rules())
        quests.update(self._get_ayeisha_quest_rules())
        quests.update(self._get_sve_quest_rules())
        return quests

    def _get_juna_quest_rules(self):
        if ModNames.juna not in self.mods:
            return {}

        return {
            ModQuest.JunaCola: self.relationship.has_hearts(ModNPC.juna, 3) & self.has(Beverage.joja_cola),
            ModQuest.JunaSpaghetti: self.relationship.has_hearts(ModNPC.juna, 6) & self.has(Meal.spaghetti)
        }

    def _get_mr_ginger_quest_rules(self):
        if ModNames.ginger not in self.mods:
            return {}

        return {
            ModQuest.MrGinger: self.relationship.has_hearts(ModNPC.mr_ginger, 6) & self.has(Loot.void_essence)
        }

    def _get_ayeisha_quest_rules(self):
        if ModNames.ayeisha not in self.mods:
            return {}

        return {
            ModQuest.AyeishaEnvelope: (self.season.has(Season.spring) | self.season.has(Season.fall)),
            ModQuest.AyeishaRing: self.season.has(Season.winter)
        }

    def _get_sve_quest_rules(self):
        if ModNames.sve not in self.mods:
            return {}

        return {
            ModQuest.RailroadBoulder: self.received(Wallet.skull_key) & self.has((Ore.iridium, Material.coal)) &
                                      self.region.can_reach(Region.blacksmith) & self.region.can_reach(Region.railroad),
            ModQuest.GrandpasShed: self.has((Material.hardwood, MetalBar.iron, ArtisanGood.battery_pack, Material.stone)) &
                                   self.region.can_reach(SVERegion.grandpas_shed_interior),
            ModQuest.MarlonsBoat: self.has((Loot.void_essence, Loot.solar_essence, Loot.slime, Loot.bat_wing, Loot.bug_meat)) &
                                  self.relationship.can_meet(ModNPC.lance) & self.region.can_reach(SVERegion.guild_summit),
            ModQuest.AuroraVineyard: self.has(Fruit.starfruit) & self.region.can_reach(SVERegion.aurora_vineyard),
            ModQuest.MonsterCrops: self.has((SVEVegetable.monster_mushroom, SVEFruit.slime_berry, SVEFruit.monster_fruit, SVEVegetable.void_root)),
            ModQuest.VoidSoul: self.region.can_reach(Region.sewer) & self.has(SVEForage.void_soul),
        }
