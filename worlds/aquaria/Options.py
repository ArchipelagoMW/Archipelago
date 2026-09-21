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
    rich_text_doc = True
    option_off = 0
    alias_false = 0
    option_common_ingredients = 1
    alias_on = 1
    alias_true = 1
    option_all_ingredients = 2
    default = 0


class DishRandomizer(Toggle):
    """Randomize the drop of Dishes (Ingredients with recipe)."""
    display_name = "Dish Randomizer"
    rich_text_doc = True


class TurtleRandomizer(Choice):
    """
    Randomize the transportation turtle.

    If the objective is "killing the four gods" or "Gods and Creator", the abyss and body turtle will not be randomized.
    """
    display_name = "Turtle Randomizer"
    rich_text_doc = True
    option_none = 0
    alias_off = 0
    alias_false = 0
    option_all = 1
    option_all_except_final = 2
    alias_on = 2
    alias_true = 2
    default = 2


class EarlyBindSong(Choice):
    """
    Force the Bind song to be in a location early in the multiworld (or directly in your world if Early and Local is
    selected).
    """
    display_name = "Early Bind song"
    rich_text_doc = True
    option_off = 0
    alias_false = 0
    option_early = 1
    alias_on = 1
    alias_true = 1
    option_early_and_local = 2
    default = 1


class EarlyEnergyForm(Choice):
    """
    Force the Energy form to be in a location early in the multiworld (or directly in your world if Early and Local is
    selected).
    """
    display_name = "Early Energy form"
    rich_text_doc = True
    option_off = 0
    alias_false = 0
    option_early = 1
    alias_on = 1
    alias_true = 1
    option_early_and_local = 2
    default = 1


class AquarianTranslation(Toggle):
    """Translate the Aquarian scripture in the game into English."""
    display_name = "Translate Aquarian"
    rich_text_doc = True


class BigBossesToBeat(Range):
    """
    The number of big bosses to beat before having access to the creator (the final boss).

    The big bosses are "Fallen God", "Mithalan God", "Drunian God", "Lumerean God" and "The Golem".

    Has no effect if the objective is "killing the four gods" or "Gods and Creator".
    """
    display_name = "Big bosses to beat"
    rich_text_doc = True
    range_start = 0
    range_end = 5
    default = 0


class MiniBossesToBeat(Range):
    """
    The number of minibosses to beat before having access to the goal.

    The minibosses are "Nautilus Prime", "Blaster Peg Prime", "Mergog", "Mithalan priests", "Octopus Prime",
    "Crabbius Maximus", "Mantis Shrimp Prime" and "King Jellyfish God Prime".

    Note that the "Energy Statue" and "Simon Says" are not minibosses.

    Also note that if the objective is "killing the four enemy gods" or "Gods and creator", it might be needed to go in the abyss and
    bubble cave to kill "King Jellyfish God Prime" and "Mantis Shrimp Prime".
    """
    display_name = "Minibosses to beat"
    rich_text_doc = True
    range_start = 0
    range_end = 8
    default = 0


class Objective(Choice):
    """
    **Kill the Creator:** Get to the final boss (the Creator) and beat all it's forms.

    **Obtain secrets and kill the Creator:** like the "Kill the Creator", but need to find all three secret memories
    before getting to the Creator.

    **Killing the four gods:**, Beat all four enemy gods ("Fallen God", "Mithalan God", "Drunian God", "Lumerean God").

    **Gods and Creator:** like "Killing the four gods" but you also have to beat the creator.
    """
    display_name = "Objective"
    rich_text_doc = True
    option_kill_the_creator = 0
    option_obtain_secrets_and_kill_the_creator = 1
    option_killing_the_four_gods = 2
    option_gods_and_creator = 3
    default = 0


class SkipFirstVision(Toggle):
    """
    Skip the first vision in the game, where Naija transforms into Energy Form and gets flooded by enemies.
    """
    display_name = "Skip Naija's first vision"
    rich_text_doc = True


class LightNeededToGetToDarkPlaces(Choice):
    """
    Make sure that the sun form or the dumbo pet can be acquired before getting to dark places.

    Be aware that navigating in dark places without light is extremely difficult.

    You can also force the sun form to be accessible by using the "sun form" option.
    """
    display_name = "Light needed to get to dark places"
    rich_text_doc = True
    option_off = 0
    alias_false = 0
    option_on = 1
    alias_true = 1
    option_sun_form = 2
    default = 1


class BindSongNeededToGetUnderRockBulb(DefaultOnToggle):
    """
    Make sure that the bind song can be acquired before having to obtain sing bulbs under rocks.
    """
    display_name = "Bind song needed to get sing bulbs under rocks"
    rich_text_doc = True


class BlindGoal(Toggle):
    """
    Hide the goal's requirements from the help page so that you don't know what is needed to goal.

    Note that when you get to the final boss door (or you beat the last gods when the "Killing the four gods"
    is selected) you can then see the requirements in the help page.
    """
    display_name = "Hide the goal's requirements"
    rich_text_doc = True


class InfiniteHotSoup(DefaultOnToggle):
    """
    As soon as a "hot soup" is received, the user will never run out of this dish.

    This option is recommended if using Ingredient randomization since "hot soup" ingredients may become hard to get
    and the "hot soup" is necessary to get to some locations.
    """
    display_name = "Infinite Hot Soup"
    rich_text_doc = True


