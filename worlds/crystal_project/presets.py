from Options import ProgressionBalancing
from .options import *
from .constants.key_items import *

explorer_mode_options = {
    "progression_balancing":         ProgressionBalancing.default,
    "goal":                          Goal.option_clamshells,
    "clamshell_goal_quantity":         50,
    "extra_clamshells_in_pool":         10,
    "shopsanity":                    Shopsanity.option_disabled,
    "regionsanity":                  Regionsanity.option_extreme,
    "progressive_mount_mode":          ProgressiveMountMode.option_false,
    "level_gating":                   LevelGating.option_level_catch_up,
    "progressive_level_size":          10,
    "max_level":                      99,
    "key_mode":                       KeyMode.option_vanilla_skelefree,
    "obscure_routes":                 True,
    "start_inventory_from_pool":     {PROGRESSIVE_LEVEL: 9},
    "auto_spend_lp":                 True,
    "auto_equip_passives":           True,
    "item_info_mode":                ItemInfoMode.option_obscured,
}

crystal_project_options_presets: Dict[str, Dict[str, Any]] = {
    "Explorer Mode": explorer_mode_options,
}
