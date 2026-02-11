from typing import Any

gatoroboto_options_presets: dict[str, dict[str, Any]] = {
    "Normal": {
        "rocket_jumps": False,
        "precise_tricks": False,
        "water_mech": False,
        "small_mech": False
    },
    "Hard": {
        "rocket_jumps": True,
        "precise_tricks": True,
        "water_mech": False,
        "small_mech": False
    },
    "Glitched": {
        "rocket_jumps": True,
        "precise_tricks": True,
        "water_mech": True,
        "small_mech": True
    }
}