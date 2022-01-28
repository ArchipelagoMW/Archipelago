import typing
from Options import Option, DeathLink, Range, Toggle

class DoorCost(Range):
    """Amount of Trinkets required to enter Areas. Set to 0 to disable artificial locks."""
    range_start = 0
    range_end = 3
    default = 3

class DeathLinkAmnesty(Range):
    """Amount of Deaths to take before sending a DeathLink signal, for balancing difficulty"""
    range_start = 0
    range_end = 30
    default = 15

class AreaRandomizer(Toggle):
    """Randomize Entrances to Areas"""
    displayname = "Area Randomizer"

v6_options: typing.Dict[str,type(Option)] = {
    "AreaRandomizer": AreaRandomizer,
    "DoorCost": DoorCost,
    "DeathLink": DeathLink,
    "DeathLinkAmnesty": DeathLinkAmnesty
}