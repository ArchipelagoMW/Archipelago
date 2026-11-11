from dataclasses import dataclass, field

from .game_item import Source

RecipeIngredient = tuple[str, int]


@dataclass(frozen=True)
class CookingRecipe:
    name: str
    ingredients: tuple[RecipeIngredient, ...]
    sources: tuple[Source, ...] = field(kw_only=True)

    def __repr__(self):
        return f"{self.name} ({self.ingredients})"
