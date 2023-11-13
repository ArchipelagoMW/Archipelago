from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, Union, Optional, Iterable, Sized, List, Set

from .data import all_fish, FishItem, all_purchasable_seeds, SeedItem, all_crops, CropItem
from .data.bundle_data import BundleItem
from .data.crops_data import crops_by_name
from .data.fish_data import island_fish
from .data.museum_data import all_museum_items, MuseumItem, all_museum_artifacts, dwarf_scrolls, all_museum_minerals
from .data.recipe_data import all_cooking_recipes, CookingRecipe, RecipeSource, FriendshipSource, QueenOfSauceSource, \
    StarterSource, ShopSource, SkillSource
from .data.villagers_data import all_villagers_by_name, Villager
from .items import all_items, Group
from .mods.logic.buildings import get_modded_building_rules
from .mods.logic.quests import get_modded_quest_rules
from .mods.logic.special_orders import get_modded_special_orders_rules
from .mods.logic.skullcavernelevator import has_skull_cavern_elevator_to_floor
from .mods.mod_data import ModNames
from .mods.logic import magic, skills
from .options import Museumsanity, SeasonRandomization, StardewValleyOptions, BuildingProgression, SkillProgression, ToolProgression, Friendsanity, Cropsanity, \
    ExcludeGingerIsland, ElevatorProgression, ArcadeMachineLocations, FestivalLocations, SpecialOrderLocations
from .regions import vanilla_regions
from .stardew_rule import False_, Reach, Or, True_, Received, Count, And, Has, TotalReceived, StardewRule
from .strings.animal_names import Animal, coop_animals, barn_animals
from .strings.animal_product_names import AnimalProduct
from .strings.ap_names.buff_names import Buff
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.building_names import Building
from .strings.calendar_names import Weekday
from .strings.craftable_names import Craftable
from .strings.crop_names import Fruit, Vegetable, all_fruits, all_vegetables
from .strings.fertilizer_names import Fertilizer
from .strings.festival_check_names import FestivalCheck
from .strings.fish_names import Fish, Trash, WaterItem
from .strings.flower_names import Flower
from .strings.forageable_names import Forageable
from .strings.fruit_tree_names import Sapling
from .strings.generic_names import Generic
from .strings.geode_names import Geode
from .strings.gift_names import Gift
from .strings.ingredient_names import Ingredient
from .strings.material_names import Material
from .strings.machine_names import Machine
from .strings.food_names import Meal, Beverage
from .strings.metal_names import Ore, MetalBar, Mineral, Fossil
from .strings.monster_drop_names import Loot
from .strings.performance_names import Performance
from .strings.quest_names import Quest
from .strings.region_names import Region
from .strings.season_names import Season
from .strings.seed_names import Seed
from .strings.skill_names import Skill, ModSkill
from .strings.special_order_names import SpecialOrder
from .strings.spells import MagicSpell
from .strings.tool_names import Tool, ToolMaterial, APTool
from .strings.tv_channel_names import Channel
from .strings.villager_names import NPC
from .strings.wallet_item_names import Wallet
from .strings.weapon_names import Weapon

MAX_MONTHS = 12
MONEY_PER_MONTH = 15000
MISSING_ITEM = "THIS ITEM IS MISSING"

tool_materials = {
    ToolMaterial.copper: 1,
    ToolMaterial.iron: 2,
    ToolMaterial.gold: 3,
    ToolMaterial.iridium: 4
}

tool_upgrade_prices = {
    ToolMaterial.copper: 2000,
    ToolMaterial.iron: 5000,
    ToolMaterial.gold: 10000,
    ToolMaterial.iridium: 25000
}

fishing_regions = [Region.beach, Region.town, Region.forest, Region.mountain, Region.island_south, Region.island_west]


