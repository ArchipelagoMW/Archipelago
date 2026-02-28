"""Encryption and Decryption of settings strings."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Tuple

from randomizer.Enums.Settings import (
    LogicType,
    SettingsStringDataType,
    SettingsStringEnum,
    SettingsStringIntRangeMap,
    SettingsStringListTypeMap,
    SettingsStringTypeMap,
    SpoilerHints,
)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
index_to_letter = {i: letters[i] for i in range(64)}
letter_to_index = {letters[i]: i for i in range(len(letters))}


def int_to_bin_string(num, bytesize):
    """Convert an integer to a binary representation.

    This function is needed to handle negative numbers.
    """
    return format(num if num >= 0 else (1 << bytesize) + num, f"0{bytesize}b").zfill(bytesize)


def bin_string_to_int(bin_str: str, bytesize: int) -> int:
    """Convert a binary string to an integer.

    This function is needed to handle negative numbers.
    """
    if bin_str[0] == "1":
        return int(bin_str, 2) - (1 << bytesize)
    else:
        return int(bin_str, 2)


def get_var_int_encode_details(settingEnum: SettingsStringEnum) -> Tuple[int, bool]:
    """Return key information needed to encode/decode a given var_int setting.

    Returns:
        int - The bit length of the int.
        bool - True if negative numbers are possible.
    """
    range = SettingsStringIntRangeMap[settingEnum]
    max_val = range["max"]
    min_val = range["min"]
    limiting_val = max_val
    negatives_possible = min_val < 0
    if negatives_possible and abs(min_val) > max_val:
        # We subtract one, to handle the edge case where the absolute value is
        # a negative power of 2.
        limiting_val = abs(min_val) - 1
    # Get the bit length of the limiting value.
    bit_len = limiting_val.bit_length()
    # If negatives are possible, add one to the bit length.
    if negatives_possible:
        bit_len += 1
    return bit_len, negatives_possible


def encode_var_int(settingEnum, num):
    """Convert a variable-size integer to a binary representation."""
    bit_len, _ = get_var_int_encode_details(settingEnum)
    return int_to_bin_string(num, bit_len)


def decode_var_int(settingEnum: SettingsStringEnum, bin_str: str) -> int:
    """Convert a binary string to a variable-size integer."""
    bit_len, negatives_possible = get_var_int_encode_details(settingEnum)
    if negatives_possible:
        return bin_string_to_int(bin_str, bit_len)
    else:
        return int(bin_str, 2)


# A map tying certain key settings to other settings that should be excluded
# from the string, if the key setting has a certain value.
settingsExclusionMap = {
    "helm_hurry": {
        False: [
            "helmhurry_list_banana_medal",
            "helmhurry_list_battle_crown",
            "helmhurry_list_bean",
            "helmhurry_list_blueprint",
            "helmhurry_list_boss_key",
            "helmhurry_list_colored_bananas",
            "helmhurry_list_company_coins",
            "helmhurry_list_fairies",
            "helmhurry_list_golden_banana",
            "helmhurry_list_ice_traps",
            "helmhurry_list_kongs",
            "helmhurry_list_move",
            "helmhurry_list_pearl",
            "helmhurry_list_rainbow_coin",
            "helmhurry_list_starting_time",
        ]
    },
    "shuffle_items": {False: ["item_rando_list_selected"]},
    "cb_rando_enabled": {False: ["cb_rando_list_selected"]},
    "logic_type": {LogicType.glitchless: ["glitches_selected"], LogicType.nologic: ["glitches_selected"], LogicType.minimal: ["glitches_selected"]},
    "spoiler_hints": {
        SpoilerHints.off: [
            "points_list_kongs"
            "points_list_keys"
            "points_list_guns"
            "points_list_instruments"
            "points_list_training_moves"
            "points_list_fairy_moves"
            "points_list_important_shared"
            "points_list_pad_moves"
            "points_list_barrel_moves"
            "points_list_active_moves"
            "points_list_bean"
            "points_list_shopkeepers"
        ],
        SpoilerHints.vial_colors: [
            "points_list_kongs"
            "points_list_keys"
            "points_list_guns"
            "points_list_instruments"
            "points_list_training_moves"
            "points_list_fairy_moves"
            "points_list_important_shared"
            "points_list_pad_moves"
            "points_list_barrel_moves"
            "points_list_active_moves"
            "points_list_bean"
            "points_list_shopkeepers"
        ],
    },
}


def prune_settings(settings_dict: dict):
    """Remove certain settings based on the values of other settings."""
    settings_to_remove = ["plandomizer_data", "enable_song_select", "music_selections"]
    # Remove settings based on the exclusion map above.
    for keySetting, exclusions in settingsExclusionMap.items():
        if keySetting in settings_dict.keys() and settings_dict[keySetting] in exclusions:
            settings_to_remove.extend(exclusions[settings_dict[keySetting]])
    # Remove any deprecated settings.
    for pop in settings_to_remove:
        if pop in settings_dict:
            settings_dict.pop(pop)
    return settings_dict


def encrypt_settings_string_enum(dict_data: dict):
    """Take a dictionary and return an enum-based encrypted string.

    Args:
        dict_data (dict): Posted JSON data from the form.

    Returns:
        str: Returns an encrypted string.
    """
    for pop in [
        "download_patch_file",
        "load_patch_file",
        "seed",
        "settings_string",
        "chunky_main_colors",
        "chunky_main_custom_color",
        "chunky_other_colors",
        "chunky_other_custom_color",
        "diddy_clothes_colors",
        "diddy_clothes_custom_color",
        "dk_fur_colors",
        "dk_fur_custom_color",
        "dk_tie_colors",
        "dk_tie_custom_color",
        "enguarde_skin_colors",
        "enguarde_skin_custom_color",
        "klaptrap_model",
        "random_models",
        "random_enemy_colors",
        "misc_cosmetics",
        "disco_donkey",
        "disco_chunky",
        "rainbow_ammo",
        "dark_mode_textboxes",
        "pause_hint_coloring",
        "lanky_clothes_colors",
        "lanky_fur_colors",
        "lanky_clothes_custom_color",
        "lanky_fur_custom_color",
        "rambi_skin_colors",
        "rambi_skin_custom_color",
        "gb_colors",
        "gb_custom_color",
        "random_kong_colors",
        "random_music",
        "music_is_custom",
        "music_bgm_randomized",
        "music_events_randomized",
        "music_majoritems_randomized",
        "music_minoritems_randomized",
        "music_vanilla_locations",
        "tiny_hair_colors",
        "tiny_clothes_colors",
        "tiny_hair_custom_color",
        "tiny_clothes_custom_color",
        "override_cosmetics",
        "remove_water_oscillation",
        "fps_display",
        "head_balloons",
        "song_speed_near_win",
        "disable_flavor_text",
        "colorblind_mode",
        "big_head_mode",
        "search",
        "holiday_setting",
        "holiday_setting_offseason",
        "homebrew_header",
        "homebrew_header_patch",
        "dpad_display",
        "camera_is_follow",
        "sfx_volume",
        "music_volume",
        "true_widescreen",
        "anamorphic_widescreen",
        "camera_is_not_inverted",
        "sound_type",
        "smoother_camera",
        "songs_excluded",
        "excluded_songs_selected",
        "random_colors",
        "random_colors_selected",
        "music_filtering",
        "music_filtering_selected",
        "troff_brighten",
        "better_dirt_patch_cosmetic",
        "crosshair_outline",
        "custom_music_proportion",
        "fill_with_custom_music",
        "pool_tracks",
        "color_coded_powerups",
        "show_song_name",
        "delayed_spoilerlog_release",
        "shockwave_status",  # Deprecated with starting move selector rework - this is now derived in the settings constructor
        "music_disable_reverb",
        "isles_cool_musical",
        "archipelago",
        "bonus_barrel_rando",  # Deprecated with dropdown multiselector rework
        "hard_mode",  # Deprecated with dropdown multiselector rework
        "hard_bosses",  # Deprecated with dropdown multiselector rework
        "quality_of_life",  # Deprecated with dropdown multiselector rework
        "enemy_rando",  # Deprecated with dropdown multiselector rework
        "faster_checks_enabled",  # Deprecated with dropdown multiselector rework
        "remove_barriers_enabled",  # Deprecated with dropdown multiselector rework
        "",
    ]:
        if pop in dict_data:
            dict_data.pop(pop)
    dict_data = prune_settings(dict_data)
    bitstring = ""
    for sort_this in ["starting_moves_list_1", "starting_moves_list_2", "starting_moves_list_3", "starting_moves_list_4", "starting_moves_list_5"]:
        if sort_this in dict_data.keys():
            dict_data[sort_this].sort()
    for key in dict_data:
        value = dict_data[key]
        # At this time, all strings represent ints, so just convert.
        if isinstance(value, str):
            value = int(value)
        key_enum = SettingsStringEnum[key]
        key_data_type = SettingsStringTypeMap[key_enum]
        # Encode the key.
        key_size = max([member.value for member in SettingsStringEnum]).bit_length()
        bitstring += bin(key_enum)[2:].zfill(key_size)
        if key_data_type == SettingsStringDataType.bool:
            bitstring += "1" if value else "0"
        elif key_data_type == SettingsStringDataType.int4:
            bitstring += int_to_bin_string(value, 4)
        elif key_data_type in (SettingsStringDataType.int8, SettingsStringDataType.u8):
            bitstring += int_to_bin_string(value, 8)
        elif key_data_type in (SettingsStringDataType.int16, SettingsStringDataType.u16):
            bitstring += int_to_bin_string(value, 16)
        elif key_data_type == SettingsStringDataType.var_int:
            bitstring += encode_var_int(key_enum, value)
        elif key_data_type == SettingsStringDataType.list:
            bitstring += f"{len(value):08b}"
            key_list_data_type = SettingsStringListTypeMap[key_enum]
            for item in value:
                if isinstance(item, str):
                    item = int(item)
                if key_list_data_type == SettingsStringDataType.bool:
                    bitstring += "1" if item else "0"
                elif key_list_data_type == SettingsStringDataType.int4:
                    bitstring += int_to_bin_string(item, 4)
                elif key_list_data_type in (SettingsStringDataType.int8, SettingsStringDataType.u8):
                    bitstring += int_to_bin_string(item, 8)
                elif key_list_data_type in (SettingsStringDataType.int16, SettingsStringDataType.u16):
                    bitstring += int_to_bin_string(item, 16)
                elif key_list_data_type == SettingsStringDataType.var_int:
                    bitstring += encode_var_int(key_enum, item)
                else:
                    # The value is an enum.
                    max_value = max([member.value for member in key_list_data_type])
                    bitstring += format(item, f"0{max_value.bit_length()}b")
        else:
            # The value is an enum.
            max_value = max([member.value for member in key_data_type])
            # If value is an int
            if isinstance(value, int):
                bitstring += format(value, f"0{max_value.bit_length()}b")
            else:
                bitstring += format(value.value, f"0{max_value.bit_length()}b")

    # Pad the bitstring with zeroes until the length is divisible by 6.
    remainder = len(bitstring) % 6
    if remainder > 0:
        for _ in range(0, 6 - remainder):
            bitstring += "0"

    # Split the bitstring into 6-bit chunks and look up the corresponding
    # letters.
    letter_string = ""
    for i in range(0, len(bitstring), 6):
        chunk = int(bitstring[i : i + 6], 2)
        letter_string += letters[chunk]
    return letter_string


def decrypt_settings_string_enum(encrypted_string: str) -> Dict[str, Any]:
    """Take an enum-based encrypted string and return a dictionary.

    Args:
        encrypted_string (str): Passed settings string.

    Returns:
        dict: Returns the decrypted set of data.
    """
    # Take each letter of the encrypted_string and convert it to a 6-bit binary
    # number, then use the embedded keys to get the value from the settings
    # string.
    bitstring = ""
    for letter in encrypted_string:
        index = letter_to_index[letter]
        bitstring += f"{index:06b}"
    bitstring_length = len(bitstring)
    settings_dict = {}
    bit_index = 0
    key_size = max([member.value for member in SettingsStringEnum]).bit_length()
    # If there are fewer than (key_size + 1) characters left in our bitstring,
    # we have hit the padding. (key_size + 1 characters is the minimum needed
    # for a key and a value.)
    while bit_index < (bitstring_length - (key_size + 1)):
        # Consume the next key.
        key = int(bitstring[bit_index : bit_index + key_size], 2)
        bit_index += key_size
        key_enum = SettingsStringEnum(key)
        key_name = key_enum.name
        key_data_type = SettingsStringTypeMap[key_enum]
        val = None
        if key_data_type == SettingsStringDataType.bool:
            val = True if bitstring[bit_index] == "1" else False
            bit_index += 1
        elif key_data_type == SettingsStringDataType.int4:
            val = bin_string_to_int(bitstring[bit_index : bit_index + 4], 4)
            bit_index += 4
        elif key_data_type in (SettingsStringDataType.int8, SettingsStringDataType.u8):
            val = bin_string_to_int(bitstring[bit_index : bit_index + 8], 8)
            if key_data_type == SettingsStringDataType.u8 and val < 0:
                val += 256
            bit_index += 8
        elif key_data_type in (SettingsStringDataType.int16, SettingsStringDataType.u16):
            val = bin_string_to_int(bitstring[bit_index : bit_index + 16], 16)
            if key_data_type == SettingsStringDataType.u16 and val < 0:
                val += 65536
            bit_index += 16
        elif key_data_type == SettingsStringDataType.var_int:
            bit_len, _ = get_var_int_encode_details(key_enum)
            val = decode_var_int(key_enum, bitstring[bit_index : bit_index + bit_len])
            bit_index += bit_len
        elif key_data_type == SettingsStringDataType.list:
            list_length = int(bitstring[bit_index : bit_index + 8], 2)
            bit_index += 8
            val = []
            key_list_data_type = SettingsStringListTypeMap[key_enum]
            for _ in range(list_length):
                list_val = None
                if key_list_data_type == SettingsStringDataType.bool:
                    list_val = True if bitstring[bit_index] == "1" else False
                    bit_index += 1
                elif key_list_data_type == SettingsStringDataType.int4:
                    list_val = bin_string_to_int(bitstring[bit_index : bit_index + 4], 4)
                    bit_index += 4
                elif key_list_data_type in (SettingsStringDataType.int8, SettingsStringDataType.u8):
                    list_val = bin_string_to_int(bitstring[bit_index : bit_index + 8], 8)
                    if key_list_data_type == SettingsStringDataType.u8 and val < 0:
                        val += 256
                    bit_index += 8
                elif key_list_data_type in (SettingsStringDataType.int16, SettingsStringDataType.u16):
                    list_val = bin_string_to_int(bitstring[bit_index : bit_index + 16], 16)
                    if key_list_data_type == SettingsStringDataType.u16 and val < 0:
                        val += 65536
                    bit_index += 16
                elif key_data_type == SettingsStringDataType.var_int:
                    bit_len, _ = get_var_int_encode_details(key_enum)
                    list_val = decode_var_int(key_enum, bitstring[bit_index : bit_index + bit_len])
                    bit_index += bit_len
                else:
                    # The value is an enum.
                    max_value = max([member.value for member in key_list_data_type])
                    int_val = int(bitstring[bit_index : bit_index + max_value.bit_length()], 2)
                    list_val = key_list_data_type(int_val)
                    bit_index += max_value.bit_length()
                val.append(list_val)
        else:
            # The value is an enum.
            max_value = max([member.value for member in key_data_type])
            int_val = int(bitstring[bit_index : bit_index + max_value.bit_length()], 2)
            val = key_data_type(int_val)
            bit_index += max_value.bit_length()
        # If this setting is not deprecated, add it.
        # The plando setting needs to be encoded in settings strings but not applied when decoding for logging purposes.
        if key_enum != SettingsStringEnum.enable_plandomizer:
            settings_dict[key_name] = val
    return settings_dict
