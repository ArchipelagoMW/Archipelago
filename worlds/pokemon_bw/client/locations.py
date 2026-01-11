from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


async def check_flag_locations(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> list[int]:

    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.flags_offset, client.flag_bytes_amount, client.ram_read_write_domain),
        )
    )
    flags_buffer = read[0]
    for eight_flags in range(client.flag_bytes_amount):
        if client.flags_cache[eight_flags] != flags_buffer[eight_flags]:
            merge = client.flags_cache[eight_flags] | flags_buffer[eight_flags]
            if client.flags_cache[eight_flags] != merge:
                for bit in range(8):
                    if merge & (2 ** bit) != 0:
                        for loc_id in client.missing_flag_loc_ids[eight_flags*8+bit]:
                            locations_to_check.append(loc_id)
            client.flags_cache[eight_flags] = merge
    return locations_to_check


async def check_dex_locations(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> list[int]:

    if not client.dexsanity_included:
        return []

    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.dex_offset, client.dex_bytes_amount, client.ram_read_write_domain),
        )
    )
    dex_buffer = read[0]
    for eight_flags in range(client.dex_bytes_amount):
        if client.dex_cache[eight_flags] != dex_buffer[eight_flags]:
            merge = client.dex_cache[eight_flags] | dex_buffer[eight_flags]
            if client.dex_cache[eight_flags] != merge:
                for bit in range(8):
                    if merge & (2 ** bit):
                        for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + bit + 1]:
                            locations_to_check.append(loc_id)
            client.dex_cache[eight_flags] = merge
    return locations_to_check
