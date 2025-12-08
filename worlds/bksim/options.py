from dataclasses import dataclass
from Options import Range, PerGameCommonOptions


class LocationsPerWeather(Range):
    """The total number of locations per type of weather. (There are 3 weather types)"""
    display_name = "Locations Per Weather"
    range_start = 1
    range_end = 100
    default = 3


class StartDistance(Range):
    """The distance to the closest BK at the start.
    Each 'New Location' upgrade opens a location halfway between your house and the current closest location."""
    display_name = "Start Distance"
    range_start = 50
    range_end = 5000
    default = 300


class SpeedPerUpgrade(Range):
    """The amount of speed gained for each shoe upgrade.
    Snow boots give half this speed in the snow."""
    display_name = "Speed Per Upgrade"
    range_start = 1
    range_end = 100
    default = 2


class ExtraFillerRate(Range):
    """This percent of shoe/boot upgrades will attempt to be turned into filler.
    The number of upgrades will not be reduced below the amount logically required."""
    display_name = "Extra Filler Rate"
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class BKSim_Options(PerGameCommonOptions):
    locs_per_weather: LocationsPerWeather
    start_distance: StartDistance
    speed_per_upgrade: SpeedPerUpgrade
    extra_filler_rate: ExtraFillerRate


options_presets = {
    "Quick": {
        "locs_per_weather": 1,
        "start_distance": 100,
        "speed_per_upgrade": 5,
        "extra_filler_rate": 0,
    },
    "Marathon": {
        "locs_per_weather": 1,
        "start_distance": 5000,
        "speed_per_upgrade": 1,
        "extra_filler_rate": 0,
    },
    "Masochist": {
        "locs_per_weather": 100,
        "start_distance": 5000,
        "speed_per_upgrade": 1,
        "extra_filler_rate": 100,
    },
}
