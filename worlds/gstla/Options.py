import typing

from Options import Choice, NamedRange

class StartWithShip(Choice):
    display_name = "Start with ship"
    option_startwithship = 0
    option_shipisclosed = 1
    option_vanilla = 2
    default = 0

class HiddenItems(Choice):
    display_name = "Hidden items"
    option_revealrequired = 0
    option_included = 1
    option_excluded = 2
    default = 0

class CharacterShuffle(Choice):
    display_name = "Character Shuffle"
    option_anywhere = 0
    option_vanilla_shuffled = 1
    option_vanilla = 2

class SuperBosses(Choice):
    display_name = "Super Bosses"
    option_excludeoptionalbosses = 0
    option_excludeanemos = 1
    option_allincluded = 2
    default = 0

class DjinnLogic(NamedRange):
    display_name = "Djinn Logic"
    range_start = 0
    range_end = 100
    default = 100

    special_range_names = {
        "casual": 100,
        "hard": 50,
        "none": 0
    }

GSTLAOptions = {
    "starter_ship": StartWithShip,
    "hidden_items": HiddenItems,
    "super_bosses": SuperBosses,
    "djinn_logic": DjinnLogic,
    "character_shuffle": CharacterShuffle
}