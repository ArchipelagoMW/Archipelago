from Options import ProgressionBalancing
from .options import *

explorer_mode_options = {
    "progression_balancing":                    ProgressionBalancing.default,
    "goal":                                     Goal.option_clamshells,
    "clamshell_goal_quantity":                  50,
    "extra_clamshells_in_pool":                 10,
    "shopsanity":                               Shopsanity.option_disabled,
    "regionsanity":                             Regionsanity.option_extreme,
    "regionsanity_starter_region_min_level":    0,
    "regionsanity_starter_region_max_level":    63,
    "home_point_hustle":                        HomePointHustle.option_mixed,
    "progressive_mount_mode":                   ProgressiveMountMode.option_false,
    "starting_level":                           99,
    "level_gating":                             LevelGating.option_level_catch_up,
    "level_compared_to_enemies":                10,
    "progressive_level_size":                   10,
    "max_level":                                99,
    "key_mode":                                 KeyMode.option_vanilla_skelefree,
    "obscure_routes":                           True,
    "auto_spend_lp":                            True,
    "auto_equip_passives":                      True,
    "easy_leveling":                            True,
    "item_info_mode":                           ItemInfoMode.option_earned,
    "disable_sparks":                           True,
}

crystal_project_options_presets: Dict[str, Dict[str, Any]] = {
    "Explorer Mode": explorer_mode_options,
}
