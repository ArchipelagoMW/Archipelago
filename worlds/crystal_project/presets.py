from Options import ProgressionBalancing
from .options import *
from .constants.key_items import *

explorer_mode_options = {
    "progression_balancing":         ProgressionBalancing.default,
    "goal":                          Goal.option_clamshells,
    "clamshellGoalQuantity":         50,
    "extraClamshellsInPool":         10,
    "shopsanity":                    Shopsanity.option_disabled,
    "regionsanity":                  Regionsanity.option_extreme,
    "progressiveMountMode":          ProgressiveMountMode.option_false,
    "levelGating":                   LevelGating.option_level_catch_up,
    "progressiveLevelSize":          10,
    "maxLevel":                      99,
    "keyMode":                       KeyMode.option_vanilla_skelefree,
    "obscureRoutes":                 True,
    "start_inventory_from_pool":     {PROGRESSIVE_LEVEL: 9},
    "auto_spend_lp":                 True,
    "auto_equip_passives":           True,
    "item_info_mode":                ItemInfoMode.option_obscured,
}

crystal_project_options_presets: Dict[str, Dict[str, Any]] = {
    "Explorer Mode": explorer_mode_options,
}
