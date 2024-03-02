from ... import StardewValleyWorld

options_to_exclude = ["profit_margin", "starting_money", "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                      "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                      "quick_start", "gifting", "gift_tax", "progression_balancing", "accessibility", "start_inventory", "start_hints", "death_link"]

options_to_include = [option for option_name, option in StardewValleyWorld.options_dataclass.type_hints.items()
                      if option_name not in options_to_exclude]
