import typing

from Options import Choice

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
    option_vanilla = 2
    default = 0

class SuperBosses(Choice):
    display_name = "Super Bosses"
    option_excludeoptionalbosses = 0
    option_excludeanemos = 1
    option_allincluded = 2
    default = 0

GSTLAOptions = {
    "starter_ship": StartWithShip,
    "hidden_items": HiddenItems,
    "super_bosses": SuperBosses
}