from typing import Dict, Union

from ..mod_data import ModNames
from ... import options
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
from ...logic.quest_logic import QuestLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.season_logic import SeasonLogicMixin
from ...logic.skill_logic import SkillLogicMixin
from ...logic.time_logic import TimeLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...options import Cropsanity
from ...stardew_rule import StardewRule, True_
from ...strings.artisan_good_names import ModArtisanGood
from ...strings.craftable_names import ModCraftable, ModEdible, ModMachine
from ...strings.crop_names import SVEVegetable, SVEFruit, DistantLandsCrop, Fruit
from ...strings.fish_names import WaterItem
from ...strings.flower_names import Flower
from ...strings.food_names import SVEMeal, SVEBeverage
from ...strings.forageable_names import SVEForage, DistantLandsForageable, Forageable
from ...strings.gift_names import SVEGift
from ...strings.ingredient_names import Ingredient
from ...strings.material_names import Material
from ...strings.metal_names import all_fossils, all_artifacts, Ore, ModFossil
from ...strings.monster_drop_names import ModLoot, Loot
from ...strings.performance_names import Performance
from ...strings.quest_names import ModQuest
from ...strings.region_names import Region, SVERegion, DeepWoodsRegion, BoardingHouseRegion
from ...strings.season_names import Season
from ...strings.seed_names import SVESeed, DistantLandsSeed
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import ModNPC

display_types = [ModCraftable.wooden_display, ModCraftable.hardwood_display]
display_items = all_artifacts + all_fossils


class ModItemLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = ModItemLogic(*args, **kwargs)


