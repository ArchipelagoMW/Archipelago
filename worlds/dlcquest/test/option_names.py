from ..Options import dlc_quest_option_classes

options_to_exclude = []
options_to_include = [option_to_include for option_to_include in dlc_quest_option_classes
                      if option_to_include.internal_name not in options_to_exclude]
