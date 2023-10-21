from typing import Dict

from Options import Range, Option


class BaseElo(Range):
    """
    Determines Stock's initial ELO rating.
    """
    display_name = "Base ELO"
    range_start = 400
    range_end = 1200
    default = 800


cm_options: Dict[str, type(Option)] = {
    "base_elo": BaseElo
}
