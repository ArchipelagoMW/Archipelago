from typing import Dict, List, Optional

from .recipe_source import RecipeSource, FriendshipSource, SkillSource, QueenOfSauceSource, ShopSource, StarterSource, ShopTradeSource, ShopFriendshipSource
from ..mods.mod_data import ModNames
from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.craftable_names import ModEdible, Edible
from ..strings.crop_names import Fruit, Vegetable, SVEFruit, DistantLandsCrop
from ..strings.fish_names import Fish, SVEFish, WaterItem, DistantLandsFish, SVEWaterItem
from ..strings.flower_names import Flower
from ..strings.food_names import Meal, SVEMeal, Beverage, DistantLandsMeal, BoardingHouseMeal, ArchaeologyMeal, TrashyMeal
from ..strings.forageable_names import Forageable, SVEForage, Mushroom
from ..strings.ingredient_names import Ingredient
from ..strings.material_names import Material
from ..strings.metal_names import Fossil, Artifact
from ..strings.monster_drop_names import Loot
from ..strings.region_names import Region, SVERegion
from ..strings.season_names import Season
from ..strings.seed_names import Seed
from ..strings.skill_names import Skill, ModSkill
from ..strings.villager_names import NPC, ModNPC


class CookingRecipe:
    meal: str
    ingredients: Dict[str, int]
    source: RecipeSource
    mod_name: Optional[str] = None

    def __init__(self, meal: str, ingredients: Dict[str, int], source: RecipeSource, mod_name: Optional[str] = None):
        self.meal = meal
        self.ingredients = ingredients
        self.source = source
        self.mod_name = mod_name

    def __repr__(self):
        return f"{self.meal} (Source: {self.source} |" \
               f" Ingredients: {self.ingredients})"


all_cooking_recipes: List[CookingRecipe] = []


