import typing
import random

from Options import Choice, Range, OptionNameSet, Option, Toggle, DefaultOnToggle


class RandoPreset(OptionNameSet):
    displayname = "Rando Preset"
    randoPreset = "worlds\\sm\\variaRandomizer\\rando_presets\\default.json"

sm_options: typing.Dict[str, type(Option)] = {
    # "randoPreset": RandoPreset
}
