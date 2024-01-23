from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, SpecialRange

from .hooks.Options import before_options_defined, after_options_defined



manual_options = before_options_defined({})

# Manual can do things to define options here, though it doesn't currently

manual_options = after_options_defined(manual_options)
