from typing import Dict, Union

from ..mod_data import ModNames
from ...logic.base_logic import BaseLogic, BaseLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.monster_logic import MonsterLogicMixin
from ...logic.quest_logic import QuestLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.time_logic import TimeLogicMixin
from ...stardew_rule import StardewRule
from ...strings.animal_product_names import AnimalProduct
from ...strings.ap_names.mods.mod_items import SVEQuestItem
from ...strings.artisan_good_names import ArtisanGood
from ...strings.crop_names import Fruit, SVEFruit, SVEVegetable, Vegetable
from ...strings.fertilizer_names import Fertilizer
from ...strings.food_names import Meal, Beverage
from ...strings.material_names import Material
from ...strings.metal_names import Ore, MetalBar
from ...strings.monster_drop_names import Loot, ModLoot
from ...strings.monster_names import Monster
from ...strings.quest_names import Quest, ModQuest
from ...strings.region_names import Region, SVERegion, BoardingHouseRegion
from ...strings.season_names import Season
from ...strings.villager_names import ModNPC, NPC
from ...strings.wallet_item_names import Wallet


class ModQuestLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quest = ModQuestLogic(*args, **kwargs)


class ModQuestLogic(BaseLogic[Union[HasLogicMixin, QuestLogicMixin, ReceivedLogicMixin, RegionLogicMixin,
TimeLogicMixin, SeasonLogicMixin, RelationshipLogicMixin, MonsterLogicMixin]]):
    def get_modded_quest_rules(self) -> Dict[str, StardewRule]:
        quests = dict()
        quests.update(self._get_juna_quest_rules())
        quests.update(self._get_mr_ginger_quest_rules())
        quests.update(self._get_ayeisha_quest_rules())
        quests.update(self._get_sve_quest_rules())
        quests.update(self._get_distant_lands_quest_rules())
        quests.update(self._get_boarding_house_quest_rules())
        quests.update((self._get_hat_mouse_quest_rules()))
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
            ModQuest.RailroadBoulder: self.logic.received(Wallet.skull_key) & self.logic.has_all(*(Ore.iridium, Material.coal)) &
                                      self.logic.region.can_reach(Region.blacksmith) & self.logic.region.can_reach(Region.railroad),
            ModQuest.GrandpasShed: self.logic.has_all(*(Material.hardwood, MetalBar.iron, ArtisanGood.battery_pack, Material.stone)) &
                                   self.logic.region.can_reach(SVERegion.grandpas_shed),
            ModQuest.MarlonsBoat: self.logic.has_all(*(Loot.void_essence, Loot.solar_essence, Loot.slime, Loot.bat_wing, Loot.bug_meat)) &
                                  self.logic.relationship.can_meet(ModNPC.lance) & self.logic.region.can_reach(SVERegion.guild_summit),
            ModQuest.AuroraVineyard: self.logic.region.can_reach(SVERegion.aurora_vineyard) & self.logic.received(SVEQuestItem.aurora_vineyard_tablet) &
                                     self.logic.has(Fruit.starfruit) & self.logic.region.can_reach(Region.forest),
            ModQuest.MonsterCrops: self.logic.has_all(*(SVEVegetable.monster_mushroom, SVEFruit.slime_berry, SVEFruit.monster_fruit, SVEVegetable.void_root)),
            ModQuest.VoidSoul: self.logic.has(ModLoot.void_soul) & self.logic.region.can_reach(Region.farm) &
                               self.logic.season.has_any_not_winter() & self.logic.region.can_reach(SVERegion.badlands_entrance) &
                               self.logic.relationship.has_hearts(NPC.krobus, 10) & self.logic.quest.can_complete_quest(ModQuest.MonsterCrops) &
                               self.logic.monster.can_kill_any((Monster.shadow_brute, Monster.shadow_shaman, Monster.shadow_sniper)),
        }

    def has_completed_aurora_vineyard_bundle(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.aurora_vineyard_reclamation)
        return self.logic.quest.can_complete_quest(ModQuest.AuroraVineyard)


    def _get_distant_lands_quest_rules(self):
        if ModNames.distant_lands not in self.options.mods:
            return {}

        return {
            ModQuest.CorruptedCropsTask: self.logic.region.can_reach(Region.wizard_tower) & self.logic.has(Fertilizer.deluxe) &
                                         self.logic.quest.can_complete_quest(Quest.magic_ink),
            ModQuest.WitchOrder: self.logic.region.can_reach(Region.witch_swamp) & self.logic.has(Fertilizer.deluxe) &
                                 self.logic.quest.can_complete_quest(Quest.magic_ink),
            ModQuest.ANewPot: self.logic.region.can_reach(Region.saloon) &
                              self.logic.region.can_reach(Region.sam_house) & self.logic.region.can_reach(Region.pierre_store) &
                              self.logic.region.can_reach(Region.blacksmith) & self.logic.has(MetalBar.iron) & self.logic.relationship.has_hearts(ModNPC.goblin,
                                                                                                                                                  6),
            ModQuest.FancyBlanketTask: self.logic.region.can_reach(Region.haley_house) & self.logic.has(AnimalProduct.wool) &
                                       self.logic.has(ArtisanGood.cloth) & self.logic.relationship.has_hearts(ModNPC.goblin, 10) &
                                       self.logic.relationship.has_hearts(NPC.emily, 8) & self.logic.season.has(Season.winter)

        }

    def _get_boarding_house_quest_rules(self):
        if ModNames.boarding_house not in self.options.mods:
            return {}

        return {
            ModQuest.PumpkinSoup: self.logic.region.can_reach(BoardingHouseRegion.boarding_house_first) & self.logic.has(Vegetable.pumpkin)
        }

    def _get_hat_mouse_quest_rules(self):
        if ModNames.lacey not in self.options.mods:
            return {}

        return {
            ModQuest.HatMouseHat: self.logic.relationship.has_hearts(ModNPC.lacey, 2) & self.logic.time.has_lived_months(4)
        }
