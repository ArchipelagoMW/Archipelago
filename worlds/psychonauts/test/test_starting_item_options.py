from . import PsychonautsTestBase
from .. import Options


class TestMinimumStartingItems(PsychonautsTestBase):
    options = {
        "RandomStartingMinds": Options.RandomStartingMinds.range_start,
        "StartingLevitation": False,
        "StartingMentalMagnet": False,
        "StartingCobwebDuster": False,
    }


class TestMaximumStartingItems(PsychonautsTestBase):
    options = {
        "RandomStartingMinds": Options.RandomStartingMinds.range_end,
        "StartingLevitation": True,
        "StartingMentalMagnet": True,
        "StartingCobwebDuster": True,
    }
