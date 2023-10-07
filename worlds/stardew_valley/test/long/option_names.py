from ...options import stardew_valley_option_names

options_to_exclude = ["profit_margin", "starting_money", "multiple_day_sleep_enabled", "multiple_day_sleep_cost",
                      "experience_multiplier", "friendship_multiplier", "debris_multiplier",
                      "quick_start", "gifting", "gift_tax"]

options_to_include = [option_name for option_name in stardew_valley_option_names
                      if option_name not in options_to_exclude]
