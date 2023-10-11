from __future__ import annotations

from dataclasses import field, dataclass
from typing import Dict, List, Set

from .ability_logic import AbilityLogic
from .action_logic import ActionLogic
from .arcade_logic import ArcadeLogic
from .artisan_logic import ArtisanLogic
from .building_logic import BuildingLogic
from .combat_logic import CombatLogic
from .cooking_logic import CookingLogic
from .crafting_logic import CraftingLogic
from .crop_logic import CropLogic
from .fishing_logic import FishingLogic
from .gift_logic import GiftLogic
from .mine_logic import MineLogic
from .money_logic import MoneyLogic
from .monster_logic import MonsterLogic
from .museum_logic import MuseumLogic
from .pet_logic import PetLogic
from .received_logic import ReceivedLogic
from .has_logic import HasLogic
from .region_logic import RegionLogic
from .relationship_logic import RelationshipLogic
from .season_logic import SeasonLogic
from .shipping_logic import ShippingLogic
from .skill_logic import SkillLogic
from .special_order_logic import SpecialOrderLogic
from .time_logic import TimeLogic
from .tool_logic import ToolLogic
from .wallet_logic import WalletLogic
from ..data.craftable_data import all_crafting_recipes
from ..data.crops_data import crops_by_name
from ..data.monster_data import all_monsters_by_category, all_monsters_by_name
from ..mods.logic.mod_logic import ModLogic
from ..data import all_fish, FishItem, all_purchasable_seeds, SeedItem, all_crops
from ..data.bundle_data import BundleItem
from ..data.fish_data import island_fish, legendary_fish, extended_family
from ..data.museum_data import all_museum_items
from ..data.recipe_data import all_cooking_recipes
from ..options import Cropsanity, SpecialOrderLocations, ExcludeGingerIsland, FestivalLocations, StardewValleyOptions
from ..regions import vanilla_regions
from ..stardew_rule import False_, Or, True_, Count, And, Has, StardewRule
from ..strings.animal_names import Animal, coop_animals, barn_animals
from ..strings.animal_product_names import AnimalProduct
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.ap_names.buff_names import Buff
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.calendar_names import Weekday
from worlds.stardew_valley.strings.craftable_names import Craftable, Consumable, Furniture, Ring, Fishing, Lighting
from ..strings.crop_names import Fruit, Vegetable
from ..strings.currency_names import Currency
from ..strings.decoration_names import Decoration
from ..strings.fertilizer_names import Fertilizer
from ..strings.festival_check_names import FestivalCheck
from ..strings.fish_names import Fish, Trash, WaterItem, WaterChest
from ..strings.flower_names import Flower
from ..strings.forageable_names import Forageable
from ..strings.fruit_tree_names import Sapling
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.gift_names import Gift
from ..strings.ingredient_names import Ingredient
from ..strings.material_names import Material
from ..strings.machine_names import Machine
from ..strings.food_names import Meal, Beverage
from ..strings.metal_names import Ore, MetalBar, Mineral, Fossil
from ..strings.monster_drop_names import Loot
from ..strings.monster_names import Monster
from ..strings.quest_names import Quest
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.seed_names import Seed, TreeSeed
from ..strings.skill_names import Skill
from ..strings.tool_names import Tool, ToolMaterial
from ..strings.villager_names import NPC
from ..strings.wallet_item_names import Wallet

MISSING_ITEM = "THIS ITEM IS MISSING"

fishing_regions = [Region.beach, Region.town, Region.forest, Region.mountain, Region.island_south, Region.island_west]


