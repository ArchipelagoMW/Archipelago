from dataclasses import dataclass

from Options import Range, DeathLink, PerGameCommonOptions


class StrawberriesRequired(Range):
    """How many Strawberries you must receive to finish"""
    display_name = "Strawberries Required"
    range_start = 0
    range_end = 20
    default = 15

class DeathLinkAmnesty(Range):
    """How many deaths it takes to send a DeathLink"""
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 10


@dataclass
class Celeste64Options(PerGameCommonOptions):
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    strawberries_required: StrawberriesRequired
