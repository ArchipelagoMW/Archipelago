from typing import Dict, Union

from ..mod_data import ModNames
from ...data.craftable_data import all_crafting_recipes_by_name
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.crafting_logic import CraftingLogicMixin
from ...logic.crop_logic import CropLogicMixin
from ...logic.fishing_logic import FishingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogicMixin
from ...logic.museum_logic import MuseumLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...options import Cropsanity
from ...stardew_rule import StardewRule, True_
from ...strings.craftable_names import ModCraftable, ModEdible, ModMachine
from ...strings.crop_names import SVEVegetable, SVEFruit, DistantLandsCrop
from ...strings.fish_names import DistantLandsFish
from ...strings.food_names import SVEMeal, SVEBeverage
from ...strings.forageable_names import SVEForage, DistantLandsForageable
from ...strings.gift_names import SVEGift
from ...strings.metal_names import all_fossils, all_artifacts
from ...strings.monster_drop_names import ModLoot
from ...strings.region_names import Region, SVERegion
from ...strings.season_names import Season
from ...strings.seed_names import SVESeed, DistantLandsSeed
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import ModNPC

display_types = [ModCraftable.wooden_display, ModCraftable.hardwood_display]
display_items = all_artifacts + all_fossils


class ModItemLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = ModItemLogic(*args, **kwargs)


