from typing import Dict

from ...logic.combat_logic import CombatLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.has_logic import HasLogic
from ...logic.money_logic import MoneyLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.tool_logic import ToolLogic
from ...options import Mods
from ..mod_data import ModNames
from ...strings.crop_names import SVEVegetable, SVEFruit
from ...strings.fish_names import Fish, SVEFish
from ...strings.ingredient_names import Ingredient
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import NPC
from ...strings.food_names import Meal
from ...strings.forageable_names import SVEForage
from ...strings.monster_drop_names import Loot, ModLoot
from ...strings.season_names import Season
from ...strings.region_names import Region, SVERegion
from ...stardew_rule import StardewRule


class ModItemLogic:
    mods: Mods
    combat: CombatLogic
    cooking: CookingLogic
    has: HasLogic
    money: MoneyLogic
    region: RegionLogic
    season: SeasonLogic
    relationship: RelationshipLogic
    received: ReceivedLogic
    tool: ToolLogic

    def __init__(self, mods: Mods, combat: CombatLogic, cooking: CookingLogic, has: HasLogic, money: MoneyLogic, region: RegionLogic,
                 season: SeasonLogic, relationship: RelationshipLogic, tool: ToolLogic):
        self.combat = combat
        self.cooking = cooking
        self.mods = mods
        self.has = has
        self.money = money
        self.region = region
        self.season = season
        self.relationship = relationship
        self.tool = tool

    def get_modded_item_rules(self) -> Dict[str, StardewRule]:
        items = dict()
        if ModNames.sve in self.mods:
            items.update({
                "Aged Blue Moon Wine": self.region.can_reach(SVERegion.sophias_house) & self.money.can_spend(28000),
                "Big Bark Burger": self.cooking.can_cook() & self.has([SVEFish.puppyfish, Meal.bread, Ingredient.oil]) &
                                   self.relationship.has_hearts(NPC.gus, 5) & self.money.can_spend(5500) &
                                   self.region.can_reach(Region.saloon),
                "Blue Moon Wine": self.region.can_reach(SVERegion.sophias_house) & self.money.can_spend(3000),
                ModLoot.fungus_seed: self.region.can_reach(SVERegion.highlands_cavern) & self.combat.has_good_weapon(),
                "Glazed Butterfish": self.cooking.can_cook() & self.has([SVEFish.butterfish, Ingredient.wheat_flour, Ingredient.oil]) &
                                     self.relationship.has_hearts(NPC.gus, 10) & self.money.can_spend(
                    4000) & self.region.can_reach(Region.saloon),
                "Green Mushroom": self.region.can_reach(SVERegion.highlands) & self.tool.has_tool(Tool.axe, ToolMaterial.iron),
                SVEFruit.monster_fruit: self.season.has(Season.summer) & self.has(ModLoot.stalk_seed),
                SVEVegetable.monster_mushroom: self.season.has(Season.fall) & self.has(ModLoot.fungus_seed),
                SVEForage.ornate_treasure_chest: self.region.can_reach(SVERegion.highlands) & self.combat.has_galaxy_weapon() &
                                                 self.tool.has_tool(Tool.axe,ToolMaterial.iron),
                SVEFruit.slime_berry: self.season.has(Season.spring) & self.has(ModLoot.slime_seed),
                ModLoot.slime_seed: self.region.can_reach(SVERegion.highlands) & self.combat.has_good_weapon(),
                ModLoot.stalk_seed: self.region.can_reach(SVERegion.highlands) & self.combat.has_good_weapon(),
                SVEForage.swirl_stone: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_great_weapon(),
                "Void Delight": self.has(SVEFish.void_eel) & self.has(Loot.void_essence) & self.has(Loot.solar_essence),
                SVEForage.void_pebble: self.region.can_reach(
                    SVERegion.crimson_badlands) & self.combat.has_galaxy_weapon(),
                SVEVegetable.void_root: self.season.has(Season.winter) & self.has(ModLoot.void_seed),
                "Void Salmon Sushi": self.has(Fish.void_salmon) & self.has("Void Mayonnaise") & self.has("Seaweed"),
                ModLoot.void_seed: self.region.can_reach(SVERegion.highlands_cavern) & self.combat.has_good_weapon(),
                SVEForage.void_soul: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_good_weapon() &
                                     self.cooking.can_cook(),
            })

        return items
