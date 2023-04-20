from . import LingoTestBase


class TestMultiShuffleOptions(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "progressive_orange_tower": "true",
        "shuffle_colors": "true",
        "shuffle_paintings": "true"
    }
