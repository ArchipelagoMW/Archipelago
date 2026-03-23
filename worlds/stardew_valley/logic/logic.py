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
from .fish_pond_logic import FishPondLogicMixin
from .fishing_logic import FishingLogicMixin
from .gift_logic import GiftLogicMixin
from .goal_logic import GoalLogicMixin
from .grind_logic import GrindLogicMixin
from .harvesting_logic import HarvestingLogicMixin
from .has_logic import HasLogicMixin
from .hats_logic import HatLogicMixin
from .logic_event import all_item_events
from .meme_items_logic import MemeItemsLogicMixin
from .mine_logic import MineLogicMixin
from .money_logic import MoneyLogicMixin
from .monster_logic import MonsterLogicMixin
from .movie_logic import MovieLogicMixin
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
from .shirts_logic import ShirtLogicMixin
from .skill_logic import SkillLogicMixin
from .source_logic import SourceLogicMixin
from .special_items_logic import SpecialItemsLogicMixin
from .special_order_logic import SpecialOrderLogicMixin
from .tailoring_logic import TailoringLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from .traveling_merchant_logic import TravelingMerchantLogicMixin
from .wallet_logic import WalletLogicMixin
from .walnut_logic import WalnutLogicMixin
from ..content.game_content import StardewContent
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..data.craftable_data import all_crafting_recipes
from ..data.museum_data import all_museum_items
from ..data.recipe_data import all_cooking_recipes
from ..mods.logic.magic_logic import MagicLogicMixin
from ..mods.logic.mod_logic import ModLogicMixin
from ..options import StardewValleyOptions, BundleRandomization, IncludeEndgameLocations
from ..stardew_rule import False_, StardewRule, Or, Reach
from ..strings.animal_names import Animal
from ..strings.animal_product_names import AnimalProduct
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.artisan_good_names import ArtisanGood
from ..strings.boot_names import tier_by_boots
from ..strings.building_names import Building
from ..strings.catalogue_names import items_by_catalogue
from ..strings.craftable_names import Consumable, Ring, Fishing, Lighting, WildSeeds, Furniture
from ..strings.crop_names import Fruit, Vegetable
from ..strings.currency_names import Currency
from ..strings.decoration_names import Decoration
from ..strings.fertilizer_names import Fertilizer, SpeedGro, RetainingSoil
from ..strings.fish_names import Fish, Trash, WaterItem, WaterChest
from ..strings.flower_names import Flower
from ..strings.food_names import Meal, Beverage
from ..strings.forageable_names import Forageable
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.gift_names import Gift
from ..strings.ingredient_names import Ingredient
from ..strings.machine_names import Machine
from ..strings.material_names import Material
from ..strings.metal_names import Ore, MetalBar, Mineral, Fossil
from ..strings.monster_drop_names import Loot
from ..strings.monster_names import Monster
from ..strings.region_names import Region, LogicRegion
from ..strings.season_names import Season
from ..strings.seed_names import Seed, TreeSeed
from ..strings.skill_names import Skill
from ..strings.special_item_names import SpecialItem
from ..strings.tool_names import Tool, ToolMaterial, FishingRod
from ..strings.villager_names import NPC

logger = logging.getLogger(__name__)


