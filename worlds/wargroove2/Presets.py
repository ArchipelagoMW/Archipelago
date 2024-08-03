from typing import Dict, Any

from .Options import *

wargroove2_option_presets: Dict[str, Dict[str, Any]] = {
    "Easy": {
        "income_boost": 50,
        "commander_defense_boost": 5,
        "groove_boost": 10,
        "commander_choice": CommanderChoice.option_random_starting_faction,
        "final_levels": 1,
        "death_link": False
    },

    "Hard": {
        "income_boost": 0,
        "commander_defense_boost": 0,
        "groove_boost": 0,
        "commander_choice": CommanderChoice.option_locked_random,
        "final_levels": 4,
        "death_link": True
    },
}
