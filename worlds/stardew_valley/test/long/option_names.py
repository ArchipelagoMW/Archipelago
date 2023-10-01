from worlds.stardew_valley.options import stardew_valley_option_classes

options_to_exclude = ["profit_margin", "starting_money", "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                      "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                      "quick_start", "gifting", "gift_tax"]
options_to_include = [option_to_include for option_to_include in stardew_valley_option_classes
                      if option_to_include.internal_name not in options_to_exclude]
