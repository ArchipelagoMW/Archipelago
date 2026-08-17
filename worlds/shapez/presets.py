from .options import max_levels_and_upgrades, max_shapesanity

options_presets = {
    "Most vanilla": {
        "goal": "vanilla",
        "randomize_level_requirements": False,
        "randomize_upgrade_requirements": False,
        "early_balancer_tunnel_and_trash": "3_buildings",
        "include_achievements": True,
        "exclude_softlock_achievements": False,
        "exclude_long_playtime_achievements": False,
        "shapesanity_amount": 4,
        "toolbar_shuffling": False,
    },
    "Minimum checks": {
        "goal": "vanilla",
        "include_achievements": False,
        "shapesanity_amount": 4
    },
    "Maximum checks": {
        "goal": "even_fasterer",
        "goal_amount": max_levels_and_upgrades,
        "include_achievements": True,
        "exclude_softlock_achievements": False,
        "exclude_long_playtime_achievements": False,
        "shapesanity_amount": max_shapesanity
    },
    "Restrictive start": {
        "goal": "vanilla",
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "hardcore",
        "randomize_upgrade_logic": "hardcore",
        "early_balancer_tunnel_and_trash": "sphere_1",
        "include_achievements": False,
        "shapesanity_amount": 4
    },
    "Quick game": {
        "goal": "efficiency_iii",
        "required_shapes_multiplier": 1,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "hardcore",
        "randomize_upgrade_logic": "hardcore",
        "include_achievements": False,
        "shapesanity_amount": 4,
        "include_whacky_upgrades": True,
    }
}
