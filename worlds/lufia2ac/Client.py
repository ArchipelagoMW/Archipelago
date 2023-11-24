import logging
import time
import typing
import uuid
from logging import Logger
from typing import Dict, List, Optional

from NetUtils import ClientStatus, NetworkItem
from worlds.AutoSNIClient import SNIClient
from .Enemies import enemy_id_to_name
from .Items import start_id as items_start_id
from .Locations import start_id as locations_start_id
from .Options import BlueChestCount

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger: Logger = logging.getLogger("SNES")

SRAM_START: int = 0xE00000
L2AC_ROMNAME_START: int = 0x007FC0
L2AC_SIGN_ADDR: int = SRAM_START + 0x2000
L2AC_GOAL_ADDR: int = SRAM_START + 0x2030
L2AC_DEATH_ADDR: int = SRAM_START + 0x203D
L2AC_TX_ADDR: int = SRAM_START + 0x2040
L2AC_RX_ADDR: int = SRAM_START + 0x2800


class L2ACSNIClient(SNIClient):
    game: str = "Lufia II Ancient Cave"

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name: Optional[bytes] = await snes_read(ctx, L2AC_ROMNAME_START, 0x15)
        if rom_name is None or rom_name[:4] != b"L2AC":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # fully remote

        ctx.rom = rom_name

        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom: Optional[bytes] = await snes_read(ctx, L2AC_ROMNAME_START, 0x15)
        if rom != ctx.rom:
            ctx.rom = None
            return

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        signature: Optional[bytes] = await snes_read(ctx, L2AC_SIGN_ADDR, 16)
        if signature != b"ArchipelagoLufia":
            return

        uuid_data: Optional[bytes] = await snes_read(ctx, L2AC_TX_ADDR + 16, 16)
        if uuid_data is None:
            return

        coop_uuid: uuid.UUID = uuid.UUID(bytes=uuid_data)
        if coop_uuid.version != 4:
            coop_uuid = uuid.uuid4()
            snes_buffered_write(ctx, L2AC_TX_ADDR + 16, coop_uuid.bytes)

        blue_chests_key: str = f"lufia2ac_blue_chests_checked_T{ctx.team}_P{ctx.slot}"
        ctx.set_notify(blue_chests_key)

        # Goal
        if not ctx.finished_game:
            goal_data: Optional[bytes] = await snes_read(ctx, L2AC_GOAL_ADDR, 10)
            if goal_data is not None and goal_data[goal_data[0]] == 0x01:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        # DeathLink TX
        death_data: Optional[bytes] = await snes_read(ctx, L2AC_DEATH_ADDR, 3)
        if death_data is not None:
            await ctx.update_death_link(bool(death_data[0]))
            if death_data[1] != 0x00:
                snes_buffered_write(ctx, L2AC_DEATH_ADDR + 1, b"\x00")
                if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                    player_name: str = ctx.player_names.get(ctx.slot, str(ctx.slot))
                    enemy_name: str = enemy_id_to_name.get(death_data[1] - 1, hex(death_data[1] - 1))
                    await ctx.send_death(f"{player_name} was totally defeated by {enemy_name}.")

        # TX
        tx_data: Optional[bytes] = await snes_read(ctx, L2AC_TX_ADDR, 12)
        if tx_data is not None:
            snes_blue_chests_checked: int = int.from_bytes(tx_data[:2], "little")
            snes_ap_items_found: int = int.from_bytes(tx_data[6:8], "little")
            snes_other_locations_checked: int = int.from_bytes(tx_data[10:12], "little")

            blue_chests_checked: Dict[str, int] = ctx.stored_data.get(blue_chests_key) or {}
            if blue_chests_checked.get(str(coop_uuid), 0) < snes_blue_chests_checked:
                blue_chests_checked[str(coop_uuid)] = snes_blue_chests_checked
                if blue_chests_key in ctx.stored_data:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": blue_chests_key,
                        "default": {},
                        "want_reply": True,
                        "operations": [{
                            "operation": "update",
                            "value": {str(coop_uuid): snes_blue_chests_checked},
                        }],
                    }])

            total_blue_chests_checked: int = min(sum(blue_chests_checked.values()), BlueChestCount.overall_max)
            snes_buffered_write(ctx, L2AC_TX_ADDR + 8, total_blue_chests_checked.to_bytes(2, "little"))
            location_ids: List[int] = [locations_start_id + i for i in range(total_blue_chests_checked)]

            loc_data: Optional[bytes] = await snes_read(ctx, L2AC_TX_ADDR + 32, snes_other_locations_checked * 2)
            if loc_data is not None:
                location_ids.extend(locations_start_id + int.from_bytes(loc_data[2 * i:2 * i + 2], "little")
                                    for i in range(snes_other_locations_checked))

            if new_location_ids := [loc_id for loc_id in location_ids if loc_id not in ctx.locations_checked]:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_location_ids}])
            for location_id in new_location_ids:
                ctx.locations_checked.add(location_id)
                snes_logger.info("%d/%d blue chests" % (
                    len(list(loc for loc in ctx.locations_checked if not loc & 0x100)),
                    len(list(loc for loc in ctx.missing_locations | ctx.checked_locations if not loc & 0x100))))

            client_ap_items_found: int = sum(net_item.player != ctx.slot for net_item in ctx.locations_info.values())
            if client_ap_items_found > snes_ap_items_found:
                snes_buffered_write(ctx, L2AC_TX_ADDR + 4, client_ap_items_found.to_bytes(2, "little"))

        # RX
        rx_data: Optional[bytes] = await snes_read(ctx, L2AC_RX_ADDR, 4)
        if rx_data is not None:
            snes_items_received = int.from_bytes(rx_data[:2], "little")

            if snes_items_received < len(ctx.items_received):
                item: NetworkItem = ctx.items_received[snes_items_received]
                item_code: int = item.item - items_start_id
                snes_items_received += 1

                snes_logger.info("Received %s from %s (%s) (%d/%d in list)" % (
                    ctx.item_names[item.item],
                    ctx.player_names[item.player],
                    ctx.location_names[item.location],
                    snes_items_received, len(ctx.items_received)))
                snes_buffered_write(ctx, L2AC_RX_ADDR + 2 * (snes_items_received + 1), item_code.to_bytes(2, "little"))
                snes_buffered_write(ctx, L2AC_RX_ADDR, snes_items_received.to_bytes(2, "little"))

        await snes_flush_writes(ctx)

    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes

        # DeathLink RX
        if "DeathLink" in ctx.tags:
            snes_buffered_write(ctx, L2AC_DEATH_ADDR + 2, b"\x01")
        else:
            snes_buffered_write(ctx, L2AC_DEATH_ADDR + 2, b"\x00")
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
