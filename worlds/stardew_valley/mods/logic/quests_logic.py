from typing import Dict

from ...logic.has_logic import HasLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.time_logic import TimeLogic
from ...options import Mods
from ...strings.quest_names import ModQuest
from ..mod_data import ModNames
from ...strings.artisan_good_names import ArtisanGood
from ...strings.crop_names import Fruit
from ...strings.food_names import Meal, Beverage
from ...strings.monster_drop_names import Loot, ModLoot
from ...strings.villager_names import ModNPC
from ...strings.season_names import Season
from ...strings.region_names import Region, SVERegion
from ...strings.material_names import Material
from ...strings.metal_names import Ore, MetalBar
from ...strings.wallet_item_names import Wallet
from ...stardew_rule import StardewRule


class ModQuestLogic:
    mods: Mods
    has: HasLogic
    region: RegionLogic
    season: SeasonLogic
    relationship: RelationshipLogic
    received: ReceivedLogic
    time: TimeLogic

    def __init__(self, mods: Mods, has: HasLogic, region: RegionLogic, season: SeasonLogic, relationship: RelationshipLogic,
                 received: ReceivedLogic, time: TimeLogic):
        self.mods = mods
        self.has = has
        self.region = region
        self.season = season
        self.relationship = relationship
        self.received = received
        self.time = time

    def get_modded_quest_rules(self) -> Dict[str, StardewRule]:
        quests = dict()
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

        if ModNames.sve in self.mods:
            quests.update({
                ModQuest.RailroadBoulder: self.received(Wallet.skull_key) & self.has([Ore.iridium, Material.coal]) &
                                          self.region.can_reach(Region.blacksmith) & self.region.can_reach(Region.railroad),
                ModQuest.GrandpasShed: self.has([Material.hardwood, MetalBar.iron, ArtisanGood.battery_pack, Material.stone]) &
                                       self.region.can_reach(SVERegion.grandpas_shed_interior),
                ModQuest.MarlonsBoat: self.has([Loot.void_essence, Loot.solar_essence, Loot.slime, Loot.bat_wing, Loot.bug_meat]) &
                                      self.relationship.can_meet(ModNPC.lance) & self.region.can_reach(SVERegion.guild_summit),
                ModQuest.AuroraVineyard: self.has(Fruit.starfruit) & self.region.can_reach(SVERegion.aurora_vineyard),
                ModQuest.MonsterCrops: self.has([ModLoot.monster_mushroom, ModLoot.slime_berry, ModLoot.monster_fruit, ModLoot.void_root]),
                ModQuest.VoidSoul: self.region.can_reach(Region.sewer) & self.has(ModQuest.VoidSoul),
            })

        return quests
