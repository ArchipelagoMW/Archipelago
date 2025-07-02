from typing import Any, Dict

from Options import Accessibility, ProgressionBalancing
from .options import *
from .constants.key_items import *

explorer_mode_options = {
    "progression_balancing":         ProgressionBalancing.default,
    "goal":                          Goal.option_clamshells,
    "clamshellGoalQuantity":         50,
    "extraClamshellsInPool":         10,
    "shopsanity":                    Shopsanity.option_disabled,
    "regionsanity":                  Regionsanity.option_true,
    "progressiveMountMode":          ProgressiveMountMode.option_true,
    "levelGating":                   LevelGating.option_level_catch_up,
    "progressiveLevelSize":          10,
    "maxLevel":                      99,
    "keyMode":                       KeyMode.option_vanilla_skelefree,
    "start_inventory_from_pool":     {PROGRESSIVE_LEVEL: 9},
}

crystal_project_options_presets: Dict[str, Dict[str, Any]] = {
    "Explorer Mode": explorer_mode_options,
}
