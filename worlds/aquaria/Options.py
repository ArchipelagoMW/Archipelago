"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage options in the Aquaria game multiworld randomizer
"""

from dataclasses import dataclass
from Options import Toggle, Choice, Range, DeathLink, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool


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


class TurtleRandomizer(Choice):
    """Randomize the transportation turtle."""
    display_name = "Turtle Randomizer"
    option_no_turtle_randomization = 0
    option_randomize_all_turtle = 1
    option_randomize_turtle_other_than_the_final_one = 2
    default = 2


class EarlyEnergyForm(DefaultOnToggle):
    """
    Force the Energy Form to be in a location before leaving the areas around the Home Water.
    """
    display_name = "Early Energy Form"


class AquarianTranslation(Toggle):
    """Translate to English the Aquarian scripture in the game."""
    display_name = "Translate Aquarian"


class BigBossesToBeat(Range):
    """
    A number of big bosses to beat before having access to the creator (the final boss). The big bosses are
    "Fallen God", "Mithalan God", "Drunian God", "Sun God" and "The Golem".
    """
    display_name = "Big bosses to beat"
    range_start = 0
    range_end = 5
    default = 0


class MiniBossesToBeat(Range):
    """
    A number of Minibosses to beat before having access to the creator (the final boss). Mini bosses are
    "Nautilus Prime", "Blaster Peg Prime", "Mergog", "Mithalan priests", "Octopus Prime", "Crabbius Maximus",
    "Mantis Shrimp Prime" and "King Jellyfish God Prime". Note that the Energy statue and Simon says are not
    mini bosses.
    """
    display_name = "Mini bosses to beat"
    range_start = 0
    range_end = 8
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

class SkipFirstVision(Toggle):
    """
    The first vision in the game; where Naija transform to Energy Form and get fload by enemy; is quite cool but
    can be quite long when you already know what is going on. This option can be used to skip this vision.
    """
    display_name = "Skip first Naija's vision"

class NoProgressionHardOrHiddenLocation(Toggle):
    """
    Make sure that there is no progression items at hard to get or hard to find locations.
    Those locations that will be very High location (that need beast form, soup and skill to get), every
    location in the bubble cave, locations that need you to cross a false wall without any indication, Arnassi
    race, bosses and mini-bosses. Usefull for those that want a casual run.
    """
    display_name = "No progression in hard or hidden locations"

class LightNeededToGetToDarkPlaces(DefaultOnToggle):
    """
    Make sure that the sun form or the dumbo pet can be aquired before getting to dark places. Be aware that navigating
    in dark place without light is extremely difficult.
    """
    display_name = "Light needed to get to dark places"

class BindSongNeededToGetUnderRockBulb(Toggle):
    """
    Make sure that the bind song can be aquired before having to obtain sing bulb under rocks.
    """
    display_name = "Bind song needed to get sing bulbs under rocks"


class UnconfineHomeWater(Choice):
    """
    Open the way out of Home water area so that Naija can go to open water and beyond without the bind song.
    """
    display_name = "Unconfine Home Water Area"
    option_off = 0
    option_via_energy_door = 1
    option_via_transturtle = 2
    option_via_both = 3
    default = 0


@dataclass
class AquariaOptions(PerGameCommonOptions):
    """
    Every option in the Aquaria randomizer
    """
    start_inventory_from_pool: StartInventoryPool
    objective: Objective
    mini_bosses_to_beat: MiniBossesToBeat
    big_bosses_to_beat: BigBossesToBeat
    turtle_randomizer: TurtleRandomizer
    early_energy_form: EarlyEnergyForm
    light_needed_to_get_to_dark_places: LightNeededToGetToDarkPlaces
    bind_song_needed_to_get_under_rock_bulb: BindSongNeededToGetUnderRockBulb
    unconfine_home_water: UnconfineHomeWater
    no_progression_hard_or_hidden_locations: NoProgressionHardOrHiddenLocation
    ingredient_randomizer: IngredientRandomizer
    dish_randomizer: DishRandomizer
    aquarian_translation: AquarianTranslation
    skip_first_vision: SkipFirstVision
    death_link: DeathLink
