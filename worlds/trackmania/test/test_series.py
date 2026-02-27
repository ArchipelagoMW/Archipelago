from ..options import SeriesNumber, SeriesMinimumMapNumber, TargetTime
from . import TrackmaniaTestBase

#most of the Trackmania YAML settings are only used in the mod in game
#this just tests that games with minimum and maximum locations are completable
class TestMinimumBronzeSeries(TrackmaniaTestBase):
    options = {
        "series_number": SeriesNumber.range_end,
        "series_minimum_map_number": SeriesMinimumMapNumber.range_start,
        "series_maximum_map_number": SeriesMinimumMapNumber.range_start,
        "target_time": TargetTime.range_start
    }

class TestMaximumAuthorSeries(TrackmaniaTestBase):
    options = {
        "series_number": SeriesNumber.range_end,
        "series_minimum_map_number": SeriesMinimumMapNumber.range_end,
        "series_maximum_map_number": SeriesMinimumMapNumber.range_end,
        "target_time": TargetTime.range_end
    }
