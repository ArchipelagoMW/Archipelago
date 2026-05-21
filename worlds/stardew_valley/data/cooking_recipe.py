from dataclasses import dataclass, field
from typing import List

from .game_item import Source
from .recipe_source import RecipeSource, FriendshipSource, SkillSource, QueenOfSauceSource, ShopSource, StarterSource, ShopTradeSource, ShopFriendshipSource

RecipeIngredient = tuple[str, int]


@dataclass(frozen=True)
class CookingRecipe:
    name: str
    ingredients: tuple[RecipeIngredient, ...]
    sources: tuple[Source, ...] = field(kw_only=True)

    def __repr__(self):
        return f"{self.name} ({self.ingredients})"


all_cooking_recipes: List[CookingRecipe] = []


def friendship_recipe(name: str, friend: str, hearts: int, ingredients: dict[str, int], /, *, content_pack: str | None = None) -> CookingRecipe:
    source = FriendshipSource(friend, hearts)
    return create_recipe(name, ingredients, source, content_pack)


def friendship_and_shop_recipe(name: str, friend: str, hearts: int, region: str, price: int, ingredients: dict[str, int],
                               /, *, content_pack: str | None = None) -> CookingRecipe:
    source = ShopFriendshipSource(friend, hearts, region, price)
    return create_recipe(name, ingredients, source, content_pack)


def skill_recipe(name: str, skill: str, level: int, ingredients: dict[str, int], /, *, content_pack: str | None = None) -> CookingRecipe:
    source = SkillSource(skill, level)
    return create_recipe(name, ingredients, source, content_pack)


def shop_recipe(name: str, region: str, price: int, ingredients: dict[str, int], /, *, content_pack: str | None = None) -> CookingRecipe:
    source = ShopSource(region, price)
    return create_recipe(name, ingredients, source, content_pack)


def shop_trade_recipe(name: str, region: str, currency: str, price: int, ingredients: dict[str, int], /, *, content_pack: str | None = None) -> CookingRecipe:
    source = ShopTradeSource(region, currency, price)
    return create_recipe(name, ingredients, source, content_pack)


def queen_of_sauce_recipe(name: str, year: int, season: str, day: int, ingredients: dict[str, int], /, *, content_pack: str | None = None) -> CookingRecipe:
    source = QueenOfSauceSource(year, season, day)
    return create_recipe(name, ingredients, source, content_pack)


def starter_recipe(name: str, ingredients: dict[str, int], /, *, content_pack: str | None = None) -> CookingRecipe:
    source = StarterSource()
    return create_recipe(name, ingredients, source, content_pack)


def create_recipe(name: str, ingredients: dict[str, int], source: RecipeSource, content_pack: str | None = None) -> CookingRecipe:
    recipe = CookingRecipe(name, ingredients, source, content_pack)
    all_cooking_recipes.append(recipe)
    return recipe




all_cooking_recipes_by_name = {recipe.meal: recipe for recipe in all_cooking_recipes}
