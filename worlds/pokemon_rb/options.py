from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, SpecialRange
from schema import Schema, And, Optional


# class Routing(Choice):
#     """In Archipelago routing, the old man is moved to the entrance of Mt Moon, the Secret Key locks the Pokémon Mansion
#     instead of the Cinnabar Gym, and strength boulders block the entrance to the Route 11 gate."""
#     display_name = "Routing"
#     option_vanilla = 0
#     option_archipelago = 1
#     default = 1


class Goal(Choice):
    """If Professor Oak is selected, your victory condition will require challenging and defeating Oak after becoming"""
    """Champion and defeating or capturing the Pokemon at the end of Cerulean Cave."""
    display_name = "Goal"
    option_pokemon_league = 0
    option_professor_oak = 1
    default = 0


class BadgeGoal(Range):
    """Number of badges required to reach Victory Road. One fewer will be required to enter the Viridian Gym."""
    display_name = "Badge Goal"
    range_start = 2
    range_end = 8


class RandomizeBadges(Choice):
    """Shuffle will shuffle badges across the 8 gyms. Badgesanity will place badges into the general item pool.
    Badgesanity will make badge locations 'remote' meaning you must be connected to an Archipelago server to receive
    local items placed at these locations."""
    display_name = "Badges"
    option_vanilla = 0
    option_shuffle = 1
    option_badgesanity = 2
    default = 0


class FreeFlyLocation(Toggle):
    """One random fly destination will be unlocked by default."""
    display_name = "Free Fly Location"
    default = 1


class ExpModifier(SpecialRange):
    """Modifier for EXP gained."""
    display_name = "Exp Modifier"
    range_start = 0
    range_end = 255
    default = 50
    special_range_names = {
        "half": 25,
        "normal": 50,
        "double": 100,
        "triple": 150,
        "quadruple": 200,
        "quintuple": 250

    }


class ControlEncounters(Toggle):
    """Allows you to hold B to disable wild encounters and most trainer battles"""
    display_name = "Control Encounters"
    default = 0


pokemon_rb_options = {
    # "routing": Routing,
    "goal": Goal,
    "badge_goal": BadgeGoal,
    "randomize_badges": RandomizeBadges,
    "free_fly_location": FreeFlyLocation,
    "exp_modifier": ExpModifier,
    "control_encounters": ControlEncounters,
}