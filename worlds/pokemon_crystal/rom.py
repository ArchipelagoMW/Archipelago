import logging
import os
import random
from collections import defaultdict
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

import bsdiff4

from Generate import roll_settings
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .data import data, MiscOption, EncounterType, FishingRodType, TreeRarity, MapPalette, PaletteData
from .item_data import POKEDEX_COUNT_OFFSET, POKEDEX_OFFSET, FLY_UNLOCK_OFFSET, GRASS_OFFSET
from .items import item_const_name_to_id
from .maps import FLASH_MAP_GROUPS
from .mart_data import BETTER_MART_MARTS
from .options import UndergroundsRequirePower, RequireItemfinder, Goal, Route2Access, Route42Access, \
    BlackthornDarkCaveAccess, NationalParkAccess, Route3Access, EncounterSlotDistribution, KantoAccessRequirement, \
    FreeFlyLocation, HMBadgeRequirements, ShopsanityPrices, WildEncounterMethodsRequired, FlyCheese, Shopsanity, \
    RequireFlash, FieldMoveMenuOrder, RedGyaradosAccess, TrainerPalette, PokemonCrystalOptions
from .pokemon_data import ALL_UNOWN
from .utils import convert_to_ingame_text, write_appp_tokens, write_rom_bytes, replace_map_tiles

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

CRYSTAL_1_0_HASH = "9f2922b235a5eeb78d65594e82ef5dde"
CRYSTAL_1_1_HASH = "301899b8087289a6436b0a241fbbb474"


class PokemonCrystalAPPatchExtension(APPatchExtension):
    game = data.manifest.game

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str):
        revision_address = data.rom_addresses["AP_ROM_Revision"]
        rom_bytes = bytearray(rom)
        if rom_bytes[revision_address] == 1:
            if "basepatch11.bsdiff4" not in caller.files:
                raise Exception("This patch was generated without support for Pokemon Crystal V1.1 ROM. "
                                "Please regenerate with a newer APWorld version or use a V1.0 ROM")
            return bsdiff4.patch(rom, caller.get_file("basepatch11.bsdiff4"))
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_overrides(caller: APProcedurePatch, rom: bytes) -> bytes:
        option_overrides = get_settings().pokemon_crystal_settings.option_overrides

        if "skip_elite_four" in option_overrides:
            for trainer_name in ("WILL", "KOGA", "BRUNO", "KAREN"):
                if rom[data.rom_addresses[f"AP_AdhocTrainersanity_ITEM_FROM_ELITE_4_{trainer_name}"]] != 0:
                    logging.warning("Pokemon Crystal: One or more Elite 4 trainers is a trainersanity location. "
                                    "Ignoring skip_elite_four override.")
                    option_overrides.pop("skip_elite_four", None)
                    break

        if not option_overrides:
            return rom

        wrapped_overrides = {
            "game": data.manifest.game,
            data.manifest.game: option_overrides
        }
        rolled_options = roll_settings(wrapped_overrides)

        overridden_rom = bytearray(rom)
        write_bytes = lambda data, address: write_rom_bytes(overridden_rom, data, address)
        must_write_option = lambda option_key: option_key in option_overrides

        if must_write_option("game_options"):
            game_option_overrides = rolled_options.game_options
            game_options_address = data.rom_addresses["AP_Setting_DefaultOptions"]
            num_option_bytes = max([item.option_byte_index for item in data.game_settings.values()]) + 1
            option_bytes = overridden_rom[game_options_address:game_options_address + num_option_bytes]

            for setting_name, setting in data.game_settings.items():
                option_selection = game_option_overrides.get(setting_name, None)
                if option_selection is None:
                    continue
                if setting_name == "text_frame" and option_selection == "random":
                    option_selection = random.randint(1, 8)
                if setting_name == "time_of_day" and option_selection == "random":
                    option_selection = random.choice(("morn", "day", "nite"))
                if setting_name == "_death_link":
                    option_selection = "on" if game_option_overrides.get("death_link", False) else "off"
                elif setting_name == "_trap_link":
                    option_selection = "on" if game_option_overrides.get("trap_link", False) else "off"
                setting.set_option_byte(option_selection, option_bytes)

            write_bytes(option_bytes, game_options_address)

        write_customizable_options(rolled_options, write_bytes, must_write_option)

        return overridden_rom


