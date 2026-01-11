from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


async def early_setup(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:
    from .goals import get_method

    client.goal_checking_method = get_method(client, ctx)

    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.data_address_address, 3, client.ram_read_write_domain),
        )
    )
    client.save_data_address = int.from_bytes(read[0], "little")

    if ctx.slot_data["options"]["dexsanity"] == 0:
        client.dexsanity_included = False


async def late_setup(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:
    from ..data.items import seasons
    from .items import reload_key_items

    await reload_key_items(client, ctx)

    if ctx.slot_data["options"]["goal"] not in ("tmhm_hunt", "pokemon_master"):
        await client.write_set_flag(ctx, 0x192)
    else:
        await client.write_unset_flag(ctx, 0x192)

    if ctx.slot_data["options"]["season_control"] == "vanilla":
        await client.write_set_flag(ctx, 0x193)
    else:
        await client.write_unset_flag(ctx, 0x193)
        if ctx.slot_data["options"]["season_control"] == "randomized":
            for network_item in ctx.items_received:
                name = ctx.item_names.lookup_in_game(network_item.item)
                if name in seasons.table:
                    await client.write_var(ctx, 0xC1, seasons.table[name].var_value)
                    break

    master_ball_cost: int = ctx.slot_data["master_ball_seller_cost"]
    seller_modifiers = [mod.casefold() for mod in ctx.slot_data["options"]["master_ball_seller"]]
    await client.write_var(ctx, 0xF2, master_ball_cost)
    if "ns castle" in seller_modifiers:
        await client.write_set_flag(ctx, 0x1CF)
    else:
        await client.write_unset_flag(ctx, 0x1CF)
    if "pc" in seller_modifiers:
        await client.write_set_flag(ctx, 0x1D1)
    else:
        await client.write_unset_flag(ctx, 0x1D1)
    if "cherens mom" in seller_modifiers:
        await client.write_set_flag(ctx, 0x1D2)
    else:
        await client.write_unset_flag(ctx, 0x1D2)
    if "undella mansion seller" in seller_modifiers:
        await client.write_set_flag(ctx, 0x1D0)
    else:
        await client.write_unset_flag(ctx, 0x1D0)
