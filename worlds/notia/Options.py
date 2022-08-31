from typing import Dict
from Options import Option, DefaultOnToggle, Range

class TotalLocations(Range):
    """Number of location checks which are added to the playthrough."""
    display_name = "Total Locations"
    range_start = 10
    range_end = 500
    default = 100

class BadAffects(DefaultOnToggle):
    """Negative affects on the Noita world are added to the item pool."""
    display_name = "Bad Times"


noita_options: Dict[str, type(Option)] = {
    "total_locations":      TotalLocations,
    "bad_affects":          BadAffects
}