"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage options in the Aquaria game multiworld randomizer
"""

from dataclasses import dataclass
from Options import Toggle, Choice, DeathLink, PerGameCommonOptions


class IngredientRandomizer(Choice):
    """
    Randomize Ingredients. Select if the simple ingredients (that does not have
    a recipe) should be randomized. If 'common_ingredients' is selected, the
    randomization will exclude the "Red Bulb", "Special Bulb" and "Rukh Egg".
    """
    display_name = "Randomize Ingredients"
    option_off = 0
    option_common_ingredients = 1
    option_all_ingredients = 2
    default = 0


class DishRandomizer(Toggle):
    """Randomize the drop of Dishes (Ingredients with recipe)."""
    display_name = "Dish Randomizer"


class AquarianTranslation(Toggle):
    """Translate to English the Aquarian scripture in the game."""
    display_name = "Translate Aquarian"


class Objective(Choice):
    """
    The game objective can be only to kill the creator or to kill the creator
    and having obtained the three every secret memories
    """
    display_name = "Objective"
    option_kill_the_creator = 0
    option_obtain_secrets_and_kill_the_creator = 1
    default = 0


@dataclass
class AquariaOptions(PerGameCommonOptions):
    """
    Every options in the Aquaria randomizer
    """
    ingredient_randomizer: IngredientRandomizer
    dish_randomizer: DishRandomizer
    aquarian_translation: AquarianTranslation
    objective: Objective
    death_link: DeathLink
