import typing
from Options import Option, DefaultOnToggle, Toggle, Choice, Range

class Logic(Choice): 
    option_glitchless = 0
    option_glitched = 1
    option_no_logic = 2
    default = 0

class Forest(Choice): 
    option_open_forest = 0
    option_open_deku = 1
    option_closed_forest = 2
    default = 0

class Gate(Choice): 
    option_open = 0
    option_letter = 1
    option_closed = 2
    default = 0

class Fountain(Choice): 
    option_open = 0
    option_open_as_adult = 1
    option_closed = 2
    default = 2

class Fortress(Choice): 
    option_closed = 0
    option_one_carpenter = 1
    option_open = 2
    default = 1

open_options: typing.Dict[str, type(Option)] = {
    "forest_state": Forest,
    "kakariko_gate": Gate,
    "door_of_time": DefaultOnToggle,
    "zoras_fountain": Fountain,
    "gerudo_fortress": Fortress
}

shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_kokiri_sword": DefaultOnToggle,
    "shuffle_ocarinas": Toggle,
    "shuffle_weird_egg": Toggle,
    "shuffle_gerudo_card": Toggle,
    "shuffle_magic_beans": Toggle
}

oot_options: typing.Dict[str, type(Option)] = {
    "logic_rules": Logic, 
    **open_options, 
    **shuffle_options
}
