from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from ..tracker import should_change

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


async def set_map(client: "PokemonBWClient", ctx: "BizHawkClientContext"):

    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.map_id_offset, 2, client.ram_read_write_domain),
        )
    )
    map_id = int.from_bytes(read[0], "little")
    if 107 <= map_id <= 112 or 120 <= map_id <= 135:
        map_id += (client.game_version << 10)

    if map_id != client.current_map:
        client.current_map = map_id
        if should_change(map_id):
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_bw_map_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{
                    "operation": "replace",
                    "value": map_id,
                }],
            }])


async def set_goal_bitmap(client: "PokemonBWClient", ctx: "BizHawkClientContext"):

    bitmap = 0
    if client.get_flag(0x1D6):  # N
        bitmap |= 1
    if client.get_flag(0x1D3):  # Ghetsis
        bitmap |= 2
    if client.get_flag(0xE4):  # Cynthia
        bitmap |= 4
    if client.get_flag(705):  # Sage Giallo
        bitmap |= 8
    if client.get_flag(0x1B5):  # Sage Gorm
        bitmap |= 16
    if client.get_flag(0x1D5):  # Sage Zinzolin
        bitmap |= 32
    if client.get_flag(809):  # Sage Ryoku
        bitmap |= 64
    if client.get_flag(0x1D7):  # Sage Rood
        bitmap |= 128
    if client.get_flag(0x1D8):  # Sage Bronius
        bitmap |= 256
    if client.get_flag(779):  # Victini
        bitmap |= 512
    if client.get_flag(0x1CE):  # Reshiram/Zekrom
        bitmap |= 1024
    if client.get_flag(801):  # Kyurem
        bitmap |= 2048
    if client.get_flag(810):  # Volcarona
        bitmap |= 4096
    if client.get_flag(649):  # Cobalion
        bitmap |= 8192
    if client.get_flag(650):  # Terrakion
        bitmap |= 16384
    if client.get_flag(651):  # Virizion
        bitmap |= 32768
    if client.get_flag(0x1D4):  # Alder
        bitmap |= 65536
    if client.get_flag(0x191):  # TM/HM scientist
        bitmap |= 131072
    if client.get_flag(0x178):  # Gym leader Brycen
        bitmap |= 262144
    if client.get_flag(841):  # Daycare man
        bitmap |= 524288
    if bitmap != client.goal_bitmap:
        client.goal_bitmap |= bitmap
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"pokemon_bw_events_{ctx.team}_{ctx.slot}",
            "default": 0,
            "want_reply": False,
            "operations": [
                {
                    "operation": "default",
                    "value": 0,
                }, {
                    "operation": "or",
                    "value": bitmap,
                }
            ]
        }])


async def set_dex_caught_seen(client: "PokemonBWClient", ctx: "BizHawkClientContext"):

    packages = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.dex_offset, client.dex_bytes_amount, client.ram_read_write_domain),
            (client.save_data_address + client.dex_seen_offset, client.dex_bytes_amount, client.ram_read_write_domain),
        )
    )
    if read[0] != client.tracker_caught_cache:
        caught = [i for i in range(1, 650) if read[0][(i-1)//8] & (2 ** ((i-1) % 8)) > 0]
        for eight_flags in range(len(read[0])):
            client.tracker_caught_cache[eight_flags] |= read[0][eight_flags]
        packages.append({
            "cmd": "Set",
            "key": f"pokemon_bw_caught_{ctx.team}_{ctx.slot}",
            "default": [],
            "want_reply": False,
            "operations": [
                {
                    "operation": "default",
                    "value": [],
                }, {
                    "operation": "update",
                    "value": caught,
                }
            ]
        })
    if read[1] != client.tracker_seen_cache:
        seen = [i for i in range(1, 650) if read[1][(i-1)//8] & (2 ** ((i-1) % 8)) > 0]
        for eight_flags in range(len(read[1])):
            client.tracker_seen_cache[eight_flags] |= read[1][eight_flags]
        packages.append({
            "cmd": "Set",
            "key": f"pokemon_bw_seen_{ctx.team}_{ctx.slot}",
            "default": [],
            "want_reply": False,
            "operations": [
                {
                    "operation": "default",
                    "value": [],
                }, {
                    "operation": "update",
                    "value": seen,
                }
            ]
        })
    if packages:
        await ctx.send_msgs(packages)