@dataclass(frozen=True, repr=False)
class StardewLogic:
    player: int
    options: StardewValleyOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    sapling_rules: Dict[str, StardewRule] = field(default_factory=dict)
    tree_fruit_rules: Dict[str, StardewRule] = field(default_factory=dict)
    seed_rules: Dict[str, StardewRule] = field(default_factory=dict)
    cooking_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crop_rules: Dict[str, StardewRule] = field(default_factory=dict)
    fish_rules: Dict[str, StardewRule] = field(default_factory=dict)
    museum_rules: Dict[str, StardewRule] = field(default_factory=dict)
    building_rules: Dict[str, StardewRule] = field(default_factory=dict)
    quest_rules: Dict[str, StardewRule] = field(default_factory=dict)
    festival_rules: Dict[str, StardewRule] = field(default_factory=dict)
    special_order_rules: Dict[str, StardewRule] = field(default_factory=dict)

    def __post_init__(self):
        self.fish_rules.update({fish.name: self.can_catch_fish(fish) for fish in all_fish})
        self.museum_rules.update({donation.name: self.can_find_museum_item(donation) for donation in all_museum_items})

        for recipe in all_cooking_recipes:
            can_cook_rule = self.can_cook(recipe)
            if recipe.meal in self.cooking_rules:
                can_cook_rule = can_cook_rule | self.cooking_rules[recipe.meal]
            self.cooking_rules[recipe.meal] = can_cook_rule

        self.sapling_rules.update({
            Sapling.apple: self.can_buy_sapling(Fruit.apple),
            Sapling.apricot: self.can_buy_sapling(Fruit.apricot),
            Sapling.cherry: self.can_buy_sapling(Fruit.cherry),
            Sapling.orange: self.can_buy_sapling(Fruit.orange),
            Sapling.peach: self.can_buy_sapling(Fruit.peach),
            Sapling.pomegranate: self.can_buy_sapling(Fruit.pomegranate),
            Sapling.banana: self.can_buy_sapling(Fruit.banana),
            Sapling.mango: self.can_buy_sapling(Fruit.mango),
        })

        self.tree_fruit_rules.update({
            Fruit.apple: self.can_plant_and_grow_item(Season.fall),
            Fruit.apricot: self.can_plant_and_grow_item(Season.spring),
            Fruit.cherry: self.can_plant_and_grow_item(Season.spring),
            Fruit.orange: self.can_plant_and_grow_item(Season.summer),
            Fruit.peach: self.can_plant_and_grow_item(Season.summer),
            Fruit.pomegranate: self.can_plant_and_grow_item(Season.fall),
            Fruit.banana: self.can_plant_and_grow_item(Season.summer),
            Fruit.mango: self.can_plant_and_grow_item(Season.summer),
        })

        for tree_fruit in self.tree_fruit_rules:
            existing_rules = self.tree_fruit_rules[tree_fruit]
            sapling = f"{tree_fruit} Sapling"
            self.tree_fruit_rules[tree_fruit] = existing_rules & self.has(sapling) & self.has_lived_months(1)

        self.seed_rules.update({seed.name: self.can_buy_seed(seed) for seed in all_purchasable_seeds})
        self.crop_rules.update({crop.name: self.can_grow_crop(crop) for crop in all_crops})
        self.crop_rules.update({
            Seed.coffee: (self.has_season(Season.spring) | self.has_season(
                Season.summer)) & self.can_buy_seed(crops_by_name[Seed.coffee].seed),
            Fruit.ancient_fruit: (self.received("Ancient Seeds") | self.received("Ancient Seeds Recipe")) &
                             self.can_reach_region(Region.greenhouse) & self.has(Machine.seed_maker),
        })

        self.item_rules.update({
            ArtisanGood.aged_roe: self.can_preserves_jar(AnimalProduct.roe),
            AnimalProduct.any_egg: self.has(AnimalProduct.chicken_egg) | self.has(AnimalProduct.duck_egg),
            Fish.any: Or([self.can_catch_fish(fish) for fish in all_fish]),
            Geode.artifact_trove: self.has(Geode.omni) & self.can_reach_region(Region.desert),
            Craftable.bait: (self.has_skill_level(Skill.fishing, 2) & self.has(Loot.bug_meat)) | self.has(Machine.worm_bin),
            Fertilizer.basic: (self.has(Material.sap) & self.has_farming_level(1)) | (self.has_lived_months(1) & self.can_spend_money_at(Region.pierre_store, 100)),
            Fertilizer.quality: (self.has_farming_level(9) & self.has(Material.sap) & self.has(Fish.any)) | (self.has_year_two() & self.can_spend_money_at(Region.pierre_store, 150)),
            Fertilizer.deluxe: False_(),
            # self.received("Deluxe Fertilizer Recipe") & self.has(MetalBar.iridium) & self.has(SVItem.sap),
            Fertilizer.tree: self.has_skill_level(Skill.foraging, 7) & self.has(Material.fiber) & self.has(Material.stone),
            Loot.bat_wing: self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            ArtisanGood.battery_pack: (self.has(Machine.lightning_rod) & self.has_any_season_not_winter()) | self.has(Machine.solar_panel),
            Machine.bee_house: self.has_farming_level(3) & self.has(MetalBar.iron) & self.has(ArtisanGood.maple_syrup) & self.has(Material.coal) & self.has(Material.wood),
            Beverage.beer: self.can_keg(Vegetable.wheat) | self.can_spend_money_at(Region.saloon, 400),
            Forageable.blackberry: self.can_forage(Season.fall),
            Craftable.bomb: self.has_skill_level(Skill.mining, 6) & self.has(Material.coal) & self.has(Ore.iron),
            Fossil.bone_fragment: self.can_reach_region(Region.dig_site),
            Gift.bouquet: self.has_relationship(Generic.bachelor, 8) & self.can_spend_money_at(Region.pierre_store, 100),
            Meal.bread: self.can_spend_money_at(Region.saloon, 120),
            Trash.broken_cd: self.can_crab_pot(),
            Trash.broken_glasses: self.can_crab_pot(),
            Loot.bug_meat: self.can_mine_in_the_mines_floor_1_40(),
            Forageable.cactus_fruit: self.can_forage(Generic.any, Region.desert),
            Machine.cask: self.has_house(3) & self.can_reach_region(Region.cellar) & self.has(Material.wood) & self.has(Material.hardwood),
            Forageable.cave_carrot: self.can_forage(Generic.any, Region.mines_floor_10, True),
            ArtisanGood.caviar: self.can_preserves_jar(AnimalProduct.sturgeon_roe),
            Forageable.chanterelle: self.can_forage(Season.fall, Region.secret_woods),
            Machine.cheese_press: self.has_farming_level(6) & self.has(Material.wood) & self.has(Material.stone) & self.has(Material.hardwood) & self.has(MetalBar.copper),
            ArtisanGood.cheese: (self.has(AnimalProduct.cow_milk) & self.has(Machine.cheese_press)) | (self.can_reach_region(Region.desert) & self.has(Mineral.emerald)),
            Craftable.cherry_bomb: self.has_skill_level(Skill.mining, 1) & self.has(Material.coal) & self.has(Ore.copper),
            Animal.chicken: self.can_buy_animal(Animal.chicken),
            AnimalProduct.chicken_egg: self.has([AnimalProduct.egg, AnimalProduct.brown_egg, AnimalProduct.large_egg, AnimalProduct.large_brown_egg], 1),
            Material.cinder_shard: self.can_reach_region(Region.volcano_floor_5),
            WaterItem.clam: self.can_forage(Generic.any, Region.beach),
            Material.clay: self.can_reach_any_region([Region.farm, Region.beach, Region.quarry]) & self.has_tool(Tool.hoe),
            ArtisanGood.cloth: (self.has(AnimalProduct.wool) & self.has(Machine.loom)) | (self.can_reach_region(Region.desert) & self.has(Mineral.aquamarine)),
            Material.coal: self.can_mine_in_the_mines_floor_41_80() | self.can_do_panning(),
            WaterItem.cockle: self.can_forage(Generic.any, Region.beach),
            Forageable.coconut: self.can_forage(Generic.any, Region.desert),
            Beverage.coffee: self.can_keg(Seed.coffee) | self.has(Machine.coffee_maker) | (self.can_spend_money_at(Region.saloon, 300)) | self.has("Hot Java Ring"),
            Machine.coffee_maker: self.received(Machine.coffee_maker),
            Forageable.common_mushroom: self.can_forage(Season.fall) | (self.can_forage(Season.spring, Region.secret_woods)),
            MetalBar.copper: self.can_smelt(Ore.copper),
            Ore.copper: self.can_mine_in_the_mines_floor_1_40() | self.can_mine_in_the_skull_cavern() | self.can_do_panning(),
            WaterItem.coral: self.can_forage(Generic.any, Region.tide_pools) | self.can_forage(Season.summer, Region.beach),
            Animal.cow: self.can_buy_animal(Animal.cow),
            AnimalProduct.cow_milk: self.has(AnimalProduct.milk) | self.has(AnimalProduct.large_milk),
            Fish.crab: self.can_crab_pot(Region.beach),
            Machine.crab_pot: self.has_skill_level(Skill.fishing, 3) & (self.can_spend_money_at(Region.fish_shop, 1500) | (self.has(MetalBar.iron) & self.has(Material.wood))),
            Fish.crayfish: self.can_crab_pot(Region.town),
            Forageable.crocus: self.can_forage(Season.winter),
            Forageable.crystal_fruit: self.can_forage(Season.winter),
            Forageable.daffodil: self.can_forage(Season.spring),
            Forageable.dandelion: self.can_forage(Season.spring),
            Animal.dinosaur: self.has_building(Building.big_coop) & self.has(AnimalProduct.dinosaur_egg),
            Forageable.dragon_tooth: self.can_forage(Generic.any, Region.volcano_floor_10),
            "Dried Starfish": self.can_fish() & self.can_reach_region(Region.beach),
            Trash.driftwood: self.can_crab_pot(),
            AnimalProduct.duck_egg: self.has_animal(Animal.duck),
            AnimalProduct.duck_feather: self.has_happy_animal(Animal.duck),
            Animal.duck: self.can_buy_animal(Animal.duck),
            AnimalProduct.egg: self.has_animal(Animal.chicken),
            AnimalProduct.brown_egg: self.has_animal(Animal.chicken),
            "Energy Tonic": self.can_reach_region(Region.hospital) & self.can_spend_money(1000),
            Material.fiber: True_(),
            Forageable.fiddlehead_fern: self.can_forage(Season.summer, Region.secret_woods),
            "Magic Rock Candy": self.can_reach_region(Region.desert) & self.has("Prismatic Shard"),
            "Fishing Chest": self.can_fish_chests(),
            Craftable.flute_block: self.has_relationship(NPC.robin, 6) & self.can_reach_region(Region.carpenter) & self.has(Material.wood) & self.has(Ore.copper) & self.has(Material.fiber),
            Geode.frozen: self.can_mine_in_the_mines_floor_41_80(),
            Machine.furnace: self.has(Material.stone) & self.has(Ore.copper),
            Geode.geode: self.can_mine_in_the_mines_floor_1_40(),
            Forageable.ginger: self.can_forage(Generic.any, Region.island_west, True),
            ArtisanGood.goat_cheese: self.has(AnimalProduct.goat_milk) & self.has(Machine.cheese_press),
            AnimalProduct.goat_milk: self.has(Animal.goat),
            Animal.goat: self.can_buy_animal(Animal.goat),
            MetalBar.gold: self.can_smelt(Ore.gold),
            Ore.gold: self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern() | self.can_do_panning(),
            Geode.golden_coconut: self.can_reach_region(Region.island_north),
            Gift.golden_pumpkin: self.has_season(Season.fall) | self.can_open_geode(Geode.artifact_trove),
            WaterItem.green_algae: self.can_fish_in_freshwater(),
            ArtisanGood.green_tea: self.can_keg(Vegetable.tea_leaves),
            Material.hardwood: self.has_tool(Tool.axe, ToolMaterial.copper) & (self.can_reach_region(Region.secret_woods) | self.can_reach_region(Region.island_south)),
            Forageable.hay: self.has_building(Building.silo) & self.has_tool(Tool.scythe),
            Forageable.hazelnut: self.can_forage(Season.fall),
            Forageable.holly: self.can_forage(Season.winter),
            ArtisanGood.honey: self.can_spend_money_at(Region.oasis, 200) | (self.has(Machine.bee_house) & self.has_any_season_not_winter()),
            "Hot Java Ring": self.can_reach_region(Region.volcano_floor_10),
            Meal.ice_cream: (self.has_season(Season.summer) & self.can_spend_money_at(Region.town, 250)) | self.can_spend_money_at(Region.oasis, 240),
            # | (self.can_cook() & self.has_relationship(NPC.jodi, 7) & self.has(AnimalProduct.cow_milk) & self.has(Ingredient.sugar)),
            MetalBar.iridium: self.can_smelt(Ore.iridium),
            Ore.iridium: self.can_mine_in_the_skull_cavern(),
            MetalBar.iron: self.can_smelt(Ore.iron),
            Ore.iron: self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern() | self.can_do_panning(),
            ArtisanGood.jelly: self.has_jelly(),
            Trash.joja_cola: self.can_spend_money_at(Region.saloon, 75),
            "JotPK Small Buff": self.has_jotpk_power_level(2),
            "JotPK Medium Buff": self.has_jotpk_power_level(4),
            "JotPK Big Buff": self.has_jotpk_power_level(7),
            "JotPK Max Buff": self.has_jotpk_power_level(9),
            ArtisanGood.juice: self.has_juice(),
            "Junimo Kart Small Buff": self.has_junimo_kart_power_level(2),
            "Junimo Kart Medium Buff": self.has_junimo_kart_power_level(4),
            "Junimo Kart Big Buff": self.has_junimo_kart_power_level(6),
            "Junimo Kart Max Buff": self.has_junimo_kart_power_level(8),
            Machine.keg: self.has_farming_level(8) & self.has(Material.wood) & self.has(MetalBar.iron) & self.has(MetalBar.copper) & self.has(ArtisanGood.oak_resin),
            AnimalProduct.large_egg: self.has_happy_animal(Animal.chicken),
            AnimalProduct.large_brown_egg: self.has_happy_animal(Animal.chicken),
            AnimalProduct.large_goat_milk: self.has_happy_animal(Animal.goat),
            AnimalProduct.large_milk: self.has_happy_animal(Animal.cow),
            Forageable.leek: self.can_forage(Season.spring),
            Craftable.life_elixir: self.has_skill_level(Skill.combat, 2) & self.has(Forageable.red_mushroom) & self.has(Forageable.purple_mushroom) & self.has(Forageable.morel) & self.has(Forageable.chanterelle),
            Machine.lightning_rod: self.has_skill_level(Skill.foraging, 6) & self.has(MetalBar.iron) & self.has(MetalBar.quartz) & self.has(Loot.bat_wing),
            Fish.lobster: self.can_crab_pot(Region.beach),
            Machine.loom: self.has_farming_level(7) & self.has(Material.wood) & self.has(Material.fiber) & self.has(ArtisanGood.pine_tar),
            Forageable.magma_cap: self.can_forage(Generic.any, Region.volcano_floor_5),
            Geode.magma: self.can_mine_in_the_mines_floor_81_120() | (self.has(Fish.lava_eel) & self.has_building(Building.fish_pond)),
            ArtisanGood.maple_syrup: self.has(Machine.tapper),
            ArtisanGood.mayonnaise: self.has(Machine.mayonnaise_machine) & self.has(AnimalProduct.chicken_egg),
            Machine.mayonnaise_machine: self.has_farming_level(2) & self.has(Material.wood) & self.has(Material.stone) & self.has("Earth Crystal") & self.has(MetalBar.copper),
            ArtisanGood.mead: self.can_keg(ArtisanGood.honey),
            Craftable.mega_bomb: self.has_skill_level(Skill.mining, 8) & self.has(Ore.gold) & self.has(Loot.solar_essence) & self.has(Loot.void_essence),
            Gift.mermaid_pendant: self.can_reach_region(Region.tide_pools) & self.has_relationship(Generic.bachelor, 10) & self.has_house(1) & self.has(Craftable.rain_totem),
            AnimalProduct.milk: self.has_animal(Animal.cow),
            Craftable.monster_musk: self.has_prismatic_jelly_reward_access() & self.has(Loot.slime) & self.has(Loot.bat_wing),
            Forageable.morel: self.can_forage(Season.spring, Region.secret_woods),
            "Muscle Remedy": self.can_reach_region(Region.hospital) & self.can_spend_money(1000),
            Fish.mussel: self.can_forage(Generic.any, Region.beach) or self.has(Fish.mussel_node),
            Fish.mussel_node: self.can_reach_region(Region.island_west),
            WaterItem.nautilus_shell: self.can_forage(Season.winter, Region.beach),
            ArtisanGood.oak_resin: self.has(Machine.tapper),
            Ingredient.oil: self.can_spend_money_at(Region.pierre_store, 200) | (self.has(Machine.oil_maker) & (self.has(Vegetable.corn) | self.has(Flower.sunflower) | self.has(Seed.sunflower))),
            Machine.oil_maker: self.has_farming_level(8) & self.has(Loot.slime) & self.has(Material.hardwood) & self.has(MetalBar.gold),
            Craftable.oil_of_garlic: (self.has_skill_level(Skill.combat, 6) & self.has(Vegetable.garlic) & self.has(Ingredient.oil)) | (self.can_spend_money_at(Region.mines_dwarf_shop, 3000)),
            Geode.omni: self.can_mine_in_the_mines_floor_41_80() | self.can_reach_region(Region.desert) | self.can_do_panning() | self.received(Wallet.rusty_key) | (self.has(Fish.octopus) & self.has_building(Building.fish_pond)) | self.can_reach_region(Region.volcano_floor_10),
            Animal.ostrich: self.has_building(Building.barn) & self.has(AnimalProduct.ostrich_egg) & self.has(Machine.ostrich_incubator),
            AnimalProduct.ostrich_egg: self.can_forage(Generic.any, Region.island_north, True),
            Machine.ostrich_incubator: self.received("Ostrich Incubator Recipe") & self.has(Fossil.bone_fragment) & self.has(Material.hardwood) & self.has(Material.cinder_shard),
            Fish.oyster: self.can_forage(Generic.any, Region.beach),
            ArtisanGood.pale_ale: self.can_keg(Vegetable.hops),
            Gift.pearl: (self.has(Fish.blobfish) & self.has_building(Building.fish_pond)) | self.can_open_geode(Geode.artifact_trove),
            Fish.periwinkle: self.can_crab_pot(Region.town),
            ArtisanGood.pickles: self.has_pickle(),
            Animal.pig: self.can_buy_animal(Animal.pig),
            Beverage.pina_colada: self.can_spend_money_at(Region.island_resort, 600),
            ArtisanGood.pine_tar: self.has(Machine.tapper),
            Meal.pizza: self.can_spend_money_at(Region.saloon, 600),
            Machine.preserves_jar: self.has_farming_level(4) & self.has(Material.wood) & self.has(Material.stone) & self.has(Material.coal),
            Forageable.purple_mushroom: self.can_forage(Generic.any, Region.mines_floor_95) | self.can_forage(Generic.any, Region.skull_cavern_25),
            Animal.rabbit: self.can_buy_animal(Animal.rabbit),
            AnimalProduct.rabbit_foot: self.has_happy_animal(Animal.rabbit),
            MetalBar.radioactive: self.can_smelt(Ore.radioactive),
            Ore.radioactive: self.can_mine_perfectly() & self.can_reach_region(Region.qi_walnut_room),
            Forageable.rainbow_shell: self.can_forage(Season.summer, Region.beach),
            Craftable.rain_totem: self.has_skill_level(Skill.foraging, 9) & self.has(Material.hardwood) & self.has(ArtisanGood.truffle_oil) & self.has(ArtisanGood.pine_tar),
            Machine.recycling_machine: self.has_skill_level(Skill.fishing, 4) & self.has(Material.wood) & self.has(Material.stone) & self.has(MetalBar.iron),
            Forageable.red_mushroom: self.can_forage(Season.summer, Region.secret_woods) | self.can_forage(Season.fall, Region.secret_woods),
            MetalBar.quartz: self.can_smelt("Quartz") | self.can_smelt("Fire Quartz") |
                              (self.has(Machine.recycling_machine) & (self.has(Trash.broken_cd) | self.has(Trash.broken_glasses))),
            Ingredient.rice: self.can_spend_money_at(Region.pierre_store, 200) | (
                    self.has_building(Building.mill) & self.has(Vegetable.unmilled_rice)),
            AnimalProduct.roe: self.can_fish() & self.has_building(Building.fish_pond),
            Meal.salad: self.can_spend_money_at(Region.saloon, 220),
            # | (self.can_cook() & self.has_relationship(NPC.emily, 3) & self.has(Forageable.leek) & self.has(Forageable.dandelion) &
            # self.has(Ingredient.vinegar)),
            Forageable.salmonberry: self.can_forage(Season.spring),
            Material.sap: self.can_chop_trees(),
            Craftable.scarecrow: self.has_farming_level(1) & self.has(Material.wood) & self.has(Material.coal) & self.has(Material.fiber),
            WaterItem.sea_urchin: self.can_forage(Generic.any, Region.tide_pools),
            WaterItem.seaweed: (self.can_fish() & self.can_reach_region(Region.beach)) | self.can_reach_region(
                Region.tide_pools),
            Forageable.secret_note: self.received(Wallet.magnifying_glass) & (self.can_chop_trees() | self.can_mine_in_the_mines_floor_1_40()),
            Machine.seed_maker: self.has_farming_level(9) & self.has(Material.wood) & self.has(MetalBar.gold) & self.has(
                Material.coal),
            Animal.sheep: self.can_buy_animal(Animal.sheep),
            Fish.shrimp: self.can_crab_pot(Region.beach),
            Loot.slime: self.can_mine_in_the_mines_floor_1_40(),
            Weapon.any_slingshot: self.received(Weapon.slingshot) | self.received(Weapon.master_slingshot),
            Fish.snail: self.can_crab_pot(Region.town),
            Forageable.snow_yam: self.can_forage(Season.winter, Region.beach, True),
            Trash.soggy_newspaper: self.can_crab_pot(),
            Loot.solar_essence: self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            Machine.solar_panel: self.received("Solar Panel Recipe") & self.has(MetalBar.quartz) & self.has(
                MetalBar.iron) & self.has(MetalBar.gold),
            Meal.spaghetti: self.can_spend_money_at(Region.saloon, 240),
            Forageable.spice_berry: self.can_forage(Season.summer),
            Forageable.spring_onion: self.can_forage(Season.spring),
            AnimalProduct.squid_ink: self.can_mine_in_the_mines_floor_81_120() | (self.has_building(Building.fish_pond) & self.has(Fish.squid)),
            Craftable.staircase: self.has_skill_level(Skill.mining, 2) & self.has(Material.stone),
            Material.stone: self.has_tool(Tool.pickaxe),
            Meal.strange_bun: self.has_relationship(NPC.shane, 7) & self.has(Ingredient.wheat_flour) & self.has(Fish.periwinkle) & self.has(ArtisanGood.void_mayonnaise),
            AnimalProduct.sturgeon_roe: self.has(Fish.sturgeon) & self.has_building(Building.fish_pond),
            Ingredient.sugar: self.can_spend_money_at(Region.pierre_store, 100) | (
                    self.has_building(Building.mill) & self.has(Vegetable.beet)),
            Forageable.sweet_pea: self.can_forage(Season.summer),
            Machine.tapper: self.has_skill_level(Skill.foraging, 3) & self.has(Material.wood) & self.has(MetalBar.copper),
            Vegetable.tea_leaves: self.has(Sapling.tea) & self.has_lived_months(2) & self.has_any_season_not_winter(),
            Sapling.tea: self.has_relationship(NPC.caroline, 2) & self.has(Material.fiber) & self.has(Material.wood),
            Trash.trash: self.can_crab_pot(),
            Beverage.triple_shot_espresso: self.has("Hot Java Ring"),
            ArtisanGood.truffle_oil: self.has(AnimalProduct.truffle) & self.has(Machine.oil_maker),
            AnimalProduct.truffle: self.has_animal(Animal.pig) & self.has_any_season_not_winter(),
            Ingredient.vinegar: self.can_spend_money_at(Region.pierre_store, 200),
            AnimalProduct.void_egg: self.can_spend_money_at(Region.sewer, 5000) | (self.has_building(Building.fish_pond) & self.has(Fish.void_salmon)),
            Loot.void_essence: self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            ArtisanGood.void_mayonnaise: (self.can_reach_region(Region.witch_swamp) & self.can_fish()) | (self.has(Machine.mayonnaise_machine) & self.has(AnimalProduct.void_egg)),
            Ingredient.wheat_flour: self.can_spend_money_at(Region.pierre_store, 100) |
                                    (self.has_building(Building.mill) & self.has(Vegetable.wheat)),
            WaterItem.white_algae: self.can_fish() & self.can_reach_region(Region.mines_floor_20),
            Forageable.wild_horseradish: self.can_forage(Season.spring),
            Forageable.wild_plum: self.can_forage(Season.fall),
            Gift.wilted_bouquet: self.has(Machine.furnace) & self.has(Gift.bouquet) & self.has(Material.coal),
            ArtisanGood.wine: self.has_wine(),
            Forageable.winter_root: self.can_forage(Season.winter, Region.forest, True),
            Material.wood: self.has_tool(Tool.axe),
            AnimalProduct.wool: self.has_animal(Animal.rabbit) | self.has_animal(Animal.sheep),
            Machine.worm_bin: self.has_skill_level(Skill.fishing, 8) & self.has(Material.hardwood) & self.has(MetalBar.gold) & self.has(MetalBar.iron) & self.has(Material.fiber),
        })
        self.item_rules.update(self.fish_rules)
        self.item_rules.update(self.museum_rules)
        self.item_rules.update(self.sapling_rules)
        self.item_rules.update(self.tree_fruit_rules)
        self.item_rules.update(self.seed_rules)
        self.item_rules.update(self.crop_rules)

        # For some recipes, the cooked item can be obtained directly, so we either cook it or get it
        for recipe in self.cooking_rules:
            cooking_rule = self.cooking_rules[recipe]
            obtention_rule = self.item_rules[recipe] if recipe in self.item_rules else False_()
            self.item_rules[recipe] = obtention_rule | cooking_rule

        self.building_rules.update({
            Building.barn: self.can_spend_money_at(Region.carpenter, 6000) & self.has([Material.wood, Material.stone]),
            Building.big_barn: self.can_spend_money_at(Region.carpenter, 12000) & self.has([Material.wood, Material.stone]) & self.has_building(Building.barn),
            Building.deluxe_barn: self.can_spend_money_at(Region.carpenter, 25000) & self.has([Material.wood, Material.stone]) & self.has_building(Building.big_barn),
            Building.coop: self.can_spend_money_at(Region.carpenter, 4000) & self.has([Material.wood, Material.stone]),
            Building.big_coop: self.can_spend_money_at(Region.carpenter, 10000) & self.has([Material.wood, Material.stone]) & self.has_building(Building.coop),
            Building.deluxe_coop: self.can_spend_money_at(Region.carpenter, 20000) & self.has([Material.wood, Material.stone]) & self.has_building(Building.big_coop),
            Building.fish_pond: self.can_spend_money_at(Region.carpenter, 5000) & self.has([Material.stone, WaterItem.seaweed, WaterItem.green_algae]),
            Building.mill: self.can_spend_money_at(Region.carpenter, 2500) & self.has([Material.stone, Material.wood, ArtisanGood.cloth]),
            Building.shed: self.can_spend_money_at(Region.carpenter, 15000) & self.has(Material.wood),
            Building.big_shed: self.can_spend_money_at(Region.carpenter, 20000) & self.has([Material.wood, Material.stone]) & self.has_building(Building.shed),
            Building.silo: self.can_spend_money_at(Region.carpenter, 100) & self.has([Material.stone, Material.clay, MetalBar.copper]),
            Building.slime_hutch: self.can_spend_money_at(Region.carpenter, 10000) & self.has([Material.stone, MetalBar.quartz, MetalBar.iridium]),
            Building.stable: self.can_spend_money_at(Region.carpenter, 10000) & self.has([Material.hardwood, MetalBar.iron]),
            Building.well: self.can_spend_money_at(Region.carpenter, 1000) & self.has(Material.stone),
            Building.shipping_bin: self.can_spend_money_at(Region.carpenter, 250) & self.has(Material.wood),
            Building.kitchen: self.can_spend_money_at(Region.carpenter, 10000) & self.has(Material.wood) & self.has_house(0),
            Building.kids_room: self.can_spend_money_at(Region.carpenter, 50000) & self.has(Material.hardwood) & self.has_house(1),
            Building.cellar: self.can_spend_money_at(Region.carpenter, 100000) & self.has_house(2),
        })

        self.building_rules.update(get_modded_building_rules(self, self.options.mods))

        self.quest_rules.update({
            Quest.introductions: self.can_reach_region(Region.town),
            Quest.how_to_win_friends: self.can_complete_quest(Quest.introductions),
            Quest.getting_started: self.has(Vegetable.parsnip) & self.has_tool(Tool.hoe) & self.can_water(0),
            Quest.to_the_beach: self.can_reach_region(Region.beach),
            Quest.raising_animals: self.can_complete_quest(Quest.getting_started) & self.has_building(Building.coop),
            Quest.advancement: self.can_complete_quest(Quest.getting_started) & self.has(Craftable.scarecrow),
            Quest.archaeology: (self.has_tool(Tool.hoe) | self.can_mine_in_the_mines_floor_1_40() | self.can_fish()) & self.can_reach_region(Region.museum),
            Quest.meet_the_wizard: self.can_reach_region(Region.town) & self.can_reach_region(Region.community_center) & self.can_reach_region(Region.wizard_tower),
            Quest.forging_ahead: self.has(Ore.copper) & self.has(Machine.furnace),
            Quest.smelting: self.has(MetalBar.copper),
            Quest.initiation: self.can_mine_in_the_mines_floor_1_40(),
            Quest.robins_lost_axe: self.has_season(Season.spring) & self.can_reach_region(Region.forest) & self.can_meet(NPC.robin),
            Quest.jodis_request: self.has_season(Season.spring) & self.has(Vegetable.cauliflower) & self.can_meet(NPC.jodi),
            Quest.mayors_shorts: self.has_season(Season.summer) & self.can_reach_region(Region.ranch) &
                                 (self.has_relationship(NPC.marnie, 2) | (magic.can_blink(self))) & self.can_meet(NPC.lewis),
            Quest.blackberry_basket: self.has_season(Season.fall) & self.can_meet(NPC.linus),
            Quest.marnies_request: self.has_relationship(NPC.marnie, 3) & self.has(Forageable.cave_carrot) & self.can_reach_region(Region.ranch),
            Quest.pam_is_thirsty: self.has_season(Season.summer) & self.has(ArtisanGood.pale_ale) & self.can_meet(NPC.pam),
            Quest.a_dark_reagent: self.has_season(Season.winter) & self.has(Loot.void_essence) & self.can_meet(NPC.wizard),
            Quest.cows_delight: self.has_season(Season.fall) & self.has(Vegetable.amaranth) & self.can_meet(NPC.marnie),
            Quest.the_skull_key: self.received(Wallet.skull_key) & self.can_reach_region(Region.skull_cavern_entrance),
            Quest.crop_research: self.has_season(Season.summer) & self.has(Fruit.melon) & self.can_meet(NPC.demetrius),
            Quest.knee_therapy: self.has_season(Season.summer) & self.has(Fruit.hot_pepper) & self.can_meet(NPC.george),
            Quest.robins_request: self.has_season(Season.winter) & self.has(Material.hardwood) & self.can_meet(NPC.robin),
            Quest.qis_challenge: self.can_mine_in_the_skull_cavern(),
            Quest.the_mysterious_qi: self.can_reach_region(Region.bus_tunnel) & self.has(ArtisanGood.battery_pack) & self.can_reach_region(Region.desert) & self.has(Forageable.rainbow_shell) & self.has(Vegetable.beet) & self.has(Loot.solar_essence),
            Quest.carving_pumpkins: self.has_season(Season.fall) & self.has(Vegetable.pumpkin) & self.can_meet(NPC.caroline),
            Quest.a_winter_mystery: self.has_season(Season.winter) & self.can_reach_region(Region.town),
            Quest.strange_note: self.has(Forageable.secret_note) & self.can_reach_region(Region.secret_woods) & self.has(ArtisanGood.maple_syrup),
            Quest.cryptic_note: self.has(Forageable.secret_note) & self.can_reach_region(Region.skull_cavern_100),
            Quest.fresh_fruit: self.has_season(Season.spring) & self.has(Fruit.apricot) & self.can_meet(NPC.emily),
            Quest.aquatic_research: self.has_season(Season.summer) & self.has(Fish.pufferfish) & self.can_meet(NPC.demetrius),
            Quest.a_soldiers_star: self.has_season(Season.summer) & self.has_year_two() & self.has(Fruit.starfruit) & self.can_meet(NPC.kent),
            Quest.mayors_need: self.has_season(Season.summer) & self.has(ArtisanGood.truffle_oil) & self.can_meet(NPC.lewis),
            Quest.wanted_lobster: self.has_season(Season.fall) & self.has_season(Season.fall) & self.has(Fish.lobster) & self.can_meet(NPC.gus),
            Quest.pam_needs_juice: self.has_season(Season.fall) & self.has(ArtisanGood.battery_pack) & self.can_meet(NPC.pam),
            Quest.fish_casserole: self.has_relationship(NPC.jodi, 4) & self.has(Fish.largemouth_bass) & self.can_reach_region(Region.sam_house),
            Quest.catch_a_squid: self.has_season(Season.winter) & self.has(Fish.squid) & self.can_meet(NPC.willy),
            Quest.fish_stew: self.has_season(Season.winter) & self.has(Fish.albacore) & self.can_meet(NPC.gus),
            Quest.pierres_notice: self.has_season(Season.spring) & self.has("Sashimi") & self.can_meet(NPC.pierre),
            Quest.clints_attempt: self.has_season(Season.winter) & self.has(Mineral.amethyst) & self.can_meet(NPC.emily),
            Quest.a_favor_for_clint: self.has_season(Season.winter) & self.has(MetalBar.iron) & self.can_meet(NPC.clint),
            Quest.staff_of_power: self.has_season(Season.winter) & self.has(MetalBar.iridium) & self.can_meet(NPC.wizard),
            Quest.grannys_gift: self.has_season(Season.spring) & self.has(Forageable.leek) & self.can_meet(NPC.evelyn),
            Quest.exotic_spirits: self.has_season(Season.winter) & self.has(Forageable.coconut) & self.can_meet(NPC.gus),
            Quest.catch_a_lingcod: self.has_season(Season.winter) & self.has("Lingcod") & self.can_meet(NPC.willy),
            Quest.dark_talisman: self.has_rusty_key() & self.can_reach_region(Region.railroad) & self.can_meet(NPC.krobus) & self.can_reach_region(Region.mutant_bug_lair),
            Quest.goblin_problem: self.can_reach_region(Region.witch_swamp) & self.has(ArtisanGood.void_mayonnaise),
            Quest.magic_ink: self.can_reach_region(Region.witch_hut) & self.can_meet(NPC.wizard),
            Quest.the_pirates_wife: self.can_reach_region(Region.island_west) & self.can_meet(NPC.kent) &
                                    self.can_meet(NPC.gus) & self.can_meet(NPC.sandy) & self.can_meet(NPC.george) &
                                    self.can_meet(NPC.wizard) & self.can_meet(NPC.willy),
        })

        self.quest_rules.update(get_modded_quest_rules(self, self.options.mods))

        self.festival_rules.update({
            FestivalCheck.egg_hunt: self.has_season(Season.spring) & self.can_reach_region(Region.town) & self.can_win_egg_hunt(),
            FestivalCheck.strawberry_seeds: self.has_season(Season.spring) & self.can_reach_region(Region.town) & self.can_spend_money(1000),
            FestivalCheck.dance: self.has_season(Season.spring) & self.can_reach_region(Region.forest) & self.has_relationship(Generic.bachelor, 4),
            FestivalCheck.rarecrow_5: self.has_season(Season.spring) & self.can_reach_region(Region.forest) & self.can_spend_money(2500),
            FestivalCheck.luau_soup: self.has_season(Season.summer) & self.can_reach_region(Region.beach) & self.can_succeed_luau_soup(),
            FestivalCheck.moonlight_jellies: self.has_season(Season.summer) & self.can_reach_region(Region.beach),
            FestivalCheck.smashing_stone: self.has_season(Season.fall) & self.can_reach_region(Region.town),
            FestivalCheck.grange_display: self.has_season(Season.fall) & self.can_reach_region(Region.town) & self.can_succeed_grange_display(),
            FestivalCheck.rarecrow_1: self.has_season(Season.fall) & self.can_reach_region(Region.town),  # only cost star tokens
            FestivalCheck.fair_stardrop: self.has_season(Season.fall) & self.can_reach_region(Region.town),  # only cost star tokens
            FestivalCheck.spirit_eve_maze: self.has_season(Season.fall) & self.can_reach_region(Region.town),
            FestivalCheck.rarecrow_2: self.has_season(Season.fall) & self.can_reach_region(Region.town) & self.can_spend_money(5000),
            FestivalCheck.fishing_competition: self.has_season(Season.winter) & self.can_reach_region(Region.forest) & self.can_win_fishing_competition(),
            FestivalCheck.rarecrow_4: self.has_season(Season.winter) & self.can_reach_region(Region.forest) & self.can_spend_money(5000),
            FestivalCheck.mermaid_pearl: self.has_season(Season.winter) & self.can_reach_region(Region.beach),
            FestivalCheck.cone_hat: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(2500),
            FestivalCheck.iridium_fireplace: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(15000),
            FestivalCheck.rarecrow_7: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(5000) & self.can_donate_museum_artifacts(20),
            FestivalCheck.rarecrow_8: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(5000) & self.can_donate_museum_items(40),
            FestivalCheck.lupini_red_eagle: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(1200),
            FestivalCheck.lupini_portrait_mermaid: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(1200),
            FestivalCheck.lupini_solar_kingdom: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.can_spend_money(1200),
            FestivalCheck.lupini_clouds: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.has_year_two() & self.can_spend_money(1200),
            FestivalCheck.lupini_1000_years: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.has_year_two() & self.can_spend_money(1200),
            FestivalCheck.lupini_three_trees: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.has_year_two() & self.can_spend_money(1200),
            FestivalCheck.lupini_the_serpent: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.has_year_three() & self.can_spend_money(1200),
            FestivalCheck.lupini_tropical_fish: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.has_year_three() & self.can_spend_money(1200),
            FestivalCheck.lupini_land_of_clay: self.has_season(Season.winter) & self.can_reach_region(Region.beach) & self.has_year_three() & self.can_spend_money(1200),
            FestivalCheck.secret_santa: self.has_season(Season.winter) & self.can_reach_region(Region.town) & self.has_any_universal_love(),
            FestivalCheck.legend_of_the_winter_star: self.has_season(Season.winter) & self.can_reach_region(Region.town),
            FestivalCheck.all_rarecrows: self.can_reach_region(Region.farm) & self.has_all_rarecrows(),
        })

        self.special_order_rules.update({
            SpecialOrder.island_ingredients: self.can_meet(NPC.caroline) & self.has_island_transport() & self.can_farm_perfectly() &
                                             self.can_ship(Vegetable.taro_root) & self.can_ship(Fruit.pineapple) & self.can_ship(Forageable.ginger),
            SpecialOrder.cave_patrol: self.can_meet(NPC.clint) & self.can_mine_perfectly() & self.can_mine_to_floor(120),
            SpecialOrder.aquatic_overpopulation: self.can_meet(NPC.demetrius) & self.can_fish_perfectly(),
            SpecialOrder.biome_balance: self.can_meet(NPC.demetrius) & self.can_fish_perfectly(),
            SpecialOrder.rock_rejuivenation: self.has_relationship(NPC.emily, 4) & self.has(Mineral.ruby) & self.has(Mineral.topaz) &
                                             self.has(Mineral.emerald) & self.has(Mineral.jade) & self.has(Mineral.amethyst) &
                                             self.has(ArtisanGood.cloth) & self.can_reach_region(Region.haley_house),
            SpecialOrder.gifts_for_george: self.can_reach_region(Region.alex_house) & self.has_season(Season.spring) & self.has(Forageable.leek),
            SpecialOrder.fragments_of_the_past: self.can_reach_region(Region.museum) & self.can_reach_region(Region.dig_site) & self.has_tool(Tool.pickaxe),
            SpecialOrder.gus_famous_omelet: self.can_reach_region(Region.saloon) & self.has(AnimalProduct.any_egg),
            SpecialOrder.crop_order: self.can_farm_perfectly() & self.can_ship(),
            SpecialOrder.community_cleanup: self.can_reach_region(Region.railroad) & self.can_crab_pot(),
            SpecialOrder.the_strong_stuff: self.can_reach_region(Region.trailer) & self.can_keg(Vegetable.potato),
            SpecialOrder.pierres_prime_produce: self.can_reach_region(Region.pierre_store) & self.can_farm_perfectly(),
            SpecialOrder.robins_project: self.can_meet(NPC.robin) & self.can_reach_region(Region.carpenter) & self.can_chop_perfectly() &
                                         self.has(Material.hardwood),
            SpecialOrder.robins_resource_rush: self.can_meet(NPC.robin) & self.can_reach_region(Region.carpenter) & self.can_chop_perfectly() &
                                               self.has(Fertilizer.tree) & self.can_mine_perfectly(),
            SpecialOrder.juicy_bugs_wanted_yum: self.can_reach_region(Region.beach) & self.has(Loot.bug_meat),
            SpecialOrder.tropical_fish: self.can_meet(NPC.willy) & self.received("Island Resort") & self.has_island_transport() &
                                        self.has(Fish.stingray) & self.has(Fish.blue_discus) & self.has(Fish.lionfish),
            SpecialOrder.a_curious_substance: self.can_reach_region(Region.wizard_tower) & self.can_mine_perfectly() & self.can_mine_to_floor(80),
            SpecialOrder.prismatic_jelly: self.can_reach_region(Region.wizard_tower) & self.can_mine_perfectly() & self.can_mine_to_floor(40),
            SpecialOrder.qis_crop: self.can_farm_perfectly() & self.can_reach_region(Region.greenhouse) &
                         self.can_reach_region(Region.island_west) & self.has_total_skill_level(50) &
                         self.has(Machine.seed_maker) & self.has_building(Building.shipping_bin),
            SpecialOrder.lets_play_a_game: self.has_junimo_kart_max_level(),
            SpecialOrder.four_precious_stones: self.has_lived_months(MAX_MONTHS) & self.has("Prismatic Shard") &
                                    self.can_mine_perfectly_in_the_skull_cavern(),
            SpecialOrder.qis_hungry_challenge: self.can_mine_perfectly_in_the_skull_cavern() & self.has_max_buffs(),
            SpecialOrder.qis_cuisine: self.can_cook() & (self.can_spend_money_at(Region.saloon, 205000) | self.can_spend_money_at(Region.pierre_store, 170000)) &
                                      self.can_ship(),
            SpecialOrder.qis_kindness: self.can_give_loved_gifts_to_everyone(),
            SpecialOrder.extended_family: self.can_fish_perfectly() & self.has(Fish.angler) & self.has(Fish.glacierfish) &
                               self.has(Fish.crimsonfish) & self.has(Fish.mutant_carp) & self.has(Fish.legend),
            SpecialOrder.danger_in_the_deep: self.can_mine_perfectly() & self.has_mine_elevator_to_floor(120),
            SpecialOrder.skull_cavern_invasion: self.can_mine_perfectly_in_the_skull_cavern() & self.has_max_buffs(),
            SpecialOrder.qis_prismatic_grange: self.has(Loot.bug_meat) & # 100 Bug Meat
                                               self.can_spend_money_at(Region.saloon, 24000) &  # 100 Spaghetti
                                               self.can_spend_money_at(Region.blacksmith, 15000) &  # 100 Copper Ore
                                               self.can_spend_money_at(Region.ranch, 5000) &  # 100 Hay
                                               self.can_spend_money_at(Region.saloon, 22000) &  # 100 Salads
                                               self.can_spend_money_at(Region.saloon, 7500) &  # 100 Joja Cola
                                               self.can_spend_money(80000),  # I need this extra rule because money rules aren't additive...
        })

        self.special_order_rules.update(get_modded_special_orders_rules(self, self.options.mods))

    def has(self, items: Union[str, (Iterable[str], Sized)], count: Optional[int] = None) -> StardewRule:
        if isinstance(items, str):
            return Has(items, self.item_rules)

        if len(items) == 0:
            return True_()

        if count is None or count == len(items):
            return And(self.has(item) for item in items)

        if count == 1:
            return Or(self.has(item) for item in items)

        return Count(count, (self.has(item) for item in items))

    def received(self, items: Union[str, Iterable[str]], count: Optional[int] = 1) -> StardewRule:
        if count <= 0 or not items:
            return True_()

        if isinstance(items, str):
            return Received(items, self.player, count)

        if count is None:
            return And(self.received(item) for item in items)

        if count == 1:
            return Or(self.received(item) for item in items)

        return TotalReceived(count, items, self.player)

    def can_reach_region(self, spot: str) -> StardewRule:
        return Reach(spot, "Region", self.player)

    def can_reach_any_region(self, spots: Iterable[str]) -> StardewRule:
        return Or(self.can_reach_region(spot) for spot in spots)

    def can_reach_all_regions(self, spots: Iterable[str]) -> StardewRule:
        return And(self.can_reach_region(spot) for spot in spots)

    def can_reach_all_regions_except_one(self, spots: Iterable[str]) -> StardewRule:
        num_required = len(list(spots)) - 1
        if num_required <= 0:
            num_required = len(list(spots))
        return Count(num_required, [self.can_reach_region(spot) for spot in spots])

    def can_reach_location(self, spot: str) -> StardewRule:
        return Reach(spot, "Location", self.player)

    def can_reach_entrance(self, spot: str) -> StardewRule:
        return Reach(spot, "Entrance", self.player)

    def can_have_earned_total_money(self, amount: int) -> StardewRule:
        return self.has_lived_months(min(8, amount // MONEY_PER_MONTH))

    def can_spend_money(self, amount: int) -> StardewRule:
        if self.options.starting_money == -1:
            return True_()
        return self.has_lived_months(min(8, amount // (MONEY_PER_MONTH // 5)))

    def can_spend_money_at(self, region: str, amount: int) -> StardewRule:
        return self.can_reach_region(region) & self.can_spend_money(amount)

    def has_tool(self, tool: str, material: str = ToolMaterial.basic) -> StardewRule:
        if material == ToolMaterial.basic or tool == Tool.scythe:
            return True_()

        if self.options.tool_progression == ToolProgression.option_progressive:
            return self.received(f"Progressive {tool}", count=tool_materials[material])

        return self.has(f"{material} Bar") & self.can_spend_money(tool_upgrade_prices[material])

    def can_earn_skill_level(self, skill: str, level: int) -> StardewRule:
        if level <= 0:
            return True_()

        tool_level = (level - 1) // 2
        tool_material = ToolMaterial.tiers[tool_level]
        months = max(1, level - 1)
        months_rule = self.has_lived_months(months)
        previous_level_rule = self.has_skill_level(skill, level - 1)

        if skill == Skill.fishing:
            xp_rule = self.can_get_fishing_xp() & self.has_tool(Tool.fishing_rod, ToolMaterial.tiers[max(tool_level, 3)])
        elif skill == Skill.farming:
            xp_rule = self.can_get_farming_xp() & self.has_tool(Tool.hoe, tool_material) & self.can_water(tool_level)
        elif skill == Skill.foraging:
            xp_rule = self.can_get_foraging_xp() & \
                      (self.has_tool(Tool.axe, tool_material) | magic.can_use_clear_debris_instead_of_tool_level(self, tool_level))
        elif skill == Skill.mining:
            xp_rule = self.can_get_mining_xp() & \
                      (self.has_tool(Tool.pickaxe, tool_material) | magic.can_use_clear_debris_instead_of_tool_level(self, tool_level))
        elif skill == Skill.combat:
            combat_tier = Performance.tiers[tool_level]
            xp_rule = self.can_get_combat_xp() & self.can_do_combat_at_level(combat_tier)
        else:
            xp_rule = skills.can_earn_mod_skill_level(self, skill, level)

        return previous_level_rule & months_rule & xp_rule

    def has_skill_level(self, skill: str, level: int) -> StardewRule:
        if level <= 0:
            return True_()

        if self.options.skill_progression == SkillProgression.option_progressive:
            return self.received(f"{skill} Level", count=level)

        return self.can_earn_skill_level(skill, level)

    def has_farming_level(self, level: int) -> StardewRule:
        return self.has_skill_level(Skill.farming, level)

    def has_total_skill_level(self, level: int, allow_modded_skills: bool = False) -> StardewRule:
        if level <= 0:
            return True_()

        if self.options.skill_progression == SkillProgression.option_progressive:
            skills_items = ["Farming Level", "Mining Level", "Foraging Level",
                            "Fishing Level", "Combat Level"]
            if allow_modded_skills:
                skills.append_mod_skill_level(skills_items, self.options)
            return self.received(skills_items, count=level)

        months_with_4_skills = max(1, (level // 4) - 1)
        months_with_5_skills = max(1, (level // 5) - 1)
        rule_with_fishing = self.has_lived_months(months_with_5_skills) & self.can_get_fishing_xp()
        if level > 40:
            return rule_with_fishing
        return self.has_lived_months(months_with_4_skills) | rule_with_fishing

    def has_building(self, building: str) -> StardewRule:
        carpenter_rule = self.can_reach_region(Region.carpenter)
        if not self.options.building_progression == BuildingProgression.option_vanilla:
            count = 1
            if building in [Building.coop, Building.barn, Building.shed]:
                building = f"Progressive {building}"
            elif building.startswith("Big"):
                count = 2
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            elif building.startswith("Deluxe"):
                count = 3
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            return self.received(f"{building}", count) & carpenter_rule

        return Has(building, self.building_rules) & carpenter_rule

    def has_house(self, upgrade_level: int) -> StardewRule:
        if upgrade_level < 1:
            return True_()

        if upgrade_level > 3:
            return False_()

        if not self.options.building_progression == BuildingProgression.option_vanilla:
            return self.received(f"Progressive House", upgrade_level) & self.can_reach_region(Region.carpenter)

        if upgrade_level == 1:
            return Has(Building.kitchen, self.building_rules)

        if upgrade_level == 2:
            return Has(Building.kids_room, self.building_rules)

        # if upgrade_level == 3:
        return Has(Building.cellar, self.building_rules)

    def can_complete_quest(self, quest: str) -> StardewRule:
        return Has(quest, self.quest_rules)

    def can_complete_special_order(self, specialorder: str) -> StardewRule:
        return Has(specialorder, self.special_order_rules)

    def can_get_farming_xp(self) -> StardewRule:
        crop_rules = []
        for crop in all_crops:
            crop_rules.append(self.can_grow_crop(crop))
        return Or(crop_rules)

    def can_get_foraging_xp(self) -> StardewRule:
        tool_rule = self.has_tool(Tool.axe)
        tree_rule = self.can_reach_region(Region.forest) & self.has_any_season_not_winter()
        stump_rule = self.can_reach_region(Region.secret_woods) & self.has_tool(Tool.axe, ToolMaterial.copper)
        return tool_rule & (tree_rule | stump_rule)

    def can_get_mining_xp(self) -> StardewRule:
        tool_rule = self.has_tool(Tool.pickaxe)
        stone_rule = self.can_reach_any_region([Region.mines_floor_5, Region.quarry, Region.skull_cavern_25, Region.volcano_floor_5])
        return tool_rule & stone_rule

    def can_get_combat_xp(self) -> StardewRule:
        tool_rule = self.has_any_weapon()
        enemy_rule = self.can_reach_any_region([Region.mines_floor_5, Region.skull_cavern_25, Region.volcano_floor_5])
        return tool_rule & enemy_rule

    def can_get_fishing_xp(self) -> StardewRule:
        if self.options.skill_progression == SkillProgression.option_progressive:
            return self.can_fish() | self.can_crab_pot()

        return self.can_fish()

    def can_fish(self, difficulty: int = 0) -> StardewRule:
        skill_required = max(0, int((difficulty / 10) - 1))
        if difficulty <= 40:
            skill_required = 0
        skill_rule = self.has_skill_level(Skill.fishing, skill_required)
        region_rule = self.can_reach_any_region(fishing_regions)
        number_fishing_rod_required = 1 if difficulty < 50 else 2
        if self.options.tool_progression == ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod", number_fishing_rod_required) & skill_rule & region_rule

        return skill_rule & region_rule

    def can_fish_in_freshwater(self) -> StardewRule:
        return self.can_fish() & self.can_reach_any_region([Region.forest, Region.town, Region.mountain])

    def has_max_fishing(self) -> StardewRule:
        skill_rule = self.has_skill_level(Skill.fishing, 10)
        return self.has_max_fishing_rod() & skill_rule

    def can_fish_chests(self) -> StardewRule:
        skill_rule = self.has_skill_level(Skill.fishing, 4)
        return self.has_max_fishing_rod() & skill_rule

    def can_buy_seed(self, seed: SeedItem) -> StardewRule:
        if self.options.cropsanity == Cropsanity.option_disabled:
            item_rule = True_()
        else:
            item_rule = self.received(seed.name)
        season_rule = self.has_any_season(seed.seasons)
        region_rule = self.can_reach_all_regions(seed.regions)
        currency_rule = self.can_spend_money(1000)
        if seed.name == Seed.pineapple:
            currency_rule = self.has(Forageable.magma_cap)
        if seed.name == Seed.taro:
            currency_rule = self.has(Fossil.bone_fragment)
        return season_rule & region_rule & item_rule & currency_rule

    def can_buy_sapling(self, fruit: str) -> StardewRule:
        sapling_prices = {Fruit.apple: 4000, Fruit.apricot: 2000, Fruit.cherry: 3400, Fruit.orange: 4000,
                          Fruit.peach: 6000,
                          Fruit.pomegranate: 6000, Fruit.banana: 0, Fruit.mango: 0}
        received_sapling = self.received(f"{fruit} Sapling")
        if self.options.cropsanity == Cropsanity.option_disabled:
            allowed_buy_sapling = True_()
        else:
            allowed_buy_sapling = received_sapling
        can_buy_sapling = self.can_spend_money_at(Region.pierre_store, sapling_prices[fruit])
        if fruit == Fruit.banana:
            can_buy_sapling = self.has_island_trader() & self.has(Forageable.dragon_tooth)
        elif fruit == Fruit.mango:
            can_buy_sapling = self.has_island_trader() & self.has(Fish.mussel_node)

        return allowed_buy_sapling & can_buy_sapling

    def can_grow_crop(self, crop: CropItem) -> StardewRule:
        season_rule = self.has_any_season(crop.farm_growth_seasons)
        seed_rule = self.has(crop.seed.name)
        farm_rule = self.can_reach_region(Region.farm) & season_rule
        tool_rule = self.has_tool(Tool.hoe) & self.has_tool(Tool.watering_can)
        region_rule = farm_rule | self.can_reach_region(Region.greenhouse) | self.can_reach_region(Region.island_west)
        return seed_rule & region_rule & tool_rule

    def can_plant_and_grow_item(self, seasons: Union[str, Iterable[str]]) -> StardewRule:
        if isinstance(seasons, str):
            seasons = [seasons]
        season_rule = self.has_any_season(seasons) | self.can_reach_region(Region.greenhouse) | self.has_island_farm()
        farm_rule = self.can_reach_region(Region.farm) | self.can_reach_region(
            Region.greenhouse) | self.has_island_farm()
        return season_rule & farm_rule

    def has_island_farm(self) -> StardewRule:
        return self.can_reach_region(Region.island_south)

    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        region_rule = self.can_reach_any_region(fish.locations)
        season_rule = self.has_any_season(fish.seasons)
        if fish.difficulty == -1:
            difficulty_rule = self.can_crab_pot()
        else:
            difficulty_rule = self.can_fish(fish.difficulty)
        return region_rule & season_rule & difficulty_rule

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.has_skill_level(Skill.fishing, 10), self.has_max_fishing_rod()]
        for fish in all_fish:
            if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true and \
                    fish in island_fish:
                continue
            rules.append(self.can_catch_fish(fish))
        return And(rules)

    def has_max_fishing_rod(self) -> StardewRule:
        if self.options.tool_progression == ToolProgression.option_progressive:
            return self.received(APTool.fishing_rod, 4)
        return self.can_get_fishing_xp()

    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.has_house(1) | self.has_skill_level(Skill.foraging, 9)
        if recipe is None:
            return cook_rule

        learn_rule = self.can_learn_recipe(recipe.source)
        ingredients_rule = And([self.has(ingredient) for ingredient in recipe.ingredients])
        number_ingredients = sum(recipe.ingredients[ingredient] for ingredient in recipe.ingredients)
        time_rule = self.has_lived_months(number_ingredients)
        return cook_rule & learn_rule & ingredients_rule & time_rule

    def can_learn_recipe(self, source: RecipeSource) -> StardewRule:
        if isinstance(source, StarterSource):
            return True_()
        if isinstance(source, ShopSource):
            return self.can_spend_money_at(source.region, source.price)
        if isinstance(source, SkillSource):
            return self.has_skill_level(source.skill, source.level)
        if isinstance(source, FriendshipSource):
            return self.has_relationship(source.friend, source.hearts)
        if isinstance(source, QueenOfSauceSource):
            year_rule = self.has_year_two() if source.year == 2 else self.has_year_three()
            return self.can_watch(Channel.queen_of_sauce) & self.has_season(source.season) & year_rule

        return False_()

    def can_watch(self, channel: str = None):
        tv_rule = True_()
        if channel is None:
            return tv_rule
        return self.received(channel) & tv_rule

    def can_smelt(self, item: str) -> StardewRule:
        return self.has(Machine.furnace) & self.has(item)

    def can_do_panning(self, item: str = Generic.any) -> StardewRule:
        return self.received("Glittering Boulder Removed")

    def can_crab_pot(self, region: str = Generic.any) -> StardewRule:
        crab_pot_rule = self.has(Craftable.bait)
        if self.options.skill_progression == SkillProgression.option_progressive:
            crab_pot_rule = crab_pot_rule & self.has(Machine.crab_pot)
        else:
            crab_pot_rule = crab_pot_rule & self.can_get_fishing_xp()

        if region != Generic.any:
            return crab_pot_rule & self.can_reach_region(region)

        water_region_rules = self.can_reach_any_region(fishing_regions)
        return crab_pot_rule & water_region_rules

    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.can_reach_region(Region.mines_floor_5)

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.can_reach_region(Region.mines_floor_45)

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.can_reach_region(Region.mines_floor_85)

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(120) &
                self.can_reach_region(Region.skull_cavern))

    def can_mine_perfectly(self) -> StardewRule:
        return self.can_progress_in_the_mines_from_floor(160)

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_mine_perfectly() &
                self.can_reach_region(Region.skull_cavern))

    def can_farm_perfectly(self) -> StardewRule:
        tool_rule = self.has_tool(Tool.hoe, ToolMaterial.iridium) & self.can_water(4)
        return tool_rule & self.has_farming_level(10)

    def can_fish_perfectly(self) -> StardewRule:
        skill_rule = self.has_skill_level(Skill.fishing, 10)
        return skill_rule & self.has_max_fishing_rod()

    def can_chop_trees(self) -> StardewRule:
        return self.has_tool(Tool.axe) & self.can_reach_region(Region.forest)

    def can_chop_perfectly(self) -> StardewRule:
        magic_rule = (magic.can_use_clear_debris_instead_of_tool_level(self, 3)) & self.has_skill_level(ModSkill.magic, 10)
        tool_rule = self.has_tool(Tool.axe, ToolMaterial.iridium)
        foraging_rule = self.has_skill_level(Skill.foraging, 10)
        region_rule = self.can_reach_region(Region.forest)
        return region_rule & ((tool_rule & foraging_rule) | magic_rule)

    def has_max_buffs(self) -> StardewRule:
        return self.received(Buff.movement, self.options.movement_buff_number.value) & self.received(Buff.luck, self.options.luck_buff_number.value)

    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.can_do_combat_at_level(Performance.galaxy)
        if tier >= 3:
            return self.can_do_combat_at_level(Performance.great)
        if tier >= 2:
            return self.can_do_combat_at_level(Performance.good)
        if tier >= 1:
            return self.can_do_combat_at_level(Performance.decent)
        return self.can_do_combat_at_level(Performance.basic)

    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40)
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options.tool_progression == ToolProgression.option_progressive:
            rules.append(self.has_tool(Tool.pickaxe, ToolMaterial.tiers[tier]))
        if self.options.skill_progression == SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level(Skill.combat, combat_tier))
        return And(rules)

    def can_progress_easily_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40) + 1
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options.tool_progression == ToolProgression.option_progressive:
            rules.append(self.has_tool(Tool.pickaxe, ToolMaterial.tiers[tier]))
        if self.options.skill_progression == SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level(Skill.combat, combat_tier))
        return And(rules)

    def has_mine_elevator_to_floor(self, floor: int) -> StardewRule:
        if self.options.elevator_progression != ElevatorProgression.option_vanilla:
            return self.received("Progressive Mine Elevator", count=int(floor / 5))
        return True_()

    def can_mine_to_floor(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 5, 0)
        previous_previous_elevator = max(floor - 10, 0)
        return ((self.has_mine_elevator_to_floor(previous_elevator) &
                 self.can_progress_in_the_mines_from_floor(previous_elevator)) |
                (self.has_mine_elevator_to_floor(previous_previous_elevator) &
                 self.can_progress_easily_in_the_mines_from_floor(previous_previous_elevator)))

    def can_progress_in_the_skull_cavern_from_floor(self, floor: int) -> StardewRule:
        tier = floor // 50
        rules = []
        weapon_rule = self.has_great_weapon()
        rules.append(weapon_rule)
        rules.append(self.can_cook())
        if self.options.tool_progression == ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", min(4, max(0, tier + 2))))
        if self.options.skill_progression == SkillProgression.option_progressive:
            skill_tier = min(10, max(0, tier * 2 + 6))
            rules.extend({self.has_skill_level(Skill.combat, skill_tier),
                          self.has_skill_level(Skill.mining, skill_tier)})
        return And(rules)

    def can_progress_easily_in_the_skull_cavern_from_floor(self, floor: int) -> StardewRule:
        return self.can_progress_in_the_skull_cavern_from_floor(floor + 50)

    def can_mine_to_skull_cavern_floor(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 25, 0)
        previous_previous_elevator = max(floor - 50, 0)
        has_mine_elevator = self.has_mine_elevator_to_floor(5) # Skull Cavern Elevator menu needs a normal elevator...
        return ((has_skull_cavern_elevator_to_floor(self, previous_elevator) &
                 self.can_progress_in_the_skull_cavern_from_floor(previous_elevator)) |
                (has_skull_cavern_elevator_to_floor(self, previous_previous_elevator) &
                 self.can_progress_easily_in_the_skull_cavern_from_floor(previous_previous_elevator))) & has_mine_elevator

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        if self.options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
            return True_()
        jotpk_buffs = ["JotPK: Progressive Boots", "JotPK: Progressive Gun",
                       "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate"]
        return self.received(jotpk_buffs, power_level)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        if self.options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
            return True_()
        return self.received("Junimo Kart: Extra Life", power_level)

    def has_junimo_kart_max_level(self) -> StardewRule:
        play_rule = self.can_reach_region(Region.junimo_kart_3)
        if self.options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
            return play_rule
        return self.has_junimo_kart_power_level(8)

    def has_traveling_merchant(self, tier: int = 1):
        traveling_merchant_days = [f"Traveling Merchant: {day}" for day in Weekday.all_days]
        return self.received(traveling_merchant_days, tier)

    def can_get_married(self) -> StardewRule:
        return self.has_relationship(Generic.bachelor, 10) & self.has(Gift.mermaid_pendant)

    def has_children(self, number_children: int) -> StardewRule:
        if number_children <= 0:
            return True_()
        possible_kids = ["Cute Baby", "Ugly Baby"]
        return self.received(possible_kids, number_children) & self.has_house(2)

    def can_reproduce(self, number_children: int = 1) -> StardewRule:
        if number_children <= 0:
            return True_()
        return self.can_get_married() & self.has_house(2) & self.has_relationship(Generic.bachelor, 12) & self.has_children(number_children - 1)

    def has_relationship(self, npc: str, hearts: int = 1) -> StardewRule:
        if hearts <= 0:
            return True_()
        friendsanity = self.options.friendsanity
        if friendsanity == Friendsanity.option_none:
            return self.can_earn_relationship(npc, hearts)
        if npc not in all_villagers_by_name:
            if npc == NPC.pet:
                if friendsanity == Friendsanity.option_bachelors:
                    return self.can_befriend_pet(hearts)
                return self.received_hearts(NPC.pet, hearts)
            if npc == Generic.any or npc == Generic.bachelor:
                possible_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    if npc == Generic.any or all_villagers_by_name[name].bachelor:
                        possible_friends.append(self.has_relationship(name, hearts))
                return Or(possible_friends)
            if npc == Generic.all:
                mandatory_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    mandatory_friends.append(self.has_relationship(name, hearts))
                return And(mandatory_friends)
            if npc.isnumeric():
                possible_friends = []
                for name in all_villagers_by_name:
                    if not self.npc_is_in_current_slot(name):
                        continue
                    possible_friends.append(self.has_relationship(name, hearts))
                return Count(int(npc), possible_friends)
            return self.can_earn_relationship(npc, hearts)

        if not self.npc_is_in_current_slot(npc):
            return True_()
        villager = all_villagers_by_name[npc]
        if friendsanity == Friendsanity.option_bachelors and not villager.bachelor:
            return self.can_earn_relationship(npc, hearts)
        if friendsanity == Friendsanity.option_starting_npcs and not villager.available:
            return self.can_earn_relationship(npc, hearts)
        is_capped_at_8 = villager.bachelor and friendsanity != Friendsanity.option_all_with_marriage
        if is_capped_at_8 and hearts > 8:
            return self.received_hearts(villager, 8) & self.can_earn_relationship(npc, hearts)
        return self.received_hearts(villager, hearts)

    def received_hearts(self, npc: Union[str, Villager], hearts: int) -> StardewRule:
        if isinstance(npc, Villager):
            return self.received_hearts(npc.name, hearts)
        heart_size = self.options.friendsanity_heart_size.value
        return self.received(self.heart(npc), math.ceil(hearts / heart_size))

    def can_meet(self, npc: str) -> StardewRule:
        if npc not in all_villagers_by_name or not self.npc_is_in_current_slot(npc):
            return True_()
        villager = all_villagers_by_name[npc]
        rules = [self.can_reach_any_region(villager.locations)]
        if npc == NPC.kent:
            rules.append(self.has_year_two())
        elif npc == NPC.leo:
            rules.append(self.received("Island West Turtle"))

        return And(rules)

    def can_give_loved_gifts_to_everyone(self) -> StardewRule:
        rules = []
        for npc in all_villagers_by_name:
            if not self.npc_is_in_current_slot(npc):
                continue
            villager = all_villagers_by_name[npc]
            gift_rule = self.has_any_universal_love()
            meet_rule = self.can_meet(npc)
            rules.append(meet_rule & gift_rule)
        loved_gifts_rules = And(rules)
        simplified_rules = loved_gifts_rules.simplify()
        return simplified_rules

    def can_earn_relationship(self, npc: str, hearts: int = 0) -> StardewRule:
        if hearts <= 0:
            return True_()

        heart_size = self.options.friendsanity_heart_size.value
        previous_heart = hearts - heart_size
        previous_heart_rule = self.has_relationship(npc, previous_heart)

        if npc == NPC.pet:
            earn_rule = self.can_befriend_pet(hearts)
        elif npc == NPC.wizard and ModNames.magic in self.options.mods:
            earn_rule = self.can_meet(npc) & self.has_lived_months(hearts)
        elif npc in all_villagers_by_name:
            if not self.npc_is_in_current_slot(npc):
                return previous_heart_rule
            villager = all_villagers_by_name[npc]
            rule_if_birthday = self.has_season(villager.birthday) & self.has_any_universal_love() & self.has_lived_months(hearts // 2)
            rule_if_not_birthday = self.has_lived_months(hearts)
            earn_rule = self.can_meet(npc) & (rule_if_birthday | rule_if_not_birthday)
            if villager.bachelor:
                if hearts > 8:
                    earn_rule = earn_rule & self.can_date(npc)
                if hearts > 10:
                    earn_rule = earn_rule & self.can_marry(npc)
        else:
            earn_rule = self.has_lived_months(min(hearts // 2, 8))

        return previous_heart_rule & earn_rule

    def can_date(self, npc: str) -> StardewRule:
        return self.has_relationship(npc, 8) & self.has(Gift.bouquet)

    def can_marry(self, npc: str) -> StardewRule:
        return self.has_relationship(npc, 10) & self.has(Gift.mermaid_pendant)

    def can_befriend_pet(self, hearts: int):
        if hearts <= 0:
            return True_()
        points = hearts * 200
        points_per_month = 12 * 14
        points_per_water_month = 18 * 14
        return self.can_reach_region(Region.farm) & \
               ((self.can_water(0) & self.has_lived_months(points // points_per_water_month)) |
                self.has_lived_months(points // points_per_month))

    def can_complete_bundle(self, bundle_requirements: List[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        highest_quality_yet = 0
        can_speak_junimo = self.can_reach_region(Region.wizard_tower)
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return can_speak_junimo & self.can_spend_money(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
                if bundle_item.quality > highest_quality_yet:
                    highest_quality_yet = bundle_item.quality
        return can_speak_junimo & self.has(item_rules, number_required) & self.can_grow_gold_quality(highest_quality_yet)

    def can_grow_gold_quality(self, quality: int) -> StardewRule:
        if quality <= 0:
            return True_()
        if quality == 1:
            return self.has_farming_level(5) | (self.has_fertilizer(1) & self.has_farming_level(2)) | (
                    self.has_fertilizer(2) & self.has_farming_level(1)) | self.has_fertilizer(3)
        if quality == 2:
            return self.has_farming_level(10) | (self.has_fertilizer(1) & self.has_farming_level(5)) | (
                    self.has_fertilizer(2) & self.has_farming_level(3)) | (
                           self.has_fertilizer(3) & self.has_farming_level(2))
        if quality >= 3:
            return self.has_fertilizer(3) & self.has_farming_level(4)

    def has_fertilizer(self, tier: int) -> StardewRule:
        if tier <= 0:
            return True_()
        if tier == 1:
            return self.has(Fertilizer.basic)
        if tier == 2:
            return self.has(Fertilizer.quality)
        if tier >= 3:
            return self.has(Fertilizer.deluxe)

    def can_complete_field_office(self) -> StardewRule:
        field_office = self.can_reach_region(Region.field_office)
        professor_snail = self.received("Open Professor Snail Cave")
        dig_site = self.can_reach_region(Region.dig_site)
        tools = self.has_tool(Tool.pickaxe) & self.has_tool(Tool.hoe) & self.has_tool(Tool.scythe)
        leg_and_snake_skull = dig_site
        ribs_and_spine = self.can_reach_region(Region.island_south)
        skull = self.can_open_geode(Geode.golden_coconut)
        tail = self.can_do_panning() & dig_site
        frog = self.can_reach_region(Region.island_east)
        bat = self.can_reach_region(Region.volcano_floor_5)
        snake_vertebrae = self.can_reach_region(Region.island_west)
        return field_office & professor_snail & tools & leg_and_snake_skull & ribs_and_spine & skull & tail & frog & bat & snake_vertebrae

    def can_complete_community_center(self) -> StardewRule:
        return (self.can_reach_location("Complete Crafts Room") &
                self.can_reach_location("Complete Pantry") &
                self.can_reach_location("Complete Fish Tank") &
                self.can_reach_location("Complete Bulletin Board") &
                self.can_reach_location("Complete Vault") &
                self.can_reach_location("Complete Boiler Room"))

    def can_finish_grandpa_evaluation(self) -> StardewRule:
        # https://stardewvalleywiki.com/Grandpa
        rules_worth_a_point = [self.can_have_earned_total_money(50000),  # 50 000g
                               self.can_have_earned_total_money(100000),  # 100 000g
                               self.can_have_earned_total_money(200000),  # 200 000g
                               self.can_have_earned_total_money(300000),  # 300 000g
                               self.can_have_earned_total_money(500000),  # 500 000g
                               self.can_have_earned_total_money(1000000),  # 1 000 000g first point
                               self.can_have_earned_total_money(1000000),  # 1 000 000g second point
                               self.has_total_skill_level(30),  # Total Skills: 30
                               self.has_total_skill_level(50),  # Total Skills: 50
                               self.can_complete_museum(),  # Completing the museum for a point
                               # Catching every fish not expected
                               # Shipping every item not expected
                               self.can_get_married() & self.has_house(2),
                               self.has_relationship("5", 8),  # 5 Friends
                               self.has_relationship("10", 8),  # 10 friends
                               self.has_relationship(NPC.pet, 5),  # Max Pet
                               self.can_complete_community_center(),  # Community Center Completion
                               self.can_complete_community_center(),  # CC Ceremony first point
                               self.can_complete_community_center(),  # CC Ceremony second point
                               self.received(Wallet.skull_key),  # Skull Key obtained
                               self.has_rusty_key(),  # Rusty key obtained
                               ]
        return Count(12, rules_worth_a_point)

    def has_island_transport(self) -> StardewRule:
        return self.received(Transportation.island_obelisk) | self.received(Transportation.boat_repair)

    def has_any_weapon(self) -> StardewRule:
        return self.has_decent_weapon() | self.received(item.name for item in all_items if Group.WEAPON in item.groups)

    def has_decent_weapon(self) -> StardewRule:
        return (self.has_good_weapon() |
                self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and
                              (Group.MINES_FLOOR_50 in item.groups or Group.MINES_FLOOR_60 in item.groups)))

    def has_good_weapon(self) -> StardewRule:
        return ((self.has_great_weapon() |
                 self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and
                               (Group.MINES_FLOOR_80 in item.groups or Group.MINES_FLOOR_90 in item.groups))) &
                self.received("Adventurer's Guild"))

    def has_great_weapon(self) -> StardewRule:
        return ((self.has_galaxy_weapon() |
                 self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and Group.MINES_FLOOR_110 in item.groups)) &
                self.received("Adventurer's Guild"))

    def has_galaxy_weapon(self) -> StardewRule:
        return (self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and Group.GALAXY_WEAPONS in item.groups) &
                self.received("Adventurer's Guild"))

    def has_year_two(self) -> StardewRule:
        return self.has_lived_months(4)

    def has_year_three(self) -> StardewRule:
        return self.has_lived_months(8)

    def can_speak_dwarf(self) -> StardewRule:
        if self.options.museumsanity == Museumsanity.option_none:
            return And([self.can_donate_museum_item(item) for item in dwarf_scrolls])
        return self.received("Dwarvish Translation Guide")

    def can_donate_museum_item(self, item: MuseumItem) -> StardewRule:
        return self.can_reach_region(Region.museum) & self.can_find_museum_item(item)

    def can_donate_museum_items(self, number: int) -> StardewRule:
        return self.can_reach_region(Region.museum) & self.can_find_museum_items(number)

    def can_donate_museum_artifacts(self, number: int) -> StardewRule:
        return self.can_reach_region(Region.museum) & self.can_find_museum_artifacts(number)

    def can_donate_museum_minerals(self, number: int) -> StardewRule:
        return self.can_reach_region(Region.museum) & self.can_find_museum_minerals(number)

    def can_find_museum_item(self, item: MuseumItem) -> StardewRule:
        region_rule = self.can_reach_all_regions_except_one(item.locations)
        geodes_rule = And([self.can_open_geode(geode) for geode in item.geodes])
        # monster_rule = self.can_farm_monster(item.monsters)
        # extra_rule = True_()
        pan_rule = False_()
        if item.name == "Earth Crystal" or item.name == "Fire Quartz" or item.name == "Frozen Tear":
            pan_rule = self.can_do_panning()
        return pan_rule | (region_rule & geodes_rule)  # & monster_rule & extra_rule

    def can_find_museum_artifacts(self, number: int) -> StardewRule:
        rules = []
        for artifact in all_museum_artifacts:
            rules.append(self.can_find_museum_item(artifact))

        return Count(number, rules)

    def can_find_museum_minerals(self, number: int) -> StardewRule:
        rules = []
        for mineral in all_museum_minerals:
            rules.append(self.can_find_museum_item(mineral))

        return Count(number, rules)

    def can_find_museum_items(self, number: int) -> StardewRule:
        rules = []
        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))

        return Count(number, rules)

    def can_complete_museum(self) -> StardewRule:
        rules = [self.can_reach_region(Region.museum), self.can_mine_perfectly()]

        if self.options.museumsanity != Museumsanity.option_none:
            rules.append(self.received("Traveling Merchant Metal Detector", 4))

        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))
        return And(rules)

    def has_season(self, season: str) -> StardewRule:
        if season == Generic.any:
            return True_()
        seasons_order = [Season.spring, Season.summer, Season.fall, Season.winter]
        if self.options.season_randomization == SeasonRandomization.option_progressive:
            return self.received(Season.progressive, seasons_order.index(season))
        if self.options.season_randomization == SeasonRandomization.option_disabled:
            if season == Season.spring:
                return True_()
            return self.has_lived_months(1)
        return self.received(season)

    def has_any_season(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return Or([self.has_season(season) for season in seasons])

    def has_any_season_not_winter(self):
        return self.has_any_season([Season.spring, Season.summer, Season.fall])

    def has_all_seasons(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return And([self.has_season(season) for season in seasons])

    def has_lived_months(self, number: int) -> StardewRule:
        number = max(0, min(number, MAX_MONTHS))
        return self.received("Month End", number)

    def has_rusty_key(self) -> StardewRule:
        if self.options.museumsanity == Museumsanity.option_none:
            required_donations = 80  # It's 60, but without a metal detector I'd rather overshoot so players don't get screwed by RNG
            return self.has([item.name for item in all_museum_items], required_donations) & self.can_reach_region(Region.museum)
        return self.received(Wallet.rusty_key)

    def can_win_egg_hunt(self) -> StardewRule:
        number_of_movement_buffs = self.options.movement_buff_number.value
        if self.options.festival_locations == FestivalLocations.option_hard or number_of_movement_buffs < 2:
            return True_()
        return self.received(Buff.movement, number_of_movement_buffs // 2)

    def can_succeed_luau_soup(self) -> StardewRule:
        if self.options.festival_locations != FestivalLocations.option_hard:
            return True_()
        eligible_fish = [Fish.blobfish, Fish.crimsonfish, "Ice Pip", Fish.lava_eel, Fish.legend, Fish.angler, Fish.catfish, Fish.glacierfish,
                         Fish.mutant_carp, Fish.spookfish, Fish.stingray, Fish.sturgeon, "Super Cucumber"]
        fish_rule = [self.has(fish) for fish in eligible_fish]
        eligible_kegables = [Fruit.ancient_fruit, Fruit.apple, Fruit.banana, Forageable.coconut, Forageable.crystal_fruit, Fruit.mango,
                             Fruit.melon, Fruit.orange, Fruit.peach, Fruit.pineapple, Fruit.pomegranate, Fruit.rhubarb,
                             Fruit.starfruit, Fruit.strawberry, Forageable.cactus_fruit,
                             Fruit.cherry, Fruit.cranberries, Fruit.grape, Forageable.spice_berry, Forageable.wild_plum, Vegetable.hops, Vegetable.wheat]
        keg_rules = [self.can_keg(kegable) for kegable in eligible_kegables]
        aged_rule = [self.can_age(rule, "Iridium") for rule in keg_rules]
        # There are a few other valid items but I don't feel like coding them all
        return Or(fish_rule) | Or(aged_rule)

    def can_succeed_grange_display(self) -> StardewRule:
        if self.options.festival_locations != FestivalLocations.option_hard:
            return True_()
        animal_rule = self.has_animal(Generic.any)
        artisan_rule = self.can_keg(Generic.any) | self.can_preserves_jar(Generic.any)
        cooking_rule = True_()  # Salads at the bar are good enough
        fish_rule = self.can_fish(50)
        forage_rule = True_()  # Hazelnut always available since the grange display is in fall
        mineral_rule = self.can_open_geode(Generic.any)  # More than half the minerals are good enough
        good_fruits = [Fruit.apple, Fruit.banana, Forageable.coconut, Forageable.crystal_fruit, Fruit.mango, Fruit.orange, Fruit.peach,
                       Fruit.pomegranate,
                       Fruit.strawberry, Fruit.melon, Fruit.rhubarb, Fruit.pineapple, Fruit.ancient_fruit, Fruit.starfruit, ]
        fruit_rule = Or([self.has(fruit) for fruit in good_fruits])
        good_vegetables = [Vegetable.amaranth, Vegetable.artichoke, Vegetable.beet, Vegetable.cauliflower, Forageable.fiddlehead_fern, Vegetable.kale,
                           Vegetable.radish, Vegetable.taro_root, Vegetable.yam, Vegetable.red_cabbage, Vegetable.pumpkin]
        vegetable_rule = Or([self.has(vegetable) for vegetable in good_vegetables])

        return animal_rule & artisan_rule & cooking_rule & fish_rule & \
               forage_rule & fruit_rule & mineral_rule & vegetable_rule

    def can_win_fishing_competition(self) -> StardewRule:
        return self.can_fish(60)

    def has_any_universal_love(self) -> StardewRule:
        return self.has(Gift.golden_pumpkin) | self.has("Magic Rock Candy") | self.has(Gift.pearl) | self.has(
            "Prismatic Shard") | self.has(AnimalProduct.rabbit_foot)

    def has_jelly(self) -> StardewRule:
        return self.can_preserves_jar(Fruit.any)

    def has_pickle(self) -> StardewRule:
        return self.can_preserves_jar(Vegetable.any)

    def can_preserves_jar(self, item: str) -> StardewRule:
        machine_rule = self.has(Machine.preserves_jar)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.has(all_fruits, 1)
        if item == Vegetable.any:
            return machine_rule & self.has(all_vegetables, 1)
        return machine_rule & self.has(item)

    def has_wine(self) -> StardewRule:
        return self.can_keg(Fruit.any)

    def has_juice(self) -> StardewRule:
        return self.can_keg(Vegetable.any)

    def can_keg(self, item: str) -> StardewRule:
        machine_rule = self.has(Machine.keg)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.has(all_fruits, 1)
        if item == Vegetable.any:
            return machine_rule & self.has(all_vegetables, 1)
        return machine_rule & self.has(item)

    def can_age(self, item: Union[str, StardewRule], quality: str) -> StardewRule:
        months = 1
        if quality == "Gold":
            months = 2
        elif quality == "Iridium":
            months = 3
        if isinstance(item, str):
            rule = self.has(item)
        else:
            rule: StardewRule = item
        return self.has(Machine.cask) & self.has_lived_months(months) & rule

    def can_buy_animal(self, animal: str) -> StardewRule:
        price = 0
        building = ""
        if animal == Animal.chicken:
            price = 800
            building = Building.coop
        elif animal == Animal.cow:
            price = 1500
            building = Building.barn
        elif animal == Animal.goat:
            price = 4000
            building = Building.big_barn
        elif animal == Animal.duck:
            price = 1200
            building = Building.big_coop
        elif animal == Animal.sheep:
            price = 8000
            building = Building.deluxe_barn
        elif animal == Animal.rabbit:
            price = 8000
            building = Building.deluxe_coop
        elif animal == Animal.pig:
            price = 16000
            building = Building.deluxe_barn
        else:
            return True_()
        return self.can_spend_money_at(Region.ranch, price) & self.has_building(building)

    def has_animal(self, animal: str) -> StardewRule:
        if animal == Generic.any:
            return self.has_any_animal()
        elif animal == Building.coop:
            return self.has_any_coop_animal()
        elif animal == Building.barn:
            return self.has_any_barn_animal()
        return self.has(animal)

    def has_happy_animal(self, animal: str) -> StardewRule:
        return self.has_animal(animal) & self.has(Forageable.hay)

    def has_any_animal(self) -> StardewRule:
        return self.has_any_coop_animal() | self.has_any_barn_animal()

    def has_any_coop_animal(self) -> StardewRule:
        coop_rule = Or([self.has_animal(coop_animal) for coop_animal in coop_animals])
        return coop_rule

    def has_any_barn_animal(self) -> StardewRule:
        barn_rule = Or([self.has_animal(barn_animal) for barn_animal in barn_animals])
        return barn_rule

    def can_open_geode(self, geode: str) -> StardewRule:
        blacksmith_access = self.can_reach_region("Clint's Blacksmith")
        geodes = [Geode.geode, Geode.frozen, Geode.magma, Geode.omni]
        if geode == Generic.any:
            return blacksmith_access & Or([self.has(geode_type) for geode_type in geodes])
        return blacksmith_access & self.has(geode)

    def has_island_trader(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        return self.can_reach_region(Region.island_trader)

    def has_walnut(self, number: int) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if number <= 0:
            return True_()
        # https://stardewcommunitywiki.com/Golden_Walnut#Walnut_Locations
        reach_south = self.can_reach_region(Region.island_south)
        reach_north = self.can_reach_region(Region.island_north)
        reach_west = self.can_reach_region(Region.island_west)
        reach_hut = self.can_reach_region(Region.leo_hut)
        reach_southeast = self.can_reach_region(Region.island_south_east)
        reach_pirate_cove = self.can_reach_region(Region.pirate_cove)
        reach_outside_areas = And(reach_south, reach_north, reach_west, reach_hut)
        reach_volcano_regions = [self.can_reach_region(Region.volcano),
                                 self.can_reach_region(Region.volcano_secret_beach),
                                 self.can_reach_region(Region.volcano_floor_5),
                                 self.can_reach_region(Region.volcano_floor_10)]
        reach_volcano = Or(reach_volcano_regions)
        reach_all_volcano = And(reach_volcano_regions)
        reach_walnut_regions = [reach_south, reach_north, reach_west, reach_volcano]
        reach_caves = And(self.can_reach_region(Region.qi_walnut_room), self.can_reach_region(Region.dig_site),
                          self.can_reach_region(Region.gourmand_frog_cave),
                          self.can_reach_region(Region.colored_crystals_cave),
                          self.can_reach_region(Region.shipwreck), self.has(Weapon.any_slingshot))
        reach_entire_island = And(reach_outside_areas, reach_all_volcano,
                                  reach_caves, reach_southeast, reach_pirate_cove)
        if number <= 5:
            return Or(reach_south, reach_north, reach_west, reach_volcano)
        if number <= 10:
            return Count(2, reach_walnut_regions)
        if number <= 15:
            return Count(3, reach_walnut_regions)
        if number <= 20:
            return And(reach_walnut_regions)
        if number <= 50:
            return reach_entire_island
        gems = [Mineral.amethyst, Mineral.aquamarine, Mineral.emerald, Mineral.ruby, Mineral.topaz]
        return reach_entire_island & self.has(Fruit.banana) & self.has(gems) & self.can_mine_perfectly() & \
               self.can_fish_perfectly() & self.has(Craftable.flute_block) & self.has(Seed.melon) & self.has(Seed.wheat) & self.has(Seed.garlic)

    def has_everything(self, all_progression_items: Set[str]) -> StardewRule:
        all_regions = [region.name for region in vanilla_regions]
        rules = self.received(all_progression_items, len(all_progression_items)) & \
                self.can_reach_all_regions(all_regions)
        return rules

    def heart(self, npc: Union[str, Villager]) -> str:
        if isinstance(npc, str):
            return f"{npc} <3"
        return self.heart(npc.name)

    def can_forage(self, season: str, region: str = Region.forest, need_hoe: bool = False) -> StardewRule:
        season_rule = self.has_season(season)
        region_rule = self.can_reach_region(region)
        if need_hoe:
            return season_rule & region_rule & self.has_tool(Tool.hoe)
        return season_rule & region_rule

    def npc_is_in_current_slot(self, name: str) -> bool:
        npc = all_villagers_by_name[name]
        mod = npc.mod_name
        return mod is None or mod in self.options.mods

    def can_do_combat_at_level(self, level: str) -> StardewRule:
        if level == Performance.basic:
            return self.has_any_weapon() | magic.has_any_spell(self)
        if level == Performance.decent:
            return self.has_decent_weapon() | magic.has_decent_spells(self)
        if level == Performance.good:
            return self.has_good_weapon() | magic.has_good_spells(self)
        if level == Performance.great:
            return self.has_great_weapon() | magic.has_great_spells(self)
        if level == Performance.galaxy:
            return self.has_galaxy_weapon() | magic.has_amazing_spells(self)

    def can_water(self, level: int) -> StardewRule:
        tool_rule = self.has_tool(Tool.watering_can, ToolMaterial.tiers[level])
        spell_rule = (self.received(MagicSpell.water) & magic.can_use_altar(self) & self.has_skill_level(ModSkill.magic, level))
        return tool_rule | spell_rule

    def has_prismatic_jelly_reward_access(self) -> StardewRule:
        if self.options.special_order_locations == SpecialOrderLocations.option_disabled:
            return self.can_complete_special_order("Prismatic Jelly")
        return self.received("Monster Musk Recipe")

    def has_all_rarecrows(self) -> StardewRule:
        rules = []
        for rarecrow_number in range(1, 9):
            rules.append(self.received(f"Rarecrow #{rarecrow_number}"))
        return And(rules)

    def can_ship(self, item: str = "") -> StardewRule:
        shipping_bin_rule = self.has_building(Building.shipping_bin)
        if item == "":
            return shipping_bin_rule
        return shipping_bin_rule & self.has(item)

