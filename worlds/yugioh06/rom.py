import hashlib
import math
import os
import struct

from settings import get_settings

import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from worlds.AutoWorld import World
from .items import item_to_index
from .rom_values import banlist_ids, function_addresses, structure_deck_selection

MD5Europe = "020411d3b08f5639eb8cb878283f84bf"
MD5America = "b8a7c976b28172995fe9e465d654297a"


class YGO06ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Yu-Gi-Oh! 2006"
    hash = MD5America
    patch_file_ending = ".apygo06"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def write_tokens(world: World, patch: YGO06ProcedurePatch):
    structure_deck = structure_deck_selection.get(world.options.structure_deck.value)
    # set structure deck
    patch.write_token(APTokenTypes.WRITE, 0x000FD0AA, struct.pack("<B", structure_deck))
    # set banlist
    banlist = world.options.banlist
    patch.write_token(APTokenTypes.WRITE, 0xF4496, struct.pack("<B", banlist_ids.get(banlist.value)))
    # set items to locations map
    randomizer_data_start = 0x0000F310
    for location in world.multiworld.get_locations(world.player):
        item = location.item.name
        if location.item.player != world.player:
            item = "Remote"
        item_id = item_to_index.get(item)
        if item_id is None:
            continue
        location_id = world.location_name_to_id[location.name] - 5730000
        patch.write_token(APTokenTypes.WRITE, randomizer_data_start + location_id, struct.pack("<B", item_id))
    # set starting inventory
    inventory_map = [0 for i in range(32)]
    starting_inventory = list(map(lambda i: i.name, world.multiworld.precollected_items[world.player]))
    starting_inventory += world.options.start_inventory.value
    for start_inventory in starting_inventory:
        item_id = world.item_name_to_id[start_inventory] - 5730001
        index = math.floor(item_id / 8)
        bit = item_id % 8
        inventory_map[index] = inventory_map[index] | (1 << bit)
    for i in range(32):
        patch.write_token(APTokenTypes.WRITE, 0xE9DC + i, struct.pack("<B", inventory_map[i]))
    # set unlock conditions for the last 3 campaign opponents
    third_tier_5 = (
        world.options.third_tier_5_campaign_boss_challenges.value
        if world.options.third_tier_5_campaign_boss_unlock_condition.value == 1
        else world.options.third_tier_5_campaign_boss_campaign_opponents.value
    )
    patch.write_token(APTokenTypes.WRITE, 0xEEFA, struct.pack("<B", third_tier_5))

    fourth_tier_5 = (
        world.options.fourth_tier_5_campaign_boss_challenges.value
        if world.options.fourth_tier_5_campaign_boss_unlock_condition.value == 1
        else world.options.fourth_tier_5_campaign_boss_campaign_opponents.value
    )
    patch.write_token(APTokenTypes.WRITE, 0xEF10, struct.pack("<B", fourth_tier_5))
    final = (
        world.options.final_campaign_boss_challenges.value
        if world.options.final_campaign_boss_unlock_condition.value == 1
        else world.options.final_campaign_boss_campaign_opponents.value
    )
    patch.write_token(APTokenTypes.WRITE, 0xEF22, struct.pack("<B", final))

    patch.write_token(
        APTokenTypes.WRITE,
        0xEEF8,
        struct.pack(
            "<B",
            int((function_addresses.get(world.options.third_tier_5_campaign_boss_unlock_condition.value) - 0xEEFA) / 2),
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        0xEF0E,
        struct.pack(
            "<B",
            int(
                (function_addresses.get(world.options.fourth_tier_5_campaign_boss_unlock_condition.value) - 0xEF10) / 2
            ),
        ),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        0xEF20,
        struct.pack(
            "<B", int((function_addresses.get(world.options.final_campaign_boss_unlock_condition.value) - 0xEF22) / 2)
        ),
    )
    # set starting money
    patch.write_token(APTokenTypes.WRITE, 0xF4734, struct.pack("<I", world.options.starting_money))
    patch.write_token(APTokenTypes.WRITE, 0xE70C, struct.pack("<B", world.options.money_reward_multiplier.value))
    patch.write_token(APTokenTypes.WRITE, 0xE6E4, struct.pack("<B", world.options.money_reward_multiplier.value))
    # normalize booster packs if option is set
    if world.options.normalize_boosters_packs.value:
        booster_pack_price = world.options.booster_pack_prices.value.to_bytes(2, "little")
        for booster in range(51):
            space = booster * 16
            patch.write_token(APTokenTypes.WRITE, 0x1E5E2E8 + space, struct.pack("<B", booster_pack_price[0]))
            patch.write_token(APTokenTypes.WRITE, 0x1E5E2E9 + space, struct.pack("<B", booster_pack_price[1]))
            patch.write_token(APTokenTypes.WRITE, 0x1E5E2EA + space, struct.pack("<B", 5))
    # set shuffled campaign opponents if option is set
    if world.options.campaign_opponents_shuffle.value:
        i = 0
        for opp in world.campaign_opponents:
            space = i * 32
            patch.write_token(APTokenTypes.WRITE, 0x000F3BA + i, struct.pack("<B", opp.id))
            patch.write_token(APTokenTypes.WRITE, 0x1E58D0E + space, struct.pack("<H", opp.card_id))
            patch.write_token(APTokenTypes.WRITE, 0x1E58D10 + space, struct.pack("<H", opp.deck_name_id))
            for j, b in enumerate(opp.deck_file.encode("ascii")):
                patch.write_token(APTokenTypes.WRITE, 0x1E58D12 + space + j, struct.pack("<B", b))
            i = i + 1

    for j, b in enumerate(world.romName):
        patch.write_token(APTokenTypes.WRITE, 0x10 + j, struct.pack("<B", b))
    for j, b in enumerate(world.playerName):
        patch.write_token(APTokenTypes.WRITE, 0x30 + j, struct.pack("<B", b))

    patch.write_file("token_data.bin", patch.get_token_binary())


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        md5hash = basemd5.hexdigest()
        if MD5Europe != md5hash and MD5America != md5hash:
            raise Exception(
                "Supplied Base Rom does not match known MD5 for "
                "Yu-Gi-Oh! World Championship 2006 America or Europe "
                "Get the correct game and version, then dump it"
            )
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings().yugioh06_settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
