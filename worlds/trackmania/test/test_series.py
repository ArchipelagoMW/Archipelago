from ..options import SeriesNumber, SeriesMapNumber, TargetTime
from . import TrackmaniaTestBase

#most of the Trackmania YAML settings are only used in the mod in game
#this just tests that games with minimum and maximum locations are completable
class TestMinimumBronzeSeries(TrackmaniaTestBase):
    options = {
        "series_number": SeriesNumber.range_start,
        "series_map_number": SeriesMapNumber.range_end,
        "target_time": TargetTime.range_start
    }

class TestMaximumAuthorSeries(TrackmaniaTestBase):
    options = {
        "series_number": SeriesNumber.range_end,
        "series_map_number": SeriesMapNumber.range_end,
        "target_time": TargetTime.range_end
    }
