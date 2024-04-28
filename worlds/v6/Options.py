import typing
from dataclasses import dataclass
from Options import Option, DeathLink, Range, Toggle, PerGameCommonOptions

class DoorCost(Range):
    """Amount of Trinkets required to enter Areas. Set to 0 to disable artificial locks."""
    display_name = "Door Cost"
    range_start = 0
    range_end = 3
    default = 3

class AreaCostRandomizer(Toggle):
    """Randomize which Area requires which set of DoorCost Trinkets"""
    display_name = "Area Cost Randomizer"

class DeathLinkAmnesty(Range):
    """Amount of Deaths to take before sending a DeathLink signal, for balancing difficulty"""
    display_name = "Death Link Amnesty"
    range_start = 0
    range_end = 30
    default = 15

class AreaRandomizer(Toggle):
    """Randomize Entrances to Areas"""
    display_name = "Area Randomizer"

class MusicRandomizer(Toggle):
    """Randomize Music"""
    display_name = "Music Randomizer"

@dataclass
class V6Options(PerGameCommonOptions):
    music_rando: MusicRandomizer
    area_rando: AreaRandomizer
    door_cost: DoorCost
    area_cost: AreaCostRandomizer
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
