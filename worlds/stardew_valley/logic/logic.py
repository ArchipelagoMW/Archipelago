from __future__ import annotations

import logging
from typing import Collection, Callable

from .ability_logic import AbilityLogicMixin
from .action_logic import ActionLogicMixin
from .animal_logic import AnimalLogicMixin
from .arcade_logic import ArcadeLogicMixin
from .artisan_logic import ArtisanLogicMixin
from .base_logic import LogicRegistry
from .book_logic import BookLogicMixin
from .building_logic import BuildingLogicMixin
from .bundle_logic import BundleLogicMixin
from .combat_logic import CombatLogicMixin
from .cooking_logic import CookingLogicMixin
from .crafting_logic import CraftingLogicMixin
from .farming_logic import FarmingLogicMixin
from .festival_logic import FestivalLogicMixin
from .fishing_logic import FishingLogicMixin
from .gift_logic import GiftLogicMixin
from .grind_logic import GrindLogicMixin
from .harvesting_logic import HarvestingLogicMixin
from .has_logic import HasLogicMixin
from .logic_event import all_logic_events
from .mine_logic import MineLogicMixin
from .money_logic import MoneyLogicMixin
from .monster_logic import MonsterLogicMixin
from .museum_logic import MuseumLogicMixin
from .pet_logic import PetLogicMixin
from .quality_logic import QualityLogicMixin
from .quest_logic import QuestLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogicMixin
from .requirement_logic import RequirementLogicMixin
from .season_logic import SeasonLogicMixin
from .shipping_logic import ShippingLogicMixin
from .skill_logic import SkillLogicMixin
from .source_logic import SourceLogicMixin
from .special_order_logic import SpecialOrderLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from .traveling_merchant_logic import TravelingMerchantLogicMixin
from .wallet_logic import WalletLogicMixin
from .walnut_logic import WalnutLogicMixin
from ..content.game_content import StardewContent
from ..data.craftable_data import all_crafting_recipes
from ..data.museum_data import all_museum_items
from ..data.recipe_data import all_cooking_recipes
from ..mods.logic.magic_logic import MagicLogicMixin
from ..mods.logic.mod_logic import ModLogicMixin
from ..mods.mod_data import ModNames
from ..options import ExcludeGingerIsland, FestivalLocations, StardewValleyOptions
from ..stardew_rule import False_, True_, StardewRule
from ..strings.animal_names import Animal
from ..strings.animal_product_names import AnimalProduct
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.craftable_names import Consumable, Ring, Fishing, Lighting, WildSeeds
from ..strings.crop_names import Fruit, Vegetable
from ..strings.currency_names import Currency
from ..strings.decoration_names import Decoration
from ..strings.fertilizer_names import Fertilizer, SpeedGro, RetainingSoil
from ..strings.fish_names import Fish, Trash, WaterItem, WaterChest
from ..strings.flower_names import Flower
from ..strings.food_names import Meal, Beverage
from ..strings.forageable_names import Forageable
from ..strings.fruit_tree_names import Sapling
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.gift_names import Gift
from ..strings.ingredient_names import Ingredient
from ..strings.machine_names import Machine
from ..strings.material_names import Material
from ..strings.metal_names import Ore, MetalBar, Mineral, Fossil, Artifact
from ..strings.monster_drop_names import Loot
from ..strings.monster_names import Monster
from ..strings.region_names import Region, LogicRegion
from ..strings.season_names import Season
from ..strings.seed_names import Seed, TreeSeed
from ..strings.skill_names import Skill
from ..strings.tool_names import Tool, ToolMaterial
from ..strings.villager_names import NPC
from ..strings.wallet_item_names import Wallet

logger = logging.getLogger(__name__)