class StardewLogic(ReceivedLogicMixin, HasLogicMixin, RegionLogicMixin, TravelingMerchantLogicMixin, TimeLogicMixin,
                   SeasonLogicMixin, MoneyLogicMixin, ActionLogicMixin, ArcadeLogicMixin, ArtisanLogicMixin, GiftLogicMixin,
                   BuildingLogicMixin, ShippingLogicMixin, RelationshipLogicMixin, MuseumLogicMixin, WalletLogicMixin, AnimalLogicMixin,
                   CombatLogicMixin, MagicLogicMixin, MonsterLogicMixin, ToolLogicMixin, PetLogicMixin, QualityLogicMixin,
                   SkillLogicMixin, FarmingLogicMixin, BundleLogicMixin, FishingLogicMixin, MineLogicMixin, CookingLogicMixin, AbilityLogicMixin,
                   SpecialOrderLogicMixin, QuestLogicMixin, CraftingLogicMixin, ModLogicMixin, HarvestingLogicMixin, SourceLogicMixin,
                   RequirementLogicMixin, BookLogicMixin, GrindLogicMixin, FestivalLogicMixin, WalnutLogicMixin, GoalLogicMixin, SpecialItemsLogicMixin,
                   MovieLogicMixin, MemeItemsLogicMixin, HatLogicMixin, ShirtLogicMixin, TailoringLogicMixin, FishPondLogicMixin):
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
            if recipe.content_pack and not self.content.is_enabled(recipe.content_pack):
                continue

            can_cook_rule = self.cooking.can_cook(recipe)
            if recipe.meal in self.registry.cooking_rules:
                can_cook_rule = can_cook_rule | self.registry.cooking_rules[recipe.meal]
            self.registry.cooking_rules[recipe.meal] = can_cook_rule

        for recipe in all_crafting_recipes:
            if recipe.content_pack is not None and not self.content.are_all_enabled(recipe.content_pack):
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
            WaterChest.fishing_chest: self.fishing.can_fish_chests,
            WaterChest.golden_fishing_chest: self.fishing.can_fish_chests & self.skill.has_mastery(Skill.fishing),
            WaterChest.treasure: self.fishing.can_fish_chests,
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
            "Stardrop": self.received("Stardrop"),
            "Iridium Snake Milk": self.quest.can_drink_snake_milk(),
            # self.has(Ingredient.vinegar)),
            # self.received("Deluxe Fertilizer Recipe") & self.has(MetalBar.iridium) & self.has(SVItem.sap),
            # | (self.ability.can_cook() & self.relationship.has_hearts(NPC.emily, 3) & self.has(Forageable.leek) & self.has(Forageable.dandelion) &
            # | (self.ability.can_cook() & self.relationship.has_hearts(NPC.jodi, 7) & self.has(AnimalProduct.cow_milk) & self.has(Ingredient.sugar)),
            AnimalProduct.any_egg: self.has_any(AnimalProduct.chicken_egg, AnimalProduct.duck_egg),
            AnimalProduct.any_milk: self.has_any(AnimalProduct.cow_milk, AnimalProduct.goat_milk),
            AnimalProduct.brown_egg: self.animal.has_animal(Animal.chicken),
            AnimalProduct.chicken_egg: self.has_any(AnimalProduct.egg, AnimalProduct.brown_egg, AnimalProduct.large_egg, AnimalProduct.large_brown_egg),
            AnimalProduct.cow_milk: self.has_any(AnimalProduct.milk, AnimalProduct.large_milk),
            AnimalProduct.duck_egg: self.animal.has_animal(Animal.duck), # Should also check starter
            AnimalProduct.duck_feather: self.animal.has_happy_animal(Animal.duck),
            AnimalProduct.egg: self.animal.has_animal(Animal.chicken), # Should also check starter
            AnimalProduct.goat_milk: self.animal.has_animal(Animal.goat),
            AnimalProduct.golden_egg: self.has(AnimalProduct.golden_egg_starter), # Should also check golden chicken if there was an alternative to obtain it without golden egg
            AnimalProduct.large_brown_egg: self.animal.has_happy_animal(Animal.chicken),
            AnimalProduct.large_egg: self.animal.has_happy_animal(Animal.chicken),
            AnimalProduct.large_goat_milk: self.animal.has_happy_animal(Animal.goat),
            AnimalProduct.large_milk: self.animal.has_happy_animal(Animal.cow),
            AnimalProduct.milk: self.animal.has_animal(Animal.cow),
            AnimalProduct.rabbit_foot: self.animal.has_happy_animal(Animal.rabbit),
            AnimalProduct.roe: self.fish_pond.can_get_fish_pond_reward(Fish.any, 1, AnimalProduct.roe),
            AnimalProduct.squid_ink: self.mine.can_mine_in_the_mines_floor_81_120() | self.fish_pond.can_get_fish_pond_reward(Fish.squid, 1, AnimalProduct.squid_ink) | self.fish_pond.can_get_fish_pond_reward(Fish.midnight_squid, 1, AnimalProduct.squid_ink),
            AnimalProduct.truffle: self.animal.has_animal(Animal.pig) & self.season.has_any_not_winter(),
            AnimalProduct.void_egg: self.has(AnimalProduct.void_egg_starter),  # Should also check void chicken if there was an alternative to obtain it without void egg
            AnimalProduct.wool: self.animal.has_animal(Animal.rabbit) | self.animal.has_animal(Animal.sheep),
            AnimalProduct.slime_egg_green: self.has(Machine.slime_egg_press) & self.has(Loot.slime),
            AnimalProduct.slime_egg_blue: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(3),
            AnimalProduct.slime_egg_red: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(6),
            AnimalProduct.slime_egg_purple: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(9),
            AnimalProduct.slime_egg_tiger: self.fish_pond.can_get_fish_pond_reward(Fish.lionfish, 9, AnimalProduct.slime_egg_tiger) & self.time.has_lived_months(12) &
                                            self.building.has_building(Building.slime_hutch) & self.monster.can_kill(Monster.tiger_slime),
            AnimalProduct.duck_egg_starter: self.logic.false_,  # It could be purchased at the Feast of the Winter Star, but it's random every year, so not considering it yet...
            AnimalProduct.dinosaur_egg_starter: self.logic.false_,  # Dinosaur eggs are also part of the museum rules, and I don't want to touch them yet.
            AnimalProduct.egg_starter: self.logic.false_,  # It could be purchased at the Desert Festival, but festival logic is quite a mess, so not considering it yet...
            AnimalProduct.golden_egg_starter: self.received(AnimalProduct.golden_egg) & (self.money.can_spend_at(Region.ranch, 100000) | self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 100)),
            AnimalProduct.void_egg_starter: self.money.can_spend_at(Region.sewer, 5000),
            ArtisanGood.aged_roe: self.artisan.can_preserves_jar(AnimalProduct.roe),
            ArtisanGood.battery_pack: (self.has(Machine.lightning_rod) & self.season.has_any_not_winter()) | self.has(Machine.solar_panel),
            ArtisanGood.cheese: (self.has(AnimalProduct.cow_milk) & self.has(Machine.cheese_press)) | (self.region.can_reach(Region.desert) & self.artisan.can_replicate_gem(Mineral.emerald)),
            ArtisanGood.cloth: (self.has(AnimalProduct.wool) & self.has(Machine.loom)) | (self.region.can_reach(Region.desert) & self.artisan.can_replicate_gem(Mineral.aquamarine)),
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
            ArtisanGood.void_mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.void_egg),
            Beverage.pina_colada: self.money.can_spend_at(Region.island_resort, 600),
            Beverage.triple_shot_espresso: self.has("Hot Java Ring"),
            Consumable.butterfly_powder: self.money.can_spend_at(Region.sewer, 20000),
            Consumable.fireworks_red: self.region.can_reach(Region.casino),
            Consumable.fireworks_purple: self.region.can_reach(Region.casino),
            Consumable.fireworks_green: self.region.can_reach(Region.casino),
            Consumable.golden_animal_cracker: self.skill.has_mastery(Skill.farming) & (self.fishing.can_fish_chests | self.region.can_reach(Region.skull_cavern_25)),
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
            Fish.crab: self.fishing.can_crab_pot_at(Region.beach),
            Fish.crayfish: self.fishing.can_crab_pot_at(Region.town),
            Fish.lobster: self.fishing.can_crab_pot_at(Region.beach),
            Fish.mussel: self.tool.can_forage(Generic.any, Region.beach) or self.has(Fish.mussel_node),
            Fish.mussel_node: self.region.can_reach(Region.island_west),
            Fish.oyster: self.tool.can_forage(Generic.any, Region.beach),
            Fish.periwinkle: self.fishing.can_crab_pot_at(Region.town),
            Fish.shrimp: self.fishing.can_crab_pot_at(Region.beach),
            Fish.snail: self.fishing.can_crab_pot_at(Region.town),
            Fishing.curiosity_lure: self.monster.can_kill(self.monster.all_monsters_by_name[Monster.mummy]),
            Fishing.lead_bobber: self.skill.has_level(Skill.fishing, 6) & self.money.can_spend_at(Region.fish_shop, 200),
            Fishing.golden_bobber: self.region.can_reach(LogicRegion.desert_festival) & self.fishing.can_fish_chests,
            Forageable.hay: self.building.has_building(Building.silo) & self.tool.has_scythe(), #
            Forageable.journal_scrap: self.region.can_reach_all(Region.island_west, Region.island_north, Region.island_south, Region.volcano_floor_10) & (self.ability.can_chop_trees() | self.mine.can_mine_in_the_mines_floor_1_40()),#
            Forageable.secret_note: self.region.can_reach(LogicRegion.secret_notes), #
            Fossil.bone_fragment: (self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.pickaxe)) | self.monster.can_kill(Monster.skeleton),
            Fossil.fossilized_leg: self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.pickaxe),
            Fossil.fossilized_ribs: self.region.can_reach(Region.island_south) & self.tool.has_tool(Tool.hoe) & self.received("Open Professor Snail Cave"),
            Fossil.fossilized_skull: self.action.can_open_geode(Geode.golden_coconut),
            Fossil.fossilized_spine: self.fishing.can_fish_at(Region.dig_site),
            Fossil.fossilized_tail: self.action.can_pan_at(Region.dig_site, ToolMaterial.iridium),
            Fossil.mummified_bat: self.region.can_reach(Region.volcano_floor_10),
            Fossil.mummified_frog: self.region.can_reach(Region.island_east) & self.tool.has_scythe(),
            Fossil.snake_skull: self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.hoe),
            Fossil.snake_vertebrae: self.region.can_reach(Region.island_west) & self.tool.has_tool(Tool.hoe),
            Furniture.exotic_double_bed: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50),
            Geode.artifact_trove: self.has(Geode.omni) & self.region.can_reach(Region.desert),
            Geode.frozen: self.mine.can_mine_in_the_mines_floor_41_80(),
            Geode.geode: self.mine.can_mine_in_the_mines_floor_1_40(),
            Geode.golden_coconut: self.region.can_reach(Region.island_north),
            Geode.magma: self.mine.can_mine_in_the_mines_floor_81_120(),  # Could add self.fish_pond.can_get_fish_pond_reward(Fish.lava_eel, 9, Geode.magma) but it makes a logic loop
            Geode.omni: self.count(2, *(self.mine.can_mine_in_the_mines_floor_81_120(), self.region.can_reach_all((Region.desert, Region.oasis, Region.sewer)), self.tool.has_pan(ToolMaterial.iron), (self.region.can_reach_all((Region.island_west, Region.island_north,)) & self.has(Consumable.treasure_totem)))),  # Could add self.fish_pond.can_get_fish_pond_reward(Fish.octopus, 9, Geode.omni) but it makes a logic loop
            Gift.bouquet: self.relationship.has_hearts_with_any_bachelor(8) & self.money.can_spend_at(Region.pierre_store, 100),
            Gift.golden_pumpkin: self.festival.has_golden_pumpkin(),
            Gift.mermaid_pendant: self.region.can_reach(Region.tide_pools) & self.relationship.has_hearts_with_any_bachelor(10) & self.building.has_building(Building.kitchen) & (self.has(Consumable.rain_totem) | self.season.has_any_not_winter()),
            Gift.movie_ticket: self.money.can_spend_at(Region.movie_ticket_stand, 1000),
            Gift.pearl: self.fish_pond.can_get_fish_pond_reward(Fish.blobfish, 9, Gift.pearl) | self.action.can_open_geode(Geode.artifact_trove),
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
            Machine.sewing_machine: (self.region.can_reach(Region.haley_house) & self.has(ArtisanGood.cloth)) | (self.received(Machine.sewing_machine) & self.region.can_reach(Region.secret_woods)),
            Machine.statue_endless_fortune: self.has_statue_of_endless_fortune(),
            Material.cinder_shard: self.region.can_reach(Region.volcano_floor_5),
            Material.clay: self.region.can_reach_any(Region.farm, Region.beach, Region.quarry) & self.tool.has_tool(Tool.hoe),
            Material.coal: self.mine.can_mine_in_the_mines_floor_41_80() | self.tool.has_pan(),
            Material.fiber: self.ability.can_scythe_vines(),
            Material.hardwood: self.tool.has_tool(Tool.axe, ToolMaterial.copper) & (self.region.can_reach(Region.secret_woods) | self.region.can_reach(Region.island_west)),
            Material.moss: self.season.has_any_not_winter() & (self.tool.has_scythe() | self.combat.has_any_weapon) & self.region.can_reach(Region.forest),
            Material.sap: self.ability.can_chop_trees(),
            Material.stone: self.ability.can_mine_stone(),
            Material.wood: self.ability.can_chop_trees(),
            Meal.ice_cream: (self.season.has(Season.summer) & self.money.can_spend_at(Region.town, 250)) | self.money.can_spend_at(Region.oasis, 240),
            Meal.strange_bun: self.relationship.has_hearts(NPC.shane, 7) & self.has(Ingredient.wheat_flour) & self.has(Fish.periwinkle) & self.has(ArtisanGood.void_mayonnaise),
            MetalBar.copper: self.can_smelt(Ore.copper),
            MetalBar.gold: self.can_smelt(Ore.gold),
            MetalBar.iridium: self.can_smelt(Ore.iridium),
            MetalBar.iron: self.can_smelt(Ore.iron),
            MetalBar.quartz: self.can_smelt(Mineral.quartz) | self.can_smelt("Fire Quartz") | (self.has(Machine.recycling_machine) & (self.has(Trash.broken_cd) | self.has(Trash.broken_glasses))),
            MetalBar.radioactive: self.can_smelt(Ore.radioactive),
            Mineral.any_gem: self.museum.has_any_gem(),
            Ore.copper: self.mine.can_mine_in_the_mines_floor_1_40() | self.mine.can_mine_in_the_skull_cavern() | self.tool.has_pan(),
            Ore.gold: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern() | self.tool.has_pan(ToolMaterial.gold),
            Ore.iridium: self.ability.can_mine_perfectly_in_the_skull_cavern() | (self.mine.can_mine_in_the_skull_cavern() & self.tool.has_pan(ToolMaterial.gold)),  # Could add self.fish_pond.can_get_fish_pond_reward(Fish.super_cucumber, 9, Ore.iridium) but it makes a logic loop
            Ore.iron: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern() | self.tool.has_pan(ToolMaterial.iron),
            Ore.radioactive: self.special_order.can_get_radioactive_ore(),
            RetainingSoil.basic: self.money.can_spend_at(Region.pierre_store, 100),
            RetainingSoil.quality: self.time.has_year_two & self.money.can_spend_at(Region.pierre_store, 150),
            SpecialItem.lucky_purple_shorts: self.special_items.has_purple_shorts(),
            SpecialItem.trimmed_purple_shorts: self.has(SpecialItem.lucky_purple_shorts) & self.has(Machine.sewing_machine),
            SpecialItem.far_away_stone: self.special_items.has_far_away_stone(),
            SpecialItem.solid_gold_lewis: self.special_items.has_solid_gold_lewis(),
            SpecialItem.advanced_tv_remote: self.special_items.has_advanced_tv_remote(),
            SpeedGro.basic: self.money.can_spend_at(Region.pierre_store, 100),
            SpeedGro.deluxe: self.time.has_year_two & self.money.can_spend_at(Region.pierre_store, 150),
            Trash.broken_cd: self.fishing.can_crab_pot_anywhere,
            Trash.broken_glasses: self.fishing.can_crab_pot_anywhere,
            Trash.driftwood: self.fishing.can_crab_pot_anywhere,
            Trash.joja_cola: self.money.can_spend_at(Region.saloon, 75),
            Trash.soggy_newspaper: self.fishing.can_crab_pot_anywhere,
            Trash.trash: self.fishing.can_crab_pot_anywhere,
            TreeSeed.acorn: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mahogany: self.region.can_reach(Region.secret_woods) & self.tool.has_tool(Tool.axe, ToolMaterial.iron) & self.skill.has_level(Skill.foraging, 1),
            TreeSeed.maple: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mushroom: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 5),
            TreeSeed.pine: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mossy: self.ability.can_chop_trees() & self.season.has(Season.summer),
            Fish.clam: self.tool.can_forage(Generic.any, Region.beach),
            Fish.cockle: self.tool.can_forage(Generic.any, Region.beach),
            WaterItem.green_algae: self.fishing.can_fish_in_freshwater(),
            WaterItem.cave_jelly: self.fishing.can_fish_at(Region.mines_floor_100) & self.tool.has_fishing_rod(FishingRod.bamboo),
            WaterItem.river_jelly: self.fishing.can_fish_at(Region.town) & self.tool.has_fishing_rod(FishingRod.bamboo),
            WaterItem.sea_jelly: self.fishing.can_fish_at(Region.beach) & self.tool.has_fishing_rod(FishingRod.bamboo),
            WaterItem.seaweed: self.fishing.can_fish_at(Region.tide_pools),
            WaterItem.white_algae: self.fishing.can_fish_at(Region.mines_floor_20) & self.tool.has_fishing_rod(FishingRod.bamboo),
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

        if self.options.bundle_randomization == BundleRandomization.option_meme:
            self.meme.initialize_rules()
            self.registry.item_rules.update(self.registry.meme_item_rules)

        self.quest.initialize_rules()
        self.quest.update_rules(self.mod.quest.get_modded_quest_rules())

        self.festival.initialize_rules()

        self.special_order.initialize_rules()
        self.special_order.update_rules(self.mod.special_order.get_modded_special_orders_rules())

        self.shirt.initialize_rules()
        self.registry.item_rules.update(self.registry.shirt_rules)

        for catalogue in items_by_catalogue:
            for item in items_by_catalogue[catalogue]:
                self.registry.item_rules[item] = self.has(catalogue)

        for boots in tier_by_boots:
            self.registry.item_rules[boots] = self.combat.has_specific_boots(boots)

    def setup_events(self, register_event: Callable[[str, str, StardewRule], None]) -> None:
        for item_event in all_item_events:
            rule = self.registry.item_rules[item_event.item]

            if isinstance(rule, Or) and bool(reaches := [r for r in rule.current_rules if isinstance(r, Reach) and r.resolution_hint == "Region"]):
                logger.debug("Sharding rule for %s in multiple logic events, placed in %s.", item_event.item, [r.spot for r in reaches])

                for i, reach in enumerate(reaches):
                    location_name = f"{item_event.name} sharded_{i}"
                    new_rule = self.region.can_reach(item_event.region)
                    register_event(item_event.name, reach.spot, new_rule, location_name=location_name)

                remaining_rules = [r for r in rule.current_rules if not isinstance(r, Reach) or r.resolution_hint != "Region"]
                if remaining_rules:
                    register_event(item_event.name, item_event.region, Or(*remaining_rules))

            else:
                register_event(item_event.name, item_event.region, rule)

            self.registry.item_rules[item_event.item] = self.received(item_event.name)

    def can_smelt(self, item: str) -> StardewRule:
        return self.has(Machine.furnace) & self.has(item)

    def has_island_trader(self) -> StardewRule:
        if self.content.is_enabled(ginger_island_content_pack):
            return self.region.can_reach(Region.island_trader)
        return self.logic.false_

    def has_abandoned_jojamart(self) -> StardewRule:
        return (self.received(CommunityUpgrade.movie_theater, 1) & self.season.has_any_not_winter()) | self.has_movie_theater()

    def has_movie_theater(self) -> StardewRule:
        return self.received(CommunityUpgrade.movie_theater, 2)

    def can_use_obelisk(self, obelisk: str) -> StardewRule:
        return self.region.can_reach(Region.farm) & self.building.has_wizard_building(obelisk)

    def can_purchase_statue_of_endless_fortune(self) -> StardewRule:
        return self.money.can_spend_at(Region.casino, 1_000_000)

    def has_statue_of_endless_fortune(self) -> StardewRule:
        can_purchase_rule = self.can_purchase_statue_of_endless_fortune()
        if self.options.include_endgame_locations == IncludeEndgameLocations.option_true:
            return can_purchase_rule & self.received(Machine.statue_endless_fortune)
        return can_purchase_rule
