from . import PsychonautsTestBase
from .. import Options


class TestMinimumStartingItems(PsychonautsTestBase):
    options = {
        "RandomStartingMinds": Options.RandomStartingMinds.range_start,
        "StartingMentalMagnet": False,
    }


class TestMaximumStartingItems(PsychonautsTestBase):
    options = {
        "RandomStartingMinds": Options.RandomStartingMinds.range_end,
        "StartingMentalMagnet": True,
    }
