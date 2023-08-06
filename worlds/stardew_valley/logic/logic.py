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
from .crop_logic import CropLogic
from .fishing_logic import FishingLogic
from .gift_logic import GiftLogic
from .mine_logic import MineLogic
from .money_logic import MoneyLogic
from .museum_logic import MuseumLogic
from .pet_logic import PetLogic
from .received_logic import ReceivedLogic
from .has_logic import HasLogic
from .region_logic import RegionLogic
from .relationship_logic import RelationshipLogic
from .season_logic import SeasonLogic
from .skill_logic import SkillLogic
from .special_order_logic import SpecialOrderLogic
from .time_logic import TimeLogic
from .tool_logic import ToolLogic
from .wallet_logic import WalletLogic
from ..mods.logic.mod_logic import ModLogic
from .. import options
from ..data import all_fish, FishItem, all_purchasable_seeds, SeedItem, all_crops
from ..data.bundle_data import BundleItem
from ..data.fish_data import island_fish
from ..data.museum_data import all_museum_items
from ..data.recipe_data import all_cooking_recipes
from ..options import StardewOptions
from ..regions import vanilla_regions
from ..stardew_rule import False_, Or, True_, Count, And, Has, StardewRule
from ..strings.animal_names import Animal, coop_animals, barn_animals
from ..strings.animal_product_names import AnimalProduct
from ..strings.ap_names.buff_names import Buff
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.calendar_names import Weekday
from ..strings.craftable_names import Craftable
from ..strings.crop_names import Fruit, Vegetable
from ..strings.fertilizer_names import Fertilizer
from ..strings.festival_check_names import FestivalCheck
from ..strings.fish_names import Fish, Trash, WaterItem
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
from ..strings.quest_names import Quest
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.seed_names import Seed
from ..strings.skill_names import Skill
from ..strings.tool_names import Tool, ToolMaterial
from ..strings.villager_names import NPC
from ..strings.wallet_item_names import Wallet
from ..strings.weapon_names import Weapon

MISSING_ITEM = "THIS ITEM IS MISSING"

fishing_regions = [Region.beach, Region.town, Region.forest, Region.mountain, Region.island_south, Region.island_west]


