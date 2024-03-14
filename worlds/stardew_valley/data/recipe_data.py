from typing import Dict, List

from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Fruit, Vegetable
from ..strings.fish_names import Fish, WaterItem
from ..strings.flower_names import Flower
from ..strings.forageable_names import Forageable
from ..strings.ingredient_names import Ingredient
from ..strings.food_names import Meal, Beverage
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.skill_names import Skill
from ..strings.villager_names import NPC


class RecipeSource:
    pass


class StarterSource(RecipeSource):
    pass


class QueenOfSauceSource(RecipeSource):
    year: int
    season: str
    day: int

    def __init__(self, year: int, season: str, day: int):
        self.year = year
        self.season = season
        self.day = day


class FriendshipSource(RecipeSource):
    friend: str
    hearts: int

    def __init__(self, friend: str, hearts: int):
        self.friend = friend
        self.hearts = hearts


class SkillSource(RecipeSource):
    skill: str
    level: int

    def __init__(self, skill: str, level: int):
        self.skill = skill
        self.level = level


class ShopSource(RecipeSource):
    region: str
    price: int

    def __init__(self, region: str, price: int):
        self.region = region
        self.price = price


class ShopTradeSource(ShopSource):
    currency: str


class CookingRecipe:
    meal: str
    ingredients: Dict[str, int]
    source: RecipeSource

    def __init__(self, meal: str, ingredients: Dict[str, int], source: RecipeSource):
        self.meal = meal
        self.ingredients = ingredients
        self.source = source

    def __repr__(self):
        return f"{self.meal} (Source: {self.source} |" \
               f" Ingredients: {self.ingredients})"


all_cooking_recipes: List[CookingRecipe] = []


