options_presets = {
    "Minimum checks": {
        "goal": "vanilla",
        # "additional_locations": 1,
        "shapesanity_amount": 4
    },
    "Maximum checks": {
        "goal": "even_fasterer",
        "goal_amount": 1000,
        # "additional_locations": True,
        # "exclude_softlock_achievements": False,
        # "exclude_long_playtime_achievements": False,
        "shapesanity_amount": 5664
    },
    "Restrictive start": {
        "goal": 0,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "hardcore",
        "randomize_upgrade_logic": "hardcore",
        "early_balancer_tunnel_and_trash": "sphere_1",
        "shapesanity_amount": 4
    },
    "Quick game": {
        "goal": 3,
        "required_shapes_multiplier": 1,
        "randomize_level_requirements": True,
        "randomize_upgrade_requirements": True,
        "randomize_level_logic": "hardcore",
        "randomize_upgrade_logic": "hardcore",
        "shapesanity_amount": 4
    }
}