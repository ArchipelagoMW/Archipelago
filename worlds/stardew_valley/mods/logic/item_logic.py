from typing import Dict

from ...logic.combat_logic import CombatLogic
from ...logic.cooking_logic import CookingLogic
from ...logic.crop_logic import CropLogic
from ...logic.has_logic import HasLogic
from ...logic.money_logic import MoneyLogic
from ...logic.museum_logic import MuseumLogic
from ...logic.region_logic import RegionLogic
from ...logic.relationship_logic import RelationshipLogic
from ...logic.season_logic import SeasonLogic
from ...logic.received_logic import ReceivedLogic
from ...logic.tool_logic import ToolLogic
from ...logic.crafting_logic import CraftingLogic
from ...options import Mods
from ..mod_data import ModNames
from ...strings.crop_names import SVEVegetable, SVEFruit
from ...strings.food_names import SVEMeal, SVEBeverage
from ...strings.gift_names import SVEGift
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.forageable_names import SVEForage
from ...strings.monster_drop_names import ModLoot
from ...strings.season_names import Season
from ...strings.seed_names import SVESeed
from ...strings.region_names import Region, SVERegion
from ...stardew_rule import StardewRule


class ModItemLogic:
    mods: Mods
    combat: CombatLogic
    crop: CropLogic
    cooking: CookingLogic
    has: HasLogic
    money: MoneyLogic
    region: RegionLogic
    season: SeasonLogic
    relationship: RelationshipLogic
    museum: MuseumLogic
    received: ReceivedLogic
    tool: ToolLogic
    crafting: CraftingLogic

    def __init__(self, mods: Mods, combat: CombatLogic, crop: CropLogic, cooking: CookingLogic, has: HasLogic, money: MoneyLogic,
                 region: RegionLogic, season: SeasonLogic, relationship: RelationshipLogic, museum: MuseumLogic, tool: ToolLogic, crafting: CraftingLogic):
        self.combat = combat
        self.crop = crop
        self.cooking = cooking
        self.mods = mods
        self.has = has
        self.money = money
        self.region = region
        self.season = season
        self.relationship = relationship
        self.museum = museum
        self.tool = tool
        self.crafting = crafting

    def get_modded_item_rules(self) -> Dict[str, StardewRule]:
        items = dict()
        if ModNames.sve in self.mods:
            items.update(self._get_sve_item_rules())

        return items

    def _get_sve_item_rules(self):
        return {SVEGift.aged_blue_moon_wine: self.money.can_spend_at(SVERegion.sophias_house, 28000),
                SVEGift.blue_moon_wine: self.money.can_spend_at(SVERegion.sophias_house, 3000),
                SVESeed.fungus_seed: self.region.can_reach(SVERegion.highlands_cavern) & self.combat.has_good_weapon,
                ModLoot.green_mushroom: self.region.can_reach(SVERegion.highlands) & self.tool.has_tool(Tool.axe, ToolMaterial.iron),
                SVEFruit.monster_fruit: self.season.has(Season.summer) & self.has(SVESeed.stalk_seed),
                SVEVegetable.monster_mushroom: self.season.has(Season.fall) & self.has(SVESeed.fungus_seed),
                SVEForage.ornate_treasure_chest: self.region.can_reach(SVERegion.highlands) & self.combat.has_galaxy_weapon &
                                                 self.tool.has_tool(Tool.axe,ToolMaterial.iron),
                SVEFruit.slime_berry: self.season.has(Season.spring) & self.has(SVESeed.slime_seed),
                SVESeed.slime_seed: self.region.can_reach(SVERegion.highlands) & self.combat.has_good_weapon,
                SVESeed.stalk_seed: self.region.can_reach(SVERegion.highlands) & self.combat.has_good_weapon,
                SVEForage.swirl_stone: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_great_weapon,
                SVEVegetable.void_root: self.season.has(Season.winter) & self.has(SVESeed.void_seed),
                SVESeed.void_seed: self.region.can_reach(SVERegion.highlands_cavern) & self.combat.has_good_weapon,
                SVEForage.void_soul: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_good_weapon & self.cooking.can_cook(),
                SVEForage.winter_star_rose: self.region.can_reach(SVERegion.summit) & self.season.has(Season.winter),
                SVEForage.bearberrys: self.region.can_reach(Region.secret_woods) & self.season.has(Season.winter),
                SVEForage.poison_mushroom: self.region.can_reach(Region.secret_woods) & self.season.has_any([Season.summer, Season.fall]),
                SVEForage.red_baneberry: self.region.can_reach(Region.secret_woods) & self.season.has(Season.summer),
                SVEForage.ferngill_primrose: self.region.can_reach(SVERegion.summit) & self.season.has(Season.spring),
                SVEForage.goldenrod: self.region.can_reach(SVERegion.summit) & (self.season.has(Season.summer) | self.season.has(Season.fall)),
                SVESeed.shrub_seed: self.region.can_reach(Region.secret_woods) & self.tool.has_tool(Tool.hoe, ToolMaterial.basic),
                SVEFruit.salal_berry: self.crop.can_plant_and_grow_item([Season.spring, Season.summer]) & self.has(SVESeed.shrub_seed),
                ModEdible.aegis_elixir: self.money.can_spend_at(SVERegion.galmoran_outpost, 28000),
                ModEdible.lightning_elixir: self.money.can_spend_at(SVERegion.galmoran_outpost, 12000),
                ModEdible.barbarian_elixir: self.money.can_spend_at(SVERegion.galmoran_outpost, 22000),
                ModEdible.gravity_elixir: self.money.can_spend_at(SVERegion.galmoran_outpost, 4000),
                SVESeed.ancient_ferns_seed: self.region.can_reach(Region.secret_woods) & self.tool.has_tool(Tool.hoe, ToolMaterial.basic),
                SVEVegetable.ancient_fiber: self.crop.can_plant_and_grow_item(Season.summer) & self.has(SVESeed.ancient_ferns_seed),
                SVEForage.big_conch: self.region.can_reach_any((Region.beach, SVERegion.fable_reef)),
                SVEForage.dewdrop_berry: self.region.can_reach(SVERegion.enchanted_grove),
                SVEForage.dried_sand_dollar: self.region.can_reach(SVERegion.fable_reef) | (self.region.can_reach(Region.beach) &
                                                                                            self.season.has_any([Season.summer, Season.fall])),
                "Galdoran Gem": self.museum.can_complete_museum() & self.relationship.has_hearts(ModNPC.marlon, 8),
                SVEForage.golden_ocean_flower: self.region.can_reach(SVERegion.fable_reef),
                SVEMeal.grampleton_orange_chicken: self.money.can_spend_at(Region.saloon, 650),
                ModEdible.hero_elixir: self.money.can_spend_at(SVERegion.issac_shop, 8000),
                SVEForage.lucky_four_leaf_clover: self.region.can_reach_any((Region.secret_woods, SVERegion.forest_west)) &
                                                  self.season.has_any([Season.spring, Season.summer]),
                SVEForage.mushroom_colony: self.region.can_reach_any((Region.secret_woods, SVERegion.junimo_woods, SVERegion.forest_west)) &
                                           self.season.has(Season.fall),
                SVEForage.rusty_blade: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_great_weapon,
                SVEForage.smelly_rafflesia: self.region.can_reach(Region.secret_woods),
                SVEBeverage.sports_drink: self.money.can_spend_at(Region.hospital, 750),
                "Stamina Capsule": self.money.can_spend_at(Region.hospital, 4000),
                SVEForage.thistle: self.region.can_reach(SVERegion.summit),
                SVEForage.void_pebble: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_great_weapon,
                ModLoot.void_shard: self.region.can_reach(SVERegion.crimson_badlands) & self.combat.has_galaxy_weapon
                }
