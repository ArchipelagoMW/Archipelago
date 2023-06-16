from typing import Dict

from .game_item import GameItem

class RecipeSource:

class QueenOfSauce(RecipeSource):
    year: int
    season: str
    day: int

class Friendship(RecipeSource):
    npc: str
    hearts: int

class Skill(RecipeSource):
    skill: str
    level: int

class Shop(RecipeSource):
    region: str
    price: int

class ShopTrade(Shop):
    currency: str

class Recipe:
    meal: GameItem
    ingredients: Dict[GameItem, int]
    source: RecipeSource

    def __repr__(self):
        return f"{self.meal.name} [{self.meal.item_id}] (Source: {self.source} |" \
               f" Ingredients: {self.ingredients})"