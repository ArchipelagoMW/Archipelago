from typing import Dict, Union

from ..mod_data import ModNames
from ...logic.base_logic import BaseLogic, BaseLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.time_logic import TimeLogicMixin
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


class ModQuestLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quest = ModQuestLogic(*args, **kwargs)


class ModQuestLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, TimeLogicMixin, SeasonLogicMixin, RelationshipLogicMixin]]):
    def get_modded_quest_rules(self) -> Dict[str, StardewRule]:
        quests = dict()
        quests.update(self._get_juna_quest_rules())
        quests.update(self._get_mr_ginger_quest_rules())
        quests.update(self._get_ayeisha_quest_rules())
        quests.update(self._get_sve_quest_rules())
        return quests

    def _get_juna_quest_rules(self):
        if ModNames.juna not in self.options.mods:
            return {}

        return {
            ModQuest.JunaCola: self.logic.relationship.has_hearts(ModNPC.juna, 3) & self.logic.has(Beverage.joja_cola),
            ModQuest.JunaSpaghetti: self.logic.relationship.has_hearts(ModNPC.juna, 6) & self.logic.has(Meal.spaghetti)
        }

    def _get_mr_ginger_quest_rules(self):
        if ModNames.ginger not in self.options.mods:
            return {}

        return {
            ModQuest.MrGinger: self.logic.relationship.has_hearts(ModNPC.mr_ginger, 6) & self.logic.has(Loot.void_essence)
        }

    def _get_ayeisha_quest_rules(self):
        if ModNames.ayeisha not in self.options.mods:
            return {}

        return {
            ModQuest.AyeishaEnvelope: (self.logic.season.has(Season.spring) | self.logic.season.has(Season.fall)),
            ModQuest.AyeishaRing: self.logic.season.has(Season.winter)
        }

    def _get_sve_quest_rules(self):
        if ModNames.sve not in self.options.mods:
            return {}

        return {
            ModQuest.RailroadBoulder: self.logic.received(Wallet.skull_key) & self.logic.has((Ore.iridium, Material.coal)) &
                                      self.logic.region.can_reach(Region.blacksmith) & self.logic.region.can_reach(Region.railroad),
            ModQuest.GrandpasShed: self.logic.has((Material.hardwood, MetalBar.iron, ArtisanGood.battery_pack, Material.stone)) &
                                   self.logic.region.can_reach(SVERegion.grandpas_shed_interior),
            ModQuest.MarlonsBoat: self.logic.has((Loot.void_essence, Loot.solar_essence, Loot.slime, Loot.bat_wing, Loot.bug_meat)) &
                                  self.logic.relationship.can_meet(ModNPC.lance) & self.logic.region.can_reach(SVERegion.guild_summit),
            ModQuest.AuroraVineyard: self.logic.has(Fruit.starfruit) & self.logic.region.can_reach(SVERegion.aurora_vineyard),
            ModQuest.MonsterCrops: self.logic.has((SVEVegetable.monster_mushroom, SVEFruit.slime_berry, SVEFruit.monster_fruit, SVEVegetable.void_root)),
            ModQuest.VoidSoul: self.logic.region.can_reach(Region.sewer) & self.logic.has(SVEForage.void_soul),
        }
