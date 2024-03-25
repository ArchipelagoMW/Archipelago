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


class BigBossesToBeat(Choice):
    """
    A number of big bosses to beat before having access to the creator (the final boss). The big bosses are
    "Fallen God", "Mithalan God", "Drunian God", "Sun God" and "The Golem".
    """
    display_name = "Big bosses to beat"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    default = 0



class MiniBossesToBeat(Choice):
    """
    A number of Minibosses to beat before having access to the creator (the final boss). Mini bosses are
    "Nautilus Prime", "Blaster Peg Prime", "Mergog", "Mithalan priests", "Octopus Prime", "Crabbius Maximus",
    "Mantis Shrimp Prime" and "King Jellyfish God Prime". Note that the Energy statue and Simon says are not
    mini bosses.
    """
    display_name = "Mini bosses to beat"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_6 = 6
    option_7 = 7
    option_8 = 8
    default = 0


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
    Every option in the Aquaria randomizer
    """
    ingredient_randomizer: IngredientRandomizer
    dish_randomizer: DishRandomizer
    aquarian_translation: AquarianTranslation
    objective: Objective
    big_bosses_to_beat: BigBossesToBeat
    mini_bosses_to_beat: MiniBossesToBeat
    death_link: DeathLink
