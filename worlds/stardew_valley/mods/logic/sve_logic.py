from typing import Dict
from dataclasses import field, dataclass

from ...logic.action_logic import ActionLogic
from ...logic.building_logic import BuildingLogic
from ...logic.combat_logic import CombatLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.fishing_logic import FishingLogic
from ...logic.has_logic import HasLogic
from ...logic.money_logic import MoneyLogic
from ...logic.quest_logic import QuestLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.time_logic import TimeLogic
from ...logic.tool_logic import ToolLogic
from ..mod_regions import SVERegion
from ...options import SkillProgression
from ...strings.crop_names import SVEVegetable, SVEFruit
from ...strings.fish_names import Fish, SVEFish
from ...strings.forageable_names import SVEForage
from ...strings.ingredient_names import Ingredient
from ...strings.food_names import Meal
from ...strings.monster_drop_names import Loot, ModLoot
from ...strings.region_names import Region
from ...strings.season_names import Season
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import NPC
from ...stardew_rule import StardewRule, Or


@dataclass(frozen=False, repr=False)
class SVELogic:
    player: int
    received: ReceivedLogic
    has: HasLogic
    quest: QuestLogic
    region: RegionLogic
    relationship: RelationshipLogic
    time: TimeLogic
    tool: ToolLogic
    fishing: FishingLogic
    cooking: CookingLogic
    money: MoneyLogic
    combat: CombatLogic
    season: SeasonLogic

    sve_location_rules: Dict[str, StardewRule] = field(default_factory=dict)

    def __init__(self, player: int, skill_option: SkillProgression, received: ReceivedLogic, has: HasLogic, quest: QuestLogic, region: RegionLogic, action: ActionLogic,
                 relationship: RelationshipLogic, building: BuildingLogic, tool: ToolLogic, fishing: FishingLogic, cooking: CookingLogic,
                 money: MoneyLogic, combat: CombatLogic, season: SeasonLogic, time: TimeLogic):
        self.player = player
        self.skill_option = skill_option
        self.received = received
        self.has = has
        self.quest = quest
        self.region = region
        self.action = action
        self.relationship = relationship
        self.building = building
        self.tool = tool
        self.fishing = fishing
        self.cooking = cooking
        self.time = time
        self.money = money
        self.combat = combat
        self.season = season

        self.sve_location_rules.update({
            "Bear: Baked Berry Oatmeal Recipe": self.quest.can_complete_quest("Strange Note") & self.money.can_spend(
                12500),
            "Bear: Flower Cookie Recipe": self.quest.can_complete_quest("Strange Note") & self.money.can_spend(8750),
            "Purple Junimo: Super Starfruit": self.relationship.has_hearts("Apples", 10) &
                                              self.region.can_reach(
                                                  SVERegion.purple_junimo_shop) & self.money.can_spend(80000),
            "Alesia: Tempered Galaxy Dagger": self.region.can_reach(
                SVERegion.alesia_shop) & self.combat.has_galaxy_weapon() &
                                              self.money.can_spend(350000) & self.time.has_lived_months(3),
            "Issac: Tempered Galaxy Sword": self.region.can_reach(
                SVERegion.issac_shop) & self.combat.has_galaxy_weapon() &
                                            self.money.can_spend(600000),
            "Issac: Tempered Galaxy Hammer": self.region.can_reach(
                SVERegion.issac_shop) & self.combat.has_galaxy_weapon() &
                                             self.money.can_spend(400000),
            "Lance's Diamond Wand": self.quest.can_complete_quest("Monster Crops") & self.region.can_reach(
                SVERegion.lances_house),
        })

    def set_sve_item_rules(self, items: Dict[str, StardewRule]):
        items.update({
            "Aged Blue Moon Wine": self.region.can_reach(SVERegion.sophias_house) & self.money.can_spend(28000),
            "Big Bark Burger": self.cooking.can_cook() & self.has([SVEFish.puppyfish, Meal.bread, Ingredient.oil]) &
                               self.relationship.has_hearts(NPC.gus, 5) & self.money.can_spend(5500) &
                               self.region.can_reach(Region.saloon),
            "Blue Moon Wine": self.region.can_reach(SVERegion.sophias_house) & self.money.can_spend(3000),
            ModLoot.fungus_seed: self.region.can_reach(SVERegion.highlands_cavern) & self.combat.has_good_weapon(),
            "Glazed Butterfish": self.cooking.can_cook() & self.has([SVEFish.butterfish, Ingredient.wheat_flour, Ingredient.oil]) &
                                 self.relationship.has_hearts(NPC.gus, 10) & self.money.can_spend(4000) & self.region.can_reach(Region.saloon),
            "Green Mushroom": self.region.can_reach(SVERegion.highlands) & self.tool.has_tool(Tool.axe, ToolMaterial.iron),
            SVEFruit.monster_fruit: self.season.has(Season.summer) & self.has(ModLoot.stalk_seed),
            SVEVegetable.monster_mushroom: self.has(Season.fall) & self.has(ModLoot.fungus_seed),
            SVEForage.ornate_treasure_chest: self.region.can_reach(SVERegion.highlands) & self.combat.has_galaxy_weapon() &
                                             self.cooking.can_cook() & self.tool.has_tool(Tool.axe, ToolMaterial.iron),
            SVEFruit.slime_berry: self.season.has(Season.spring) & self.has(ModLoot.slime_seed),
            ModLoot.slime_seed: self.region.can_reach(SVERegion.highlands) & self.combat.has_good_weapon(),
            ModLoot.stalk_seed: self.region.can_reach(SVERegion.highlands) & self.combat.has_good_weapon(),
            SVEForage.swirl_stone: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_great_weapon(),
            "Void Delight": self.has(SVEFish.void_eel) & self.has(Loot.void_essence) & self.has(Loot.solar_essence),
            SVEForage.void_pebble: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_galaxy_weapon(),
            SVEVegetable.void_root: self.season.has(Season.winter) & self.has(ModLoot.void_seed),
            "Void Salmon Sushi": self.has(Fish.void_salmon) & self.has("Void Mayonnaise") & self.has("Seaweed"),
            ModLoot.void_seed: self.region.can_reach(SVERegion.highlands_cavern) & self.combat.has_good_weapon(),
            SVEForage.void_soul: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_good_weapon() &
                                 self.cooking.can_cook(),
        })

    def has_any_rune(self):
        rune_list = ["Nexus: Adventurer's Guild Runes", "Nexus: Junimo Woods Runes", "Nexus: Aurora Vineyard Runes", "Nexus: Sprite Spring Runes",
                     "Nexus: Outpost Runes"]
        return Or([self.received(rune) for rune in rune_list])

