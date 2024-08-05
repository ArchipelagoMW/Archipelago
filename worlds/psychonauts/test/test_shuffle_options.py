from . import PsychonautsTestBase

# Test Shuffle/Sanity options.


class TestCobwebShuffle(PsychonautsTestBase):
    options = {
        "MentalCobwebShuffle": True,
    }


class TestDeepArrowheadShuffle(PsychonautsTestBase):
    options = {
        "DeepArrowheadShuffle": True,
    }


# All shuffle options enabled.
class TestMaximalShuffle(PsychonautsTestBase):
    options = {
        "MentalCobwebShuffle": True,
        "DeepArrowheadShuffle": True,
    }
