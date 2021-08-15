import typing
from Options import Option, DefaultOnToggle, Toggle, Choice, Range, OptionList
from .Colors import *
import worlds.oot.Sounds as sfx

# oot has way too many options D:
# if default is not specified, it is option 0

def make_range(start, end, default_value=0):
    class NewRange(Range):
        range_start = start
        range_end = end
        default = default_value
    return NewRange

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

open_options: typing.Dict[str, type(Option)] = {
    "open_forest": Forest,
    "open_kakariko": Gate,
    "open_door_of_time": DefaultOnToggle,
    "zora_fountain": Fountain,
    "gerudo_fortress": Fortress, 
    "bridge": Bridge,
    "trials": make_range(0, 6)
}

class StartingAge(Choice): 
    option_child = 0
    option_adult = 1

class InteriorEntrances(Choice): 
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_false = 0

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
    "triforce_goal": make_range(1, 200, 20),
    "bombchus_in_logic": Toggle,
    # "mq_dungeons": make_range(0, 12),
}

class LACSCondition(Choice): 
    option_vanilla = 0
    option_stones = 1
    option_medallions = 2
    option_dungeons = 3
    option_tokens = 4

lacs_options: typing.Dict[str, type(Option)] = {
    "lacs_condition": LACSCondition,
    "lacs_stones": make_range(0, 3, 3), 
    "lacs_medallions": make_range(0, 6, 6), 
    "lacs_rewards": make_range(0, 9, 9), 
    "lacs_tokens": make_range(0, 100, 40),
}

bridge_options: typing.Dict[str, type(Option)] = {
    "bridge_stones": make_range(0, 3, 3), 
    "bridge_medallions": make_range(0, 6, 6), 
    "bridge_rewards": make_range(0, 9, 9), 
    "bridge_tokens": make_range(0, 100, 40),
}

class SongShuffle(Choice): 
    option_song = 0
    option_dungeon = 1
    option_any = 2

class ShopShuffle(Choice): 
    option_0 = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_random_value = 5
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
    option_random_prices = 3
    alias_false = 0
    alias_affordable = 1
    alias_expensive = 2

shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_song_items": SongShuffle,
    "shopsanity": ShopShuffle, 
    "tokensanity": TokenShuffle, 
    "shuffle_scrubs": ScrubShuffle,
    "shuffle_cows": Toggle, 
    "shuffle_kokiri_sword": Toggle,
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
    option_overworld = 4
    option_any_dungeon = 5
    option_keysanity = 6
    default = 1
    alias_anywhere = 6

class ShuffleKeys(Choice): 
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_overworld = 4
    option_any_dungeon = 5
    option_keysanity = 6
    default = 3
    alias_keysy = 0
    alias_anywhere = 6

class ShuffleGerudoKeys(Choice): 
    option_vanilla = 0
    option_overworld = 1
    option_any_dungeon = 2
    option_keysanity = 3
    alias_anywhere = 3

class ShuffleGanonBK(Choice):     
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_overworld = 4
    option_any_dungeon = 5
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
    "chicken_count": make_range(0, 7, 7),
    # "big_poe_count": make_range(1, 10, 1),
}

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

# Start of cosmetic options

def assemble_color_option(func, default_option: str, outer=False): 
    color_options = func()
    if outer:
        color_options.append("Match Inner")
    format_color = lambda color: color.replace(' ', '_').lower()
    color_to_id = {format_color(color): index for index, color in enumerate(color_options)}
    class ColorOption(Choice):
        default = color_options.index(default_option)
    ColorOption.options.update(color_to_id)
    ColorOption.name_lookup.update({id: color for (color, id) in color_to_id.items()})
    return ColorOption

class Targeting(Choice): 
    option_hold = 0
    option_switch = 1

class Music(Choice): 
    option_normal = 0
    option_off = 1
    option_randomized = 2
    alias_false = 1