class PokemonCrystalProcedurePatch(APProcedurePatch, APTokenMixin):
    game = data.manifest.game
    hash = [CRYSTAL_1_0_HASH, CRYSTAL_1_1_HASH]
    patch_file_ending = ".apcrystal"
    result_file_ending = ".gbc"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
        ("apply_overrides", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_customizable_options(options: PokemonCrystalOptions,
                               write_bytes: Callable[[bytes | Sequence[int], int], None],
                               must_write_option: Callable[[str], bool]
                               ) -> None:
    if must_write_option("field_move_menu_order"):
        write_bytes([FieldMoveMenuOrder.default.index(val) for val in options.field_move_menu_order.value],
                    data.rom_addresses["AP_Setting_Field_Move_Order"])

    if must_write_option("trainer_name"):
        name_bytes = convert_to_ingame_text(options.trainer_name.value[:7], string_terminator=True)
        write_bytes(name_bytes, data.rom_addresses["AP_Setting_DefaultTrainerName"])

    if must_write_option("default_pokedex_mode"):
        write_bytes([options.default_pokedex_mode.value], data.rom_addresses["AP_Setting_DefaultDexMode"] + 1)

    if must_write_option("trainer_palette"):
        if options.trainer_palette.value == TrainerPalette.option_vanilla:
            chris_palette_data = next(
                palette for palette in data.palettes if palette.index == TrainerPalette.option_red - 1)
            kris_palette_data = next(
                palette for palette in data.palettes if palette.index == TrainerPalette.option_blue - 1)
        else:
            chris_palette_data = next(
                palette for palette in data.palettes if palette.index == options.trainer_palette - 1)
            kris_palette_data = chris_palette_data

        chris_addresses = ("AP_Setting_ChrisWalkSpriteData", "AP_Setting_ChrisBikeSpriteData",
                           "AP_Setting_ChrisRunSpriteData")
        kris_addresses = ("AP_Setting_KrisWalkSpriteData", "AP_Setting_KrisBikeSpriteData",
                          "AP_Setting_KrisRunSpriteData")

        for address_ref in chris_addresses:
            write_bytes([chris_palette_data.index], data.rom_addresses[address_ref] + 5)
        for address_ref in kris_addresses:
            write_bytes([kris_palette_data.index], data.rom_addresses[address_ref] + 5)

        for i in range(1, 5):
            chris_byte = (chris_palette_data.index + PaletteData.NPC_PAL_OFFSET) << 4
            kris_byte = (kris_palette_data.index + PaletteData.NPC_PAL_OFFSET) << 4
            write_bytes([chris_byte], data.rom_addresses[f"AP_Setting_ChrisSpritePalette_{i}"] + 1)
            write_bytes([kris_byte], data.rom_addresses[f"AP_Setting_KrisSpritePalette_{i}"] + 1)

        write_bytes([chris_palette_data.index], data.rom_addresses["AP_Setting_ChrisIntroPal"] + 1)
        write_bytes([kris_palette_data.index], data.rom_addresses["AP_Setting_KrisIntroPal"] + 1)

        write_bytes(chris_palette_data.battle_palette, data.rom_addresses["AP_Setting_ChrisBattlePalette"])
        write_bytes(kris_palette_data.battle_palette, data.rom_addresses["AP_Setting_KrisBattlePalette"])

        address = data.rom_addresses["AP_Setting_OAMBlueWalk"] + 4
        for i in range(4):
            write_bytes([kris_palette_data.index], address)
            address += 4

        address = data.rom_addresses["AP_Setting_OAMRedWalk"] + 4
        for i in range(4):
            write_bytes([chris_palette_data.index], address)
            address += 4

        address = data.rom_addresses["AP_Setting_OAMMagnetTrainBlue"] + 4
        for i in range(4):
            write_bytes([kris_palette_data.index | PaletteData.PRIORITY], address)
            address += 4

        address = data.rom_addresses["AP_Setting_OAMMagnetTrainRed"] + 4
        for i in range(4):
            write_bytes([chris_palette_data.index | PaletteData.PRIORITY], address)
            address += 4

    if must_write_option("reusable_tms"):
        patched_value = 1 if options.reusable_tms.value else 0
        address = data.rom_addresses["AP_Setting_ReusableTMs"] + 1
        write_bytes([patched_value], address)

    if must_write_option("minimum_catch_rate"):
        address = data.rom_addresses["AP_Setting_MinCatchrate"] + 1
        write_bytes([options.minimum_catch_rate.value], address)

    if must_write_option("experience_modifier"):
        exp_modifier_address = data.rom_addresses["AP_Setting_ExpModifier"]
        write_bytes([options.experience_modifier.value], exp_modifier_address)

    if must_write_option("skip_elite_four"):
        # Set warp to Lance's room or set it back to Will's
        e4_warp = 0x07 if options.skip_elite_four.value else 0x03
        write_bytes([e4_warp], data.rom_addresses["AP_Setting_IndigoPlateauPokecenter1F_E4Warp"] + 4)

    if must_write_option("shopsanity_restrict_rare_candies"):
        patched_value = 1 if options.shopsanity_restrict_rare_candies.value else 0
        address = data.rom_addresses["AP_Setting_ShopsanityRestrictRareCandies"] + 1
        write_bytes([patched_value], address)

    # if must_write_option("all_pokemon_seen"):
    #     patched_value = 1 if options.all_pokemon_seen.value else 0
    #     write_bytes([patched_value], data.rom_addresses["AP_Setting_AllPokemonSeen_1"] + 1)
    #     write_bytes([patched_value], data.rom_addresses["AP_Setting_AllPokemonSeen_2"] + 1)

    if must_write_option("starting_money"):
        start_money = options.starting_money.value.to_bytes(3, "big")
        for i, byte in enumerate(start_money):
            write_bytes([byte], data.rom_addresses[f"AP_Setting_StartMoney_{i + 1}"] + 1)

    if must_write_option("better_marts"):
        patched_value = 1 if options.better_marts.value else 0
        write_bytes([patched_value], data.rom_addresses["AP_Setting_BetterMarts"] + 1)

    if must_write_option("build_a_mart"):
        custom_mart_base = data.rom_addresses["AP_Setting_CustomBetterMart"]

        available_items = {item.label: item.item_const for item in data.items.values()
                           if "CustomShop" in item.tags}

        selected_items = []
        for item_name in options.build_a_mart.value:
            if item_name in available_items:
                selected_items.append(available_items[item_name])

        if len(selected_items) > 14:
            selected_items = selected_items[:14]

        total_items = len(selected_items) + 2
        write_bytes([total_items], custom_mart_base)

        current_address = custom_mart_base + 11
        for item_const in selected_items:
            item_id = item_const_name_to_id(item_const)
            item_data = data.items[item_id]
            price_bytes = item_data.price.to_bytes(2, "little")
            write_bytes([item_id, *price_bytes, 0xFF, 0xFF], current_address)
            current_address += 5

        write_bytes([0xFF], current_address)


def generate_output(world: "PokemonCrystalWorld", output_directory: str, patch: PokemonCrystalProcedurePatch) -> None:
    write_bytes = lambda data, address: write_appp_tokens(patch, data, address)
    # The vanilla value of an option evaluates to False
    must_write_option = lambda option_key: bool(getattr(world.options, option_key))

    option_bytes = bytearray(max([item.option_byte_index for item in data.game_settings.values()]) + 1)

    for setting_name, setting in data.game_settings.items():
        option_selection = world.options.game_options.get(setting_name, None)
        if setting_name == "text_frame" and option_selection == "random":
            option_selection = world.random.randint(1, 8)
        if setting_name == "time_of_day" and option_selection == "random":
            option_selection = world.random.choice(("morn", "day", "nite"))
        if setting_name == "_death_link":
            option_selection = "on" if world.options.death_link else "off"
        if setting_name == "_trap_link":
            option_selection = "on" if world.options.trap_link else "off"
        setting.set_option_byte(option_selection, option_bytes)

    write_bytes(option_bytes, data.rom_addresses["AP_Setting_DefaultOptions"])

    def write_item(item: int, addresses: list[int]) -> None:
        for address in addresses:
            write_bytes([item], address)
            if address in data.adhoc_trainersanity:
                write_bytes([1], data.adhoc_trainersanity[address])

    item_texts = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.address >= GRASS_OFFSET:
            location_addresses = location.rom_addresses
        elif location.address > POKEDEX_COUNT_OFFSET:
            location_addresses = [data.rom_addresses["AP_DexcountsanityItems"] + address - 1 for address in
                                  location.rom_addresses]
        elif location.address > POKEDEX_OFFSET:
            location_addresses = [data.rom_addresses["AP_DexsanityItems"] + address - 1 for address in
                                  location.rom_addresses]
        else:
            location_addresses = location.rom_addresses

        if not world.options.remote_items and location.item and location.item.player == world.player:
            item_id = location.item.code
            if item_id >= FLY_UNLOCK_OFFSET:
                write_item(item_const_name_to_id("FLY_UNLOCK"), location_addresses)

                if location.address >= GRASS_OFFSET:
                    if hasattr(location, "original_grass_flag"):
                        grass_address = location.original_grass_flag
                    else:
                        grass_address = location.address
                    event_id = 0xF000 + (grass_address - GRASS_OFFSET)
                elif location.address > POKEDEX_COUNT_OFFSET:
                    event_id = 0xFE00 + (location.address - POKEDEX_COUNT_OFFSET) - 1
                elif location.address > POKEDEX_OFFSET:
                    event_id = 0xFF00 + (location.address - POKEDEX_OFFSET) - 1
                else:
                    event_id = location.address

                fly_id = item_id - FLY_UNLOCK_OFFSET
                write_bytes(event_id.to_bytes(2, "little"),
                            data.rom_addresses["AP_Setting_FlyUnlockTable"] + (fly_id * 3))
            else:
                write_item(item_id, location_addresses)
        else:
            # for in game text
            if location.address < POKEDEX_OFFSET:
                item_flag = location.address
                player_name = world.multiworld.player_name[location.item.player].upper()
                item_name = location.item.name.upper()
                item_texts.append((player_name, item_name, item_flag, "shopsanity" in location.tags))

            write_item(item_const_name_to_id("AP_ITEM"), location_addresses)

    # table has format: location id (2 bytes), string address (2 bytes), string bank (1 byte),
    # and is terminated by 0xFF
    item_name_table_length = len([entry for entry in item_texts if not entry[3]]) * 5 + 1
    item_name_table_adr = data.rom_addresses["AP_ItemText_Table"]
    shopsanity_name_table_length = len([entry for entry in item_texts if entry[3]]) * 5 + 1
    shopsanity_name_table_adr = data.rom_addresses["AP_MartItemTable"]

    # strings are 16 chars each, plus a terminator byte,
    # this gives every pair of item + player names a size of 34 bytes
    item_name_bank1 = item_name_table_adr + item_name_table_length
    item_name_bank1_length = data.rom_addresses["AP_ItemText_Bank1_End"] - item_name_bank1
    item_name_bank1_capacity = int(item_name_bank1_length / 34)

    item_name_bank2 = data.rom_addresses["AP_ItemText_Bank2"]
    item_name_bank2_length = data.rom_addresses["AP_ItemText_Bank2_End"] - item_name_bank2
    item_name_bank2_capacity = int(item_name_bank2_length / 34)

    item_name_bank3 = data.rom_addresses["AP_ItemText_Bank3"]
    item_name_bank3_length = data.rom_addresses["AP_ItemText_Bank3_End"] - item_name_bank3
    item_name_bank3_capacity = int(item_name_bank3_length / 34)

    table_offset_adr = item_name_table_adr
    shopsanity_table_offset_adr = shopsanity_name_table_adr

    for i, text in enumerate(item_texts):
        shopsanity_entry = text[3]
        # truncate if too long
        player_text = convert_to_ingame_text(text[0])[:16]
        # pad with terminator byte to keep alignment
        player_text.extend([0x50] * (17 - len(player_text)))
        item_text = convert_to_ingame_text(text[1])[:14 if shopsanity_entry else 16]
        item_text.append(0x50)
        # bank 1
        bank = 0x75

        if i >= item_name_bank1_capacity + item_name_bank2_capacity + item_name_bank3_capacity:
            # if we somehow run out of capacity in all banks, just finish the table and break,
            # there is a fallback string in the ROM, so it should handle this gracefully.
            write_bytes([0xFF], item_name_table_adr + table_offset_adr)
            write_bytes([0xFF], shopsanity_name_table_adr + shopsanity_table_offset_adr)
            print("oopsie")
            break
        if i + 1 < item_name_bank1_capacity:
            text_offset = i * 34
            text_adr = item_name_bank1 + text_offset
        elif i + 1 < (item_name_bank1_capacity + item_name_bank2_capacity):
            # bank 2
            bank = 0x76
            text_offset = (i + 1 - item_name_bank1_capacity) * 34
            text_adr = item_name_bank2 + text_offset
        else:
            # bank 3
            bank = 0x7c
            text_offset = (i + 1 - (item_name_bank1_capacity + item_name_bank2_capacity)) * 34
            text_adr = item_name_bank3 + text_offset
        write_bytes(player_text + item_text, text_adr)
        # get the address within the rom bank (0x4000 - 0x7FFF)
        text_bank_adr = (text_adr % 0x4000) + 0x4000
        offset_adr = shopsanity_table_offset_adr if shopsanity_entry else table_offset_adr
        write_bytes(((text[2] - data.mart_flag_offset) if shopsanity_entry else text[2]).to_bytes(2, "big"),
                    offset_adr)
        write_bytes(text_bank_adr.to_bytes(2, "little"), offset_adr + 2)
        write_bytes([bank], offset_adr + 4)

        if shopsanity_entry:
            shopsanity_table_offset_adr += 5
        else:
            table_offset_adr += 5

    write_bytes([0xFF], item_name_table_adr + item_name_table_length - 1)
    write_bytes([0xFF], shopsanity_name_table_adr + shopsanity_name_table_length - 1)

    if Shopsanity.johto_marts in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_JohtoShopsanityEnabled"] + 2)
        # the dw at +11 is the event flag.
        write_bytes([0xFF, 0xFF], data.rom_addresses["AP_Setting_Shopsanity_MahoganyMart_1"] + 11)
        write_bytes([0xFF, 0xFF], data.rom_addresses["AP_Setting_Shopsanity_MahoganyMart_2"] + 11)

    if Shopsanity.kanto_marts in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_KantoShopsanityEnabled"] + 2)

    if Shopsanity.blue_card in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_BlueCardShopsanityEnabled"] + 2)

    if Shopsanity.game_corners in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_GameCornerShopsanityEnabled"] + 2)

    if Shopsanity.apricorns in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_ApricornShopsanityEnabled"] + 2)

    if world.options.shopsanity:

        min_shop_price = world.options.shopsanity_minimum_price.value
        max_shop_price = world.options.shopsanity_maximum_price.value
        total_shop_spheres = len(world.shop_locations_by_spheres)

        remote_items = world.options.remote_items.value

        by_item_price = world.options.shopsanity_prices == ShopsanityPrices.option_item_price

        by_spheres = world.options.shopsanity_prices in (
            ShopsanityPrices.option_spheres,
            ShopsanityPrices.option_spheres_and_classification
        )
        by_classification = world.options.shopsanity_prices in (
            ShopsanityPrices.option_classification,
            ShopsanityPrices.option_spheres_and_classification
        )
        by_location = world.options.shopsanity_prices == ShopsanityPrices.option_vanilla

        if world.options.shopsanity_minimum_price > world.options.shopsanity_maximum_price:
            logging.info("Pokemon Crystal: Minimum Shopsanity Price for player %s (%s)"
                         " is greater than Maximum Shopsanity Price.",
                         world.player, world.player_name)
            min_shop_price = world.options.shopsanity_maximum_price.value
            max_shop_price = world.options.shopsanity_minimum_price.value

        for i, locations in enumerate(world.shop_locations_by_spheres):
            sphere_min_shop_price = min_shop_price
            sphere_max_shop_price = max_shop_price
            if by_spheres:
                base_price = sphere_min_shop_price
                price_difference = max_shop_price - min_shop_price
                sphere_min_shop_price = int(round(base_price + ((price_difference / total_shop_spheres) * i)))
                sphere_max_shop_price = int(round(base_price + ((price_difference / total_shop_spheres) * (i + 1))))

            for location in locations:
                item_min_shop_price = sphere_min_shop_price
                item_max_shop_price = sphere_max_shop_price

                item_price = location.item.price if location.item.player == world.player else 0
                location_price = location.price

                if by_item_price:
                    if item_price < item_min_shop_price:
                        item_price = item_min_shop_price
                    elif item_price > item_max_shop_price:
                        item_price = item_max_shop_price
                    item_min_shop_price = item_price
                    item_max_shop_price = item_price
                elif by_classification:
                    base_price = item_min_shop_price
                    price_difference = item_max_shop_price - item_min_shop_price
                    if location.item.advancement:
                        item_min_shop_price = base_price + int(round(price_difference * 0.6))
                    elif location.item.useful:
                        item_min_shop_price = base_price + int(round(price_difference * 0.2))
                        item_max_shop_price = base_price + int(round(price_difference * 0.6))
                    else:
                        item_max_shop_price = base_price + int(round(price_difference * 0.2))
                elif by_location:
                    item_min_shop_price = location_price
                    item_max_shop_price = location_price

                if not remote_items and item_min_shop_price < item_price // 2:
                    item_min_shop_price = item_price // 2

                address = location.rom_addresses[0] + 1
                shop_price = world.random.randint(item_min_shop_price, item_max_shop_price) \
                    if item_max_shop_price > item_min_shop_price else item_min_shop_price
                logging.debug(f"Setting ¥{shop_price} for {location.name}")
                shop_price_bytes = shop_price.to_bytes(2, "little")
                write_bytes(shop_price_bytes, address)

    world.finished_level_scaling.wait()

    for _, pkmn_data in world.generated_static.items():
        pokemon_id = data.pokemon[pkmn_data.pokemon].id
        if pkmn_data.level_type == "gamecorner":
            addresses = pkmn_data.addresses[:-1]
        else:
            addresses = pkmn_data.addresses

        for address in addresses:
            cur_address = data.rom_addresses[address] + 1
            write_bytes([pokemon_id], cur_address)

        if pkmn_data.level_type == "gamecorner":
            static_name = world.generated_pokemon[pkmn_data.pokemon].friendly_name.upper()
            static_name = "NIDORAN♀" if static_name == "NIDORAN F" else static_name
            static_name = "NIDORAN♂" if static_name == "NIDORAN M" else static_name
            static_text = convert_to_ingame_text(static_name)

            write_bytes(static_text, data.rom_addresses[pkmn_data.addresses[-1]])

        if pkmn_data.level_address is not None:
            if pkmn_data.level_type in ("givepoke", "loadwildmon", "gamecorner"):
                write_bytes([pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 2)
            elif pkmn_data.level_type == "custom":
                write_bytes([pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 1)

    if world.options.randomize_trades:
        trade_table_address = data.rom_addresses["AP_Setting_TradeTable"]
        for trade in world.generated_trades.values():
            trade_address = trade_table_address + (trade.index * 32)  # each trade record is 32 bytes
            requested = data.pokemon[trade.requested_pokemon].id
            write_bytes([requested], trade_address + 1)

            received = data.pokemon[trade.received_pokemon].id
            write_bytes([received], trade_address + 2)

            write_bytes([trade.requested_gender], trade_address + 30)

            item_id = item_const_name_to_id(trade.held_item)
            write_bytes([item_id], trade_address + 16)

    if world.options.randomize_starters:
        for j, pokemon in enumerate(["CYNDAQUIL_", "TOTODILE_", "CHIKORITA_"]):
            pokemon_id = data.pokemon[world.generated_starters[j][0]].id
            starter_name = world.generated_pokemon[world.generated_starters[j][0]].friendly_name.upper()
            starter_name = "NIDORAN♀" if starter_name == "NIDORAN F" else starter_name
            starter_name = "NIDORAN♂" if starter_name == "NIDORAN M" else starter_name
            starter_text = convert_to_ingame_text(starter_name)
            for i in range(1, 9):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)] + 1
                write_bytes([pokemon_id], cur_address)
                if i == 4:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes([helditem], cur_address + 2)
                if i == 8:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes([helditem], cur_address + 10)
            for i in range(9, 10):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)]
                write_bytes(starter_text + [0x7f] * (10 - len(starter_text)), cur_address)

    tree_encounter_rates = []
    rock_encounter_rates = []
    if world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_balanced:
        tree_encounter_rates = [20, 20, 20, 15, 15, 10]
        rock_encounter_rates = [70, 30]
    elif world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_equal:
        tree_encounter_rates = [16, 16, 17, 17, 17, 17]
        rock_encounter_rates = [50, 50]

    for region_key, encounters in world.generated_wild.items():
        if region_key.encounter_type is EncounterType.Grass:
            cur_address = data.rom_addresses[f"AP_WildGrass_{region_key.region_id}"] + 3

            for _ in range(3):  # morn, day, nite
                for encounter in encounters:
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes([encounter.level, pokemon_id], cur_address)
                    cur_address += 2

        elif region_key.encounter_type is EncounterType.Water:
            cur_address = data.rom_addresses[f"AP_WildWater_{region_key.region_id}"] + 1
            for encounter in encounters:
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([encounter.level, pokemon_id], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.Fish:
            cur_address = data.rom_addresses[f"AP_FishMons_{region_key.region_id}"]
            if region_key.fishing_rod is FishingRodType.Good:
                cur_address += 9  # skip the first 3 encounters, each encounter is 3 bytes
            elif region_key.fishing_rod is FishingRodType.Super:
                cur_address += 21  # skip the first 7 encounters

            for i, encounter in enumerate(encounters):
                if world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_equal:
                    # fishing encounter rates are stored as an increasing fraction of 255
                    encounter_rate = int(((i + 1) / len(encounters)) * 255)
                    write_bytes([encounter_rate], cur_address)
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([pokemon_id, encounter.level], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.Tree:
            cur_address = data.rom_addresses[f"TreeMonSet_{region_key.region_id}"]
            if region_key.rarity is TreeRarity.Rare:
                cur_address += 19  # skip the first 6 encounters + terminator byte, each encounter is 3 bytes
            for i, encounter in enumerate(encounters):
                if tree_encounter_rates:
                    write_bytes([tree_encounter_rates[i]], cur_address)
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([pokemon_id, encounter.level], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.RockSmash:
            cur_address = data.rom_addresses["TreeMonSet_Rock"]
            for i, encounter in enumerate(encounters):
                if rock_encounter_rates:
                    write_bytes([rock_encounter_rates[i]], cur_address)
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([pokemon_id, encounter.level], cur_address)
                cur_address += 2

    wooper_sprite_address = data.rom_addresses["AP_Setting_Intro_Wooper_1"] + 1
    wooper_cry_address = data.rom_addresses["AP_Setting_Intro_Wooper_2"] + 1
    wooper_id = data.pokemon[world.generated_wooper].id
    write_bytes([wooper_id], wooper_sprite_address)
    write_bytes([wooper_id], wooper_cry_address)

    grass_probs = []
    water_probs = []

    if world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_remove_one_percents:
        grass_probs = [30, 55, 75, 85, 90, 95, 100]
    elif world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_equal:
        grass_probs = [14, 28, 42, 57, 71, 85, 100]
        water_probs = [33, 66, 100]
    elif world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_balanced:
        grass_probs = [20, 40, 55, 70, 80, 90, 100]

    if grass_probs:
        grass_prob_table = [f(x) for x in enumerate(grass_probs) for f in (lambda x: x[1], lambda x: x[0] * 2)]
        write_bytes(grass_prob_table, data.rom_addresses["AP_Prob_GrassMon"])

    if water_probs:
        water_prob_table = [f(x) for x in enumerate(water_probs) for f in (lambda x: x[1], lambda x: x[0] * 2)]
        write_bytes(water_prob_table, data.rom_addresses["AP_Prob_WaterMon"])

    if world.options.randomize_berry_trees:
        write_bytes([1], data.rom_addresses["AP_Setting_BerryTrees"] + 1)
        # 0xC9 = ret
        write_bytes([0xC9], data.rom_addresses["AP_Setting_FruitTreesReset"])

    for move_name, move in world.generated_moves.items():  # effect modification is also possible but not included
        if move_name in ("NO_MOVE", "CURSE"):
            continue

        address = data.rom_addresses["AP_MoveData_Type_" + move_name]
        move_category_type = [world.generated_types[move.type].rom_id | move.category]
        write_bytes(move_category_type, address)

        address = data.rom_addresses["AP_MoveData_Power_" + move_name]
        write_bytes([move.power], address)  # power 20-150

        address = data.rom_addresses["AP_MoveData_PP_" + move_name]
        write_bytes([move.pp], address)  # 5-40 PP

        address = data.rom_addresses["AP_MoveData_Accuracy_" + move_name]
        acc = int(move.accuracy * 255 / 100)
        write_bytes([acc], address)  # accuracy 30-100

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        address = data.rom_addresses["AP_Stats_Types_" + pkmn_name]
        if world.options.randomize_types.value:
            pkmn_types = [pkmn_data.types[0], pkmn_data.types[-1]]
            type_ids = [world.generated_types[pkmn_types[0]].rom_id, world.generated_types[pkmn_types[1]].rom_id]
            write_bytes(type_ids, address)

        address += 15  # growth rate lives 15 bytes after type1
        write_bytes([pkmn_data.growth_rate], address)

        if world.options.randomize_base_stats.value:
            address = data.rom_addresses["AP_Stats_Base_" + pkmn_name]
            write_bytes(pkmn_data.base_stats, address)

        if world.options.randomize_evolution:
            address = data.rom_addresses["AP_Evos_" + pkmn_name]
            for evo in pkmn_data.evolutions:
                evo_pkmn_id = data.pokemon[evo.pokemon].id
                if evo_pkmn_id == pkmn_name:
                    if len(evo.evo_type) < 4:
                        # Edge case: no valid evolution found, is not Tyrogue
                        write_bytes([evo.evo_type.value, evo.condition, evo_pkmn_id], address)
                        address += len(evo.evo_type)
                    else:
                        # Edge case: no valid evolution found, is Tyrogue
                        write_bytes([evo.evo_type.value, evo.level], address)
                        write_bytes([evo_pkmn_id], address + 3)
                        address += len(evo.evo_type)
                else:
                    # Normal case
                    address += len(evo.evo_type) - 1
                    # Enums over evolution conditions would be needed to write the whole evolution data for all cases
                    write_bytes([evo_pkmn_id], address)
                    address += 1

        if world.options.randomize_learnsets.value:
            address = data.rom_addresses["AP_Attacks_" + pkmn_name]
            for move in pkmn_data.learnset:
                move_id = data.moves[move.move].rom_id
                write_bytes([move.level, move_id], address)
                address += 2

        if pkmn_name in world.generated_palettes:
            palettes = world.generated_palettes[pkmn_name]
            address = data.rom_addresses["AP_Stats_Palette_" + pkmn_name]
            write_bytes(palettes, address)

        tm_bytes = [0, 0, 0, 0, 0, 0, 0, 0]
        for tm in pkmn_data.tm_hm:
            tm_num = data.tmhm[tm].tm_num
            tm_bytes[int((tm_num - 1) / 8)] |= 1 << (tm_num - 1) % 8
        tm_address = data.rom_addresses["AP_Stats_TMHM_" + pkmn_name]
        write_bytes(tm_bytes, tm_address)

    if world.options.randomize_type_chart:
        for type_id, type_data in world.generated_types.items():
            address = data.rom_addresses["AP_Setting_TypeMatchups_" + type_id] - 1
            for _, matchup in sorted(
                    type_data.matchups.items(), key=lambda matchup: world.generated_types[matchup[0]].rom_id):
                address += 3
                write_bytes([matchup], address)

    if world.options.randomize_breeding:
        base_address = data.rom_addresses["AP_Setting_EggMons"]

        for pokemon_data in world.generated_pokemon.values():
            index = pokemon_data.id - 1
            produces_egg_id = world.generated_pokemon[pokemon_data.produces_egg].id
            write_bytes([produces_egg_id], base_address + index)

    for trainer_name, trainer_data in world.generated_trainers.items():
        address = data.rom_addresses["AP_TrainerParty_" + trainer_name]
        address += trainer_data.name_length + 1  # skip name and type
        for pokemon in trainer_data.pokemon:
            pokemon_data = [pokemon.level, data.pokemon[pokemon.pokemon].id]
            if pokemon.item is not None:
                item_id = item_const_name_to_id(pokemon.item)
                pokemon_data.append(item_id)
            for move in pokemon.moves:
                move_id = data.moves[move].rom_id
                pokemon_data.append(move_id)
            write_bytes(pokemon_data, address)
            address += len(pokemon_data)

    if world.options.randomize_tm_moves.value or world.options.metronome_only.value or world.options.tm_plando.value:
        tm_moves = [tm_data.move_id for _name, tm_data in world.generated_tms.items()]
        address = data.rom_addresses["AP_Setting_TMMoves"]
        write_bytes(tm_moves, address)

        address = data.rom_addresses["AP_Setting_GoldenrodMoveTutorMoveNames"]
        for tm in ("FLAMETHROWER", "THUNDERBOLT", "ICE_BEAM"):
            move_data = world.generated_moves[world.generated_tms[tm].id]
            move_name = convert_to_ingame_text(move_data.name + " " * (12 - len(move_data.name)),
                                               string_terminator=True)
            write_bytes(move_name, address)
            address += 13

        for tm in ("FLAMETHROWER", "THUNDERBOLT", "ICE_BEAM"):
            move_id = world.generated_tms[tm].move_id
            address = data.rom_addresses["AP_Setting_MoveTutor_" + tm] + 1
            write_bytes([move_id], address)

    if world.options.enable_mischief:
        if MiscOption.FuchsiaGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_FuchsiaTrainers"] + 1
            write_bytes([0x0a], address + 2)  # spin speed
            for c in world.generated_misc.fuchsia_gym_trainers:
                write_coords = [c[1] + 4, c[0] + 4]
                write_bytes(write_coords, address)
                address += 13

        if MiscOption.SaffronGym.value in world.generated_misc.selected:
            for pair in world.generated_misc.saffron_gym_warps.pairs:
                addresses = [data.rom_addresses["AP_Misc_SaffronGymWarp_" + warp] + 2 for warp in pair]
                ids = [world.generated_misc.saffron_gym_warps.warps[warp].id for warp in pair]
                write_bytes([ids[1]], addresses[0])  # reverse ids
                write_bytes([ids[0]], addresses[1])

        if MiscOption.EcruteakGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Ecruteak_Gym_Warp"]
            write_bytes([2, 5], address)

        if MiscOption.OhkoMoves.value in world.generated_misc.selected:
            for move in ("GUILLOTINE", "HORN_DRILL", "FISSURE"):
                address = data.rom_addresses["AP_MoveData_Effect_" + move]
                write_bytes([0x65], address)  # false swipe effect
                address = data.rom_addresses["AP_MoveData_Power_" + move]
                write_bytes([0xFF], address)  # power 255
                address = data.rom_addresses["AP_MoveData_Accuracy_" + move]
                write_bytes([0xFF], address)  # accuracy 100%
                address = data.rom_addresses["AP_MoveData_PP_" + move]
                write_bytes([0x14], address)  # 20 PP

        if MiscOption.RadioTowerQuestions.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_N"] + 1
            # bad pokedex rating jingle
            write_bytes([0x9F], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y2"] + 1
            # increasing pokedex rating jingles
            write_bytes([0xA0], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y3"] + 1
            write_bytes([0xA1], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y4"] + 1
            write_bytes([0xA2], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y5"] + 1
            write_bytes([0xA3], address)
            for i in range(0, 5):
                answer = world.generated_misc.radio_tower_questions[i]
                # # 0x08 is iffalse (.WrongAnswer), 0x09 is iftrue (.WrongAnswer)
                byte = 0x08 if answer == "Y" else 0x09
                address = data.rom_addresses["AP_Misc_RadioTower_Q" + str(i + 1)]
                write_bytes([byte], address)

        if MiscOption.FanClubChairman.value in world.generated_misc.selected:
            # gives the chairman a 15/16 chance of repeating the rapidash rant each time
            address = data.rom_addresses["AP_Misc_Rapidash_Loop"] + 1
            write_bytes([1], address)

        if MiscOption.Amphy.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Amphy"] + 1
            write_bytes([1], address)

        if MiscOption.SecretSwitch.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_SecretSwitch"] + 1
            write_bytes([1], address)

        if MiscOption.RedGyarados.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RedGyarados"] + 1
            write_bytes([1], address)

        if MiscOption.RadioChannels.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioChannels"]
            for channel_addr in world.generated_misc.radio_channel_addresses:
                write_bytes(channel_addr.to_bytes(2, "little"), address + 1)
                address += 3

        if MiscOption.MomItems.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_MomItems"]
            for mom_item in world.generated_misc.mom_items:
                write_bytes([item_const_name_to_id(mom_item.item)], address + (8 * mom_item.index) + 7)

        if MiscOption.IcePath.value in world.generated_misc.selected:
            write_bytes([13, 3], data.rom_addresses["AP_Misc_IcePathWarp_1"])
            write_bytes([13, 13], data.rom_addresses["AP_Misc_IcePathWarp_2"])

        if MiscOption.TooManyDogs.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_TooManyDogs"] + 1)

        if MiscOption.Farfetchd.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_Farfetchd"] + 1)

        if MiscOption.DarkAreas.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_DarkAreas"] + 1)

        if MiscOption.VermilionGym.value in world.generated_misc.selected:
            write_bytes([0], data.rom_addresses["AP_Misc_VermilionGymSwitch1"] + 2)
            write_bytes([0], data.rom_addresses["AP_Misc_VermilionGymSwitch2"] + 2)
            write_bytes([1], data.rom_addresses["AP_Misc_VermilionGymTraps_1"] + 1)
            write_bytes([1], data.rom_addresses["AP_Misc_VermilionGymTraps_2"] + 1)
            write_bytes([1], data.rom_addresses["AP_Misc_VermilionGymEventReset"] + 1)

        if MiscOption.UnLuckyEgg.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_UnLuckyEgg"] + 1)
            write_bytes(convert_to_ingame_text("?"), data.rom_addresses["AP_Misc_LuckyEggDesc"] + 7)

    if world.options.randomize_music:
        for map_name, map_music in world.generated_music.maps.items():
            music_address = data.rom_addresses["AP_Music_" + map_name]
            # map music uses a single byte
            write_bytes([world.generated_music.consts[map_music].id], music_address)
        for i, music_name in enumerate(world.generated_music.encounters):
            music_address = data.rom_addresses["AP_EncounterMusic"] + i
            write_bytes([world.generated_music.consts[music_name].id], music_address)
        for script_name, script_music in world.generated_music.scripts.items():
            music_address = data.rom_addresses["AP_Music_" + script_name] + 1
            # script music is 2 bytes LE
            write_bytes(world.generated_music.consts[script_music].id.to_bytes(2, "little"), music_address)

    if world.options.better_marts and not world.options.shopsanity:
        mart_address = data.rom_addresses["Marts"]
        marts_end_address = data.rom_addresses["MartsEnd"]
        better_mart_address = data.rom_addresses["MartBetterMart"] - 0x10000
        better_mart_bytes = better_mart_address.to_bytes(2, "little")
        better_mart_indexes = [data.marts[mart].index for mart in BETTER_MART_MARTS]
        for i in range((marts_end_address - mart_address) // 2):
            if i in better_mart_indexes:
                write_bytes(better_mart_bytes, mart_address)
            mart_address += 2

    for hm in [hm for hm in world.options.remove_badge_requirement.valid_keys if not hm.startswith("_")]:
        hm_address = data.rom_addresses[f"AP_Setting_HMBadges_{hm}"] + 1
        requirement = world.options.hm_badge_requirements.value
        if hm in world.options.remove_badge_requirement:
            requirement = HMBadgeRequirements.option_no_badges
        if requirement == HMBadgeRequirements.option_regional and hm == "Fly":
            requirement = HMBadgeRequirements.option_add_kanto
        write_bytes([requirement], hm_address)

    if world.options.hm_badge_requirements.value == HMBadgeRequirements.option_regional:
        write_bytes([1], data.rom_addresses["AP_Setting_RegionalHMBadges_1"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_RegionalHMBadges_2"] + 1)

    elite_four_text = convert_to_ingame_text("{:02d}".format(world.options.elite_four_count.value))
    write_bytes([world.options.elite_four_requirement.value],
                data.rom_addresses["AP_Setting_VictoryRoadRequirement"] + 1)
    write_bytes(elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadBadges_Text"] + 1)
    write_bytes(elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadGyms_Text"] + 1)
    write_bytes(elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadJohtoBadges_Text"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_1"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_2"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_3"] + 1)

    write_bytes([world.options.radio_tower_requirement.value],
                data.rom_addresses["AP_Setting_RocketsRequirement"] + 1)
    write_bytes([world.options.radio_tower_count.value], data.rom_addresses["AP_Setting_RocketsCount"] + 1)

    for i in range(4):
        write_bytes([world.options.route_44_access_requirement.value],
                    data.rom_addresses[f"AP_Setting_Route44Requirement_{i + 1}"] + 1)
    for i in range(8):
        write_bytes([world.options.route_44_access_count.value],
                    data.rom_addresses[f"AP_Setting_Route44Count_{i + 1}"] + 1)

    mt_silver_text = convert_to_ingame_text("{:02d}".format(world.options.mt_silver_count.value))
    write_bytes([world.options.mt_silver_requirement.value],
                data.rom_addresses["AP_Setting_MtSilverRequirement_Gate"] + 1)
    write_bytes([world.options.mt_silver_requirement.value],
                data.rom_addresses["AP_Setting_MtSilverRequirement_Oak"] + 1)
    write_bytes(mt_silver_text, data.rom_addresses["AP_Setting_MtSilverBadges_Gate_Text"] + 1)
    write_bytes(mt_silver_text, data.rom_addresses["AP_Setting_MtSilverGyms_Gate_Text"] + 1)
    write_bytes(mt_silver_text, data.rom_addresses["AP_Setting_MtSilverBadges_Oak_Text"] + 1)
    write_bytes(mt_silver_text, data.rom_addresses["AP_Setting_MtSilverGyms_Oak_Text"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_1"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_2"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_1"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_2"] + 1)

    write_bytes([world.options.red_requirement.value], data.rom_addresses["AP_Setting_RedRequirement"] + 1)
    write_bytes([world.options.red_count], data.rom_addresses["AP_Setting_RedCount_1"] + 1)
    write_bytes([world.options.red_count], data.rom_addresses["AP_Setting_RedCount_2"] + 1)

    if not world.options.johto_only:
        kanto_access_become_champion = [1] if (world.options.kanto_access_requirement.value
                                               == KantoAccessRequirement.option_become_champion) else [0]
        write_bytes(kanto_access_become_champion, data.rom_addresses["AP_Setting_KantoAccess_Champion"] + 1)

        kanto_access_wake_snorlax = [1] if (world.options.kanto_access_requirement.value
                                            == KantoAccessRequirement.option_wake_snorlax) else [0]
        write_bytes(kanto_access_wake_snorlax, data.rom_addresses["AP_Setting_KantoAccess_Snorlax"] + 1)

        kanto_badges_text = convert_to_ingame_text("{:02d}".format(world.options.kanto_access_count.value))
        write_bytes([world.options.kanto_access_requirement.value],
                    data.rom_addresses["AP_SettingKantoAccess_Requirement"] + 1)
        write_bytes(kanto_badges_text, data.rom_addresses["AP_Setting_KantoAccess_Badges_Text"] + 1)
        write_bytes(kanto_badges_text, data.rom_addresses["AP_Setting_KantoAccess_Gyms_Text"] + 1)
        write_bytes([world.options.kanto_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_1"] + 1)
        write_bytes([world.options.kanto_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_2"] + 1)

    if world.options.johto_trainersanity or world.options.kanto_trainersanity:
        # prevents disabling gym trainers, among a few others
        write_bytes([1], data.rom_addresses["AP_Setting_Trainersanity"] + 2)
        # removes events from certain trainers, to prevent disabling them.
        missable_trainers = ("GruntM29", "GruntM2", "GruntF1", "GruntM16", "ScientistJed", "GruntM17", "GruntM18",
                             "GruntM19", "RocketMurkrow", "SlowpokeGrunt", "RaticateGrunt", "ScientistRoss",
                             "ScientistMitch", "RocketBaseB3FRocket")

        for trainer in missable_trainers:
            # the dw at +11 is the event flag.
            write_bytes([0xFF, 0xFF], data.rom_addresses[f"AP_Setting_Trainersanity_{trainer}"] + 11)

    for i, script in enumerate(world.generated_phone_traps):
        address = data.rom_addresses["AP_Setting_PhoneCallTrapTexts"] + (i * 0x400)
        s_bytes = script.get_script_bytes()
        # write script text
        write_bytes(s_bytes, address)
        # write script caller id
        address = data.rom_addresses["AP_Setting_SpecialCalls"] + (6 * i) + 2
        write_bytes([script.caller_id], address)

    phone_location_bytes = []
    for loc in world.generated_phone_indices:
        phone_location_bytes += list(loc.to_bytes(2, "little"))
    phone_location_address = data.rom_addresses["AP_Setting_Phone_Trap_Locations"]
    write_bytes(phone_location_bytes, phone_location_address)

    start_inventory_address = data.rom_addresses["AP_Start_Inventory"]
    start_inventory = defaultdict[str, int](int)
    for item in world.multiworld.precollected_items[world.player]:
        start_inventory[item.name] += 1

    free_fly_write = [0, 0, 0, 0]

    for item, quantity in start_inventory.items():
        if quantity == 0:
            quantity = 1
        while quantity:
            item_code = world.item_name_to_id[item]
            if item_code >= FLY_UNLOCK_OFFSET:
                fly_id = item_code - FLY_UNLOCK_OFFSET
                free_fly_write[fly_id // 8] |= (1 << (fly_id % 8))
            if item_code > 255:
                quantity = 0
                continue
            if quantity > 99:
                write_bytes([item_code, 99], start_inventory_address)
                quantity -= 99
            else:
                write_bytes([item_code, quantity], start_inventory_address)
                quantity = 0
            start_inventory_address += 2

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        free_fly_write[world.free_fly_location.id // 8] |= (1 << (world.free_fly_location.id % 8))

    write_bytes(free_fly_write, data.rom_addresses["AP_Setting_FreeFly"])

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_fly_offset = int(world.map_card_fly_location.id / 8).to_bytes(2, "little")
        map_fly_byte = 1 << (world.map_card_fly_location.id % 8)
        write_bytes([map_fly_byte], data.rom_addresses["AP_Setting_MapCardFreeFly_Byte"] + 1)
        write_bytes(map_fly_offset, data.rom_addresses["AP_Setting_MapCardFreeFly_Offset"] + 1)

    if world.options.remove_ilex_cut_tree:
        # Set cut tree tile to floor
        replace_map_tiles(patch, "IlexForest", 0, 11, [0x1])

    route_32_flag = world.options.route_32_condition.value
    write_bytes([route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_1"] + 1)
    write_bytes([route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_2"] + 1)
    write_bytes([route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_3"] + 1)

    if "North" in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute5Blocked"] + 2)
    if "East" in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute8Blocked"] + 2)
    if "South" in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute6Blocked"] + 2)
    if "West" in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute7Blocked"] + 2)

    if world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_TeaEnabled"] + 1)

    if world.options.east_west_underground.value:
        write_bytes([1], data.rom_addresses["AP_Setting_EastWestUndergroundEnabled"] + 1)

    if world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_neither,
                                                          UndergroundsRequirePower.option_east_west):
        write_bytes([1], data.rom_addresses["AP_Setting_NorthSouthUndergroundOpen"] + 2)

    if (world.options.east_west_underground.value and
            world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_neither,
                                                               UndergroundsRequirePower.option_north_south)):
        write_bytes([1], data.rom_addresses["AP_Setting_EastWestUndergroundOpen"] + 2)

    if world.options.remote_items:
        write_bytes([1], data.rom_addresses["AP_Setting_RemoteItems"])

    if world.options.require_itemfinder.value == RequireItemfinder.option_hard_required:
        write_bytes([1], data.rom_addresses["AP_Setting_ItemfinderRequired"] + 1)

    if world.options.goal.value != Goal.option_elite_four:
        write_bytes([1], data.rom_addresses["AP_Setting_SkipE4Credits"] + 1)

    if world.options.vanilla_clair:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaClair"] + 2)

    if world.options.victory_road_access:
        write_bytes([0], data.rom_addresses["AP_Setting_VictoryRoadBoulder"] + 2)

    if world.options.route_2_access.value == Route2Access.option_open:
        tiles = [0x01]  # ground
    elif world.options.route_2_access.value == Route2Access.option_ledge:
        tiles = [0x58, 0x0A]  # grass with left ledge, grass
    else:
        tiles = None

    if tiles:
        replace_map_tiles(patch, "Route2", 5, 1, tiles)

    if world.options.route_42_access.value in \
            (Route42Access.option_blocked, Route42Access.option_whirlpool_open_mortar):
        map_name = "MountMortar1FOutside"
        replace_map_tiles(patch, map_name, 9, 8, [0x1D])  # rocks above waterfall
        replace_map_tiles(patch, map_name, 9, 11, [0x37])  # cave entrance
        replace_map_tiles(patch, map_name, 8, 12, [0x25, 0x02, 0x26])  # shore
        replace_map_tiles(patch, map_name, 8, 13, [0x32, 0x27, 0x33])  # shore edge

        map_name = "MountMortar1FInside"
        replace_map_tiles(patch, map_name, 9, 23, [0x02])  # remove rocks
        replace_map_tiles(patch, map_name, 8, 24, [0x06, 0x24, 0x04])  # entrance corridor + warp tile
        replace_map_tiles(patch, map_name, 9, 25, [0x23])  # exit

    if world.options.route_42_access.value != Route42Access.option_vanilla:
        map_name = "Route42"
        replace_map_tiles(patch, map_name, 7, 3, [0x0A])  # west rock
        replace_map_tiles(patch, map_name, 8, 6, [0x3A])  # west buoys
        replace_map_tiles(patch, map_name, 8, 7, [0x34])  # west buoys
        replace_map_tiles(patch, map_name, 16, 3, [0x0A, 0x0A])  # east rocks
        if world.options.route_42_access.value == Route42Access.option_blocked:
            replace_map_tiles(patch, map_name, 8, 3, [0x38])  # west buoys
            replace_map_tiles(patch, map_name, 8, 4, [0x36])  # west buoys
            replace_map_tiles(patch, map_name, 18, 4, [0x0A])  # east rock
            replace_map_tiles(patch, map_name, 18, 3, [0x54])  # prettier shore edge
            replace_map_tiles(patch, map_name, 17, 4, [0x54])  # prettier shore edge
        else:
            replace_map_tiles(patch, map_name, 8, 4, [0x07])  # west whirlpool
            replace_map_tiles(patch, map_name, 18, 4, [0x07])  # east whirlpool

    if world.options.red_gyarados_access == RedGyaradosAccess.option_whirlpool:
        whirlpool_tile = 0x07
        rock_tile = 0x0A
        water_tile = 0x35
        map_name = "LakeOfRage"
        replace_map_tiles(patch, map_name, 8, 10, [rock_tile, whirlpool_tile, 0x39])
        replace_map_tiles(patch, map_name, 7, 11, [0x30, water_tile, water_tile, rock_tile])
        replace_map_tiles(patch, map_name, 7, 12, [0x31, whirlpool_tile, 0x3A, 0x31])
    elif world.options.red_gyarados_access == RedGyaradosAccess.option_shore:
        write_bytes([31], data.rom_addresses["AP_Setting_LakeOfRage_RED_GYARADOS"] + 1)

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        map_name = "DarkCaveVioletEntrance"
        replace_map_tiles(patch, map_name, 6, 0, [0x11, 0x10])
        replace_map_tiles(patch, map_name, 6, 1, [0x08, 0x0A])
        replace_map_tiles(patch, map_name, 6, 2, [0x0C, 0x0E, 0x27, 0x0C, 0x0D, 0x0E])
        replace_map_tiles(patch, map_name, 6, 3, [0x2D, 0x2F, 0x2C, 0x2D, 0x2E, 0x2F])
        replace_map_tiles(patch, map_name, 9, 4, [0x04, 0x06])

        map_name = "DarkCaveBlackthornEntrance"
        replace_map_tiles(patch, map_name, 2, 7, [0x02])
        replace_map_tiles(patch, map_name, 2, 8, [0x02])

    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        write_bytes([1], data.rom_addresses["AP_Setting_NationalParkBicycle"] + 2)

    if world.options.route_3_access.value == Route3Access.option_boulder_badge:
        # This is a sprite event, so 0 shows the sprite
        write_bytes([0], data.rom_addresses["AP_Setting_PewterCityBadgeRequired_1"] + 2)
        # Don't set the scene to the noop scene
        write_bytes([0], data.rom_addresses["AP_Setting_PewterCityBadgeRequired_2"] + 2)

    if world.options.mount_mortar_access:
        # This is a sprite event, so 0 shows the sprite
        write_bytes([0], data.rom_addresses["AP_Setting_MountMortarRocks"] + 2)

    headbutt_seed = (world.multiworld.seed & 0xFFFF).to_bytes(2, "little")
    write_bytes(headbutt_seed[:0], data.rom_addresses["AP_Setting_TreeMonSeed_1"] + 1)
    write_bytes(headbutt_seed[-1:], data.rom_addresses["AP_Setting_TreeMonSeed_2"] + 1)

    if world.options.randomize_starting_town:
        town_id = world.starting_town.id
        write_bytes([town_id], data.rom_addresses["AP_Setting_RandomStartTown_1"] + 1)
        write_bytes([town_id], data.rom_addresses["AP_Setting_RandomStartTown_2"] + 1)
        write_bytes([town_id], data.rom_addresses["AP_Setting_RandomStartTown_3"] + 1)
        write_bytes([town_id], data.rom_addresses["AP_Setting_RandomStartTown_4"] + 1)

    if world.options.randomize_starting_town or world.options.dexsanity or world.options.dexcountsanity:
        write_bytes([1], data.rom_addresses["AP_Setting_StartWithPokedex_1"] + 2)
        write_bytes([1], data.rom_addresses["AP_Setting_StartWithPokedex_2"] + 2)

    if world.options.metronome_only:
        for i in range(4):
            write_bytes([1], data.rom_addresses[f"AP_Setting_MetronomeOnly_{i + 1}"] + 1)

    if world.options.randomize_fly_unlocks:
        write_bytes([1], data.rom_addresses["AP_Setting_FlyUnlocksShuffled"] + 2)

    if world.options.enforce_wild_encounter_methods_logic:
        valid_methods = [key for key in WildEncounterMethodsRequired.valid_keys if
                         not key.startswith("_") and key != "Bug Catching Contest"]
        assert len(valid_methods) == 5
        methods = [method in world.options.wild_encounter_methods_required.value for method in valid_methods]

        write_bytes(methods, data.rom_addresses["AP_Setting_AllowedCatchTypes"])

    if world.options.fly_cheese == FlyCheese.option_disallow:
        write_bytes([1], data.rom_addresses["AP_Setting_FlyCheeseDisabled"] + 2)
        write_bytes([1], data.rom_addresses["AP_Setting_FlyCheeseDisabled_2"] + 2)
        write_bytes([0], data.rom_addresses["AP_Setting_FlyCheeseDisabled_3"] + 2)  # sprite flag

    if world.options.randomize_pokemon_requests:
        for pokemon_index, pokemon in enumerate(world.generated_request_pokemon[:5]):
            pokemon_id = world.generated_pokemon[pokemon].id
            for i in range(3):
                write_bytes([pokemon_id],
                            data.rom_addresses[f"AP_Setting_BillsGrandpaRequested{pokemon_index + 1}_{i + 1}"] + 1)

        requesters = ["Beverly", "Derek", "Tiffany"]
        if world.options.randomize_phone_call_items:
            for pokemon_index, pokemon in enumerate(world.generated_request_pokemon[5:]):
                pokemon_id = world.generated_pokemon[pokemon].id
                requester = requesters[pokemon_index]
                for i in range(3):
                    write_bytes([pokemon_id], data.rom_addresses[f"AP_Setting_{requester}Requested_{i + 1}"] + 1)

    if world.options.always_unlock_fly_destinations:
        write_bytes([1], data.rom_addresses["AP_Setting_FlyUnlocksQoLEnabled"] + 2)

    for map_group in [key for key in world.options.dark_areas.valid_keys if not key.startswith("_")]:
        maps = FLASH_MAP_GROUPS[map_group]
        for map in maps:
            map_data = data.maps[map]
            default_palette = map_data.palette if map_data.palette is not MapPalette.Dark else MapPalette.Nite
            resolved_palette = MapPalette.Dark if map_group in world.options.dark_areas else default_palette
            palette_byte = (map_data.phone_service << 4) | resolved_palette
            write_bytes([palette_byte], data.rom_addresses[f"AP_MapPalette_{map}"])

    if world.options.require_flash == RequireFlash.option_hard_required:
        write_bytes([1], data.rom_addresses["AP_Setting_FlashHardRequired"] + 1)

    if world.options.require_flash and ("Ilex Forest" in world.options.dark_areas):
        write_bytes([1], data.rom_addresses["AP_Setting_IlexRequiresFlash"] + 1)

    if world.options.field_moves_always_usable:
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_SetUp"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_CallMove"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_CheckTMHM"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_MustKnowFieldMove"] + 1)

    if world.options.route_12_access:
        write_bytes([0], data.rom_addresses["AP_Setting_Route12Sudowoodo"] + 2)

    if world.options.magnet_train_access:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMagnetTrain_1"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMagnetTrain_2"] + 1)

    dexcount = len(world.logic.available_pokemon)
    write_bytes([dexcount - 1], data.rom_addresses["AP_Setting_DiplomaCount"] + 1)
    write_bytes([dexcount], data.rom_addresses["AP_Setting_DiplomaCount_2"] + 1)

    for i, slot in enumerate(world.generated_contest):
        address = data.rom_addresses["AP_Setting_BugContestMons"] + (i * 4)  # contest entries are 4 bytes
        write_bytes([slot.percentage, world.generated_pokemon[slot.pokemon].id, slot.min_level, slot.max_level],
                    address)
    if world.options.randomize_bug_catching_contest:
        write_bytes([world.options.randomize_bug_catching_contest.value - 1],
                    data.rom_addresses["AP_Setting_BugContestMode"] + 1)

    for i in range(1, 5):
        write_bytes([world.options.ss_aqua_access.value],
                    data.rom_addresses[f"AP_Setting_ShipRequiresLighthouse_{i}"] + 1)

    if world.options.randomize_phone_call_items:
        write_bytes([world.options.randomize_phone_call_items.value - 1],
                    data.rom_addresses["AP_Setting_PhoneCallMode"] + 1)

    write_bytes([world.options.require_pokegear_for_phone_numbers.value],
                data.rom_addresses["AP_Setting_PhoneRequiresGear_1"] + 1)
    write_bytes([world.options.require_pokegear_for_phone_numbers.value],
                data.rom_addresses["AP_Setting_PhoneRequiresGear_2"] + 1)

    for sign, unown in world.generated_unown_signs.items():
        write_bytes([ALL_UNOWN.index(unown) + 1], data.rom_addresses[f"AP_Sign_{sign}"] + 1)

    if world.options.goal == Goal.option_unown_hunt:
        write_bytes([1], data.rom_addresses["AP_Setting_AlphPuzzlesLocked"] + 1)

    if world.options.route_30_battle:
        standing_left = 8
        standing_right = 9

        write_bytes([27, 6, standing_right], data.rom_addresses["AP_Setting_Route30Battle_Joey"] + 1)
        write_bytes([standing_left], data.rom_addresses["AP_Setting_Route30Battle_Mikey"] + 3)
        write_bytes([27, 8, standing_left], data.rom_addresses["AP_Setting_Route30Battle_MikeysMon"] + 1)
        write_bytes([27, 7, standing_right], data.rom_addresses["AP_Setting_Route30Battle_JoeysMon"] + 1)

        left = 2
        move_left = 16 | left
        right = 3
        move_right = 16 | right
        write_bytes([move_right], data.rom_addresses["AP_Setting_Route30Battle_JoeysMonAttacks1"])
        write_bytes([move_left], data.rom_addresses["AP_Setting_Route30Battle_JoeysMonAttacks2"])
        write_bytes([move_left], data.rom_addresses["AP_Setting_Route30Battle_MikeysMonAttacks1"])
        write_bytes([move_right], data.rom_addresses["AP_Setting_Route30Battle_MikeysMonAttacks2"])

        write_bytes([right], data.rom_addresses["AP_Setting_Route30Battle_JoeyTurn"] + 2)
        write_bytes([left], data.rom_addresses["AP_Setting_Route30Battle_MikeyTurn"] + 2)

    if world.options.all_pokemon_seen:
        write_bytes([1], data.rom_addresses["AP_Setting_AllPokemonSeen_1"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_AllPokemonSeen_2"] + 1)

    write_customizable_options(world.options, write_bytes, must_write_option)

    # Set slot auth
    ap_version_text = convert_to_ingame_text(data.manifest.pokemon_crystal_version)[:19]
    ap_version_text.append(0x50)
    # truncated to 19 to preserve the "v" at the beginning
    write_bytes(world.auth, data.rom_addresses["AP_Seed_Auth"])
    write_bytes(data.manifest.world_version.encode("ascii")[:32], data.rom_addresses["AP_Version"])
    write_bytes(ap_version_text, data.rom_addresses["AP_Version_Text"] + 1)

    patch.write_file("token_data.bin", patch.get_token_binary())

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_crystal_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes
