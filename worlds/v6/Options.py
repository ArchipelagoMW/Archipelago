import typing
from Options import Option, DeathLink, Range, Toggle

class DoorCost(Range):
    """Amount of Trinkets required to enter Areas. Set to 0 to disable artificial locks."""
    range_start = 0
    range_end = 3
    default = 3

class AreaCostRandomizer(Toggle):
    """Randomize which Area requires which set of DoorCost Trinkets"""
    display_name = "Area Cost Randomizer"

class DeathLinkAmnesty(Range):
    """Amount of Deaths to take before sending a DeathLink signal, for balancing difficulty"""
    range_start = 0
    range_end = 30
    default = 15

class AreaRandomizer(Toggle):
    """Randomize Entrances to Areas"""
    display_name = "Area Randomizer"

class MusicRandomizer(Toggle):
    """Randomize Music"""
    display_name = "Music Randomizer"

v6_options: typing.Dict[str,type(Option)] = {
    "MusicRandomizer": MusicRandomizer,
    "AreaRandomizer": AreaRandomizer,
    "DoorCost": DoorCost,
    "AreaCostRandomizer": AreaCostRandomizer,
    "death_link": DeathLink,
    "DeathLinkAmnesty": DeathLinkAmnesty
}