import typing
from Options import Choice, Option, Toggle, Range

terraria_options: typing.Dict[str, type(Option)] = {
    "include_hardmode_achievements": Toggle,
    "include_insane_achievements": Toggle,
    "include_postgame_achievements": Toggle,
}