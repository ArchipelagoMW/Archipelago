from . import LingoTestBase


class TestMultiShuffleOptions(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "progressive_orange_tower": "true",
        "shuffle_colors": "true",
        "shuffle_paintings": "true",
        "early_color_hallways": "true"
    }


class TestPanelsanity(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "progressive_orange_tower": "true",
        "location_checks": "insanity",
        "shuffle_colors": "true"
    }


class TestAllPanelHunt(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "progressive_orange_tower": "true",
        "shuffle_colors": "true",
        "victory_condition": "level_2",
        "level_2_requirement": "800",
        "early_color_hallways": "true"
    }


class TestAllPanelHuntPanelsMode(LingoTestBase):
    options = {
        "shuffle_doors": "panels",
        "progressive_orange_tower": "true",
        "shuffle_colors": "true",
        "victory_condition": "level_2",
        "level_2_requirement": "800",
        "early_color_hallways": "true"
    }


class TestShuffleSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "shuffle_colors": "false",
        "victory_condition": "pilgrimage",
        "shuffle_sunwarps": "true",
        "sunwarp_access": "normal"
    }


class TestShuffleSunwarpsAccess(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "shuffle_colors": "false",
        "victory_condition": "pilgrimage",
        "shuffle_sunwarps": "true",
        "sunwarp_access": "individual"
    }


class TestSpeedBoostMode(LingoTestBase):
    options = {
        "location_checks": "insanity",
        "speed_boost_mode": "true",
    }
