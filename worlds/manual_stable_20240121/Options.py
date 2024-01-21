from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, SpecialRange

from .hooks.Options import before_options_defined, after_options_defined
from .Data import category_table


class FillerTrapPercent(Range):
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps."""
    range_end = 100

manual_options = before_options_defined({})

manual_options["filler_traps"] = FillerTrapPercent

for category in category_table:
    for option_name in category_table[category].get("yaml_option", []):
        if option_name not in manual_options:
            manual_options[option_name] = type(option_name, (Toggle,), {"default": True})

manual_options = after_options_defined(manual_options)