class SaveHealing(DefaultOnToggle):
    """
    When you save, Naija is healed back to full health. If disabled, saving won't heal Naija.

    Note that Naija can still heal by sleeping in some beds in the game (including in her home).
    """
    display_name = "Save heal Naija"
    rich_text_doc = True


class OpenBodyTongue(Toggle):
    """
    Remove the body tongue making the body accessible without going in the sunken city
    """
    display_name = "Open the body tongue"
    rich_text_doc = True


class SkipFinalBoss3rdForm(Toggle):
    """
    The Final boss third form (the hide and seek form) can be easy and quite long. So, this option can be used
    to skip this form.

    Note that you will still need to deliver the final blow to the 3rd form in order to activate the 4th form animation.
    """
    display_name = "Skip final boss third form"


class MaximumIngredientAmount(Range):
    """
    The maximum number of the same ingredients that can be stacked on the ingredient inventory.
    """
    display_name = "Maximum ingredient amount"
    rich_text_doc = True
    range_start = 2
    range_end = 20
    default = 8


class UnconfineHomeWater(Choice):
    """
    Open the way out of the Home Waters area so that Naija can go to open water and beyond without the bind song.

    **Via energy door:** Open the energy door between the home waters and the open waters

    **Via transturtle:** Remove the rock blocking the home water transturtle.

    Note that if you turn this option off, it is recommended to turn on the Early Energy form and Early Bind Song
    options.
    """
    display_name = "Unconfine Home Waters Area"
    rich_text_doc = True
    option_off = 0
    alias_false = 0
    option_via_energy_door = 1
    option_via_transturtle = 2
    option_via_both = 3
    alias_on = 3
    alias_true = 3
    default = 0


class ThroneAsLocation(Toggle):
    """
    If enabled, sitting on the Mithalas City Castle throne (with the seal on it) will be a location and opening the
    door to the Mithalas Cathedral will be an item.
    """
    display_name = "Throne as a location"
    rich_text_doc = True


class NoProgressionHardOrHiddenLocation(Toggle):
    """
    Make sure that there are no progression items at hard-to-reach or hard-to-find locations.

    Those locations are very High locations (that need beast form, soup and skill to get), every location in the
    bubble cave, locations where need you to cross a false wall without any indication, the Arnassi race,
    bosses and minibosses.

    Useful for those that want a more casual run.
    """
    display_name = "No progression in hard or hidden locations"
    rich_text_doc = True


class NoProgressionSimonSays(Toggle):
    """
    Make sure that there are no progression items in the says area.
    """
    display_name = "No progression in Simon says area"
    rich_text_doc = True


class NoProgressionKelpForest(Toggle):
    """
    Make sure that there are no progression items in Kelp Forest (excluding Simon says area).

    Can be useful to get smaller runs.
    """
    display_name = "No progression in Kelp Forest"


class NoProgressionVeil(Toggle):
    """
    Make sure that there are no progression items in the Veil.

    Can be useful to get smaller runs.
    """
    display_name = "No progression in the Veil"
    rich_text_doc = True


class NoProgressionMithalas(Toggle):
    """
    Make sure that there are no progression items in the Mithalas (city, castle and cathedral).

    Can be useful to get smaller runs.
    """
    display_name = "No progression in Mithalas"
    rich_text_doc = True


class NoProgressionEnergyTemple(Toggle):
    """
    Make sure that there are no progression items in the Energy Temple.

    Can be useful to get smaller runs.
    """
    display_name = "No progression in the Energy Temple"
    rich_text_doc = True


class NoProgressionArnassiRuins(Toggle):
    """
    Make sure that there are no progression items in the Arnassi Ruins.

    Can be useful to get smaller runs.

    Note that if the Transportation turtle are not randomize, this include Simon Says area.
    """
    display_name = "No progression in Arnassi Ruins"
    rich_text_doc = True


class NoProgressionFrozenVeil(Toggle):
    """
    Make sure that there are no progression items in the Frozen Veil (including Ice Cavern and Bubble Cave).

    Can be useful to get smaller runs.
    """
    display_name = "No progression in the Frozen Veil"
    rich_text_doc = True


class NoProgressionAbyss(Toggle):
    """
    Make sure that there are no progression items in the Abyss.

    Can be useful to get smaller runs.

    Has no effect if the objective is "killing the four gods".
    """
    display_name = "No progression in the Abyss"
    rich_text_doc = True


class NoProgressionSunkenCity(Toggle):
    """
    Make sure that there are no progression items in the Sunken City.

    Can be useful to get smaller runs.

    Has no effect if the objective is "killing the four gods".
    """
    display_name = "No progression in the Sunken City"
    rich_text_doc = True


class NoProgressionBody(Toggle):
    """
    Make sure that there are no progression items in the Body (including the before-boss transturtle room
    and the boss location).

    Can be useful to get smaller runs.

    Has no effect if the objective is "killing the four gods".
    """
    display_name = "No progression in the Body"
    rich_text_doc = True

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
    ingredient_randomizer: IngredientRandomizer
    dish_randomizer: DishRandomizer
    aquarian_translation: AquarianTranslation
    skip_first_vision: SkipFirstVision
    blind_goal: BlindGoal
    infinite_hot_soup: InfiniteHotSoup
    open_body_tongue: OpenBodyTongue
    maximum_ingredient_amount: MaximumIngredientAmount
    skip_final_boss_3rd_form: SkipFinalBoss3rdForm
    save_healing: SaveHealing
    throne_as_location: ThroneAsLocation
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
