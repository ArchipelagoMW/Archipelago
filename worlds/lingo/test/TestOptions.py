from . import LingoTestBase


class TestMultiShuffleOptions(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "progressive_orange_tower": "true",
        "shuffle_colors": "true",
        "shuffle_paintings": "true",
        "early_color_hallways": "true"
    }


class TestPanelsanity(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "progressive_orange_tower": "true",
        "location_checks": "insanity",
        "shuffle_colors": "true"
    }


class TestAllPanelHunt(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "progressive_orange_tower": "true",
        "shuffle_colors": "true",
        "victory_condition": "level_2",
        "level_2_requirement": "800",
        "early_color_hallways": "true"
    }
