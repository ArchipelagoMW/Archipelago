import typing
from Options import Option, DeathLink, Range

class DeathLinkAmnesty(Range):
    """Amount of Deaths to take before sending a DeathLink signal, for balancing difficulty"""
    range_start = 0
    range_end = 30
    default = 15

v6_options: typing.Dict[str,type(Option)] = {
    "DeathLink": DeathLink,
    "DeathLinkAmnesty": DeathLinkAmnesty
}