@dataclass(frozen=False, repr=False)
class StardewLogic:
    player: int
    options: StardewValleyOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    sapling_rules: Dict[str, StardewRule] = field(default_factory=dict)
    tree_fruit_rules: Dict[str, StardewRule] = field(default_factory=dict)
    seed_rules: Dict[str, StardewRule] = field(default_factory=dict)
    cooking_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crafting_rules: Dict[str, StardewRule] = field(default_factory=dict)
    crop_rules: Dict[str, StardewRule] = field(default_factory=dict)
    fish_rules: Dict[str, StardewRule] = field(default_factory=dict)
    museum_rules: Dict[str, StardewRule] = field(default_factory=dict)
    quest_rules: Dict[str, StardewRule] = field(default_factory=dict)
    festival_rules: Dict[str, StardewRule] = field(default_factory=dict)

    def __post_init__(self):
        self.received = ReceivedLogic(self.player)
        self.has = HasLogic(self.player, self.item_rules)
        self.region = RegionLogic(self.player)
        self.time = TimeLogic(self.player, self.received)
        self.season = SeasonLogic(self.player, self.options.season_randomization, self.received, self.time)
        self.money = MoneyLogic(self.player, self.options.starting_money, self.received, self.has, self.region, self.time)
        self.action = ActionLogic(self.player, self.received, self.has, self.region)
        self.arcade = ArcadeLogic(self.player, self.options.arcade_machine_locations, self.received, self.region)
        self.artisan = ArtisanLogic(self.player, self.has, self.time)
        self.gifts = GiftLogic(self.player, self.has)
        tool_option = self.options.tool_progression
        skill_option = self.options.skill_progression
        elevator_option = self.options.elevator_progression
        friendsanity_option = self.options.friendsanity
        heart_size_option = self.options.friendsanity_heart_size
        mods_option = self.options.mods
        self.buildings = BuildingLogic(self.player, self.options.building_progression, self.received, self.has, self.region, self.money)
        self.shipping = ShippingLogic(self.player, self.options.exclude_ginger_island, self.options.special_order_locations, self.has,
                                      self.region, self.buildings)
        self.relationship = RelationshipLogic(self.player, friendsanity_option, heart_size_option,
                                              self.received, self.has, self.region, self.time, self.season, self.gifts, self.buildings, mods_option)
        self.museum = MuseumLogic(self.player, self.options.museumsanity, self.received, self.has, self.region, self.action)
        self.wallet = WalletLogic(self.player, self.received, self.museum)
        self.combat = CombatLogic(self.player, self.received, self.region)
        self.monster = MonsterLogic(self.player, self.region, self.time, self.combat)
        self.tool = ToolLogic(self.player, tool_option, self.received, self.has, self.region, self.season, self.money)
        self.pet = PetLogic(self.player, friendsanity_option, heart_size_option, self.received, self.region, self.time, self.tool)
        self.crop = CropLogic(self.player, self.has, self.region, self.season, self.tool)
        self.skill = SkillLogic(self.player, skill_option, self.received, self.has, self.region, self.season, self.time, self.tool, self.combat, self.crop)
        self.fishing = FishingLogic(self.player, self.region, self.tool, self.skill)
        self.mine = MineLogic(self.player, tool_option, skill_option, elevator_option, self.received, self.region, self.combat,
                              self.tool, self.skill)
        self.cooking = CookingLogic(self.player, self.options.chefsanity, self.options.exclude_ginger_island, self.received, self.has, self.region, self.season, self.time, self.money, self.action, self.buildings, self.relationship, self.skill)
        self.ability = AbilityLogic(self.player, self.options.number_of_movement_buffs, self.options.number_of_luck_buffs, self.received,
                                    self.region, self.tool, self.skill, self.mine)
        self.special_order = SpecialOrderLogic(self.player, self.received, self.has, self.region, self.season, self.time, self.money, self.shipping,
                                               self.arcade, self.artisan, self.relationship, self.tool, self.skill, self.mine, self.cooking, self.ability)
        self.crafting = CraftingLogic(self.player, self.options.craftsanity, self.options.festival_locations,
                                      self.options.special_order_locations, self.received, self.has, self.region, self.time, self.money,
                                      self.relationship, self.skill, self.special_order)

        self.mod = ModLogic(self.player, skill_option, elevator_option, mods_option, self.received, self.has, self.region, self.action, self.season, self.money,
                            self.relationship, self.buildings, self.wallet, self.combat, self.tool, self.skill, self.fishing, self.cooking, self.mine, self.ability)

        self.fish_rules.update({fish.name: self.can_catch_fish(fish) for fish in all_fish})
        self.museum_rules.update({donation.name: self.museum.can_find_museum_item(donation) for donation in all_museum_items})

        for recipe in all_cooking_recipes:
            can_cook_rule = self.cooking.can_cook(recipe)
            if recipe.meal in self.cooking_rules:
                can_cook_rule = can_cook_rule | self.cooking_rules[recipe.meal]
            self.cooking_rules[recipe.meal] = can_cook_rule

        for recipe in all_crafting_recipes:
            can_craft_rule = self.crafting.can_craft(recipe)
            if recipe.item in self.crafting_rules:
                can_craft_rule = can_craft_rule | self.crafting_rules[recipe.item]
            self.crafting_rules[recipe.item] = can_craft_rule

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
            Fruit.apple: self.crop.can_plant_and_grow_item(Season.fall),
            Fruit.apricot: self.crop.can_plant_and_grow_item(Season.spring),
            Fruit.cherry: self.crop.can_plant_and_grow_item(Season.spring),
            Fruit.orange: self.crop.can_plant_and_grow_item(Season.summer),
            Fruit.peach: self.crop.can_plant_and_grow_item(Season.summer),
            Fruit.pomegranate: self.crop.can_plant_and_grow_item(Season.fall),
            Fruit.banana: self.crop.can_plant_and_grow_item(Season.summer),
            Fruit.mango: self.crop.can_plant_and_grow_item(Season.summer),
        })

        for tree_fruit in self.tree_fruit_rules:
            existing_rules = self.tree_fruit_rules[tree_fruit]
            sapling = f"{tree_fruit} Sapling"
            self.tree_fruit_rules[tree_fruit] = existing_rules & self.has(sapling) & self.time.has_lived_months(1)

        self.seed_rules.update({seed.name: self.can_buy_seed(seed) for seed in all_purchasable_seeds})
        self.crop_rules.update({crop.name: self.crop.can_grow(crop) for crop in all_crops})
        self.crop_rules.update({
            Seed.coffee: (self.season.has(Season.spring) | self.season.has(Season.summer)) & self.can_buy_seed(crops_by_name[Seed.coffee].seed),
            Fruit.ancient_fruit: (self.received("Ancient Seeds") | self.received("Ancient Seeds Recipe")) &
                                  self.region.can_reach(Region.greenhouse) & self.has(Machine.seed_maker),
        })

        self.item_rules.update({
            "Energy Tonic": self.money.can_spend_at(Region.hospital, 1000),
            WaterChest.fishing_chest: self.fishing.can_fish_chests(),
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
            Animal.chicken: self.can_buy_animal(Animal.chicken),
            Animal.cow: self.can_buy_animal(Animal.cow),
            Animal.dinosaur: self.buildings.has_building(Building.big_coop) & self.has(AnimalProduct.dinosaur_egg),
            Animal.duck: self.can_buy_animal(Animal.duck),
            Animal.goat: self.can_buy_animal(Animal.goat),
            Animal.ostrich: self.buildings.has_building(Building.barn) & self.has(AnimalProduct.ostrich_egg) & self.has(Machine.ostrich_incubator),
            Animal.pig: self.can_buy_animal(Animal.pig),
            Animal.rabbit: self.can_buy_animal(Animal.rabbit),
            Animal.sheep: self.can_buy_animal(Animal.sheep),
            AnimalProduct.any_egg: self.has(AnimalProduct.chicken_egg) | self.has(AnimalProduct.duck_egg),
            AnimalProduct.brown_egg: self.has_animal(Animal.chicken),
            AnimalProduct.chicken_egg: self.has([AnimalProduct.egg, AnimalProduct.brown_egg, AnimalProduct.large_egg, AnimalProduct.large_brown_egg], 1),
            AnimalProduct.cow_milk: self.has(AnimalProduct.milk) | self.has(AnimalProduct.large_milk),
            AnimalProduct.duck_egg: self.has_animal(Animal.duck),
            AnimalProduct.duck_feather: self.has_happy_animal(Animal.duck),
            AnimalProduct.egg: self.has_animal(Animal.chicken),
            AnimalProduct.goat_milk: self.has(Animal.goat),
            AnimalProduct.golden_egg: self.received(AnimalProduct.golden_egg) & (self.money.can_spend_at(Region.ranch, 100000) | self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 100)),
            AnimalProduct.large_brown_egg: self.has_happy_animal(Animal.chicken),
            AnimalProduct.large_egg: self.has_happy_animal(Animal.chicken),
            AnimalProduct.large_goat_milk: self.has_happy_animal(Animal.goat),
            AnimalProduct.large_milk: self.has_happy_animal(Animal.cow),
            AnimalProduct.milk: self.has_animal(Animal.cow),
            AnimalProduct.ostrich_egg: self.tool.can_forage(Generic.any, Region.island_north, True),
            AnimalProduct.rabbit_foot: self.has_happy_animal(Animal.rabbit),
            AnimalProduct.roe: self.skill.can_fish() & self.buildings.has_building(Building.fish_pond),
            AnimalProduct.squid_ink: self.mine.can_mine_in_the_mines_floor_81_120() | (self.buildings.has_building(Building.fish_pond) & self.has(Fish.squid)),
            AnimalProduct.sturgeon_roe: self.has(Fish.sturgeon) & self.buildings.has_building(Building.fish_pond),
            AnimalProduct.truffle: self.has_animal(Animal.pig) & self.season.has_any_not_winter(),
            AnimalProduct.void_egg: self.money.can_spend_at(Region.sewer, 5000) | (self.buildings.has_building(Building.fish_pond) & self.has(Fish.void_salmon)),
            AnimalProduct.wool: self.has_animal(Animal.rabbit) | self.has_animal(Animal.sheep),
            AnimalProduct.slime_egg_green: self.has(Machine.slime_egg_press) & self.has(Loot.slime),
            AnimalProduct.slime_egg_blue: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(3),
            AnimalProduct.slime_egg_red: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(6),
            AnimalProduct.slime_egg_purple: self.has(Machine.slime_egg_press) & self.has(Loot.slime) & self.time.has_lived_months(9),
            AnimalProduct.slime_egg_tiger: self.has(Fish.lionfish) & self.buildings.has_building(Building.fish_pond),
            ArtisanGood.aged_roe: self.artisan.can_preserves_jar(AnimalProduct.roe),
            ArtisanGood.battery_pack: (self.has(Machine.lightning_rod) & self.season.has_any_not_winter()) | self.has(Machine.solar_panel),
            ArtisanGood.caviar: self.artisan.can_preserves_jar(AnimalProduct.sturgeon_roe),
            ArtisanGood.cheese: (self.has(AnimalProduct.cow_milk) & self.has(Machine.cheese_press)) | (self.region.can_reach(Region.desert) & self.has(Mineral.emerald)),
            ArtisanGood.cloth: (self.has(AnimalProduct.wool) & self.has(Machine.loom)) | (self.region.can_reach(Region.desert) & self.has(Mineral.aquamarine)),
            ArtisanGood.dinosaur_mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.dinosaur_egg),
            ArtisanGood.duck_mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.duck_egg),
            ArtisanGood.goat_cheese: self.has(AnimalProduct.goat_milk) & self.has(Machine.cheese_press),
            ArtisanGood.green_tea: self.artisan.can_keg(Vegetable.tea_leaves),
            ArtisanGood.honey: self.money.can_spend_at(Region.oasis, 200) | (self.has(Machine.bee_house) & self.season.has_any_not_winter()),
            ArtisanGood.jelly: self.artisan.has_jelly(),
            ArtisanGood.juice: self.artisan.has_juice(),
            ArtisanGood.maple_syrup: self.has(Machine.tapper),
            ArtisanGood.mayonnaise: self.artisan.can_mayonnaise(AnimalProduct.chicken_egg),
            ArtisanGood.mead: self.artisan.can_keg(ArtisanGood.honey),
            ArtisanGood.oak_resin: self.has(Machine.tapper),
            ArtisanGood.pale_ale: self.artisan.can_keg(Vegetable.hops),
            ArtisanGood.pickles: self.artisan.has_pickle(),
            ArtisanGood.pine_tar: self.has(Machine.tapper),
            ArtisanGood.truffle_oil: self.has(AnimalProduct.truffle) & self.has(Machine.oil_maker),
            ArtisanGood.void_mayonnaise: (self.skill.can_fish(Region.witch_swamp)) | (self.artisan.can_mayonnaise(AnimalProduct.void_egg)),
            ArtisanGood.wine: self.artisan.has_wine(),
            Beverage.beer: self.artisan.can_keg(Vegetable.wheat) | self.money.can_spend_at(Region.saloon, 400),
            Beverage.coffee: self.artisan.can_keg(Seed.coffee) | self.has(Machine.coffee_maker) | (self.money.can_spend_at(Region.saloon, 300)) | self.has("Hot Java Ring"),
            Beverage.pina_colada: self.money.can_spend_at(Region.island_resort, 600),
            Beverage.triple_shot_espresso: self.has("Hot Java Ring"),
            Decoration.rotten_plant: self.has(Lighting.jack_o_lantern) & self.season.has(Season.winter),
            Fertilizer.basic: (self.has(Material.sap) & self.skill.has_farming_level(1)) | (self.time.has_lived_months(1) & self.money.can_spend_at(Region.pierre_store, 100)),
            Fertilizer.deluxe: False_(),
            Fertilizer.quality: (self.skill.has_farming_level(9) & self.has(Material.sap) & self.has(Fish.any)) | (self.time.has_year_two() & self.money.can_spend_at(Region.pierre_store, 150)),
            Fertilizer.tree: self.skill.has_level(Skill.foraging, 7) & self.has(Material.fiber) & self.has(Material.stone),
            Fish.any: Or([self.can_catch_fish(fish) for fish in all_fish]),
            Fish.crab: self.skill.can_crab_pot(Region.beach),
            Fish.crayfish: self.skill.can_crab_pot(Region.town),
            Fish.lobster: self.skill.can_crab_pot(Region.beach),
            Fish.mussel: self.tool.can_forage(Generic.any, Region.beach) or self.has(Fish.mussel_node),
            Fish.mussel_node: self.region.can_reach(Region.island_west),
            Fish.oyster: self.tool.can_forage(Generic.any, Region.beach),
            Fish.periwinkle: self.skill.can_crab_pot(Region.town),
            Fish.shrimp: self.skill.can_crab_pot(Region.beach),
            Fish.snail: self.skill.can_crab_pot(Region.town),
            Fishing.curiosity_lure: self.monster.can_kill(all_monsters_by_name[Monster.mummy]),
            Fishing.lead_bobber: self.skill.has_level(Skill.fishing, 6) & self.money.can_spend_at(Region.fish_shop, 200),
            Forageable.blackberry: self.tool.can_forage(Season.fall),
            Forageable.cactus_fruit: self.tool.can_forage(Generic.any, Region.desert),
            Forageable.cave_carrot: self.tool.can_forage(Generic.any, Region.mines_floor_10, True),
            Forageable.chanterelle: self.tool.can_forage(Season.fall, Region.secret_woods),
            Forageable.coconut: self.tool.can_forage(Generic.any, Region.desert),
            Forageable.common_mushroom: self.tool.can_forage(Season.fall) | (self.tool.can_forage(Season.spring, Region.secret_woods)),
            Forageable.crocus: self.tool.can_forage(Season.winter),
            Forageable.crystal_fruit: self.tool.can_forage(Season.winter),
            Forageable.daffodil: self.tool.can_forage(Season.spring),
            Forageable.dandelion: self.tool.can_forage(Season.spring),
            Forageable.dragon_tooth: self.tool.can_forage(Generic.any, Region.volcano_floor_10),
            Forageable.fiddlehead_fern: self.tool.can_forage(Season.summer, Region.secret_woods),
            Forageable.ginger: self.tool.can_forage(Generic.any, Region.island_west, True),
            Forageable.hay: self.buildings.has_building(Building.silo) & self.tool.has_tool(Tool.scythe),
            Forageable.hazelnut: self.tool.can_forage(Season.fall),
            Forageable.holly: self.tool.can_forage(Season.winter),
            Forageable.journal_scrap: self.region.can_reach_all([Region.island_west, Region.island_north, Region.island_south, Region.volcano_floor_10]) & self.received(Wallet.magnifying_glass) & (self.ability.can_chop_trees() | self.mine.can_mine_in_the_mines_floor_1_40()),
            Forageable.leek: self.tool.can_forage(Season.spring),
            Forageable.magma_cap: self.tool.can_forage(Generic.any, Region.volcano_floor_5),
            Forageable.morel: self.tool.can_forage(Season.spring, Region.secret_woods),
            Forageable.purple_mushroom: self.tool.can_forage(Generic.any, Region.mines_floor_95) | self.tool.can_forage(Generic.any, Region.skull_cavern_25),
            Forageable.rainbow_shell: self.tool.can_forage(Season.summer, Region.beach),
            Forageable.red_mushroom: self.tool.can_forage(Season.summer, Region.secret_woods) | self.tool.can_forage(Season.fall, Region.secret_woods),
            Forageable.salmonberry: self.tool.can_forage(Season.spring),
            Forageable.secret_note: self.received(Wallet.magnifying_glass) & (self.ability.can_chop_trees() | self.mine.can_mine_in_the_mines_floor_1_40()),
            Forageable.snow_yam: self.tool.can_forage(Season.winter, Region.beach, True),
            Forageable.spice_berry: self.tool.can_forage(Season.summer),
            Forageable.spring_onion: self.tool.can_forage(Season.spring),
            Forageable.sweet_pea: self.tool.can_forage(Season.summer),
            Forageable.wild_horseradish: self.tool.can_forage(Season.spring),
            Forageable.wild_plum: self.tool.can_forage(Season.fall),
            Forageable.winter_root: self.tool.can_forage(Season.winter, Region.forest, True),
            Fossil.bone_fragment: (self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.pickaxe)) | self.monster.can_kill(Monster.skeleton),
            Fossil.fossilized_leg: self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.pickaxe),
            Fossil.fossilized_ribs: self.region.can_reach(Region.island_south) & self.tool.has_tool(Tool.hoe),
            Fossil.fossilized_skull: self.action.can_open_geode(Geode.golden_coconut),
            Fossil.fossilized_spine: self.fishing.can_fish_at(Region.dig_site),
            Fossil.fossilized_tail: self.action.can_pan_at(Region.dig_site),
            Fossil.mummified_bat: self.region.can_reach(Region.volcano_floor_10),
            Fossil.mummified_frog: self.region.can_reach(Region.island_east) & self.tool.has_tool(Tool.scythe),
            Fossil.snake_skull: self.region.can_reach(Region.dig_site) & self.tool.has_tool(Tool.hoe),
            Fossil.snake_vertebrae: self.region.can_reach(Region.island_west) & self.tool.has_tool(Tool.hoe),
            Geode.artifact_trove: self.has(Geode.omni) & self.region.can_reach(Region.desert),
            Geode.frozen: self.mine.can_mine_in_the_mines_floor_41_80(),
            Geode.geode: self.mine.can_mine_in_the_mines_floor_1_40(),
            Geode.golden_coconut: self.region.can_reach(Region.island_north),
            Geode.magma: self.mine.can_mine_in_the_mines_floor_81_120() | (self.has(Fish.lava_eel) & self.buildings.has_building(Building.fish_pond)),
            Geode.omni: self.mine.can_mine_in_the_mines_floor_41_80() | self.region.can_reach(Region.desert) | self.action.can_pan() | self.received(Wallet.rusty_key) | (self.has(Fish.octopus) & self.buildings.has_building(Building.fish_pond)) | self.region.can_reach(Region.volcano_floor_10),
            Gift.bouquet: self.relationship.has_hearts(Generic.bachelor, 8) & self.money.can_spend_at(Region.pierre_store, 100),
            Gift.golden_pumpkin: self.season.has(Season.fall) | self.action.can_open_geode(Geode.artifact_trove),
            Gift.mermaid_pendant: self.region.can_reach(Region.tide_pools) & self.relationship.has_hearts(Generic.bachelor, 10) & self.buildings.has_house(1) & self.has(Consumable.rain_totem),
            Gift.movie_ticket: self.money.can_spend_at(Region.movie_ticket_stand, 1000),
            Gift.pearl: (self.has(Fish.blobfish) & self.buildings.has_building(Building.fish_pond)) | self.action.can_open_geode(Geode.artifact_trove),
            Gift.tea_set: self.season.has(Season.winter) & self.time.has_lived_max_months(),
            Gift.void_ghost_pendant: self.money.can_trade_at(Region.desert, Loot.void_essence, 200),
            Gift.wilted_bouquet: self.has(Machine.furnace) & self.has(Gift.bouquet) & self.has(Material.coal),
            Ingredient.oil: self.money.can_spend_at(Region.pierre_store, 200) | (self.has(Machine.oil_maker) & (self.has(Vegetable.corn) | self.has(Flower.sunflower) | self.has(Seed.sunflower))),
            Ingredient.qi_seasoning: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 10),
            Ingredient.rice: self.money.can_spend_at(Region.pierre_store, 200) | (self.buildings.has_building(Building.mill) & self.has(Vegetable.unmilled_rice)),
            Ingredient.sugar: self.money.can_spend_at(Region.pierre_store, 100) | (self.buildings.has_building(Building.mill) & self.has(Vegetable.beet)),
            Ingredient.vinegar: self.money.can_spend_at(Region.pierre_store, 200),
            Ingredient.wheat_flour: self.money.can_spend_at(Region.pierre_store, 100) | (self.buildings.has_building(Building.mill) & self.has(Vegetable.wheat)),
            Loot.bat_wing: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern(),
            Loot.bug_meat: self.mine.can_mine_in_the_mines_floor_1_40(),
            Loot.slime: self.mine.can_mine_in_the_mines_floor_1_40(),
            Loot.solar_essence: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern(),
            Loot.void_essence: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern(),
            Machine.bee_house: self.skill.has_farming_level(3) & self.has(MetalBar.iron) & self.has(ArtisanGood.maple_syrup) & self.has(Material.coal) & self.has(Material.wood),
            Machine.cask: self.buildings.has_house(3) & self.region.can_reach(Region.cellar) & self.has(Material.wood) & self.has(Material.hardwood),
            Machine.cheese_press: self.skill.has_farming_level(6) & self.has(Material.wood) & self.has(Material.stone) & self.has(Material.hardwood) & self.has(MetalBar.copper),
            Machine.coffee_maker: self.received(Machine.coffee_maker),
            Machine.crab_pot: self.skill.has_level(Skill.fishing, 3) & (self.money.can_spend_at(Region.fish_shop, 1500) | (self.has(MetalBar.iron) & self.has(Material.wood))),
            Machine.furnace: self.has(Material.stone) & self.has(Ore.copper),
            Machine.keg: self.skill.has_farming_level(8) & self.has(Material.wood) & self.has(MetalBar.iron) & self.has(MetalBar.copper) & self.has(ArtisanGood.oak_resin),
            Machine.lightning_rod: self.skill.has_level(Skill.foraging, 6) & self.has(MetalBar.iron) & self.has(MetalBar.quartz) & self.has(Loot.bat_wing),
            Machine.loom: self.skill.has_farming_level(7) & self.has(Material.wood) & self.has(Material.fiber) & self.has(ArtisanGood.pine_tar),
            Machine.mayonnaise_machine: self.skill.has_farming_level(2) & self.has(Material.wood) & self.has(Material.stone) & self.has("Earth Crystal") & self.has(MetalBar.copper),
            Machine.ostrich_incubator: self.received("Ostrich Incubator Recipe") & self.has(Fossil.bone_fragment) & self.has(Material.hardwood) & self.has(Material.cinder_shard),
            Machine.preserves_jar: self.skill.has_farming_level(4) & self.has(Material.wood) & self.has(Material.stone) & self.has(Material.coal),
            Machine.recycling_machine: self.skill.has_level(Skill.fishing, 4) & self.has(Material.wood) & self.has(Material.stone) & self.has(MetalBar.iron),
            Machine.seed_maker: self.skill.has_farming_level(9) & self.has(Material.wood) & self.has(MetalBar.gold) & self.has(Material.coal),
            Machine.solar_panel: self.received("Solar Panel Recipe") & self.has(MetalBar.quartz) & self.has(MetalBar.iron) & self.has(MetalBar.gold),
            Machine.tapper: self.skill.has_level(Skill.foraging, 3) & self.has(Material.wood) & self.has(MetalBar.copper),
            Machine.worm_bin: self.skill.has_level(Skill.fishing, 8) & self.has(Material.hardwood) & self.has(MetalBar.gold) & self.has(MetalBar.iron) & self.has(Material.fiber),
            Machine.enricher: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 20),
            Machine.pressure_nozzle: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 20),
            Material.cinder_shard: self.region.can_reach(Region.volcano_floor_5),
            Material.clay: self.region.can_reach_any([Region.farm, Region.beach, Region.quarry]) & self.tool.has_tool(Tool.hoe),
            Material.coal: self.mine.can_mine_in_the_mines_floor_41_80() | self.action.can_pan(),
            Material.fiber: True_(),
            Material.hardwood: self.tool.has_tool(Tool.axe, ToolMaterial.copper) & (self.region.can_reach(Region.secret_woods) | self.region.can_reach(Region.island_west)),
            Material.sap: self.ability.can_chop_trees(),
            Material.stone: self.tool.has_tool(Tool.pickaxe),
            Material.wood: self.tool.has_tool(Tool.axe),
            Meal.bread: self.money.can_spend_at(Region.saloon, 120),
            Meal.ice_cream: (self.season.has(Season.summer) & self.money.can_spend_at(Region.town, 250)) | self.money.can_spend_at(Region.oasis, 240),
            Meal.pizza: self.money.can_spend_at(Region.saloon, 600),
            Meal.salad: self.money.can_spend_at(Region.saloon, 220),
            Meal.spaghetti: self.money.can_spend_at(Region.saloon, 240),
            Meal.strange_bun: self.relationship.has_hearts(NPC.shane, 7) & self.has(Ingredient.wheat_flour) & self.has(Fish.periwinkle) & self.has(ArtisanGood.void_mayonnaise),
            MetalBar.copper: self.can_smelt(Ore.copper),
            MetalBar.gold: self.can_smelt(Ore.gold),
            MetalBar.iridium: self.can_smelt(Ore.iridium),
            MetalBar.iron: self.can_smelt(Ore.iron),
            MetalBar.quartz: self.can_smelt("Quartz") | self.can_smelt("Fire Quartz") | (self.has(Machine.recycling_machine) & (self.has(Trash.broken_cd) | self.has(Trash.broken_glasses))),
            MetalBar.radioactive: self.can_smelt(Ore.radioactive),
            Ore.copper: self.mine.can_mine_in_the_mines_floor_1_40() | self.mine.can_mine_in_the_skull_cavern() | self.action.can_pan(),
            Ore.gold: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern() | self.action.can_pan(),
            Ore.iridium: self.mine.can_mine_in_the_skull_cavern(),
            Ore.iron: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern() | self.action.can_pan(),
            Ore.radioactive: self.ability.can_mine_perfectly() & self.region.can_reach(Region.qi_walnut_room),
            Sapling.tea: self.relationship.has_hearts(NPC.caroline, 2) & self.has(Material.fiber) & self.has(Material.wood),
            Seed.mixed: self.tool.has_tool(Tool.scythe) & self.region.can_reach_all([Region.farm, Region.forest, Region.town]),
            Trash.broken_cd: self.skill.can_crab_pot(),
            Trash.broken_glasses: self.skill.can_crab_pot(),
            Trash.driftwood: self.skill.can_crab_pot(),
            Trash.joja_cola: self.money.can_spend_at(Region.saloon, 75),
            Trash.soggy_newspaper: self.skill.can_crab_pot(),
            Trash.trash: self.skill.can_crab_pot(),
            TreeSeed.acorn: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mahogany: self.region.can_reach(Region.secret_woods) & self.tool.has_tool(Tool.axe, ToolMaterial.iron) & self.skill.has_level(Skill.foraging, 1),
            TreeSeed.maple: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            TreeSeed.mushroom: self.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 5),
            TreeSeed.pine: self.skill.has_level(Skill.foraging, 1) & self.ability.can_chop_trees(),
            Vegetable.tea_leaves: self.has(Sapling.tea) & self.time.has_lived_months(2) & self.season.has_any_not_winter(),
            WaterItem.clam: self.tool.can_forage(Generic.any, Region.beach),
            WaterItem.cockle: self.tool.can_forage(Generic.any, Region.beach),
            WaterItem.coral: self.tool.can_forage(Generic.any, Region.tide_pools) | self.tool.can_forage(Season.summer, Region.beach),
            WaterItem.green_algae: self.fishing.can_fish_in_freshwater(),
            WaterItem.nautilus_shell: self.tool.can_forage(Season.winter, Region.beach),
            WaterItem.sea_urchin: self.tool.can_forage(Generic.any, Region.tide_pools),
            WaterItem.seaweed: self.skill.can_fish(Region.beach) | self.region.can_reach(Region.tide_pools),
            WaterItem.white_algae: self.skill.can_fish(Region.mines_floor_20),
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

        # For some recipes, the crafted item can be obtained directly, so we either craft it or get it
        for recipe in self.crafting_rules:
            crafting_rule = self.crafting_rules[recipe]
            obtention_rule = self.item_rules[recipe] if recipe in self.item_rules else False_()
            self.item_rules[recipe] = obtention_rule | crafting_rule

        self.buildings.initialize_rules()
        self.buildings.update_rules(self.mod.buildings.get_modded_building_rules())

        self.quest_rules.update({
            Quest.introductions: self.region.can_reach(Region.town),
            Quest.how_to_win_friends: self.can_complete_quest(Quest.introductions),
            Quest.getting_started: self.has(Vegetable.parsnip) & self.tool.has_tool(Tool.hoe) & self.tool.can_water(0),
            Quest.to_the_beach: self.region.can_reach(Region.beach),
            Quest.raising_animals: self.can_complete_quest(Quest.getting_started) & self.buildings.has_building(Building.coop),
            Quest.advancement: self.can_complete_quest(Quest.getting_started) & self.has(Craftable.scarecrow),
            Quest.archaeology: (self.tool.has_tool(Tool.hoe) | self.mine.can_mine_in_the_mines_floor_1_40() | self.skill.can_fish()) & self.region.can_reach(Region.museum),
            Quest.meet_the_wizard: self.region.can_reach(Region.town) & self.region.can_reach(Region.community_center) & self.region.can_reach(Region.wizard_tower),
            Quest.forging_ahead: self.has(Ore.copper) & self.has(Machine.furnace),
            Quest.smelting: self.has(MetalBar.copper),
            Quest.initiation: self.mine.can_mine_in_the_mines_floor_1_40(),
            Quest.robins_lost_axe: self.season.has(Season.spring) & self.region.can_reach(Region.forest) & self.relationship.can_meet(NPC.robin),
            Quest.jodis_request: self.season.has(Season.spring) & self.has(Vegetable.cauliflower) & self.relationship.can_meet(NPC.jodi),
            Quest.mayors_shorts: self.season.has(Season.summer) & self.region.can_reach(Region.ranch) &
                                 (self.relationship.has_hearts(NPC.marnie, 2) | (self.mod.magic.can_blink())) & self.relationship.can_meet(NPC.lewis),
            Quest.blackberry_basket: self.season.has(Season.fall) & self.relationship.can_meet(NPC.linus),
            Quest.marnies_request: self.relationship.has_hearts(NPC.marnie, 3) & self.has(Forageable.cave_carrot) & self.region.can_reach(Region.ranch),
            Quest.pam_is_thirsty: self.season.has(Season.summer) & self.has(ArtisanGood.pale_ale) & self.relationship.can_meet(NPC.pam),
            Quest.a_dark_reagent: self.season.has(Season.winter) & self.has(Loot.void_essence) & self.relationship.can_meet(NPC.wizard),
            Quest.cows_delight: self.season.has(Season.fall) & self.has(Vegetable.amaranth) & self.relationship.can_meet(NPC.marnie),
            Quest.the_skull_key: self.received(Wallet.skull_key) & self.region.can_reach(Region.skull_cavern_entrance),
            Quest.crop_research: self.season.has(Season.summer) & self.has(Fruit.melon) & self.relationship.can_meet(NPC.demetrius),
            Quest.knee_therapy: self.season.has(Season.summer) & self.has(Fruit.hot_pepper) & self.relationship.can_meet(NPC.george),
            Quest.robins_request: self.season.has(Season.winter) & self.has(Material.hardwood) & self.relationship.can_meet(NPC.robin),
            Quest.qis_challenge: self.mine.can_mine_in_the_skull_cavern(),
            Quest.the_mysterious_qi: self.region.can_reach(Region.bus_tunnel) & self.has(ArtisanGood.battery_pack) & self.region.can_reach(Region.desert) & self.has(Forageable.rainbow_shell) & self.has(Vegetable.beet) & self.has(Loot.solar_essence),
            Quest.carving_pumpkins: self.season.has(Season.fall) & self.has(Vegetable.pumpkin) & self.relationship.can_meet(NPC.caroline),
            Quest.a_winter_mystery: self.season.has(Season.winter) & self.region.can_reach(Region.town),
            Quest.strange_note: self.has(Forageable.secret_note) & self.region.can_reach(Region.secret_woods) & self.has(ArtisanGood.maple_syrup),
            Quest.cryptic_note: self.has(Forageable.secret_note) & self.region.can_reach(Region.skull_cavern_100),
            Quest.fresh_fruit: self.season.has(Season.spring) & self.has(Fruit.apricot) & self.relationship.can_meet(NPC.emily),
            Quest.aquatic_research: self.season.has(Season.summer) & self.has(Fish.pufferfish) & self.relationship.can_meet(NPC.demetrius),
            Quest.a_soldiers_star: self.season.has(Season.summer) & self.time.has_year_two() & self.has(Fruit.starfruit) & self.relationship.can_meet(NPC.kent),
            Quest.mayors_need: self.season.has(Season.summer) & self.has(ArtisanGood.truffle_oil) & self.relationship.can_meet(NPC.lewis),
            Quest.wanted_lobster: self.season.has(Season.fall) & self.season.has(Season.fall) & self.has(Fish.lobster) & self.relationship.can_meet(NPC.gus),
            Quest.pam_needs_juice: self.season.has(Season.fall) & self.has(ArtisanGood.battery_pack) & self.relationship.can_meet(NPC.pam),
            Quest.fish_casserole: self.relationship.has_hearts(NPC.jodi, 4) & self.has(Fish.largemouth_bass) & self.region.can_reach(Region.sam_house),
            Quest.catch_a_squid: self.season.has(Season.winter) & self.has(Fish.squid) & self.relationship.can_meet(NPC.willy),
            Quest.fish_stew: self.season.has(Season.winter) & self.has(Fish.albacore) & self.relationship.can_meet(NPC.gus),
            Quest.pierres_notice: self.season.has(Season.spring) & self.has("Sashimi") & self.relationship.can_meet(NPC.pierre),
            Quest.clints_attempt: self.season.has(Season.winter) & self.has(Mineral.amethyst) & self.relationship.can_meet(NPC.emily),
            Quest.a_favor_for_clint: self.season.has(Season.winter) & self.has(MetalBar.iron) & self.relationship.can_meet(NPC.clint),
            Quest.staff_of_power: self.season.has(Season.winter) & self.has(MetalBar.iridium) & self.relationship.can_meet(NPC.wizard),
            Quest.grannys_gift: self.season.has(Season.spring) & self.has(Forageable.leek) & self.relationship.can_meet(NPC.evelyn),
            Quest.exotic_spirits: self.season.has(Season.winter) & self.has(Forageable.coconut) & self.relationship.can_meet(NPC.gus),
            Quest.catch_a_lingcod: self.season.has(Season.winter) & self.has("Lingcod") & self.relationship.can_meet(NPC.willy),
            Quest.dark_talisman: self.wallet.has_rusty_key() & self.region.can_reach(Region.railroad) & self.relationship.can_meet(NPC.krobus) & self.region.can_reach(Region.mutant_bug_lair),
            Quest.goblin_problem: self.region.can_reach(Region.witch_swamp) & self.has(ArtisanGood.void_mayonnaise),
            Quest.magic_ink: self.region.can_reach(Region.witch_hut) & self.relationship.can_meet(NPC.wizard),
            Quest.the_pirates_wife: self.region.can_reach(Region.island_west) & self.relationship.can_meet(NPC.kent) &
                                    self.relationship.can_meet(NPC.gus) & self.relationship.can_meet(NPC.sandy) & self.relationship.can_meet(NPC.george) &
                                    self.relationship.can_meet(NPC.wizard) & self.relationship.can_meet(NPC.willy),
        })

        self.quest_rules.update(self.mod.quests.get_modded_quest_rules())

        self.festival_rules.update({
            FestivalCheck.egg_hunt: self.can_win_egg_hunt(),
            FestivalCheck.strawberry_seeds: self.money.can_spend(1000),
            FestivalCheck.dance: self.relationship.has_hearts(Generic.bachelor, 4),
            FestivalCheck.tub_o_flowers: self.money.can_spend(2000),
            FestivalCheck.rarecrow_5: self.money.can_spend(2500),
            FestivalCheck.luau_soup: self.can_succeed_luau_soup(),
            FestivalCheck.moonlight_jellies: True_(),
            FestivalCheck.moonlight_jellies_banner: self.money.can_spend(800),
            FestivalCheck.starport_decal: self.money.can_spend(1000),
            FestivalCheck.smashing_stone: True_(),
            FestivalCheck.grange_display: self.can_succeed_grange_display(),
            FestivalCheck.rarecrow_1: True_(),  # only cost star tokens
            FestivalCheck.fair_stardrop: True_(),  # only cost star tokens
            FestivalCheck.spirit_eve_maze: True_(),
            FestivalCheck.jack_o_lantern: self.money.can_spend(2000),
            FestivalCheck.rarecrow_2: self.money.can_spend(5000),
            FestivalCheck.fishing_competition: self.can_win_fishing_competition(),
            FestivalCheck.rarecrow_4: self.money.can_spend(5000),
            FestivalCheck.mermaid_pearl: self.has(Forageable.secret_note),
            FestivalCheck.cone_hat: self.money.can_spend(2500),
            FestivalCheck.iridium_fireplace: self.money.can_spend(15000),
            FestivalCheck.rarecrow_7: self.money.can_spend(5000) & self.museum.can_donate_museum_artifacts(20),
            FestivalCheck.rarecrow_8: self.money.can_spend(5000) & self.museum.can_donate_museum_items(40),
            FestivalCheck.lupini_red_eagle: self.money.can_spend(1200),
            FestivalCheck.lupini_portrait_mermaid: self.money.can_spend(1200),
            FestivalCheck.lupini_solar_kingdom: self.money.can_spend(1200),
            FestivalCheck.lupini_clouds: self.time.has_year_two() & self.money.can_spend(1200),
            FestivalCheck.lupini_1000_years: self.time.has_year_two() & self.money.can_spend(1200),
            FestivalCheck.lupini_three_trees: self.time.has_year_two() & self.money.can_spend(1200),
            FestivalCheck.lupini_the_serpent: self.time.has_year_three() & self.money.can_spend(1200),
            FestivalCheck.lupini_tropical_fish: self.time.has_year_three() & self.money.can_spend(1200),
            FestivalCheck.lupini_land_of_clay: self.time.has_year_three() & self.money.can_spend(1200),
            FestivalCheck.secret_santa: self.gifts.has_any_universal_love(),
            FestivalCheck.legend_of_the_winter_star: True_(),
            FestivalCheck.all_rarecrows: self.region.can_reach(Region.farm) & self.has_all_rarecrows(),
        })

        self.special_order.initialize_rules()
        self.special_order.update_rules(self.mod.special_orders.get_modded_special_orders_rules(self.special_order.special_order_rules))

    def can_complete_quest(self, quest: str) -> StardewRule:
        return Has(quest, self.quest_rules)

    def can_buy_seed(self, seed: SeedItem) -> StardewRule:
        if self.options.cropsanity == Cropsanity.option_disabled or seed.name == Seed.qi_bean:
            item_rule = True_()
        else:
            item_rule = self.received(seed.name)
        if seed.name == Seed.coffee:
            item_rule = item_rule & self.has_traveling_merchant(3)
        season_rule = self.season.has_any(seed.seasons)
        region_rule = self.region.can_reach_all(seed.regions)
        currency_rule = self.money.can_spend(1000)
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
        can_buy_sapling = self.money.can_spend_at(Region.pierre_store, sapling_prices[fruit])
        if fruit == Fruit.banana:
            can_buy_sapling = self.has_island_trader() & self.has(Forageable.dragon_tooth)
        elif fruit == Fruit.mango:
            can_buy_sapling = self.has_island_trader() & self.has(Fish.mussel_node)

        return allowed_buy_sapling & can_buy_sapling

    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        quest_rule = True_()
        if fish.extended_family:
            quest_rule = self.can_start_extended_family_quest()
        region_rule = self.region.can_reach_any(fish.locations)
        season_rule = self.season.has_any(fish.seasons)
        if fish.difficulty == -1:
            difficulty_rule = self.skill.can_crab_pot()
        else:
            difficulty_rule = self.skill.can_fish([], 120 if fish.legendary else fish.difficulty)
        return quest_rule & region_rule & season_rule & difficulty_rule

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.skill.has_level(Skill.fishing, 10), self.tool.has_fishing_rod(4)]
        exclude_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        exclude_extended_family = self.options.special_order_locations != SpecialOrderLocations.option_board_qi
        for fish in all_fish:
            if exclude_island and fish in island_fish:
                continue
            if exclude_extended_family and fish in extended_family:
                continue
            rules.append(self.can_catch_fish(fish))
        return And(rules)

    def can_start_extended_family_quest(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if self.options.special_order_locations != SpecialOrderLocations.option_board_qi:
            return False_()
        return self.region.can_reach(Region.qi_walnut_room) & And([self.can_catch_fish(fish) for fish in legendary_fish])

    def can_smelt(self, item: str) -> StardewRule:
        return self.has(Machine.furnace) & self.has(item)

    def has_traveling_merchant(self, tier: int = 1):
        if tier <= 0:
            return True_()
        tier = min(7, max(1, tier))
        traveling_merchant_days = [f"Traveling Merchant: {day}" for day in Weekday.all_days]
        return self.received(traveling_merchant_days, tier)

    def can_complete_bundle(self, bundle_requirements: List[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        highest_quality_yet = 0
        can_speak_junimo = self.region.can_reach(Region.wizard_tower)
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return can_speak_junimo & self.money.can_spend(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
                if bundle_item.quality > highest_quality_yet:
                    highest_quality_yet = bundle_item.quality
        return can_speak_junimo & self.has(item_rules, number_required) & self.can_grow_gold_quality(highest_quality_yet)

    def can_grow_gold_quality(self, quality: int) -> StardewRule:
        if quality <= 0:
            return True_()
        if quality == 1:
            return self.skill.has_farming_level(5) | (self.has_fertilizer(1) & self.skill.has_farming_level(2)) | (
                    self.has_fertilizer(2) & self.skill.has_farming_level(1)) | self.has_fertilizer(3)
        if quality == 2:
            return self.skill.has_farming_level(10) | (self.has_fertilizer(1) & self.skill.has_farming_level(5)) | (
                    self.has_fertilizer(2) & self.skill.has_farming_level(3)) | (
                           self.has_fertilizer(3) & self.skill.has_farming_level(2))
        if quality >= 3:
            return self.has_fertilizer(3) & self.skill.has_farming_level(4)

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
        field_office = self.region.can_reach(Region.field_office)
        professor_snail = self.received("Open Professor Snail Cave")
        tools = self.tool.has_tool(Tool.pickaxe) & self.tool.has_tool(Tool.hoe) & self.tool.has_tool(Tool.scythe)
        leg_and_snake_skull = self.has(Fossil.fossilized_leg) & self.has(Fossil.snake_skull)
        ribs_and_spine = self.has(Fossil.fossilized_ribs) & self.has(Fossil.fossilized_spine)
        skull = self.has(Fossil.fossilized_skull)
        tail = self.has(Fossil.fossilized_tail)
        frog = self.has(Fossil.mummified_frog)
        bat = self.has(Fossil.mummified_bat)
        snake_vertebrae = self.has(Fossil.snake_vertebrae)
        return field_office & professor_snail & tools & leg_and_snake_skull & ribs_and_spine & skull & tail & frog & bat & snake_vertebrae

    def can_complete_community_center(self) -> StardewRule:
        return (self.region.can_reach_location("Complete Crafts Room") &
                self.region.can_reach_location("Complete Pantry") &
                self.region.can_reach_location("Complete Fish Tank") &
                self.region.can_reach_location("Complete Bulletin Board") &
                self.region.can_reach_location("Complete Vault") &
                self.region.can_reach_location("Complete Boiler Room"))

    def can_finish_grandpa_evaluation(self) -> StardewRule:
        # https://stardewvalleywiki.com/Grandpa
        rules_worth_a_point = [self.money.can_have_earned_total(50000),  # 50 000g
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
                               self.relationship.can_get_married() & self.buildings.has_house(2),
                               self.relationship.has_hearts("5", 8),  # 5 Friends
                               self.relationship.has_hearts("10", 8),  # 10 friends
                               self.pet.has_hearts(5),  # Max Pet
                               self.can_complete_community_center(),  # Community Center Completion
                               self.can_complete_community_center(),  # CC Ceremony first point
                               self.can_complete_community_center(),  # CC Ceremony second point
                               self.received(Wallet.skull_key),  # Skull Key obtained
                               self.wallet.has_rusty_key(),  # Rusty key obtained
                               ]
        return Count(12, rules_worth_a_point)

    def can_complete_all_monster_slaying_goals(self) -> StardewRule:
        rules = [self.time.has_lived_max_months()]
        exclude_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        island_regions = [Region.volcano_floor_5, Region.volcano_floor_10, Region.island_west]
        for category in all_monsters_by_category:
            if exclude_island and all(monster.locations[0] in island_regions for monster in all_monsters_by_category[category]):
                continue
            rules.append(self.monster.can_kill_any(all_monsters_by_category[category]))

        return And(rules)

    def can_win_egg_hunt(self) -> StardewRule:
        number_of_movement_buffs = self.options.number_of_movement_buffs
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
        keg_rules = [self.artisan.can_keg(kegable) for kegable in eligible_kegables]
        aged_rule = [self.artisan.can_age(rule, "Iridium") for rule in keg_rules]
        # There are a few other valid items but I don't feel like coding them all
        return Or(fish_rule) | Or(aged_rule)

    def can_succeed_grange_display(self) -> StardewRule:
        if self.options.festival_locations != FestivalLocations.option_hard:
            return True_()
        animal_rule = self.has_animal(Generic.any)
        artisan_rule = self.artisan.can_keg(Generic.any) | self.artisan.can_preserves_jar(Generic.any)
        cooking_rule = self.money.can_spend_at(Region.saloon, 220)  # Salads at the bar are good enough
        fish_rule = self.skill.can_fish([], 50)
        forage_rule = self.region.can_reach_any([Region.forest, Region.backwoods])  # Hazelnut always available since the grange display is in fall
        mineral_rule = self.action.can_open_geode(Generic.any)  # More than half the minerals are good enough
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
        return self.skill.can_fish([], 60)

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
        return self.money.can_spend_at(Region.ranch, price) & self.buildings.has_building(building)

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

    def has_island_trader(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        return self.region.can_reach(Region.island_trader)

    def has_walnut(self, number: int) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if number <= 0:
            return True_()
        # https://stardewcommunitywiki.com/Golden_Walnut#Walnut_Locations
        reach_south = self.region.can_reach(Region.island_south)
        reach_north = self.region.can_reach(Region.island_north)
        reach_west = self.region.can_reach(Region.island_west)
        reach_hut = self.region.can_reach(Region.leo_hut)
        reach_southeast = self.region.can_reach(Region.island_south_east)
        reach_pirate_cove = self.region.can_reach(Region.pirate_cove)
        reach_outside_areas = And(reach_south, reach_north, reach_west, reach_hut)
        reach_volcano_regions = [self.region.can_reach(Region.volcano),
                                 self.region.can_reach(Region.volcano_secret_beach),
                                 self.region.can_reach(Region.volcano_floor_5),
                                 self.region.can_reach(Region.volcano_floor_10)]
        reach_volcano = Or(reach_volcano_regions)
        reach_all_volcano = And(reach_volcano_regions)
        reach_walnut_regions = [reach_south, reach_north, reach_west, reach_volcano]
        reach_caves = And(self.region.can_reach(Region.qi_walnut_room), self.region.can_reach(Region.dig_site),
                          self.region.can_reach(Region.gourmand_frog_cave),
                          self.region.can_reach(Region.colored_crystals_cave),
                          self.region.can_reach(Region.shipwreck), self.received(APWeapon.slingshot))
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
        return reach_entire_island & self.has(Fruit.banana) & self.has(gems) & self.ability.can_mine_perfectly() & \
               self.ability.can_fish_perfectly() & self.has(Furniture.flute_block) & self.has(Seed.melon) & self.has(Seed.wheat) & self.has(Seed.garlic)

    def has_everything(self, all_progression_items: Set[str]) -> StardewRule:
        all_regions = [region.name for region in vanilla_regions]
        rules = self.received(all_progression_items, len(all_progression_items)) & \
                self.region.can_reach_all(all_regions)
        return rules

    def has_prismatic_jelly_reward_access(self) -> StardewRule:
        if self.options.special_order_locations == SpecialOrderLocations.option_disabled:
            return self.special_order.can_complete_special_order("Prismatic Jelly")
        return self.received("Monster Musk Recipe")

    def has_all_rarecrows(self) -> StardewRule:
        rules = []
        for rarecrow_number in range(1, 9):
            rules.append(self.received(f"Rarecrow #{rarecrow_number}"))
        return And(rules)

    def has_abandoned_jojamart(self) -> StardewRule:
        return self.received(CommunityUpgrade.movie_theater, 1)

    def has_movie_theater(self) -> StardewRule:
        return self.received(CommunityUpgrade.movie_theater, 2)

    def can_use_obelisk(self, obelisk: str) -> StardewRule:
        return self.region.can_reach(Region.wizard_tower) & self.region.can_reach(Region.farm) & self.received(obelisk)

