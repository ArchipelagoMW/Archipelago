import typing
from Options import Choice, Option, Toggle, Range

khcom_options: typing.Dict[str, type(Option)] = {
    "include_battle_cards" Toggle
}