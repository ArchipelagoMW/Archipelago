import typing
import random

from Options import Choice, Range, Option, Toggle, DefaultOnToggle


class StartLocation(Choice):
    displayname = "Starting location"
    option_landing_site = 0
    option_green_brinstar_elevator = 1

sm_options: typing.Dict[str, type(Option)] = {
    "startLocation": StartLocation,
}