class StardewLogic(ReceivedLogicMixin, HasLogicMixin, RegionLogicMixin, TravelingMerchantLogicMixin, TimeLogicMixin,
                   SeasonLogicMixin, MoneyLogicMixin, ActionLogicMixin, ArcadeLogicMixin, ArtisanLogicMixin, GiftLogicMixin,
                   BuildingLogicMixin, ShippingLogicMixin, RelationshipLogicMixin, MuseumLogicMixin, WalletLogicMixin, AnimalLogicMixin,
                   CombatLogicMixin, MagicLogicMixin, MonsterLogicMixin, ToolLogicMixin, PetLogicMixin, QualityLogicMixin,
                   SkillLogicMixin, FarmingLogicMixin, BundleLogicMixin, FishingLogicMixin, MineLogicMixin, CookingLogicMixin, AbilityLogicMixin,
                   SpecialOrderLogicMixin, QuestLogicMixin, CraftingLogicMixin, ModLogicMixin, HarvestingLogicMixin, SourceLogicMixin,
                   RequirementLogicMixin, BookLogicMixin, GrindLogicMixin, FestivalLogicMixin, WalnutLogicMixin):
    player: int
    options: StardewValleyOptions
    content: StardewContent
    regions: Collection[str]

    def __init__(self, player: int, options: StardewValleyOptions, content: StardewContent, regions: Collection[str]):
        self.registry = LogicRegistry()
        super().__init__(player, self.registry, options, content, regions, self)

        self.registry.fish_rules.update({fish.name: self.fishing.can_catch_fish(fish) for fish in content.fishes.values()})
        self.registry.museum_rules.update({donation.item_name: self.museum.can_find_museum_item(donation) for donation in all_museum_items})

        for recipe in all_cooking_recipes:
            if recipe.mod_name and recipe.mod_name not in self.options.mods:
                continue
            can_cook_rule = self.cooking.can_cook(recipe)
            if recipe.meal in self.registry.cooking_rules:
                can_cook_rule = can_cook_rule | self.registry.cooking_rules[recipe.meal]
            self.registry.cooking_rules[recipe.meal] = can_cook_rule

        for recipe in all_crafting_recipes:
            if recipe.mod_name and recipe.mod_name not in self.options.mods:
                continue
            can_craft_rule = self.crafting.can_craft(recipe)
            if recipe.item in self.registry.crafting_rules:
                can_craft_rule = can_craft_rule | self.registry.crafting_rules[recipe.item]
            self.registry.crafting_rules[recipe.item] = can_craft_rule

        self.registry.crop_rules.update({
            Fruit.ancient_fruit: (self.received("Ancient Seeds") | self.received("Ancient Seeds Recipe")) &
                                 self.region.can_reach(Region.greenhouse) & self.has(Machine.seed_maker),
        })

        # @formatter:off
        self.registry.item_rules.update({
            "Energy Tonic": self.money.can_spend_at(Region.hospital, 1000),
            WaterChest.fishing_chest: self.fishing.can_fish_chests(),
            WaterChest.golden_fishing_chest: self.fishing.can_fish_chests() & self.skill.has_mastery(Skill.fishing),
            WaterChest.treasure: self.fishing.can_fish_chests(),
            Ring.hot_java_ring: self.region.can_reach(Region.volcano_floor_10),
            "Galaxy Soul": self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 40),
            "JotPK Big Buff": self.arcade.has_jotpk_power_level(7),
            "JotPK Max Buff": self.arcade.has_jotpk_power_level(9),
            "JotPK Medium Buff": self.arcade.has_jotpk_power_level(4),
            "JotPK Small Buff": self.arcade.has_jotpk_power_level(2),
            "Junimo Kart Big Buff": self.arcade.has_junimo_kart_power_level(6),
            "Junimo Kart Max Buff": self.arcade.has_junimo_kart_power_level(8),
            "Junimo Kart Medium Buff": self.arcade.has_junimo_kart_power_level(4),
            "Junimo Kart Small Buff": self.arcade.has_junimo_kart_power_level(2),
            "Magic Rock Candy": self.region.can_reach(Region.desert) & self.has("Prismatic Shard"),
            "Muscle Remedy": self.money.can_spend_at(Region.hospital, 1000),
            # self.has(Ingredient.vinegar)),
            # self.received("Deluxe Fertilizer Recipe") & self.has(MetalBar.iridium) & self.has(SVItem.sap),
            # | (self.ability.can_cook() & self.relationship.has_hearts(NPC.emily, 3) & self.has(Forageable.leek) & self.has(Forageable.dandelion) &
            # | (self.ability.can_cook() & self.relationship.has_hearts(NPC.jodi, 7) & self.has(AnimalProduct.cow_milk) & self.has(Ingredient.sugar)),
            Animal.chicken: self.animal.can_buy_animal(Animal.chicken),
            Animal.cow: self.animal.can_buy_animal(Animal.cow),
            Animal.dinosaur: self.building.has_building(Building.big_coop) & self.has(AnimalProduct.dinosaur_egg),
            Animal.duck: self.animal.can_buy_animal(Animal.duck),
            Animal.goat: self.animal.can_buy_animal(Animal.goat),
            Animal.ostrich: self.building.has_building(Building.barn) & self.has(AnimalProduct.ostrich_egg) & self.has(Machine.ostrich_incubator),
            Animal.pig: self.animal.can_buy_animal(Animal.pig),
            Animal.rabbit: self.animal.can_buy_animal(Animal.rabbit),
            Animal.sheep: self.animal.can_buy_animal(Animal.sheep),
            AnimalProduct.any_egg: self.has_any(AnimalProduct.chicken_egg, AnimalProduct.duck_egg),
            AnimalProduct.brown_egg: self.animal.has_animal(Animal.chicken),
            AnimalProduct.chicken_egg: self.has_any(AnimalProduct.egg, AnimalProduct.brown_egg, AnimalProduct.large_egg, AnimalProduct.large_brown_egg),
            AnimalProduct.cow_milk: self.has_any(AnimalProduct.milk, AnimalProduct.large_milk),
            AnimalProduct.duck_egg: self.animal.has_animal(Animal.duck),
            AnimalProduct.duck_feather: self.animal.has_happy_animal(Animal.duck),
            AnimalProduct.egg: self.animal.has_animal(Animal.chicken),
            AnimalProduct.goat_milk: self.has(Animal.goat),
            AnimalProduct.golden_egg: self.received(AnimalProduct.golden_egg) & (self.money.can_spend_at(Region.ranch, 100000) | self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 100)),
            AnimalProduct.large_brown_egg: self.animal.has_happy_animal(Animal.chicken),
            AnimalProduct.large_egg: self.animal.has_happy_animal(Animal.chicken),
            AnimalProduct.large_goat_milk: self.animal.has_happy_animal(Animal.goat),
            AnimalProduct.large_milk: self.animal.has_happy_animal(Animal.cow),
            AnimalProduct.milk: self.animal.has_animal(Animal.cow),
            AnimalProduct.ostrich_egg: self.tool.can_forage(Generic.any, Region.island_north, True) & self.has(Forageable.journal_scrap) & self.region.can_reach(Region.volcano_floor_5),
            AnimalProduct.rabbit_foot: self.animal.has_happy_animal(Animal.rabbit),
            AnimalProduct.roe: self.skill.can_fish() & self.building.has_building(Building.fish_pond),
            AnimalProduct.squid_ink: self.mine.can_mine_in_the_mines_floor_81_120() | (self.building.has_building(Building.fish_pond) & self.has(Fish.squid)),
            AnimalProduct.sturgeon_roe: self.has(Fish.sturgeon) & self.building.has_building(Building.fish_pond),
            AnimalProduct.truffle: self.animal.has_animal(Animal.pig) & self.season.has_any_not_winter(),
            AnimalProduct.void_egg: self.money.can_spend_at(Region.sewer, 5000) | (self.building.has_building(Building.fish_pond) & self.has(Fish.void_salmon)),
            AnimalProduct.wool: self.animal.has_animal(Animal.rabbit) | self.animal.has_animal(Animal.sheep),
            AnimalProduct.slime_egg_green: self.has(Machine.slime_egg_press) & self.has(Loot.slime),
            AnimalProduct.slime_egg_blue: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(3),
            AnimalProduct.slime_egg_red: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(6),
            AnimalProduct.slime_egg_purple: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(9),
            AnimalProduct.slime_egg_tiger: self.has(Fish.lionfish) & self.building.has_building(Building.fish_pond),
            ArtisanGood.aged_roe: self.artisan.can_preserves_jar(AnimalProduct.roe),
            ArtisanGood.battery_pack: (self.has(Machine.lightning_rod) & self.season.has_any_not_winter()) | self.has(Machine.solar_panel),
            ArtisanGood.caviar: self.artisan.can_preserves_jar(AnimalProduct.sturgeon_roe),
            ArtisanGood.cheese: (self.has(AnimalProduct.cow_milk) & self.has(Machine.cheese_press)) | (self.region.can_reach(Region.desert) & self.has(Mineral.emerald)),
            ArtisanGood.cloth: (self.has(AnimalProduct.wool) & self.has(Machine.loom)) | (self.region.can_reach(Region.desert) & self.has(Mineral.aquamarine)),
            ArtisanGood.dinosaur_mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.dinosaur_egg),
            ArtisanGood.duck_mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.duck_egg),
            ArtisanGood.goat_cheese: self.has(AnimalProduct.goat_milk) & self.has(Machine.cheese_press),
            ArtisanGood.honey: self.money.can_spend_at(Region.oasis, 200) | (self.has(Machine.bee_house) & self.season.has_any_not_winter()),
            ArtisanGood.maple_syrup: self.has(Machine.tapper),
            ArtisanGood.mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.chicken_egg),
            ArtisanGood.mystic_syrup: self.has(Machine.tapper) & self.has(TreeSeed.mystic),
            ArtisanGood.oak_resin: self.has(Machine.tapper),
            ArtisanGood.pine_tar: self.has(Machine.tapper),
            ArtisanGood.smoked_fish: self.artisan.has_smoked_fish(),
            ArtisanGood.targeted_bait: self.artisan.has_targeted_bait(),
            ArtisanGood.stardrop_tea: self.has(WaterChest.golden_fishing_chest),
            ArtisanGood.truffle_oil: self.has(AnimalProduct.truffle) & self.has(Machine.oil_maker),
            ArtisanGood.void_mayonnaise: (self.skill.can_fish(Region.witch_swamp)) | (self.artisan.can_mayonnaise(AnimalProduct.void_egg)),
            Beverage.pina_colada: self.money.can_spend_at(Region.island_resort, 600),
            Beverage.triple_shot_espresso: self.has("Hot Java Ring"),
            Consumable.butterfly_powder: self.money.can_spend_at(Region.sewer, 20000),
            Consumable.far_away_stone: self.region.can_reach(Region.mines_floor_100) & self.has(Artifact.ancient_doll),
            Consumable.fireworks_red: self.region.can_reach(Region.casino),
            Consumable.fireworks_purple: self.region.can_reach(Region.casino),
            Consumable.fireworks_green: self.region.can_reach(Region.casino),
            Consumable.golden_animal_cracker: self.skill.has_mastery(Skill.farming),
            Consumable.mystery_box: self.received(CommunityUpgrade.mr_qi_plane_ride),
            Consumable.gold_mystery_box: self.received(CommunityUpgrade.mr_qi_plane_ride) & self.skill.has_mastery(Skill.foraging),
            Currency.calico_egg: self.region.can_reach(LogicRegion.desert_festival),
            Currency.golden_tag: self.region.can_reach(LogicRegion.trout_derby),
            Currency.prize_ticket: self.time.has_lived_months(2),  # Time to do a few help wanted quests
            Decoration.rotten_plant: self.has(Lighting.jack_o_lantern) & self.season.has(Season.winter),
            Fertilizer.basic: self.money.can_spend_at(Region.pierre_store, 100),
            Fertilizer.quality: self.time.has_year_two & self.money.can_spend_at(Region.pierre_store, 150),
            Fertilizer.tree: self.skill.has_level(Skill.foraging, 7) & self.has(Material.fiber) & self.has(Material.stone),
            Fish.any: self.logic.or_(*(self.fishing.can_catch_fish(fish) for fish in content.fishes.values())),
            Fish.crab: self.skill.can_crab_pot_at(Region.beach),
            Fish.crayfish: self.skill.can_crab_pot_at(Region.town),
            Fish.lobster: self.skill.can_crab_pot_at(Region.beach),
            Fish.mussel: self.tool.can_forage(Generic.any, Region.beach) or self.has(Fish.mussel_node),
            Fish.mussel_node: self.region.can_reach(Region.island_west),
            Fish.oyster: self.tool.can_forage(Generic.any, Region.beach),
            Fish.periwinkle: self.skill.can_crab_pot_at(Region.town),
            Fish.shrimp: self.skill.can_crab_pot_at(Region.beach),
            Fish.snail: self.skill.can_crab_pot_at(Region.town),
            Fishing.curiosity_lure: self.monster.can_kill(self.monster.all_monsters_by_name[Monster.mummy]),
            Fishing.lead_bobber: self.skill.has_level(Skill.fishing, 6) & self.money.can_spend_at(Region.fish_shop, 200),
            Forageable.hay: self.building.has_building(Building.silo) & self.tool.has_tool(Tool.scythe), #
            Forageable.journal_scrap: self.region.can_reach_all((Region.island_west, Region.island_north, Region.island_south, Region.volcano_floor_10)) & (self.ability.can_chop_trees() | self.mine.can_mine_in_the_mines_floor_1_40()),#
            Forageable.secret_note: self.quest.has_magnifying_glass() & (self.ability.can_chop_trees() | self.mine.can_mine_in_the_mines_floor_1_40()), #
            Fossil.bone_fragment: (self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.pickaxe)) | self.monster.can_kill(Monster.skeleton),
            Fossil.fossilized_leg: self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.pickaxe),
            Fossil.fossilized_ribs: self.region.can_reach(Region.island_south) & self.tool.has_tool(Tool.hoe),
            Fossil.fossilized_skull: self.action.can_open_geode(Geode.golden_coconut),
            Fossil.fossilized_spine: self.skill.can_fish(Region.dig_site),
            Fossil.fossilized_tail: self.action.can_pan_at(Region.dig_site, ToolMaterial.copper),
            Fossil.mummified_bat: self.region.can_reach(Region.volcano_floor_10),
            Fossil.mummified_frog: self.region.can_reach(Region.island_east) & self.tool.has_tool(Tool.scythe),
            Fossil.snake_skull: self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.hoe),
            Fossil.snake_vertebrae: self.region.can_reach(Region.island_west) & self.tool.has_tool(Tool.hoe),
            Geode.artifact_trove: self.has(Geode.omni) & self.region.can_reach(Region.desert),
            Geode.frozen: self.mine.can_mine_in_the_mines_floor_41_80(),
            Geode.geode: self.mine.can_mine_in_the_mines_floor_1_40(),
            Geode.golden_coconut: self.region.can_reach(Region.island_north),
            Geode.magma: self.mine.can_mine_in_the_mines_floor_81_120() | (self.has(Fish.lava_eel) & self.building.has_building(Building.fish_pond)),
            Geode.omni: self.mine.can_mine_in_the_mines_floor_41_80() | self.region.can_reach(Region.desert) | self.tool.has_tool(Tool.pan, ToolMaterial.iron) | self.received(Wallet.rusty_key) | (self.has(Fish.octopus) & self.building.has_building(Building.fish_pond)) | self.region.can_reach(Region.volcano_floor_10),
            Gift.bouquet: self.relationship.has_hearts_with_any_bachelor(8) & self.money.can_spend_at(Region.pierre_store, 100),
            Gift.golden_pumpkin: self.season.has(Season.fall) | self.action.can_open_geode(Geode.artifact_trove),
            Gift.mermaid_pendant: self.region.can_reach(Region.tide_pools) & self.relationship.has_hearts_with_any_bachelor(10) & self.building.has_house(1) & self.has(Consumable.rain_totem),
            Gift.movie_ticket: self.money.can_spend_at(Region.movie_ticket_stand, 1000),
            Gift.pearl: (self.has(Fish.blobfish) & self.building.has_building(Building.fish_pond)) | self.action.can_open_geode(Geode.artifact_trove),
            Gift.tea_set: self.season.has(Season.winter) & self.time.has_lived_max_months,
            Gift.void_ghost_pendant: self.money.can_trade_at(Region.desert, Loot.void_essence, 200) & self.relationship.has_hearts(NPC.krobus, 10),
            Gift.wilted_bouquet: self.has(Machine.furnace) & self.has(Gift.bouquet) & self.has(Material.coal),
            Ingredient.oil: self.money.can_spend_at(Region.pierre_store, 200) | (self.has(Machine.oil_maker) & (self.has(Vegetable.corn) | self.has(Flower.sunflower) | self.has(Seed.sunflower))),
            Ingredient.qi_seasoning: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 10),
            Ingredient.rice: self.money.can_spend_at(Region.pierre_store, 200) | (self.building.has_building(Building.mill) & self.has(Vegetable.unmilled_rice)),
            Ingredient.sugar: self.money.can_spend_at(Region.pierre_store, 100) | (self.building.has_building(Building.mill) & self.has(Vegetable.beet)),
            Ingredient.vinegar: self.money.can_spend_at(Region.pierre_store, 200) | self.artisan.can_keg(Ingredient.rice),
            Ingredient.wheat_flour: self.money.can_spend_at(Region.pierre_store, 100) | (self.building.has_building(Building.mill) & self.has(Vegetable.wheat)),
            Loot.bat_wing: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern(),
            Loot.bug_meat: self.mine.can_mine_in_the_mines_floor_1_40(),
            Loot.slime: self.mine.can_mine_in_the_mines_floor_1_40(),
            Loot.solar_essence: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern(),
            Loot.void_essence: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern(),
            Machine.coffee_maker: self.received(Machine.coffee_maker),
            Machine.crab_pot: self.skill.has_level(Skill.fishing, 3) & self.money.can_spend_at(Region.fish_shop, 1500),
            Machine.enricher: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 20),
            Machine.pressure_nozzle: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 20),
            Material.cinder_shard: self.region.can_reach(Region.volcano_floor_5),
            Material.clay: self.region.can_reach_any((Region.farm, Region.beach, Region.quarry)) & self.tool.has_tool(Tool.hoe),
            Material.coal: self.mine.can_mine_in_the_mines_floor_41_80() | self.tool.has_tool(Tool.pan),
            Material.fiber: True_(),
            Material.hardwood: self.tool.has_tool(Tool.axe, ToolMaterial.copper) & (self.region.can_reach(Region.secret_woods) | self.region.can_reach(Region.island_west)),
            Material.moss: self.season.has_any_not_winter() & (self.tool.has_tool(Tool.scythe) | self.combat.has_any_weapon) & self.region.can_reach(Region.forest),
            Material.sap: self.ability.can_chop_trees(),
            Material.stone: self.tool.has_tool(Tool.pickaxe),
            Material.wood: self.tool.has_tool(Tool.axe),
            Meal.ice_cream: (self.season.has(Season.summer) & self.money.can_spend_at(Region.town, 250)) | self.money.can_spend_at(Region.oasis, 240),
            Meal.strange_bun: self.relationship.has_hearts(NPC.shane, 7) & self.has(Ingredient.wheat_flour) & self.has(Fish.periwinkle) & self.has(ArtisanGood.void_mayonnaise),
            MetalBar.copper: self.can_smelt(Ore.copper),
            MetalBar.gold: self.can_smelt(Ore.gold),
            MetalBar.iridium: self.can_smelt(Ore.iridium),
            MetalBar.iron: self.can_smelt(Ore.iron),
            MetalBar.quartz: self.can_smelt(Mineral.quartz) | self.can_smelt("Fire Quartz") | (self.has(Machine.recycling_machine) & (self.has(Trash.broken_cd) | self.has(Trash.broken_glasses))),
            MetalBar.radioactive: self.can_smelt(Ore.radioactive),
            Ore.copper: self.mine.can_mine_in_the_mines_floor_1_40() | self.mine.can_mine_in_the_skull_cavern() | self.tool.has_tool(Tool.pan, ToolMaterial.copper),
            Ore.gold: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern() | self.tool.has_tool(Tool.pan, ToolMaterial.iron),
            Ore.iridium: self.mine.can_mine_in_the_skull_cavern() | self.can_fish_pond(Fish.super_cucumber) | self.tool.has_tool(Tool.pan, ToolMaterial.gold),
            Ore.iron: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern() | self.tool.has_tool(Tool.pan, ToolMaterial.copper),
            Ore.radioactive: self.ability.can_mine_perfectly() & self.region.can_reach(Region.qi_walnut_room),
            RetainingSoil.basic: self.money.can_spend_at(Region.pierre_store, 100),
            RetainingSoil.quality: self.time.has_year_two & self.money.can_spend_at(Region.pierre_store, 150),
            Sapling.tea: self.relationship.has_hearts(NPC.caroline, 2) & self.has(Material.fiber) & self.has(Material.wood),
            SpeedGro.basic: self.money.can_spend_at(Region.pierre_store, 100),
            SpeedGro.deluxe: self.time.has_year_two & self.money.can_spend_at(Region.pierre_store, 150),
            Trash.broken_cd: self.skill.can_crab_pot,
            Trash.broken_glasses: self.skill.can_crab_pot,
            Trash.driftwood: self.skill.can_crab_pot,
            Trash.joja_cola: self.money.can_spend_at(Region.saloon, 75),
            Trash.soggy_newspaper: self.skill.can_crab_pot,
            Trash.trash: self.skill.can_crab_pot,
            TreeSeed.acorn: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mahogany: self.region.can_reach(Region.secret_woods) & self.tool.has_tool(Tool.axe, ToolMaterial.iron) & self.skill.has_level(Skill.foraging, 1),
            TreeSeed.maple: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mushroom: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 5),
            TreeSeed.pine: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mossy: self.ability.can_chop_trees() & self.season.has(Season.summer),
            Fish.clam: self.tool.can_forage(Generic.any, Region.beach),
            Fish.cockle: self.tool.can_forage(Generic.any, Region.beach),
            WaterItem.green_algae: self.fishing.can_fish_in_freshwater(),
            WaterItem.cave_jelly: self.fishing.can_fish_at(Region.mines_floor_100) & self.tool.has_fishing_rod(2),
            WaterItem.river_jelly: self.fishing.can_fish_at(Region.town) & self.tool.has_fishing_rod(2),
            WaterItem.sea_jelly: self.fishing.can_fish_at(Region.beach) & self.tool.has_fishing_rod(2),
            WaterItem.seaweed: self.skill.can_fish(Region.tide_pools),
            WaterItem.white_algae: self.skill.can_fish(Region.mines_floor_20),
            WildSeeds.grass_starter: self.money.can_spend_at(Region.pierre_store, 100),
        })
        # @formatter:on

        content_rules = {
            item_name: self.source.has_access_to_item(game_item)
            for item_name, game_item in self.content.game_items.items()
        }

        for item in set(content_rules.keys()).intersection(self.registry.item_rules.keys()):
            logger.warning(f"Rule for {item} already exists in the registry, overwriting it.")

        self.registry.item_rules.update(content_rules)
        self.registry.item_rules.update(self.registry.fish_rules)
        self.registry.item_rules.update(self.registry.museum_rules)
        self.registry.item_rules.update(self.registry.crop_rules)
        self.artisan.initialize_rules()
        self.registry.item_rules.update(self.registry.artisan_good_rules)

        self.registry.item_rules.update(self.mod.item.get_modded_item_rules())
        self.mod.item.modify_vanilla_item_rules_with_mod_additions(self.registry.item_rules)  # New regions and content means new ways to obtain old items

        # For some recipes, the cooked item can be obtained directly, so we either cook it or get it
        for recipe in self.registry.cooking_rules:
            cooking_rule = self.registry.cooking_rules[recipe]
            obtention_rule = self.registry.item_rules[recipe] if recipe in self.registry.item_rules else False_()
            self.registry.item_rules[recipe] = obtention_rule | cooking_rule

        # For some recipes, the crafted item can be obtained directly, so we either craft it or get it
        for recipe in self.registry.crafting_rules:
            crafting_rule = self.registry.crafting_rules[recipe]
            obtention_rule = self.registry.item_rules[recipe] if recipe in self.registry.item_rules else False_()
            self.registry.item_rules[recipe] = obtention_rule | crafting_rule

        self.building.initialize_rules()
        self.building.update_rules(self.mod.building.get_modded_building_rules())

        self.quest.initialize_rules()
        self.quest.update_rules(self.mod.quest.get_modded_quest_rules())

        self.festival.initialize_rules()

        self.special_order.initialize_rules()
        self.special_order.update_rules(self.mod.special_order.get_modded_special_orders_rules())

    def setup_events(self, register_event: Callable[[str, str, StardewRule], None]) -> None:
        for logic_event in all_logic_events:
            rule = self.registry.item_rules[logic_event.item]
            register_event(logic_event.name, logic_event.region, rule)
            self.registry.item_rules[logic_event.item] = self.received(logic_event.name)

    def can_smelt(self, item: str) -> StardewRule:
        return self.has(Machine.furnace) & self.has(item)

    def can_finish_grandpa_evaluation(self) -> StardewRule:
        # https://stardewvalleywiki.com/Grandpa
        rules_worth_a_point = [
            self.money.can_have_earned_total(50000),  # 50 000g
            self.money.can_have_earned_total(100000),  # 100 000g
            self.money.can_have_earned_total(200000),  # 200 000g
            self.money.can_have_earned_total(300000),  # 300 000g
            self.money.can_have_earned_total(500000),  # 500 000g
            self.money.can_have_earned_total(1000000),  # 1 000 000g first point
            self.money.can_have_earned_total(1000000),  # 1 000 000g second point
            self.skill.has_total_level(30),  # Total Skills: 30
            self.skill.has_total_level(50),  # Total Skills: 50
            self.museum.can_complete_museum(),  # Completing the museum for a point
            # Catching every fish not expected
            # Shipping every item not expected
            self.relationship.can_get_married() & self.building.has_house(2),
            self.relationship.has_hearts_with_n(5, 8),  # 5 Friends
            self.relationship.has_hearts_with_n(10, 8),  # 10 friends
            self.pet.has_pet_hearts(5),  # Max Pet
            self.bundle.can_complete_community_center,  # Community Center Completion
            self.bundle.can_complete_community_center,  # CC Ceremony first point
            self.bundle.can_complete_community_center,  # CC Ceremony second point
            self.received(Wallet.skull_key),  # Skull Key obtained
            self.wallet.has_rusty_key(),  # Rusty key obtained
        ]
        return self.count(12, *rules_worth_a_point)

    def has_island_trader(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        return self.region.can_reach(Region.island_trader)

    def has_all_stardrops(self) -> StardewRule:
        other_rules = []
        number_of_stardrops_to_receive = 0
        number_of_stardrops_to_receive += 1  # The Mines level 100
        number_of_stardrops_to_receive += 1  # Old Master Cannoli
        number_of_stardrops_to_receive += 1  # Museum Stardrop
        number_of_stardrops_to_receive += 1  # Krobus Stardrop

        # Master Angler Stardrop
        if self.content.features.fishsanity.is_enabled:
            number_of_stardrops_to_receive += 1
        else:
            other_rules.append(self.fishing.can_catch_every_fish())

        if self.options.festival_locations == FestivalLocations.option_disabled:  # Fair Stardrop
            other_rules.append(self.season.has(Season.fall))
        else:
            number_of_stardrops_to_receive += 1

        # Spouse Stardrop
        if self.content.features.friendsanity.is_enabled:
            number_of_stardrops_to_receive += 1
        else:
            other_rules.append(self.relationship.has_hearts_with_any_bachelor(13))

        if ModNames.deepwoods in self.options.mods:  # Petting the Unicorn
            number_of_stardrops_to_receive += 1

        if not other_rules:
            return self.received("Stardrop", number_of_stardrops_to_receive)

        return self.received("Stardrop", number_of_stardrops_to_receive) & self.logic.and_(*other_rules)

    def has_abandoned_jojamart(self) -> StardewRule:
        return self.received(CommunityUpgrade.movie_theater, 1)

    def has_movie_theater(self) -> StardewRule:
        return self.received(CommunityUpgrade.movie_theater, 2)

    def can_use_obelisk(self, obelisk: str) -> StardewRule:
        return self.region.can_reach(Region.farm) & self.received(obelisk)

    def can_fish_pond(self, fish: str) -> StardewRule:
        return self.building.has_building(Building.fish_pond) & self.has(fish)
