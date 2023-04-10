import typing
from Options import Option, DefaultOnToggle, Choice


class StructureDeck(Choice):
    display_name = "Structure Deck"
    option_dragons_roar = 0
    option_zombie_madness = 1
    option_blazing_destruction = 2
    option_fury_from_the_deep = 3
    option_warriors_triumph = 4
    option_spellcasters_judgement = 5


ygo06_options: typing.Dict[str, type(Option)] = {
    "StructureDeck": StructureDeck
}