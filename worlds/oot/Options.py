import typing
from Options import Option, DefaultOnToggle, Toggle, Choice, Range

# oot has way too many options D:
# if default is not specified, it is option 0

class Logic(Choice): 
    option_glitchless = 0
    option_glitched = 1
    option_no_logic = 2

class Forest(Choice): 
    option_open = 0
    option_closed_deku = 1
    option_closed = 2

class Gate(Choice): 
    option_open = 0
    option_zelda = 1
    option_closed = 2

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

class StartingAge(Choice): 
    option_child = 0
    option_adult = 1

class InteriorEntrances(Choice): 
    option_off = 0
    option_simple = 1
    option_all = 2

world_options: typing.Dict[str, type(Option)] = {
    "starting_age": StartingAge,
    # "shuffle_interior_entrances": InteriorEntrances,
    # "shuffle_overworld_entrances": Toggle,
    # "randomize_overworld_spawns": Toggle, 
    "triforce_hunt": Toggle, 
    "bombchus_in_logic": Toggle,
}

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

class SongShuffle(Choice): 
    option_song = 0
    option_any = 2

class ShopShuffle(Choice):  # usually I would put 'off' at 0, but this is numeric so it makes an ugly off-by-one
    option_0 = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_random = 5
    option_off = 6
    default = 6

class TokenShuffle(Choice): 
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3

class ScrubShuffle(Choice): 
    option_off = 0
    option_low = 1
    option_regular = 2
    option_random = 3

shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_song_items": SongShuffle,
    "shopsanity": ShopShuffle, 
    "tokensanity": TokenShuffle, 
    "shuffle_scrubs": ScrubShuffle,
    "shuffle_cows": Toggle, 
    "shuffle_kokiri_sword": DefaultOnToggle,
    "shuffle_ocarinas": Toggle,
    "shuffle_weird_egg": Toggle,
    "shuffle_gerudo_card": Toggle,
    "shuffle_beans": Toggle, 
    "shuffle_medigoron_carpet_salesman": Toggle
}

class ShuffleMapCompass(Choice): 
    option_remove = 0
    option_startwith = 1
    option_vanilla = 2
    option_dungeon = 3
    option_keysanity = 6
    default = 1

class ShuffleKeys(Choice): 
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_keysanity = 6
    default = 3

class ShuffleGerudoKeys(Choice): 
    option_vanilla = 0
    option_overworld = 1
    option_keysanity = 3

class ShuffleGanonBK(Choice):     
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_keysanity = 6
    option_on_lacs = 7
    default = 3

dungeon_items_options: typing.Dict[str, type(Option)] = {
    "shuffle_mapcompass": ShuffleMapCompass, 
    "shuffle_smallkeys": ShuffleKeys, 
    "shuffle_fortresskeys": ShuffleGerudoKeys, 
    "shuffle_bosskeys": ShuffleKeys,
    "shuffle_ganon_bosskey": ShuffleGanonBK
}

class BigPoes(Range): 
    range_start = 1
    range_end = 10
    default = 1

timesavers_options: typing.Dict[str, type(Option)] = {
    "skip_child_zelda": Toggle, 
    "no_escape_sequence": Toggle, 
    "no_guard_stealth": Toggle, 
    "no_epona_race": Toggle, 
    "skip_some_minigame_phases": Toggle, 
    "complete_mask_quest": Toggle, 
    "useful_cutscenes": Toggle, 
    "fast_chests": DefaultOnToggle, 
    "free_scarecrow": Toggle, 
    "fast_bunny_hood": Toggle, 
    "big_poe_count": BigPoes, 
}

class DamageMultiplier(Choice): 
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quadruple = 3
    option_ohko = 4
    default = 1

misc_options: typing.Dict[str, type(Option)] = {
    "damage_multiplier": DamageMultiplier,
}

class ItemPoolValue(Choice): 
    option_plentiful = 0
    option_balanced = 1
    option_scarce = 2
    option_minimal = 3
    default = 1

class IceTraps(Choice): 
    option_off = 0
    option_normal = 1
    option_on = 2
    option_mayhem = 3
    option_onslaught = 4
    default = 1

class IceTrapVisual(Choice): 
    option_major_only = 0
    option_junk_only = 1
    option_anything = 2

class AdultTradeItem(Choice): 
    option_pocket_egg = 0
    option_pocket_cucco = 1
    option_cojiro = 2
    option_odd_mushroom = 3
    option_poachers_saw = 4
    option_broken_sword = 5
    option_prescription = 6
    option_eyeball_frog = 7
    option_eyedrops = 8
    option_claim_check = 9
    default = 0

itempool_options: typing.Dict[str, type(Option)] = {
    "item_pool_value": ItemPoolValue, 
    "junk_ice_traps": IceTraps,
    "ice_trap_appearance": IceTrapVisual, 
    "logic_earliest_adult_trade": AdultTradeItem, 
    "logic_latest_adult_trade": AdultTradeItem
}

oot_options: typing.Dict[str, type(Option)] = {
    "logic_rules": Logic, 
    "logic_no_night_tokens_without_suns_song": Toggle, 
    **open_options, 
    **world_options, 
    **lacs_options,
    **bridge_options,
    **dungeon_items_options,
    **shuffle_options,
    **timesavers_options,
    **misc_options, 
    **itempool_options,
}
