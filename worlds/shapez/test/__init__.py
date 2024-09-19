from test.bases import WorldTestBase
from .. import options_presets


class ShapezTestBase(WorldTestBase):
    game = "shapez"


class TestDefault(ShapezTestBase):
    options = {}


class TestMinimum(ShapezTestBase):
    options = options_presets["Minimum checks"]


class TestMaximum(ShapezTestBase):
    options = options_presets["Maximum checks"]


class TestRestrictive(ShapezTestBase):
    options = options_presets["Restrictive start"]


class TestAllRelevantOptions1(ShapezTestBase):
    options = {
        "goal": "vanilla",
        "randomize_level_requirements": False,
        "randomize_upgrade_requirements": False,
        "early_balancer_tunnel_and_trash": "none",
        "lock_belt_and_extractor": True,
        "include_achievements": True,
        "exclude_softlock_achievements": False,
        "exclude_long_playtime_achievements": False,
        "exclude_progression_unreasonable": True,
        "shapesanity_amount": 1000,
        "traps_percentage": "random"
    }


class TestAllRelevantOptions2(ShapezTestBase):
    options = {
        "goal": "mam",
        "goal_amount": 500,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "random_steps",
        "randomize_upgrade_logic": "vanilla_like",
        "early_balancer_tunnel_and_trash": "5_buildings",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": False,
        "exclude_long_playtime_achievements": False,
        "exclude_progression_unreasonable": False,
        "shapesanity_amount": 4,
        "traps_percentage": 0
    }


class TestAllRelevantOptions3(ShapezTestBase):
    options = {
        "goal": "even_fasterer",
        "goal_amount": 500,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "vanilla_shuffled",
        "randomize_upgrade_logic": "linear",
        "early_balancer_tunnel_and_trash": "3_buildings",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": True,
        "exclude_long_playtime_achievements": True,
        "shapesanity_amount": "random",
        "traps_percentage": 100,
        "split_inventory_draining_trap": True
    }


class TestAllRelevantOptions4(ShapezTestBase):
    options = {
        "goal": "efficiency_iii",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "stretched_shuffled",
        "randomize_upgrade_logic": "category",
        "early_balancer_tunnel_and_trash": "sphere_1",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": True,
        "exclude_long_playtime_achievements": True,
        "shapesanity_amount": "random",
        "traps_percentage": "random"
    }


class TestAllRelevantOptions5(ShapezTestBase):
    options = {
        "goal": "mam",
        "goal_amount": "random-range-27-500",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "quick_shuffled",
        "randomize_upgrade_logic": "category_random",
        "lock_belt_and_extractor": False,
        "include_achievements": True,
        "exclude_softlock_achievements": True,
        "exclude_long_playtime_achievements": True,
        "shapesanity_amount": "random",
        "traps_percentage": 100,
        "split_inventory_draining_trap": False
    }


class TestAllRelevantOptions6(ShapezTestBase):
    options = {
        "goal": "mam",
        "goal_amount": "random-range-27-500",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "hardcore",
        "randomize_upgrade_logic": "hardcore",
        "lock_belt_and_extractor": False,
        "include_achievements": False,
        "shapesanity_amount": "random",
        "traps_percentage": "random"
    }