cosmetic_options: typing.Dict[str, type(Option)] = {
    "default_targeting": Targeting,
    "display_dpad": DefaultOnToggle,
    "correct_model_colors": DefaultOnToggle,
    "background_music": Music,
    "fanfares": Music,
    "ocarina_fanfares": Toggle,
    "kokiri_color": assemble_color_option(get_tunic_color_options, "Kokiri Green"),
    "goron_color":  assemble_color_option(get_tunic_color_options, "Goron Red"),
    "zora_color":   assemble_color_option(get_tunic_color_options, "Zora Blue"),
    "silver_gauntlets_color":   assemble_color_option(get_gauntlet_color_options, "Silver"),
    "golden_gauntlets_color":   assemble_color_option(get_gauntlet_color_options, "Gold"),
    "mirror_shield_frame_color": assemble_color_option(get_shield_frame_color_options, "Red"),
    "navi_color_default_inner": assemble_color_option(get_navi_color_options, "White"),
    "navi_color_default_outer": assemble_color_option(get_navi_color_options, "Match Inner", outer=True),
    "navi_color_enemy_inner":   assemble_color_option(get_navi_color_options, "Yellow"),
    "navi_color_enemy_outer":   assemble_color_option(get_navi_color_options, "Match Inner", outer=True),
    "navi_color_npc_inner":     assemble_color_option(get_navi_color_options, "Light Blue"),
    "navi_color_npc_outer":     assemble_color_option(get_navi_color_options, "Match Inner", outer=True),
    "navi_color_prop_inner":    assemble_color_option(get_navi_color_options, "Green"),
    "navi_color_prop_outer":    assemble_color_option(get_navi_color_options, "Match Inner", outer=True),
    "sword_trail_duration": make_range(4, 20, 4),
    "sword_trail_color_inner": assemble_color_option(get_sword_trail_color_options, "White"),
    "sword_trail_color_outer": assemble_color_option(get_sword_trail_color_options, "Match Inner", outer=True),
    "bombchu_trail_color_inner": assemble_color_option(get_bombchu_trail_color_options, "Red"),
    "bombchu_trail_color_outer": assemble_color_option(get_bombchu_trail_color_options, "Match Inner", outer=True),
    "boomerang_trail_color_inner": assemble_color_option(get_boomerang_trail_color_options, "Yellow"),
    "boomerang_trail_color_outer": assemble_color_option(get_boomerang_trail_color_options, "Match Inner", outer=True),
    "heart_color":          assemble_color_option(get_heart_color_options, "Red"),
    "magic_color":          assemble_color_option(get_magic_color_options, "Green"),
    "a_button_color":       assemble_color_option(get_a_button_color_options, "N64 Blue"),
    "b_button_color":       assemble_color_option(get_b_button_color_options, "N64 Green"),
    "c_button_color":       assemble_color_option(get_c_button_color_options, "Yellow"),
    "start_button_color":   assemble_color_option(get_start_button_color_options, "N64 Red"),
}

def assemble_sfx_option(sound_hook: sfx.SoundHooks):
    options = sfx.get_setting_choices(sound_hook).keys()
    sfx_to_id = {sfx.replace('-', '_'): index for index, sfx in enumerate(options)}
    class SfxOption(Choice):
        pass
    SfxOption.options.update(sfx_to_id)
    SfxOption.name_lookup.update({id: sfx for (sfx, id) in sfx_to_id.items()})
    return SfxOption

class SfxOcarina(Choice):
    option_ocarina = 1
    option_malon = 2
    option_whistle = 3
    option_harp = 4
    option_grind_organ = 5
    option_flute = 6
    default = 1

sfx_options: typing.Dict[str, type(Option)] = {
    "sfx_navi_overworld":   assemble_sfx_option(sfx.SoundHooks.NAVI_OVERWORLD),
    "sfx_navi_enemy":       assemble_sfx_option(sfx.SoundHooks.NAVI_ENEMY),
    "sfx_low_hp":           assemble_sfx_option(sfx.SoundHooks.HP_LOW),
    "sfx_menu_cursor":      assemble_sfx_option(sfx.SoundHooks.MENU_CURSOR),
    "sfx_menu_select":      assemble_sfx_option(sfx.SoundHooks.MENU_SELECT),
    "sfx_nightfall":        assemble_sfx_option(sfx.SoundHooks.NIGHTFALL),
    "sfx_horse_neigh":      assemble_sfx_option(sfx.SoundHooks.HORSE_NEIGH),
    "sfx_hover_boots":      assemble_sfx_option(sfx.SoundHooks.BOOTS_HOVER),
    "sfx_ocarina":          SfxOcarina,
}


# All options assembled into a single dict
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
    **cosmetic_options,
    **sfx_options,
    "logic_tricks": OptionList,
}
