"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage options in the Aquaria game multiworld randomizer
"""

from dataclasses import dataclass
from Options import Toggle, Choice, Range, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool


class IngredientRandomizer(Choice):
    """
    Select if the simple ingredients (that do not have a recipe) should be randomized.
    If "Common Ingredients" is selected, the randomization will exclude the "Red Bulb", "Special Bulb" and "Rukh Egg".
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
    option_none = 0
    option_all = 1
    option_all_except_final = 2
    default = 2


class EarlyBindSong(Choice):
    """
    Force the Bind song to be in a location early in the multiworld (It is not guaranteed to be in your world).
    """
    display_name = "Early Bind song"
    option_off = 0
    option_early = 1
    option_early_and_local = 2
    default = 1


class EarlyEnergyForm(Choice):
    """
    Force the Energy form to be in a location early in the multiworld (It is not guaranteed to be in your world).
    """
    display_name = "Early Energy form"
    option_off = 0
    option_early = 1
    option_early_and_local = 2
    default = 1


class AquarianTranslation(Toggle):
    """Translate the Aquarian scripture in the game into English."""
    display_name = "Translate Aquarian"


class BigBossesToBeat(Range):
    """
    The number of big bosses to beat before having access to the creator (the final boss). The big bosses are
    "Fallen God", "Mithalan God", "Drunian God", "Lumerean God" and "The Golem".
    """
    display_name = "Big bosses to beat"
    range_start = 0
    range_end = 5
    default = 0


class MiniBossesToBeat(Range):
    """
    The number of minibosses to beat before having access to the creator (the final boss). The minibosses are
    "Nautilus Prime", "Blaster Peg Prime", "Mergog", "Mithalan priests", "Octopus Prime", "Crabbius Maximus",
    "Mantis Shrimp Prime" and "King Jellyfish God Prime".
    Note that the Energy Statue and Simon Says are not minibosses.
    """
    display_name = "Minibosses to beat"
    range_start = 0
    range_end = 8
    default = 0


class Objective(Choice):
    """
    The game objective can be to kill the creator or to kill the creator after obtaining all three secret memories.
    """
    display_name = "Objective"
    option_kill_the_creator = 0
    option_obtain_secrets_and_kill_the_creator = 1
    default = 0


class SkipFirstVision(Toggle):
    """
    The first vision in the game, where Naija transforms into Energy Form and gets flooded by enemies, is quite cool but
    can be quite long when you already know what is going on. This option can be used to skip this vision.
    """
    display_name = "Skip Naija's first vision"


class NoProgressionHardOrHiddenLocation(Toggle):
    """
    Make sure that there are no progression items at hard-to-reach or hard-to-find locations.
    Those locations are very High locations (that need beast form, soup and skill to get),
    every location in the bubble cave, locations where need you to cross a false wall without any indication,
    the Arnassi race, bosses and minibosses. Useful for those that want a more casual run.
    """
    display_name = "No progression in hard or hidden locations"


class NoProgressionSimonSays(Toggle):
    """
    Make sure that there are no progression items in the says area
    """
    display_name = "No progression in Simon says area"


class NoProgressionKelpForest(Toggle):
    """
    Make sure that there are no progression items in Kelp Forest (excluding Simon says area).
    Can be usefull to get smaller runs.
    """
    display_name = "No progression in Kelp Forest"


class NoProgressionVeil(Toggle):
    """
    Make sure that there are no progression items in the Veil. Can be usefull to get smaller runs.
    """
    display_name = "No progression in the Veil"


class NoProgressionMithalas(Toggle):
    """
    Make sure that there are no progression items in the Mithalas (city, castle and cathedral).
    Can be usefull to get smaller runs.
    """
    display_name = "No progression in Mithalas"


class NoProgressionEnergyTemple(Toggle):
    """
    Make sure that there are no progression items in the Energy Temple. Can be usefull to get smaller runs.
    """
    display_name = "No progression in the Energy Temple"


class NoProgressionArnassiRuins(Toggle):
    """
    Make sure that there are no progression items in the Arnassi Ruins. Can be usefull to get smaller runs.
    Note that if the Transportation turtle are not randomize, this include Simon Says area.
    """
    display_name = "No progression in Arnassi Ruins"


