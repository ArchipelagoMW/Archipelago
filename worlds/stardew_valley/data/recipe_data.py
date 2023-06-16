from typing import Dict, List

from worlds.stardew_valley.strings.animal_product_names import AnimalProduct
from worlds.stardew_valley.strings.crop_names import Crop
from worlds.stardew_valley.strings.forageable_names import Forageable
from worlds.stardew_valley.strings.ingredient_names import Ingredient
from worlds.stardew_valley.strings.meal_names import Meal
from worlds.stardew_valley.strings.season_names import Season
from worlds.stardew_valley.strings.villager_names import NPC


class RecipeSource:
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


class ShopSource(RecipeSource):
    region: str
    price: int


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


def queen_of_sauce_recipe(name: str, year: int, season: str, day: int, ingredients: Dict[str, int]) -> CookingRecipe:
    source = QueenOfSauceSource(year, season, day)
    return create_recipe(name, ingredients, source)


def create_recipe(name: str, ingredients: Dict[str, int], source: RecipeSource) -> CookingRecipe:
    recipe = CookingRecipe(name, ingredients, source)
    all_cooking_recipes.append(recipe)
    return recipe


bread = queen_of_sauce_recipe(Meal.bread, 1, Season.summer, 28, {Ingredient.wheat_flour: 1})
blueberry_tart = friendship_recipe(Meal.blueberry_tart, NPC.pierre, 3,
                                   {Crop.blueberry: 1, Ingredient.wheat_flour: 1, Ingredient.sugar: 1,
                                    AnimalProduct.any_egg: 1})
fiddlehead_risotto = queen_of_sauce_recipe(Meal.fiddlehead_risotto, 2, Season.fall, 28,
                                           {Ingredient.oil: 1, Forageable.fiddlehead_fern: 1, Crop.garlic: 1})
