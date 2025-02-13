from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, OptionGroup, PerGameCommonOptions


class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 10

class TotalStrawberries(Range):
    """
    How many Strawberries exist
    """
    display_name = "Total Strawberries"
    range_start = 0
    range_end = 200
    default = 20

class StrawberriesRequiredPercentage(Range):
    """
    Percentage of existing Strawberries you must receive to finish
    """
    display_name = "Strawberries Required Percentage"
    range_start = 0
    range_end = 100
    default = 80


celeste_option_groups = [
    OptionGroup("Goal Options", [
        TotalStrawberries,
        StrawberriesRequiredPercentage,
    ]),
]


@dataclass
class CelesteOptions(PerGameCommonOptions):
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    total_strawberries: TotalStrawberries
    strawberries_required_percentage: StrawberriesRequiredPercentage