class NoProgressionFrozenVeil(Toggle):
    """
    Make sure that there are no progression items in the Frozen Veil (including Ice Cavern and Bubble Cave)
    Can be usefull to get smaller runs.
    """
    display_name = "No progression in the Frozen Veil"


class NoProgressionAbyss(Toggle):
    """
    Make sure that there are no progression items in the Abyss
    Can be usefull to get smaller runs.
    """
    display_name = "No progression in the Abyss"


class NoProgressionSunkenCity(Toggle):
    """
    Make sure that there are no progression items in the Sunken City
    Can be usefull to get smaller runs.
    """
    display_name = "No progression in the Sunken City"


class NoProgressionBody(Toggle):
    """
    Make sure that there are no progression items in the Body (including the before boss transturtle room
    and the boss location. Can be usefull to get smaller runs.
    """
    display_name = "No progression in the Body"


class LightNeededToGetToDarkPlaces(DefaultOnToggle):
    """
    Make sure that the sun form or the dumbo pet can be acquired before getting to dark places.
    Be aware that navigating in dark places without light is extremely difficult.
    """
    display_name = "Light needed to get to dark places"


class BindSongNeededToGetUnderRockBulb(Toggle):
    """
    Make sure that the bind song can be acquired before having to obtain sing bulbs under rocks.
    """
    display_name = "Bind song needed to get sing bulbs under rocks"


class BlindGoal(Toggle):
    """
    Hide the goal's requirements from the help page so that you have to go to the last boss door to know
    what is needed to access the boss.
    """
    display_name = "Hide the goal's requirements"


class InfiniteHotSoup(DefaultOnToggle):
    """
    As soon as a hot soup is received, the user will never run out of those dishes.
    This option is recommended if using Ingredient randomization since Hot soup ingredients can be hard to get.
    """
    display_name = "Infinite Hot Soup"


class OpenBodyTongue(Toggle):
    """
    Remove the body tongue making the body accessible without going in the sunken city
    """
    display_name = "Open the body tongue"


class SkipFinalBoss3rdForm(Toggle):
    """
    The Final boss third form (the hide and seek form) can be easy and quite long. So, this option can be used
    to skip this form.
    """
    display_name = "Skip final boss third form"


class MaximumIngredientAmount(Range):
    """
    The maximum number of the same ingredients that can be stacked on the ingredient inventory
    """
    display_name = "Maximum ingredient amount"
    range_start = 2
    range_end = 20
    default = 8


class UnconfineHomeWater(Choice):
    """
    Open the way out of the Home Waters area so that Naija can go to open water and beyond without the bind song.
    Note that if you put this option off, it is recommended to activate the Early Energy form and Early Bind Song
    options.
    """
    display_name = "Unconfine Home Waters Area"
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
    early_bind_song: EarlyBindSong
    light_needed_to_get_to_dark_places: LightNeededToGetToDarkPlaces
    bind_song_needed_to_get_under_rock_bulb: BindSongNeededToGetUnderRockBulb
    unconfine_home_water: UnconfineHomeWater
    no_progression_hard_or_hidden_locations: NoProgressionHardOrHiddenLocation
    no_progression_simon_says: NoProgressionSimonSays
    no_progression_kelp_forest: NoProgressionKelpForest
    no_progression_veil: NoProgressionVeil
    no_progression_mithalas: NoProgressionMithalas
    no_progression_energy_temple: NoProgressionEnergyTemple
    no_progression_arnassi_ruins: NoProgressionArnassiRuins
    no_progression_frozen_veil: NoProgressionFrozenVeil
    no_progression_abyss: NoProgressionAbyss
    no_progression_sunken_city: NoProgressionSunkenCity
    no_progression_body: NoProgressionBody
    ingredient_randomizer: IngredientRandomizer
    dish_randomizer: DishRandomizer
    aquarian_translation: AquarianTranslation
    skip_first_vision: SkipFirstVision
    blind_goal: BlindGoal
    infinite_hot_soup: InfiniteHotSoup
    open_body_tongue: OpenBodyTongue
    maximum_ingredient_amount: MaximumIngredientAmount
    skip_final_boss_3rd_form: SkipFinalBoss3rdForm
