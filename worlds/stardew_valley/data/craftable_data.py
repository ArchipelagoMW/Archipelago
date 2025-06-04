from typing import Dict, List, Optional

from .recipe_source import RecipeSource, StarterSource, QueenOfSauceSource, ShopSource, SkillSource, FriendshipSource, ShopTradeSource, CutsceneSource, \
    ArchipelagoSource, LogicSource, SpecialOrderSource, FestivalShopSource, QuestSource, MasterySource, SkillCraftsanitySource
from ..mods.mod_data import ModNames
from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.craftable_names import Bomb, Fence, Sprinkler, WildSeeds, Floor, Fishing, Ring, Consumable, Edible, Lighting, Storage, Furniture, Sign, \
    Craftable, \
    ModEdible, ModCraftable, ModMachine, ModFloor, ModConsumable, Statue
from ..strings.crop_names import Fruit, Vegetable
from ..strings.currency_names import Currency
from ..strings.fertilizer_names import Fertilizer, RetainingSoil, SpeedGro
from ..strings.fish_names import Fish, WaterItem, ModTrash, Trash
from ..strings.flower_names import Flower
from ..strings.food_names import Meal
from ..strings.forageable_names import Forageable, DistantLandsForageable, Mushroom
from ..strings.gift_names import Gift
from ..strings.ingredient_names import Ingredient
from ..strings.machine_names import Machine
from ..strings.material_names import Material
from ..strings.metal_names import Ore, MetalBar, Fossil, Artifact, Mineral, ModFossil
from ..strings.monster_drop_names import Loot, ModLoot
from ..strings.quest_names import Quest
from ..strings.region_names import Region, SVERegion, LogicRegion
from ..strings.seed_names import Seed, TreeSeed
from ..strings.skill_names import Skill, ModSkill
from ..strings.special_order_names import SpecialOrder
from ..strings.villager_names import NPC, ModNPC


class CraftingRecipe:
    item: str
    ingredients: Dict[str, int]
    source: RecipeSource
    mod_name: Optional[str]

    def __init__(self, item: str, ingredients: Dict[str, int], source: RecipeSource, mod_name: Optional[str] = None):
        self.item = item
        self.ingredients = ingredients
        self.source = source
        self.mod_name = mod_name

    def __repr__(self):
        return f"{self.item} (Source: {self.source} |" \
               f" Ingredients: {self.ingredients})"


all_crafting_recipes: List[CraftingRecipe] = []


