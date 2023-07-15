import typing

from Options import Choice

class StartWithShip(Choice):
    display_name = "Start with ship"
    option_startwithship = 0
    option_startwithcrystal = 1
    option_shipisclosed = 2
    default = 0

GSTLAOptions = {
    "starting_ship": StartWithShip
}