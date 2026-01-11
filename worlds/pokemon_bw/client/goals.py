
from typing import TYPE_CHECKING, Coroutine, Any, Callable

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


def get_method(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> Callable[
    ["PokemonBWClient", "BizHawkClientContext"], Coroutine[Any, Any, bool]
]:

    match ctx.slot_data["options"]["goal"]:
        case "ghetsis":
            return defeat_ghetsis
        case "champion":
            return become_champion
        case "cynthia":
            return defeat_cynthia
        case "cobalion":
            return encounter_cobalion
        # case "regional_pokedex":
        # case "national_pokedex":
        # case "custom_pokedex":
        case "tmhm_hunt":
            return verify_tms_hms
        case "seven_sages_hunt":
            return find_seven_sages
        case "legendary_hunt":
            return encounter_legendaries
        case "pokemon_master":
            return do_everything
        case _:
            client.logger.warning("Bad goal in slot data: "+ctx.slot_data["options"]["goal"])
            return error


async def defeat_ghetsis(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return client.get_flag(0x1D3)


async def become_champion(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return client.get_flag(0x1D4)


async def defeat_cynthia(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return (await client.read_var(ctx, 0xE4)) >= 2


async def encounter_cobalion(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return client.get_flag(649)


async def verify_tms_hms(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return client.get_flag(0x191)


async def find_seven_sages(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return (await client.read_var(ctx, 0xCC)) >= 6 and await defeat_ghetsis(client, ctx)


async def encounter_legendaries(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return (
        client.get_flag(649) and  # Cobalion
        client.get_flag(650) and  # Terrakion
        client.get_flag(651) and  # Virizion
        client.get_flag(801) and  # Kyurem
        client.get_flag(779) and  # Victini
        client.get_flag(810) and  # Volcarona
        client.get_flag(0x1CE)  # Reshiram/Zekrom
    )


async def do_everything(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return (
        await defeat_ghetsis(client, ctx) and
        await become_champion(client, ctx) and
        await defeat_cynthia(client, ctx) and
        await encounter_cobalion(client, ctx) and
        await verify_tms_hms(client, ctx) and
        await find_seven_sages(client, ctx) and
        await encounter_legendaries(client, ctx)
    )


async def error(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> bool:
    return False