def friendship_recipe(name: str, friend: str, hearts: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CraftingRecipe:
    source = FriendshipSource(friend, hearts)
    return create_recipe(name, ingredients, source, mod_name)


def cutscene_recipe(name: str, region: str, friend: str, hearts: int, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = CutsceneSource(region, friend, hearts)
    return create_recipe(name, ingredients, source)


def skill_recipe(name: str, skill: str, level: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CraftingRecipe:
    source = SkillSource(skill, level)
    return create_recipe(name, ingredients, source, mod_name)


def skill_craftsanity_recipe(name: str, skill: str, level: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CraftingRecipe:
    source = SkillCraftsanitySource(skill, level)
    return create_recipe(name, ingredients, source, mod_name)


def mastery_recipe(name: str, skill: str, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CraftingRecipe:
    source = MasterySource(skill)
    return create_recipe(name, ingredients, source, mod_name)


def shop_recipe(name: str, region: str, price: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CraftingRecipe:
    source = ShopSource(region, price)
    return create_recipe(name, ingredients, source, mod_name)


def festival_shop_recipe(name: str, region: str, price: int, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = FestivalShopSource(region, price)
    return create_recipe(name, ingredients, source)


def shop_trade_recipe(name: str, region: str, currency: str, price: int, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = ShopTradeSource(region, currency, price)
    return create_recipe(name, ingredients, source)


def queen_of_sauce_recipe(name: str, year: int, season: str, day: int, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = QueenOfSauceSource(year, season, day)
    return create_recipe(name, ingredients, source)


def quest_recipe(name: str, quest: str, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = QuestSource(quest)
    return create_recipe(name, ingredients, source)


def special_order_recipe(name: str, special_order: str, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = SpecialOrderSource(special_order)
    return create_recipe(name, ingredients, source)


def starter_recipe(name: str, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = StarterSource()
    return create_recipe(name, ingredients, source)


def ap_recipe(name: str, ingredients: Dict[str, int], ap_item: str = None) -> CraftingRecipe:
    if ap_item is None:
        ap_item = f"{name} Recipe"
    source = ArchipelagoSource(ap_item)
    return create_recipe(name, ingredients, source)


def cellar_recipe(name: str, ingredients: Dict[str, int]) -> CraftingRecipe:
    source = LogicSource("Cellar")
    return create_recipe(name, ingredients, source)


def create_recipe(name: str, ingredients: Dict[str, int], source: RecipeSource, mod_name: Optional[str] = None) -> CraftingRecipe:
    recipe = CraftingRecipe(name, ingredients, source, mod_name)
    all_crafting_recipes.append(recipe)
    return recipe


cherry_bomb = skill_recipe(Bomb.cherry_bomb, Skill.mining, 1, {Ore.copper: 4, Material.coal: 1})
bomb = skill_recipe(Bomb.bomb, Skill.mining, 6, {Ore.iron: 4, Material.coal: 1})
mega_bomb = skill_recipe(Bomb.mega_bomb, Skill.mining, 8, {Ore.gold: 4, Loot.solar_essence: 1, Loot.void_essence: 1})

gate = starter_recipe(Fence.gate, {Material.wood: 10})
wood_fence = starter_recipe(Fence.wood, {Material.wood: 2})
stone_fence = skill_recipe(Fence.stone, Skill.farming, 2, {Material.stone: 2})
iron_fence = skill_recipe(Fence.iron, Skill.farming, 4, {MetalBar.iron: 2})
hardwood_fence = skill_recipe(Fence.hardwood, Skill.farming, 6, {Material.hardwood: 2})

sprinkler = skill_recipe(Sprinkler.basic, Skill.farming, 2, {MetalBar.copper: 1, MetalBar.iron: 1})
quality_sprinkler = skill_recipe(Sprinkler.quality, Skill.farming, 6, {MetalBar.iron: 1, MetalBar.gold: 1, MetalBar.quartz: 1})
iridium_sprinkler = skill_recipe(Sprinkler.iridium, Skill.farming, 9, {MetalBar.gold: 1, MetalBar.iridium: 1, ArtisanGood.battery_pack: 1})

bee_house = skill_recipe(Machine.bee_house, Skill.farming, 3, {Material.wood: 40, Material.coal: 8, MetalBar.iron: 1, ArtisanGood.maple_syrup: 1})
cask = cellar_recipe(Machine.cask, {Material.wood: 40, Material.hardwood: 1})
cheese_press = skill_recipe(Machine.cheese_press, Skill.farming, 6, {Material.wood: 45, Material.stone: 45, Material.hardwood: 10, MetalBar.copper: 1})
keg = skill_recipe(Machine.keg, Skill.farming, 8, {Material.wood: 30, MetalBar.copper: 1, MetalBar.iron: 1, ArtisanGood.oak_resin: 1})
loom = skill_recipe(Machine.loom, Skill.farming, 7, {Material.wood: 60, Material.fiber: 30, ArtisanGood.pine_tar: 1})
mayonnaise_machine = skill_recipe(Machine.mayonnaise_machine, Skill.farming, 2,
                                  {Material.wood: 15, Material.stone: 15, Mineral.earth_crystal: 10, MetalBar.copper: 1})
oil_maker = skill_recipe(Machine.oil_maker, Skill.farming, 8, {Loot.slime: 50, Material.hardwood: 20, MetalBar.gold: 1})
preserves_jar = skill_recipe(Machine.preserves_jar, Skill.farming, 4, {Material.wood: 50, Material.stone: 40, Material.coal: 8})
fish_smoker = shop_recipe(Machine.fish_smoker, Region.fish_shop, 10000,
                          {Material.hardwood: 10, WaterItem.sea_jelly: 1, WaterItem.river_jelly: 1, WaterItem.cave_jelly: 1})
dehydrator = shop_recipe(Machine.dehydrator, Region.pierre_store, 10000, {Material.wood: 30, Material.clay: 2, Mineral.fire_quartz: 1})

basic_fertilizer = skill_recipe(Fertilizer.basic, Skill.farming, 1, {Material.sap: 2})

quality_fertilizer = skill_recipe(Fertilizer.quality, Skill.farming, 9, {Material.sap: 4, Fish.any: 1})
deluxe_fertilizer = ap_recipe(Fertilizer.deluxe, {MetalBar.iridium: 1, Material.sap: 40})

basic_speed_gro = skill_recipe(SpeedGro.basic, Skill.farming, 3, {ArtisanGood.pine_tar: 1, Material.moss: 5})
deluxe_speed_gro = skill_recipe(SpeedGro.deluxe, Skill.farming, 8, {ArtisanGood.oak_resin: 1, Fossil.bone_fragment: 5})
hyper_speed_gro = ap_recipe(SpeedGro.hyper, {Ore.radioactive: 1, Fossil.bone_fragment: 3, Loot.solar_essence: 1})
basic_retaining_soil = skill_recipe(RetainingSoil.basic, Skill.farming, 4, {Material.stone: 2})
quality_retaining_soil = skill_recipe(RetainingSoil.quality, Skill.farming, 7, {Material.stone: 3, Material.clay: 1})
deluxe_retaining_soil = shop_trade_recipe(RetainingSoil.deluxe, Region.island_trader, Currency.cinder_shard, 50,
                                          {Material.stone: 5, Material.fiber: 3, Material.clay: 1})
tree_fertilizer = skill_recipe(Fertilizer.tree, Skill.foraging, 7, {Material.fiber: 5, Material.stone: 5})

spring_seeds = skill_recipe(WildSeeds.spring, Skill.foraging, 1,
                            {Forageable.wild_horseradish: 1, Forageable.daffodil: 1, Forageable.leek: 1, Forageable.dandelion: 1})
summer_seeds = skill_recipe(WildSeeds.summer, Skill.foraging, 4, {Forageable.spice_berry: 1, Fruit.grape: 1, Forageable.sweet_pea: 1})
fall_seeds = skill_recipe(WildSeeds.fall, Skill.foraging, 6, {Mushroom.common: 1, Forageable.wild_plum: 1, Forageable.hazelnut: 1, Forageable.blackberry: 1})
winter_seeds = skill_recipe(WildSeeds.winter, Skill.foraging, 7,
                            {Forageable.winter_root: 1, Forageable.crystal_fruit: 1, Forageable.snow_yam: 1, Forageable.crocus: 1})
ancient_seeds = ap_recipe(WildSeeds.ancient, {Artifact.ancient_seed: 1})
grass_starter = shop_recipe(WildSeeds.grass_starter, Region.pierre_store, 1000, {Material.fiber: 10})
blue_grass_starter = ap_recipe(WildSeeds.blue_grass_starter, {Material.fiber: 25, Material.moss: 10, ArtisanGood.mystic_syrup: 1})
for wild_seeds in [WildSeeds.spring, WildSeeds.summer, WildSeeds.fall, WildSeeds.winter]:
    tea_sapling = cutscene_recipe(WildSeeds.tea_sapling, Region.sunroom, NPC.caroline, 2, {wild_seeds: 2, Material.fiber: 5, Material.wood: 5})
fiber_seeds = special_order_recipe(WildSeeds.fiber, SpecialOrder.community_cleanup, {Seed.mixed: 1, Material.sap: 5, Material.clay: 1})

wood_floor = shop_recipe(Floor.wood, Region.carpenter, 100, {Material.wood: 1})
rustic_floor = shop_recipe(Floor.rustic, Region.carpenter, 200, {Material.wood: 1})
straw_floor = shop_recipe(Floor.straw, Region.carpenter, 200, {Material.wood: 1, Material.fiber: 1})
weathered_floor = shop_recipe(Floor.weathered, LogicRegion.mines_dwarf_shop, 500, {Material.wood: 1})
crystal_floor = shop_recipe(Floor.crystal, Region.sewer, 500, {MetalBar.quartz: 1})
stone_floor = shop_recipe(Floor.stone, Region.carpenter, 100, {Material.stone: 1})
stone_walkway_floor = shop_recipe(Floor.stone_walkway, Region.carpenter, 200, {Material.stone: 1})
brick_floor = shop_recipe(Floor.brick, Region.carpenter, 500, {Material.clay: 2, Material.stone: 5})
wood_path = starter_recipe(Floor.wood_path, {Material.wood: 1})
gravel_path = starter_recipe(Floor.gravel_path, {Material.stone: 1})
cobblestone_path = starter_recipe(Floor.cobblestone_path, {Material.stone: 1})
stepping_stone_path = shop_recipe(Floor.stepping_stone_path, Region.carpenter, 100, {Material.stone: 1})
crystal_path = shop_recipe(Floor.crystal_path, Region.carpenter, 200, {MetalBar.quartz: 1})

spinner = skill_recipe(Fishing.spinner, Skill.fishing, 6, {MetalBar.iron: 2})
trap_bobber = skill_recipe(Fishing.trap_bobber, Skill.fishing, 6, {MetalBar.copper: 1, Material.sap: 10})
sonar_bobber = skill_recipe(Fishing.sonar_bobber, Skill.fishing, 6, {MetalBar.iron: 1, MetalBar.quartz: 2})
cork_bobber = skill_recipe(Fishing.cork_bobber, Skill.fishing, 7, {Material.wood: 10, Material.hardwood: 5, Loot.slime: 10})
quality_bobber = special_order_recipe(Fishing.quality_bobber, SpecialOrder.juicy_bugs_wanted, {MetalBar.copper: 1, Material.sap: 20, Loot.solar_essence: 5})
treasure_hunter = skill_recipe(Fishing.treasure_hunter, Skill.fishing, 7, {MetalBar.gold: 2})
dressed_spinner = skill_recipe(Fishing.dressed_spinner, Skill.fishing, 8, {MetalBar.iron: 2, ArtisanGood.cloth: 1})
barbed_hook = skill_recipe(Fishing.barbed_hook, Skill.fishing, 8, {MetalBar.copper: 1, MetalBar.iron: 1, MetalBar.gold: 1})
magnet = skill_recipe(Fishing.magnet, Skill.fishing, 9, {MetalBar.iron: 1})
bait = skill_recipe(Fishing.bait, Skill.fishing, 2, {Loot.bug_meat: 1})
deluxe_bait = skill_recipe(Fishing.deluxe_bait, Skill.fishing, 4, {Fishing.bait: 5, Material.moss: 2})
wild_bait = cutscene_recipe(Fishing.wild_bait, Region.tent, NPC.linus, 4, {Material.fiber: 10, Loot.bug_meat: 5, Loot.slime: 5})
magic_bait = ap_recipe(Fishing.magic_bait, {Ore.radioactive: 1, Loot.bug_meat: 3})
crab_pot = skill_recipe(Machine.crab_pot, Skill.fishing, 3, {Material.wood: 40, MetalBar.iron: 3})

sturdy_ring = skill_recipe(Ring.sturdy_ring, Skill.combat, 1, {MetalBar.copper: 2, Loot.bug_meat: 25, Loot.slime: 25})
warrior_ring = skill_recipe(Ring.warrior_ring, Skill.combat, 4, {MetalBar.iron: 10, Material.coal: 25, Mineral.frozen_tear: 10})
ring_of_yoba = skill_recipe(Ring.ring_of_yoba, Skill.combat, 7, {MetalBar.gold: 5, MetalBar.iron: 5, Mineral.diamond: 1})
thorns_ring = skill_recipe(Ring.thorns_ring, Skill.combat, 7, {Fossil.bone_fragment: 50, Material.stone: 50, MetalBar.gold: 1})
glowstone_ring = skill_recipe(Ring.glowstone_ring, Skill.mining, 4, {Loot.solar_essence: 5, MetalBar.iron: 5})
iridium_band = skill_recipe(Ring.iridium_band, Skill.combat, 9, {MetalBar.iridium: 5, Loot.solar_essence: 50, Loot.void_essence: 50})
wedding_ring = shop_recipe(Ring.wedding_ring, LogicRegion.traveling_cart, 500, {MetalBar.iridium: 5, Mineral.prismatic_shard: 1})

field_snack = skill_recipe(Edible.field_snack, Skill.foraging, 1, {TreeSeed.acorn: 1, TreeSeed.maple: 1, TreeSeed.pine: 1})
bug_steak = skill_recipe(Edible.bug_steak, Skill.combat, 1, {Loot.bug_meat: 10})
life_elixir = skill_recipe(Edible.life_elixir, Skill.combat, 2, {Mushroom.red: 1, Mushroom.purple: 1, Mushroom.morel: 1, Mushroom.chanterelle: 1})
oil_of_garlic = skill_recipe(Edible.oil_of_garlic, Skill.combat, 6, {Vegetable.garlic: 10, Ingredient.oil: 1})

monster_musk = special_order_recipe(Consumable.monster_musk, SpecialOrder.prismatic_jelly, {Loot.bat_wing: 30, Loot.slime: 30})
fairy_dust = quest_recipe(Consumable.fairy_dust, Quest.the_pirates_wife, {Mineral.diamond: 1, Flower.fairy_rose: 1})
warp_totem_beach = skill_recipe(Consumable.warp_totem_beach, Skill.foraging, 6, {Material.hardwood: 1, WaterItem.coral: 2, Material.fiber: 10})
warp_totem_mountains = skill_recipe(Consumable.warp_totem_mountains, Skill.foraging, 7, {Material.hardwood: 1, MetalBar.iron: 1, Material.stone: 25})
warp_totem_farm = skill_recipe(Consumable.warp_totem_farm, Skill.foraging, 8, {Material.hardwood: 1, ArtisanGood.honey: 1, Material.fiber: 20})
warp_totem_desert = shop_trade_recipe(Consumable.warp_totem_desert, Region.desert, MetalBar.iridium, 10,
                                      {Material.hardwood: 2, Forageable.coconut: 1, Ore.iridium: 4})
warp_totem_island = shop_recipe(Consumable.warp_totem_island, Region.volcano_dwarf_shop, 10000,
                                {Material.hardwood: 5, Forageable.dragon_tooth: 1, Forageable.ginger: 1})
rain_totem = skill_recipe(Consumable.rain_totem, Skill.foraging, 9, {Material.hardwood: 1, ArtisanGood.truffle_oil: 1, ArtisanGood.pine_tar: 5})

torch = starter_recipe(Lighting.torch, {Material.wood: 1, Material.sap: 2})
campfire = starter_recipe(Lighting.campfire, {Material.stone: 10, Material.wood: 10, Material.fiber: 10})
wooden_brazier = shop_recipe(Lighting.wooden_brazier, Region.carpenter, 250, {Material.wood: 10, Material.coal: 1, Material.fiber: 5})
stone_brazier = shop_recipe(Lighting.stone_brazier, Region.carpenter, 400, {Material.stone: 10, Material.coal: 1, Material.fiber: 5})
gold_brazier = shop_recipe(Lighting.gold_brazier, Region.carpenter, 1000, {MetalBar.gold: 1, Material.coal: 1, Material.fiber: 5})
carved_brazier = shop_recipe(Lighting.carved_brazier, Region.carpenter, 2000, {Material.hardwood: 10, Material.coal: 1})
stump_brazier = shop_recipe(Lighting.stump_brazier, Region.carpenter, 800, {Material.hardwood: 5, Material.coal: 1})
barrel_brazier = shop_recipe(Lighting.barrel_brazier, Region.carpenter, 800, {Material.wood: 50, Loot.solar_essence: 1, Material.coal: 1})
skull_brazier = shop_recipe(Lighting.skull_brazier, Region.carpenter, 3000, {Fossil.bone_fragment: 10})
marble_brazier = shop_recipe(Lighting.marble_brazier, Region.carpenter, 5000, {Mineral.marble: 1, Mineral.aquamarine: 1, Material.stone: 100})
wood_lamp_post = shop_recipe(Lighting.wood_lamp_post, Region.carpenter, 500, {Material.wood: 50, ArtisanGood.battery_pack: 1})
iron_lamp_post = shop_recipe(Lighting.iron_lamp_post, Region.carpenter, 1000, {MetalBar.iron: 1, ArtisanGood.battery_pack: 1})
jack_o_lantern = festival_shop_recipe(Lighting.jack_o_lantern, LogicRegion.spirit_eve, 2000, {Vegetable.pumpkin: 1, Lighting.torch: 1})

bone_mill = special_order_recipe(Machine.bone_mill, SpecialOrder.fragments_of_the_past, {Fossil.bone_fragment: 10, Material.clay: 3, Material.stone: 20})
bait_maker = skill_recipe(Machine.bait_maker, Skill.fishing, 6, {MetalBar.iron: 3, WaterItem.coral: 3, WaterItem.sea_urchin: 1})

charcoal_kiln = skill_recipe(Machine.charcoal_kiln, Skill.foraging, 2, {Material.wood: 20, MetalBar.copper: 2})

crystalarium = skill_recipe(Machine.crystalarium, Skill.mining, 9, {Material.stone: 99, MetalBar.gold: 5, MetalBar.iridium: 2, ArtisanGood.battery_pack: 1})
# In-Game, the Furnace recipe is completely unique. It is the only recipe that is obtained in a cutscene after doing a skill-related action.
# So it has a custom source that needs both the craftsanity item from AP and the skill, if craftsanity is enabled.
furnace = skill_craftsanity_recipe(Machine.furnace, Skill.mining, 1, {Ore.copper: 20, Material.stone: 25})
geode_crusher = special_order_recipe(Machine.geode_crusher, SpecialOrder.cave_patrol, {MetalBar.gold: 2, Material.stone: 50, Mineral.diamond: 1})
mushroom_log = skill_recipe(Machine.mushroom_log, Skill.foraging, 4, {Material.hardwood: 10, Material.moss: 10})
heavy_tapper = ap_recipe(Machine.heavy_tapper, {Material.hardwood: 30, MetalBar.radioactive: 1})
lightning_rod = skill_recipe(Machine.lightning_rod, Skill.foraging, 6, {MetalBar.iron: 1, MetalBar.quartz: 1, Loot.bat_wing: 5})
ostrich_incubator = ap_recipe(Machine.ostrich_incubator, {Fossil.bone_fragment: 50, Material.hardwood: 50, Currency.cinder_shard: 20})
recycling_machine = skill_recipe(Machine.recycling_machine, Skill.fishing, 4, {Material.wood: 25, Material.stone: 25, MetalBar.iron: 1})
seed_maker = skill_recipe(Machine.seed_maker, Skill.farming, 9, {Material.wood: 25, Material.coal: 10, MetalBar.gold: 1})
slime_egg_press = skill_recipe(Machine.slime_egg_press, Skill.combat, 6, {Material.coal: 25, Mineral.fire_quartz: 1, ArtisanGood.battery_pack: 1})
slime_incubator = skill_recipe(Machine.slime_incubator, Skill.combat, 8, {MetalBar.iridium: 2, Loot.slime: 100})
solar_panel = special_order_recipe(Machine.solar_panel, SpecialOrder.island_ingredients, {MetalBar.quartz: 10, MetalBar.iron: 5, MetalBar.gold: 5})

tapper = skill_recipe(Machine.tapper, Skill.foraging, 4, {Material.wood: 40, MetalBar.copper: 2})

worm_bin = skill_recipe(Machine.worm_bin, Skill.fishing, 4, {Material.hardwood: 25, MetalBar.gold: 1, MetalBar.iron: 1, Material.fiber: 50})
deluxe_worm_bin = skill_recipe(Machine.deluxe_worm_bin, Skill.fishing, 8, {Machine.worm_bin: 1, Material.moss: 30})

tub_o_flowers = festival_shop_recipe(Furniture.tub_o_flowers, LogicRegion.flower_dance, 2000,
                                     {Material.wood: 15, Seed.tulip: 1, Seed.jazz: 1, Seed.poppy: 1, Seed.spangle: 1})
wicked_statue = shop_recipe(Furniture.wicked_statue, Region.sewer, 1000, {Material.stone: 25, Material.coal: 5})
flute_block = cutscene_recipe(Furniture.flute_block, Region.carpenter, NPC.robin, 6, {Material.wood: 10, Ore.copper: 2, Material.fiber: 20})
drum_block = cutscene_recipe(Furniture.drum_block, Region.carpenter, NPC.robin, 6, {Material.stone: 10, Ore.copper: 2, Material.fiber: 20})

chest = starter_recipe(Storage.chest, {Material.wood: 50})
stone_chest = special_order_recipe(Storage.stone_chest, SpecialOrder.robins_resource_rush, {Material.stone: 50})
big_chest = shop_recipe(Storage.big_chest, Region.carpenter, 5000, {Material.wood: 120, MetalBar.copper: 2})
big_stone_chest = shop_recipe(Storage.big_stone_chest, LogicRegion.mines_dwarf_shop, 5000, {Material.stone: 250})

wood_sign = starter_recipe(Sign.wood, {Material.wood: 25})
stone_sign = starter_recipe(Sign.stone, {Material.stone: 25})
dark_sign = friendship_recipe(Sign.dark, NPC.krobus, 3, {Loot.bat_wing: 5, Fossil.bone_fragment: 5})
text_sign = starter_recipe(Sign.text, {Material.wood: 25})

garden_pot = ap_recipe(Craftable.garden_pot, {Material.clay: 1, Material.stone: 10, MetalBar.quartz: 1}, "Greenhouse")
scarecrow = skill_recipe(Craftable.scarecrow, Skill.farming, 1, {Material.wood: 50, Material.coal: 1, Material.fiber: 20})
deluxe_scarecrow = ap_recipe(Craftable.deluxe_scarecrow, {Material.wood: 50, Material.fiber: 40, Ore.iridium: 1})
staircase = skill_recipe(Craftable.staircase, Skill.mining, 2, {Material.stone: 99})
explosive_ammo = skill_recipe(Craftable.explosive_ammo, Skill.combat, 8, {MetalBar.iron: 1, Material.coal: 2})
transmute_fe = skill_recipe(Craftable.transmute_fe, Skill.mining, 4, {MetalBar.copper: 3})
transmute_au = skill_recipe(Craftable.transmute_au, Skill.mining, 7, {MetalBar.iron: 2})
mini_jukebox = cutscene_recipe(Craftable.mini_jukebox, Region.saloon, NPC.gus, 5, {MetalBar.iron: 2, ArtisanGood.battery_pack: 1})
mini_obelisk = special_order_recipe(Craftable.mini_obelisk, SpecialOrder.a_curious_substance, {Material.hardwood: 30, Loot.solar_essence: 20, MetalBar.gold: 3})
farm_computer = special_order_recipe(Craftable.farm_computer, SpecialOrder.aquatic_overpopulation,
                                     {Artifact.dwarf_gadget: 1, ArtisanGood.battery_pack: 1, MetalBar.quartz: 10})
hopper = ap_recipe(Craftable.hopper, {Material.hardwood: 10, MetalBar.iridium: 1, MetalBar.radioactive: 1})

cookout_kit = skill_recipe(Craftable.cookout_kit, Skill.foraging, 3, {Material.wood: 15, Material.fiber: 10, Material.coal: 3})
tent_kit = skill_recipe(Craftable.tent_kit, Skill.foraging, 8, {Material.hardwood: 10, Material.fiber: 25, ArtisanGood.cloth: 1})

statue_of_blessings = mastery_recipe(Statue.blessings, Skill.farming, {Material.sap: 999, Material.fiber: 999, Material.stone: 999, Material.moss: 333})
statue_of_dwarf_king = mastery_recipe(Statue.dwarf_king, Skill.mining, {MetalBar.iridium: 20})
heavy_furnace = mastery_recipe(Machine.heavy_furnace, Skill.mining, {Machine.furnace: 2, MetalBar.iron: 3, Material.stone: 50})
mystic_tree_seed = mastery_recipe(TreeSeed.mystic, Skill.foraging, {TreeSeed.acorn: 5, TreeSeed.maple: 5, TreeSeed.pine: 5, TreeSeed.mahogany: 5})
treasure_totem = mastery_recipe(Consumable.treasure_totem, Skill.foraging, {Material.hardwood: 5, ArtisanGood.mystic_syrup: 1, Material.moss: 10})
challenge_bait = mastery_recipe(Fishing.challenge_bait, Skill.fishing, {Fossil.bone_fragment: 5, Material.moss: 2})
anvil = mastery_recipe(Machine.anvil, Skill.combat, {MetalBar.iron: 50})
mini_forge = mastery_recipe(Machine.mini_forge, Skill.combat, {Forageable.dragon_tooth: 5, MetalBar.iron: 10, MetalBar.gold: 10, MetalBar.iridium: 5})

travel_charm = shop_recipe(ModCraftable.travel_core, Region.adventurer_guild, 250, {Loot.solar_essence: 1, Loot.void_essence: 1}, ModNames.magic)
preservation_chamber = skill_recipe(ModMachine.preservation_chamber, ModSkill.archaeology, 1,
                                    {MetalBar.copper: 1, Material.wood: 15, ArtisanGood.oak_resin: 30},
                                    ModNames.archaeology)
restoration_table = skill_recipe(ModMachine.restoration_table, ModSkill.archaeology, 1, {Material.wood: 15, MetalBar.copper: 1, MetalBar.iron: 1},
                                 ModNames.archaeology)
preservation_chamber_h = skill_recipe(ModMachine.hardwood_preservation_chamber, ModSkill.archaeology, 6, {MetalBar.copper: 1, Material.hardwood: 15,
                                                                                                          ArtisanGood.oak_resin: 30}, ModNames.archaeology)
grinder = skill_recipe(ModMachine.grinder, ModSkill.archaeology, 2, {Artifact.rusty_cog: 10, MetalBar.iron: 5, ArtisanGood.battery_pack: 1},
                       ModNames.archaeology)
ancient_battery = skill_recipe(ModMachine.ancient_battery, ModSkill.archaeology, 7, {Material.stone: 40, MetalBar.copper: 10, MetalBar.iron: 5},
                               ModNames.archaeology)
glass_bazier = skill_recipe(ModCraftable.glass_brazier, ModSkill.archaeology, 4, {Artifact.glass_shards: 10}, ModNames.archaeology)
glass_path = skill_recipe(ModFloor.glass_path, ModSkill.archaeology, 3, {Artifact.glass_shards: 1}, ModNames.archaeology)
glass_fence = skill_recipe(ModCraftable.glass_fence, ModSkill.archaeology, 7, {Artifact.glass_shards: 5}, ModNames.archaeology)
bone_path = skill_recipe(ModFloor.bone_path, ModSkill.archaeology, 4, {Fossil.bone_fragment: 1}, ModNames.archaeology)
rust_path = skill_recipe(ModFloor.rusty_path, ModSkill.archaeology, 2, {ModTrash.rusty_scrap: 2}, ModNames.archaeology)
rusty_brazier = skill_recipe(ModCraftable.rusty_brazier, ModSkill.archaeology, 3, {ModTrash.rusty_scrap: 10, Material.coal: 1, Material.fiber: 1},
                             ModNames.archaeology)
bone_fence = skill_recipe(ModCraftable.bone_fence, ModSkill.archaeology, 8, {Fossil.bone_fragment: 2}, ModNames.archaeology)
water_shifter = skill_recipe(ModCraftable.water_shifter, ModSkill.archaeology, 4, {Material.wood: 40, MetalBar.copper: 4}, ModNames.archaeology)
wooden_display = skill_recipe(ModCraftable.wooden_display, ModSkill.archaeology, 1, {Material.wood: 25}, ModNames.archaeology)
hardwood_display = skill_recipe(ModCraftable.hardwood_display, ModSkill.archaeology, 7, {Material.hardwood: 10}, ModNames.archaeology)
lucky_ring = skill_recipe(Ring.lucky_ring, ModSkill.archaeology, 8, {Artifact.elvish_jewelry: 1, AnimalProduct.rabbit_foot: 5, Mineral.tigerseye: 1},
                          ModNames.archaeology)
volcano_totem = skill_recipe(ModConsumable.volcano_totem, ModSkill.archaeology, 9, {Material.cinder_shard: 5, Artifact.rare_disc: 1, Artifact.dwarf_gadget: 1},
                             ModNames.archaeology)
haste_elixir = shop_recipe(ModEdible.haste_elixir, SVERegion.alesia_shop, 35000, {Loot.void_essence: 35, ModLoot.void_soul: 5, Ingredient.sugar: 1,
                                                                                  Meal.spicy_eel: 1}, ModNames.sve)
hero_elixir = shop_recipe(ModEdible.hero_elixir, SVERegion.isaac_shop, 65000, {ModLoot.void_pebble: 3, ModLoot.void_soul: 5, Ingredient.oil: 1,
                                                                               Loot.slime: 10}, ModNames.sve)
armor_elixir = shop_recipe(ModEdible.armor_elixir, SVERegion.alesia_shop, 50000, {Loot.solar_essence: 30, ModLoot.void_soul: 5, Ingredient.vinegar: 5,
                                                                                  Fossil.bone_fragment: 5}, ModNames.sve)
ginger_tincture = friendship_recipe(ModConsumable.ginger_tincture, ModNPC.goblin, 4, {DistantLandsForageable.brown_amanita: 1, Forageable.ginger: 5,
                                                                                      Material.cinder_shard: 1, DistantLandsForageable.swamp_herb: 1},
                                    ModNames.distant_lands)

neanderthal_skeleton = shop_recipe(ModCraftable.neanderthal_skeleton, LogicRegion.mines_dwarf_shop, 5000,
                                   {ModFossil.neanderthal_skull: 1, ModFossil.neanderthal_ribs: 1, ModFossil.neanderthal_pelvis: 1,
                                    ModFossil.neanderthal_limb_bones: 1,
                                    MetalBar.iron: 5, Material.hardwood: 10}, ModNames.boarding_house)
pterodactyl_skeleton_l = shop_recipe(ModCraftable.pterodactyl_skeleton_l, LogicRegion.mines_dwarf_shop, 5000,
                                     {ModFossil.pterodactyl_phalange: 1, ModFossil.pterodactyl_skull: 1, ModFossil.pterodactyl_l_wing_bone: 1,
                                      MetalBar.iron: 10, Material.hardwood: 15}, ModNames.boarding_house)
pterodactyl_skeleton_m = shop_recipe(ModCraftable.pterodactyl_skeleton_m, LogicRegion.mines_dwarf_shop, 5000,
                                     {ModFossil.pterodactyl_phalange: 1, ModFossil.pterodactyl_vertebra: 1, ModFossil.pterodactyl_ribs: 1,
                                      MetalBar.iron: 10, Material.hardwood: 15}, ModNames.boarding_house)
pterodactyl_skeleton_r = shop_recipe(ModCraftable.pterodactyl_skeleton_r, LogicRegion.mines_dwarf_shop, 5000,
                                     {ModFossil.pterodactyl_phalange: 1, ModFossil.pterodactyl_claw: 1, ModFossil.pterodactyl_r_wing_bone: 1,
                                      MetalBar.iron: 10, Material.hardwood: 15}, ModNames.boarding_house)
trex_skeleton_l = shop_recipe(ModCraftable.trex_skeleton_l, LogicRegion.mines_dwarf_shop, 5000,
                              {ModFossil.dinosaur_vertebra: 1, ModFossil.dinosaur_tooth: 1, ModFossil.dinosaur_skull: 1,
                               MetalBar.iron: 10, Material.hardwood: 15}, ModNames.boarding_house)
trex_skeleton_m = shop_recipe(ModCraftable.trex_skeleton_m, LogicRegion.mines_dwarf_shop, 5000,
                              {ModFossil.dinosaur_vertebra: 1, ModFossil.dinosaur_ribs: 1, ModFossil.dinosaur_claw: 1,
                               MetalBar.iron: 10, Material.hardwood: 15}, ModNames.boarding_house)
trex_skeleton_r = shop_recipe(ModCraftable.trex_skeleton_r, LogicRegion.mines_dwarf_shop, 5000,
                              {ModFossil.dinosaur_vertebra: 1, ModFossil.dinosaur_femur: 1, ModFossil.dinosaur_pelvis: 1,
                               MetalBar.iron: 10, Material.hardwood: 15}, ModNames.boarding_house)

bouquet = skill_recipe(Gift.bouquet, ModSkill.socializing, 3, {Flower.tulip: 3}, ModNames.socializing_skill)
trash_bin = skill_recipe(ModMachine.trash_bin, ModSkill.binning, 2, {Material.stone: 30, MetalBar.iron: 2}, ModNames.binning_skill)
composter = skill_recipe(ModMachine.composter, ModSkill.binning, 4, {Material.wood: 70, Material.sap: 20, Material.fiber: 30}, ModNames.binning_skill)
recycling_bin = skill_recipe(ModMachine.recycling_bin, ModSkill.binning, 7, {MetalBar.iron: 3, Material.fiber: 10, MetalBar.gold: 2}, ModNames.binning_skill)
advanced_recycling_machine = skill_recipe(ModMachine.advanced_recycling_machine, ModSkill.binning, 9,
                                          {MetalBar.iridium: 5, ArtisanGood.battery_pack: 2, MetalBar.quartz: 10}, ModNames.binning_skill)

coppper_slot_machine = skill_recipe(ModMachine.copper_slot_machine, ModSkill.luck, 2, {MetalBar.copper: 15, Material.stone: 1, Material.wood: 1,
                                                                                       Material.fiber: 1, Material.sap: 1, Loot.slime: 1,
                                                                                       Forageable.salmonberry: 1, Material.clay: 1, Trash.joja_cola: 1}, ModNames.luck_skill)

gold_slot_machine = skill_recipe(ModMachine.gold_slot_machine, ModSkill.luck, 4, {MetalBar.gold: 15, ModMachine.copper_slot_machine: 1}, ModNames.luck_skill)
iridium_slot_machine = skill_recipe(ModMachine.iridium_slot_machine, ModSkill.luck, 4, {MetalBar.iridium: 15, ModMachine.gold_slot_machine: 1}, ModNames.luck_skill)
radioactive_slot_machine = skill_recipe(ModMachine.radioactive_slot_machine, ModSkill.luck, 4, {MetalBar.radioactive: 15, ModMachine.iridium_slot_machine: 1}, ModNames.luck_skill)

all_crafting_recipes_by_name = {recipe.item: recipe for recipe in all_crafting_recipes}
