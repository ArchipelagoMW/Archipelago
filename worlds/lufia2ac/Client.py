import logging
import time
import typing
from logging import Logger
from typing import Optional

from NetUtils import ClientStatus, NetworkItem
from worlds.AutoSNIClient import SNIClient
from .Enemies import enemy_id_to_name
from .Items import start_id as items_start_id
from .Locations import start_id as locations_start_id

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
        tx_data: Optional[bytes] = await snes_read(ctx, L2AC_TX_ADDR, 8)
        if tx_data is not None:
            snes_items_sent = int.from_bytes(tx_data[:2], "little")
            client_items_sent = int.from_bytes(tx_data[2:4], "little")
            client_ap_items_found = int.from_bytes(tx_data[4:6], "little")

            if client_items_sent < snes_items_sent:
                location_id: int = locations_start_id + client_items_sent
                location: str = ctx.location_names[location_id]
                client_items_sent += 1

                ctx.locations_checked.add(location_id)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

                snes_logger.info("New Check: %s (%d/%d)" % (
                    location,
                    len(ctx.locations_checked),
                    len(ctx.missing_locations) + len(ctx.checked_locations)))
                snes_buffered_write(ctx, L2AC_TX_ADDR + 2, client_items_sent.to_bytes(2, "little"))

            ap_items_found: int = sum(net_item.player != ctx.slot for net_item in ctx.locations_info.values())
            if client_ap_items_found < ap_items_found:
                snes_buffered_write(ctx, L2AC_TX_ADDR + 4, ap_items_found.to_bytes(2, "little"))

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