@dataclass(frozen=False, repr=False)
class StardewLogic:
    player: int
    options: StardewOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    sapling_rules: Dict[str, StardewRule] = field(default_factory=dict)
    tree_fruit_rules: Dict[str, StardewRule] = field(default_factory=dict)
    seed_rules: Dict[str, StardewRule] = field(default_factory=dict)
    cooking_rules: Dict[str, StardewRule] = field(default_factory=dict)
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
        self.season = SeasonLogic(self.player, self.options[options.SeasonRandomization], self.received, self.time)
        self.money = MoneyLogic(self.player, self.options[options.StartingMoney], self.region, self.time)
        self.action = ActionLogic(self.player, self.received, self.has, self.region)
        self.arcade = ArcadeLogic(self.player, self.options[options.ArcadeMachineLocations], self.received, self.region)
        self.artisan = ArtisanLogic(self.player, self.has, self.time)
        self.gifts = GiftLogic(self.player, self.has)
        tool_option = self.options[options.ToolProgression]
        skill_option = self.options[options.SkillProgression]
        elevator_option = self.options[options.ElevatorProgression]
        friendsanity_option = self.options[options.Friendsanity]
        heart_size_option = self.options[options.FriendsanityHeartSize]
        mods_option = self.options[options.Mods]
        self.buildings = BuildingLogic(self.player, self.options[options.BuildingProgression], self.received, self.has, self.region, self.money, mods_option)
        self.relationship = RelationshipLogic(self.player, friendsanity_option, heart_size_option,
                                              self.received, self.has, self.region, self.time, self.season, self.gifts, self.buildings, mods_option)
        self.museum = MuseumLogic(self.player, self.options[options.Museumsanity], self.received, self.has, self.region, self.action)
        self.wallet = WalletLogic(self.player, self.received, self.museum)
        self.combat = CombatLogic(self.player, self.received, self.region)
        self.tool = ToolLogic(self.player, tool_option, self.received, self.has, self.region, self.season, self.money)
        self.pet = PetLogic(self.player, friendsanity_option, heart_size_option, self.received, self.region, self.time, self.tool)
        self.crop = CropLogic(self.player, self.has, self.region, self.season, self.tool)
        self.skill = SkillLogic(self.player, skill_option, self.received, self.has, self.region, self.season, self.time, self.tool, self.combat, self.crop)
        self.fishing = FishingLogic(self.player, self.region, self.tool, self.skill)
        self.mine = MineLogic(self.player, tool_option, skill_option, elevator_option, self.received, self.region, self.combat,
                              self.tool, self.skill)
        self.cooking = CookingLogic(self.player, self.has, self.season, self.time, self.money, self.action, self.buildings, self.relationship, self.skill)
        self.ability = AbilityLogic(self.player, self.options[options.NumberOfMovementBuffs], self.options[options.NumberOfLuckBuffs], self.received,
                                    self.region, self.tool, self.skill, self.mine)
        self.special_order = SpecialOrderLogic(self.player, self.received, self.has, self.region, self.season, self.time, self.money, self.arcade, self.artisan,
                                               self.relationship, self.skill, self.mine, self.cooking, self.ability)

        self.mod = ModLogic(self.player, skill_option, elevator_option, mods_option, self.received, self.has, self.region, self.action, self.season, self.money,
                            self.relationship, self.buildings, self.wallet, self.combat, self.tool, self.skill, self.fishing, self.cooking, self.mine, self.ability)

        self.fish_rules.update({fish.name: self.can_catch_fish(fish) for fish in all_fish})
        self.museum_rules.update({donation.name: self.museum.can_find_museum_item(donation) for donation in all_museum_items})

        for recipe in all_cooking_recipes:
            can_cook_rule = self.cooking.can_cook(recipe)
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
            Seed.coffee: (self.season.has(Season.spring) | self.season.has(
                Season.summer)) & self.has_traveling_merchant(),
            Fruit.ancient_fruit: (self.received("Ancient Seeds") | self.received("Ancient Seeds Recipe")) &
                             self.region.can_reach(Region.greenhouse) & self.has(Machine.seed_maker),
        })

        self.item_rules.update({
            ArtisanGood.aged_roe: self.artisan.can_preserves_jar(AnimalProduct.roe),
            AnimalProduct.any_egg: self.has(AnimalProduct.chicken_egg) | self.has(AnimalProduct.duck_egg),
            Fish.any: Or([self.can_catch_fish(fish) for fish in all_fish]),
            Geode.artifact_trove: self.has(Geode.omni) & self.region.can_reach(Region.desert),
            Craftable.bait: (self.skill.has_level(Skill.fishing, 2) & self.has(Loot.bug_meat)) | self.has(Machine.worm_bin),
            Fertilizer.basic: (self.has(Material.sap) & self.skill.has_farming_level(1)) | (self.time.has_lived_months(1) & self.money.can_spend_at(Region.pierre_store, 100)),
            Fertilizer.quality: (self.skill.has_farming_level(9) & self.has(Material.sap) & self.has(Fish.any)) | (self.time.has_year_two() & self.money.can_spend_at(Region.pierre_store, 150)),
            Fertilizer.deluxe: False_(),
            # self.received("Deluxe Fertilizer Recipe") & self.has(MetalBar.iridium) & self.has(SVItem.sap),
            Fertilizer.tree: self.skill.has_level(Skill.foraging, 7) & self.has(Material.fiber) & self.has(Material.stone),
            Loot.bat_wing: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern(),
            ArtisanGood.battery_pack: (self.has(Machine.lightning_rod) & self.season.has_any_not_winter()) | self.has(Machine.solar_panel),
            Machine.bee_house: self.skill.has_farming_level(3) & self.has(MetalBar.iron) & self.has(ArtisanGood.maple_syrup) & self.has(Material.coal) & self.has(Material.wood),
            Beverage.beer: self.artisan.can_keg(Vegetable.wheat) | self.money.can_spend_at(Region.saloon, 400),
            Forageable.blackberry: self.tool.can_forage(Season.fall),
            Craftable.bomb: self.skill.has_level(Skill.mining, 6) & self.has(Material.coal) & self.has(Ore.iron),
            Fossil.bone_fragment: self.region.can_reach(Region.dig_site),
            Gift.bouquet: self.relationship.has_hearts(Generic.bachelor, 8) & self.money.can_spend_at(Region.pierre_store, 100),
            Meal.bread: self.money.can_spend_at(Region.saloon, 120),
            Trash.broken_cd: self.skill.can_crab_pot(),
            Trash.broken_glasses: self.skill.can_crab_pot(),
            Loot.bug_meat: self.mine.can_mine_in_the_mines_floor_1_40(),
            Forageable.cactus_fruit: self.tool.can_forage(Generic.any, Region.desert),
            Machine.cask: self.buildings.has_house(3) & self.region.can_reach(Region.cellar) & self.has(Material.wood) & self.has(Material.hardwood),
            Forageable.cave_carrot: self.tool.can_forage(Generic.any, Region.mines_floor_10, True),
            ArtisanGood.caviar: self.artisan.can_preserves_jar(AnimalProduct.sturgeon_roe),
            Forageable.chanterelle: self.tool.can_forage(Season.fall, Region.secret_woods),
            Machine.cheese_press: self.skill.has_farming_level(6) & self.has(Material.wood) & self.has(Material.stone) & self.has(Material.hardwood) & self.has(MetalBar.copper),
            ArtisanGood.cheese: (self.has(AnimalProduct.cow_milk) & self.has(Machine.cheese_press)) | (self.region.can_reach(Region.desert) & self.has(Mineral.emerald)),
            Craftable.cherry_bomb: self.skill.has_level(Skill.mining, 1) & self.has(Material.coal) & self.has(Ore.copper),
            Animal.chicken: self.can_buy_animal(Animal.chicken),
            AnimalProduct.chicken_egg: self.has([AnimalProduct.egg, AnimalProduct.brown_egg, AnimalProduct.large_egg, AnimalProduct.large_brown_egg], 1),
            Material.cinder_shard: self.region.can_reach(Region.volcano_floor_5),
            WaterItem.clam: self.tool.can_forage(Generic.any, Region.beach),
            Material.clay: self.region.can_reach_any([Region.farm, Region.beach, Region.quarry]) & self.tool.has_tool(Tool.hoe),
            ArtisanGood.cloth: (self.has(AnimalProduct.wool) & self.has(Machine.loom)) | (self.region.can_reach(Region.desert) & self.has(Mineral.aquamarine)),
            Material.coal: self.mine.can_mine_in_the_mines_floor_41_80() | self.action.can_do_panning(),
            WaterItem.cockle: self.tool.can_forage(Generic.any, Region.beach),
            Forageable.coconut: self.tool.can_forage(Generic.any, Region.desert),
            Beverage.coffee: self.artisan.can_keg(Seed.coffee) | self.has(Machine.coffee_maker) | (self.money.can_spend_at(Region.saloon, 300)) | self.has("Hot Java Ring"),
            Machine.coffee_maker: self.received(Machine.coffee_maker),
            Forageable.common_mushroom: self.tool.can_forage(Season.fall) | (self.tool.can_forage(Season.spring, Region.secret_woods)),
            MetalBar.copper: self.can_smelt(Ore.copper),
            Ore.copper: self.mine.can_mine_in_the_mines_floor_1_40() | self.mine.can_mine_in_the_skull_cavern() | self.action.can_do_panning(),
            WaterItem.coral: self.tool.can_forage(Generic.any, Region.tide_pools) | self.tool.can_forage(Season.summer, Region.beach),
            Animal.cow: self.can_buy_animal(Animal.cow),
            AnimalProduct.cow_milk: self.has(AnimalProduct.milk) | self.has(AnimalProduct.large_milk),
            Fish.crab: self.skill.can_crab_pot(Region.beach),
            Machine.crab_pot: self.skill.has_level(Skill.fishing, 3) & (self.money.can_spend_at(Region.fish_shop, 1500) | (self.has(MetalBar.iron) & self.has(Material.wood))),
            Fish.crayfish: self.skill.can_crab_pot(Region.town),
            Forageable.crocus: self.tool.can_forage(Season.winter),
            Forageable.crystal_fruit: self.tool.can_forage(Season.winter),
            Forageable.daffodil: self.tool.can_forage(Season.spring),
            Forageable.dandelion: self.tool.can_forage(Season.spring),
            Animal.dinosaur: self.buildings.has_building(Building.big_coop) & self.has(AnimalProduct.dinosaur_egg),
            Forageable.dragon_tooth: self.tool.can_forage(Generic.any, Region.volcano_floor_10),
            "Dried Starfish": self.skill.can_fish() & self.region.can_reach(Region.beach),
            Trash.driftwood: self.skill.can_crab_pot(),
            AnimalProduct.duck_egg: self.has_animal(Animal.duck),
            AnimalProduct.duck_feather: self.has_happy_animal(Animal.duck),
            Animal.duck: self.can_buy_animal(Animal.duck),
            AnimalProduct.egg: self.has_animal(Animal.chicken),
            AnimalProduct.brown_egg: self.has_animal(Animal.chicken),
            "Energy Tonic": self.region.can_reach(Region.hospital) & self.money.can_spend(1000),
            Material.fiber: True_(),
            Forageable.fiddlehead_fern: self.tool.can_forage(Season.summer, Region.secret_woods),
            "Magic Rock Candy": self.region.can_reach(Region.desert) & self.has("Prismatic Shard"),
            "Fishing Chest": self.fishing.can_fish_chests(),
            Craftable.flute_block: self.relationship.has_hearts(NPC.robin, 6) & self.region.can_reach(Region.carpenter) & self.has(Material.wood) & self.has(Ore.copper) & self.has(Material.fiber),
            Geode.frozen: self.mine.can_mine_in_the_mines_floor_41_80(),
            Machine.furnace: self.has(Material.stone) & self.has(Ore.copper),
            Geode.geode: self.mine.can_mine_in_the_mines_floor_1_40(),
            Forageable.ginger: self.tool.can_forage(Generic.any, Region.island_west, True),
            ArtisanGood.goat_cheese: self.has(AnimalProduct.goat_milk) & self.has(Machine.cheese_press),
            AnimalProduct.goat_milk: self.has(Animal.goat),
            Animal.goat: self.can_buy_animal(Animal.goat),
            MetalBar.gold: self.can_smelt(Ore.gold),
            Ore.gold: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern() | self.action.can_do_panning(),
            Geode.golden_coconut: self.region.can_reach(Region.island_north),
            Gift.golden_pumpkin: self.season.has(Season.fall) | self.action.can_open_geode(Geode.artifact_trove),
            WaterItem.green_algae: self.fishing.can_fish_in_freshwater(),
            ArtisanGood.green_tea: self.artisan.can_keg(Vegetable.tea_leaves),
            Material.hardwood: self.tool.has_tool(Tool.axe, ToolMaterial.copper) & (self.region.can_reach(Region.secret_woods) | self.region.can_reach(Region.island_south)),
            Forageable.hay: self.buildings.has_building(Building.silo) & self.tool.has_tool(Tool.scythe),
            Forageable.hazelnut: self.tool.can_forage(Season.fall),
            Forageable.holly: self.tool.can_forage(Season.winter),
            ArtisanGood.honey: self.money.can_spend_at(Region.oasis, 200) | (self.has(Machine.bee_house) & self.season.has_any_not_winter()),
            "Hot Java Ring": self.region.can_reach(Region.volcano_floor_10),
            Meal.ice_cream: (self.season.has(Season.summer) & self.money.can_spend_at(Region.town, 250)) | self.money.can_spend_at(Region.oasis, 240),
            # | (self.ability.can_cook() & self.relationship.has_hearts(NPC.jodi, 7) & self.has(AnimalProduct.cow_milk) & self.has(Ingredient.sugar)),
            MetalBar.iridium: self.can_smelt(Ore.iridium),
            Ore.iridium: self.mine.can_mine_in_the_skull_cavern(),
            MetalBar.iron: self.can_smelt(Ore.iron),
            Ore.iron: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern() | self.action.can_do_panning(),
            ArtisanGood.jelly: self.artisan.has_jelly(),
            Trash.joja_cola: self.money.can_spend_at(Region.saloon, 75),
            "JotPK Small Buff": self.arcade.has_jotpk_power_level(2),
            "JotPK Medium Buff": self.arcade.has_jotpk_power_level(4),
            "JotPK Big Buff": self.arcade.has_jotpk_power_level(7),
            "JotPK Max Buff": self.arcade.has_jotpk_power_level(9),
            ArtisanGood.juice: self.artisan.has_juice(),
            "Junimo Kart Small Buff": self.arcade.has_junimo_kart_power_level(2),
            "Junimo Kart Medium Buff": self.arcade.has_junimo_kart_power_level(4),
            "Junimo Kart Big Buff": self.arcade.has_junimo_kart_power_level(6),
            "Junimo Kart Max Buff": self.arcade.has_junimo_kart_power_level(8),
            Machine.keg: self.skill.has_farming_level(8) & self.has(Material.wood) & self.has(MetalBar.iron) & self.has(MetalBar.copper) & self.has(ArtisanGood.oak_resin),
            AnimalProduct.large_egg: self.has_happy_animal(Animal.chicken),
            AnimalProduct.large_brown_egg: self.has_happy_animal(Animal.chicken),
            AnimalProduct.large_goat_milk: self.has_happy_animal(Animal.goat),
            AnimalProduct.large_milk: self.has_happy_animal(Animal.cow),
            Forageable.leek: self.tool.can_forage(Season.spring),
            Craftable.life_elixir: self.skill.has_level(Skill.combat, 2) & self.has(Forageable.red_mushroom) & self.has(Forageable.purple_mushroom) & self.has(Forageable.morel) & self.has(Forageable.chanterelle),
            Machine.lightning_rod: self.skill.has_level(Skill.foraging, 6) & self.has(MetalBar.iron) & self.has(MetalBar.quartz) & self.has(Loot.bat_wing),
            Fish.lobster: self.skill.can_crab_pot(Region.beach),
            Machine.loom: self.skill.has_farming_level(7) & self.has(Material.wood) & self.has(Material.fiber) & self.has(ArtisanGood.pine_tar),
            Forageable.magma_cap: self.tool.can_forage(Generic.any, Region.volcano_floor_5),
            Geode.magma: self.mine.can_mine_in_the_mines_floor_81_120() | (self.has(Fish.lava_eel) & self.buildings.has_building(Building.fish_pond)),
            ArtisanGood.maple_syrup: self.has(Machine.tapper),
            ArtisanGood.mayonnaise: self.has(Machine.mayonnaise_machine) & self.has(AnimalProduct.chicken_egg),
            Machine.mayonnaise_machine: self.skill.has_farming_level(2) & self.has(Material.wood) & self.has(Material.stone) & self.has("Earth Crystal") & self.has(MetalBar.copper),
            ArtisanGood.mead: self.artisan.can_keg(ArtisanGood.honey),
            Craftable.mega_bomb: self.skill.has_level(Skill.mining, 8) & self.has(Ore.gold) & self.has(Loot.solar_essence) & self.has(Loot.void_essence),
            Gift.mermaid_pendant: self.region.can_reach(Region.tide_pools) & self.relationship.has_hearts(Generic.bachelor, 10) & self.buildings.has_house(1) & self.has(Craftable.rain_totem),
            AnimalProduct.milk: self.has_animal(Animal.cow),
            Craftable.monster_musk: self.has_prismatic_jelly_reward_access() & self.has(Loot.slime) & self.has(Loot.bat_wing),
            Forageable.morel: self.tool.can_forage(Season.spring, Region.secret_woods),
            "Muscle Remedy": self.region.can_reach(Region.hospital) & self.money.can_spend(1000),
            Fish.mussel: self.tool.can_forage(Generic.any, Region.beach) or self.has(Fish.mussel_node),
            Fish.mussel_node: self.region.can_reach(Region.island_west),
            WaterItem.nautilus_shell: self.tool.can_forage(Season.winter, Region.beach),
            ArtisanGood.oak_resin: self.has(Machine.tapper),
            Ingredient.oil: self.money.can_spend_at(Region.pierre_store, 200) | (self.has(Machine.oil_maker) & (self.has(Vegetable.corn) | self.has(Flower.sunflower) | self.has(Seed.sunflower))),
            Machine.oil_maker: self.skill.has_farming_level(8) & self.has(Loot.slime) & self.has(Material.hardwood) & self.has(MetalBar.gold),
            Craftable.oil_of_garlic: (self.skill.has_level(Skill.combat, 6) & self.has(Vegetable.garlic) & self.has(Ingredient.oil)) | (self.money.can_spend_at(Region.mines_dwarf_shop, 3000)),
            Geode.omni: self.mine.can_mine_in_the_mines_floor_41_80() | self.region.can_reach(Region.desert) | self.action.can_do_panning() | self.received(Wallet.rusty_key) | (self.has(Fish.octopus) & self.buildings.has_building(Building.fish_pond)) | self.region.can_reach(Region.volcano_floor_10),
            Animal.ostrich: self.buildings.has_building(Building.barn) & self.has(AnimalProduct.ostrich_egg) & self.has(Machine.ostrich_incubator),
            AnimalProduct.ostrich_egg: self.tool.can_forage(Generic.any, Region.island_north, True),
            Machine.ostrich_incubator: self.received("Ostrich Incubator Recipe") & self.has(Fossil.bone_fragment) & self.has(Material.hardwood) & self.has(Material.cinder_shard),
            Fish.oyster: self.tool.can_forage(Generic.any, Region.beach),
            ArtisanGood.pale_ale: self.artisan.can_keg(Vegetable.hops),
            Gift.pearl: (self.has(Fish.blobfish) & self.buildings.has_building(Building.fish_pond)) | self.action.can_open_geode(Geode.artifact_trove),
            Fish.periwinkle: self.skill.can_crab_pot(Region.town),
            ArtisanGood.pickles: self.artisan.has_pickle(),
            Animal.pig: self.can_buy_animal(Animal.pig),
            Beverage.pina_colada: self.money.can_spend_at(Region.island_resort, 600),
            ArtisanGood.pine_tar: self.has(Machine.tapper),
            Meal.pizza: self.money.can_spend_at(Region.saloon, 600),
            Machine.preserves_jar: self.skill.has_farming_level(4) & self.has(Material.wood) & self.has(Material.stone) & self.has(Material.coal),
            Forageable.purple_mushroom: self.tool.can_forage(Generic.any, Region.mines_floor_95) | self.tool.can_forage(Generic.any, Region.skull_cavern_25),
            Animal.rabbit: self.can_buy_animal(Animal.rabbit),
            AnimalProduct.rabbit_foot: self.has_happy_animal(Animal.rabbit),
            MetalBar.radioactive: self.can_smelt(Ore.radioactive),
            Ore.radioactive: self.ability.can_mine_perfectly() & self.region.can_reach(Region.qi_walnut_room),
            Forageable.rainbow_shell: self.tool.can_forage(Season.summer, Region.beach),
            Craftable.rain_totem: self.skill.has_level(Skill.foraging, 9) & self.has(Material.hardwood) & self.has(ArtisanGood.truffle_oil) & self.has(ArtisanGood.pine_tar),
            Machine.recycling_machine: self.skill.has_level(Skill.fishing, 4) & self.has(Material.wood) & self.has(Material.stone) & self.has(MetalBar.iron),
            Forageable.red_mushroom: self.tool.can_forage(Season.summer, Region.secret_woods) | self.tool.can_forage(Season.fall, Region.secret_woods),
            MetalBar.quartz: self.can_smelt("Quartz") | self.can_smelt("Fire Quartz") |
                              (self.has(Machine.recycling_machine) & (self.has(Trash.broken_cd) | self.has(Trash.broken_glasses))),
            Ingredient.rice: self.money.can_spend_at(Region.pierre_store, 200) | (
                    self.buildings.has_building(Building.mill) & self.has(Vegetable.unmilled_rice)),
            AnimalProduct.roe: self.skill.can_fish() & self.buildings.has_building(Building.fish_pond),
            Meal.salad: self.money.can_spend_at(Region.saloon, 220),
            # | (self.ability.can_cook() & self.relationship.has_hearts(NPC.emily, 3) & self.has(Forageable.leek) & self.has(Forageable.dandelion) &
            # self.has(Ingredient.vinegar)),
            Forageable.salmonberry: self.tool.can_forage(Season.spring),
            Material.sap: self.ability.can_chop_trees(),
            Craftable.scarecrow: self.skill.has_farming_level(1) & self.has(Material.wood) & self.has(Material.coal) & self.has(Material.fiber),
            WaterItem.sea_urchin: self.tool.can_forage(Generic.any, Region.tide_pools),
            WaterItem.seaweed: (self.skill.can_fish() & self.region.can_reach(Region.beach)) | self.region.can_reach(
                Region.tide_pools),
            Forageable.secret_note: self.received(Wallet.magnifying_glass) & (self.ability.can_chop_trees() | self.mine.can_mine_in_the_mines_floor_1_40()),
            Machine.seed_maker: self.skill.has_farming_level(9) & self.has(Material.wood) & self.has(MetalBar.gold) & self.has(
                Material.coal),
            Animal.sheep: self.can_buy_animal(Animal.sheep),
            Fish.shrimp: self.skill.can_crab_pot(Region.beach),
            Loot.slime: self.mine.can_mine_in_the_mines_floor_1_40(),
            Weapon.any_slingshot: self.received(Weapon.slingshot) | self.received(Weapon.master_slingshot),
            Fish.snail: self.skill.can_crab_pot(Region.town),
            Forageable.snow_yam: self.tool.can_forage(Season.winter, Region.beach, True),
            Trash.soggy_newspaper: self.skill.can_crab_pot(),
            Loot.solar_essence: self.mine.can_mine_in_the_mines_floor_41_80() | self.mine.can_mine_in_the_skull_cavern(),
            Machine.solar_panel: self.received("Solar Panel Recipe") & self.has(MetalBar.quartz) & self.has(
                MetalBar.iron) & self.has(MetalBar.gold),
            Meal.spaghetti: self.money.can_spend_at(Region.saloon, 240),
            Forageable.spice_berry: self.tool.can_forage(Season.summer),
            Forageable.spring_onion: self.tool.can_forage(Season.spring),
            AnimalProduct.squid_ink: self.mine.can_mine_in_the_mines_floor_81_120() | (self.buildings.has_building(Building.fish_pond) & self.has(Fish.squid)),
            Craftable.staircase: self.skill.has_level(Skill.mining, 2) & self.has(Material.stone),
            Material.stone: self.tool.has_tool(Tool.pickaxe),
            Meal.strange_bun: self.relationship.has_hearts(NPC.shane, 7) & self.has(Ingredient.wheat_flour) & self.has(Fish.periwinkle) & self.has(ArtisanGood.void_mayonnaise),
            AnimalProduct.sturgeon_roe: self.has(Fish.sturgeon) & self.buildings.has_building(Building.fish_pond),
            Ingredient.sugar: self.money.can_spend_at(Region.pierre_store, 100) | (
                    self.buildings.has_building(Building.mill) & self.has(Vegetable.beet)),
            Forageable.sweet_pea: self.tool.can_forage(Season.summer),
            Machine.tapper: self.skill.has_level(Skill.foraging, 3) & self.has(Material.wood) & self.has(MetalBar.copper),
            Vegetable.tea_leaves: self.has(Sapling.tea) & self.time.has_lived_months(2) & self.season.has_any_not_winter(),
            Sapling.tea: self.relationship.has_hearts(NPC.caroline, 2) & self.has(Material.fiber) & self.has(Material.wood),
            Trash.trash: self.skill.can_crab_pot(),
            Beverage.triple_shot_espresso: self.has("Hot Java Ring"),
            ArtisanGood.truffle_oil: self.has(AnimalProduct.truffle) & self.has(Machine.oil_maker),
            AnimalProduct.truffle: self.has_animal(Animal.pig) & self.season.has_any_not_winter(),
            Ingredient.vinegar: self.money.can_spend_at(Region.pierre_store, 200),
            AnimalProduct.void_egg: self.money.can_spend_at(Region.sewer, 5000) | (self.buildings.has_building(Building.fish_pond) & self.has(Fish.void_salmon)),
            Loot.void_essence: self.mine.can_mine_in_the_mines_floor_81_120() | self.mine.can_mine_in_the_skull_cavern(),
            ArtisanGood.void_mayonnaise: (self.region.can_reach(Region.witch_swamp) & self.skill.can_fish()) | (self.has(Machine.mayonnaise_machine) & self.has(AnimalProduct.void_egg)),
            Ingredient.wheat_flour: self.money.can_spend_at(Region.pierre_store, 100) |
                                    (self.buildings.has_building(Building.mill) & self.has(Vegetable.wheat)),
            WaterItem.white_algae: self.skill.can_fish() & self.region.can_reach(Region.mines_floor_20),
            Forageable.wild_horseradish: self.tool.can_forage(Season.spring),
            Forageable.wild_plum: self.tool.can_forage(Season.fall),
            Gift.wilted_bouquet: self.has(Machine.furnace) & self.has(Gift.bouquet) & self.has(Material.coal),
            ArtisanGood.wine: self.artisan.has_wine(),
            Forageable.winter_root: self.tool.can_forage(Season.winter, Region.forest, True),
            Material.wood: self.tool.has_tool(Tool.axe),
            AnimalProduct.wool: self.has_animal(Animal.rabbit) | self.has_animal(Animal.sheep),
            Machine.worm_bin: self.skill.has_level(Skill.fishing, 8) & self.has(Material.hardwood) & self.has(MetalBar.gold) & self.has(MetalBar.iron) & self.has(Material.fiber),
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
            FestivalCheck.egg_hunt: self.season.has(Season.spring) & self.region.can_reach(Region.town) & self.can_win_egg_hunt(),
            FestivalCheck.strawberry_seeds: self.season.has(Season.spring) & self.region.can_reach(Region.town) & self.money.can_spend(1000),
            FestivalCheck.dance: self.season.has(Season.spring) & self.region.can_reach(Region.forest) & self.relationship.has_hearts(Generic.bachelor, 4),
            FestivalCheck.rarecrow_5: self.season.has(Season.spring) & self.region.can_reach(Region.forest) & self.money.can_spend(2500),
            FestivalCheck.luau_soup: self.season.has(Season.summer) & self.region.can_reach(Region.beach) & self.can_succeed_luau_soup(),
            FestivalCheck.moonlight_jellies: self.season.has(Season.summer) & self.region.can_reach(Region.beach),
            FestivalCheck.smashing_stone: self.season.has(Season.fall) & self.region.can_reach(Region.town),
            FestivalCheck.grange_display: self.season.has(Season.fall) & self.region.can_reach(Region.town) & self.can_succeed_grange_display(),
            FestivalCheck.rarecrow_1: self.season.has(Season.fall) & self.region.can_reach(Region.town),  # only cost star tokens
            FestivalCheck.fair_stardrop: self.season.has(Season.fall) & self.region.can_reach(Region.town),  # only cost star tokens
            FestivalCheck.spirit_eve_maze: self.season.has(Season.fall) & self.region.can_reach(Region.town),
            FestivalCheck.rarecrow_2: self.season.has(Season.fall) & self.region.can_reach(Region.town) & self.money.can_spend(5000),
            FestivalCheck.fishing_competition: self.season.has(Season.winter) & self.region.can_reach(Region.forest) & self.can_win_fishing_competition(),
            FestivalCheck.rarecrow_4: self.season.has(Season.winter) & self.region.can_reach(Region.forest) & self.money.can_spend(5000),
            FestivalCheck.mermaid_pearl: self.season.has(Season.winter) & self.region.can_reach(Region.beach),
            FestivalCheck.cone_hat: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(2500),
            FestivalCheck.iridium_fireplace: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(15000),
            FestivalCheck.rarecrow_7: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(5000) & self.museum.can_find_museum_artifacts(20),
            FestivalCheck.rarecrow_8: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(5000) & self.museum.can_find_museum_items(40),
            FestivalCheck.lupini_red_eagle: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(1200),
            FestivalCheck.lupini_portrait_mermaid: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(1200),
            FestivalCheck.lupini_solar_kingdom: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.money.can_spend(1200),
            FestivalCheck.lupini_clouds: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.time.has_year_two() & self.money.can_spend(1200),
            FestivalCheck.lupini_1000_years: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.time.has_year_two() & self.money.can_spend(1200),
            FestivalCheck.lupini_three_trees: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.time.has_year_two() & self.money.can_spend(1200),
            FestivalCheck.lupini_the_serpent: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.time.has_year_three() & self.money.can_spend(1200),
            FestivalCheck.lupini_tropical_fish: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.time.has_year_three() & self.money.can_spend(1200),
            FestivalCheck.lupini_land_of_clay: self.season.has(Season.winter) & self.region.can_reach(Region.beach) & self.time.has_year_three() & self.money.can_spend(1200),
            FestivalCheck.secret_santa: self.season.has(Season.winter) & self.region.can_reach(Region.town) & self.gifts.has_any_universal_love(),
            FestivalCheck.legend_of_the_winter_star: self.season.has(Season.winter) & self.region.can_reach(Region.town),
            FestivalCheck.all_rarecrows: self.region.can_reach(Region.farm) & self.has_all_rarecrows(),
        })

        self.special_order.initialize_rules()
        self.special_order.update_rules(self.mod.special_orders.get_modded_special_orders_rules(self.special_order.special_order_rules))

    def can_complete_quest(self, quest: str) -> StardewRule:
        return Has(quest, self.quest_rules)

    def can_buy_seed(self, seed: SeedItem) -> StardewRule:
        if self.options[options.Cropsanity] == options.Cropsanity.option_disabled:
            item_rule = True_()
        else:
            item_rule = self.received(seed.name)
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
        if self.options[options.Cropsanity] == options.Cropsanity.option_disabled:
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
        region_rule = self.region.can_reach_any(fish.locations)
        season_rule = self.season.has_any(fish.seasons)
        if fish.difficulty == -1:
            difficulty_rule = self.skill.can_crab_pot()
        else:
            difficulty_rule = self.skill.can_fish(fish.difficulty)
        return region_rule & season_rule & difficulty_rule

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.skill.has_level(Skill.fishing, 10), self.tool.has_fishing_rod(4)]
        for fish in all_fish:
            if self.options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true and \
                    fish in island_fish:
                continue
            rules.append(self.can_catch_fish(fish))
        return And(rules)

    def can_smelt(self, item: str) -> StardewRule:
        return self.has(Machine.furnace) & self.has(item)

    def has_traveling_merchant(self, tier: int = 1):
        traveling_merchant_days = [f"Traveling Merchant: {day}" for day in Weekday.all_days]
        return self.received(traveling_merchant_days, tier)

    def can_complete_bundle(self, bundle_requirements: List[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        highest_quality_yet = 0
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return self.money.can_spend(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
                if bundle_item.quality > highest_quality_yet:
                    highest_quality_yet = bundle_item.quality
        return self.has(item_rules, number_required) & self.can_grow_gold_quality(highest_quality_yet)

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
        dig_site = self.region.can_reach(Region.dig_site)
        tools = self.tool.has_tool(Tool.pickaxe) & self.tool.has_tool(Tool.hoe) & self.tool.has_tool(Tool.scythe)
        leg_and_snake_skull = dig_site
        ribs_and_spine = self.region.can_reach(Region.island_south)
        skull = self.action.can_open_geode(Geode.golden_coconut)
        tail = self.action.can_do_panning() & dig_site
        frog = self.region.can_reach(Region.island_east)
        bat = self.region.can_reach(Region.volcano_floor_5)
        snake_vertebrae = self.region.can_reach(Region.island_west)
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
                               # Completing the museum not expected
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
                               self.wallet.has_rusty_key(),  # Rusty key not expected
                               ]
        return Count(12, rules_worth_a_point)

    def can_win_egg_hunt(self) -> StardewRule:
        number_of_movement_buffs: int = self.options[options.NumberOfMovementBuffs]
        if self.options[options.FestivalLocations] == options.FestivalLocations.option_hard or number_of_movement_buffs < 2:
            return True_()
        return self.received(Buff.movement, number_of_movement_buffs // 2)

    def can_succeed_luau_soup(self) -> StardewRule:
        if self.options[options.FestivalLocations] != options.FestivalLocations.option_hard:
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
        if self.options[options.FestivalLocations] != options.FestivalLocations.option_hard:
            return True_()
        animal_rule = self.has_animal(Generic.any)
        artisan_rule = self.artisan.can_keg(Generic.any) | self.artisan.can_preserves_jar(Generic.any)
        cooking_rule = True_()  # Salads at the bar are good enough
        fish_rule = self.skill.can_fish(50)
        forage_rule = True_()  # Hazelnut always available since the grange display is in fall
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
        return self.skill.can_fish(60)

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
        if self.options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
            return False_()
        return self.region.can_reach(Region.island_trader)

    def has_walnut(self, number: int) -> StardewRule:
        if self.options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
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
                          self.region.can_reach(Region.shipwreck), self.has(Weapon.any_slingshot))
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
               self.ability.can_fish_perfectly() & self.has(Craftable.flute_block) & self.has(Seed.melon) & self.has(Seed.wheat) & self.has(Seed.garlic)

    def has_everything(self, all_progression_items: Set[str]) -> StardewRule:
        all_regions = [region.name for region in vanilla_regions]
        rules = self.received(all_progression_items, len(all_progression_items)) & \
                self.region.can_reach_all(all_regions)
        return rules

    def has_prismatic_jelly_reward_access(self) -> StardewRule:
        if self.options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_disabled:
            return self.special_order.can_complete_special_order("Prismatic Jelly")
        return self.received("Monster Musk Recipe")

    def has_all_rarecrows(self) -> StardewRule:
        rules = []
        for rarecrow_number in range(1, 9):
            rules.append(self.received(f"Rarecrow #{rarecrow_number}"))
        return And(rules)

