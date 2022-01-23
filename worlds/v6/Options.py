import typing
from Options import Option, DeathLink, Range

class DoorCost(Range):
    """Amount of Trinkets required to enter Areas. Set to 0 to disable artificial locks."""
    range_start = 0
    range_end = 5
    default = 3

class DeathLinkAmnesty(Range):
    """Amount of Deaths to take before sending a DeathLink signal, for balancing difficulty"""
    range_start = 0
    range_end = 30
    default = 15

v6_options: typing.Dict[str,type(Option)] = {
    "DoorCost": DoorCost,
    "DeathLink": DeathLink,
    "DeathLinkAmnesty": DeathLinkAmnesty
}