from typing import Dict, List

from worlds.stardew_valley.strings.animal_product_names import AnimalProduct
from worlds.stardew_valley.strings.artisan_good_names import ArtisanGood
from worlds.stardew_valley.strings.crop_names import Fruit, Vegetable
from worlds.stardew_valley.strings.fish_names import Fish, WaterItem
from worlds.stardew_valley.strings.forageable_names import Forageable
from worlds.stardew_valley.strings.ingredient_names import Ingredient
from worlds.stardew_valley.strings.food_names import Meal, Beverage
from worlds.stardew_valley.strings.region_names import Region
from worlds.stardew_valley.strings.season_names import Season
from worlds.stardew_valley.strings.skill_names import Skill
from worlds.stardew_valley.strings.villager_names import NPC


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


bread = queen_of_sauce_recipe(Meal.bread, 1, Season.summer, 28, {Ingredient.wheat_flour: 1})
blueberry_tart = friendship_recipe(Meal.blueberry_tart, NPC.pierre, 3,
                                   {Fruit.blueberry: 1,
                                    Ingredient.wheat_flour: 1,
                                    Ingredient.sugar: 1,
                                    AnimalProduct.any_egg: 1})
fiddlehead_risotto = queen_of_sauce_recipe(Meal.fiddlehead_risotto, 2, Season.fall, 28,
                                           {Ingredient.oil: 1,
                                            Forageable.fiddlehead_fern: 1,
                                            Vegetable.garlic: 1})

complete_breakfast = queen_of_sauce_recipe(Meal.complete_breakfast, 2, Season.spring, 21,
                                           {Meal.fried_egg: 1,
                                            AnimalProduct.milk: 1,
                                            Meal.hashbrowns: 1,
                                            Meal.pancakes: 1})

hashbrowns = queen_of_sauce_recipe(Meal.hashbrowns, 2, Season.spring, 14,
                                   {Vegetable.potato: 1, Ingredient.oil: 1})

pancakes = queen_of_sauce_recipe(Meal.pancakes, 1, Season.summer, 14,
                                 {Ingredient.wheat_flour: 1,
                                  AnimalProduct.chicken_egg: 1})

fried_egg = starter_recipe(Meal.fried_egg, {AnimalProduct.chicken_egg: 1})

ginger_ale = shop_recipe(Beverage.ginger_ale, Region.volcano_dwarf_shop, 1000, {Forageable.ginger: 3, Ingredient.sugar: 1})
ice_cream = friendship_recipe(Meal.ice_cream, NPC.jodi, 7, {AnimalProduct.cow_milk: 1, Ingredient.sugar: 1})
maki_roll = queen_of_sauce_recipe(Meal.maki_roll, 1, Season.summer, 21, {Fish.any: 1, WaterItem.seaweed: 1, Ingredient.rice: 1})
miners_treat = skill_recipe(Meal.miners_treat, Skill.mining, 3, {Forageable.cave_carrot: 2, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1})
omelet = queen_of_sauce_recipe(Meal.omelet, 1, Season.spring, 28, {AnimalProduct.chicken_egg: 1, AnimalProduct.cow_milk: 1})
parsnip_soup = friendship_recipe(Meal.parsnip_soup, NPC.caroline, 3, {Vegetable.parsnip: 1, AnimalProduct.cow_milk: 1, Ingredient.vinegar: 1})
pink_cake = queen_of_sauce_recipe(Meal.pink_cake, 2, Season.summer, 21, {Fruit.melon: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.chicken_egg: 1})
pizza_ingredients = {Ingredient.wheat_flour: 1, Vegetable.tomato: 1, ArtisanGood.cheese: 1}
pizza_qos = queen_of_sauce_recipe(Meal.pizza, 2, Season.spring, 7, pizza_ingredients)
pizza_saloon = shop_recipe(Meal.pizza, Region.saloon, 150, pizza_ingredients)
pumpkin_pie = queen_of_sauce_recipe(Meal.pumpkin_pie, 1, Season.winter, 21, {Vegetable.pumpkin: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1, AnimalProduct.cow_milk: 1})
roasted_hazelnuts = queen_of_sauce_recipe(Meal.roasted_hazelnuts, 2, Season.summer, 28, {Forageable.hazelnut: 3})
salad = friendship_recipe(Meal.salad, NPC.emily, 3, {Forageable.leek: 1, Forageable.dandelion: 1, Ingredient.vinegar: 1})
spaghetti = friendship_recipe(Meal.spaghetti, NPC.lewis, 3, {Vegetable.tomato: 1, Ingredient.wheat_flour: 1})
tortilla_ingredients = {Vegetable.corn: 1}
tortilla_qos = queen_of_sauce_recipe(Meal.tortilla, 1, Season.fall, 7, tortilla_ingredients)
tortilla_saloon = shop_recipe(Meal.tortilla, Region.saloon, 100, tortilla_ingredients)
triple_shot_espresso = shop_recipe(Beverage.triple_shot_espresso, Region.saloon, 5000, {Beverage.coffee: 3})
algae_soup = friendship_recipe(Meal.algae_soup, NPC.clint, 3, {WaterItem.green_algae: 4})










