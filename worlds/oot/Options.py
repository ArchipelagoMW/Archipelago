import typing
from Options import Option, DefaultOnToggle, Toggle, Choice, Range

# oot has way too many options D:

class Logic(Choice): 
    option_glitchless = 0
    option_glitched = 1
    option_no_logic = 2
    default = 0

class Forest(Choice): 
    option_open = 0
    option_closed_deku = 1
    option_closed = 2
    default = 0

class Gate(Choice): 
    option_open = 0
    option_zelda = 1
    option_closed = 2
    default = 0

class Fountain(Choice): 
    option_open = 0
    option_adult = 1
    option_closed = 2
    default = 2

class Fortress(Choice): 
    option_normal = 0
    option_fast = 1
    option_open = 2
    default = 1

open_options: typing.Dict[str, type(Option)] = {
    "open_forest": Forest,
    "open_kakariko": Gate,
    "open_door_of_time": DefaultOnToggle,
    "zora_fountain": Fountain,
    "gerudo_fortress": Fortress
}


class InteriorEntrances(Choice): 
    option_off = 0
    option_simple = 1
    option_all = 2
    default = 0

# world_options: typing.Dict[str, type(Option)] = {
#     "shuffle_interior_entrances": InteriorEntrances,
#     "shuffle_overworld_entrances": Toggle,
#     "randomize_overworld_spawns": Toggle
# }

class CheckStones(Range): 
    range_start = 0
    range_end = 3
    default = 3

class CheckMedallions(Range): 
    range_start = 0
    range_end = 6
    default = 6

class CheckRewards(Range): 
    range_start = 0
    range_end = 9
    default = 9

class CheckTokens(Range): 
    range_start = 0
    range_end = 100
    default = 40


lacs_options: typing.Dict[str, type(Option)] = {
    "lacs_stones": CheckStones, 
    "lacs_medallions": CheckMedallions, 
    "lacs_rewards": CheckRewards, 
    "lacs_tokens": CheckTokens
}

bridge_options: typing.Dict[str, type(Option)] = {
    "bridge_stones": CheckStones, 
    "bridge_medallions": CheckMedallions, 
    "bridge_rewards": CheckRewards, 
    "bridge_tokens": CheckTokens
}

shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_kokiri_sword": DefaultOnToggle,
    "shuffle_ocarinas": Toggle,
    "shuffle_weird_egg": Toggle,
    "shuffle_gerudo_card": Toggle,
    "shuffle_magic_beans": Toggle
}

class ShuffleDungeonItem(Choice): 
    option_remove = 0
    option_startwith = 1
    option_dungeon = 3
    option_keysanity = 6
    default = 1

dungeon_items_options: typing.Dict[str, type(Option)] = {
    "shuffle_mapcompass": ShuffleDungeonItem
}

class BigPoes(Range): 
    range_start = 1
    range_end = 10
    default = 1

timesavers_options: typing.Dict[str, type(Option)] = {
    "big_poe_count": BigPoes
}

oot_options: typing.Dict[str, type(Option)] = {
    "logic_rules": Logic, 
    "logic_no_night_tokens_without_suns_song": Toggle, 
    **open_options, 
    # **world_options, 
    **lacs_options,
    **bridge_options,
    **dungeon_items_options,
    **shuffle_options,
    **timesavers_options
}