def friendship_recipe(name: str, friend: str, hearts: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CookingRecipe:
    source = FriendshipSource(friend, hearts)
    return create_recipe(name, ingredients, source, mod_name)


def friendship_and_shop_recipe(name: str, friend: str, hearts: int, region: str, price: int, ingredients: Dict[str, int],
                               mod_name: Optional[str] = None) -> CookingRecipe:
    source = ShopFriendshipSource(friend, hearts, region, price)
    return create_recipe(name, ingredients, source, mod_name)


def skill_recipe(name: str, skill: str, level: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CookingRecipe:
    source = SkillSource(skill, level)
    return create_recipe(name, ingredients, source, mod_name)


def shop_recipe(name: str, region: str, price: int, ingredients: Dict[str, int], mod_name: Optional[str] = None) -> CookingRecipe:
    source = ShopSource(region, price)
    return create_recipe(name, ingredients, source, mod_name)


def shop_trade_recipe(name: str, region: str, currency: str, price: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = ShopTradeSource(region, currency, price)
    return create_recipe(name, ingredients, source)


def queen_of_sauce_recipe(name: str, year: int, season: str, day: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = QueenOfSauceSource(year, season, day)
    return create_recipe(name, ingredients, source)


def starter_recipe(name: str, ingredients: Dict[str, int]) -> CookingRecipe:
    source = StarterSource()
    return create_recipe(name, ingredients, source)


def create_recipe(name: str, ingredients: Dict[str, int], source: RecipeSource, mod_name: Optional[str] = None) -> CookingRecipe:
    recipe = CookingRecipe(name, ingredients, source, mod_name)
    all_cooking_recipes.append(recipe)
    return recipe


algae_soup = friendship_recipe(Meal.algae_soup, NPC.clint, 3, {WaterItem.green_algae: 4})
artichoke_dip = queen_of_sauce_recipe(Meal.artichoke_dip, 1, Season.fall, 28, {Vegetable.artichoke: 1, AnimalProduct.cow_milk: 1})
autumn_bounty = friendship_recipe(Meal.autumn_bounty, NPC.demetrius, 7, {Vegetable.yam: 1, Vegetable.pumpkin: 1})
baked_fish = queen_of_sauce_recipe(Meal.baked_fish, 1, Season.summer, 7, {Fish.sunfish: 1, Fish.bream: 1, Ingredient.wheat_flour: 1})
banana_pudding = shop_trade_recipe(Meal.banana_pudding, Region.island_trader, Fossil.bone_fragment, 30,
                                   {Fruit.banana: 1, AnimalProduct.cow_milk: 1, Ingredient.sugar: 1})
bean_hotpot = friendship_recipe(Meal.bean_hotpot, NPC.clint, 7, {Vegetable.green_bean: 2})
blackberry_cobbler_ingredients = {Forageable.blackberry: 2, Ingredient.sugar: 1, Ingredient.wheat_flour: 1}
blackberry_cobbler_qos = queen_of_sauce_recipe(Meal.blackberry_cobbler, 2, Season.fall, 14, blackberry_cobbler_ingredients)
blueberry_tart_ingredients = {Fruit.blueberry: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.any_egg: 1}
blueberry_tart = friendship_recipe(Meal.blueberry_tart, NPC.pierre, 3, blueberry_tart_ingredients)
bread = queen_of_sauce_recipe(Meal.bread, 1, Season.summer, 28, {Ingredient.wheat_flour: 1})
bruschetta = queen_of_sauce_recipe(Meal.bruschetta, 2, Season.winter, 21, {Meal.bread: 1, Ingredient.oil: 1, Vegetable.tomato: 1})
carp_surprise = queen_of_sauce_recipe(Meal.carp_surprise, 2, Season.summer, 7, {Fish.carp: 4})
cheese_cauliflower = friendship_recipe(Meal.cheese_cauliflower, NPC.pam, 3, {Vegetable.cauliflower: 1, ArtisanGood.cheese: 1})
chocolate_cake_ingredients = {Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1}
chocolate_cake_qos = queen_of_sauce_recipe(Meal.chocolate_cake, 1, Season.winter, 14, chocolate_cake_ingredients)
chowder = friendship_recipe(Meal.chowder, NPC.willy, 3, {Fish.clam: 1, AnimalProduct.cow_milk: 1})
coleslaw = queen_of_sauce_recipe(Meal.coleslaw, 14, Season.spring, 14, {Vegetable.red_cabbage: 1, Ingredient.vinegar: 1, ArtisanGood.mayonnaise: 1})
complete_breakfast_ingredients = {Meal.fried_egg: 1, AnimalProduct.milk: 1, Meal.hashbrowns: 1, Meal.pancakes: 1}
complete_breakfast = queen_of_sauce_recipe(Meal.complete_breakfast, 2, Season.spring, 21, complete_breakfast_ingredients)
cookie = friendship_recipe(Meal.cookie, NPC.evelyn, 4, {Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1})
crab_cakes_ingredients = {Fish.crab: 1, Ingredient.wheat_flour: 1, AnimalProduct.chicken_egg: 1, Ingredient.oil: 1}
crab_cakes_qos = queen_of_sauce_recipe(Meal.crab_cakes, 2, Season.fall, 21, crab_cakes_ingredients)
cranberry_candy = queen_of_sauce_recipe(Meal.cranberry_candy, 1, Season.winter, 28, {Fruit.cranberries: 1, Fruit.apple: 1, Ingredient.sugar: 1})
cranberry_sauce = friendship_recipe(Meal.cranberry_sauce, NPC.gus, 7, {Fruit.cranberries: 1, Ingredient.sugar: 1})
crispy_bass = friendship_recipe(Meal.crispy_bass, NPC.kent, 3, {Fish.largemouth_bass: 1, Ingredient.wheat_flour: 1, Ingredient.oil: 1})
dish_o_the_sea = skill_recipe(Meal.dish_o_the_sea, Skill.fishing, 3, {Fish.sardine: 2, Meal.hashbrowns: 1})
eggplant_parmesan = friendship_recipe(Meal.eggplant_parmesan, NPC.lewis, 7, {Vegetable.eggplant: 1, Vegetable.tomato: 1})
escargot = friendship_recipe(Meal.escargot, NPC.willy, 5, {Fish.snail: 1, Vegetable.garlic: 1})
farmer_lunch = skill_recipe(Meal.farmer_lunch, Skill.farming, 3, {Meal.omelet: 2, Vegetable.parsnip: 1})
fiddlehead_risotto = queen_of_sauce_recipe(Meal.fiddlehead_risotto, 2, Season.fall, 28, {Ingredient.oil: 1, Forageable.fiddlehead_fern: 1, Vegetable.garlic: 1})
fish_stew = friendship_recipe(Meal.fish_stew, NPC.willy, 7, {Fish.crayfish: 1, Fish.mussel: 1, Fish.periwinkle: 1, Vegetable.tomato: 1})
fish_taco = friendship_recipe(Meal.fish_taco, NPC.linus, 7, {Fish.tuna: 1, Meal.tortilla: 1, Vegetable.red_cabbage: 1, ArtisanGood.mayonnaise: 1})
fried_calamari = friendship_recipe(Meal.fried_calamari, NPC.jodi, 3, {Fish.squid: 1, Ingredient.wheat_flour: 1, Ingredient.oil: 1})
fried_eel = friendship_recipe(Meal.fried_eel, NPC.george, 3, {Fish.eel: 1, Ingredient.oil: 1})
fried_egg = starter_recipe(Meal.fried_egg, {AnimalProduct.chicken_egg: 1})
fried_mushroom = friendship_recipe(Meal.fried_mushroom, NPC.demetrius, 3, {Mushroom.common: 1, Mushroom.morel: 1, Ingredient.oil: 1})
fruit_salad = queen_of_sauce_recipe(Meal.fruit_salad, 2, Season.fall, 7, {Fruit.blueberry: 1, Fruit.melon: 1, Fruit.apricot: 1})
ginger_ale = shop_recipe(Beverage.ginger_ale, Region.volcano_dwarf_shop, 1000, {Forageable.ginger: 3, Ingredient.sugar: 1})
glazed_yams = queen_of_sauce_recipe(Meal.glazed_yams, 1, Season.fall, 21, {Vegetable.yam: 1, Ingredient.sugar: 1})
hashbrowns = queen_of_sauce_recipe(Meal.hashbrowns, 2, Season.spring, 14, {Vegetable.potato: 1, Ingredient.oil: 1})
ice_cream = friendship_recipe(Meal.ice_cream, NPC.jodi, 7, {AnimalProduct.cow_milk: 1, Ingredient.sugar: 1})
lobster_bisque_ingredients = {Fish.lobster: 1, AnimalProduct.cow_milk: 1}
lobster_bisque_friend = friendship_recipe(Meal.lobster_bisque, NPC.willy, 9, lobster_bisque_ingredients)
lobster_bisque_qos = queen_of_sauce_recipe(Meal.lobster_bisque, 2, Season.winter, 14, lobster_bisque_ingredients)
lucky_lunch = queen_of_sauce_recipe(Meal.lucky_lunch, 2, Season.spring, 28, {Fish.sea_cucumber: 1, Meal.tortilla: 1, Flower.blue_jazz: 1})
maki_roll = queen_of_sauce_recipe(Meal.maki_roll, 1, Season.summer, 21, {Fish.any: 1, WaterItem.seaweed: 1, Ingredient.rice: 1})
mango_sticky_rice = friendship_recipe(Meal.mango_sticky_rice, NPC.leo, 7, {Fruit.mango: 1, Forageable.coconut: 1, Ingredient.rice: 1})
maple_bar = queen_of_sauce_recipe(Meal.maple_bar, 2, Season.summer, 14, {ArtisanGood.maple_syrup: 1, Ingredient.sugar: 1, Ingredient.wheat_flour: 1})
miners_treat = skill_recipe(Meal.miners_treat, Skill.mining, 3, {Forageable.cave_carrot: 2, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1})
moss_soup = skill_recipe(Meal.moss_soup, Skill.foraging, 3, {Material.moss: 20})
omelet = queen_of_sauce_recipe(Meal.omelet, 1, Season.spring, 28, {AnimalProduct.chicken_egg: 1, AnimalProduct.cow_milk: 1})
pale_broth = friendship_recipe(Meal.pale_broth, NPC.marnie, 3, {WaterItem.white_algae: 2})
pancakes = queen_of_sauce_recipe(Meal.pancakes, 1, Season.summer, 14, {Ingredient.wheat_flour: 1, AnimalProduct.chicken_egg: 1})
parsnip_soup = friendship_recipe(Meal.parsnip_soup, NPC.caroline, 3, {Vegetable.parsnip: 1, AnimalProduct.cow_milk: 1, Ingredient.vinegar: 1})
pepper_poppers = friendship_recipe(Meal.pepper_poppers, NPC.shane, 3, {Fruit.hot_pepper: 1, ArtisanGood.cheese: 1})
pink_cake_ingredients = {Fruit.melon: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1}
pink_cake_qos = queen_of_sauce_recipe(Meal.pink_cake, 2, Season.summer, 21, pink_cake_ingredients)
pizza_ingredients = {Ingredient.wheat_flour: 1, Vegetable.tomato: 1, ArtisanGood.cheese: 1}
pizza_qos = queen_of_sauce_recipe(Meal.pizza, 2, Season.spring, 7, pizza_ingredients)
pizza_saloon = shop_recipe(Meal.pizza, Region.saloon, 150, pizza_ingredients)
plum_pudding = queen_of_sauce_recipe(Meal.plum_pudding, 1, Season.winter, 7, {Forageable.wild_plum: 2, Ingredient.wheat_flour: 1, Ingredient.sugar: 1})
poi = friendship_recipe(Meal.poi, NPC.leo, 3, {Vegetable.taro_root: 4})
poppyseed_muffin = queen_of_sauce_recipe(Meal.poppyseed_muffin, 2, Season.winter, 7, {Flower.poppy: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1})
pumpkin_pie_ingredients = {Vegetable.pumpkin: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1}
pumpkin_pie_qos = queen_of_sauce_recipe(Meal.pumpkin_pie, 1, Season.winter, 21, pumpkin_pie_ingredients)
pumpkin_soup = friendship_recipe(Meal.pumpkin_soup, NPC.robin, 7, {Vegetable.pumpkin: 1, AnimalProduct.cow_milk: 1})
radish_salad = queen_of_sauce_recipe(Meal.radish_salad, 1, Season.spring, 21, {Ingredient.oil: 1, Ingredient.vinegar: 1, Vegetable.radish: 1})
red_plate = friendship_recipe(Meal.red_plate, NPC.emily, 7, {Vegetable.red_cabbage: 1, Vegetable.radish: 1})
rhubarb_pie = friendship_recipe(Meal.rhubarb_pie, NPC.marnie, 7, {Fruit.rhubarb: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1})
rice_pudding = friendship_recipe(Meal.rice_pudding, NPC.evelyn, 7, {AnimalProduct.milk: 1, Ingredient.sugar: 1, Ingredient.rice: 1})
roasted_hazelnuts = queen_of_sauce_recipe(Meal.roasted_hazelnuts, 2, Season.summer, 28, {Forageable.hazelnut: 3})
roots_platter = skill_recipe(Meal.roots_platter, Skill.combat, 3, {Forageable.cave_carrot: 1, Forageable.winter_root: 1})
salad = friendship_recipe(Meal.salad, NPC.emily, 3, {Forageable.leek: 1, Forageable.dandelion: 1, Ingredient.vinegar: 1})
salmon_dinner = friendship_recipe(Meal.salmon_dinner, NPC.gus, 3, {Fish.salmon: 1, Vegetable.amaranth: 1, Vegetable.kale: 1})
sashimi = friendship_recipe(Meal.sashimi, NPC.linus, 3, {Fish.any: 1})
seafoam_pudding = skill_recipe(Meal.seafoam_pudding, Skill.fishing, 9, {Fish.flounder: 1, Fish.midnight_carp: 1, AnimalProduct.squid_ink: 1})
shrimp_cocktail = queen_of_sauce_recipe(Meal.shrimp_cocktail, 2, Season.winter, 28, {Vegetable.tomato: 1, Fish.shrimp: 1, Forageable.wild_horseradish: 1})
spaghetti = friendship_recipe(Meal.spaghetti, NPC.lewis, 3, {Vegetable.tomato: 1, Ingredient.wheat_flour: 1})
spicy_eel = friendship_recipe(Meal.spicy_eel, NPC.george, 7, {Fish.eel: 1, Fruit.hot_pepper: 1})
squid_ink_ravioli = skill_recipe(Meal.squid_ink_ravioli, Skill.combat, 9, {AnimalProduct.squid_ink: 1, Ingredient.wheat_flour: 1, Vegetable.tomato: 1})
stir_fry_ingredients = {Forageable.cave_carrot: 1, Mushroom.common: 1, Vegetable.kale: 1, Ingredient.sugar: 1}
stir_fry_qos = queen_of_sauce_recipe(Meal.stir_fry, 1, Season.spring, 7, stir_fry_ingredients)
strange_bun = friendship_recipe(Meal.strange_bun, NPC.shane, 7, {Ingredient.wheat_flour: 1, Fish.periwinkle: 1, ArtisanGood.void_mayonnaise: 1})
stuffing = friendship_recipe(Meal.stuffing, NPC.pam, 7, {Meal.bread: 1, Fruit.cranberries: 1, Forageable.hazelnut: 1})
super_meal = friendship_recipe(Meal.super_meal, NPC.kent, 7, {Vegetable.bok_choy: 1, Fruit.cranberries: 1, Vegetable.artichoke: 1})

survival_burger = skill_recipe(Meal.survival_burger, Skill.foraging, 8, {Meal.bread: 1, Forageable.cave_carrot: 1, Vegetable.eggplant: 1})
tom_kha_soup = friendship_recipe(Meal.tom_kha_soup, NPC.sandy, 7, {Forageable.coconut: 1, Fish.shrimp: 1, Mushroom.common: 1})
tortilla_ingredients = {Vegetable.corn: 1}
tortilla_qos = queen_of_sauce_recipe(Meal.tortilla, 1, Season.fall, 7, tortilla_ingredients)
tortilla_saloon = shop_recipe(Meal.tortilla, Region.saloon, 100, tortilla_ingredients)
triple_shot_espresso = shop_recipe(Beverage.triple_shot_espresso, Region.saloon, 5000, {Beverage.coffee: 3})
tropical_curry = shop_recipe(Meal.tropical_curry, Region.island_resort, 2000, {Forageable.coconut: 1, Fruit.pineapple: 1, Fruit.hot_pepper: 1})
trout_soup = queen_of_sauce_recipe(Meal.trout_soup, 1, Season.fall, 14, {Fish.rainbow_trout: 1, WaterItem.green_algae: 1})
vegetable_medley = friendship_recipe(Meal.vegetable_medley, NPC.caroline, 7, {Vegetable.tomato: 1, Vegetable.beet: 1})

magic_elixir = shop_recipe(ModEdible.magic_elixir, Region.adventurer_guild, 3000, {Edible.life_elixir: 1, Mushroom.purple: 1}, ModNames.magic)

baked_berry_oatmeal = shop_recipe(SVEMeal.baked_berry_oatmeal, SVERegion.bear_shop, 0, {Forageable.salmonberry: 15, Forageable.blackberry: 15,
                                                                                        Ingredient.sugar: 1, Ingredient.wheat_flour: 2}, ModNames.sve)
big_bark_burger = friendship_and_shop_recipe(SVEMeal.big_bark_burger, NPC.gus, 5, Region.saloon, 5500,
                                             {SVEFish.puppyfish: 1, Meal.bread: 1, Ingredient.oil: 1}, ModNames.sve)
flower_cookie = shop_recipe(SVEMeal.flower_cookie, SVERegion.bear_shop, 0, {SVEForage.ferngill_primrose: 1, SVEForage.goldenrod: 1,
                                                                            SVEForage.winter_star_rose: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1,
                                                                            AnimalProduct.large_egg: 1}, ModNames.sve)
frog_legs = shop_recipe(SVEMeal.frog_legs, Region.adventurer_guild, 2000, {SVEFish.frog: 1, Ingredient.oil: 1, Ingredient.wheat_flour: 1}, ModNames.sve)
glazed_butterfish = friendship_and_shop_recipe(SVEMeal.glazed_butterfish, NPC.gus, 10, Region.saloon, 4000,
                                               {SVEFish.butterfish: 1, Ingredient.wheat_flour: 1, Ingredient.oil: 1}, ModNames.sve)
mixed_berry_pie = shop_recipe(SVEMeal.mixed_berry_pie, Region.saloon, 3500, {Fruit.strawberry: 6, SVEFruit.salal_berry: 6, Forageable.blackberry: 6,
                                                                             SVEForage.bearberry: 6, Ingredient.sugar: 1, Ingredient.wheat_flour: 1},
                              ModNames.sve)
mushroom_berry_rice = friendship_and_shop_recipe(SVEMeal.mushroom_berry_rice, ModNPC.marlon, 6, Region.adventurer_guild, 1500,
                                                 {SVEForage.poison_mushroom: 3, SVEForage.red_baneberry: 10, Ingredient.rice: 1, Ingredient.sugar: 2},
                                                 ModNames.sve)
seaweed_salad = shop_recipe(SVEMeal.seaweed_salad, Region.fish_shop, 1250, {SVEWaterItem.dulse_seaweed: 2, WaterItem.seaweed: 2, Ingredient.oil: 1},
                            ModNames.sve)
void_delight = friendship_and_shop_recipe(SVEMeal.void_delight, NPC.krobus, 10, Region.sewer, 5000,
                                          {SVEFish.void_eel: 1, Loot.void_essence: 50, Loot.solar_essence: 20}, ModNames.sve)
void_salmon_sushi = friendship_and_shop_recipe(SVEMeal.void_salmon_sushi, NPC.krobus, 10, Region.sewer, 5000,
                                               {Fish.void_salmon: 1, ArtisanGood.void_mayonnaise: 1, WaterItem.seaweed: 3}, ModNames.sve)

mushroom_kebab = friendship_recipe(DistantLandsMeal.mushroom_kebab, ModNPC.goblin, 2, {Mushroom.chanterelle: 1, Mushroom.common: 1,
                                                                                       Mushroom.red: 1, Material.wood: 1}, ModNames.distant_lands)
void_mint_tea = friendship_recipe(DistantLandsMeal.void_mint_tea, ModNPC.goblin, 4, {DistantLandsCrop.void_mint: 1}, ModNames.distant_lands)
crayfish_soup = friendship_recipe(DistantLandsMeal.crayfish_soup, ModNPC.goblin, 6, {Forageable.cave_carrot: 1, Fish.crayfish: 1,
                                                                                     DistantLandsFish.purple_algae: 1, WaterItem.white_algae: 1},
                                  ModNames.distant_lands)
pemmican = friendship_recipe(DistantLandsMeal.pemmican, ModNPC.goblin, 8, {Loot.bug_meat: 1, Fish.any: 1, Forageable.salmonberry: 3,
                                                                           Material.stone: 2}, ModNames.distant_lands)

special_pumpkin_soup = friendship_recipe(BoardingHouseMeal.special_pumpkin_soup, ModNPC.joel, 6, {Vegetable.pumpkin: 2, AnimalProduct.large_goat_milk: 1,
                                                                                                  Vegetable.garlic: 1}, ModNames.boarding_house)
diggers_delight = skill_recipe(ArchaeologyMeal.diggers_delight, ModSkill.archaeology, 3,
                               {Forageable.cave_carrot: 2, Ingredient.sugar: 1, AnimalProduct.milk: 1}, ModNames.archaeology)
rocky_root = skill_recipe(ArchaeologyMeal.rocky_root, ModSkill.archaeology, 7, {Forageable.cave_carrot: 3, Seed.coffee: 1, Material.stone: 1},
                          ModNames.archaeology)
ancient_jello = skill_recipe(ArchaeologyMeal.ancient_jello, ModSkill.archaeology, 9,
                             {WaterItem.cave_jelly: 6, Ingredient.sugar: 5, AnimalProduct.egg: 1, AnimalProduct.milk: 1, Artifact.chipped_amphora: 1},
                             ModNames.archaeology)

grilled_cheese = skill_recipe(TrashyMeal.grilled_cheese, ModSkill.binning, 1, {Meal.bread: 1, ArtisanGood.cheese: 1}, ModNames.binning_skill)
fish_casserole = skill_recipe(TrashyMeal.fish_casserole, ModSkill.binning, 8, {Fish.any: 1, AnimalProduct.milk: 1, Vegetable.carrot: 1}, ModNames.binning_skill)

all_cooking_recipes_by_name = {recipe.meal: recipe for recipe in all_cooking_recipes}