def friendship_recipe(name: str, friend: str, hearts: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = FriendshipSource(friend, hearts)
    return create_recipe(name, ingredients, source)


def skill_recipe(name: str, skill: str, level: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = SkillSource(skill, level)
    return create_recipe(name, ingredients, source)


def shop_recipe(name: str, region: str, price: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = ShopSource(region, price)
    return create_recipe(name, ingredients, source)


def queen_of_sauce_recipe(name: str, year: int, season: str, day: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = QueenOfSauceSource(year, season, day)
    return create_recipe(name, ingredients, source)


def starter_recipe(name: str, ingredients: Dict[str, int]) -> CookingRecipe:
    source = StarterSource()
    return create_recipe(name, ingredients, source)


def create_recipe(name: str, ingredients: Dict[str, int], source: RecipeSource) -> CookingRecipe:
    recipe = CookingRecipe(name, ingredients, source)
    all_cooking_recipes.append(recipe)
    return recipe


algae_soup = friendship_recipe(Meal.algae_soup, NPC.clint, 3, {WaterItem.green_algae: 4})
artichoke_dip = queen_of_sauce_recipe(Meal.artichoke_dip, 1, Season.fall, 28, {Vegetable.artichoke: 1, AnimalProduct.cow_milk: 1})
baked_fish = queen_of_sauce_recipe(Meal.baked_fish, 1, Season.summer, 7, {Fish.sunfish: 1, Fish.bream: 1, Ingredient.wheat_flour: 1})
bean_hotpot = friendship_recipe(Meal.bean_hotpot, NPC.clint, 7, {Vegetable.green_bean: 2})
blackberry_cobbler_ingredients = {Forageable.blackberry: 2, Ingredient.sugar: 1, Ingredient.wheat_flour: 1}
blackberry_cobbler_qos = queen_of_sauce_recipe(Meal.blackberry_cobbler, 2, Season.fall, 14, blackberry_cobbler_ingredients)
blueberry_tart = friendship_recipe(Meal.blueberry_tart, NPC.pierre, 3, {Fruit.blueberry: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.any_egg: 1})
bread = queen_of_sauce_recipe(Meal.bread, 1, Season.summer, 28, {Ingredient.wheat_flour: 1})
cheese_cauliflower = friendship_recipe(Meal.cheese_cauliflower, NPC.pam, 3, {Vegetable.cauliflower: 1, ArtisanGood.cheese: 1})
chocolate_cake_ingredients = {Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1}
chocolate_cake_qos = queen_of_sauce_recipe(Meal.chocolate_cake, 1, Season.winter, 14, chocolate_cake_ingredients)
chowder = friendship_recipe(Meal.chowder, NPC.willy, 3, {WaterItem.clam: 1, AnimalProduct.cow_milk: 1})
complete_breakfast = queen_of_sauce_recipe(Meal.complete_breakfast, 2, Season.spring, 21, {Meal.fried_egg: 1, AnimalProduct.milk: 1, Meal.hashbrowns: 1, Meal.pancakes: 1})
crab_cakes_ingredients = {Fish.crab: 1, Ingredient.wheat_flour: 1, AnimalProduct.chicken_egg: 1, Ingredient.oil: 1}
crab_cakes_qos = queen_of_sauce_recipe(Meal.crab_cakes, 2, Season.fall, 21, crab_cakes_ingredients)
cranberry_candy = queen_of_sauce_recipe(Meal.cranberry_candy, 1, Season.winter, 28, {Fruit.cranberries: 1, Fruit.apple: 1, Ingredient.sugar: 1})
crispy_bass = friendship_recipe(Meal.crispy_bass, NPC.kent, 3, {Fish.largemouth_bass: 1, Ingredient.wheat_flour: 1, Ingredient.oil: 1})
dish_o_the_sea = skill_recipe(Meal.dish_o_the_sea, Skill.fishing, 3, {Fish.sardine: 2, Meal.hashbrowns: 1})
eggplant_parmesan = friendship_recipe(Meal.eggplant_parmesan, NPC.lewis, 7, {Vegetable.eggplant: 1, Vegetable.tomato: 1})
escargot = friendship_recipe(Meal.escargot, NPC.willy, 5, {Fish.snail: 1, Vegetable.garlic: 1})
farmer_lunch = skill_recipe(Meal.farmer_lunch, Skill.farming, 3, {Meal.omelet: 2, Vegetable.parsnip: 1})
fiddlehead_risotto = queen_of_sauce_recipe(Meal.fiddlehead_risotto, 2, Season.fall, 28, {Ingredient.oil: 1, Forageable.fiddlehead_fern: 1, Vegetable.garlic: 1})
fish_taco = friendship_recipe(Meal.fish_taco, NPC.linus, 7, {Fish.tuna: 1, Meal.tortilla: 1, Vegetable.red_cabbage: 1, ArtisanGood.mayonnaise: 1})
fried_calamari = friendship_recipe(Meal.fried_calamari, NPC.jodi, 3, {Fish.squid: 1, Ingredient.wheat_flour: 1, Ingredient.oil: 1})
fried_eel = friendship_recipe(Meal.fried_eel, NPC.george, 3, {Fish.eel: 1, Ingredient.oil: 1})
fried_egg = starter_recipe(Meal.fried_egg, {AnimalProduct.chicken_egg: 1})
fried_mushroom = friendship_recipe(Meal.fried_mushroom, NPC.demetrius, 3, {Forageable.common_mushroom: 1, Forageable.morel: 1, Ingredient.oil: 1})
fruit_salad = queen_of_sauce_recipe(Meal.fruit_salad, 2, Season.fall, 7, {Fruit.blueberry: 1, Fruit.melon: 1, Fruit.apricot: 1})
ginger_ale = shop_recipe(Beverage.ginger_ale, Region.volcano_dwarf_shop, 1000, {Forageable.ginger: 3, Ingredient.sugar: 1})
glazed_yams = queen_of_sauce_recipe(Meal.glazed_yams, 1, Season.fall, 21, {Vegetable.yam: 1, Ingredient.sugar: 1})
hashbrowns = queen_of_sauce_recipe(Meal.hashbrowns, 2, Season.spring, 14, {Vegetable.potato: 1, Ingredient.oil: 1})
ice_cream = friendship_recipe(Meal.ice_cream, NPC.jodi, 7, {AnimalProduct.cow_milk: 1, Ingredient.sugar: 1})
maki_roll = queen_of_sauce_recipe(Meal.maki_roll, 1, Season.summer, 21, {Fish.any: 1, WaterItem.seaweed: 1, Ingredient.rice: 1})
maple_bar = queen_of_sauce_recipe(Meal.maple_bar, 2, Season.summer, 14, {ArtisanGood.maple_syrup: 1, Ingredient.sugar: 1, Ingredient.wheat_flour: 1})
miners_treat = skill_recipe(Meal.miners_treat, Skill.mining, 3, {Forageable.cave_carrot: 2, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1})
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
poppyseed_muffin = queen_of_sauce_recipe(Meal.poppyseed_muffin, 2, Season.winter, 7, {Flower.poppy: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1})
pumpkin_pie_ingredients = {Vegetable.pumpkin: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1}
pumpkin_pie_qos = queen_of_sauce_recipe(Meal.pumpkin_pie, 1, Season.winter, 21, pumpkin_pie_ingredients)
red_plate = friendship_recipe(Meal.red_plate, NPC.emily, 7, {Vegetable.red_cabbage: 1, Vegetable.radish: 1})
rhubarb_pie = friendship_recipe(Meal.rhubarb_pie, NPC.marnie, 7, {Fruit.rhubarb: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1})
rice_pudding = friendship_recipe(Meal.rice_pudding, NPC.evelyn, 7, {AnimalProduct.milk: 1, Ingredient.sugar: 1, Ingredient.rice: 1})
roasted_hazelnuts = queen_of_sauce_recipe(Meal.roasted_hazelnuts, 2, Season.summer, 28, {Forageable.hazelnut: 3})
roots_platter = skill_recipe(Meal.roots_platter, Skill.combat, 3, {Forageable.cave_carrot: 1, Forageable.winter_root: 1})
salad = friendship_recipe(Meal.salad, NPC.emily, 3, {Forageable.leek: 1, Forageable.dandelion: 1, Ingredient.vinegar: 1})
salmon_dinner = friendship_recipe(Meal.salmon_dinner, NPC.gus, 3, {Fish.salmon: 1, Vegetable.amaranth: 1, Vegetable.kale: 1})
sashimi = friendship_recipe(Meal.sashimi, NPC.linus, 3, {Fish.any: 1})
spaghetti = friendship_recipe(Meal.spaghetti, NPC.lewis, 3, {Vegetable.tomato: 1, Ingredient.wheat_flour: 1})
stir_fry_ingredients = {Forageable.cave_carrot: 1, Forageable.common_mushroom: 1, Vegetable.kale: 1, Ingredient.sugar: 1}
stir_fry_qos = queen_of_sauce_recipe(Meal.stir_fry, 1, Season.spring, 7, stir_fry_ingredients)
stuffing = friendship_recipe(Meal.stuffing, NPC.pam, 7, {Meal.bread: 1, Fruit.cranberries: 1, Forageable.hazelnut: 1})
survival_burger = skill_recipe(Meal.survival_burger, Skill.foraging, 2, {Meal.bread: 1, Forageable.cave_carrot: 1, Vegetable.eggplant: 1})
tortilla_ingredients = {Vegetable.corn: 1}
tortilla_qos = queen_of_sauce_recipe(Meal.tortilla, 1, Season.fall, 7, tortilla_ingredients)
tortilla_saloon = shop_recipe(Meal.tortilla, Region.saloon, 100, tortilla_ingredients)
triple_shot_espresso = shop_recipe(Beverage.triple_shot_espresso, Region.saloon, 5000, {Beverage.coffee: 3})
tropical_curry = shop_recipe(Meal.tropical_curry, Region.island_resort, 2000, {Forageable.coconut: 1, Fruit.pineapple: 1, Fruit.hot_pepper: 1})
vegetable_medley = friendship_recipe(Meal.vegetable_medley, NPC.caroline, 7, {Vegetable.tomato: 1, Vegetable.beet: 1})







