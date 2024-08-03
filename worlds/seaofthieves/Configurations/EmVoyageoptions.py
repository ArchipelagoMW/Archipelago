import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle


class VoyageCountSpecificAf(Range):
    """Randomly selects selected number of Athena's Fortune Voyages, adds their 'Voyage Completion' location to the location pool.
     Selecting -1 will add a single location on complete any voyage. Selecting 0 will only add the Skull of Destiny."""
    range_start = -1
    range_end = 10
    display_name = "(VOY) Athena"
    default = 0


class VoyageCountSpecificGh(Range):
    """Randomly selects selected number of Gold Hoarder Voyages, adds their 'Voyage Completion' location to the location pool.
     Selecting -1 will add a single location on complete any voyage. Selecting 0 will add no loactions"""
    range_start = -1
    range_end = 6
    display_name = "(VOY) Gold Hoarder"
    default = 0


class VoyageCountSpecificMa(Range):
    """Randomly selects selected number of Merchant Alliance Voyages, adds their 'Voyage Completion' location to the location pool.
     Selecting -1 will add a single location on complete any voyage. Selecting 0 will add no loactions"""
    range_start = -1
    range_end = 3
    display_name = "(VOY) Merchant Alliance"
    default = 0


class VoyageCountSpecificOos(Range):
    """Randomly selects selected number of Order of Souls Voyages, adds their 'Voyage Completion' location to the location pool.
     Selecting -1 will add a single location on complete any voyage. Selecting 0 will add no loactions"""
    range_start = -1
    range_end = 4
    display_name = "(VOY) Order of Souls"
    default = 0


class VoyageCountSpecificRoar(Range):
    """Randomly selects selected number of Devil's Roar voyages, adds their 'Voyage Completion' location to the location pool.
     Selecting -1 will add a single location on complete any voyage. Selecting 0 will add no loactions"""
    range_start = -1
    range_end = 4
    display_name = "(VOY) Devil's Roar"
    default = 0


class VoyageOnceAf(DefaultOnToggle):
    """If true, overrides Voyagesanity - Athena. Adds location check on completing any Athena Voyage"""
    display_name = "Single Athena Voyage"


class VoyageOnceMa(DefaultOnToggle):
    """If true, overrides Voyagesanity - Merchant Alliance. Adds location check on completing any Merchant Alliance Voyage"""
    display_name = "Single Merchant Alliance Voyage"


class VoyageOnceGh(DefaultOnToggle):
    """If true, overrides Voyagesanity - Gold Hoarder. Adds location check on completing any Gold Hoarder Voyage"""
    display_name = "Single Gold Hoarder Voyage"


class VoyageOnceOos(DefaultOnToggle):
    """If true, overrides Voyagesanity - Order of Souls. Adds location check on completing any Order of Souls Voyage"""
    display_name = "Single Order of Souls Voyage"