class ModItemLogic(BaseLogic[Union[CombatLogicMixin, ReceivedLogicMixin, CropLogicMixin, CookingLogicMixin, FishingLogicMixin, HasLogicMixin, MoneyLogicMixin,
RegionLogicMixin, SeasonLogicMixin, RelationshipLogicMixin, MuseumLogicMixin, ToolLogicMixin, CraftingLogicMixin, SkillLogicMixin, TimeLogicMixin, QuestLogicMixin]]):

    def get_modded_item_rules(self) -> Dict[str, StardewRule]:
        items = dict()
        if ModNames.sve in self.options.mods:
            items.update(self.get_sve_item_rules())
        if ModNames.archaeology in self.options.mods:
            items.update(self.get_archaeology_item_rules())
        if ModNames.distant_lands in self.options.mods:
            items.update(self.get_distant_lands_item_rules())
        if ModNames.boarding_house in self.options.mods:
            items.update(self.get_boarding_house_item_rules())
        return items

    def modify_vanilla_item_rules_with_mod_additions(self, item_rule: Dict[str, StardewRule]):
        if ModNames.sve in self.options.mods:
            item_rule.update(self.get_modified_item_rules_for_sve(item_rule))
        if ModNames.deepwoods in self.options.mods:
            item_rule.update(self.get_modified_item_rules_for_deep_woods(item_rule))
        return item_rule

    def get_sve_item_rules(self):
        return {SVEGift.aged_blue_moon_wine: self.logic.money.can_spend_at(SVERegion.sophias_house, 28000),
                SVEGift.blue_moon_wine: self.logic.money.can_spend_at(SVERegion.sophias_house, 3000),
                SVESeed.fungus_seed: self.logic.region.can_reach(SVERegion.highlands_cavern) & self.logic.combat.has_good_weapon,
                ModLoot.green_mushroom: self.logic.region.can_reach(SVERegion.highlands_outside) &
                                        self.logic.tool.has_tool(Tool.axe, ToolMaterial.iron) & self.logic.season.has_any_not_winter(),
                SVEFruit.monster_fruit: self.logic.season.has(Season.summer) & self.logic.has(SVESeed.stalk_seed),
                SVEVegetable.monster_mushroom: self.logic.season.has(Season.fall) & self.logic.has(SVESeed.fungus_seed),
                SVEForage.ornate_treasure_chest: self.logic.region.can_reach(SVERegion.highlands_outside) & self.logic.combat.has_galaxy_weapon &
                                                 self.logic.tool.has_tool(Tool.axe, ToolMaterial.iron),
                SVEFruit.slime_berry: self.logic.season.has(Season.spring) & self.logic.has(SVESeed.slime_seed),
                SVESeed.slime_seed: self.logic.region.can_reach(SVERegion.highlands_outside) & self.logic.combat.has_good_weapon,
                SVESeed.stalk_seed: self.logic.region.can_reach(SVERegion.highlands_outside) & self.logic.combat.has_good_weapon,
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
                ModLoot.void_shard: self.logic.region.can_reach(SVERegion.crimson_badlands) & self.logic.combat.has_galaxy_weapon &
                                    self.logic.skill.has_level(Skill.combat, 10) & self.logic.region.can_reach(Region.saloon) & self.logic.time.has_year_three
                }
        # @formatter:on

    def get_modified_item_rules_for_sve(self, items: Dict[str, StardewRule]):
        return {
            Loot.void_essence: items[Loot.void_essence] | self.logic.region.can_reach(SVERegion.highlands_cavern) | self.logic.region.can_reach(
                SVERegion.crimson_badlands),
            Loot.solar_essence: items[Loot.solar_essence] | self.logic.region.can_reach(SVERegion.crimson_badlands),
            Flower.tulip: items[Flower.tulip] | self.logic.tool.can_forage(Season.spring, SVERegion.sprite_spring),
            Flower.blue_jazz: items[Flower.blue_jazz] | self.logic.tool.can_forage(Season.spring, SVERegion.sprite_spring),
            Flower.summer_spangle: items[Flower.summer_spangle] | self.logic.tool.can_forage(Season.summer, SVERegion.sprite_spring),
            Flower.sunflower: items[Flower.sunflower] | self.logic.tool.can_forage((Season.summer, Season.fall), SVERegion.sprite_spring),
            Flower.fairy_rose: items[Flower.fairy_rose] | self.logic.tool.can_forage(Season.fall, SVERegion.sprite_spring),
            Fruit.ancient_fruit: items[Fruit.ancient_fruit] | (
                    self.logic.tool.can_forage((Season.spring, Season.summer, Season.fall), SVERegion.sprite_spring) &
                    self.logic.time.has_year_three) | self.logic.region.can_reach(SVERegion.sprite_spring_cave),
            Fruit.sweet_gem_berry: items[Fruit.sweet_gem_berry] | (
                    self.logic.tool.can_forage((Season.spring, Season.summer, Season.fall), SVERegion.sprite_spring) &
                    self.logic.time.has_year_three),
            WaterItem.coral: items[WaterItem.coral] | self.logic.region.can_reach(SVERegion.fable_reef),
            Forageable.rainbow_shell: items[Forageable.rainbow_shell] | self.logic.region.can_reach(SVERegion.fable_reef),
            WaterItem.sea_urchin: items[WaterItem.sea_urchin] | self.logic.region.can_reach(SVERegion.fable_reef),
            Forageable.red_mushroom: items[Forageable.red_mushroom] | self.logic.tool.can_forage((Season.summer, Season.fall), SVERegion.forest_west) |
                                     self.logic.region.can_reach(SVERegion.sprite_spring_cave),
            Forageable.purple_mushroom: items[Forageable.purple_mushroom] | self.logic.tool.can_forage(Season.fall, SVERegion.forest_west) |
                                        self.logic.region.can_reach(SVERegion.sprite_spring_cave),
            Forageable.morel: items[Forageable.morel] | self.logic.tool.can_forage(Season.fall, SVERegion.forest_west),
            Forageable.chanterelle: items[Forageable.chanterelle] | self.logic.tool.can_forage(Season.fall, SVERegion.forest_west) |
                                    self.logic.region.can_reach(SVERegion.sprite_spring_cave),
            Ore.copper: items[Ore.copper] | (self.logic.tool.can_use_tool_at(Tool.pickaxe, ToolMaterial.basic, SVERegion.highlands_cavern) &
                                             self.logic.combat.can_fight_at_level(Performance.great)),
            Ore.iron: items[Ore.iron] | (self.logic.tool.can_use_tool_at(Tool.pickaxe, ToolMaterial.basic, SVERegion.highlands_cavern) &
                                         self.logic.combat.can_fight_at_level(Performance.great)),
            Ore.iridium: items[Ore.iridium] | (self.logic.tool.can_use_tool_at(Tool.pickaxe, ToolMaterial.basic, SVERegion.crimson_badlands) &
                                               self.logic.combat.can_fight_at_level(Performance.maximum)),
        }

    def get_modified_item_rules_for_deep_woods(self, items: Dict[str, StardewRule]):
        options_to_update = {
            Fruit.apple: items[Fruit.apple] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),  # Deep enough to have seen such a tree at least once
            Fruit.apricot: items[Fruit.apricot] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Fruit.cherry: items[Fruit.cherry] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Fruit.orange: items[Fruit.orange] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Fruit.peach: items[Fruit.peach] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Fruit.pomegranate: items[Fruit.pomegranate] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Fruit.mango: items[Fruit.mango] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Flower.tulip: items[Flower.tulip] | self.logic.tool.can_forage(Season.not_winter, DeepWoodsRegion.floor_10),
            Flower.blue_jazz: items[Flower.blue_jazz] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Flower.summer_spangle: items[Flower.summer_spangle] | self.logic.tool.can_forage(Season.not_winter, DeepWoodsRegion.floor_10),
            Flower.poppy: items[Flower.poppy] | self.logic.tool.can_forage(Season.not_winter, DeepWoodsRegion.floor_10),
            Flower.fairy_rose: items[Flower.fairy_rose] | self.logic.region.can_reach(DeepWoodsRegion.floor_10),
            Material.hardwood: items[Material.hardwood] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.iron, DeepWoodsRegion.floor_10),
            Ingredient.sugar: items[Ingredient.sugar] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.gold, DeepWoodsRegion.floor_50),
            # Gingerbread House
            Ingredient.wheat_flour: items[Ingredient.wheat_flour] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.gold, DeepWoodsRegion.floor_50),
            # Gingerbread House
        }

        if self.options.tool_progression & options.ToolProgression.option_progressive:
            options_to_update.update({
                Ore.iridium: items[Ore.iridium] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.iridium, DeepWoodsRegion.floor_50),  # Iridium Tree
            })

        return options_to_update

    def get_archaeology_item_rules(self):
        archaeology_item_rules = {}
        preservation_chamber_rule = self.logic.has(ModMachine.preservation_chamber)
        hardwood_preservation_chamber_rule = self.logic.has(ModMachine.hardwood_preservation_chamber)
        for item in display_items:
            for display_type in display_types:
                if item == "Trilobite":
                    location_name = f"{display_type}: Trilobite Fossil"
                else:
                    location_name = f"{display_type}: {item}"
                display_item_rule = self.logic.crafting.can_craft(all_crafting_recipes_by_name[display_type]) & self.logic.has(item)
                if "Wooden" in display_type:
                    archaeology_item_rules[location_name] = display_item_rule & preservation_chamber_rule
                else:
                    archaeology_item_rules[location_name] = display_item_rule & hardwood_preservation_chamber_rule
        return archaeology_item_rules

    def get_distant_lands_item_rules(self):
        return {
            DistantLandsForageable.swamp_herb: self.logic.region.can_reach(Region.witch_swamp),
            DistantLandsForageable.brown_amanita: self.logic.region.can_reach(Region.witch_swamp),
            DistantLandsSeed.vile_ancient_fruit: self.logic.quest.can_complete_quest(ModQuest.WitchOrder) | self.logic.quest.can_complete_quest(
                ModQuest.CorruptedCropsTask),
            DistantLandsSeed.void_mint: self.logic.quest.can_complete_quest(ModQuest.WitchOrder) | self.logic.quest.can_complete_quest(
                ModQuest.CorruptedCropsTask),
            DistantLandsCrop.void_mint: self.logic.season.has_any_not_winter() & self.logic.has(DistantLandsSeed.void_mint),
            DistantLandsCrop.vile_ancient_fruit: self.logic.season.has_any_not_winter() & self.logic.has(DistantLandsSeed.vile_ancient_fruit),
        }

    def get_boarding_house_item_rules(self):
        return {
            # Mob Drops from lost valley enemies
            ModArtisanGood.pterodactyl_egg: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                             BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_claw: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                         BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_ribs: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                         BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_vertebra: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                             BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_skull: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                          BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_phalange: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                             BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_l_wing_bone: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                                BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.pterodactyl_r_wing_bone: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                                BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_skull: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                       BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_tooth: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                       BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_femur: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                       BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_pelvis: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                        BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_ribs: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                      BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_vertebra: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                          BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.dinosaur_claw: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                      BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.good),
            ModFossil.neanderthal_skull: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                          BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.great),
            ModFossil.neanderthal_ribs: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                         BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.great),
            ModFossil.neanderthal_pelvis: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                           BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.great),
            ModFossil.neanderthal_limb_bones: self.logic.region.can_reach_any((BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                               BoardingHouseRegion.lost_valley_house_2,)) & self.logic.combat.can_fight_at_level(
                Performance.great),
        }

    def has_seed_unlocked(self, seed_name: str):
        if self.options.cropsanity == Cropsanity.option_disabled:
            return True_()
        return self.logic.received(seed_name)
