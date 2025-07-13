from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets


# TODO: Explain what a webworld is
class APQuestWebWorld(WebWorld):
    game = "APQuest"

    option_groups = option_groups
    options_presets = option_presets
