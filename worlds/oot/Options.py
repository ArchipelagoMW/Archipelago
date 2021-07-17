import typing
from Options import Option, DefaultOnToggle, Toggle, Choice, Range, OptionList

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
    alias_open_forest = 0
    alias_closed_forest = 2

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

class Bridge(Choice): 
    option_open = 0
    option_vanilla = 1
    option_stones = 2
    option_medallions = 3
    option_dungeons = 4
    option_tokens = 5
    default = 3

class Trials(Range): 
    range_start = 0
    range_end = 6
    default = 0

open_options: typing.Dict[str, type(Option)] = {
    "open_forest": Forest,
    "open_kakariko": Gate,
    "open_door_of_time": DefaultOnToggle,
    "zora_fountain": Fountain,
    "gerudo_fortress": Fortress, 
    "bridge": Bridge,
    "trials": Trials,
}

class StartingAge(Choice): 
    option_child = 0
    option_adult = 1

class InteriorEntrances(Choice): 
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_false = 0

class TriforceGoal(Range): 
    range_start = 1
    range_end = 100
    default = 20

class MQDungeons(Range):
    range_start = 0
    range_end = 12
    default = 0

world_options: typing.Dict[str, type(Option)] = {
    "starting_age": StartingAge,
    # "shuffle_interior_entrances": InteriorEntrances,
    # "shuffle_grotto_entrances": Toggle,
    # "shuffle_dungeon_entrances": Toggle,
    # "shuffle_overworld_entrances": Toggle,
    # "owl_drops": Toggle,
    # "warp_songs": Toggle,
    # "spawn_positions": Toggle,
    "triforce_hunt": Toggle, 
    "triforce_goal": TriforceGoal,
    "bombchus_in_logic": Toggle,
    "mq_dungeons": MQDungeons,
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

class LACSCondition(Choice): 
    option_vanilla = 0
    option_stones = 1
    option_medallions = 2
    option_dungeons = 3
    option_tokens = 4

lacs_options: typing.Dict[str, type(Option)] = {
    "lacs_condition": LACSCondition,
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
    # option_dungeon = 1
    option_any = 2

class ShopShuffle(Choice): 
    option_0 = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_random = 5
    option_off = 6
    default = 6
    alias_false = 6

class TokenShuffle(Choice): 
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3
    alias_false = 0

class ScrubShuffle(Choice): 
    option_off = 0
    option_low = 1
    option_regular = 2
    option_random = 3
    alias_false = 0
    alias_affordable = 1
    alias_expensive = 2
    alias_random_prices = 3

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
    # option_overworld = 4
    # option_any_dungeon = 5
    option_keysanity = 6
    default = 1
    alias_anywhere = 6

class ShuffleKeys(Choice): 
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    # option_overworld = 4
    # option_any_dungeon = 5
    option_keysanity = 6
    default = 3
    alias_keysy = 0
    alias_anywhere = 6

class ShuffleGerudoKeys(Choice): 
    option_vanilla = 0
    # option_overworld = 1
    # option_any_dungeon = 2
    option_keysanity = 3
    alias_anywhere = 3

class ShuffleGanonBK(Choice):     
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    # option_overworld = 4
    # option_any_dungeon = 5
    option_keysanity = 6
    option_on_lacs = 7
    default = 0
    alias_keysy = 0
    alias_anywhere = 6

dungeon_items_options: typing.Dict[str, type(Option)] = {
    "shuffle_mapcompass": ShuffleMapCompass, 
    "shuffle_smallkeys": ShuffleKeys, 
    "shuffle_fortresskeys": ShuffleGerudoKeys, 
    "shuffle_bosskeys": ShuffleKeys,
    "shuffle_ganon_bosskey": ShuffleGanonBK,
    "enhance_map_compass": Toggle,
}

class Cuccos(Range): 
    range_start = 0
    range_end = 7
    default = 7

class BigPoes(Range): 
    range_start = 1
    range_end = 10
    default = 1

timesavers_options: typing.Dict[str, type(Option)] = {
    # "skip_child_zelda": Toggle, 
    "no_escape_sequence": DefaultOnToggle, 
    "no_guard_stealth": DefaultOnToggle, 
    "no_epona_race": DefaultOnToggle, 
    "skip_some_minigame_phases": DefaultOnToggle, 
    "complete_mask_quest": Toggle, 
    "useful_cutscenes": Toggle, 
    "fast_chests": DefaultOnToggle, 
    "free_scarecrow": Toggle, 
    "fast_bunny_hood": Toggle, 
    "chicken_count": Cuccos,
    "big_poe_count": BigPoes, 
}

class Targeting(Choice): 
    option_hold = 0
    option_switch = 1

class Hints(Choice): 
    option_none = 0
    option_mask = 1
    option_agony = 2
    option_always = 3
    default = 3
    alias_false = 0

class TextShuffle(Choice): 
    option_none = 0
    option_except_hints = 1
    option_complete = 2
    alias_false = 0

class DamageMultiplier(Choice): 
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quadruple = 3
    option_ohko = 4
    default = 1

class StartingToD(Choice):
    option_default = 0
    option_sunrise = 1
    option_morning = 2
    option_noon = 3
    option_afternoon = 4
    option_sunset = 5
    option_evening = 6
    option_midnight = 7
    option_witching_hour = 8

misc_options: typing.Dict[str, type(Option)] = {
    "default_targeting": Targeting, # move this to cosmetic options later
    "clearer_hints": DefaultOnToggle,
    # "hints": Hints,
    "text_shuffle": TextShuffle,
    "damage_multiplier": DamageMultiplier,
    "no_collectible_hearts": Toggle,
    "starting_tod": StartingToD,
    "start_with_consumables": Toggle, 
    "start_with_rupees": Toggle,
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
    alias_false = 0
    alias_true = 2
    alias_extra = 2

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
    "logic_tricks": OptionList,
    "patch_uncompressed_rom": Toggle
}