class ModItemLogic(BaseLogic[Union[CombatLogicMixin, ReceivedLogicMixin, CropLogicMixin, CookingLogicMixin, FishingLogicMixin, HasLogicMixin, MoneyLogicMixin,
RegionLogicMixin, SeasonLogicMixin, RelationshipLogicMixin, MuseumLogicMixin, ToolLogicMixin, CraftingLogicMixin]]):

    def get_modded_item_rules(self) -> Dict[str, StardewRule]:
        items = dict()
        if ModNames.sve in self.options.mods:
            items.update(self.get_sve_item_rules())
        if ModNames.archaeology in self.options.mods:
            items.update(self.get_archaeology_item_rules())
        if ModNames.distant_lands in self.options.mods:
            items.update(self.get_distant_lands_item_rules())
        return items

    def get_sve_item_rules(self):
        return {SVEGift.aged_blue_moon_wine: self.logic.money.can_spend_at(SVERegion.sophias_house, 28000),
                SVEGift.blue_moon_wine: self.logic.money.can_spend_at(SVERegion.sophias_house, 3000),
                SVESeed.fungus_seed: self.logic.region.can_reach(SVERegion.highlands_cavern) & self.logic.combat.has_good_weapon,
                ModLoot.green_mushroom: self.logic.region.can_reach(SVERegion.highlands) & self.logic.tool.has_tool(Tool.axe, ToolMaterial.iron),
                SVEFruit.monster_fruit: self.logic.season.has(Season.summer) & self.logic.has(SVESeed.stalk_seed),
                SVEVegetable.monster_mushroom: self.logic.season.has(Season.fall) & self.logic.has(SVESeed.fungus_seed),
                SVEForage.ornate_treasure_chest: self.logic.region.can_reach(SVERegion.highlands) & self.logic.combat.has_galaxy_weapon &
                                                 self.logic.tool.has_tool(Tool.axe, ToolMaterial.iron),
                SVEFruit.slime_berry: self.logic.season.has(Season.spring) & self.logic.has(SVESeed.slime_seed),
                SVESeed.slime_seed: self.logic.region.can_reach(SVERegion.highlands) & self.logic.combat.has_good_weapon,
                SVESeed.stalk_seed: self.logic.region.can_reach(SVERegion.highlands) & self.logic.combat.has_good_weapon,
                SVEForage.swirl_stone: self.logic.region.can_reach(SVERegion.crimson_badlands) & self.logic.combat.has_great_weapon,
                SVEVegetable.void_root: self.logic.season.has(Season.winter) & self.logic.has(SVESeed.void_seed),
                SVESeed.void_seed: self.logic.region.can_reach(SVERegion.highlands_cavern) & self.logic.combat.has_good_weapon,
                SVEForage.void_soul: self.logic.region.can_reach(
                    SVERegion.crimson_badlands) & self.logic.combat.has_good_weapon & self.logic.cooking.can_cook(),
                SVEForage.winter_star_rose: self.logic.region.can_reach(SVERegion.summit) & self.logic.season.has(Season.winter),
                SVEForage.bearberrys: self.logic.region.can_reach(Region.secret_woods) & self.logic.season.has(Season.winter),
                SVEForage.poison_mushroom: self.logic.region.can_reach(Region.secret_woods) & self.logic.season.has_any([Season.summer, Season.fall]),
                SVEForage.red_baneberry: self.logic.region.can_reach(Region.secret_woods) & self.logic.season.has(Season.summer),
                SVEForage.ferngill_primrose: self.logic.region.can_reach(SVERegion.summit) & self.logic.season.has(Season.spring),
                SVEForage.goldenrod: self.logic.region.can_reach(SVERegion.summit) & (
                            self.logic.season.has(Season.summer) | self.logic.season.has(Season.fall)),
                SVESeed.shrub_seed: self.logic.region.can_reach(Region.secret_woods) & self.logic.tool.has_tool(Tool.hoe, ToolMaterial.basic),
                SVEFruit.salal_berry: self.logic.crop.can_plant_and_grow_item([Season.spring, Season.summer]) & self.logic.has(SVESeed.shrub_seed),
                ModEdible.aegis_elixir: self.logic.money.can_spend_at(SVERegion.galmoran_outpost, 28000),
                ModEdible.lightning_elixir: self.logic.money.can_spend_at(SVERegion.galmoran_outpost, 12000),
                ModEdible.barbarian_elixir: self.logic.money.can_spend_at(SVERegion.galmoran_outpost, 22000),
                ModEdible.gravity_elixir: self.logic.money.can_spend_at(SVERegion.galmoran_outpost, 4000),
                SVESeed.ancient_ferns_seed: self.logic.region.can_reach(Region.secret_woods) & self.logic.tool.has_tool(Tool.hoe, ToolMaterial.basic),
                SVEVegetable.ancient_fiber: self.logic.crop.can_plant_and_grow_item(Season.summer) & self.logic.has(SVESeed.ancient_ferns_seed),
                SVEForage.big_conch: self.logic.region.can_reach_any((Region.beach, SVERegion.fable_reef)),
                SVEForage.dewdrop_berry: self.logic.region.can_reach(SVERegion.enchanted_grove),
                SVEForage.dried_sand_dollar: self.logic.region.can_reach(SVERegion.fable_reef) | (self.logic.region.can_reach(Region.beach) &
                                                                                                  self.logic.season.has_any([Season.summer, Season.fall])),
                "Galdoran Gem": self.logic.museum.can_complete_museum() & self.logic.relationship.has_hearts(ModNPC.marlon, 8),
                SVEForage.golden_ocean_flower: self.logic.region.can_reach(SVERegion.fable_reef),
                SVEMeal.grampleton_orange_chicken: self.logic.money.can_spend_at(Region.saloon, 650) & self.logic.relationship.has_hearts(ModNPC.sophia, 6),
                ModEdible.hero_elixir: self.logic.money.can_spend_at(SVERegion.isaac_shop, 8000),
                SVEForage.lucky_four_leaf_clover: self.logic.region.can_reach_any((Region.secret_woods, SVERegion.forest_west)) &
                                                  self.logic.season.has_any([Season.spring, Season.summer]),
                SVEForage.mushroom_colony: self.logic.region.can_reach_any((Region.secret_woods, SVERegion.junimo_woods, SVERegion.forest_west)) &
                                           self.logic.season.has(Season.fall),
                SVEForage.rusty_blade: self.logic.region.can_reach(SVERegion.crimson_badlands) & self.logic.combat.has_great_weapon,
                SVEForage.smelly_rafflesia: self.logic.region.can_reach(Region.secret_woods),
                SVEBeverage.sports_drink: self.logic.money.can_spend_at(Region.hospital, 750),
                "Stamina Capsule": self.logic.money.can_spend_at(Region.hospital, 4000),
                SVEForage.thistle: self.logic.region.can_reach(SVERegion.summit),
                SVEForage.void_pebble: self.logic.region.can_reach(SVERegion.crimson_badlands) & self.logic.combat.has_great_weapon,
                ModLoot.void_shard: self.logic.region.can_reach(SVERegion.crimson_badlands) & self.logic.combat.has_galaxy_weapon
                }
        # @formatter:on

    def get_archaeology_item_rules(self):
        archaeology_item_rules = {}
        preservation_chamber_rule = self.logic.has(ModMachine.preservation_chamber)
        hardwood_preservation_chamber_rule = self.logic.has(ModMachine.hardwood_preservation_chamber)
        for item in display_items:
            for display_type in display_types:
                location_name = f"{display_type}: {item}"
                display_item_rule = self.logic.crafting.can_craft(all_crafting_recipes_by_name[display_type]) & self.logic.has(item)
                if "Wooden" in display_type:
                    archaeology_item_rules[location_name] = display_item_rule & preservation_chamber_rule
                else:
                    archaeology_item_rules[location_name] = display_item_rule & hardwood_preservation_chamber_rule
        return archaeology_item_rules

    def get_distant_lands_item_rules(self):
        return{
            DistantLandsForageable.swamp_herb: self.logic.region.can_reach(Region.witch_swamp),
            DistantLandsForageable.brown_amanita: self.logic.region.can_reach(Region.witch_swamp),
            DistantLandsFish.purple_algae: self.logic.fishing.can_fish_at(Region.witch_swamp),
            DistantLandsSeed.vile_ancient_fruit: self.logic.money.can_spend_at(Region.oasis, 50) & self.pseudo_cropsanity_check(DistantLandsSeed.vile_ancient_fruit),
            DistantLandsSeed.void_mint: self.logic.money.can_spend_at(Region.oasis, 80) & self.pseudo_cropsanity_check(DistantLandsSeed.void_mint),
            DistantLandsCrop.void_mint: self.logic.has(DistantLandsSeed.void_mint),
            DistantLandsCrop.vile_ancient_fruit: self.logic.has(DistantLandsSeed.vile_ancient_fruit)
        }

    # Items that don't behave enough like a crop but enough to warrant a portion of the cropsanity logic.
    def pseudo_cropsanity_check(self, seed_name: str):
        if self.options.cropsanity == Cropsanity.option_disabled:
            return True_()
        return self.logic.received(seed_name)
